#!/bin/bash

# Script for running the api locally with docker-compose

# Change to script dir
cd $(dirname ${BASH_SOURCE[0]})

# Setup poetry and install dependencies
curl -sSL https://install.python-poetry.org | python3 -
export PATH="$POETRY_HOME/bin:$VENV_PATH/bin:$PATH"
poetry install --no-root -vvv --sync

# activate the env
source $(poetry env info --path)/bin/activate

# Start app
poetry run fastapi dev --host 0.0.0.0 --port 3000 src/sample_api/main.py 