# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ana/dev/dexy-clean/dexy/filters/pyparse.py
# Compiled at: 2020-03-18 15:12:33
# Size of source mod 2**32: 11308 bytes
from dexy.filter import DexyFilter
from lib2to3.pytree import Leaf
import inspect, lib2to3.pgen2.driver, lib2to3.pytree, os
driver_file = lib2to3.pgen2.driver.__file__
grammar_dir = os.path.abspath(os.path.join(os.path.dirname(driver_file), '..'))

class PyParse(DexyFilter):
    __doc__ = "\n    Parses Python source code using lib2to3, without loading files, so doesn't\n    cause side effects or care if imports work.\n    "
    aliases = ['pyparse']
    _settings = {'data-type':'keyvalue', 
     'whitespace-types':('Token types corresponding to whitespace.', (4, 5)), 
     'string-types':('Token types corresponding to strings.', (3,)), 
     'grammar-file':('Name or full path to file specifying Python language grammar.', 'Grammar.txt')}

    def grammar_path(self):
        grammar_file = self.setting('grammar-file')
        if '/' in grammar_file:
            return grammar_file
        return os.path.join(grammar_dir, grammar_file)

    def setup_driver(self):
        self.grammar = lib2to3.pgen2.driver.load_grammar(self.grammar_path())
        self.driver = lib2to3.pgen2.driver.Driver((self.grammar), convert=(lib2to3.pytree.convert))

    def type_repr(self, type_num):
        if not hasattr(self, '_type_reprs'):
            from lib2to3.pygram import python_symbols
            self._type_reprs = {}
            for name, val in python_symbols.__dict__.items():
                if type(val) == int:
                    self._type_reprs[val] = name

        return self._type_reprs.setdefault(type_num, type_num)

    def type_of(self, node):
        return self.type_repr(node.type)

    def eval_string(self, leaf):
        return eval(leaf.value).strip()

    def first_simple_statement_after_any_whitespace(self, parent):
        for child in parent.children:
            if child.type in self.setting('whitespace-types'):
                continue
            if child.type in self.setting('string-types'):
                first_child = child
                return self.eval_string(first_child)
                if self.type_of(child) == 'simple_stmt':
                    first_child = child.children[0]
                    if isinstance(first_child, Leaf) and first_child.type in self.setting('string-types'):
                        return self.eval_string(first_child)

    def process_node(self, node, prefix):
        node_type = self.type_of(node)
        decorators = []
        if node_type == 'decorated':
            for child in node.children:
                if self.type_of(child) == 'decorator':
                    decorators.append(str(child).rstrip())
                elif self.type_of(child) == 'decorators':
                    for decorator in child.children:
                        decorators.append(str(decorator).rstrip())

                else:
                    child_type = self.type_of(child)
                    if child_type == 'funcdef':
                        self.process_function(node, prefix, decorators)
                    elif child_type == 'classdef':
                        self.process_class(node, prefix, decorators)
                    else:
                        raise Exception("unknown decorated child type '%s'" % child_type)

        else:
            if node_type == 'funcdef':
                return self.process_function(node, prefix, decorators)
            if node_type == 'classdef':
                return self.process_class(node, prefix, decorators)
            if node_type == 'simple_stmt':
                return self.process_simple_stmt(node, prefix, decorators)
            return prefix

    def process_root(self, node, prefix):
        docstring = self.first_simple_statement_after_any_whitespace(node)
        if prefix is None:
            key = ':doc'
        else:
            if 'None' in prefix:
                key = ':doc'
            else:
                key = '%s:doc' % prefix
        not_already_in_keys = key not in list(self.output_data.keys())
        is_a_docstring = docstring is not None
        if not_already_in_keys:
            if is_a_docstring:
                self.output_data.append(key, inspect.cleandoc(docstring))
        self.process_node(node, prefix)

    def process(self):
        self.func_name = None
        self.class_name = None
        self.setup_driver()
        text = str(self.input_data)
        if text == 'None':
            self.output_data.set_data({})
        else:
            root = self.driver.parse_string(text)
            for node in root.children:
                self.process_root(node, None)

            self.output_data.save()

    def name_with_prefix(self, name, prefix):
        if prefix is None:
            return name
        return '%s.%s' % (prefix, name)

    def process_function(self, node, prefix, decorators):

        def process_func_part(state, part):
            if state == 'def':
                if isinstance(part, Leaf):
                    if not part.value == 'def':
                        raise AssertionError(part)
                    return 'funcname'
                    if state == 'funcname':
                        if not (isinstance(part, Leaf) and part.type == 1):
                            raise AssertionError
                        self.func_name = part.value
                        name_with_prefix = self.name_with_prefix(self.func_name, prefix)
                        raw_source = str(node).rstrip().splitlines()
                        is_function_started = False
                        leading_comments = []
                        source_lines = []
                        indent = None
                        for line in raw_source:
                            is_comment = line.lstrip().startswith('#')
                            is_decorator = line.lstrip().startswith('@')
                            has_def = 'def' in line
                            if has_def:
                                if indent is None:
                                    indent = len(line) - len(line.lstrip())
                                else:
                                    if is_function_started:
                                        source_lines.append(line)
                                if not is_function_started:
                                    if is_comment:
                                        leading_comments.append(line)
                                if is_comment or has_def or is_decorator:
                                    is_function_started = True
                                    source_lines.append(line)

                        while not source_lines[(-1)].lstrip().startswith('#'):
                            source_lines[(-1)].lstrip() or source_lines.pop()

                        for i, line in enumerate(source_lines):
                            if not line.startswith('@'):
                                break
                            if len(line) - len(line.lstrip()) == 0 and indent > 0:
                                source_lines[i] = ' ' * indent + line

                        self.output_data.append('%s:source' % name_with_prefix, '\n'.join(source_lines))
                        self.output_data.append('%s:decorators' % name_with_prefix, '\n'.join(decorators))
                        return 'parameters'
                    if state == 'parameters':
                        assert self.type_of(part) == 'parameters'
                        return 'colon'
                    if state == 'colon':
                        if not part.value == ':':
                            raise AssertionError
                else:
                    return 'body'
                if state == 'body':
                    assert self.type_of(part) == 'suite'
                    docstring = self.first_simple_statement_after_any_whitespace(part)
                    if docstring is not None:
                        self.output_data.append('%s:doc' % self.name_with_prefix(self.func_name, prefix), inspect.cleandoc(docstring))
            elif state is None:
                pass
            else:
                raise Exception("invalid state '%s'" % state)

        state = 'def'
        for child in node.children:
            if self.type_of(child) in ('decorator', 'decorators'):
                continue
            if self.type_of(child) == 'funcdef':
                for grandchild in child.children:
                    state = process_func_part(state, grandchild)
                    if state == None:
                        break

            else:
                state = process_func_part(state, child)
                if state is None:
                    break

        name_with_prefix = self.name_with_prefix(self.func_name, prefix)
        self.func_name = None
        return name_with_prefix

    def process_class(self, node, prefix, decorators):

        def process_class_part(state, part):
            if state == 'class':
                raise isinstance(part, Leaf) and part.value == 'class' or AssertionError
            else:
                return 'classname'
                if state == 'classname':
                    if not (isinstance(part, Leaf) and part.type == 1):
                        raise AssertionError
                    self.class_name = part.value
                    name_with_prefix = self.name_with_prefix(self.class_name, prefix)
                    self.output_data.append('%s:source' % name_with_prefix, str(node).strip())
                    return 'parameters'
                    if state == 'parameters':
                        if isinstance(part, Leaf):
                            if part.value == ':':
                                return 'body'
                        return 'parameters'
                elif state == 'body':
                    assert self.type_of(part) == 'suite'
                    name_with_prefix = self.name_with_prefix(self.class_name, prefix)
                    docstring = self.first_simple_statement_after_any_whitespace(part)
                    if docstring is not None:
                        self.output_data.append('%s:doc' % name_with_prefix, inspect.cleandoc(docstring))
                    for child in part.children:
                        if self.type_of(child) in ('funcdef', 'decorated'):
                            self.process_node(child, self.name_with_prefix(self.class_name, prefix))

                else:
                    raise Exception("invalid state '%s'" % state)

        state = 'class'
        for child in node.children:
            if self.type_of(child) in ('decorator', 'decorators'):
                continue
            if self.type_of(child) == 'classdef':
                for grandchild in child.children:
                    state = process_class_part(state, grandchild)
                    if state == None:
                        break

            else:
                state = process_class_part(state, child)
                if state is None:
                    break

        name_with_prefix = self.name_with_prefix(self.class_name, prefix)
        self.class_name = None
        return name_with_prefix

    def process_simple_stmt(self, node, prefix, decorators):
        for child in node.children:
            child_type = self.type_of(child)
            if child_type == 'expr_stmt':
                if isinstance(child.children[0], Leaf):
                    name_leaf = child.children[0]
                    name = name_leaf.value
                    self.output_data.append('%s:source' % name, str(child))
                else:
                    continue