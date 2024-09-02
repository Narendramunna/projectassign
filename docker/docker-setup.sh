#!/bin/bash

ENV_BASE=docker/.env/

FLYWAY_VARS=$ENV_BASE.flyway
POSTGRES_VARS=$ENV_BASE.postgres
PYTHON_VARS=$ENV_BASE.python
SHARED_VARS=$ENV_BASE.shared

FLYWAY_VARS=$(cat ${FLYWAY_VARS})
POSTGRES_VARS=$(cat ${POSTGRES_VARS})
PYTHON_VARS=$(cat ${PYTHON_VARS})
SHARED_VARS=$(cat ${SHARED_VARS})

ENV_VARS="${FLYWAY_VARS}$'\t'${POSTGRES_VARS}$'\t'${PYTHON_VARS}$'\t'${SHARED_VARS}"

for item in $ENV_VARS; do
    if ! echo "$item" | grep -q '\${[^}]*}'; then
        export $item
    fi
done

while IFS= read -r line; do
    key=$(echo "$line" | cut -d'=' -f1)
    value=$(echo "$line" | cut -d'=' -f2-)

     if echo "$value" | grep -q '\${[^}]*}'; then
        value="${value//'$''{'}"
        value="${value//'}'}"
        eval "echo ENV $key=\$${value}"  >> "$2"
        echo "ENV $key=$value"
    else
        echo "ENV $key=$value" >> "$2"
    fi
done < "$1"