#!/usr/bin/env sh

echo "Running The Webservice..."
/usr/local/bin/gunicorn --bind 0.0.0.0:9001 --workers 1 --worker-class gevent clickandobey.dockerized.webservice.api.app:API
echo "The Webservice has finished."