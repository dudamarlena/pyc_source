# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/uforgecli/utils/uforgecli_utils.py
# Compiled at: 2017-03-01 08:38:06
__author__ = 'UShareSoft'
import json, sys, re, traceback
from os.path import expanduser
import os, urllib
from uforge.objects.uforge import *
from ussclicore.utils import printer

def is_uforge_exception(e):
    if len(e.args) >= 1 and type(e.args[0]) is UForgeError:
        return True


def get_uforge_exception(e):
    if len(e.args) >= 1 and type(e.args[0]) is UForgeError:
        return "UForge Error '" + str(e.args[0].statusCode) + "' with method: " + e.args[0].requestMethod + ' ' + e.args[0].requestUri + '\n' + 'Message:\n\t' + e.args[0].localizedErrorMsg.message


def print_uforge_exception(e):
    if len(e.args) >= 1 and type(e.args[0]) is UForgeError:
        printer.out(get_uforge_exception(e), printer.ERROR)
    else:
        traceback.print_exc()


def handle_uforge_exception(e):
    print_uforge_exception(e)
    return 2


def handle_bad_parameters(cmd, e):
    printer.out('ERROR: In Arguments: ' + str(e), printer.ERROR)