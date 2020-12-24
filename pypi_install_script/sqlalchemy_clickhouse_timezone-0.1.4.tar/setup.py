#!/usr/bin/env python

from os import path, getenv
from setuptools import setup
from codecs import open

VERSION = [0, 1, 4]
readme = open('README.rst').read()

setup(
    name='sqlalchemy_clickhouse_timezone',
    version='.'.join('%d' % v for v in VERSION[0:3]),
    description='ClickHouse SQLAlchemy Dialect with timezone support',
    long_description = readme,
    author = '21499836@qq.com',
    author_email = '21499836@qq.com',
    license = 'Apache License, Version 2.0',
    url = 'https://github.com/ufully/sqlalchemy-clickhouse-timezone',
    keywords = "db database cloud analytics clickhouse with tiemzone support",
    download_url = 'https://github.com/ufully/sqlalchemy-clickhouse-timezone/releases/tag/v0.1.0',
    install_requires = [
        'sqlalchemy>=1.0.0',
        'infi.clickhouse_orm==1.0.4',
        'tzlocal>=2.0.0'
    ],
    packages=[
        'sqlalchemy_clickhouse_timezone',
    ],
    package_dir={
        'sqlalchemy_clickhouse_timezone': '.',
    },
    package_data={
        'sqlalchemy_clickhouse_timezone': ['LICENSE.txt'],
    },
    entry_points={
        'sqlalchemy.dialects': [
            'clickhouse=sqlalchemy_clickhouse_timezone.base',
        ]
    },
    classifiers = [
        'Development Status :: 5 - Production/Stable',

        'Environment :: Console',
        'Environment :: Other Environment',

        'Intended Audience :: Developers',
        'Intended Audience :: Education',
        'Intended Audience :: Information Technology',
        'Intended Audience :: System Administrators',

        'License :: OSI Approved :: Apache Software License',

        'Operating System :: OS Independent',

        'Programming Language :: SQL',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',

        'Topic :: Database',
        'Topic :: Software Development',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Application Frameworks',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)
