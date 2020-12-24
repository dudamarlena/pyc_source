"""
Py-OpenVPN
----------
Python wrapper of `openvpn`

Links
`````
* `Docs <https://gitlab.com/petercrosby/py-openvpn>`_
* `Gitlab <https://gitlab.com/petercrosby/py-openvpn>`_



"""

import os
import sys

from setuptools import setup, find_packages


NAME = 'py_openvpn'
__v__ = '0.1.7'


if sys.version_info < (3, 5, 2):
    print('ERROR: {} requires at least Python 3.5.2 to run.'.format(NAME))
    sys.exit(1)

# Set the requirements.txt file path, located next to setup.py
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
    url='https://gitlab.com/petercrosby/py-openvpn',
    license='MIT',
    author='Peter Crosby',
    author_email='peter@headwall.io',
    description='Python wrapper of openvpn.',
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
