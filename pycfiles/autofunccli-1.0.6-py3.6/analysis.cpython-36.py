# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/autofunccli/analysis.py
# Compiled at: 2020-05-04 17:26:08
# Size of source mod 2**32: 17942 bytes
"""
Script containing the funciton analysis process
"""
from inspect import getfullargspec, isfunction
import re, argparse
from typing import Tuple, List
from enum import Enum
acceptedTypes = [
 bool,
 int,
 float,
 str,
 List,
 Tuple]
acceptedTypesArg = [
 bool,
 int,
 float,
 str]
acceptedSubClass = [
 Enum]

def typeRep(t):
    """
    Return a string representing a type
    """
    try:
        if t == None:
            return '?'
        else:
            return t.__name__
    except:
        return '?'


class UnsupportedTypeException(Exception):
    __doc__ = "\n    Exception to throw when a function argument doesn't have a supported type.\n    "

    def __init__(self, t, n):
        self.t = t
        self.n = n

    def __str__(self):
        out = '{} argument has type {} which is not accepted.'.format(self.n, self.t)
        out += '\nAccepted types are : {}'.format([str(e) for e in acceptedTypes])
        out += '\nAccepted type arguments are {}'.format([str(e) for e in acceptedTypesArg])
        return out


class WrongInputTypeException(Exception):
    __doc__ = "\n    Exception to throw when the input can't use to build an object from the argument type\n    "

    def __init__(self, n, value):
        self.n = n
        self.value = value

    def __str__(self):
        return "Argument {} doesn't have the right type, input is {}, check the -h.".format(self.n, self.value)


class NonHomogenousEnumTypeException(Exception):
    __doc__ = "\n    Exception to throw when an Enum type is use and doesn't have values with the same type.\n    "

    def __init__(self, n, types):
        self.n = n
        self.types = types

    def __str__(self):
        return "Argument Enum {} doesn't have homogenous types {}, each values of the enum must be the same.".format(self.n, self.types)


class EnumHasNoTypeException(Exception):
    __doc__ = "\n    Exception to throw when an Enum type is use and doesn't have any definied value.\n    "

    def __init__(self, n, t):
        self.n = n
        self.t = t

    def __str__(self):
        return "Enum type {} of argument {} doesn't have any value.".format(self.t, self.n)


class IsNotAFunctionException(Exception):
    __doc__ = '\n    Exception to throw when the input is not a function\n    '

    def __str__(self):
        return 'Argument is not a function.'


class FunctionArgument:
    __doc__ = '\n    Simple class to group informations about a function argument obtained with\n    the inspect module\n    '

    def __init__(self, name, t, default, doc, index):
        self.name = name
        self.type = t
        self.default = default
        self.doc = doc
        self.index = index


class CommandArgument:
    __doc__ = '\n    Class to transform a function argument to an usable argument for the\n    argparse.add_argument method.\n    '

    @staticmethod
    def __buildType(t, default, name):
        """
        Analyse the type of a function argument and add parameters.
        list : nargs='*'
        optional : nargs='?'
        tuple[x,y...] : nargs='len(tuple)'
        add automatic argument parsing using builtin types.
        """
        aType = [str(c) for c in acceptedTypes]
        aArgType = [str(c) for c in acceptedTypesArg]
        subClsType = set([str(c) for c in acceptedSubClass])
        parse = t
        representation = ''
        action = None
        nargs = None
        nDefault = default

        class typeManagement:
            __doc__ = '\n            Class to manipulate informations about function argument\n            and get command argument.\n            '

            class parameters:
                __doc__ = '\n                Class to group informations about command argument\n                '

                def __init__(self, t, default):
                    self.parse = t
                    self.representation = ''
                    self.action = None
                    self.nargs = None
                    self.default = default
                    self.choices = None

                def toArr(self):
                    out = [
                     self.parse]
                    out += [self.representation]
                    out += [self.action]
                    out += [self.nargs]
                    out += [self.default]
                    out += [self.choices]
                    return out

            def __init__(self, t, default):
                self.t = t
                self.default = default
                self.parameters = typeManagement.parameters(t, default)

            def toTuple(self):
                """
                Transform the function argument to a tuple command argument :
                        - nargs : length of the tuple type list
                        - parse : parse each values with the corresponding types
                        - represention : show the tuple types
                """
                self.parameters.nargs = len(self.t.__args__)
                self.parameters.parse = lambda src: tuple([self.t.__args__[i](x) for i, x in enumerate(src)])
                self.parameters.representation = ','.join([typeRep(x) for i, x in enumerate(self.t.__args__)])

            def toList(self):
                """
                Transform the function argument to a list command argument :
                        - nargs : '+'
                        - parse : parse each values with the list type
                        - represention : show the list type
                """
                self.parameters.nargs = '+'
                self.parameters.parse = lambda src: [self.t.__args__[0](x) for i, x in enumerate(src)]
                self.parameters.representation = 'List[{}]'.format(typeRep(self.t.__args__[0]))

            def toChoices(self):
                enumTypes = set([type(e.value) for e in self.t])
                if len(enumTypes) > 1:
                    raise NonHomogenousEnumTypeException(name, set([type(e.value) for e in self.t]))
                if len(enumTypes) == 0:
                    raise EnumHasNoTypeException(name, self.t)
                enumType = enumTypes.pop()
                if str(enumType) not in aType:
                    raise UnsupportedTypeException(enumType, name)
                self.parameters.choices = [str(e.value) for e in self.t]
                self.parameters.parse = lambda src: self.t(enumType(src))

            def toBool(self):
                """
                Transform the function argument to a boolean command argument :
                        - represention : show the boolean type
                        - if the default value is True use 'store_false' as action else 'store_true'
                """
                if self.default:
                    self.parameters.action = 'store_false'
                else:
                    self.parameters.action = 'store_true'
                    self.parameters.default = False
                self.parameters.representation = typeRep(self.t)

            def toType(self):
                """
                Transform the function argument to a simple command argument :
                        - parse : type of the function argument
                        - represention : type of the function argument
                """
                self.parameters.parse = self.t
                self.parameters.representation = typeRep(self.t)

            def toOther(self):
                """
                If there is no type, convert it to a string
                """
                self.parameters.parse = str
                self.parameters.representation = typeRep(str)

            def analyse(self):
                switchGeneric = {Tuple: self.toTuple, 
                 List: self.toList}
                if self.t != None and type(self.t) != type(None):
                    baseTypes = set([str(b) for b in self.t.__bases__]) if hasattr(self.t, '__bases__') else []
                    if hasattr(t, '__args__'):
                        if t.__origin__ in switchGeneric:
                            genBaseTypes = set([str(c) for c in t.__args__ if str(c) not in aArgType])
                            if len([c for c in t.__args__ if str(c) not in aArgType]) > 0:
                                raise UnsupportedTypeException(self.t, name)
                            switchGeneric[t.__origin__]()
                        else:
                            raise UnsupportedTypeException(self.t, name)
                    else:
                        if str(self.t) not in aType:
                            if not baseTypes.intersection(subClsType):
                                raise UnsupportedTypeException(self.t, name)
                        if baseTypes.intersection(subClsType) == {str(Enum)}:
                            self.toChoices()
                        else:
                            if self.t == bool:
                                self.toBool()
                            else:
                                self.toType()
                else:
                    self.toOther()
                return self.parameters.toArr()

        return typeManagement(t, default).analyse()

    @staticmethod
    def __buildHelp(fArg: FunctionArgument, rep, default):
        """
        Generate the help command argument
        """
        return fArg.doc + (' : <' + rep + '>' if rep else '') + ('(' + str(default) + ')' if default != None else '')

    previousName = set()

    def __init__(self, fArg: FunctionArgument):
        self.parse, representation, self.action, self.nargs, self.default, self.choices = CommandArgument._CommandArgument__buildType(fArg.type, fArg.default, fArg.name)
        self.name = [fArg.name] if self.default == None else [
         '-' + fArg.name[0], '--' + fArg.name]
        if len(self.name) > 1:
            if len(CommandArgument.previousName.intersection({self.name[0]})) > 0:
                self.name = [
                 self.name[1]]
            else:
                CommandArgument.previousName.add(self.name[0])
        self.help = CommandArgument._CommandArgument__buildHelp(fArg, representation, self.default)

    def toCommand(self):
        out = {'help': self.help}
        if self.action:
            out.update({'action': self.action})
        else:
            if self.choices:
                out.update({'choices': self.choices})
            else:
                out.update({'type': str})
        if self.default != None:
            out.update({'default': self.default})
        if self.nargs:
            out.update({'nargs': self.nargs})
        return out


class FunctionReturn:
    __doc__ = '\n    class for representing the return type and documentation of a function\n    '

    def __init__(self, t, doc):
        self.type = t
        self.doc = doc


class FunctionArgParser:
    __doc__ = '\n    Parse a function to extract arguments,annotations and documentation\n    to build an argparser from it.\n    '
    _FunctionArgParser__paramReg = re.compile(':\\s*(\\w+)\\s*(\\w*)\\s*:(.*)\\n?')

    @staticmethod
    def __extractDoc(func):
        """
        Return the description of the function and its parameters using
        the doc.
        """
        if not isfunction(func):
            raise IsNotAFunctionException()
        doc = func.__doc__
        params = FunctionArgParser._FunctionArgParser__paramReg.findall(doc) if doc else ''
        desc = doc[0:FunctionArgParser._FunctionArgParser__paramReg.search(doc).span()[0]] if (doc and FunctionArgParser._FunctionArgParser__paramReg.search(doc)) else doc
        desc = '\n'.join([s.strip() for s in desc.split('\n')]) if doc else ''
        retDesc = ''
        paramsDesc = {}
        for i in params:
            if i[0] == 'param':
                paramsDesc[i[1]] = i[2].strip()
            if i[0] == 'return':
                retDesc = i[2].strip()

        return (
         desc, paramsDesc, retDesc)

    @staticmethod
    def __extractArgs(func, argDoc, retDoc):
        """
        return informations of the function and transform them to command arguments
        """
        args = []
        spec = getfullargspec(func)
        defautls_set = spec.defaults if spec.defaults else []
        annotations = spec.annotations if spec.annotations else []
        varNames = spec.args
        types = {d:None for d in varNames}
        types.update({'return': None})
        for k in types:
            if k in annotations:
                types[k] = annotations[k]

        defaults = {d:None for d in varNames}
        for i in range(len(varNames) - len(defautls_set), len(varNames)):
            defaults[varNames[i]] = defautls_set[(i - len(defautls_set))]

        index = {}
        for i in range(0, len(varNames)):
            index[varNames[i]] = i

        for n in varNames:
            if n not in argDoc:
                argDoc[n] = ''
            else:
                if n not in types:
                    types[n] = str
                if n not in defaults:
                    defaults[n] = None
            args.append(FunctionArgument(n, types[n], defaults[n], argDoc[n], index[n]))

        returned = FunctionReturn(types['return'], retDoc)
        return (args, returned)

    def __init__(self, func):
        CommandArgument.previousName = set()
        self.argList = []
        self.ref = func
        self.name = func.__name__
        self.doc, argDoc, retDoc = FunctionArgParser._FunctionArgParser__extractDoc(func)
        self.argList, self.ret = FunctionArgParser._FunctionArgParser__extractArgs(func, argDoc, retDoc)
        self.commandList = [CommandArgument(a) for a in self.argList]
        self.postParse = {self.argList[i].name:x.parse for i, x in enumerate(self.commandList)}
        if self.ret:
            self.epilog = '\n\t[RETURN] '
            self.epilog += self.ret.doc if self.ret.doc else ''
            self.epilog += ': <' + typeRep(self.ret.type) + '>' if self.ret.type else ''

    def toArgParse(self):
        """
        Convert the analyzed function to an argparser.
        """
        parser = argparse.ArgumentParser(description=(self.doc),
          epilog=(self.epilog))
        for arg in self.commandList:
            (parser.add_argument)(*arg.name, **arg.toCommand())

        return parser

    def parse(self, *arg, **kwargs):
        """
        Parse an input using the function parser and return the result
        If there is no input, try to parse sys.argv.
        """
        parser = self.toArgParse()
        if parser:
            parsed = (parser.parse_args)(*arg, **kwargs)
            out = {}
            if parsed:
                for k, value in parsed._get_kwargs():
                    try:
                        out.update({k: self.postParse[k](value)})
                    except:
                        raise WrongInputTypeException(k, value)

            return (self.ref)(**out)

    def __call__(self, *arg, **kwargs):
        (self.ref)(*arg, **kwargs)

    def main(self, __name__):
        if __name__ == '__main__':
            return self.parse()
        else:
            return