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
    name='soundac',
    version=VERSION,
    description='Python library for soundac',
    #long_description=open('README.md').read(),
    #download_url='https://github.com/bitshares/python-bitshares/tarball/' + VERSION,
    author='Fabian Schuh',
    author_email='Fabian@chainsquad.com',
    maintainer='Fabian Schuh',
    maintainer_email='Fabian@chainsquad.com',
    #url='http://www.github.com/bitshares/python-bitshares',
    keywords=['bitshares', 'library', 'api', 'rpc'],
    packages=[
        "soundac",
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
