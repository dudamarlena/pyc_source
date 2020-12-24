#!/usr/bin/env python3

from setuptools import setup

# Work around mbcs bug in distutils.
# http://bugs.python.org/issue10945
import codecs
try:
    codecs.lookup('mbcs')
except LookupError:
    ascii = codecs.lookup('ascii')
    codecs.register(lambda name, enc=ascii: {True: enc}.get(name == 'mbcs'))

VERSION = '0.0.0'

setup(
    name='dascoin',
    version=VERSION,
    description='Python library for dascoin',
    author='Blockchain Projects B.V.',
    author_email='info@blockchainprojectsbv.com',
    maintainer='Fabian Schuh',
    maintainer_email='Fabian.Schuh@blockchainprojectsbv.com',
    keywords=['dascoin', 'library', 'api', 'rpc'],
    packages=[
        "dascoin",
    ],
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
    ],
    install_requires=[
        #"graphenelib>=0.6.3",
        #"websockets",
        #"appdirs",
        #"Events",
        #"scrypt",
        #"pycryptodome",  # for AES, installed through graphenelib already
    ],
    setup_requires=['pytest-runner'],
    tests_require=['pytest'],
    include_package_data=True,
)
