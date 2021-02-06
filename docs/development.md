# Development

## Docker

We dockerize the webservice to make it available to services like ECS (Elastic Container Service) and Kubernetes.
Dockerizing an application (or anything really) also helps with build consistency as docker is a silo-ed environment
that should be identical between whatever machine you are running on. Couple of caveats to that, but none you are likely
to ever run in to with general development.

## Flask RESTPlus

[Flask RESTPlus](https://flask-restplus.readthedocs.io/en/stable/) is an extension to Flask that makes building a
webservice as easy as possible. It builds in Swagger to your webservice as well, which makes documentation of your API
implicit to your implementation.

## Gunicorn

[Gunicorn](https://gunicorn.org/) is a WSGI server to be used for python applications. We use Gunicorn to act as a proxy
that accepts webrequests, then passes them to a running instance of our python webserver. Gunicorn boots a number of
workers (specified by us) which then can accept the web requests.