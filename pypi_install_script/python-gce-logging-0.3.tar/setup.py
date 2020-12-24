#!/usr/bin/python
# coding: utf8

import os
import re

from setuptools import setup

# reqs is a list of requirement
reqs = [
    "python-json-logger>=0.1.5,<2.0"
]

test_requirements = [
    "pytest"
]

with open('README.md') as readme_file:
    readme = readme_file.read()

# parse version
with open(os.path.join(os.path.abspath(os.path.dirname(__file__)),
                       'pythongcelogging', "__init__.py")) as fdp:
    pattern = re.compile(r".*__version__ = '(.*?)'", re.S)
    VERSION = pattern.match(fdp.read()).group(1)

config = {
    'description': 'GCE Logging',
    'author': 'Matthias Wutte',
    'url': '',
    'download_url': 'https://github.com/wuttem',
    'author_email': 'matthias.wutte@gmail.com',
    'version': VERSION,
    'install_requires': reqs,
    'tests_require': test_requirements,
    'packages': {"pythongcelogging": "pythongcelogging"},
    'scripts': [],
    'name': 'python-gce-logging'
}

setup(**config)