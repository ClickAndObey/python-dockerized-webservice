"""
This exists due to the multi-location pathing problem in Python. We would like our tests to have the same pathing as the
modules being tested, so we need to add the following 2 lines to make it work.
"""

from pkgutil import extend_path
__path__ = extend_path(__path__, __name__)
