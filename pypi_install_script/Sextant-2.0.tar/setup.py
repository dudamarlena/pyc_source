# -----------------------------------------
# Sextant
# Copyright 2014, Ensoft Ltd.
# Author: James Harkin, using work from Patrick Stevens and James Harkin
# -----------------------------------------
#

import glob
import os
from setuptools import setup

setup(
    name='Sextant',
    version='2.0',
    description= 'Navigating the C',
    url='http://open.ensoft.co.uk/Sextant',
    license='Simplified BSD License',
    packages=['sextant', 'sextant.web', 'resources', 'etc'],
    package_dir={'sextant': 'src/sextant', 'resources': 'resources', 'etc': 'etc'},
    scripts=['bin/sextant'],
    install_requires=['neo4jrestclient', 'twisted'],
    package_data={
        'resources': ['sextant/web/*'],
        'etc': ['*.conf', 'init/*'],
    },
)


