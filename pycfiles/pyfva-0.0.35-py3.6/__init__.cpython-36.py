# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pyfva/__init__.py
# Compiled at: 2017-07-30 20:17:58
# Size of source mod 2**32: 312 bytes
from importlib import import_module
from .clientes.autenticador import ClienteAutenticador
from .clientes.firmador import ClienteFirmador
from .clientes.validador import ClienteValidador
from .clientes.verificador import ClienteVerificador

def load_module_responder(module):
    return import_module(module)