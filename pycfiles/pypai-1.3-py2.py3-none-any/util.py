# uncompyle6 version 3.6.7
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.6-universal/egg/pypagseguro/util.py
# Compiled at: 2011-01-06 19:06:57
from re import compile

def telefone(tel):
    u"""
    Trata telefones, retornando o ddd e o telefone necessário

    Exemplo:

    >>> telefone ('(11) 1234-5678')
    ('11', '12345678')
    >>> telefone ('11 1234.5678')
    ('11', '12345678')
    >>> telefone ('1187654321')
    ('11', '87654321')
    >>> telefone ('12345678')
    ('', '12345678')
  """
    c = compile('\\D')
    tel = c.sub('', tel)
    if len(tel) <= 8:
        return ('', tel)
    return (tel[:2], tel[2:])