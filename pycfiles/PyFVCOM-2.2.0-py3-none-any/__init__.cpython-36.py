# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
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