"""
Module used to manage metrics handling.
"""

import logging

from typing import Optional


class Metrics:
    """
    Class used to handle metrics.
    """

    def __init__(self, logger: logging.Logger = logging.getLogger(__name__)):
        self.__logger = logger

    def publish_elapsed_time(self, metric: str, millis: int, description: Optional[str] = None) -> None:
        """
        Send an event for the stat with the given name/duration.
        """
        try:
            self.__logger.debug("%s timing of %i milliseconds (%s)", metric, millis, description)
            self.__logger.info("Implement your metrics management for timing.")
        except Exception as ex:
            self.__logger.exception("Failed to publish elapsed stat: %s", str(ex))

    def publish_count(self, metric: str, value: int, description: Optional[str] = None) -> None:
        """
        Publish a value for the given metric as a counter.
        """
        try:
            self.__logger.debug("%s count of %i (%s)", metric, value, description)
            self.__logger.info("Implement your metrics management for counts.")
        except Exception as ex:
            self.__logger.exception("Failed to publish counter metric: %s", str(ex))

    def publish_error(self, metric: str, description: Optional[str] = None) -> None:
        """
        Publish an error for the given metric as a counter.
        """
        try:
            self.__logger.debug("%s error (%s)", metric, description)
            self.__logger.info("Implement your metrics management for errors.")
        except Exception as ex:
            self.__logger.exception("Failed to publish error metric: %s", str(ex))
