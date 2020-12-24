# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-x0nyl_ya/pyflakes/pyflakes/checker.py
# Compiled at: 2019-07-30 18:47:05
# Size of source mod 2**32: 61215 bytes
"""
Main module.

Implement the central Checker class.
Also, it models the Bindings and Scopes.
"""
import __future__, ast, bisect, collections, doctest, functools, os, re, sys, tokenize
from pyflakes import messages
PY2 = sys.version_info < (3, 0)
PY35_PLUS = sys.version_info >= (3, 5)
PY36_PLUS = sys.version_info >= (3, 6)
PY38_PLUS = sys.version_info >= (3, 8)
try:
    sys.pypy_version_info
    PYPY = True
except AttributeError:
    PYPY = False

builtin_vars = dir(__import__('__builtin__' if PY2 else 'builtins'))
if PY2:
    tokenize_tokenize = tokenize.generate_tokens
else:
    tokenize_tokenize = tokenize.tokenize
if PY2:

    def getNodeType(node_class):
        return str(unicode(node_class.__name__).upper())


    def get_raise_argument(node):
        return node.type


else:

    def getNodeType(node_class):
        return node_class.__name__.upper()


    def get_raise_argument(node):
        return node.exc


    unicode = str
if PY2:

    def getAlternatives(n):
        if isinstance(n, (ast.If, ast.TryFinally)):
            return [
             n.body]
        if isinstance(n, ast.TryExcept):
            return [
             n.body + n.orelse] + [[hdl] for hdl in n.handlers]


else:

    def getAlternatives(n):
        if isinstance(n, ast.If):
            return [
             n.body]
        if isinstance(n, ast.Try):
            return [
             n.body + n.orelse] + [[hdl] for hdl in n.handlers]


if PY35_PLUS:
    FOR_TYPES = (
     ast.For, ast.AsyncFor)
    LOOP_TYPES = (ast.While, ast.For, ast.AsyncFor)
else:
    FOR_TYPES = (
     ast.For,)
    LOOP_TYPES = (ast.While, ast.For)
TYPE_COMMENT_RE = re.compile('^#\\s*type:\\s*')
TYPE_IGNORE_RE = re.compile(TYPE_COMMENT_RE.pattern + 'ignore\\s*(#|$)')
TYPE_FUNC_RE = re.compile('^(\\(.*?\\))\\s*->\\s*(.*)$')

class _FieldsOrder(dict):
    __doc__ = 'Fix order of AST node fields.'

    def _get_fields(self, node_class):
        fields = node_class._fields
        if 'iter' in fields:
            key_first = 'iter'.find
        else:
            if 'generators' in fields:
                key_first = 'generators'.find
            else:
                key_first = 'value'.find
        return tuple(sorted(fields, key=key_first, reverse=True))

    def __missing__(self, node_class):
        self[node_class] = fields = self._get_fields(node_class)
        return fields


def counter(items):
    """
    Simplest required implementation of collections.Counter. Required as 2.6
    does not have Counter in collections.
    """
    results = {}
    for item in items:
        results[item] = results.get(item, 0) + 1

    return results


def iter_child_nodes(node, omit=None, _fields_order=_FieldsOrder()):
    """
    Yield all direct child nodes of *node*, that is, all fields that
    are nodes and all items of fields that are lists of nodes.

    :param node:          AST node to be iterated upon
    :param omit:          String or tuple of strings denoting the
                          attributes of the node to be omitted from
                          further parsing
    :param _fields_order: Order of AST node fields
    """
    for name in _fields_order[node.__class__]:
        if omit:
            if name in omit:
                continue
        field = getattr(node, name, None)
        if isinstance(field, ast.AST):
            yield field
        else:
            if isinstance(field, list):
                for item in field:
                    yield item


def convert_to_value(item):
    if isinstance(item, ast.Str):
        return item.s
    else:
        if hasattr(ast, 'Bytes'):
            if isinstance(item, ast.Bytes):
                return item.s
            else:
                if isinstance(item, ast.Tuple):
                    return tuple(convert_to_value(i) for i in item.elts)
                if isinstance(item, ast.Num):
                    return item.n
            if isinstance(item, ast.Name):
                result = VariableKey(item=item)
                constants_lookup = {'True':True, 
                 'False':False, 
                 'None':None}
                return constants_lookup.get(result.name, result)
        else:
            if not PY2:
                if isinstance(item, ast.NameConstant):
                    return item.value
        return UnhandledKeyType()


def is_notimplemented_name_node(node):
    return isinstance(node, ast.Name) and getNodeName(node) == 'NotImplemented'


class Binding(object):
    __doc__ = '\n    Represents the binding of a value to a name.\n\n    The checker uses this to keep track of which names have been bound and\n    which names have not. See L{Assignment} for a special type of binding that\n    is checked with stricter rules.\n\n    @ivar used: pair of (L{Scope}, node) indicating the scope and\n                the node that this binding was last used.\n    '

    def __init__(self, name, source):
        self.name = name
        self.source = source
        self.used = False

    def __str__(self):
        return self.name

    def __repr__(self):
        return '<%s object %r from line %r at 0x%x>' % (self.__class__.__name__,
         self.name,
         self.source.lineno,
         id(self))

    def redefines(self, other):
        return isinstance(other, Definition) and self.name == other.name


class Definition(Binding):
    __doc__ = '\n    A binding that defines a function or a class.\n    '


class Builtin(Definition):
    __doc__ = 'A definition created for all Python builtins.'

    def __init__(self, name):
        super(Builtin, self).__init__(name, None)

    def __repr__(self):
        return '<%s object %r at 0x%x>' % (self.__class__.__name__,
         self.name,
         id(self))


class UnhandledKeyType(object):
    __doc__ = '\n    A dictionary key of a type that we cannot or do not check for duplicates.\n    '


class VariableKey(object):
    __doc__ = '\n    A dictionary key which is a variable.\n\n    @ivar item: The variable AST object.\n    '

    def __init__(self, item):
        self.name = item.id

    def __eq__(self, compare):
        return compare.__class__ == self.__class__ and compare.name == self.name

    def __hash__(self):
        return hash(self.name)


class Importation(Definition):
    __doc__ = '\n    A binding created by an import statement.\n\n    @ivar fullName: The complete name given to the import statement,\n        possibly including multiple dotted components.\n    @type fullName: C{str}\n    '

    def __init__(self, name, source, full_name=None):
        self.fullName = full_name or name
        self.redefined = []
        super(Importation, self).__init__(name, source)

    def redefines(self, other):
        if isinstance(other, SubmoduleImportation):
            return self.fullName == other.fullName
        else:
            return isinstance(other, Definition) and self.name == other.name

    def _has_alias(self):
        """Return whether importation needs an as clause."""
        return not self.fullName.split('.')[(-1)] == self.name

    @property
    def source_statement(self):
        """Generate a source statement equivalent to the import."""
        if self._has_alias():
            return 'import %s as %s' % (self.fullName, self.name)
        else:
            return 'import %s' % self.fullName

    def __str__(self):
        """Return import full name with alias."""
        if self._has_alias():
            return self.fullName + ' as ' + self.name
        else:
            return self.fullName


class SubmoduleImportation(Importation):
    __doc__ = "\n    A binding created by a submodule import statement.\n\n    A submodule import is a special case where the root module is implicitly\n    imported, without an 'as' clause, and the submodule is also imported.\n    Python does not restrict which attributes of the root module may be used.\n\n    This class is only used when the submodule import is without an 'as' clause.\n\n    pyflakes handles this case by registering the root module name in the scope,\n    allowing any attribute of the root module to be accessed.\n\n    RedefinedWhileUnused is suppressed in `redefines` unless the submodule\n    name is also the same, to avoid false positives.\n    "

    def __init__(self, name, source):
        assert '.' in name and (not source or isinstance(source, ast.Import))
        package_name = name.split('.')[0]
        super(SubmoduleImportation, self).__init__(package_name, source)
        self.fullName = name

    def redefines(self, other):
        if isinstance(other, Importation):
            return self.fullName == other.fullName
        else:
            return super(SubmoduleImportation, self).redefines(other)

    def __str__(self):
        return self.fullName

    @property
    def source_statement(self):
        return 'import ' + self.fullName


class ImportationFrom(Importation):

    def __init__(self, name, source, module, real_name=None):
        self.module = module
        self.real_name = real_name or name
        if module.endswith('.'):
            full_name = module + self.real_name
        else:
            full_name = module + '.' + self.real_name
        super(ImportationFrom, self).__init__(name, source, full_name)

    def __str__(self):
        """Return import full name with alias."""
        if self.real_name != self.name:
            return self.fullName + ' as ' + self.name
        else:
            return self.fullName

    @property
    def source_statement(self):
        if self.real_name != self.name:
            return 'from %s import %s as %s' % (self.module,
             self.real_name,
             self.name)
        else:
            return 'from %s import %s' % (self.module, self.name)


class StarImportation(Importation):
    __doc__ = "A binding created by a 'from x import *' statement."

    def __init__(self, name, source):
        super(StarImportation, self).__init__('*', source)
        self.name = name + '.*'
        self.fullName = name

    @property
    def source_statement(self):
        return 'from ' + self.fullName + ' import *'

    def __str__(self):
        if self.fullName.endswith('.'):
            return self.source_statement
        else:
            return self.name


class FutureImportation(ImportationFrom):
    __doc__ = '\n    A binding created by a from `__future__` import statement.\n\n    `__future__` imports are implicitly used.\n    '

    def __init__(self, name, source, scope):
        super(FutureImportation, self).__init__(name, source, '__future__')
        self.used = (scope, source)


class Argument(Binding):
    __doc__ = '\n    Represents binding a name as an argument.\n    '


class Assignment(Binding):
    __doc__ = "\n    Represents binding a name with an explicit assignment.\n\n    The checker will raise warnings for any Assignment that isn't used. Also,\n    the checker does not consider assignments in tuple/list unpacking to be\n    Assignments, rather it treats them as simple Bindings.\n    "


class FunctionDefinition(Definition):
    pass


class ClassDefinition(Definition):
    pass


class ExportBinding(Binding):
    __doc__ = "\n    A binding created by an C{__all__} assignment.  If the names in the list\n    can be determined statically, they will be treated as names for export and\n    additional checking applied to them.\n\n    The only recognized C{__all__} assignment via list concatenation is in the\n    following format:\n\n        __all__ = ['a'] + ['b'] + ['c']\n\n    Names which are imported and not otherwise used but appear in the value of\n    C{__all__} will not have an unused import warning reported for them.\n    "

    def __init__(self, name, source, scope):
        if '__all__' in scope:
            if isinstance(source, ast.AugAssign):
                self.names = list(scope['__all__'].names)
        else:
            self.names = []

        def _add_to_names(container):
            for node in container.elts:
                if isinstance(node, ast.Str):
                    self.names.append(node.s)

        if isinstance(source.value, (ast.List, ast.Tuple)):
            _add_to_names(source.value)
        else:
            if isinstance(source.value, ast.BinOp):
                currentValue = source.value
                while isinstance(currentValue.right, ast.List):
                    left = currentValue.left
                    right = currentValue.right
                    _add_to_names(right)
                    if isinstance(left, ast.BinOp):
                        currentValue = left
                    else:
                        if isinstance(left, ast.List):
                            _add_to_names(left)
                            break
                        else:
                            break

        super(ExportBinding, self).__init__(name, source)


class Scope(dict):
    importStarred = False

    def __repr__(self):
        scope_cls = self.__class__.__name__
        return '<%s at 0x%x %s>' % (scope_cls, id(self), dict.__repr__(self))


class ClassScope(Scope):
    pass


class FunctionScope(Scope):
    __doc__ = "\n    I represent a name scope for a function.\n\n    @ivar globals: Names declared 'global' in this function.\n    "
    usesLocals = False
    alwaysUsed = {'__tracebackhide__', '__traceback_info__',
     '__traceback_supplement__'}

    def __init__(self):
        super(FunctionScope, self).__init__()
        self.globals = self.alwaysUsed.copy()
        self.returnValue = None
        self.isGenerator = False

    def unusedAssignments(self):
        """
        Return a generator for the assignments which have not been used.
        """
        for name, binding in self.items():
            if not binding.used and name != '_' and name not in self.globals and not self.usesLocals and isinstance(binding, Assignment):
                yield (
                 name, binding)


class GeneratorScope(Scope):
    pass


class ModuleScope(Scope):
    __doc__ = 'Scope for a module.'
    _futures_allowed = True
    _annotations_future_enabled = False


class DoctestScope(ModuleScope):
    __doc__ = 'Scope for a doctest.'


class DummyNode(object):
    __doc__ = 'Used in place of an `ast.AST` to set error message positions'

    def __init__(self, lineno, col_offset):
        self.lineno = lineno
        self.col_offset = col_offset


_MAGIC_GLOBALS = [
 '__file__', '__builtins__', 'WindowsError']
if PY36_PLUS:
    _MAGIC_GLOBALS.append('__annotations__')

def getNodeName(node):
    if hasattr(node, 'id'):
        return node.id
    if hasattr(node, 'name'):
        return node.name


def is_typing_overload(value, scope):

    def is_typing_overload_decorator(node):
        return isinstance(node, ast.Name) and node.id in scope and isinstance(scope[node.id], ImportationFrom) and scope[node.id].fullName == 'typing.overload' or isinstance(node, ast.Attribute) and isinstance(node.value, ast.Name) and node.value.id == 'typing' and node.attr == 'overload'

    return isinstance(value.source, ast.FunctionDef) and len(value.source.decorator_list) == 1 and is_typing_overload_decorator(value.source.decorator_list[0])


def make_tokens(code):
    if not isinstance(code, bytes):
        code = code.encode('UTF-8')
    lines = iter(code.splitlines(True))
    return tuple(tokenize_tokenize(lambda : next(lines, b'')))


class _TypeableVisitor(ast.NodeVisitor):
    __doc__ = 'Collect the line number and nodes which are deemed typeable by\n    PEP 484\n\n    https://www.python.org/dev/peps/pep-0484/#type-comments\n    '

    def __init__(self):
        self.typeable_lines = []
        self.typeable_nodes = {}

    def _typeable(self, node):
        self.typeable_lines.append(node.lineno)
        self.typeable_nodes[node.lineno] = node
        self.generic_visit(node)

    visit_Assign = visit_For = visit_FunctionDef = visit_With = _typeable
    visit_AsyncFor = visit_AsyncFunctionDef = visit_AsyncWith = _typeable


def _collect_type_comments(tree, tokens):
    visitor = _TypeableVisitor()
    visitor.visit(tree)
    type_comments = collections.defaultdict(list)
    for tp, text, start, _, _ in tokens:
        if not tp != tokenize.COMMENT:
            if not TYPE_COMMENT_RE.match(text) or TYPE_IGNORE_RE.match(text):
                pass
            else:
                lineno, _ = start
                idx = bisect.bisect_right(visitor.typeable_lines, lineno)
                if idx == 0:
                    pass
                else:
                    node = visitor.typeable_nodes[visitor.typeable_lines[(idx - 1)]]
                    type_comments[node].append((start, text))

    return type_comments


class Checker(object):
    __doc__ = '\n    I check the cleanliness and sanity of Python code.\n\n    @ivar _deferredFunctions: Tracking list used by L{deferFunction}.  Elements\n        of the list are two-tuples.  The first element is the callable passed\n        to L{deferFunction}.  The second element is a copy of the scope stack\n        at the time L{deferFunction} was called.\n\n    @ivar _deferredAssignments: Similar to C{_deferredFunctions}, but for\n        callables which are deferred assignment checks.\n    '
    _ast_node_scope = {ast.Module: ModuleScope, 
     ast.ClassDef: ClassScope, 
     ast.FunctionDef: FunctionScope, 
     ast.Lambda: FunctionScope, 
     ast.ListComp: GeneratorScope, 
     ast.SetComp: GeneratorScope, 
     ast.GeneratorExp: GeneratorScope, 
     ast.DictComp: GeneratorScope}
    if PY35_PLUS:
        _ast_node_scope[ast.AsyncFunctionDef] = (
         FunctionScope,)
    nodeDepth = 0
    offset = None
    traceTree = False
    builtIns = set(builtin_vars).union(_MAGIC_GLOBALS)
    _customBuiltIns = os.environ.get('PYFLAKES_BUILTINS')
    if _customBuiltIns:
        builtIns.update(_customBuiltIns.split(','))
    del _customBuiltIns

    def __init__(self, tree, filename='(none)', builtins=None, withDoctest='PYFLAKES_DOCTEST' in os.environ, file_tokens=()):
        self._nodeHandlers = {}
        self._deferredFunctions = []
        self._deferredAssignments = []
        self.deadScopes = []
        self.messages = []
        self.filename = filename
        if builtins:
            self.builtIns = self.builtIns.union(builtins)
        self.withDoctest = withDoctest
        try:
            self.scopeStack = [
             Checker._ast_node_scope[type(tree)]()]
        except KeyError:
            raise RuntimeError('No scope implemented for the node %r' % tree)

        self.exceptHandlers = [()]
        self.root = tree
        self._type_comments = _collect_type_comments(tree, file_tokens)
        for builtin in self.builtIns:
            self.addBinding(None, Builtin(builtin))

        self.handleChildren(tree)
        self.runDeferred(self._deferredFunctions)
        self._deferredFunctions = None
        self.runDeferred(self._deferredAssignments)
        self._deferredAssignments = None
        del self.scopeStack[1:]
        self.popScope()
        self.checkDeadScopes()

    def deferFunction(self, callable):
        """
        Schedule a function handler to be called just before completion.

        This is used for handling function bodies, which must be deferred
        because code later in the file might modify the global scope. When
        `callable` is called, the scope at the time this is called will be
        restored, however it will contain any new bindings added to it.
        """
        self._deferredFunctions.append((callable, self.scopeStack[:], self.offset))

    def deferAssignment(self, callable):
        """
        Schedule an assignment handler to be called just after deferred
        function handlers.
        """
        self._deferredAssignments.append((callable, self.scopeStack[:], self.offset))

    def runDeferred(self, deferred):
        """
        Run the callables in C{deferred} using their associated scope stack.
        """
        for handler, scope, offset in deferred:
            self.scopeStack = scope
            self.offset = offset
            handler()

    def _in_doctest(self):
        return len(self.scopeStack) >= 2 and isinstance(self.scopeStack[1], DoctestScope)

    @property
    def futuresAllowed(self):
        if not all(isinstance(scope, ModuleScope) for scope in self.scopeStack):
            return False
        else:
            return self.scope._futures_allowed

    @futuresAllowed.setter
    def futuresAllowed(self, value):
        assert value is False
        if isinstance(self.scope, ModuleScope):
            self.scope._futures_allowed = False

    @property
    def annotationsFutureEnabled(self):
        scope = self.scopeStack[0]
        if not isinstance(scope, ModuleScope):
            return False
        else:
            return scope._annotations_future_enabled

    @annotationsFutureEnabled.setter
    def annotationsFutureEnabled(self, value):
        if not value is True:
            raise AssertionError
        elif not isinstance(self.scope, ModuleScope):
            raise AssertionError
        self.scope._annotations_future_enabled = True

    @property
    def scope(self):
        return self.scopeStack[(-1)]

    def popScope(self):
        self.deadScopes.append(self.scopeStack.pop())

    def checkDeadScopes(self):
        """
        Look at scopes which have been fully examined and report names in them
        which were imported but unused.
        """
        for scope in self.deadScopes:
            if isinstance(scope, ClassScope):
                pass
            else:
                all_binding = scope.get('__all__')
                if all_binding:
                    if not isinstance(all_binding, ExportBinding):
                        all_binding = None
                if all_binding:
                    all_names = set(all_binding.names)
                    undefined = all_names.difference(scope)
                else:
                    all_names = undefined = []
                if undefined:
                    if not scope.importStarred:
                        if os.path.basename(self.filename) != '__init__.py':
                            for name in undefined:
                                self.report(messages.UndefinedExport, scope['__all__'].source, name)

                    if scope.importStarred:
                        from_list = []
                        for binding in scope.values():
                            if isinstance(binding, StarImportation):
                                binding.used = all_binding
                                from_list.append(binding.fullName)

                        from_list = ', '.join(sorted(from_list))
                        for name in undefined:
                            self.report(messages.ImportStarUsage, scope['__all__'].source, name, from_list)

                for value in scope.values():
                    if isinstance(value, Importation):
                        used = value.used or value.name in all_names
                        if not used:
                            messg = messages.UnusedImport
                            self.report(messg, value.source, str(value))
                        for node in value.redefined:
                            if isinstance(self.getParent(node), FOR_TYPES):
                                messg = messages.ImportShadowedByLoopVar
                            else:
                                if used:
                                    continue
                                else:
                                    messg = messages.RedefinedWhileUnused
                            self.report(messg, node, value.name, value.source)

    def pushScope(self, scopeClass=FunctionScope):
        self.scopeStack.append(scopeClass())

    def report(self, messageClass, *args, **kwargs):
        self.messages.append(messageClass(self.filename, *args, **kwargs))

    def getParent(self, node):
        while 1:
            node = node.parent
            if not hasattr(node, 'elts'):
                if not hasattr(node, 'ctx'):
                    return node

    def getCommonAncestor(self, lnode, rnode, stop):
        if stop in (lnode, rnode) or not (hasattr(lnode, 'parent') and hasattr(rnode, 'parent')):
            return
        else:
            if lnode is rnode:
                return lnode
            else:
                if lnode.depth > rnode.depth:
                    return self.getCommonAncestor(lnode.parent, rnode, stop)
                if lnode.depth < rnode.depth:
                    return self.getCommonAncestor(lnode, rnode.parent, stop)
            return self.getCommonAncestor(lnode.parent, rnode.parent, stop)

    def descendantOf(self, node, ancestors, stop):
        for a in ancestors:
            if self.getCommonAncestor(node, a, stop):
                return True

        return False

    def _getAncestor(self, node, ancestor_type):
        parent = node
        while 1:
            if parent is self.root:
                return
            parent = self.getParent(parent)
            if isinstance(parent, ancestor_type):
                return parent

    def getScopeNode(self, node):
        return self._getAncestor(node, tuple(Checker._ast_node_scope.keys()))

    def differentForks(self, lnode, rnode):
        """True, if lnode and rnode are located on different forks of IF/TRY"""
        ancestor = self.getCommonAncestor(lnode, rnode, self.root)
        parts = getAlternatives(ancestor)
        if parts:
            for items in parts:
                if self.descendantOf(lnode, items, ancestor) ^ self.descendantOf(rnode, items, ancestor):
                    return True

        return False

    def addBinding(self, node, value):
        """
        Called when a binding is altered.

        - `node` is the statement responsible for the change
        - `value` is the new value, a Binding instance
        """
        for scope in self.scopeStack[::-1]:
            if value.name in scope:
                break

        existing = scope.get(value.name)
        if existing and not isinstance(existing, Builtin) and not self.differentForks(node, existing.source):
            parent_stmt = self.getParent(value.source)
            if isinstance(existing, Importation):
                if isinstance(parent_stmt, FOR_TYPES):
                    self.report(messages.ImportShadowedByLoopVar, node, value.name, existing.source)
            if scope is self.scope:
                if isinstance(parent_stmt, ast.comprehension):
                    if not isinstance(self.getParent(existing.source), (
                     FOR_TYPES, ast.comprehension)):
                        self.report(messages.RedefinedInListComp, node, value.name, existing.source)
                    if not existing.used and value.redefines(existing) and (value.name != '_' or isinstance(existing, Importation)):
                        is_typing_overload(existing, self.scope) or self.report(messages.RedefinedWhileUnused, node, value.name, existing.source)
            elif isinstance(existing, Importation):
                if value.redefines(existing):
                    existing.redefined.append(node)
        if value.name in self.scope:
            value.used = self.scope[value.name].used
        self.scope[value.name] = value

    def getNodeHandler(self, node_class):
        try:
            return self._nodeHandlers[node_class]
        except KeyError:
            nodeType = getNodeType(node_class)

        self._nodeHandlers[node_class] = handler = getattr(self, nodeType)
        return handler

    def handleNodeLoad(self, node):
        name = getNodeName(node)
        if not name:
            return
        in_generators = None
        importStarred = None
        for scope in self.scopeStack[-1::-1]:
            if isinstance(scope, ClassScope):
                if not PY2:
                    if name == '__class__':
                        return
                    else:
                        if in_generators is False:
                            continue
                        if name == 'print':
                            if isinstance(scope.get(name, None), Builtin):
                                parent = self.getParent(node)
                                if isinstance(parent, ast.BinOp):
                                    if isinstance(parent.op, ast.RShift):
                                        self.report(messages.InvalidPrintSyntax, node)
                else:
                    try:
                        scope[name].used = (
                         self.scope, node)
                        n = scope[name]
                        if isinstance(n, Importation) and n._has_alias():
                            try:
                                scope[n.fullName].used = (
                                 self.scope, node)
                            except KeyError:
                                pass

                    except KeyError:
                        pass
                    else:
                        return
                importStarred = importStarred or scope.importStarred
                if in_generators is not False:
                    in_generators = isinstance(scope, GeneratorScope)

        if importStarred:
            from_list = []
            for scope in self.scopeStack[-1::-1]:
                for binding in scope.values():
                    if isinstance(binding, StarImportation):
                        binding.used = (self.scope, node)
                        from_list.append(binding.fullName)

            from_list = ', '.join(sorted(from_list))
            self.report(messages.ImportStarUsage, node, name, from_list)
            return
        if name == '__path__':
            if os.path.basename(self.filename) == '__init__.py':
                return
        if name == '__module__':
            if isinstance(self.scope, ClassScope):
                return
        if 'NameError' not in self.exceptHandlers[(-1)]:
            self.report(messages.UndefinedName, node, name)

    def handleNodeStore(self, node):
        name = getNodeName(node)
        if not name:
            return
        elif isinstance(self.scope, FunctionScope):
            if name not in self.scope:
                for scope in self.scopeStack[:-1]:
                    if not isinstance(scope, (FunctionScope, ModuleScope)):
                        pass
                    else:
                        used = name in scope and scope[name].used
                        if used:
                            if used[0] is self.scope:
                                if name not in self.scope.globals:
                                    self.report(messages.UndefinedLocal, scope[name].used[1], name, scope[name].source)
                                    break

        else:
            parent_stmt = self.getParent(node)
            if isinstance(parent_stmt, (FOR_TYPES, ast.comprehension)) or parent_stmt != node.parent and not self.isLiteralTupleUnpacking(parent_stmt):
                binding = Binding(name, node)
            else:
                if name == '__all__' and isinstance(self.scope, ModuleScope):
                    binding = ExportBinding(name, node.parent, self.scope)
                else:
                    if isinstance(getattr(node, 'ctx', None), ast.Param):
                        binding = Argument(name, self.getScopeNode(node))
                    else:
                        binding = Assignment(name, node)
        self.addBinding(node, binding)

    def handleNodeDelete(self, node):

        def on_conditional_branch():
            current = getattr(node, 'parent', None)
            while current:
                if isinstance(current, (ast.If, ast.While, ast.IfExp)):
                    return True
                current = getattr(current, 'parent', None)

            return False

        name = getNodeName(node)
        if not name:
            return
        if on_conditional_branch():
            return
        if isinstance(self.scope, FunctionScope):
            if name in self.scope.globals:
                self.scope.globals.remove(name)
        try:
            del self.scope[name]
        except KeyError:
            self.report(messages.UndefinedName, node, name)

    def _handle_type_comments(self, node):
        for (lineno, col_offset), comment in self._type_comments.get(node, ()):
            comment = comment.split(':', 1)[1].strip()
            func_match = TYPE_FUNC_RE.match(comment)
            if func_match:
                parts = (func_match.group(1).replace('*', ''),
                 func_match.group(2).strip())
            else:
                parts = (
                 comment,)
            for part in parts:
                if PY2:
                    part = part.replace('...', 'Ellipsis')
                self.deferFunction(functools.partial(self.handleStringAnnotation, part, DummyNode(lineno, col_offset), lineno, col_offset, messages.CommentAnnotationSyntaxError))

    def handleChildren(self, tree, omit=None):
        self._handle_type_comments(tree)
        for node in iter_child_nodes(tree, omit=omit):
            self.handleNode(node, tree)

    def isLiteralTupleUnpacking(self, node):
        if isinstance(node, ast.Assign):
            for child in node.targets + [node.value]:
                if not hasattr(child, 'elts'):
                    return False

            return True

    def isDocstring(self, node):
        """
        Determine if the given node is a docstring, as long as it is at the
        correct place in the node tree.
        """
        return isinstance(node, ast.Str) or isinstance(node, ast.Expr) and isinstance(node.value, ast.Str)

    def getDocstring(self, node):
        if isinstance(node, ast.Expr):
            node = node.value
        if not isinstance(node, ast.Str):
            return (None, None)
        else:
            if PYPY or PY38_PLUS:
                doctest_lineno = node.lineno - 1
            else:
                doctest_lineno = node.lineno - node.s.count('\n') - 1
            return (node.s, doctest_lineno)

    def handleNode(self, node, parent):
        if node is None:
            return
        else:
            if self.offset:
                if getattr(node, 'lineno', None) is not None:
                    node.lineno += self.offset[0]
                    node.col_offset += self.offset[1]
                if self.traceTree:
                    print('  ' * self.nodeDepth + node.__class__.__name__)
            else:
                if self.futuresAllowed:
                    if not (isinstance(node, ast.ImportFrom) or self.isDocstring(node)):
                        self.futuresAllowed = False
            self.nodeDepth += 1
            node.depth = self.nodeDepth
            node.parent = parent
            try:
                handler = self.getNodeHandler(node.__class__)
                handler(node)
            finally:
                self.nodeDepth -= 1

            if self.traceTree:
                print('  ' * self.nodeDepth + 'end ' + node.__class__.__name__)

    _getDoctestExamples = doctest.DocTestParser().get_examples

    def handleDoctests(self, node):
        try:
            if hasattr(node, 'docstring'):
                docstring = node.docstring
                node_lineno = node.lineno
                if hasattr(node, 'args'):
                    node_lineno = max([node_lineno] + [arg.lineno for arg in node.args.args])
            else:
                docstring, node_lineno = self.getDocstring(node.body[0])
            examples = docstring and self._getDoctestExamples(docstring)
        except (ValueError, IndexError):
            return
        else:
            if not examples:
                return
            saved_stack = self.scopeStack
            self.scopeStack = [self.scopeStack[0]]
            node_offset = self.offset or (0, 0)
            self.pushScope(DoctestScope)
            self.addBinding(None, Builtin('_'))
            for example in examples:
                try:
                    tree = ast.parse(example.source, '<doctest>')
                except SyntaxError:
                    e = sys.exc_info()[1]
                    if PYPY:
                        e.offset += 1
                    position = (
                     node_lineno + example.lineno + e.lineno,
                     example.indent + 4 + (e.offset or 0))
                    self.report(messages.DoctestSyntaxError, node, position)
                else:
                    self.offset = (
                     node_offset[0] + node_lineno + example.lineno,
                     node_offset[1] + example.indent + 4)
                    self.handleChildren(tree)
                    self.offset = node_offset

            self.popScope()
            self.scopeStack = saved_stack

    def handleStringAnnotation(self, s, node, ref_lineno, ref_col_offset, err):
        try:
            tree = ast.parse(s)
        except SyntaxError:
            self.report(err, node, s)
            return
        else:
            body = tree.body
            if len(body) != 1 or not isinstance(body[0], ast.Expr):
                self.report(err, node, s)
                return
            parsed_annotation = tree.body[0].value
            for descendant in ast.walk(parsed_annotation):
                if 'lineno' in descendant._attributes and 'col_offset' in descendant._attributes:
                    descendant.lineno = ref_lineno
                    descendant.col_offset = ref_col_offset

            self.handleNode(parsed_annotation, node)

    def handleAnnotation(self, annotation, node):
        if isinstance(annotation, ast.Str):
            self.deferFunction(functools.partial(self.handleStringAnnotation, annotation.s, node, annotation.lineno, annotation.col_offset, messages.ForwardAnnotationSyntaxError))
        else:
            if self.annotationsFutureEnabled:
                self.deferFunction(lambda : self.handleNode(annotation, node))
            else:
                self.handleNode(annotation, node)

    def ignore(self, node):
        pass

    DELETE = PRINT = FOR = ASYNCFOR = WHILE = IF = WITH = WITHITEM = ASYNCWITH = ASYNCWITHITEM = TRYFINALLY = EXEC = EXPR = ASSIGN = handleChildren
    PASS = ignore
    BOOLOP = BINOP = UNARYOP = IFEXP = SET = CALL = REPR = ATTRIBUTE = SUBSCRIPT = STARRED = NAMECONSTANT = handleChildren
    NUM = STR = BYTES = ELLIPSIS = CONSTANT = ignore
    SLICE = EXTSLICE = INDEX = handleChildren
    LOAD = STORE = DEL = AUGLOAD = AUGSTORE = PARAM = ignore
    AND = OR = ADD = SUB = MULT = DIV = MOD = POW = LSHIFT = RSHIFT = BITOR = BITXOR = BITAND = FLOORDIV = INVERT = NOT = UADD = USUB = EQ = NOTEQ = LT = LTE = GT = GTE = IS = ISNOT = IN = NOTIN = MATMULT = ignore

    def RAISE(self, node):
        self.handleChildren(node)
        arg = get_raise_argument(node)
        if isinstance(arg, ast.Call):
            if is_notimplemented_name_node(arg.func):
                self.report(messages.RaiseNotImplemented, node)
        elif is_notimplemented_name_node(arg):
            self.report(messages.RaiseNotImplemented, node)

    COMPREHENSION = KEYWORD = FORMATTEDVALUE = JOINEDSTR = handleChildren

    def DICT(self, node):
        keys = [convert_to_value(key) for key in node.keys]
        key_counts = counter(keys)
        duplicate_keys = [key for key, count in key_counts.items() if count > 1]
        for key in duplicate_keys:
            key_indices = [i for i, i_key in enumerate(keys) if i_key == key]
            values = counter(convert_to_value(node.values[index]) for index in key_indices)
            if any(count == 1 for value, count in values.items()):
                for key_index in key_indices:
                    key_node = node.keys[key_index]
                    if isinstance(key, VariableKey):
                        self.report(messages.MultiValueRepeatedKeyVariable, key_node, key.name)
                    else:
                        self.report(messages.MultiValueRepeatedKeyLiteral, key_node, key)

        self.handleChildren(node)

    def ASSERT(self, node):
        if isinstance(node.test, ast.Tuple):
            if node.test.elts != []:
                self.report(messages.AssertTuple, node)
        self.handleChildren(node)

    def GLOBAL(self, node):
        """
        Keep track of globals declarations.
        """
        global_scope_index = 1 if self._in_doctest() else 0
        global_scope = self.scopeStack[global_scope_index]
        if self.scope is not global_scope:
            for node_name in node.names:
                node_value = Assignment(node_name, node)
                self.messages = [m for m in self.messages if not isinstance(m, messages.UndefinedName) or m.message_args[0] != node_name]
                global_scope.setdefault(node_name, node_value)
                node_value.used = (
                 global_scope, node)
                for scope in self.scopeStack[global_scope_index + 1:]:
                    scope[node_name] = node_value

    NONLOCAL = GLOBAL

    def GENERATOREXP(self, node):
        self.pushScope(GeneratorScope)
        self.handleChildren(node)
        self.popScope()

    LISTCOMP = handleChildren if PY2 else GENERATOREXP
    DICTCOMP = SETCOMP = GENERATOREXP

    def NAME(self, node):
        """
        Handle occurrence of Name (which can be a load/store/delete access.)
        """
        if isinstance(node.ctx, (ast.Load, ast.AugLoad)):
            self.handleNodeLoad(node)
            if node.id == 'locals':
                if isinstance(self.scope, FunctionScope):
                    if isinstance(node.parent, ast.Call):
                        self.scope.usesLocals = True
        else:
            if isinstance(node.ctx, (ast.Store, ast.AugStore, ast.Param)):
                self.handleNodeStore(node)
            else:
                if isinstance(node.ctx, ast.Del):
                    self.handleNodeDelete(node)
                else:
                    raise RuntimeError('Got impossible expression context: %r' % (node.ctx,))

    def CONTINUE(self, node):
        n = node
        while hasattr(n, 'parent'):
            n, n_child = n.parent, n
            if isinstance(n, LOOP_TYPES):
                if n_child not in n.orelse:
                    return
            else:
                if isinstance(n, (ast.FunctionDef, ast.ClassDef)):
                    break
                if hasattr(n, 'finalbody'):
                    if isinstance(node, ast.Continue):
                        if n_child in n.finalbody:
                            self.report(messages.ContinueInFinally, node)
                            return

        if isinstance(node, ast.Continue):
            self.report(messages.ContinueOutsideLoop, node)
        else:
            self.report(messages.BreakOutsideLoop, node)

    BREAK = CONTINUE

    def RETURN(self, node):
        if isinstance(self.scope, (ClassScope, ModuleScope)):
            self.report(messages.ReturnOutsideFunction, node)
            return
        if node.value:
            if hasattr(self.scope, 'returnValue'):
                if not self.scope.returnValue:
                    self.scope.returnValue = node.value
        self.handleNode(node.value, node)

    def YIELD(self, node):
        if isinstance(self.scope, (ClassScope, ModuleScope)):
            self.report(messages.YieldOutsideFunction, node)
            return
        self.scope.isGenerator = True
        self.handleNode(node.value, node)

    AWAIT = YIELDFROM = YIELD

    def FUNCTIONDEF(self, node):
        for deco in node.decorator_list:
            self.handleNode(deco, node)

        self.LAMBDA(node)
        self.addBinding(node, FunctionDefinition(node.name, node))
        if self.withDoctest:
            if not self._in_doctest():
                if not isinstance(self.scope, FunctionScope):
                    self.deferFunction(lambda : self.handleDoctests(node))

    ASYNCFUNCTIONDEF = FUNCTIONDEF

    def LAMBDA(self, node):
        args = []
        annotations = []
        if PY2:

            def addArgs(arglist):
                for arg in arglist:
                    if isinstance(arg, ast.Tuple):
                        addArgs(arg.elts)
                    else:
                        args.append(arg.id)

            addArgs(node.args.args)
            defaults = node.args.defaults
        else:
            for arg in node.args.args + node.args.kwonlyargs:
                args.append(arg.arg)
                annotations.append(arg.annotation)

            defaults = node.args.defaults + node.args.kw_defaults
        is_py3_func = hasattr(node, 'returns')
        for arg_name in ('vararg', 'kwarg'):
            wildcard = getattr(node.args, arg_name)
            if not wildcard:
                pass
            else:
                args.append(wildcard if PY2 else wildcard.arg)
            if is_py3_func:
                if PY2:
                    argannotation = arg_name + 'annotation'
                    annotations.append(getattr(node.args, argannotation))
                else:
                    annotations.append(wildcard.annotation)

        if is_py3_func:
            annotations.append(node.returns)
        if len(set(args)) < len(args):
            for idx, arg in enumerate(args):
                if arg in args[:idx]:
                    self.report(messages.DuplicateArgument, node, arg)

        for annotation in annotations:
            self.handleAnnotation(annotation, node)

        for default in defaults:
            self.handleNode(default, node)

        def runFunction():
            self.pushScope()
            self.handleChildren(node, omit='decorator_list')

            def checkUnusedAssignments():
                for name, binding in self.scope.unusedAssignments():
                    self.report(messages.UnusedVariable, binding.source, name)

            self.deferAssignment(checkUnusedAssignments)
            if PY2:

                def checkReturnWithArgumentInsideGenerator():
                    if self.scope.isGenerator:
                        if self.scope.returnValue:
                            self.report(messages.ReturnWithArgsInsideGenerator, self.scope.returnValue)

                self.deferAssignment(checkReturnWithArgumentInsideGenerator)
            self.popScope()

        self.deferFunction(runFunction)

    def ARGUMENTS(self, node):
        self.handleChildren(node, omit=('defaults', 'kw_defaults'))
        if PY2:
            scope_node = self.getScopeNode(node)
            if node.vararg:
                self.addBinding(node, Argument(node.vararg, scope_node))
            if node.kwarg:
                self.addBinding(node, Argument(node.kwarg, scope_node))

    def ARG(self, node):
        self.addBinding(node, Argument(node.arg, self.getScopeNode(node)))

    def CLASSDEF(self, node):
        """
        Check names used in a class definition, including its decorators, base
        classes, and the body of its definition.  Additionally, add its name to
        the current scope.
        """
        for deco in node.decorator_list:
            self.handleNode(deco, node)

        for baseNode in node.bases:
            self.handleNode(baseNode, node)

        if not PY2:
            for keywordNode in node.keywords:
                self.handleNode(keywordNode, node)

        self.pushScope(ClassScope)
        if self.withDoctest:
            if not self._in_doctest():
                if not isinstance(self.scope, FunctionScope):
                    self.deferFunction(lambda : self.handleDoctests(node))
        for stmt in node.body:
            self.handleNode(stmt, node)

        self.popScope()
        self.addBinding(node, ClassDefinition(node.name, node))

    def AUGASSIGN(self, node):
        self.handleNodeLoad(node.target)
        self.handleNode(node.value, node)
        self.handleNode(node.target, node)

    def TUPLE(self, node):
        if not PY2:
            if isinstance(node.ctx, ast.Store):
                has_starred = False
                star_loc = -1
                for i, n in enumerate(node.elts):
                    if isinstance(n, ast.Starred):
                        if has_starred:
                            self.report(messages.TwoStarredExpressions, node)
                            break
                        has_starred = True
                        star_loc = i

                if star_loc >= 256 or len(node.elts) - star_loc - 1 >= 16777216:
                    self.report(messages.TooManyExpressionsInStarredAssignment, node)
        self.handleChildren(node)

    LIST = TUPLE

    def IMPORT(self, node):
        for alias in node.names:
            if '.' in alias.name:
                if not alias.asname:
                    importation = SubmoduleImportation(alias.name, node)
            else:
                name = alias.asname or alias.name
                importation = Importation(name, node, alias.name)
            self.addBinding(node, importation)

    def IMPORTFROM(self, node):
        if node.module == '__future__':
            if not self.futuresAllowed:
                self.report(messages.LateFutureImport, node, [n.name for n in node.names])
        else:
            self.futuresAllowed = False
        module = '.' * node.level + (node.module or '')
        for alias in node.names:
            name = alias.asname or alias.name
            if node.module == '__future__':
                importation = FutureImportation(name, node, self.scope)
                if alias.name not in __future__.all_feature_names:
                    self.report(messages.FutureFeatureNotDefined, node, alias.name)
                if alias.name == 'annotations':
                    self.annotationsFutureEnabled = True
            else:
                if alias.name == '*':
                    if not PY2:
                        if not isinstance(self.scope, ModuleScope):
                            self.report(messages.ImportStarNotPermitted, node, module)
                            continue
                    self.scope.importStarred = True
                    self.report(messages.ImportStarUsed, node, module)
                    importation = StarImportation(module, node)
                else:
                    importation = ImportationFrom(name, node, module, alias.name)
                self.addBinding(node, importation)

    def TRY(self, node):
        handler_names = []
        for i, handler in enumerate(node.handlers):
            if isinstance(handler.type, ast.Tuple):
                for exc_type in handler.type.elts:
                    handler_names.append(getNodeName(exc_type))

            else:
                if handler.type:
                    handler_names.append(getNodeName(handler.type))
            if handler.type is None and i < len(node.handlers) - 1:
                self.report(messages.DefaultExceptNotLast, handler)

        self.exceptHandlers.append(handler_names)
        for child in node.body:
            self.handleNode(child, node)

        self.exceptHandlers.pop()
        self.handleChildren(node, omit='body')

    TRYEXCEPT = TRY

    def EXCEPTHANDLER(self, node):
        if PY2 or node.name is None:
            self.handleChildren(node)
            return
        else:
            if node.name in self.scope:
                self.handleNodeStore(node)
            try:
                prev_definition = self.scope.pop(node.name)
            except KeyError:
                prev_definition = None

            self.handleNodeStore(node)
            self.handleChildren(node)
            try:
                binding = self.scope.pop(node.name)
            except KeyError:
                pass
            else:
                if not binding.used:
                    self.report(messages.UnusedVariable, node, node.name)
                if prev_definition:
                    self.scope[node.name] = prev_definition

    def ANNASSIGN(self, node):
        if node.value:
            self.handleNode(node.target, node)
        self.handleAnnotation(node.annotation, node)
        if node.value:
            self.handleNode(node.value, node)

    def COMPARE(self, node):
        literals = (ast.Str, ast.Num)
        if not PY2:
            literals += (ast.Bytes,)
        left = node.left
        for op, right in zip(node.ops, node.comparators):
            if isinstance(op, (ast.Is, ast.IsNot)):
                if isinstance(left, literals) or isinstance(right, literals):
                    self.report(messages.IsLiteral, node)
            left = right

        self.handleChildren(node)