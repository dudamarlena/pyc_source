# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-intel/egg/scxml/datamodel.py
# Compiled at: 2011-12-09 05:02:34
"""
Created on Nov 1, 2011

@author: johan
"""
from eventprocessor import Event
import sys, traceback
from errors import ExprEvalError, DataModelError
import eventlet, re
try:
    from PyV8 import JSContext, JSLocker, JSUnlocker
except:
    pass

assignOnce = [
 '_sessionid', '_x', '_name', '_ioprocessors']
hidden = ['_event']

def getTraceback():
    tb_list = traceback.extract_tb(sys.exc_info()[2])
    tb_list = [ (lineno, fname, text) for filename, lineno, fname, text in tb_list if filename == '<string>' and fname != '<module>'
              ]
    return tb_list


def exceptionFormatter(f):

    def wrapper(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except Exception as e:
            traceback = getTraceback()
            raise ExprEvalError(e, traceback)

    return wrapper


class DataModel(dict):

    def __init__(self, *args, **kwargs):
        dict.__init__(self, *args, **kwargs)

    def __setitem__(self, key, val):
        if key in assignOnce and key in self or key in hidden or not self.isLegalName(key):
            raise DataModelError("You can't assign to the name '%s'." % key)
        else:
            dict.__setitem__(self, key, val)

    def __getitem__(self, key):
        if key in hidden:
            return dict.__getitem__(self, '_' + key)
        return dict.__getitem__(self, key)

    def hasLocation(self, location):
        try:
            eval(location, self)
            return True
        except:
            return False

    def isLegalName(self, name):
        return bool(re.match('[a-zA-Z_][0-9a-zA-Z_]*', name))

    @exceptionFormatter
    def evalExpr(self, expr):
        return eval(expr, self)

    @exceptionFormatter
    def execExpr(self, expr):
        exec expr in self


class ECMAScriptDataModel(object):

    def __init__(self):

        class GlobalEcmaContext(object):
            pass

        self.g = GlobalEcmaContext()

    def __setitem__(self, key, val):
        if key in assignOnce and key in self or key in hidden or not self.isLegalName(key):
            raise DataModelError("You can't assign to the name '%s'." % key)
        else:
            if key == '__event':
                key = '_event'
            setattr(self.g, key, val)

    def __getitem__(self, key):
        return getattr(self.g, key)

    def __contains__(self, key):
        return hasattr(self.g, key)

    def __str__(self):
        return str(self.g.__dict__)

    def keys(self):
        return self.g.__dict__.keys()

    def hasLocation(self, location):
        return self.evalExpr("typeof(%s) != 'undefined'" % location)

    def isLegalName(self, name):
        return bool(re.match('[a-zA-Z_$][0-9a-zA-Z_$]*', name))

    def evalExpr(self, expr):
        with JSContext(self.g) as (c):
            try:
                ret = c.eval(expr)
            except Exception as e:
                raise ExprEvalError(e, [])

            for key in c.locals.keys():
                setattr(self.g, key, c.locals[key])

            return ret

    def execExpr(self, expr):
        self.evalExpr(expr)


if __name__ == '__main__':
    import PyV8
    d = DataModel()
    d['__event'] = Event('yeah')
    print 'scxml' == d.evalExpr('_event').origintype
    sys.exit()
    try:
        d.evalExpr('g()')
    except Exception as e:
        print e