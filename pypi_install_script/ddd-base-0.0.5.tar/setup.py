"""Setuptools entry point."""
import codecs
import os
from setuptools import find_packages

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


HERE = os.path.abspath(os.path.dirname(__file__))
ABOUT = {}
with open(os.path.join(HERE, 'ddd_base', '__version__.py')) as f:
    exec(f.read(), ABOUT)

CLASSIFIERS = [
    'Development Status :: 4 - Beta',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: MIT License',
    'Natural Language :: English',
    'Operating System :: OS Independent',
    'Programming Language :: Python',
    'Programming Language :: Python :: 2.7',
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
    'Topic :: Software Development :: Libraries :: Python Modules'
]

dirname = os.path.dirname(__file__)

long_description = (
    codecs.open(os.path.join(dirname, 'README.rst'), encoding='utf-8').read() + '\n' +
    codecs.open(os.path.join(dirname, 'CHANGES.rst'), encoding='utf-8').read()
)

setup(
    name='ddd-base',
    version=ABOUT['__version__'],
    description='DDD base framework for python',
    long_description=long_description,
    author='Sun Wei',
    author_email='wayde.sun@gmail.com',
    url='https://github.com/sunwei/ddd-base',
    packages=find_packages(exclude=['tests*']),
    install_requires=[],
    classifiers=CLASSIFIERS)
