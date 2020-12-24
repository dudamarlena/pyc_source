# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/SimpleChat/__init__.py
# Compiled at: 2011-06-02 04:49:39
import SimpleChat

def initialize(context):
    """Initialize."""
    try:
        context.registerClass(SimpleChat.SimpleChat, constructors=(SimpleChat.manage_add_simple_chat_form, SimpleChat.manage_add_simple_chat))
    except:
        import sys, traceback, string
        (type, val, tb) = sys.exc_info()
        sys.stderr.write(string.join(traceback.format_exception(type, val, tb), ''))
        del type
        del val
        del tb