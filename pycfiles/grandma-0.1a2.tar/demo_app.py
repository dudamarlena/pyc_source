# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/mark/devel/grandma/demo/demo_app.py
# Compiled at: 2011-10-03 06:03:28
from exceptions import ValueError
data = {'font': [
          'arial', 'tahoma', 'brushScript', 'monotypeCorsive'], 
   'bold': [
          True, False], 
   'italic': [
            True, False], 
   'strikethrough': [
                   True, False], 
   'underline': [
               True, False], 
   'color': [
           'black', 'yellow', 'white', 'blue', 'red', 'green'], 
   'size': [
          'small', 'nominal', 'large', 'xLarge', 'xxLarge', 'xxxLarge', 'ridiculouslyLarge']}

def run_app(**params):
    """This is a simple sample app for demonstration purposes."""
    for p in params.keys():
        if params[p] not in data[p]:
            raise ValueError('Parameter ' + params[p] + ' not in defined range of ' + p + '!')

    return True