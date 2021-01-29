"""
Module used to test the base configuration class.
"""

import os
import pytest

from clickandobey.dockerized.webservice.configuration.webservice_configuration import WebserviceConfiguration


@pytest.mark.unit
@pytest.mark.WebserviceConfiguration
class TestWebserviceConfiguration:
    """
    Class used to test the WebserviceConfiguration class.
    """

    @staticmethod
    def __clean_env_vars() -> None:
        """
        Clean out environment variables between test runs.
        """
        for variable in [
                "ENVIRONMENT",
                "USER",
                "VERSION",
        ]:
            if os.getenv(variable) is not None:
                del os.environ[variable]

    def test_configuration(self):
        """
        Test to ensure the configuration works as expected.
        """
        configuration = WebserviceConfiguration("1.0.0", "env", {"foo": "bar"})
        assert configuration.version == "1.0.0", "Failed to get the right configuration version."
        assert configuration.environment == "env", "Failed to get the right configuration environment."
        assert configuration.config == {"foo": "bar"}, "Failed to get the right configuration config."
        expected_dict = {
            "Version": "1.0.0",
            "Environment": "env",
            "Configuration": {
                "foo": "bar"
            }
        }
        assert configuration.to_dict() == expected_dict, "Failed to match the expected dictionary output for the config"

        self.__clean_env_vars()
        os.environ["USER"] = "test"

        configuration = WebserviceConfiguration()
        assert configuration.version == "1.0.test", "Failed to get the right configuration version."
        assert configuration.environment == "localhost", "Failed to get the right configuration environment."
        assert configuration.config == {}, "Failed to get the right configuration config."
        expected_dict = {
            "Version": "1.0.test",
            "Environment": "localhost",
            "Configuration": {}
        }
        assert configuration.to_dict() == expected_dict, "Failed to match the expected dictionary output for the config"

        self.__clean_env_vars()
        os.environ["ENVIRONMENT"] = "configTest"
        os.environ["VERSION"] = "1.2.3"

        configuration = WebserviceConfiguration()
        assert configuration.version == "1.2.3", "Failed to get the right configuration version."
        assert configuration.environment == "configTest", "Failed to get the right configuration environment."
        assert configuration.config == {}, "Failed to get the right configuration config."
        expected_dict = {
            "Version": "1.2.3",
            "Environment": "configTest",
            "Configuration": {}
        }
        assert configuration.to_dict() == expected_dict, "Failed to match the expected dictionary output for the config"
