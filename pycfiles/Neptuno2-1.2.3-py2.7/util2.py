# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/neptuno/util2.py
# Compiled at: 2012-10-29 11:33:17
from datetime import datetime, date

def strtodate(s, fmt='%d/%m/%Y'):
    return datetime.strptime(s, fmt).date()


def strtotime(s, fmt='%H:%M'):
    return datetime.strptime(s, fmt).time()


def strtobool(s):
    if s.lower() == 'true':
        return True
    if s.lower() == 'false':
        return False
    raise TypeError('No es un tipo booleano')


def datetostr(d, fmt='%d/%m/%Y'):
    if d is None:
        return ''
    else:
        try:
            return d.strftime(fmt)
        except ValueError:
            return ''

        return


def timetostr(t, fmt='%H:%M'):
    if t is None:
        return ''
    else:
        return t.strftime(fmt)
        return


def inicio_fin_mes(fecha):
    u"""
    Devuelve el primer y el último día del mes en la fecha 'fecha'.
    IN
      fecha <date>
      
    OUT
      (<date>, <date>)
    """
    inicio = date(fecha.year, fecha.month, 1)
    mes_siguiente = date.fromordinal(inicio.toordinal() + 31)
    fin = date.fromordinal(date(mes_siguiente.year, mes_siguiente.month, 1).toordinal() - 1)
    return (
     inicio, fin)