"""
Install script used to package this module. Nothing special here, just package everything and include the requirements.
"""

import os
import subprocess

from setuptools import setup, find_packages

__THIS_DIR = os.path.dirname(os.path.abspath(__file__))


def main():
    """
    Build the whl file.
    """
    # pipfile2req generates a requirements.txt output. Pipenv utilities don't pin the version to what is in the lock
    # (at least not without updating first), which is not what we want for our application package installers.
    requirements = subprocess.check_output(["pipfile2req", "/python/Pipfile.lock"]).decode("utf-8").splitlines()
    print("Requirements:\n")
    print("\n".join(requirements))

    main_source_dir = "/python"
    setup(
        name="clickandobey.dockerized.webservice",
        version=os.environ.get("VERSION", "1.0.0"),
        description="Example Python Dockerized Webservice to use as a template.",
        author="Click and Obey",
        url="http://github.com/clickandobey/python-dockerized-webservice",
        license="Unlicensed",
        scripts=[
        ],
        zip_safe=False,
        packages=find_packages(main_source_dir),
        package_dir={"": main_source_dir},
        python_requires=">=3.9, <4",
        install_requires=requirements
    )


if __name__ == "__main__":
    main()
