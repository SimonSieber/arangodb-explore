#!/bin/bash

# Prepare environment
shopt -s expand_aliases
source $(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/env.sh
source ${PROJECT_HOME}/.env

# set folder name from parameter, if set, else use latest backup
FOLDER_NAME=$1

if [ -n ${FOLDER_NAME} ]
  then
    FOLDER_NAME=$(docker-compose -f ${PROJECT_HOME}/docker-compose.yaml exec -T arangodb ls /backups -r | head -1)
fi

# try to restore if folder exists
if [ -n ${FOLDER_NAME} ]
  then
    echo "INFO: Start arangorestore with folder <${FOLDER_NAME}>."
    docker-compose -f ${PROJECT_HOME}/docker-compose.yaml exec -T arangodb arangorestore \
      --input-directory /backups/${FOLDER_NAME} \
      --server.username ${ARANGO_USERNAME} \
      --server.password ${ARANGO_PASSWORD} \
      --server.database NetZeroNet \
      --create-database true
    echo "INFO: Restored database successful!"
  else
    echo "ERROR: Please provide the backup folder as argument."
fi
