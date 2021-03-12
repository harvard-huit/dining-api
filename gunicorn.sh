#!/bin/bash

# Wrapper script to start gunicorn.

# SSL certificate files are in a different place depending upon whether we are running 
# in a container on a developer workstation, or under ECS.
# Also add --reload parameter in developer runtimes so developer can edit source code
# without restarting gunicorn. 

case "$STACK" in

	# Developer loose Python deployment.
	"")
		CERTPATH=./ssl
		EXTRA="--reload"
		;;
		
	# Developer Docker deployment.
	"DEVELOPER") 
		CERTPATH=/opt/api/src/ssl
		EXTRA="--reload"
		;;

	# ECS deployment.
	*) 
		CERTPATH=/opt/shared/ssl
		EXTRA=""
		;;
		
esac

# This is the base path and is used by gunicorn.
export SCRIPT_NAME=/ats/dining


# Run gunicorn, starting "app:app", i.e. in 'app.py', find the application in 
# variable 'app'.

cd src
exec gunicorn ${EXTRA} --certfile=${CERTPATH}/cert.pem --keyfile=${CERTPATH}/key.pem \
	-b 0.0.0.0:9022 app:app