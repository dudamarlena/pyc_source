# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/will/projects/moya/moya/run.py
# Compiled at: 2015-09-01 07:17:44
from __future__ import unicode_literals
from .archive import Archive

def get_callable_from_document(path, element_ref, fs=b'./', breakpoint=False):
    """Shortcut to get a callable from a moya xml document"""
    callable = Archive.get_callable_from_document(path, element_ref, fs=fs, default_context=True, breakpoint=breakpoint)
    return callable


def run(path, element_ref, fs=b'./', breakpoint=False):
    """Run a callable element in a moya xml document"""
    callable = Archive.get_callable_from_document(path, element_ref, fs=fs, default_context=True, breakpoint=breakpoint)
    return callable()