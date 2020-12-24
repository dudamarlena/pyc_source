#!/usr/bin/env python
from setuptools import find_packages, setup

with open('README.rst', encoding='utf-8') as f:
    readme = f.read()

setup(
    name='flask-qcloudsms',
    version='0.0.1',
    url='https://github.com/codeif/flask-qcloudsms',
    description='Flask Extension for qcloud sms',
    long_description=readme,
    author='codeif',
    author_email='me@codeif.com',
    license='MIT',
    install_requires=['qcloudsms-py'],
    classifiers=[
        "Programming Language :: Python :: 3",
    ],
    packages=find_packages(),
)
