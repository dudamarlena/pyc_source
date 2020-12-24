# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/symath/match.py
# Compiled at: 2015-08-21 11:58:24
import core

def extract(a, b, rv=None):
    """
  extract values from an expression
  returns a dictionary of wild names => values where b contains the wilds
  """
    if rv == None:
        rv = {}
    if isinstance(b, core.Wild):
        if b.name in rv and rv[b.name] != a:
            return
        rv[b.name] = a
        return rv
    else:
        if len(a) != len(b):
            return
        else:
            if len(b) > 1:
                for i in range(len(b)):
                    if extract(a[i], b[i], rv) == None:
                        return

                return rv
            if a == b:
                return a
            return

        return


def match(a, b, valuestore=None):
    """
  matches against a pattern, use wilds() to generate wilds

  Example:
    a,b = wilds('a b')
    val = WildsResults()
    
    if exp.match(a(b + 4), val):
      print val.a
      print val.b
  """
    if valuestore != None:
        valuestore.clear()
    d = extract(a, b)
    if d == None:
        return False
    else:
        if valuestore != None:
            for k in d:
                if d[k] == core.wild(k):
                    continue
                valuestore[k] = d[k]

        return True