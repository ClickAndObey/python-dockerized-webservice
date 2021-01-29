"""
Module used to define the base application configuration.
"""

import logging
import os
import yaml

from typing import Any, Dict, Optional


class WebserviceConfiguration:
    """
    Class used to define the base Configuration.
    """

    __CONFIGURATION_DIRECTORY_ENV_VARIABLE = "CONFIGURATION_DIRECTORY"
    __ENVIRONMENT_ENV_VARIABLE = "ENVIRONMENT"
    __USER_ENV_VARIABLE = "USER"
    __VERSION_ENV_VARIABLE = "VERSION"

    __DEFAULT_ENVIRONMENT_VALUE = "localhost"

    __CONFIGURATION_KEY = "Configuration"
    __ENVIRONMENT_KEY = "Environment"
    __VERSION_KEY = "Version"

    def __init__(self,
                 version: Optional[str] = None,
                 environment: Optional[str] = None,
                 config: Optional[Dict] = None,
                 logger: Optional[logging.Logger] = None):
        logger = logger or logging.getLogger(__name__)

        self.version = version or self.__get_default_version()
        self.environment = environment or self.__get_default_environment()
        self.config = config or self.__get_config(logger)

    def __get_config(self, logger: logging.Logger) -> Dict:
        configuration_directory = os.getenv(self.__CONFIGURATION_DIRECTORY_ENV_VARIABLE, "/configuration")
        environment_configuration_file = os.path.join(configuration_directory, self.__environment, "config.yaml")
        logger.info(f"Loading configuration file {environment_configuration_file}...")
        if not os.path.exists(environment_configuration_file):
            logger.warning(f"Configuration file {environment_configuration_file} doesn't exist.")
            return {}

        with open(environment_configuration_file) as yaml_file:
            # Empty yaml returns as None, so make sure to return as at least an empty dictionary.
            config_from_yaml = yaml.load(yaml_file, Loader=yaml.FullLoader)
            logger.info(f"Loaded configuration file {environment_configuration_file}.")
            return config_from_yaml or {}

    @property
    def debug(self) -> bool:
        """
        Whether we are trying to debug the application or not.
        """
        return self.config.get("debug", False)

    @property
    def version(self) -> str:
        """
        The version of the application.
        """
        return self.__version

    @property
    def environment(self) -> str:
        """
        The environment of the application.
        """
        return self.__environment

    @property
    def config(self) -> Dict:
        """
        The complex configuration for the environment.
        """
        return self.__config

    @version.setter
    def version(self, value: str) -> None:
        if not isinstance(value, str):
            raise TypeError("Invalid type given for version. Must be of type string.")

        self.__version = value

    @environment.setter
    def environment(self, value: str) -> None:
        if not isinstance(value, str):
            raise TypeError("Invalid type given for environment. Must be of type string.")

        self.__environment = value

    @config.setter
    def config(self, value: str) -> None:
        if not isinstance(value, dict):
            raise TypeError("Invalid type given for config. Must be of type dict.")

        self.__config = value

    @staticmethod
    def __get_default_version() -> str:
        version = os.getenv(WebserviceConfiguration.__VERSION_ENV_VARIABLE, None)
        user = os.environ.get(WebserviceConfiguration.__USER_ENV_VARIABLE, 'local')
        return version if version else f"1.0.{user}"

    @staticmethod
    def __get_default_environment() -> str:
        return os.getenv(
            WebserviceConfiguration.__ENVIRONMENT_ENV_VARIABLE,
            WebserviceConfiguration.__DEFAULT_ENVIRONMENT_VALUE
        )

    def to_dict(self) -> Dict[str, Any]:
        return {
            self.__VERSION_KEY: self.version,
            self.__ENVIRONMENT_KEY: self.environment,
            self.__CONFIGURATION_KEY: self.config
        }


__CONFIGURATION: Optional[WebserviceConfiguration] = None


def get_configuration() -> WebserviceConfiguration:
    """
    Return the global configuration.
    """
    global __CONFIGURATION
    if not __CONFIGURATION:
        __CONFIGURATION = WebserviceConfiguration()

    return __CONFIGURATION
