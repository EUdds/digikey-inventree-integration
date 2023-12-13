# Digikey-Inventree-Integration

## Setup

### Installation

#### Install from Pypi

`pip install inventree_digikey_integration`

#### Install from source

1. Install [poetry](https://python-poetry.org/docs/#installation)
2. Clone the repo `git clone git@github.com:EUdds/digikey-inventree-integration.git`
3. `cd digikey-inventree-integration`
4. `poetry install`

### Configuration

Create a config.ini file according to the template and specify it's location with the `-c <path>` flag

```
[DIGIKEY_API]
CLIENT_ID=
CLIENT_SECRET=

[INVENTREE_API]
URL=<URL to the inventree instance>
USER=
PASSWORD=
```


## Usage

Invoke the cli by running `import_digikey_parts`

```bash
usage: import_digikey_parts [-h] [-y] [-c CONFIG] query_numbers [query_numbers ...]

Import Digikey part numbers into InvenTree

positional arguments:
  query_numbers         Part number(s) to import

optional arguments:
  -h, --help            show this help message and exit
  -y, --yes             Bypass user prompts and assume "yes"
  -c CONFIG, --config CONFIG
                        Path to config file
```

## Testing

Run the test suite by running `poetry run pytest`