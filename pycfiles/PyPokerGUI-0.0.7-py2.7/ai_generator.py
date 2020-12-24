# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.12-intel/egg/pypokergui/ai_generator.py
# Compiled at: 2017-03-20 20:51:28
import os, sys, importlib
from pypokerengine.players import BasePokerPlayer

def healthcheck(script_path, quiet=False):
    status = True
    try:
        setup_method = _import_setup_method(script_path)
    except Exception as e:
        if not quiet:
            print '"setup_ai" method was not found in [ %s ].(Exception=%s)' % (script_path, e.message)
        status = False

    try:
        if status:
            player = setup_method()
    except Exception as e:
        if not quiet:
            print 'Exception [ %s ] was raised when your "setup_ai" method invoked' % e.message
        status = False

    if status and not isinstance(player, BasePokerPlayer):
        if not quiet:
            print 'Generated player is not instance of [ BasePokerPlayer ] but of [ %s ]' % type(player).__name__
        status = False
    if status and not quiet:
        print 'health check succeeded for script of [ %s ]' % script_path
    return status


def _import_setup_method(script_path):
    dirname = os.path.dirname(script_path)
    filename = os.path.basename(script_path)
    sys.path.append(dirname)
    m = importlib.import_module(os.path.splitext(filename)[0])
    return m.setup_ai