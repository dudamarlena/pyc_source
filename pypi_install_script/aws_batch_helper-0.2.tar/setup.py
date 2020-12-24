#!/usr/bin/env python

import os

from setuptools import setup, find_packages


def local_file(name):
    return os.path.relpath(os.path.join(os.path.dirname(__file__), name))

SOURCE = local_file('src')

setup(
    name="aws_batch_helper",
    version="0.2",
    packages=find_packages(SOURCE),
    author='Robert Kenny',
    author_email='R.Kenny@wellcome.ac.uk',
    url='https://github.com/wellcometrust/aws_batch_helper',
    package_dir={'': SOURCE},
    entry_points = {
        'console_scripts': ['aws_batch_helper=aws_batch_helper.aws_batch:main']
    },
    python_requires='>=3.6',
    install_requires=['docopt==0.6.2','boto3>=1.4.5']
)

