"""
Module used to test the administrative endpoints for the api.
"""

import pytest
import requests

from clickandobey.dockerized.webservice.configuration.webservice_configuration import WebserviceConfiguration


@pytest.mark.integration
@pytest.mark.system
@pytest.mark.AdminEndpoints
class TestAdminEndpoints:
    """
    Class used to test the administrative endpoints for the api.
    """

    @pytest.fixture()
    def admin_host_url(self) -> str:
        """
        Return the admin url for the api.
        """
        environment = WebserviceConfiguration().environment
        if environment == "localhost":
            yield "http://localhost:9001"
            return
        if environment == "docker":
            yield "http://clickandobey-python-dockerized-webservice-app:9001"
            return

        raise ValueError(f"Unexpected environment value {environment}")

    def test_configuration(self, admin_host_url: str):
        """
        Test to ensure the configuration endpoint comes back as expected.
        """
        response = requests.get(f"{admin_host_url}/admin/configuration")
        response.raise_for_status()
        assert response.status_code == 200, "Failed to get the correct response code from the configuration request."

        configuration = response.json()
        assert configuration, "Failed to get a configuration."
        assert len(configuration) != 0, "Failed to find keys in the configuration dict."

    def test_status(self, admin_host_url: str):
        """
        Test to ensure the status endpoint comes back as expected.
        """
        response = requests.get(f"{admin_host_url}/admin/status")
        response.raise_for_status()
        assert response.status_code == 200, "Failed to get the correct response code from the configuration request."

        status = response.json()
        assert status["Running"], "Failed to get the correct status."
