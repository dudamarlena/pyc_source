# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /mnt/c/Users/hakan/Desktop/project/unimport/unimport/refactor.py
# Compiled at: 2020-04-09 19:08:42
# Size of source mod 2**32: 4741 bytes
from contextlib import contextmanager
from lib2to3.fixer_base import BaseFix
from lib2to3.fixer_util import BlankLine, Leaf, Newline, Node, syms, token
from lib2to3.refactor import RefactoringTool

def traverse_imports(names):
    """
    Walks over all the names imported in a dotted_as_names node.
    """
    pending = [
     names]
    while pending:
        node = pending.pop()
        if node.type in {token.NAME, token.STAR}:
            yield node.value
        elif node.type == syms.dotted_name:
            yield ''.join([ch.value for ch in node.children])
        else:
            if node.type in {syms.dotted_as_name, syms.import_as_name}:
                pending.append(node.children[0])
            else:
                if node.type in {syms.dotted_as_names, syms.import_as_names}:
                    pending.extend(node.children[::-2])
                else:
                    raise ValueError('unknown node type', node.type)


class RefactorImports(BaseFix):
    PATTERN = "\n        simple_stmt<\n            (\n                import_name< 'import' imp=any >\n                |\n                import_from< 'from' imp=(['.'*] any) 'import' ['('] items=any [')'] >\n            ) '\\n'\n        >\n    "

    def __init__(self):
        self.unused_modules = []
        super().__init__(None, None)

    @contextmanager
    def clean(self, unused_modules):
        try:
            self.unused_modules.clear()
            self.unused_modules.extend(unused_modules)
            yield
        finally:
            self.unused_modules.clear()

    def transform(self, node, results):
        imports = results['imp']
        if node.children[0].type == syms.import_from:
            if str(imports).strip() in self.unused_modules:
                return BlankLine()
            else:
                try:
                    unused_imp = [imp for imp in self.unused_modules if imp['lineno'] == node.get_lineno()][0]
                except IndexError:
                    pass
                else:
                    if unused_imp['star']:
                        if not unused_imp['modules']:
                            return BlankLine()
                        else:
                            return self.suggestion_to_star_import(unused_imp)
                return self.transform_inner_body(node,
                  (results['items']), from_import=True)
        else:
            return self.transform_inner_body(node, imports)

    def suggestion_to_star_import(self, unused_imp):
        children = [
         Leaf(token.NAME, 'from'),
         Leaf((token.NAME), (unused_imp['module'].__name__), prefix=' '),
         Leaf((token.NAME), 'import', prefix=' '),
         Leaf((token.NAME),
           (', '.join(sorted(unused_imp['modules']))),
           prefix=' '),
         Newline()]
        return Node(syms.import_from, children)

    def transform_inner_body(self, node, imports, from_import=False):
        module_names = [imp['name'] for imp in self.unused_modules]
        if imports.children:
            body = imports.children
        else:
            body = [
             imports]

        def remove_comma():
            nonlocal trailing_comma
            if index + 1 == len(modules):
                comma = commas.pop(index - remove_counter - 1)
                if trailing_comma:
                    trailing_comma.remove()
                    trailing_comma = None
            else:
                comma = commas.pop(index - remove_counter)
            comma.remove()

        trailing_comma = None
        if body[(-1)].type == token.COMMA:
            trailing_comma = body.pop()
        commas = body[1:-1:2]
        module_nodes = body[::2]
        modules = tuple(traverse_imports(imports))
        remove_counter = 0
        for index, module in enumerate(modules):
            if module in module_names:
                if commas:
                    remove_comma()
                module_nodes.pop(index - remove_counter).remove()
                remove_counter += 1

        if remove_counter == len(modules):
            return BlankLine()
        if trailing_comma:
            body.append(trailing_comma)


class RefactorTool(RefactoringTool):

    def __init__(self):
        self._fixer = RefactorImports()
        self._fixers = [self._fixer]
        super().__init__(None, options={'print_function': True})

    def get_fixers(self):
        return (
         self._fixers, [])

    def refactor_string(self, data, unused_imports, name='unimport'):
        with self._fixer.clean(unused_imports):
            source = super().refactor_string(data, name)
        return str(source)