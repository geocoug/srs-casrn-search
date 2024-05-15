#!/usr/bin/env python

import argparse
import logging
import os
import re
import sys

import pandas as pd
import requests

__version__ = "0.1.2"
__vdate = "2024-04-02"

BASE_URL = "https://cdxapps.epa.gov/oms-substance-registry-services/rest-api/substance/cas"

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
formatter = logging.Formatter("%(message)s")
stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter)


def clparser() -> argparse.ArgumentParser:
    """Create a parser to handle input arguments and displaying.
    a script specific help message.
    """
    desc_msg = f"""Search the EPA Substance Registry Service (SRS)
    for matching substances based on CAS RN and display results as a markdown table in the terminal.\nVersion {__version__}, {__vdate}"""  # noqa E501
    parser = argparse.ArgumentParser(description=desc_msg)
    parser.add_argument(
        "cas_rn",
        nargs="+",
        help="""CAS RN or list of CAS RN to search in the EPA Substance Registry Service (SRS).""",
    )
    parser.add_argument(
        "-s",
        "--synonyms",
        action="store_true",
        help="Include chemical synonyms.",
    )
    parser.add_argument(
        "-f",
        "--file",
        action="store_true",
        help="Output results to a CSV file instead of the terminal.",
    )
    parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        help="Control the amount of information to display.",
    )
    return parser


def send_request(url: str) -> requests.Response | None:
    """Send an HTTP GET request.

    Args:
    ----
        url (str): Request endpoint.

    Raises:
    ------
        requests.RequestException: Response errors.

    Returns:
    -------
        requests.Response: HTTP response.

    """
    try:
        response = requests.get(url, timeout=5)
    except requests.RequestException as err:
        logger.warning(err)
        return None
    if not response.ok:
        return None
    return response


def casrn_search(
    cas_rn_list: list,
    synonyms: bool = False,
    write_file: bool = False,
) -> None:
    """Query EPA SRS for a list of CAS RN and write results to the terminal or a CSV.

    The output table contains a column for the provided CAS RN, plus the following:
    'systematicName', 'epaName', and 'currentCasNumber'.

    Args:
    ----
        cas_rn (list): List of CAS RN to search.
        synonyms (bool): Include chemical synonyms.
        write_file (bool): Write results to a CSV file.
        verbose (bool): Control the amount of information to display.

    """
    logger.info(f"{os.path.basename(__file__)}, {__version__}, {__vdate}\n")
    logger.info("Querying CAS Record Numbers:")
    header = ["cas_rn", "systematicName", "epaName", "currentCasNumber"]
    if synonyms:
        header.append("synonyms")
    df = pd.DataFrame(columns=header)
    for idx, cas_rn in enumerate(cas_rn_list):
        cas_rn = re.sub(r"[^a-zA-Z0-9-]", "", cas_rn)
        url = f"{BASE_URL}/{cas_rn}?qualifier=exact"
        logger.info(
            f"{str(idx + 1).zfill(len(str(len(cas_rn_list))))}/{len(cas_rn_list)}: {cas_rn}",
        )
        response = send_request(url)
        if response:
            response = response.json()
            if len(response) == 0:
                df.loc[idx] = [cas_rn] + [None] * (len(header) - 1)
            else:
                if synonyms:
                    df.loc[idx] = [
                        cas_rn,
                        response[0]["systematicName"],
                        response[0]["epaName"],
                        response[0]["currentCasNumber"],
                        ";".join([s["synonymName"] for s in response[0]["synonyms"]]),
                    ]
                else:
                    df.loc[idx] = [
                        cas_rn,
                        response[0]["systematicName"],
                        response[0]["epaName"],
                        response[0]["currentCasNumber"],
                    ]
        else:
            df.loc[idx] = [cas_rn] + [None] * (len(header) - 1)
    df = df.sort_values(by=["currentCasNumber", "cas_rn"]).reset_index(drop=True)
    if write_file:
        df.to_csv("casrn_search.csv", index=False)
        logger.info("\nResults written to 'casrn_search.csv'.")
    else:
        logger.info("\nResults:")
        sys.stdout.write(f"{df.to_markdown(index=False, tablefmt='github')}\n")
        sys.stdout.flush()


if __name__ == "__main__":
    args = clparser().parse_args()
    if args.verbose:
        logger.addHandler(stream_handler)
    casrn_search(
        cas_rn_list=args.cas_rn,
        synonyms=args.synonyms,
        write_file=args.file,
    )
