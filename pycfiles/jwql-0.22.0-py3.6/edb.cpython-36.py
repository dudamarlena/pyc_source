# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/jwql/utils/edb.py
# Compiled at: 2019-08-26 11:08:03
# Size of source mod 2**32: 871 bytes
"""Tests for the ``engineering_database`` module.

Authors
-------

    - Johannes Sahlmann

Use
---

    These tests can be run via the command line (omit the ``-s`` to
    suppress verbose output to ``stdout``):

    ::

        pytest -s test_edb_interface.py
"""
from astropy.time import Time
import jwql.utils.engineering_database as edb

def test_query_single_mnemonic():
    """Test the query of a mnemonic over a given time range."""
    mnemonic_identifier = 'SE_ZIMIRICEA'
    start_time = Time(2018.01, format='decimalyear')
    end_time = Time(2018.02, format='decimalyear')
    mnemonic = edb.query_single_mnemonic(mnemonic_identifier, start_time, end_time)
    print(mnemonic)


def main():
    data, meta = edb.get_all_mnemonic_identifiers()
    print(data)
    test_query_single_mnemonic()


if __name__ == '__main__':
    main()