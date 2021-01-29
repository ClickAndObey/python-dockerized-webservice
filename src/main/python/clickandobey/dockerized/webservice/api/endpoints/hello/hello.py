"""
Module used to define the trade machine endpoint for our flask app.
"""


from clickandobey.dockerized.webservice.metrics.metrics_collector import MetricsTimer
from flask_restplus import Resource, Namespace

NAMESPACE = Namespace('hello', description='Hello World API')


@NAMESPACE.route('')
@NAMESPACE.response(404, 'Job not found.')
class HELLO(Resource):
    """
    Endpoint used to handle hello.
    """

    def get(self):
        """
        Return hello world information.
        """
        try:
            with MetricsTimer("Hello World Timer"):
                return {"hello": "world"}, 200

        except Exception as error:
            return 400, str(error)
