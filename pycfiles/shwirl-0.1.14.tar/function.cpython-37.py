# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/vohl/Documents/code/shwirl/shwirl/extern/vispy/visuals/shaders/function.py
# Compiled at: 2018-10-01 14:58:41
# Size of source mod 2**32: 26400 bytes
"""
Classses representing GLSL objects (functions, variables, etc) that may be
composed together to create complete shaders. 
See the docstring of Function for details.

Details
-------

A complete GLSL program is composed of ShaderObjects, each of which may be used
inline as an expression, and some of which include a definition that must be
included on the final code. ShaderObjects keep track of a hierarchy of
dependencies so that all necessary code is included at compile time, and
changes made to any object may be propagated to the root of the hierarchy to 
trigger a recompile.
"""
import re, logging, numpy as np
import util.eq as eq
from ...util import logger
from ext.ordereddict import OrderedDict
from ext.six import string_types
from . import parsing
from .shader_object import ShaderObject
from .variable import Variable, Varying
from .expression import TextExpression, FunctionCall

class Function(ShaderObject):
    __doc__ = 'Representation of a GLSL function\n    \n    Objects of this class can be used for re-using and composing GLSL\n    snippets. Each Function consists of a GLSL snippet in the form of\n    a function. The code may have template variables that start with\n    the dollar sign. These stubs can be replaced with expressions using\n    the index operation. Expressions can be:\n    \n    * plain text that is inserted verbatim in the code\n    * a Function object or a call to a funcion\n    * a Variable (or Varying) object\n    * float, int, tuple are automatically turned into a uniform Variable\n    * a VertexBuffer is automatically turned into an attribute Variable\n    \n    All functions have implicit "$pre" and "$post" placeholders that may be\n    used to insert code at the beginning and end of the function.\n    \n    Examples\n    --------\n    This example shows the basic usage of the Function class::\n\n        vert_code_template = Function(\'\'\'\n            void main() {\n            gl_Position = $pos;\n            gl_Position.x += $xoffset;\n            gl_Position.y += $yoffset;\n        }\'\'\')\n        \n        scale_transform = Function(\'\'\'\n        vec4 transform_scale(vec4 pos){\n            return pos * $scale;\n        }\'\'\')\n        \n        # If you get the function from a snippet collection, always\n        # create new Function objects to ensure they are \'fresh\'.\n        vert_code = Function(vert_code_template)\n        trans1 = Function(scale_transform)\n        trans2 = Function(scale_transform)  # trans2 != trans1\n        \n        # Three ways to assign to template variables:\n        #\n        # 1) Assign verbatim code\n        vert_code[\'xoffset\'] = \'(3.0 / 3.1415)\'\n        \n        # 2) Assign a value (this creates a new uniform or attribute)\n        vert_code[\'yoffset\'] = 5.0\n        \n        # 3) Assign a function call expression\n        pos_var = Variable(\'attribute vec4 a_position\')\n        vert_code[\'pos\'] = trans1(trans2(pos_var))\n        \n        # Transforms also need their variables set\n        trans1[\'scale\'] = 0.5\n        trans2[\'scale\'] = (1.0, 0.5, 1.0, 1.0)\n        \n        # You can actually change any code you want, but use this with care!\n        vert_code.replace(\'gl_Position.y\', \'gl_Position.z\')\n        \n        # Finally, you can set special variables explicitly. This generates\n        # a new statement at the end of the vert_code function.\n        vert_code[\'gl_PointSize\'] = \'10.\'\n    \n    \n    If we use ``vert_code.compile()`` we get::\n\n        attribute vec4 a_position;\n        uniform float u_yoffset;\n        uniform float u_scale_1;\n        uniform vec4 u_scale_2;\n        uniform float u_pointsize;\n        \n        vec4 transform_scale_1(vec4 pos){\n            return pos * u_scale_1;\n        }\n        \n        vec4 transform_scale_2(vec4 pos){\n            return pos * u_scale_2;\n        }\n        \n        void main() {\n            gl_Position = transform_scale_1(transform_scale_2(a_position));\n            gl_Position.x += (3.0 / 3.1415);\n            gl_Position.z += u_yoffset;\n        \n            gl_PointSize = u_pointsize;\n        }\n    \n    Note how the two scale function resulted in two different functions\n    and two uniforms for the scale factors.\n    \n    Function calls\n    --------------\n    \n    As can be seen above, the arguments with which a function is to be\n    called must be specified by calling the Function object. The\n    arguments can be any of the expressions mentioned earlier. If the\n    signature is already specified in the template code, that function\n    itself must be given.\n    \n        code = Function(\'\'\'\n            void main() {\n                vec4 position = $pos;\n                gl_Position = $scale(position)\n            }\n        \'\'\')\n        \n        # Example of a function call with all possible three expressions\n        vert_code[\'pos\'] = func1(\'3.0\', \'uniform float u_param\', func2())\n        \n        # For scale, the sigfnature is already specified\n        code[\'scale\'] = scale_func  # Must not specify args\n    \n    Data for uniform and attribute variables\n    ----------------------------------------\n    To each variable a value can be associated. In fact, in most cases\n    the Function class is smart enough to be able to create a Variable\n    object if only the data is given.\n    \n        code[\'offset\'] = Variable(\'uniform float offset\')  # No data\n        code[\'offset\'] = Variable(\'uniform float offset\', 3.0)  # With data\n        code[\'offset\'] = 3.0  # -> Uniform Variable\n        position[\'position\'] = VertexBuffer()  # -> attribute Variable\n        \n        # Updating variables\n        code[\'offset\'].value = 4.0\n        position[\'position\'].value.set_data(...)\n    '

    def __init__(self, code, dependencies=None):
        super(Function, self).__init__()
        if dependencies is not None:
            for dep in dependencies:
                self._add_dep(dep)

        self.code = code
        self._expressions = OrderedDict()
        self._replacements = OrderedDict()
        self._assignments = OrderedDict()

    def __setitem__(self, key, val):
        """ Setting of replacements through a dict-like syntax.
        
        Each replacement can be:
        * verbatim code: ``fun1['foo'] = '3.14159'``
        * a FunctionCall: ``fun1['foo'] = fun2()``
        * a Variable: ``fun1['foo'] = Variable(...)`` (can be auto-generated)
        """
        if isinstance(key, Variable):
            if key.vtype == 'varying':
                if self.name != 'main':
                    raise Exception("Varying assignment only alowed in 'main' function.")
                storage = self._assignments
            else:
                raise TypeError('Variable assignment only allowed for varyings, not %s (in %s)' % (
                 key.vtype, self.name))
        elif isinstance(key, string_types):
            if any(map(key.startswith, ('gl_PointSize', 'gl_Position', 'gl_FragColor'))):
                storage = self._assignments
            elif key in self.template_vars or key in ('pre', 'post'):
                storage = self._expressions
            else:
                raise KeyError('Invalid template variable %r' % key)
        else:
            raise TypeError('In `function[key]` key must be a string or varying.')
        if eq(storage.get(key), val):
            return
        if val is not None and not isinstance(val, Variable):
            variable = storage.get(key, None)
            if isinstance(variable, Variable):
                if np.any(variable.value != val):
                    variable.value = val
                    self.changed(value_changed=True)
                return
            val = ShaderObject.create(val, ref=key)
            if variable is val:
                return
            oldval = storage.pop(key, None)
            if oldval is not None:
                for obj in (key, oldval):
                    if isinstance(obj, ShaderObject):
                        self._remove_dep(obj)

            if val is not None:
                if isinstance(key, Varying):
                    key.link(val)
                storage[key] = val
                for obj in (key, val):
                    if isinstance(obj, ShaderObject):
                        self._add_dep(obj)

            if isinstance(val, TextExpression):
                for var in parsing.find_template_variables(val.expression()):
                    if var not in self.template_vars:
                        self.template_vars.add(var.lstrip('$'))

            self.changed(code_changed=True, value_changed=True)
            if logger.level <= logging.DEBUG:
                import traceback
                last = traceback.format_list(traceback.extract_stack()[-2:-1])
                logger.debug('Assignment would trigger shader recompile:\nOriginal:\n%r\nReplacement:\n%r\nSource:\n%s', oldval, val, ''.join(last))

    def __getitem__(self, key):
        """ Return a reference to a program variable from this function.

        This allows variables between functions to be linked together::

            func1['var_name'] = func2['other_var_name']

        In the example above, the two local variables would be assigned to the
        same program variable whenever func1 and func2 are attached to the same
        program.
        """
        try:
            return self._expressions[key]
        except KeyError:
            pass

        try:
            return self._assignments[key]
        except KeyError:
            pass

        if key not in self.template_vars:
            raise KeyError('Invalid template variable %r' % key)
        else:
            raise KeyError('No value known for key %r' % key)

    def __call__(self, *args):
        """ Set the signature for this function and return an FunctionCall
        object. Each argument can be verbatim code or a FunctionCall object.
        """
        return FunctionCall(self, args)

    @property
    def signature(self):
        if self._signature is None:
            try:
                self._signature = parsing.parse_function_signature(self._code)
            except Exception as err:
                try:
                    raise ValueError('Invalid code: ' + str(err))
                finally:
                    err = None
                    del err

        return self._signature

    @property
    def name(self):
        """ The function name. The name may be mangled in the final code
        to avoid name clashes.
        """
        return self.signature[0]

    @property
    def args(self):
        """
        List of input arguments in the function signature::

            [(arg_name, arg_type), ...]
        """
        return self.signature[1]

    @property
    def rtype(self):
        """
        The return type of this function.
        """
        return self.signature[2]

    @property
    def code(self):
        """ The template code used to generate the definition for this 
        function.
        """
        return self._code

    @code.setter
    def code(self, code):
        if isinstance(code, Function):
            code = code._code
        else:
            if not isinstance(code, string_types):
                raise ValueError('Function needs a string or Function; got %s.' % type(code))
        self._code = self._clean_code(code)
        self._signature = None
        self._template_vars = None
        self._static_vars = None

    @property
    def template_vars(self):
        if self._template_vars is None:
            self._template_vars = self._parse_template_vars()
        return self._template_vars

    def static_names(self):
        if self._static_vars is None:
            self._static_vars = parsing.find_program_variables(self._code)
        return list(self._static_vars.keys()) + [arg[0] for arg in self.args]

    def replace(self, str1, str2):
        """ Set verbatim code replacement
        
        It is strongly recommended to use function['$foo'] = 'bar' where
        possible because template variables are less likely to changed
        than the code itself in future versions of vispy.
        
        Parameters
        ----------
        str1 : str
            String to replace
        str2 : str
            String to replace str1 with
        """
        if str2 != self._replacements.get(str1, None):
            self._replacements[str1] = str2
            self.changed(code_changed=True)

    def _parse_template_vars(self):
        """ find all template variables in self._code, excluding the
        function name. 
        """
        template_vars = set()
        for var in parsing.find_template_variables(self._code):
            var = var.lstrip('$')
            if var == self.name:
                continue
            if var in ('pre', 'post'):
                raise ValueError('GLSL uses reserved template variable $%s' % var)
            template_vars.add(var)

        return template_vars

    def _get_replaced_code(self, names):
        """ Return code, with new name, expressions, and replacements applied.
        """
        code = self._code
        fname = names[self]
        code = code.replace(' ' + self.name + '(', ' ' + fname + '(')
        for key, val in self._replacements.items():
            code = code.replace(key, val)

        post_lines = []
        for key, val in self._assignments.items():
            if isinstance(key, Variable):
                key = names[key]
            if isinstance(val, ShaderObject):
                val = val.expression(names)
            line = '    %s = %s;' % (key, val)
            post_lines.append(line)

        if 'post' in self._expressions:
            post_lines.append('    $post')
        post_text = '\n'.join(post_lines)
        if post_text:
            post_text = '\n' + post_text + '\n'
        code = code.rpartition('}')
        code = code[0] + post_text + code[1] + code[2]
        if 'pre' in self._expressions:
            m = re.search(fname + '\\s*\\([^{]*\\)\\s*{', code)
            if m is None:
                raise RuntimeError("Cound not find beginning of function '%s'" % fname)
            ind = m.span()[1]
            code = code[:ind] + '\n    $pre\n' + code[ind:]
        for key, val in self._expressions.items():
            val = val.expression(names)
            search = '\\$' + key + '($|[^a-zA-Z0-9_])'
            code = re.sub(search, val + '\\1', code)

        if '$' in code:
            v = parsing.find_template_variables(code)
            logger.warning('Unsubstituted placeholders in code: %s\n  replacements made: %s', v, list(self._expressions.keys()))
        return code + '\n'

    def definition(self, names):
        return self._get_replaced_code(names)

    def expression(self, names):
        return names[self]

    def _clean_code(self, code):
        """ Return *code* with indentation and leading/trailing blank lines
        removed. 
        """
        lines = code.split('\n')
        min_indent = 100
        for line in lines:
            if line.strip() != '':
                indent = len(line) - len(line.lstrip())
                min_indent = min(indent, min_indent)

        if min_indent > 0:
            lines = [line[min_indent:] for line in lines]
        code = '\n'.join(lines)
        return code

    def __repr__(self):
        try:
            args = ', '.join([' '.join(arg) for arg in self.args])
        except Exception:
            return '<%s (error parsing signature) at 0x%x>' % (
             self.__class__.__name__, id(self))
        else:
            return '<%s "%s %s(%s)" at 0x%x>' % (self.__class__.__name__,
             self.rtype,
             self.name,
             args,
             id(self))


class MainFunction(Function):
    __doc__ = ' Subclass of Function that allows multiple functions and variables to \n    be defined in a single code string. The code must contain a main() function\n    definition.\n    '

    def __init__(self, *args, **kwargs):
        self._chains = {}
        (Function.__init__)(self, *args, **kwargs)

    @property
    def signature(self):
        return ('main', [], 'void')

    def static_names(self):
        if self._static_vars is not None:
            return self._static_vars
        names = Function.static_names(self)
        funcs = parsing.find_functions(self.code)
        for f in funcs:
            if f[0] == 'main':
                continue
            names.append(f[0])
            for arg in f[1]:
                names.append(arg[1])

        self._static_vars = names
        return names

    def add_chain(self, var):
        """
        Create a new ChainFunction and attach to $var.
        """
        chain = FunctionChain(var, [])
        self._chains[var] = chain
        self[var] = chain

    def add_callback(self, hook, func):
        self._chains[hook].append(func)

    def remove_callback(self, hook, func):
        self._chains[hook].remove(func)


class FunctionChain(Function):
    __doc__ = "Subclass that generates GLSL code to call Function list in order\n\n    Functions may be called independently, or composed such that the\n    output of each function provides the input to the next.\n\n    Parameters\n    ----------\n    name : str\n        The name of the generated function\n    funcs : list of Functions\n        The list of Functions that will be called by the generated GLSL code.\n\n    Examples\n    --------\n    This creates a function chain:\n\n        >>> func1 = Function('void my_func_1() {}')\n        >>> func2 = Function('void my_func_2() {}')\n        >>> chain = FunctionChain('my_func_chain', [func1, func2])\n\n    If *chain* is included in a ModularProgram, it will generate the following\n    output:\n\n        void my_func_1() {}\n        void my_func_2() {}\n\n        void my_func_chain() {\n            my_func_1();\n            my_func_2();\n        }\n\n    The return type of the generated function is the same as the return type\n    of the last function in the chain. Likewise, the arguments for the\n    generated function are the same as the first function in the chain.\n\n    If the return type is not 'void', then the return value of each function\n    will be used to supply the first input argument of the next function in\n    the chain. For example:\n\n        vec3 my_func_1(vec3 input) {return input + vec3(1, 0, 0);}\n        void my_func_2(vec3 input) {return input + vec3(0, 1, 0);}\n\n        vec3 my_func_chain(vec3 input) {\n            return my_func_2(my_func_1(input));\n        }\n    "

    def __init__(self, name=None, funcs=()):
        ShaderObject.__init__(self)
        if not name is None:
            if not isinstance(name, string_types):
                raise TypeError('Name argument must be string or None.')
        self._funcs = []
        self._code = None
        self._name = name or 'chain'
        self._args = []
        self._rtype = 'void'
        self.functions = funcs

    @property
    def functions(self):
        return self._funcs[:]

    @functions.setter
    def functions(self, funcs):
        while self._funcs:
            self.remove((self._funcs[0]), update=False)

        for f in funcs:
            self.append(f, update=False)

        self._update()

    @property
    def signature(self):
        return (self._name, self._args, self._rtype)

    def _update(self):
        funcs = self._funcs
        if len(funcs) > 0:
            self._rtype = funcs[(-1)].rtype
            self._args = funcs[0].args[:]
        else:
            self._rtype = 'void'
            self._args = []
        self.changed(code_changed=True)

    @property
    def code(self):
        pass

    @code.setter
    def code(self, c):
        raise TypeError('Cannot set code property on FunctionChain.')

    @property
    def template_vars(self):
        return {}

    def append(self, function, update=True):
        """ Append a new function to the end of this chain.
        """
        self._funcs.append(function)
        self._add_dep(function)
        if update:
            self._update()

    def __setitem__(self, index, func):
        self._remove_dep(self._funcs[index])
        self._add_dep(func)
        self._funcs[index] = func
        self._update()

    def __getitem__(self, k):
        return self.functions[k]

    def insert(self, index, function, update=True):
        """ Insert a new function into the chain at *index*.
        """
        self._funcs.insert(index, function)
        self._add_dep(function)
        if update:
            self._update()

    def remove(self, function, update=True):
        """ Remove a function from the chain.
        """
        self._funcs.remove(function)
        self._remove_dep(function)
        if update:
            self._update()

    def definition(self, obj_names):
        name = obj_names[self]
        args = ', '.join(['%s %s' % arg for arg in self.args])
        code = '%s %s(%s) {\n' % (self.rtype, name, args)
        result_index = 0
        if len(self.args) == 0:
            last_rtype = 'void'
            last_result = ''
        else:
            last_rtype, last_result = self.args[0][:2]
        for fn in self._funcs:
            if last_rtype == 'void':
                args = ''
            else:
                args = last_result
                if not len(fn.args) != 1:
                    if last_rtype != fn.args[0][0]:
                        raise Exception("Cannot chain output '%s' of function to input of '%s'" % (
                         last_rtype, fn.signature))
                else:
                    last_rtype = fn.rtype
                    if fn.rtype == 'void':
                        set_str = ''
                    else:
                        result_index += 1
                    result = 'result_%d' % result_index
                    set_str = '%s %s = ' % (fn.rtype, result)
                    last_result = result
                code += '    %s%s(%s);\n' % (set_str, obj_names[fn], args)

        if self.rtype != 'void':
            code += '    return result_%d;\n' % result_index
        code += '}\n'
        return code

    def static_names(self):
        return []

    def __repr__(self):
        fn = ',\n                '.join(map(repr, self.functions))
        return '<FunctionChain [%s] at 0x%x>' % (fn, id(self))


class StatementList(ShaderObject):
    __doc__ = 'Represents a list of statements. \n    '

    def __init__(self):
        self.items = {}
        self.order = []
        ShaderObject.__init__(self)

    def add(self, item, position=5):
        """Add an item to the list unless it is already present.
        
        If the item is an expression, then a semicolon will be appended to it
        in the final compiled code.
        """
        if item in self.items:
            return
        self.items[item] = position
        self._add_dep(item)
        self.order = None
        self.changed(code_changed=True)

    def remove(self, item):
        """Remove an item from the list.
        """
        self.items.pop(item)
        self._remove_dep(item)
        self.order = None
        self.changed(code_changed=True)

    def expression(self, obj_names):
        if self.order is None:
            self.order = list(self.items.items())
            self.order.sort(key=(lambda x: x[1]))
        code = ''
        for item, pos in self.order:
            code += item.expression(obj_names) + ';\n'

        return code