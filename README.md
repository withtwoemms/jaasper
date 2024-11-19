# jaaspr
the Jobs as a Service, Provisioned Runtime

# Development

### Setup

The project uses [`poetry`](https://github.com/python-poetry/poetry) as its buildtool.
All dependencies can be installed with:
```
poetry install
```
There are (uninstalled) `poetry` scripts that export individual "requirements.txt" files for dependency groups defined in the "pyproject.toml" file.
An example being as follows:
```
poetry run export-api-deps
```
