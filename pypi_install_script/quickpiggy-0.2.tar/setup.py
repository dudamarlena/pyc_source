#!/usr/bin/env python2
from distutils.core import setup
setup(
    name = "quickpiggy",
    version = "0.2",
    py_modules = ['quickpiggy'],
    description = "QuickPiggy - launch a PostgreSQL server, without the hassle.",
    author = "Wicher Minnaard",
    author_email = "wicher@gavagai.eu",
    url = "http://smormedia.gavagai.nl/dist/quickpiggy/",
    download_url = "http://smormedia.gavagai.nl/dist/quickpiggy/quickpiggy-0.2.tar.gz",
    keywords = ["postgresql"],
    classifiers = [
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Development Status :: 4 - Beta",
        "Environment :: Other Environment",
        "Intended Audience :: Developers",
        "License :: Public Domain",
        "Operating System :: POSIX",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Database",
        ],
    long_description = """\
QuickPiggy - launch a PostgreSQL server from Python, without the hassle.
--------------------------------------------------------------------------------
by Wicher Minnaard <wicher@gavagai.eu> <http://smorgasbord.gavagai.nl>

Rationale: http://smorgasbord.gavagai.nl/2011/02/postgresql-quickie-server/

This is public domain software.

Prerequisites:

- postgresql-server (tested with v9.0), providing 'postgres', 'initdb', 'createdb'

- postgresql libraries and clients (tested with v9.0), providing 'psql'

Test your prerequisites by running 'quickpiggy.py' as a program.

A makeshift PostgresSQL instance can be obtained quite easily:

pig = quickpiggy.Piggy(volatile=True, create_db='somedb')

conn = psycopg2.connect(pig.dsnstring())

Most other use cases can be accommodated for by passing more parameters.

This version works with Python 2.7 and 3.1+.
"""
)
