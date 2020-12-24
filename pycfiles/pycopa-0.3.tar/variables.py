# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build\bdist.win32\egg\pycoon\variables.py
# Compiled at: 2007-03-10 11:34:46
__author__ = 'Andrey Nordin <mailto:anrienord@inbox.ru>'
import re, logging

def getResolver(expr):
    if needsResolve(expr):
        return PreparedVariableResolver(expr)
    else:
        return NopVariableResolver(expr)


def buildMap(exprs, context, objectModel):
    return dict(((k.resolve(context, objectModel), v.resolve(context, objectModel)) for (k, v) in exprs.items()))


def needsResolve(expr):
    if expr is None or len(expr) == 0:
        return False
    if expr[0] == '{':
        return True
    if len(expr) < 2:
        return False
    pos = 1
    pos = expr.find('{', pos)
    while pos != -1:
        if expr[(pos - 1)] != '\\':
            return True
        pos = expr.find('{', pos + 1)

    return False


class VariableResolver:
    __module__ = __name__

    def __init__(self, expr):
        self.expr = expr

    def resolve(self, context, objectModel):
        raise NotImplementedError()


class NopVariableResolver(VariableResolver):
    __module__ = __name__

    def resolve(self, context, objectModel):
        return self.expr


class PreparedVariableResolver(VariableResolver):
    __module__ = __name__

    def resolve(self, context, objectModel):
        vars = re.findall('{([^}]*)}', self.expr)
        if len(vars) > 0 and len(context.mapStack) == 0:
            raise Exception('There are variables to be resolved, but the context stack is empty')
        expr = self.expr
        for v in vars:
            if v.find(':') != -1:
                (scheme, name) = v.split(':', 1)
                mgr = objectModel['processor'].componentManager
                m = mgr.getComponent('input-module', scheme)
                subst = m.get(name, objectModel, '')
            else:
                subst = context.mapStack[(-1)].get(v, '')
            expr = re.sub('\\{%s}' % v, subst, expr)

        return expr


class InputModule(object):
    __module__ = __name__

    def configure(self, element=None):
        if element is not None:
            self.log = logging.getLogger(element.get('logger'))
        return

    def get(self, name, objectModel, default=None):
        return NotImplementedError()


class RequestParameterModule(InputModule):
    __module__ = __name__

    def get(self, name, objectModel, default=None):
        encoding = objectModel['request'].formEncoding
        param = objectModel['request'].params.get(name, default)
        if encoding is not None:
            return param.decode(encoding)
        else:
            return param
        return


class GlobalInputModule(InputModule):
    __module__ = __name__

    def get(self, name, objectModel, default=None):
        ret = default
        processor = objectModel['processor']
        while processor is not None:
            confs = processor.componentConfigurations
            if confs is not None:
                e = confs.find('global-variables/%s' % name)
                if e is not None:
                    ret = e.text
            processor = processor.parent

        return ret