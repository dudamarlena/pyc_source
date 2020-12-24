# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/grs/mobileapi.py
# Compiled at: 2011-10-05 02:42:28
from realtime import twsk

def covstr(s):
    """ convert string to int or float. """
    try:
        ret = int(s)
    except ValueError:
        ret = float(s)

    return ret


class mapi(object):

    def __init__(self, stock_no):
        self.g = twsk(stock_no).real

    @property
    def output(self):
        '''
    re = """<table>
            <tr><td>%(name)s</td><td>%(c)s</td><td>%(range)+.2f(%(pp)+.2f%%)</td></tr>
            <tr><td>%(stock_no)s</td><td>%(value)s</td><td>%(time)s</td></tr></table>""" % {
    '''
        if covstr(self.g['range']) > 0:
            css = 'red'
        elif covstr(self.g['range']) < 0:
            css = 'green'
        else:
            css = 'gray'
        re = {'name': self.g['name'], 
           'stock_no': self.g['no'], 
           'time': self.g['time'], 
           'open': self.g['open'], 
           'h': self.g['h'], 
           'l': self.g['l'], 
           'c': self.g['c'], 
           'max': self.g['max'], 
           'min': self.g['min'], 
           'range': covstr(self.g['range']), 
           'ranges': self.g['ranges'], 
           'value': self.g['value'], 
           'pvalue': self.g['pvalue'], 
           'pp': covstr(self.g['pp']), 
           'top5buy': self.g['top5buy'], 
           'top5sell': self.g['top5sell'], 
           'crosspic': self.g['crosspic'], 
           'css': css}
        return re