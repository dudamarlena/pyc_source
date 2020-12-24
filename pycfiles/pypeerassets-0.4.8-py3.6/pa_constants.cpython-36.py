# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pypeerassets/pa_constants.py
# Compiled at: 2018-06-29 14:42:01
# Size of source mod 2**32: 1252 bytes
"""various protocol constants"""
from collections import namedtuple
from decimal import Decimal
from pypeerassets.exceptions import UnsupportedNetwork
PAParams = namedtuple('PAParams', [
 'network_name',
 'network_shortname',
 'P2TH_wif',
 'P2TH_addr',
 'test_P2TH_wif',
 'test_P2TH_addr',
 'P2TH_fee'])
params = (
 PAParams('peercoin', 'ppc', 'U624wXL6iT7XZ9qeHsrtPGEiU78V1YxDfwq75Mymd61Ch56w47KE', 'PAprodbYvZqf4vjhef49aThB9rSZRxXsM6', 'UAbxMGQQKmfZCwKXAhUQg3MZNXcnSqG5Z6wAJMLNVUAcyJ5yYxLP', 'PAtesth4QreCwMzXJjYHBcCVKbC4wjbYKP', Decimal(0.01)),
 PAParams('peercoin-testnet', 'tppc', 'cTJVuFKuupqVjaQCFLtsJfG8NyEyHZ3vjCdistzitsD2ZapvwYZH', 'miHhMLaMWubq4Wx6SdTEqZcUHEGp8RKMZt', 'cQToBYwzrB3yHr8h7PchBobM3zbrdGKj2LtXqg7NQLuxsHeKJtRL', 'mvfR2sSxAfmDaGgPcmdsTwPqzS6R9nM5Bo', Decimal(0.01)))

def param_query(name: str) -> PAParams:
    """Find the PAParams for a network by its long or short name. Raises
    UnsupportedNetwork if no PAParams is found.
    """
    for pa_params in params:
        if name in (pa_params.network_name, pa_params.network_shortname):
            return pa_params

    raise UnsupportedNetwork