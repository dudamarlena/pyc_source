# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/noval/python/parser/codeparser.py
# Compiled at: 2019-08-20 20:31:02
# Size of source mod 2**32: 16604 bytes
import ast, os, sys, nodeast, config, utils
CLASS_METHOD_NAME = 'classmethod'
STATIC_METHOD_NAME = 'staticmethod'

def GetAssignValueType(node):
    value = ''
    if type(node.value) == ast.Call:
        if type(node.value.func) == ast.Name:
            value = node.value.func.id
        elif type(node.value.func) == ast.Attribute:
            value = get_attribute_name(node.value.func)
        value_type = config.ASSIGN_TYPE_OBJECT
    else:
        value_type = GetAstType(node.value)
    if type(node.value) == ast.Name:
        value = node.value.id
    return (
     value_type, value)


def GetTupleOrListValueType(node, i):
    if type(node.value) == ast.Tuple:
        elts = node.value.elts
        return (
         GetAstType(elts[i]), '')
    return (
     config.ASSIGN_TYPE_OBJECT, '')


def GetBases(node):
    base_names = []
    for base in node.bases:
        if type(base) == ast.Name:
            base_names.append(base.id)
        elif type(base) == ast.Attribute:
            base_name = get_attribute_name(base)
            base_names.append(base_name)

    return base_names


def GetAstType(ast_type):
    if isinstance(ast_type, ast.Num):
        return config.ASSIGN_TYPE_INT
    else:
        if isinstance(ast_type, ast.Str):
            return config.ASSIGN_TYPE_STR
        if isinstance(ast_type, ast.List):
            return config.ASSIGN_TYPE_LIST
        if isinstance(ast_type, ast.Tuple):
            return config.ASSIGN_TYPE_TUPLE
        if isinstance(ast_type, ast.Dict):
            return config.ASSIGN_TYPE_DICT
        if isinstance(ast_type, ast.Name):
            return config.ASSIGN_TYPE_OBJECT
        return config.ASSIGN_TYPE_UNKNOWN


def get_attribute_name(node):
    value = node.value
    names = [node.attr]
    while type(value) == ast.Attribute:
        names.append(value.attr)
        value = value.value

    if type(value) == ast.Name:
        names.append(value.id)
    else:
        return
    return '.'.join(names[::-1])


class CodebaseParser(object):
    __doc__ = 'description of class'

    def __init__(self, deep=True):
        self._stopped = False
        self._is_analysing = False
        self._deep = deep

    def Stop(self):
        self._stopped = True

    @property
    def IsAnalysing(self):
        return self._is_analysing

    def get_node_doc(self, node):
        body = node.body
        if len(body) > 0:
            element = body[0]
            if isinstance(element, ast.Expr) and isinstance(element.value, ast.Str):
                pass
            return element.value.s

    def Parsefile(self, filepath, file_encoding='utf-8'):
        args = {}
        if utils.IsPython3():
            args['encoding'] = file_encoding
        with open(filepath, **args) as (f):
            content = f.read()
            return self.ParsefileContent(filepath, content)

    def ParsefileContent(self, filepath, content, encoding=None):
        if encoding is not None:
            content = content.encode(encoding)
        node = ast.parse(content, filepath)
        if self._stopped:
            utils.get_logger().info('user stop parse ast tree....')
            return
        return node

    def MakeElementNode(self, element, parent):
        if isinstance(element, ast.FunctionDef):
            self.WalkFuncElement(element, parent)
        else:
            if isinstance(element, ast.ClassDef):
                self.WalkClassElement(element, parent)
            else:
                if isinstance(element, ast.Assign):
                    self.WalkAssignElement(element, parent)
                else:
                    if isinstance(element, ast.Import):
                        self.WalkImportElement(element, parent)
                    else:
                        if isinstance(element, ast.ImportFrom):
                            self.WalkFromImportElement(element, parent)
                        else:
                            if isinstance(element, ast.If):
                                self.WalkIfElement(element, parent)
                            else:
                                if utils.IsPython3() and isinstance(element, ast.Try) or utils.IsPython2() and isinstance(element, ast.TryExcept):
                                    self.WalkTryExceptElement(element, parent)
                                else:
                                    if self._deep:
                                        if isinstance(element, ast.For):
                                            self.WalkForElement(element, parent)
                                    else:
                                        if isinstance(element, ast.Return):
                                            self.WalkReturnElement(element, parent)
                                        else:
                                            if isinstance(element, ast.With):
                                                self.WalkWithElement(element, parent)
                                            else:
                                                if isinstance(element, ast.While):
                                                    self.WalkWhileElement(element, parent)
                                                else:
                                                    self.AddNodeData('', element.lineno, element.col_offset, config.NODE_UNKNOWN_TYPE, parent=parent)

    def WalkReturnElement(self, element, parent):
        target = element.value
        value_type, value = config.ASSIGN_TYPE_UNKNOWN, ''
        if type(target) == ast.Tuple:
            value_type, value = config.ASSIGN_TYPE_TUPLE, ''
        else:
            if type(target) == ast.Name:
                name = target.id
                value_type, value = GetAssignValueType(element)
            elif type(target) == ast.Attribute and type(target.value) == ast.Name and target.value.id == 'self' and self.GetParentType(parent) == config.NODE_FUNCDEF_TYPE and parent.IsMethod:
                name = target.attr
                value_type, value = GetAssignValueType(element)
        self.AddNodeData('', element.lineno, element.col_offset, config.NODE_RETURN_TYPE, parent=parent, **{'value': value, 'value_type': value_type})

    def WalkFuncElement(self, element, parent):
        def_name = element.name
        line_no = element.lineno
        col = element.col_offset
        is_property_def = False
        is_class_method = False
        for deco in element.decorator_list:
            line_no += 1
            if type(deco) == ast.Name:
                if deco.id == 'property':
                    is_property_def = True
                    break
                elif deco.id == CLASS_METHOD_NAME or deco.id == STATIC_METHOD_NAME:
                    is_class_method = True
                    break

        is_method = False
        default_arg_num = len(element.args.defaults)
        arg_num = len(element.args.args)
        args = []
        for i, arg in enumerate(element.args.args):
            is_default = False
            if i >= arg_num - default_arg_num:
                is_default = True
            if type(arg) == ast.Name:
                if arg.id == 'self' and self.GetParentType(parent) == config.NODE_CLASSDEF_TYPE:
                    is_method = True
                arg_node = self.AddNodeData(arg.id, arg.lineno, arg.col_offset, config.NODE_ARG_TYPE, None, **{'is_default': is_default})
                args.append(arg_node)
            elif utils.IsPython3() and type(arg) == ast.arg:
                if arg.arg == 'self' and self.GetParentType(parent) == config.NODE_CLASSDEF_TYPE:
                    is_method = True
                arg_node = self.AddNodeData(arg.arg, arg.lineno, arg.col_offset, config.NODE_ARG_TYPE, None, **{'is_default': is_default})
                args.append(arg_node)

        if element.args.vararg is not None:
            if utils.IsPython2():
                name = element.args.vararg
            else:
                name = element.args.vararg.arg
            arg_node = self.AddNodeData(name, line_no, col, config.NODE_ARG_TYPE, None, **{'is_var': True})
            args.append(arg_node)
        if element.args.kwarg is not None:
            if utils.IsPython2():
                name = element.args.kwarg
            else:
                name = element.args.kwarg.arg
            arg_node = self.AddNodeData(name, line_no, col, config.NODE_ARG_TYPE, None, **{'is_kw': True})
            args.append(arg_node)
        doc = self.get_node_doc(element)
        func_def = self.AddNodeData(def_name, line_no, col, config.NODE_FUNCDEF_TYPE, parent, **{'doc': doc, 'is_method': is_method, 
         'is_class_method': is_class_method, 'args': args, 'is_class_property': is_property_def and is_method})
        if self._deep:
            self.WalkBody(element.body, func_def)

    def WalkClassElement(self, element, parent):
        class_name = element.name
        base_names = GetBases(element)
        line_no = element.lineno
        col = element.col_offset
        doc = self.get_node_doc(element)
        class_def = self.AddNodeData(class_name, line_no, col, config.NODE_CLASSDEF_TYPE, parent=parent, **{'bases': base_names, 'doc': doc})
        self.WalkBody(element.body, class_def)

    def WalkAssignElement(self, element, parent):
        targets = element.targets
        line_no = element.lineno
        col = element.col_offset
        for target in targets:
            if type(target) == ast.Tuple:
                elts = target.elts
                for i, elt in enumerate(elts):
                    if type(elt) == ast.Name:
                        name = elt.id
                        value_type, value = GetTupleOrListValueType(element, i)
                        self.AddNodeData(name, line_no, col, config.NODE_ASSIGN_TYPE, parent=parent, **{'value': value, 'value_type': value_type})

            else:
                if type(target) == ast.Name:
                    name = target.id
                    value_type, value = GetAssignValueType(element)
                    self.AddNodeData(name, line_no, col, config.NODE_ASSIGN_TYPE, parent=parent, **{'value': value, 'value_type': value_type})
                elif type(target) == ast.Attribute and type(target.value) == ast.Name and target.value.id == 'self' and self.GetParentType(parent) == config.NODE_FUNCDEF_TYPE and parent.IsMethod:
                    name = target.attr
                    if parent.Parent.HasChild(name):
                        if parent.Name == '__init__':
                            parent.Parent.RemoveChild(name)
                        else:
                            continue
                        value_type, value = GetAssignValueType(element)
                        self.AddNodeData(name, line_no, col, config.NODE_CLASS_PROPERTY, parent=parent, **{'value': value, 'value_type': value_type})

    def WalkImportElement(self, element, parent):
        for name in element.names:
            self.AddNodeData(name.name, element.lineno, element.col_offset, config.NODE_IMPORT_TYPE, parent=parent, **{'as_name': name.asname})

    def WalkFromImportElement(self, element, parent):
        module_name = element.module
        if utils.IsNoneOrEmpty(module_name):
            if element.level == 1:
                module_name = '.'
            elif element.level == 2:
                module_name = '..'
        else:
            if element.level == 1:
                module_name = '.' + module_name
            elif element.level == 2:
                module_name = '..' + module_name
        from_import_node = self.AddNodeData(module_name, element.lineno, element.col_offset, config.NODE_FROMIMPORT_TYPE, parent=parent)
        for name in element.names:
            self.AddNodeData(name.name, element.lineno, element.col_offset, config.NODE_IMPORT_TYPE, parent=from_import_node, **{'as_name': name.asname, 'root': parent})

    def WalkIfElement(self, element, parent):
        if isinstance(element.test, ast.Compare) and isinstance(element.test.left, ast.Name) and element.test.left.id == '__name__' and len(element.test.ops) > 0 and isinstance(element.test.ops[0], ast.Eq) and len(element.test.comparators) > 0 and isinstance(element.test.comparators[0], ast.Str) and element.test.comparators[0].s == nodeast.MainFunctionNode.MAIN_FUNCTION_NAME:
            self.AddNodeData('', element.lineno, element.col_offset, config.NODE_MAIN_FUNCTION_TYPE, parent=parent)
        else:
            self.AddNodeData('', element.lineno, element.col_offset, config.NODE_UNKNOWN_TYPE, parent=parent)
        self.WalkBody(element.body, parent)
        for orelse in element.orelse:
            self.MakeElementNode(orelse, parent)

    def WalkTryExceptElement(self, element, parent):
        self.WalkBody(element.body, parent)
        for handler in element.handlers:
            self.WalkBody(handler.body, parent)

    def WalkBody(self, body, parent):
        for child in body:
            self.MakeElementNode(child, parent)

    def WalkWhileElement(self, element, parent):
        self.WalkBody(element.body, parent)

    def WalkForElement(self, element, parent):
        self.WalkBody(element.body, parent)

    def WalkWithElement(self, element, parent):
        self.WalkBody(element.body, parent)

    def AddNodeData(self, name, lineno, col, node_type, parent, **kwargs):
        raise NotImplementedError('AddNodeData not implemented in base class')

    def GetParentType(self, parent):
        raise NotImplementedError('GetParentType not implemented in base class')


class CodeParser(CodebaseParser):

    def ParsefileContent(self, filepath, content, encoding=None):
        node = CodebaseParser.ParsefileContent(self, filepath, content, encoding)
        doc = self.get_node_doc(node)
        module = nodeast.Module(os.path.basename(filepath).split('.')[0], filepath, doc)
        self.WalkBody(node.body, module)
        nodeast.BuiltinImportNode(module)
        return module

    def AddNodeData(self, name, lineno, col, node_type, parent, **kwargs):
        if node_type == config.NODE_CLASS_PROPERTY:
            return nodeast.PropertyDef(name, lineno, col, parent=parent, **kwargs)
        else:
            if node_type == config.NODE_ARG_TYPE:
                return nodeast.ArgNode(name, lineno, col, parent=parent, **kwargs)
            if node_type == config.NODE_FUNCDEF_TYPE:
                return nodeast.FuncDef(name, lineno, col, parent=parent, **kwargs)
            if node_type == config.NODE_CLASSDEF_TYPE:
                return nodeast.ClassDef(name, lineno, col, parent=parent, **kwargs)
            if node_type == config.NODE_IMPORT_TYPE:
                if 'root' in kwargs:
                    kwargs.pop('root')
                return nodeast.ImportNode(name, lineno, col, parent=parent, **kwargs)
            if node_type == config.NODE_FROMIMPORT_TYPE:
                return nodeast.FromImportNode(name, lineno, col, parent=parent)
            if node_type == config.NODE_MAIN_FUNCTION_TYPE:
                return nodeast.MainFunctionNode(lineno, col, parent)
            if node_type == config.NODE_ASSIGN_TYPE:
                return nodeast.AssignDef(name, lineno, col, parent=parent, **kwargs)
            if node_type == config.NODE_RETURN_TYPE:
                return nodeast.ReturnNode(name, lineno, col, parent=parent, **kwargs)
            return nodeast.UnknownNode(lineno, col, parent)

    def GetParentType(self, parent):
        return parent.Type