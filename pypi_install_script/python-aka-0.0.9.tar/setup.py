import os
from setuptools import setup, find_packages


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
    name="python-aka",
    version="0.0.9",
    author="Drew Stinnett",
    author_email="drew.stinnett@duke.edu",
    description=("Interact with AKA through Python"),
    license="BSD",
    keywords="aka cli",
    packages=find_packages(),
    scripts=['scripts/aka-cli.py'],
    long_description_content_type="text/markdown",
    long_description=read('README.md'),
)
