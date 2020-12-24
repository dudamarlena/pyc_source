# -*- coding: utf-8 -*-
"""
    Setup for CoinMate.io API wrapper.
"""

from distutils.core import setup
import setuptools

setup(
    name='coinmate-api',
    keywords=['bitcoin', 'coinmate.io', 'bitcoin api'],
    url='https://github.com/rrguardo/coinmate.io-api',
    packages=setuptools.find_packages(),
    package_dir={'': 'src'},
    version='1.1.7',
    description='CoinMate.io exchange API client.',
    author='https://github.com/rrguardo/',
    author_email='17535309+rrguardo@users.noreply.github.com',
    classifiers=['Development Status :: 5 - Production/Stable',
                   'Intended Audience :: Developers',
                   'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
                   'Programming Language :: Python :: 3',
                   'Programming Language :: Python :: 3.6',
                   'Programming Language :: Python :: 2.7',
                   'Topic :: Software Development'],
    long_description = '''
Coinmate.io API wrapper
-----------------------

Basic CoinMate.io API client, that support get the balance, withdrawal
and more ::

    from coinmate_api import coinmate
    cm_api = coinmate('privateApiKey', 'publicApiKey', 'client_id')
    print cm_api.get_eur_available()
    result = cm_api.withdraw_bitcoins(0.01,'1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa')
    if not result['error']:
        print "Transaction ID:"
        print result['data']
    ticker_info = cm_api.get_ticker()

''')
