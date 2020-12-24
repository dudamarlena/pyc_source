# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

from sitef import sdk

__description__ = 'Python SiTef'
__long_description__ = 'Python library for SiTef API'

__author__ = 'DevTeam Digisat'
__author_email__ = 'devteam@digisat.com.br'
__special_things__ = 'Rodrigo Vaccari'

testing_extras = [
    'pytest',
    'pytest-cov',
]

setup(
    name='python-sitef',
    version=sdk.VERSION,
    author=__author__,
    author_email=__author_email__,
    packages=find_packages(),
    license='MIT',
    description=__description__,
    long_description=__long_description__,
    special_things=__special_things__,
    url='https://digisat.com.br',
    keywords='Payment, sitef',
    include_package_data=True,
    zip_safe=False,
    install_requires=['requests>2.20.0'],
    classifiers=[
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'Operating System :: OS Independent',
        'Topic :: Software Development',
        'Environment :: Web Environment',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'License :: OSI Approved :: MIT License',
    ],
    tests_require=['pytest'],
    extras_require={
        'testing': testing_extras,
    },
)
