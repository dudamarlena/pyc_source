# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/dossier/models/tests/test_sip.py
# Compiled at: 2015-07-08 07:34:06
"""test of NP and SIP extraction

.. This software is released under an MIT/X11 open source license.
   Copyright 2015 Diffeo, Inc.

"""
from __future__ import absolute_import, division, print_function
from dossier.models.features.sip import sip_noun_phrases, noun_phrases

def test_noun_phrases():
    text = '\nThis is a test of noun phrase extraction on New York Harbour and the cheese burger!\n'
    np = noun_phrases(text)
    assert 'chees_burger' in np