# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/qt/work/pyside/pyside-setup/pyside2_install/py2.7-qt5.14.2-64bit-release/lib/python2.7/site-packages/shiboken2/files.dir/shibokensupport/signature/layout.py
# Compiled at: 2020-03-30 06:40:47
from __future__ import print_function, absolute_import
from textwrap import dedent
from shibokensupport.signature import inspect, typing
from shibokensupport.signature.mapping import ellipsis
from shibokensupport.signature.lib.tool import SimpleNamespace

class SignatureLayout(SimpleNamespace):
    """
    Configure a signature.

    The layout of signatures can have different layouts which are
    controlled by keyword arguments:

    definition=True         Determines if self will generated.
    defaults=True
    ellipsis=False          Replaces defaults by "...".
    return_annotation=True
    parameter_names=True    False removes names before ":".
    """
    allowed_keys = SimpleNamespace(definition=True, defaults=True, ellipsis=False, return_annotation=True, parameter_names=True)
    allowed_values = (True, False)

    def __init__(self, **kwds):
        args = SimpleNamespace(**self.allowed_keys.__dict__)
        args.__dict__.update(kwds)
        self.__dict__.update(args.__dict__)
        err_keys = list(set(self.__dict__) - set(self.allowed_keys.__dict__))
        if err_keys:
            self._attributeerror(err_keys)
        err_values = list(set(self.__dict__.values()) - set(self.allowed_values))
        if err_values:
            self._valueerror(err_values)

    def __setattr__(self, key, value):
        if key not in self.allowed_keys.__dict__:
            self._attributeerror([key])
        if value not in self.allowed_values:
            self._valueerror([value])
        self.__dict__[key] = value

    def _attributeerror(self, err_keys):
        err_keys = (', ').join(err_keys)
        allowed_keys = (', ').join(self.allowed_keys.__dict__.keys())
        raise AttributeError(dedent(("            Not allowed: '{err_keys}'.\n            The only allowed keywords are '{allowed_keys}'.\n            ").format(**locals())))

    def _valueerror(self, err_values):
        err_values = (', ').join(map(str, err_values))
        allowed_values = (', ').join(map(str, self.allowed_values))
        raise ValueError(dedent(("            Not allowed: '{err_values}'.\n            The only allowed values are '{allowed_values}'.\n            ").format(**locals())))


signature = SignatureLayout()
existence = SignatureLayout(definition=False, defaults=False, return_annotation=False, parameter_names=False)
hintingstub = SignatureLayout(ellipsis=True)
typeerror = SignatureLayout(definition=False, return_annotation=False, parameter_names=False)

def define_nameless_parameter():
    """
    Create Nameless Parameters

    A nameless parameter has a reduced string representation.
    This is done by cloning the parameter type and overwriting its
    __str__ method. The inner structure is still a valid parameter.
    """

    def __str__(self):
        klass = self.__class__
        self.__class__ = P
        txt = P.__str__(self)
        self.__class__ = klass
        txt = txt[txt.index(':') + 1:].strip() if ':' in txt else txt
        return txt

    P = inspect.Parameter
    newname = 'NamelessParameter'
    bases = P.__bases__
    body = dict(P.__dict__)
    if '__slots__' in body:
        for name in body['__slots__']:
            del body[name]

    body['__str__'] = __str__
    return type(newname, bases, body)


NamelessParameter = define_nameless_parameter()

def make_signature_nameless(signature):
    """
    Make a Signature Nameless

    We use an existing signature and change the type of its parameters.
    The signature looks different, but is totally intact.
    """
    for key in signature.parameters.keys():
        signature.parameters[key].__class__ = NamelessParameter


_POSITIONAL_ONLY = inspect._POSITIONAL_ONLY
_POSITIONAL_OR_KEYWORD = inspect._POSITIONAL_OR_KEYWORD
_VAR_POSITIONAL = inspect._VAR_POSITIONAL
_KEYWORD_ONLY = inspect._KEYWORD_ONLY
_VAR_KEYWORD = inspect._VAR_KEYWORD
_empty = inspect._empty

def create_signature(props, key):
    if not props:
        return
    if isinstance(props['multi'], list):
        return list(create_signature(elem, key) for elem in props['multi'])
    else:
        if type(key) is tuple:
            sig_kind, modifier = key
        else:
            sig_kind, modifier = key, 'signature'
        layout = globals()[modifier]
        if not isinstance(layout, SignatureLayout):
            raise SystemError('Modifiers must be names of a SignatureLayout instance')
        varnames = props['varnames']
        if layout.definition:
            if sig_kind == 'function':
                pass
            elif sig_kind == 'method':
                varnames = ('self', ) + varnames
            elif sig_kind == 'staticmethod':
                pass
            elif sig_kind == 'classmethod':
                varnames = ('klass', ) + varnames
            else:
                raise SystemError('Methods must be function, method, staticmethod or classmethod')
        defaults = props['defaults'][:]
        if not layout.defaults:
            defaults = ()
        annotations = props['annotations'].copy()
        if not layout.return_annotation and 'return' in annotations:
            del annotations['return']
        kind = inspect._POSITIONAL_OR_KEYWORD
        params = []
        for idx, name in enumerate(varnames):
            if name.startswith('**'):
                kind = _VAR_KEYWORD
            elif name.startswith('*'):
                kind = _VAR_POSITIONAL
            ann = annotations.get(name, _empty)
            name = name.lstrip('*')
            defpos = idx - len(varnames) + len(defaults)
            default = defaults[defpos] if defpos >= 0 else _empty
            if default is None:
                ann = typing.Optional[ann]
            if default is not _empty and layout.ellipsis:
                default = ellipsis
            param = inspect.Parameter(name, kind, annotation=ann, default=default)
            params.append(param)
            if kind == _VAR_POSITIONAL:
                kind = _KEYWORD_ONLY

        sig = inspect.Signature(params, return_annotation=annotations.get('return', _empty), __validate_parameters__=False)
        if not layout.parameter_names:
            make_signature_nameless(sig)
        return sig