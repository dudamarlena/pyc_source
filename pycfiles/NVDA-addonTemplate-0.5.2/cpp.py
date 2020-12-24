# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\derek_2\Google Drive\nvda-addon-exploded\notepad++\scons-local-2.5.0\SCons\cpp.py
# Compiled at: 2016-07-07 03:21:31
__revision__ = 'src/engine/SCons/cpp.py rel_2.5.0:3543:937e55cd78f7 2016/04/09 11:29:54 bdbaddog'
__doc__ = '\nSCons C Pre-Processor module\n'
import SCons.compat, os, re
cpp_lines_dict = {('if', 'elif', 'ifdef', 'ifndef'): '\\s+(.+)', 
   ('import', 'include', 'include_next'): '\\s*(.+)', 
   ('else', 'endif'): '', 
   ('define',): '\\s+([_A-Za-z][_A-Za-z0-9_]*)(\\([^)]*\\))?\\s*(.*)', 
   ('undef',): '\\s+([_A-Za-z][A-Za-z0-9_]*)'}
Table = {}
for op_list, expr in cpp_lines_dict.items():
    e = re.compile(expr)
    for op in op_list:
        Table[op] = e

del e
del op
del op_list
override = {'if': 'if(?!def)'}
l = [ override.get(x, x) for x in Table.keys() ]
e = '^\\s*#\\s*(' + ('|').join(l) + ')(.*)$'
CPP_Expression = re.compile(e, re.M)
CPP_to_Python_Ops_Dict = {'!': ' not ', 
   '!=': ' != ', 
   '&&': ' and ', 
   '||': ' or ', 
   '?': ' and ', 
   ':': ' or ', 
   '\r': ''}
CPP_to_Python_Ops_Sub = lambda m: CPP_to_Python_Ops_Dict[m.group(0)]
l = sorted(CPP_to_Python_Ops_Dict.keys(), key=lambda a: len(a), reverse=True)
expr = ('|').join(map(re.escape, l))
CPP_to_Python_Ops_Expression = re.compile(expr)
CPP_to_Python_Eval_List = [
 [
  'defined\\s+(\\w+)', '"\\1" in __dict__'],
 [
  'defined\\s*\\((\\w+)\\)', '"\\1" in __dict__'],
 [
  '/\\*.*\\*/', ''],
 [
  '/\\*.*', ''],
 [
  '//.*', ''],
 [
  '(0x[0-9A-Fa-f]*)[UL]+', '\\1']]
for l in CPP_to_Python_Eval_List:
    l[0] = re.compile(l[0])

def CPP_to_Python(s):
    """
    Converts a C pre-processor expression into an equivalent
    Python expression that can be evaluated.
    """
    s = CPP_to_Python_Ops_Expression.sub(CPP_to_Python_Ops_Sub, s)
    for expr, repl in CPP_to_Python_Eval_List:
        s = expr.sub(repl, s)

    return s


del expr
del l
del override

class FunctionEvaluator(object):
    """
    Handles delayed evaluation of a #define function call.
    """

    def __init__(self, name, args, expansion):
        """
        Squirrels away the arguments and expansion value of a #define
        macro function for later evaluation when we must actually expand
        a value that uses it.
        """
        self.name = name
        self.args = function_arg_separator.split(args)
        try:
            expansion = expansion.split('##')
        except AttributeError:
            pass

        self.expansion = expansion

    def __call__(self, *values):
        """
        Evaluates the expansion of a #define macro function called
        with the specified values.
        """
        if len(self.args) != len(values):
            raise ValueError("Incorrect number of arguments to `%s'" % self.name)
        locals = {}
        for k, v in zip(self.args, values):
            locals[k] = v

        parts = []
        for s in self.expansion:
            if s not in self.args:
                s = repr(s)
            parts.append(s)

        statement = (' + ').join(parts)
        return eval(statement, globals(), locals)


line_continuations = re.compile('\\\\\r?\n')
function_name = re.compile('(\\S+)\\(([^)]*)\\)')
function_arg_separator = re.compile(',\\s*')

class PreProcessor(object):
    """
    The main workhorse class for handling C pre-processing.
    """

    def __init__(self, current=os.curdir, cpppath=(), dict={}, all=0):
        global Table
        cpppath = tuple(cpppath)
        self.searchpath = {'"': (
               current,) + cpppath, 
           '<': cpppath + (current,)}
        self.cpp_namespace = dict.copy()
        self.cpp_namespace['__dict__'] = self.cpp_namespace
        if all:
            self.do_include = self.all_include
        d = {'scons_current_file': self.scons_current_file}
        for op in Table.keys():
            d[op] = getattr(self, 'do_' + op)

        self.default_table = d

    def tupleize(self, contents):
        """
        Turns the contents of a file into a list of easily-processed
        tuples describing the CPP lines in the file.

        The first element of each tuple is the line's preprocessor
        directive (#if, #include, #define, etc., minus the initial '#').
        The remaining elements are specific to the type of directive, as
        pulled apart by the regular expression.
        """
        global CPP_Expression
        contents = line_continuations.sub('', contents)
        cpp_tuples = CPP_Expression.findall(contents)
        return [ (m[0],) + Table[m[0]].match(m[1]).groups() for m in cpp_tuples ]

    def __call__(self, file):
        """
        Pre-processes a file.

        This is the main public entry point.
        """
        self.current_file = file
        return self.process_contents(self.read_file(file), file)

    def process_contents(self, contents, fname=None):
        """
        Pre-processes a file contents.

        This is the main internal entry point.
        """
        self.stack = []
        self.dispatch_table = self.default_table.copy()
        self.current_file = fname
        self.tuples = self.tupleize(contents)
        self.initialize_result(fname)
        while self.tuples:
            t = self.tuples.pop(0)
            self.dispatch_table[t[0]](t)

        return self.finalize_result(fname)

    def save(self):
        """
        Pushes the current dispatch table on the stack and re-initializes
        the current dispatch table to the default.
        """
        self.stack.append(self.dispatch_table)
        self.dispatch_table = self.default_table.copy()

    def restore(self):
        """
        Pops the previous dispatch table off the stack and makes it the
        current one.
        """
        try:
            self.dispatch_table = self.stack.pop()
        except IndexError:
            pass

    def do_nothing(self, t):
        """
        Null method for when we explicitly want the action for a
        specific preprocessor directive to do nothing.
        """
        pass

    def scons_current_file(self, t):
        self.current_file = t[1]

    def eval_expression(self, t):
        """
        Evaluates a C preprocessor expression.

        This is done by converting it to a Python equivalent and
        eval()ing it in the C preprocessor namespace we use to
        track #define values.
        """
        t = CPP_to_Python((' ').join(t[1:]))
        try:
            return eval(t, self.cpp_namespace)
        except (NameError, TypeError):
            return 0

    def initialize_result(self, fname):
        self.result = [
         fname]

    def finalize_result(self, fname):
        return self.result[1:]

    def find_include_file(self, t):
        """
        Finds the #include file for a given preprocessor tuple.
        """
        fname = t[2]
        for d in self.searchpath[t[1]]:
            if d == os.curdir:
                f = fname
            else:
                f = os.path.join(d, fname)
            if os.path.isfile(f):
                return f

        return

    def read_file(self, file):
        return open(file).read()

    def start_handling_includes(self, t=None):
        """
        Causes the PreProcessor object to start processing #import,
        #include and #include_next lines.

        This method will be called when a #if, #ifdef, #ifndef or #elif
        evaluates True, or when we reach the #else in a #if, #ifdef,
        #ifndef or #elif block where a condition already evaluated
        False.

        """
        d = self.dispatch_table
        p = self.stack[(-1)] if self.stack else self.default_table
        for k in ('import', 'include', 'include_next'):
            d[k] = p[k]

    def stop_handling_includes(self, t=None):
        """
        Causes the PreProcessor object to stop processing #import,
        #include and #include_next lines.

        This method will be called when a #if, #ifdef, #ifndef or #elif
        evaluates False, or when we reach the #else in a #if, #ifdef,
        #ifndef or #elif block where a condition already evaluated True.
        """
        d = self.dispatch_table
        d['import'] = self.do_nothing
        d['include'] = self.do_nothing
        d['include_next'] = self.do_nothing

    def _do_if_else_condition(self, condition):
        """
        Common logic for evaluating the conditions on #if, #ifdef and
        #ifndef lines.
        """
        self.save()
        d = self.dispatch_table
        if condition:
            self.start_handling_includes()
            d['elif'] = self.stop_handling_includes
            d['else'] = self.stop_handling_includes
        else:
            self.stop_handling_includes()
            d['elif'] = self.do_elif
            d['else'] = self.start_handling_includes

    def do_ifdef(self, t):
        """
        Default handling of a #ifdef line.
        """
        self._do_if_else_condition(t[1] in self.cpp_namespace)

    def do_ifndef(self, t):
        """
        Default handling of a #ifndef line.
        """
        self._do_if_else_condition(t[1] not in self.cpp_namespace)

    def do_if(self, t):
        """
        Default handling of a #if line.
        """
        self._do_if_else_condition(self.eval_expression(t))

    def do_elif(self, t):
        """
        Default handling of a #elif line.
        """
        d = self.dispatch_table
        if self.eval_expression(t):
            self.start_handling_includes()
            d['elif'] = self.stop_handling_includes
            d['else'] = self.stop_handling_includes

    def do_else(self, t):
        """
        Default handling of a #else line.
        """
        pass

    def do_endif(self, t):
        """
        Default handling of a #endif line.
        """
        self.restore()

    def do_define(self, t):
        """
        Default handling of a #define line.
        """
        _, name, args, expansion = t
        try:
            expansion = int(expansion)
        except (TypeError, ValueError):
            pass

        if args:
            evaluator = FunctionEvaluator(name, args[1:-1], expansion)
            self.cpp_namespace[name] = evaluator
        else:
            self.cpp_namespace[name] = expansion

    def do_undef(self, t):
        """
        Default handling of a #undef line.
        """
        try:
            del self.cpp_namespace[t[1]]
        except KeyError:
            pass

    def do_import(self, t):
        """
        Default handling of a #import line.
        """
        pass

    def do_include(self, t):
        """
        Default handling of a #include line.
        """
        t = self.resolve_include(t)
        include_file = self.find_include_file(t)
        if include_file:
            self.result.append(include_file)
            contents = self.read_file(include_file)
            new_tuples = [
             (
              'scons_current_file', include_file)] + self.tupleize(contents) + [
             (
              'scons_current_file', self.current_file)]
            self.tuples[:] = new_tuples + self.tuples

    do_include_next = do_include

    def resolve_include(self, t):
        """Resolve a tuple-ized #include line.

        This handles recursive expansion of values without "" or <>
        surrounding the name until an initial " or < is found, to handle
                #include FILE
        where FILE is a #define somewhere else.
        """
        s = t[1]
        while s[0] not in '<"':
            try:
                s = self.cpp_namespace[s]
            except KeyError:
                m = function_name.search(s)
                s = self.cpp_namespace[m.group(1)]
                if callable(s):
                    args = function_arg_separator.split(m.group(2))
                    s = s(*args)

            if not s:
                return None

        return (
         t[0], s[0], s[1:-1])

    def all_include(self, t):
        """
        """
        self.result.append(self.resolve_include(t))


class DumbPreProcessor(PreProcessor):
    """A preprocessor that ignores all #if/#elif/#else/#endif directives
    and just reports back *all* of the #include files (like the classic
    SCons scanner did).

    This is functionally equivalent to using a regular expression to
    find all of the #include lines, only slower.  It exists mainly as
    an example of how the main PreProcessor class can be sub-classed
    to tailor its behavior.
    """

    def __init__(self, *args, **kw):
        PreProcessor.__init__(self, *args, **kw)
        d = self.default_table
        for func in ['if', 'elif', 'else', 'endif', 'ifdef', 'ifndef']:
            d[func] = d[func] = self.do_nothing


del __revision__