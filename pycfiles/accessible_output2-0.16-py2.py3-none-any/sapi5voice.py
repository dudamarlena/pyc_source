# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build\bdist.win32\egg\accessible_output\speech\outputs\sapi5voice.py
# Compiled at: 2011-03-02 02:28:01
from collections import OrderedDict
import win32com.client
sapi5 = win32com.client.Dispatch('SAPI.SPVoice')

def available_voices():
    _voices = OrderedDict()
    for v in sapi5.GetVoices():
        _voices[v.GetDescription()] = v

    return _voices


def list_voices():
    return available_voices().keys()