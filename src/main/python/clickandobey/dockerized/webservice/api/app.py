"""
Module used to define the flask application used for running the webservice.
"""

import logging
from flask import Blueprint, Flask
from flask_cors import CORS
from flask_restplus import Api

from clickandobey.dockerized.webservice.api.endpoints.admin.configuration import NAMESPACE as CONFIGURATION_NAMESPACE
from clickandobey.dockerized.webservice.api.endpoints.admin.status import NAMESPACE as STATUS_NAMESPACE
from clickandobey.dockerized.webservice.api.endpoints.hello.hello import NAMESPACE as HELLO_NAMESPACE
from clickandobey.dockerized.webservice.api.logger import LOGGER
from clickandobey.dockerized.webservice.configuration.webservice_configuration import get_configuration
from clickandobey.dockerized.webservice.metrics.metrics_collector import initialize_metrics_collector


def __create_admin_api(flask_app: Flask) -> None:
    api = Api(version=get_configuration().version,
              title='Webservice - Admin',
              description='Administrative tasks for the Webservice.')

    @api.errorhandler
    # pylint: disable=unused-argument
    # pylint: disable=unused-variable
    def default_error_handler(exception):
        """
        Error handler for the Restplus API.
        """
        return

    blueprint = Blueprint('admin', __name__)
    api.init_app(blueprint)
    api.add_namespace(CONFIGURATION_NAMESPACE)
    api.add_namespace(STATUS_NAMESPACE)
    flask_app.register_blueprint(blueprint, url_prefix='/admin')


def __create_hello_world_api(flask_app: Flask) -> None:
    api = Api(version=get_configuration().version,
              title='Webservice - Hello World',
              description='Hello World Endpoints for the Webservice.')

    @api.errorhandler
    # pylint: disable=unused-argument
    # pylint: disable=unused-variable
    def default_error_handler(exception):
        """
        Error handler for the Restplus API.
        """
        return

    blueprint = Blueprint('hello', __name__)
    api.init_app(blueprint)
    api.add_namespace(HELLO_NAMESPACE)
    flask_app.register_blueprint(blueprint, url_prefix='')


def create_flask_app(logger: logging.Logger) -> Flask:
    """
    Create our flask app and return it.
    """
    logger.info("Creating Webservice...")
    flask_app = Flask(__name__)
    CORS(flask_app)

    # Register our endpoints.
    __create_admin_api(flask_app)
    __create_hello_world_api(flask_app)
    initialize_metrics_collector(logger=LOGGER)

    # Make sure to setup the app with our intended logging mechanism.
    for handler in logger.handlers:
        flask_app.logger.addHandler(handler)
    flask_app.logger.setLevel(logger.level)

    logger.info("Webservice created.")
    return flask_app


API = create_flask_app(LOGGER)
