"""
Module used to define the configuration endpoint for our flask app.
"""

from flask_restplus import Resource, Namespace

from clickandobey.dockerized.webservice.configuration.webservice_configuration import get_configuration

NAMESPACE = Namespace('configuration', description='Operations Related to Application Status')


@NAMESPACE.route('')
@NAMESPACE.response(404, 'Job not found.')
class Configuration(Resource):
    """
    Class defining the configuration endpoint for our flask app.
    """

    def get(self):
        """
        Returns our configuration.
        """
        try:
            configuration_info = get_configuration()
        except Exception as error:
            return 400, str(error)
        return configuration_info.to_dict(), 200
