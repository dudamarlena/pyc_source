# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/will/projects/moya/moya/diagnose.py
# Compiled at: 2015-09-01 07:17:44
"""Diagnose common problems"""
from __future__ import unicode_literals
_moya_exception_errors = {b'db.operational-error': b"This error can occur when the database doesn't match Moya's model definitions.\n\nDo you need to run *moya db sync*?", 
   b'db.error': b"This error typically occurs when the database doesn't match Moya's model definitions.\n\nDo you need to run *moya db sync*?", 
   b'widget.app-required': b'An application is required to display a widget.\n\nYou may need to add a &lt;install/&gt; tag to your *server.xml*.', 
   b'widget.ambiguous-app': b"Moya doesn't know which application to use for this widget because the library is installed multiple times.\n\nYou can resolve this ambiguity by adding a 'from' attribute to the tag."}

def diagnose_moya_exception(moya_exc):
    diagnosis = getattr(moya_exc, b'_diagnosis', None) or _moya_exception_errors.get(moya_exc.type, None)
    return diagnosis