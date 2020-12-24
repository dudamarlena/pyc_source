"""
Py-Cache
----------
Simple SQLite3 + Python3 key-value cache.

Referenced from: http://flask.pocoo.org/snippets/87/

Links
`````
* `Docs <https://gitlab.com/petercrosby/py-cache>`_
* `SQLite Cache <http://flask.pocoo.org/snippets/87/>`_
* `Gitlab <https://gitlab.com/petercrosby/py-cache>`_

"""

import os
import sys

from setuptools import setup


NAME = 'py-cache'
__v__ = '0.1.4'


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
    url='https://gitlab.com/petercrosby/py-cache',
    license='MIT',
    author='Peter Crosby',
    author_email='peter@headwall.io',
    description='Simple SQLite3+Python3 key-value cache.',
    long_description=__doc__,
    python_requires='>=3.5.2',
    py_modules=['pycache'],
    install_requires=requirements,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ]
)
