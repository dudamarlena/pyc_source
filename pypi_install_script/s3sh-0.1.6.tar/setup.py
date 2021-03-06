#!/usr/bin/env python

from setuptools import setup, find_packages

setup(
    name='s3sh',
    version='0.1.6',
    description='A repl for s3',
    long_description='Traverse s3 just like it would be a filesystem',
    author='Wim Berchmans',
    author_email="wimberchmans@gmail.com",
    license='',
    url='https://github.com/WRRB/s3sh',
    include_package_data=True,
    package_data={},
    packages=find_packages(),
    install_requires=['boto3'],
    tests_require=[],
    scripts=['s3sh/cli/s3sh', 's3sh/cli/s3sh.bat'],
    zip_safe=False
)
