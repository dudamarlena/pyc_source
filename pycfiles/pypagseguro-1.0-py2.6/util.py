# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
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
    return (
     tel[:2], tel[2:])