#!/bin/bash

# Wrapper script to start gunicorn.
CERTPATH=/ssl

# This is the base path and is used by gunicorn.
export SCRIPT_NAME=/ats/dining

# Run gunicorn, starting "app:app", i.e. in 'app.py', find the application in 
# variable 'app'.

cd src

if [ ! -f "${CERTPATH}/cert.pem" ]
then
    echo "Could not find certificate."
fi

exec gunicorn \
	${EXTRA} --certfile=${CERTPATH}/cert.pem \
    --keyfile=${CERTPATH}/key.pem \
    --timeout=900 \
	--graceful-timeout 900 \
    --workers=2 \
    --worker-connections=10 \
	  -b 0.0.0.0:9022 \
    app:app