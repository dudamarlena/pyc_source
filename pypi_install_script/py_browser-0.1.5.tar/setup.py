"""
Py-Browser
----------
Python3 + Selenium configurable browser

"""
import os
import sys

from setuptools import setup, find_packages


NAME = 'py_browser'
__v__ = '0.1.5'

if sys.version_info < (3, 5, 2):
    print('ERROR: {} requires at least Python 3.5.2 to run.'.format(NAME))
    sys.exit(1)

requirements_file = os.path.join(os.path.abspath(os.path.dirname(__file__)),
                                 'requirements.txt')

try:
    with open(requirements_file, 'r') as open_file:
        requirements = open_file.readlines()
except (FileNotFoundError, IOError):
    raise

setup(
    name=NAME,
    version=__v__,
    url='https://gitlab.com/petercrosby/py-browser',
    license='MIT',
    author='Peter Crosby',
    author_email='peter@headwall.io',
    description='Python3 + Selenium configurable browser',
    long_description=__doc__,
    python_requires='>=3.5.2',
    install_requires=requirements,
    packages=find_packages(
        exclude=['tests', 'bin', 'dist']
    ),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ]
)
