#!/usr/bin/env python

from setuptools import setup, find_packages

install_requires = [
    'requests>=2.13.0',
#    'six==1.10.0',
#    'bintrees==2.0.7',
#    'websocket-client==0.40.0'
]

setup(
    name='coinbasepro-python',
    version='0.0.5',
    author='Kyle A. Pearson',
    author_email='k.pearson112@gmail.com',
    license='MIT',
    url='https://github.com/pearsonkyle/coinbasepro-python',
    packages=find_packages(),
    install_requires=install_requires,
    description='The unofficial Python client for the Coinbase Pro API',
    download_url='',
    keywords=['coinbase', 'coinbasepro', 'orderbook', 'trade', 'bitcoin', 'ethereum', 'BTC', 'ETH', 'client', 'api', 'wrapper', 'exchange', 'crypto', 'currency', 'trading', 'trading-api', 'coinbase-api', 'coinbasepro-api'],
    classifiers=[
        'Development Status :: 1 - Planning',
        'Intended Audience :: Developers',
        'Intended Audience :: Financial and Insurance Industry',
        'Intended Audience :: Information Technology',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
)
