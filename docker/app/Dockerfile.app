FROM python:3.9-slim as build-base

ARG VERSION

COPY dist/ /dist/
RUN pip3 install /dist/clickandobey.dockerized.webservice-${VERSION}-py3-none-any.whl

FROM python:3.9-slim

ENV VERSION=1.0.0
ENV PYTHON_VERSION=3.9
ENV APP_NAME=webservice

WORKDIR /${APP_NAME}

# Gunicorn for handling multiple requests at a time
RUN apt-get update
RUN apt-get install -y gunicorn --no-install-recommends

# Use the wrapper script to start everything in Gunicorn.
RUN mkdir -p /${APP_NAME}/flask-metrics
COPY docker/app/run_webservice.sh /${APP_NAME}/run_webservice.sh

COPY configuration /configuration
COPY --from=build-base /usr/local/lib/python${PYTHON_VERSION}/site-packages/ /usr/local/lib/python${PYTHON_VERSION}/site-packages/
COPY --from=build-base /usr/local/bin/ /usr/local/bin/

ENTRYPOINT ["sh", "-c", "/${APP_NAME}/run_webservice.sh"]