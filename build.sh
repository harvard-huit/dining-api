#!/bin/bash

docker build -t dining-api .
docker tag dining-api artifactory.huit.harvard.edu/aais-docker-local/dining-api:latest

if [[ -z "${ARTIFACTORY_USER}" || -z "${ARTIFACTORY_PWD}" ]]; then
    docker login artifactory.huit.harvard.edu
else
    docker login artifactory.huit.harvard.edu --username "${ARTIFACTORY_USER}" --password "${ARTIFACTORY_PWD}"
fi

docker push artifactory.huit.harvard.edu/aais-docker-local/dining-api:latest