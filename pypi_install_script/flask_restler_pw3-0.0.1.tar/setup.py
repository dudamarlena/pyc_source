#!/usr/bin/env python

import re
from os import path as op

from setuptools import setup


def _read(fname):
    try:
        return open(op.join(op.dirname(__file__), fname)).read()
    except IOError:
        return ''

_meta = _read('flask_restler_pw3/__init__.py')

install_requires = [
    l for l in _read('requirements.txt').split('\n')
    if l and not l.startswith('#') and not l.startswith('-')]

setup(
    name="flask_restler_pw3",
    version="0.0.1",
    license="",
    description='Build REST API for Flask using Marshmallow.',
    long_description=_read('README.rst'),
    platforms=('Any'),
    keywords = "flask marshmallow rest api".split(), # noqa

    author='Kirill Klenov',
    author_email='horneds@gmail.com',
    url='https://github.com/jianc65/flask-restler',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        'Natural Language :: Russian',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Software Development :: Testing',
        'Topic :: Utilities',
    ],

    packages=['flask_restler'],
    include_package_data=True,
    install_requires=install_requires,
)
