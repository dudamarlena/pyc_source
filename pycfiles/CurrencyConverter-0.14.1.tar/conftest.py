# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/richardn/tcc/currencycloud-python/test/conftest.py
# Compiled at: 2015-06-30 08:53:27
from betamax import Betamax
import os
record_mode = 'never' if os.environ.get('TRAVIS_GH3') else 'once'
with Betamax.configure() as (config):
    config.cassette_library_dir = 'test/fixtures/vcr_cassettes'
    config.default_cassette_options['record_mode'] = record_mode
    config.define_cassette_placeholder('<AUTH_TOKEN>', os.environ.get('GH_AUTH', 'xxxxxxxxxxxxxxxxxxxx'))