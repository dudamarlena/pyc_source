#!/usr/bin/env python

from setuptools import setup
from setuptools import find_packages

try:
    import pypandoc
    long_description = pypandoc.convert('README.md', 'rst')
except (IOError, ImportError):
    long_description = open('README.md').read()

version = '0.1.1'
requirements = [
    'requests >= 2.4',
    'click >= 4.1',
    'tabletext >= 0.1',
]

setup(
    name='btcprice-cli',
    version=version,
    install_requires=requirements,
    author='Fausto Carrera',
    author_email='fausto.carrera@gmx.com',
    packages=find_packages(),
    include_package_data=True,
    url='https://github.com/faustocarrera/btcprice-cli',
    license='MIT',
    description='Check the Bitcoin price from the cli',
    long_description=long_description,
    entry_points={
        'console_scripts': [
            'btcprice-cli=btcprice:cli'
        ]
    },
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'License :: OSI Approved :: MIT License',
        'Operating System :: POSIX',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.4',
        'Topic :: Utilities',
    ]
)
