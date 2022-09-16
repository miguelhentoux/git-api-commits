# GIT API
API to fetch public data from GitHub. This project uses the GitHub [REST API](https://docs.github.com/en/rest).

## Dependencies
- **Python**: ^3.10
- **Poetry**: 1.1.15

## Install
First install the package manager **Poetry**, follow the official documentation [here](https://python-poetry.org/docs/).

## Run
Run using Makefile: `make local/run` <br>
Run command line: `poetry run uvicorn api.main:app --reload --port=8000` <br>
APi will be avalable on: http://127.0.0.1:8000/

## API Doc
To have more information about the endpoints, access the API Documentation on http://127.0.0.1:8000/docs.