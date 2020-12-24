# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: ./scripts/../apps/example/webapp/controller/bad_import.py
# Compiled at: 2011-03-19 21:05:04
__doc__ = '\nThis module cannot be imported because it should itself raise an\nimport error.\n'
import intentionally_non_existent_module