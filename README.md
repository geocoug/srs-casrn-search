# srs-casrn-search

[![ci/cd](https://github.com/geocoug/srs-casrn-search/workflows/ci-cd/badge.svg)](https://github.com/geocoug/srs-casrn-search/actions/workflows/ci-cd.yml)

Query the [EPA Substance Registry Service](https://cdxapps.epa.gov/oms-substance-registry-services) using a list of [CAS Registry Numbers](https://en.wikipedia.org/wiki/CAS_Registry_Number).

## Usage

### Python

```sh
$ python casrn_search.py --help

usage: casrn_search.py [-h] [-s] [-f] [-v] cas_rn [cas_rn ...]

Search the EPA Substance Registry Service (SRS) for matching substances based on CAS RN and display results as a markdown table in the terminal. Version 0.1.2, 2024-04-02

positional arguments:
  cas_rn          CAS RN or list of CAS RN to search in the EPA Substance Registry Service (SRS).

options:
  -h, --help      show this help message and exit
  -s, --synonyms  Include chemical synonyms.
  -f, --file      Output results to a CSV file instead of the terminal.
  -v, --verbose   Control the amount of information to display.
```

### Docker

#### Building from source

```sh
docker build -t casrn_search .
```

Run the container:

```sh
docker run -it --rm casrn_search --help
```

#### Using the pre-built image

```sh
docker pull ghcr.io/geocoug/srs-casrn-search:latest
```

Optionally tag the image:

```sh
docker tag ghcr.io/geocoug/srs-casrn-search:latest casrn_search
```

Run the container:

```sh
docker run -it --rm ghcr.io/geocoug/srs-casrn-search:latest --help
```

### Examples

1. Search for a list of CAS RN and output the results to the terminal:

    ```sh
    docker run -it --rm casrn_search -v 7440-66-6 7440097
    ```

    Output:

    ```txt
    casrn_search.py, 0.1.2, 2024-04-02

    Querying CAS Record Numbers:
    1/2: 7440-66-6
    2/2: 7440097

    Results:
    | cas_rn    | systematicName   | epaName   | currentCasNumber   |
    |-----------|------------------|-----------|--------------------|
    | 7440097   | Potassium        | Potassium | 7440-09-7          |
    | 7440-66-6 | Zinc             | Zinc      | 7440-66-6          |
    ```

2. Search for a list of CAS RN and output the results to a CSV file:

    > ***Note***: you must mount a directory to the container to save the file locally.

    ```sh
    docker run -v $(pwd):/app -it --rm casrn_search -v -f 7440-66-6 7440097
    ```

    Output:

    ```txt
    cas_rn,systematicName,epaName,currentCasNumber
    7440097,Potassium,Potassium,7440-09-7
    7440-66-6,Zinc,Zinc,7440-66-6
    ```
