"""
Module used to define the status endpoint for our flask app.
"""

from flask_restplus import Resource, Namespace


NAMESPACE = Namespace('status', description='Operations Related to Application Status')


@NAMESPACE.route('')
@NAMESPACE.response(404, 'Job not found.')
class Status(Resource):
    """
    Endpoint used to get status information about the flask app. i.e. running/healthy.
    """

    def get(self):
        """
        Returns our health status.
        """
        try:
            status_info = {
                "Running": True,
            }
        except Exception as error:
            return 400, str(error)
        return status_info, 200
