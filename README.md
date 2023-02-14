# srs-casrn-search

[![ci](https://github.com/geocoug/srs-casrn-search/workflows/ci/badge.svg)](https://github.com/geocoug/srs-casrn-search/actions/workflows/ci.yml)
[![pre-commit.ci status](https://results.pre-commit.ci/badge/github/geocoug/srs-casrn-search/main.svg)](https://results.pre-commit.ci/latest/github/geocoug/srs-casrn-search/main)

Query the [EPA Substance Registry Serivce](https://cdxnodengn.epa.gov/cdx-srs-rest/) using a list of [CAS Registry Numbers](https://en.wikipedia.org/wiki/CAS_Registry_Number).

## Usage

### CLI

```sh
$ python casrn_search.py --help

Search the EPA Substance Registry Service (SRS) for matching substances based on CAS RN.

positional arguments:
  input_file      CSV containing a list of CAS Registry Numbers to search. CAS Registry Numbers must be in the first column.
  output_file     Name of the output CSV file.

options:
  -h, --help      show this help message and exit
  -s, --synonyms  Include chemical synonyms.
  -v, --verbose   Control the amount of information to display.
```

### Docker

```sh
docker run -it --rm -v $(pwd):/usr/local/app $(docker build -q -t casrn_search .) python casrn_search.py -v chemicals.csv srs_chemicals.csv
```
