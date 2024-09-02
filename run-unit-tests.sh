#!/bin/bash

# Change to script dir
cd $(dirname ${BASH_SOURCE[0]})

# Setup poetry and install dependencies
curl -sSL https://install.python-poetry.org | python3 -
export PATH="/root/.local/bin:$POETRY_HOME/bin:$VENV_PATH/bin:$PATH"

poetry install --no-root -v

# activate the env
source $(poetry env info --path)/bin/activate

poetry run pytest ./tests -x -o log_cli=true --disable-warnings -vvv
