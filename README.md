# srs-casrn-search

[![test](https://github.com/geocoug/srs-casrn-search/actions/workflows/test.yml/badge.svg)](https://github.com/geocoug/srs-casrn-search/actions/workflows/test.yml)
[![Docker](https://github.com/geocoug/srs-casrn-search/workflows/docker%20build/badge.svg)](https://github.com/geocoug/srs-casrn-search/actions/workflows/docker-build.yml)

Query the [EPA Substance Registry Serivce](https://cdxnodengn.epa.gov/cdx-srs-rest/) using a list of [CAS Registry Numbers](https://en.wikipedia.org/wiki/CAS_Registry_Number).

## Usage

### CLI

```sh
$ python casrn_search.py --help

Search the EPA Substance Registry Service (SRS) for matching substances based on CAS RN. Version 0.1., 2023-01-04

positional arguments:
  input_file      CSV containing a list of CAS Registry Numbers to search. CAS Registry Numbers must be in the first column.
  output_file     Name of the output CSV file.

options:
  -h, --help      show this help message and exit
  -s, --synonyms  Include chemical synonyms.
  -v, --verbose   Control the amount of information to display.
```

### Docker

#### Build the Image

```sh
docker build -t casrn_search .
```

#### Run

```sh
docker run -it --rm -v $(pwd):/usr/local/app casrn_search python casrn_search.py -v chemicals.csv srs_chemicals.csv
```
