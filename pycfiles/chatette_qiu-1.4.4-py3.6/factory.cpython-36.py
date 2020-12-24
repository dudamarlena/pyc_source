# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\chatette_qiu\adapters\factory.py
# Compiled at: 2019-03-27 03:00:31
# Size of source mod 2**32: 742 bytes
"""
Module `chatette_qiu.adapters.factory`.
Defines a factory method that allows to create an adapter from a string name.
"""
from chatette_qiu.adapters.jsonl import JsonListAdapter
from chatette_qiu.adapters.rasa import RasaAdapter

def create_adapter(adapter_name):
    """
    Instantiate an adapter and returns it given the name of the adapter as a str.
    Names are:
        - 'rasa': RasaAdapter
        - 'jsonl': JsonListAdapter
    """
    if adapter_name is None:
        return
    else:
        adapter_name = adapter_name.lower()
        if adapter_name == 'rasa':
            return RasaAdapter()
        if adapter_name == 'jsonl':
            return JsonListAdapter()
    raise ValueError('Unknown adapter was selected.')