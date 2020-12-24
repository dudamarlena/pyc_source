# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/gdcdictionary/__init__.py
# Compiled at: 2019-04-23 20:54:02
import os
from dictionaryutils import DataDictionary as GDCDictionary
SCHEMA_DIR = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'schemas')
gdcdictionary = GDCDictionary(root_dir=SCHEMA_DIR)