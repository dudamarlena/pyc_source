# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\tikon\SIG.py
# Compiled at: 2016-08-23 16:03:43
# Size of source mod 2**32: 318 bytes
"""
Para manejar datos de SIG de parcelas.
"""

class Parcela(object):

    def __init__(símismo, coordinadas):
        símismo.coordinadas = coordinadas
        símismo.área = símismo.calcular_área()

    def calcular_área(símismo):
        área = 0
        return área