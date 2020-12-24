# -*- coding: utf-8 -*-
from setuptools import find_packages, setup

with open('README.md') as f:
    readme_contents = f.read()

setup(
    name='asyncy-hub',
    version='0.0.1',
    description='A Python SDK to access the Asyncy Hub, '
                'which supports caching and more',
    long_description=readme_contents,
    author='Asyncy',
    author_email='support@asyncy.com',
    url='https://github.com/asyncy/hub-sdk-python',
    packages=find_packages(exclude=('tests', 'docs')),
    install_requires=[
        'requests==2.21.0',
        'peewee==3.9.3',
        'cachetools==3.1.0'
    ],
    tests_require=[
        'pytest==4.3.1',
        'pytest-mock==1.10.2',
        'pytest-cov==2.6.1'
    ],
    setup_requires=['pytest-runner==4.4']
)
