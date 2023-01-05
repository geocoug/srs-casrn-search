import os
from typing import Generator

import pytest
import requests

from casrn_search import (
    casrn_search,
    clparser,
    read_csv,
    send_request,
    validate_args,
    write_csv,
)

TEST_INPUT_FILE = "chemicals.csv"
TEST_OUTPUT_FILE = "srs_chemicals.csv"


@pytest.fixture(autouse=True)
def cleanup():
    """Fixture to execute asserts before and after a test is run."""
    # Before test
    yield
    # After test
    if os.path.exists(TEST_OUTPUT_FILE):
        os.remove(TEST_OUTPUT_FILE)


def test_clparser():
    parser = clparser()
    args = parser.parse_args(["-v", "-s", "foo.csv", "bar.csv"])
    assert args.synonyms
    assert args.input_file == "foo.csv"
    args = parser.parse_args(["-s", "foo.csv", "bar.csv"])
    assert not args.verbose
    with pytest.raises(SystemExit):
        args = parser.parse_args(["bar.csv"])


def test_validate_args():
    parser = clparser()
    args = parser.parse_args(["foo.csv", "bar.csv"])
    with pytest.raises(FileNotFoundError):
        validate_args(args)
    args = parser.parse_args(["requirements.txt", "bar"])
    with pytest.raises(Exception):
        validate_args(args)
    args = parser.parse_args(["chemicals.csv", "bar"])
    with pytest.raises(Exception):
        validate_args(args)


def test_read_csv():
    rows = read_csv(TEST_INPUT_FILE)
    assert isinstance(rows, Generator)
    assert next(rows)[0] == "cas_rn"
    assert next(rows)[0] == "23811941"


def test_write_csv():
    write_csv(file=TEST_OUTPUT_FILE, row=["column1", "column2"], mode="w")
    rows = read_csv(TEST_OUTPUT_FILE)
    assert next(rows)[1] == "column2"
    write_csv(file=TEST_OUTPUT_FILE, row=["foo", "bar"], mode="a")
    rows = read_csv(TEST_OUTPUT_FILE)
    next(rows)
    assert next(rows)[1] == "bar"


def test_send_bad_request():
    url = (
        "https://cdxnodengn.epa.gov/cdx-srs-rest/substance/cas/abcdefg?qualifier=exact"
    )
    with pytest.raises(requests.exceptions.RequestException):
        send_request(url)


def test_send_good_request():
    url = "https://cdxnodengn.epa.gov/cdx-srs-rest/substance/cas/66251?qualifier=exact"
    assert send_request(url).ok


def test_casrn_search_no_synonyms():
    casrn_search(TEST_INPUT_FILE, TEST_OUTPUT_FILE)
    rows = read_csv(TEST_OUTPUT_FILE)
    assert next(rows)[-1] == "currentCasNumber"


def test_casrn_search_with_synonyms():
    casrn_search(TEST_INPUT_FILE, TEST_OUTPUT_FILE, synonyms=True)
    rows = read_csv(TEST_OUTPUT_FILE)
    assert next(rows)[-1] == "synonyms"
    next(rows)
    next(rows)
    assert len(next(rows)[-1]) > 0


def test_all_codes_searched():
    casrn_search(TEST_INPUT_FILE, TEST_OUTPUT_FILE)
    with open(TEST_INPUT_FILE) as infile:
        num_inputs = len(infile.readlines())
    with open(TEST_OUTPUT_FILE) as outfile:
        num_outputs = len(outfile.readlines())
    assert num_inputs == num_outputs


if __name__ == "__main__":
    pytest.main()
