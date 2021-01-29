"""
Module used for handling logging utilities.
"""

import logging


def create_logger(verbose: bool) -> logging.Logger:
    """
    Create a stream logger.
    :param verbose: Whether to output debug information.
    """
    logger = logging.getLogger(__name__)
    logging_level = logging.DEBUG if verbose else logging.INFO
    logger.setLevel(logging_level)

    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(logging_level)
    logger.addHandler(stream_handler)

    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    stream_handler.setFormatter(formatter)

    return logger
