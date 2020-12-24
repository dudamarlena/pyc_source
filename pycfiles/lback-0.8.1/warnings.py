# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: warnings.pyc
# Compiled at: 2011-03-08 12:43:28
"""Python part of the warnings subsystem."""
import linecache, sys, types
__all__ = [
 'warn', 'showwarning', 'formatwarning', 'filterwarnings',
 'resetwarnings', 'catch_warnings']

def warnpy3k(message, category=None, stacklevel=1):
    """Issue a deprecation warning for Python 3.x related changes.

    Warnings are omitted unless Python is started with the -3 option.
    """
    if sys.py3kwarning:
        if category is None:
            category = DeprecationWarning
        warn(message, category, stacklevel + 1)
    return


def _show_warning(message, category, filename, lineno, file=None, line=None):
    """Hook to write a warning to a file; replace if you like."""
    if file is None:
        file = sys.stderr
    try:
        file.write(formatwarning(message, category, filename, lineno, line))
    except IOError:
        pass

    return


showwarning = _show_warning

def formatwarning(message, category, filename, lineno, line=None):
    """Function to format a warning the standard way."""
    s = '%s:%s: %s: %s\n' % (filename, lineno, category.__name__, message)
    line = linecache.getline(filename, lineno) if line is None else line
    if line:
        line = line.strip()
        s += '  %s\n' % line
    return s


def filterwarnings--- This code section failed: ---

 L.  57         0  LOAD_CONST               -1
                3  LOAD_CONST               None
                6  IMPORT_NAME           0  're'
                9  STORE_FAST            6  're'

 L.  58        12  LOAD_FAST             0  'action'

 L.  59        15  LOAD_CONST               ('error', 'ignore', 'always', 'default', 'module', 'once')
               18  COMPARE_OP            6  in
               21  POP_JUMP_IF_TRUE     40  'to 40'
               24  LOAD_ASSERT              AssertionError
               27  LOAD_CONST               'invalid action: %r'
               30  LOAD_FAST             0  'action'
               33  BUILD_TUPLE_1         1 
               36  BINARY_MODULO    
               37  RAISE_VARARGS_2       2  None

 L.  60        40  LOAD_GLOBAL           2  'isinstance'
               43  LOAD_FAST             1  'message'
               46  LOAD_GLOBAL           3  'basestring'
               49  CALL_FUNCTION_2       2  None
               52  POP_JUMP_IF_TRUE     64  'to 64'
               55  LOAD_ASSERT              AssertionError
               58  LOAD_CONST               'message must be a string'
               61  RAISE_VARARGS_2       2  None

 L.  61        64  LOAD_GLOBAL           2  'isinstance'
               67  LOAD_FAST             2  'category'
               70  LOAD_GLOBAL           4  'type'
               73  LOAD_GLOBAL           5  'types'
               76  LOAD_ATTR             6  'ClassType'
               79  BUILD_TUPLE_2         2 
               82  CALL_FUNCTION_2       2  None
               85  POP_JUMP_IF_TRUE     97  'to 97'
               88  LOAD_ASSERT              AssertionError

 L.  62        91  LOAD_CONST               'category must be a class'
               94  RAISE_VARARGS_2       2  None

 L.  63        97  LOAD_GLOBAL           7  'issubclass'
              100  LOAD_FAST             2  'category'
              103  LOAD_GLOBAL           8  'Warning'
              106  CALL_FUNCTION_2       2  None
              109  POP_JUMP_IF_TRUE    121  'to 121'
              112  LOAD_ASSERT              AssertionError
              115  LOAD_CONST               'category must be a Warning subclass'
              118  RAISE_VARARGS_2       2  None

 L.  64       121  LOAD_GLOBAL           2  'isinstance'
              124  LOAD_FAST             3  'module'
              127  LOAD_GLOBAL           3  'basestring'
              130  CALL_FUNCTION_2       2  None
              133  POP_JUMP_IF_TRUE    145  'to 145'
              136  LOAD_ASSERT              AssertionError
              139  LOAD_CONST               'module must be a string'
              142  RAISE_VARARGS_2       2  None

 L.  65       145  LOAD_GLOBAL           2  'isinstance'
              148  LOAD_FAST             4  'lineno'
              151  LOAD_GLOBAL           9  'int'
              154  CALL_FUNCTION_2       2  None
              157  POP_JUMP_IF_FALSE   172  'to 172'
              160  LOAD_FAST             4  'lineno'
              163  LOAD_CONST               0
              166  COMPARE_OP            5  >=
            169_0  COME_FROM           157  '157'
              169  POP_JUMP_IF_TRUE    181  'to 181'
              172  LOAD_ASSERT              AssertionError

 L.  66       175  LOAD_CONST               'lineno must be an int >= 0'
              178  RAISE_VARARGS_2       2  None

 L.  67       181  LOAD_FAST             0  'action'
              184  LOAD_FAST             6  're'
              187  LOAD_ATTR            10  'compile'
              190  LOAD_FAST             1  'message'
              193  LOAD_FAST             6  're'
              196  LOAD_ATTR            11  'I'
              199  CALL_FUNCTION_2       2  None
              202  LOAD_FAST             2  'category'

 L.  68       205  LOAD_FAST             6  're'
              208  LOAD_ATTR            10  'compile'
              211  LOAD_FAST             3  'module'
              214  CALL_FUNCTION_1       1  None
              217  LOAD_FAST             4  'lineno'
              220  BUILD_TUPLE_5         5 
              223  STORE_FAST            7  'item'

 L.  69       226  LOAD_FAST             5  'append'
              229  POP_JUMP_IF_FALSE   248  'to 248'

 L.  70       232  LOAD_GLOBAL          12  'filters'
              235  LOAD_ATTR            13  'append'
              238  LOAD_FAST             7  'item'
              241  CALL_FUNCTION_1       1  None
              244  POP_TOP          
              245  JUMP_FORWARD         16  'to 264'

 L.  72       248  LOAD_GLOBAL          12  'filters'
              251  LOAD_ATTR            14  'insert'
              254  LOAD_CONST               0
              257  LOAD_FAST             7  'item'
              260  CALL_FUNCTION_2       2  None
              263  POP_TOP          
            264_0  COME_FROM           245  '245'

Parse error at or near `POP_TOP' instruction at offset 263


def simplefilter--- This code section failed: ---

 L.  84         0  LOAD_FAST             0  'action'

 L.  85         3  LOAD_CONST               ('error', 'ignore', 'always', 'default', 'module', 'once')
                6  COMPARE_OP            6  in
                9  POP_JUMP_IF_TRUE     28  'to 28'
               12  LOAD_ASSERT              AssertionError
               15  LOAD_CONST               'invalid action: %r'
               18  LOAD_FAST             0  'action'
               21  BUILD_TUPLE_1         1 
               24  BINARY_MODULO    
               25  RAISE_VARARGS_2       2  None

 L.  86        28  LOAD_GLOBAL           1  'isinstance'
               31  LOAD_FAST             2  'lineno'
               34  LOAD_GLOBAL           2  'int'
               37  CALL_FUNCTION_2       2  None
               40  POP_JUMP_IF_FALSE    55  'to 55'
               43  LOAD_FAST             2  'lineno'
               46  LOAD_CONST               0
               49  COMPARE_OP            5  >=
             52_0  COME_FROM            40  '40'
               52  POP_JUMP_IF_TRUE     64  'to 64'
               55  LOAD_ASSERT              AssertionError

 L.  87        58  LOAD_CONST               'lineno must be an int >= 0'
               61  RAISE_VARARGS_2       2  None

 L.  88        64  LOAD_FAST             0  'action'
               67  LOAD_CONST               None
               70  LOAD_FAST             1  'category'
               73  LOAD_CONST               None
               76  LOAD_FAST             2  'lineno'
               79  BUILD_TUPLE_5         5 
               82  STORE_FAST            4  'item'

 L.  89        85  LOAD_FAST             3  'append'
               88  POP_JUMP_IF_FALSE   107  'to 107'

 L.  90        91  LOAD_GLOBAL           4  'filters'
               94  LOAD_ATTR             5  'append'
               97  LOAD_FAST             4  'item'
              100  CALL_FUNCTION_1       1  None
              103  POP_TOP          
              104  JUMP_FORWARD         16  'to 123'

 L.  92       107  LOAD_GLOBAL           4  'filters'
              110  LOAD_ATTR             6  'insert'
              113  LOAD_CONST               0
              116  LOAD_FAST             4  'item'
              119  CALL_FUNCTION_2       2  None
              122  POP_TOP          
            123_0  COME_FROM           104  '104'
              123  LOAD_CONST               None
              126  RETURN_VALUE     

Parse error at or near `LOAD_CONST' instruction at offset 123


def resetwarnings():
    """Clear the list of warning filters, so that no filters are active."""
    filters[:] = []


class _OptionError(Exception):
    """Exception used by option processing helpers."""
    pass


def _processoptions(args):
    for arg in args:
        try:
            _setoption(arg)
        except _OptionError as msg:
            print >> sys.stderr, 'Invalid -W option ignored:', msg


def _setoption(arg):
    import re
    parts = arg.split(':')
    if len(parts) > 5:
        raise _OptionError('too many fields (max 5): %r' % (arg,))
    while len(parts) < 5:
        parts.append('')

    action, message, category, module, lineno = [ s.strip() for s in parts ]
    action = _getaction(action)
    message = re.escape(message)
    category = _getcategory(category)
    module = re.escape(module)
    if module:
        module = module + '$'
    if lineno:
        try:
            lineno = int(lineno)
            if lineno < 0:
                raise ValueError
        except (ValueError, OverflowError):
            raise _OptionError('invalid lineno %r' % (lineno,))

    else:
        lineno = 0
    filterwarnings(action, message, category, module, lineno)


def _getaction(action):
    if not action:
        return 'default'
    if action == 'all':
        return 'always'
    for a in ('default', 'always', 'ignore', 'module', 'once', 'error'):
        if a.startswith(action):
            return a

    raise _OptionError('invalid action: %r' % (action,))


def _getcategory(category):
    import re
    if not category:
        return Warning
    else:
        if re.match('^[a-zA-Z0-9_]+$', category):
            try:
                cat = eval(category)
            except NameError:
                raise _OptionError('unknown warning category: %r' % (category,))

        else:
            i = category.rfind('.')
            module = category[:i]
            klass = category[i + 1:]
            try:
                m = __import__(module, None, None, [klass])
            except ImportError:
                raise _OptionError('invalid module name: %r' % (module,))

            try:
                cat = getattr(m, klass)
            except AttributeError:
                raise _OptionError('unknown warning category: %r' % (category,))

        if not issubclass(cat, Warning):
            raise _OptionError('invalid warning category: %r' % (category,))
        return cat


def warn(message, category=None, stacklevel=1):
    """Issue a warning, or maybe ignore it or raise an exception."""
    if isinstance(message, Warning):
        category = message.__class__
    if category is None:
        category = UserWarning
    assert issubclass(category, Warning)
    try:
        caller = sys._getframe(stacklevel)
    except ValueError:
        globals = sys.__dict__
        lineno = 1
    else:
        globals = caller.f_globals
        lineno = caller.f_lineno

    if '__name__' in globals:
        module = globals['__name__']
    else:
        module = '<string>'
    filename = globals.get('__file__')
    if filename:
        fnl = filename.lower()
        if fnl.endswith(('.pyc', '.pyo')):
            filename = filename[:-1]
    else:
        if module == '__main__':
            try:
                filename = sys.argv[0]
            except AttributeError:
                filename = '__main__'

        if not filename:
            filename = module
    registry = globals.setdefault('__warningregistry__', {})
    warn_explicit(message, category, filename, lineno, module, registry, globals)
    return


def warn_explicit(message, category, filename, lineno, module=None, registry=None, module_globals=None):
    lineno = int(lineno)
    if module is None:
        module = filename or '<unknown>'
        if module[-3:].lower() == '.py':
            module = module[:-3]
    if registry is None:
        registry = {}
    if isinstance(message, Warning):
        text = str(message)
        category = message.__class__
    else:
        text = message
        message = category(message)
    key = (
     text, category, lineno)
    if registry.get(key):
        return
    else:
        for item in filters:
            action, msg, cat, mod, ln = item
            if (msg is None or msg.match(text)) and issubclass(category, cat) and (mod is None or mod.match(module)) and (ln == 0 or lineno == ln):
                break
        else:
            action = defaultaction

        if action == 'ignore':
            registry[key] = 1
            return
        linecache.getlines(filename, module_globals)
        if action == 'error':
            raise message
        if action == 'once':
            registry[key] = 1
            oncekey = (text, category)
            if onceregistry.get(oncekey):
                return
            onceregistry[oncekey] = 1
        elif action == 'always':
            pass
        elif action == 'module':
            registry[key] = 1
            altkey = (text, category, 0)
            if registry.get(altkey):
                return
            registry[altkey] = 1
        elif action == 'default':
            registry[key] = 1
        else:
            raise RuntimeError('Unrecognized action (%r) in warnings.filters:\n %s' % (
             action, item))
        showwarning(message, category, filename, lineno)
        return


class WarningMessage(object):
    """Holds the result of a single showwarning() call."""
    _WARNING_DETAILS = ('message', 'category', 'filename', 'lineno', 'file', 'line')

    def __init__(self, message, category, filename, lineno, file=None, line=None):
        local_values = locals()
        for attr in self._WARNING_DETAILS:
            setattr(self, attr, local_values[attr])

        self._category_name = category.__name__ if category else None
        return

    def __str__(self):
        return '{message : %r, category : %r, filename : %r, lineno : %s, line : %r}' % (
         self.message, self._category_name,
         self.filename, self.lineno, self.line)


class catch_warnings(object):
    """A context manager that copies and restores the warnings filter upon
    exiting the context.

    The 'record' argument specifies whether warnings should be captured by a
    custom implementation of warnings.showwarning() and be appended to a list
    returned by the context manager. Otherwise None is returned by the context
    manager. The objects appended to the list are arguments whose attributes
    mirror the arguments to showwarning().

    The 'module' argument is to specify an alternative module to the module
    named 'warnings' and imported under that name. This argument is only useful
    when testing the warnings module itself.

    """

    def __init__(self, record=False, module=None):
        """Specify whether to record warnings and if an alternative module
        should be used other than sys.modules['warnings'].

        For compatibility with Python 3.0, please consider all arguments to be
        keyword-only.

        """
        self._record = record
        self._module = sys.modules['warnings'] if module is None else module
        self._entered = False
        return

    def __repr__(self):
        args = []
        if self._record:
            args.append('record=True')
        if self._module is not sys.modules['warnings']:
            args.append('module=%r' % self._module)
        name = type(self).__name__
        return '%s(%s)' % (name, (', ').join(args))

    def __enter__(self):
        if self._entered:
            raise RuntimeError('Cannot enter %r twice' % self)
        self._entered = True
        self._filters = self._module.filters
        self._module.filters = self._filters[:]
        self._showwarning = self._module.showwarning
        if self._record:
            log = []

            def showwarning(*args, **kwargs):
                log.append(WarningMessage(*args, **kwargs))

            self._module.showwarning = showwarning
            return log
        else:
            return
            return

    def __exit__(self, *exc_info):
        if not self._entered:
            raise RuntimeError('Cannot exit %r without entering first' % self)
        self._module.filters = self._filters
        self._module.showwarning = self._showwarning


_warnings_defaults = False
try:
    from _warnings import filters, default_action, once_registry, warn, warn_explicit
    defaultaction = default_action
    onceregistry = once_registry
    _warnings_defaults = True
except ImportError:
    filters = []
    defaultaction = 'default'
    onceregistry = {}

_processoptions(sys.warnoptions)
if not _warnings_defaults:
    silence = [
     ImportWarning, PendingDeprecationWarning]
    if not sys.py3kwarning and not sys.flags.division_warning:
        silence.append(DeprecationWarning)
    for cls in silence:
        simplefilter('ignore', category=cls)

    bytes_warning = sys.flags.bytes_warning
    if bytes_warning > 1:
        bytes_action = 'error'
    elif bytes_warning:
        bytes_action = 'default'
    else:
        bytes_action = 'ignore'
    simplefilter(bytes_action, category=BytesWarning, append=1)
del _warnings_defaults