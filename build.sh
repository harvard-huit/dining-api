#!/bin/bash

docker build -t dining-api .
docker tag dining-api artifactory.huit.harvard.edu/aais-docker-local/dining-api:latest
docker login artifactory.huit.harvard.edu
docker push artifactory.huit.harvard.edu/aais-docker-local/dining-api:latest