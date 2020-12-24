# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/marketplacecli/utils/marketplace_utils.py
# Compiled at: 2016-06-03 07:47:35
__author__ = 'UShareSoft'
import traceback
from marketplacecli.exceptions.UForgeException import UForgeException
from marketplace.objects.marketplace import UForgeError
from ussclicore.utils import printer

def is_uforge_exception(e):
    if len(e.args) >= 1 and type(e.args[0]) is UForgeError:
        return True


def get_uforge_exception(e):
    if len(e.args) >= 1 and type(e.args[0]) is UForgeError:
        return "UForge Error '" + str(e.args[0].statusCode) + "' with method: " + e.args[0].requestMethod + ' ' + e.args[0].requestUri + '\n' + 'Message:\n\t' + e.args[0].localizedErrorMsg.message


def print_uforge_exception(e):
    if type(e) is UForgeException:
        printer.out(e.value, printer.ERROR)
    elif len(e.args) >= 1 and type(e.args[0]) is UForgeError:
        printer.out(get_uforge_exception(e), printer.ERROR)
    else:
        traceback.print_exc()


def handle_uforge_exception(e):
    print_uforge_exception(e)
    return 2


def handle_bad_parameters(cmd, e):
    printer.out('ERROR: In Arguments: ' + str(e), printer.ERROR)