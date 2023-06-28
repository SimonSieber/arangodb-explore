#!/bin/bash

CUR_DATE=$(date +%Y-%m-%d)

# Prepare environment
shopt -s expand_aliases
source $(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/env.sh
source ${PROJECT_HOME}/.env

docker-compose -f ${PROJECT_HOME}/docker-compose.yaml exec -T arangodb arangodump \
 --output-directory /backups/${CUR_DATE} \
 --server.username ${ARANGO_USERNAME} \
 --server.password ${ARANGO_PASSWORD} \
 --server.database NetZeroNet \
 --overwrite true
