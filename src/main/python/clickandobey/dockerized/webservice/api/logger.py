"""
Module used to control the logger used by the app.
"""

from clickandobey.dockerized.webservice.logging.logger import create_logger
from clickandobey.dockerized.webservice.configuration.webservice_configuration import get_configuration

LOGGER = create_logger(get_configuration().debug)
