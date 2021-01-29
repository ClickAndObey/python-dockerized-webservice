"""
Module used to manage wrapper methods for collecting metrics.
"""

import logging

from time import perf_counter
from typing import Optional, Union

from clickandobey.dockerized.webservice.metrics.metrics import Metrics


__METRICS_COLLECTOR: Optional[Metrics] = None


def initialize_metrics_collector(logger: logging.Logger = logging.getLogger(__name__)) -> None:
    """
    Initialize the metrics collector.
    """
    global __METRICS_COLLECTOR

    if __METRICS_COLLECTOR is not None:
        raise AssertionError("Metrics Collector has already been initialized.")

    __METRICS_COLLECTOR = Metrics(logger)


def _get_metrics_collector() -> Metrics:
    global __METRICS_COLLECTOR

    if __METRICS_COLLECTOR is None:
        raise AssertionError("Need to initialize the metrics collector before calling get.")

    return __METRICS_COLLECTOR


class MetricsTimer:
    """
    Timer to be used as a with statement.
    """

    def __init__(self, metric_name: str, description: str = ""):
        self.__metric_name = metric_name
        self.__description = description
        self.__start_time_seconds = None
        self.__stop_time_seconds = None

    def __enter__(self):
        self.start()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.stop()
        self.push()

    @property
    def start_time_seconds(self) -> float:
        """
        When the timer started or was said to have started.
        """
        return self.__start_time_seconds

    @property
    def stop_time_seconds(self) -> float:
        """
        When the timer stopped or was said to have stopped.
        """
        return self.__stop_time_seconds

    def start(self, start_time_seconds=None) -> None:
        """
        Start the timer.
        """
        self.__start_time_seconds = start_time_seconds or perf_counter()

    def stop(self, stop_time_seconds=None) -> None:
        """
        Stop the timer.
        """
        self.__stop_time_seconds = stop_time_seconds or perf_counter()

    def elapased_time_in_milliseconds(self) -> float:
        """
        Return the elapsed time in milliseconds. This assumes that perf_counter() is being used to determine the start
        and stop values. If either stop or start is -1 (i.e. we didn't start or stop) then return -1.
        """
        if self.stop_time_seconds is None or self.start_time_seconds is None:
            return -1

        return (self.stop_time_seconds - self.start_time_seconds) * 1000

    def push(self) -> None:
        """
        Push the elapsed time metric.
        """
        elapsed_time_in_milliseconds = self.elapased_time_in_milliseconds()
        if elapsed_time_in_milliseconds == -1:
            return

        publish_elapsed_time(
            self.__metric_name,
            elapsed_time_in_milliseconds,
            self.__description,
        )


class MetricsCounter:
    """
    Counter to be used as a with statement.
    """

    def __init__(self, metric_name: str, count: int, description: str = ""):
        self.__metric_name = metric_name
        self.__count = count
        self.__description = description
        self.__start_time_seconds = None
        self.__stop_time_seconds = None

    def __enter__(self):
        self.count()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

    def count(self) -> None:
        """
        Increment the count.
        """
        publish_count(self.__metric_name, self.__description, self.__count)


def elapsed(metric_name: str, description: str = ""):
    """
    Wrap a function with a timer and publish the timing stat.
    :param metric_name: Name of the stat to publish the timing for.
    :param description: Description for the stat.
    """
    def real_elapsed(func):
        """
        Wrapper function.
        """
        def wrapper(*args, **kwargs):
            """
            Perform the function and publish the elapsed time.
            """
            with MetricsTimer(metric_name, description):
                value = func(*args, **kwargs)
            return value
        return wrapper
    return real_elapsed


def counter(metric_name: str, description: str = "", count: int = 1):
    """
    Wrap a function with a counter and publish the counting stat.
    :param metric_name: Name of the stat to publish the count for.
    :param description: Description for the stat.
    :param count: The count to increment by.
    """
    def real_count(func):
        """
        Wrapper function.
        """
        def wrapper(*args, **kwargs):
            """
            Perform the function and publish the count.
            """
            with MetricsCounter(metric_name, count, description):
                value = func(*args, **kwargs)
            return value

        return wrapper
    return real_count


def publish_elapsed_time(stat: str, time_in_milliseconds: Union[int, float], description: str = ""):
    """
    :param stat: Name of the stat to publish the count for.
    :param time_in_milliseconds: The amount of milliseconds to push for the stat.
    :param description: Description for the stat.
    """
    _get_metrics_collector().publish_elapsed_time(
        stat,
        time_in_milliseconds,
        description
    )


def publish_count(stat: str, description: str = "", count: int = 1) -> None:
    """
    :param stat: Name of the stat to publish the count for.
    :param description: Description for the stat.
    :param count: The count to increment by.
    """
    _get_metrics_collector().publish_count(stat, count, description)


def publish_error(stat: str, description: str = "") -> None:
    """
    :param stat: Name of the stat to publish the error for.
    :param description: Description for the stat.
    """
    _get_metrics_collector().publish_error(stat, description)
