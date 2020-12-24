# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/reviewboard/diffviewer/evolutions/filediff_filenames_1024_chars.py
# Compiled at: 2020-02-11 04:03:56
from __future__ import unicode_literals
from django_evolution.mutations import ChangeField
MUTATIONS = [
 ChangeField(b'FileDiff', b'source_file', initial=None, max_length=1024),
 ChangeField(b'FileDiff', b'dest_file', initial=None, max_length=1024)]