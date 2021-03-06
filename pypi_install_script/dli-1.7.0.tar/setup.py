"""Packaging settings."""

from os.path import abspath, dirname
from setuptools import find_packages, setup

import dli

with open('requirements.txt', 'r') as f:
    requirements = f.readlines()


setup(
    name='dli',
    python_requires='>3.6.0',
    version=dli.__version__,
    url='https://ihsmarkit.com',
    description='Data Lake command line Interface.',
    author='IHS Markit Data Lake Team',
    author_email='datalake-support@ihsmarkit.com',
    license='MOZ-2',
    classifiers=[
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'License :: OSI Approved :: Mozilla Public License 2.0 (MPL 2.0)',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
    ],
    keywords='cli, datalake, data, lake',
    packages=find_packages(exclude=['docs', 'tests*']),
    install_requires=requirements,
)
