import sys, os
from setuptools import setup


with open('./README.rst') as f:
    long_description = f.read()

setup(
    name='swimbundle_dev',
    packages=['swimbundle_dev'],
    version='0.1.2',
    description='Swimlane Bundle Development Package',
    author='Swimlane',
    author_email="info@swimlane.com",
    long_description=long_description,
    install_requires=[],
    keywords=['dev', 'development'],
    classifiers=[],
)
