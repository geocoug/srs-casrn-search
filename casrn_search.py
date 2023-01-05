#! /usr/bin/python
# casrn_search.py

import argparse
import csv
import logging
import os
from typing import Generator

import requests

__version__ = "0.1."
__vdate = "2023-01-04"
verbose = False

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
formatter = logging.Formatter("%(message)s")
stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter)


def clparser() -> argparse.ArgumentParser:
    """Create a parser to handle input arguments and displaying.

    a script specific help message.
    """
    desc_msg = (
        """Search the EPA Substance Registry Service (SRS) for matching substances based on CAS RN.\nVersion %s, %s"""
        % (
            __version__,
            __vdate,
        )
    )
    parser = argparse.ArgumentParser(description=desc_msg)
    parser.add_argument(
        "input_file",
        help="""CSV containing a list of CAS Registry Numbers to search.
        CAS Registry Numbers must be in the first column.""",
    )
    parser.add_argument(
        "output_file",
        help="Name of the output CSV file.",
    )
    parser.add_argument(
        "-s",
        "--synonyms",
        action="store_true",
        help="Include chemical synonyms.",
    )
    parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        help="Control the amount of information to display.",
    )
    return parser


def send_request(url: str) -> requests.Response:
    """Send an HTTP GET request.

    Args:
        url (str): Request endpoint.

    Raises:
        requests.RequestException: Response errors.

    Returns:
        requests.Response: HTTP response.
    """
    try:
        response = requests.get(url)
    except requests.RequestException:
        raise
    if not response.ok:
        raise requests.RequestException(
            f"Request returned status code {response.status_code}.\nRequest: {url}",
        )
    return response


def read_csv(file: str) -> Generator:
    """Read a CSV file.

    Args:
        file (str): CSV file to read.

    Yields:
        Generator: Single record/row.
    """
    try:
        with open(file, encoding="utf-8-sig") as f:
            yield from csv.reader(f, quotechar='"')
    except Exception:
        raise


def write_csv(file: str, row: list, mode: str) -> None:
    """Write a single record to a CSV file.

    Args:
        file (str): CSV file to write to.
        row (list): Record to write.
        mode (str): Mode to open CSV file.
    """
    try:
        with open(file, mode) as f:
            writer = csv.writer(f, delimiter=",", quoting=csv.QUOTE_MINIMAL)
            writer.writerow(row)
    except Exception:
        raise


def casrn_search(incsv: str, outcsv: str, synonyms: bool = False) -> None:
    """Query EPA SRS for a list of CAS RN and write results to a CSV.

    The output CSV contains columns from the input file, plus the following:
    "systematicName", "epaName", and "currentCasNumber".

    Args:
        incsv (str): Input CSV containing CAS RN to search in the first column.
        outcsv (str): Output CSV to write results.
        synonyms (bool, optional): Include chemical synonyms in output. Defaults to False.
    """
    logger.info("Querying CAS Record Numbers:")
    num_rows = sum(1 for _ in read_csv(incsv)) - 1
    rows = read_csv(incsv)
    for idx, row in enumerate(rows):
        result = row
        header = ["systematicName", "epaName", "currentCasNumber"]
        if synonyms:
            header.append("synonyms")
        if idx == 0:
            result.extend(header)
            write_csv(file=outcsv, row=result, mode="w+")
        else:
            cas_rn = row[0].replace("-", "")
            url = f"https://cdxnodengn.epa.gov/cdx-srs-rest/substance/cas/{cas_rn}?qualifier=exact"
            if verbose:
                logger.info(f"{idx}/{num_rows} - {cas_rn}")
            response = send_request(url).json()
            if len(response) == 0:
                result.extend([None] * len(header))
            else:
                result.extend(
                    [
                        response[0]["systematicName"],
                        response[0]["epaName"],
                        response[0]["currentCasNumber"],
                    ],
                )
                if synonyms:
                    result.append(
                        ";".join([s["synonymName"] for s in response[0]["synonyms"]]),
                    )
            write_csv(file=outcsv, row=result, mode="a")


def validate_args(args: argparse.Namespace) -> None:
    """Validate input arguments.

    Args:
        args (argparse.Namespace): Script arguments.

    Raises:
        FileNotFoundError: Input file not found error.
        Exception: Input file does not have valid CSV extension.
        Exception: Output file does not have valid CSV extension.
    """
    if args.input_file:
        if not os.path.exists(args.input_file):
            raise FileNotFoundError(args.input_file)
        if not os.path.splitext(args.input_file)[-1] in [".csv"]:
            raise Exception(f"File extension not valid: {args.input_file}")

    if args.output_file:
        if not os.path.splitext(args.output_file)[-1] in [".csv"]:
            raise Exception(f"File extension not valid: {args.output_file}")


if __name__ == "__main__":
    parser = clparser()
    args = parser.parse_args()
    validate_args(args)
    verbose = args.verbose
    if verbose:
        logger.addHandler(stream_handler)
    logger.info("%s\n" % parser.description)
    casrn_search(
        incsv=args.input_file,
        outcsv=args.output_file,
        synonyms=args.synonyms,
    )
