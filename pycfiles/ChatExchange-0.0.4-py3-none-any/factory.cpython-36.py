# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build\bdist.win-amd64\egg\chatette_qiu\adapters\factory.py
# Compiled at: 2019-03-27 03:00:31
# Size of source mod 2**32: 742 bytes
__doc__ = '\nModule `chatette_qiu.adapters.factory`.\nDefines a factory method that allows to create an adapter from a string name.\n'
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