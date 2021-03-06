#! /usr/bin/env python
from distutils.core import setup
from setuptools import find_packages
import sys

# python2 and python3 support
try:
    reload
except NameError:
    # py3k has unicode by default
    pass
else:
    reload(sys).setdefaultencoding('utf-8')


setup(
    name='django-gipsy',
    version='2.10',
    author='Guillaume Pousseo',
    author_email='guillaumepousseo@revsquare.com',
    description='A set of fancy tools for django.',
    long_description=open('README.rst').read(),
    url='http://www.revsquare.com',
    license='BSD License',
    platforms=['OS Independent'],
    packages=find_packages(),
    include_package_data=True,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
    ],
    install_requires=[
        'google-api-python-client==1.5.5'
    ],
)
