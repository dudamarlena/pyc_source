# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/land/copernicus/content/rules/download/handler.py
# Compiled at: 2017-11-01 05:34:47
""" Content rules handler
"""
from plone.app.contentrules.handlers import execute

def execute_event(event):
    """ Execute custom rules
    """
    execute(event.object, event)