"""This file is part of the activitypub_server package

Copyright (c) 2017 Mark Shane Hayden
Copyright (c) 2017 Coalesco Digital Systems Inc.

See the COPYRIGHT.txt file in the root directory of the package source for
full copyright notice

Distribution granted under the terms of EITHER GPLv3+ OR Apache v2

See LICENSE_*.txt files in the root directory for full license terms.
"""

from setuptools import setup, find_packages
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

# Use the README file as the Long Description
with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='zerosms',

    version='0.0.1',

    description='Send a text message via Way2SMS to your friends and family in India. Enter your India mobile number and sms text message as parameters. Your Free SMS sending to India will be delivered instantly',
    long_description=long_description,

    url='https://github.com/username/',

    author='Siva Avis',
    author_email='forhacku@gmail.com',

    classifiers=[
        'Intended Audience :: Developers',
        'Topic :: Communications',
        'Topic :: Software Development :: Libraries',
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
        'Programming Language :: Python :: 3',
    ],

    keywords='Way2sms zerosms freesms futuresms',
    install_requires=['beautifulsoup4', 'requests'],
    packages=[
        'zerosms',
    ],

)
