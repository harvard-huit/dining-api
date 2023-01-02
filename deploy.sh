#!/bin/bash

APP_FOLDER="${PWD}"
AAIS_HOME=${AAIS_HOME:-${HOME}/workshop/aais-ecs-infrastructure/}
ECS_CONFIG=${HOME}/workshop/aais-services-config/aais_services_dev.yml

export OBJC_DISABLE_INITIALIZE_FORK_SAFETY=YES

cd ${AAIS_HOME}

if [ -d env ]
then
  . env/bin/activate
fi

if [ -z "${ECS_CONFIG}" ]
then
    echo "Please source an env or set ECS_CONFIG"
    exit 1
fi

STACK=$1
shift;

echo "********************************************************************************"
echo "Deploying app ${APP_FOLDER}"
echo "********************************************************************************"
PARMS=""
PARMS="${PARMS} config_file=${ECS_CONFIG}"
PARMS="${PARMS} target_app_folder=${APP_FOLDER}"
PARMS="${PARMS} $*"

ansible-playbook deploy-container.yml --extra-vars "${PARMS}" "$@" -v
# ./runDockerDeploy.sh -c ${APP_FOLDER} -s src