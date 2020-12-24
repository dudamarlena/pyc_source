# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\empywiz\em.py
# Compiled at: 2006-10-06 10:24:39
"""
A system for processing Python as markup embedded in text.
"""
__program__ = 'empy'
__version__ = '3.3'
__url__ = 'http://www.alcyone.com/software/empy/'
__author__ = 'Erik Max Francis <max@alcyone.com>'
__copyright__ = 'Copyright (C) 2002-2003 Erik Max Francis'
__license__ = 'LGPL'
import copy, getopt, os, re, string, sys, types
try:
    import cStringIO
    StringIO = cStringIO
    del cStringIO
except ImportError:
    import StringIO

(False, True) = (
 0, 1)
FAILURE_CODE = 1
DEFAULT_PREFIX = '@'
DEFAULT_PSEUDOMODULE_NAME = 'empy'
DEFAULT_SCRIPT_NAME = '?'
SIGNIFICATOR_RE_SUFFIX = '%(\\S+)\\s*(.*)\\s*$'
SIGNIFICATOR_RE_STRING = DEFAULT_PREFIX + SIGNIFICATOR_RE_SUFFIX
BANGPATH = '#!'
DEFAULT_CHUNK_SIZE = 8192
DEFAULT_ERRORS = 'strict'
IDENTIFIER_FIRST_CHARS = '_abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
IDENTIFIER_CHARS = IDENTIFIER_FIRST_CHARS + '0123456789.'
ENDING_CHARS = {'(': ')', '[': ']', '{': '}'}
OPTIONS_ENV = 'EMPY_OPTIONS'
PREFIX_ENV = 'EMPY_PREFIX'
PSEUDO_ENV = 'EMPY_PSEUDO'
FLATTEN_ENV = 'EMPY_FLATTEN'
RAW_ENV = 'EMPY_RAW_ERRORS'
INTERACTIVE_ENV = 'EMPY_INTERACTIVE'
BUFFERED_ENV = 'EMPY_BUFFERED_OUTPUT'
NO_OVERRIDE_ENV = 'EMPY_NO_OVERRIDE'
UNICODE_ENV = 'EMPY_UNICODE'
INPUT_ENCODING_ENV = 'EMPY_UNICODE_INPUT_ENCODING'
OUTPUT_ENCODING_ENV = 'EMPY_UNICODE_OUTPUT_ENCODING'
INPUT_ERRORS_ENV = 'EMPY_UNICODE_INPUT_ERRORS'
OUTPUT_ERRORS_ENV = 'EMPY_UNICODE_OUTPUT_ERRORS'
BANGPATH_OPT = 'processBangpaths'
BUFFERED_OPT = 'bufferedOutput'
RAW_OPT = 'rawErrors'
EXIT_OPT = 'exitOnError'
FLATTEN_OPT = 'flatten'
OVERRIDE_OPT = 'override'
CALLBACK_OPT = 'noCallbackError'
OPTION_INFO = [
 (
  '-V --version', 'Print version and exit'),
 (
  '-h --help', 'Print usage and exit'),
 (
  '-H --extended-help', 'Print extended usage and exit'),
 (
  '-k --suppress-errors', 'Do not exit on errors; go interactive'),
 (
  '-p --prefix=<char>', 'Change prefix to something other than @'),
 (
  '   --no-prefix', 'Do not do any markup processing at all'),
 (
  '-m --module=<name>', 'Change the internal pseudomodule name'),
 (
  '-f --flatten', 'Flatten the members of pseudmodule to start'),
 (
  '-r --raw-errors', 'Show raw Python errors'),
 (
  '-i --interactive', 'Go into interactive mode after processing'),
 (
  '-n --no-override-stdout', 'Do not override sys.stdout with proxy'),
 (
  '-o --output=<filename>', 'Specify file for output as write'),
 (
  '-a --append=<filename>', 'Specify file for output as append'),
 (
  '-b --buffered-output', 'Fully buffer output including open'),
 (
  '   --binary', 'Treat the file as a binary'),
 (
  '   --chunk-size=<chunk>', 'Use this chunk size for reading binaries'),
 (
  '-P --preprocess=<filename>', 'Interpret EmPy file before main processing'),
 (
  '-I --import=<modules>', 'Import Python modules before processing'),
 (
  '-D --define=<definition>', 'Execute Python assignment statement'),
 (
  '-E --execute=<statement>', 'Execute Python statement before processing'),
 (
  '-F --execute-file=<filename>', 'Execute Python file before processing'),
 (
  '   --pause-at-end', 'Prompt at the ending of processing'),
 (
  '   --relative-path', 'Add path of EmPy script to sys.path'),
 (
  '   --no-callback-error', 'Custom markup without callback is error'),
 (
  '   --no-bangpath-processing', 'Suppress bangpaths as comments'),
 (
  '-u --unicode', 'Enable Unicode subsystem (Python 2+ only)'),
 (
  '   --unicode-encoding=<e>', 'Set both input and output encodings'),
 (
  '   --unicode-input-encoding=<e>', 'Set input encoding'),
 (
  '   --unicode-output-encoding=<e>', 'Set output encoding'),
 (
  '   --unicode-errors=<E>', 'Set both input and output error handler'),
 (
  '   --unicode-input-errors=<E>', 'Set input error handler'),
 (
  '   --unicode-output-errors=<E>', 'Set output error handler')]
USAGE_NOTES = "Notes: Whitespace immediately inside parentheses of @(...) are\nignored.  Whitespace immediately inside braces of @{...} are ignored,\nunless ... spans multiple lines.  Use @{ ... }@ to suppress newline\nfollowing expansion.  Simple expressions ignore trailing dots; `@x.'\nmeans `@(x).'.  A #! at the start of a file is treated as a @#\ncomment."
MARKUP_INFO = [
 (
  '@# ... NL', 'Comment; remove everything up to newline'),
 (
  '@? NAME NL', 'Set the current context name'),
 (
  '@! INTEGER NL', 'Set the current context line number'),
 (
  '@ WHITESPACE', 'Remove following whitespace; line continuation'),
 (
  '@\\ ESCAPE_CODE', 'A C-style escape sequence'),
 (
  '@@', 'Literal @; @ is escaped (duplicated prefix)'),
 (
  '@), @], @}', 'Literal close parenthesis, bracket, brace'),
 (
  '@ STRING_LITERAL', 'Replace with string literal contents'),
 (
  '@( EXPRESSION )', 'Evaluate expression and substitute with str'),
 (
  '@( TEST [? THEN [! ELSE]] )', 'If test is true, evaluate then, otherwise else'),
 (
  '@( TRY $ CATCH )', 'Expand try expression, or catch if it raises'),
 (
  '@ SIMPLE_EXPRESSION', 'Evaluate simple expression and substitute;\ne.g., @x, @x.y, @f(a, b), @l[i], etc.'),
 (
  '@` EXPRESSION `', 'Evaluate expression and substitute with repr'),
 (
  '@: EXPRESSION : [DUMMY] :', 'Evaluates to @:...:expansion:'),
 (
  '@{ STATEMENTS }', 'Statements are executed for side effects'),
 (
  '@[ CONTROL ]', 'Control markups: if E; elif E; for N in E;\nwhile E; try; except E, N; finally; continue;\nbreak; end X'),
 (
  '@%% KEY WHITESPACE VALUE NL', 'Significator form of __KEY__ = VALUE'),
 (
  '@< CONTENTS >', 'Custom markup; meaning provided by user')]
ESCAPE_INFO = [
 (
  '@\\0', 'NUL, null'),
 (
  '@\\a', 'BEL, bell'),
 (
  '@\\b', 'BS, backspace'),
 (
  '@\\dDDD', 'three-digit decimal code DDD'),
 (
  '@\\e', 'ESC, escape'),
 (
  '@\\f', 'FF, form feed'),
 (
  '@\\h', 'DEL, delete'),
 (
  '@\\n', 'LF, linefeed, newline'),
 (
  '@\\N{NAME}', 'Unicode character named NAME'),
 (
  '@\\oOOO', 'three-digit octal code OOO'),
 (
  '@\\qQQQQ', 'four-digit quaternary code QQQQ'),
 (
  '@\\r', 'CR, carriage return'),
 (
  '@\\s', 'SP, space'),
 (
  '@\\t', 'HT, horizontal tab'),
 (
  '@\\uHHHH', '16-bit hexadecimal Unicode HHHH'),
 (
  '@\\UHHHHHHHH', '32-bit hexadecimal Unicode HHHHHHHH'),
 (
  '@\\v', 'VT, vertical tab'),
 (
  '@\\xHH', 'two-digit hexadecimal code HH'),
 (
  '@\\z', 'EOT, end of transmission')]
PSEUDOMODULE_INFO = [
 (
  'VERSION', 'String representing EmPy version'),
 (
  'SIGNIFICATOR_RE_STRING', 'Regular expression matching significators'),
 (
  'SIGNIFICATOR_RE_SUFFIX', 'The above stub, lacking the prefix'),
 (
  'interpreter', 'Currently-executing interpreter instance'),
 (
  'argv', 'The EmPy script name and command line arguments'),
 (
  'args', 'The command line arguments only'),
 (
  'identify()', 'Identify top context as name, line'),
 (
  'setContextName(name)', 'Set the name of the current context'),
 (
  'setContextLine(line)', 'Set the line number of the current context'),
 (
  'atExit(callable)', 'Invoke no-argument function at shutdown'),
 (
  'getGlobals()', "Retrieve this interpreter's globals"),
 (
  'setGlobals(dict)', "Set this interpreter's globals"),
 (
  'updateGlobals(dict)', "Merge dictionary into interpreter's globals"),
 (
  'clearGlobals()', 'Start globals over anew'),
 (
  'saveGlobals([deep])', 'Save a copy of the globals'),
 (
  'restoreGlobals([pop])', 'Restore the most recently saved globals'),
 (
  'defined(name, [loc])', 'Find if the name is defined'),
 (
  'evaluate(expression, [loc])', 'Evaluate the expression'),
 (
  'serialize(expression, [loc])', 'Evaluate and serialize the expression'),
 (
  'execute(statements, [loc])', 'Execute the statements'),
 (
  'single(source, [loc])', "Execute the 'single' object"),
 (
  'atomic(name, value, [loc])', 'Perform an atomic assignment'),
 (
  'assign(name, value, [loc])', 'Perform an arbitrary assignment'),
 (
  'significate(key, [value])', 'Significate the given key, value pair'),
 (
  'include(file, [loc])', 'Include filename or file-like object'),
 (
  'expand(string, [loc])', 'Explicitly expand string and return'),
 (
  'string(data, [name], [loc])', 'Process string-like object'),
 (
  'quote(string)', 'Quote prefixes in provided string and return'),
 (
  'flatten([keys])', 'Flatten module contents into globals namespace'),
 (
  'getPrefix()', 'Get current prefix'),
 (
  'setPrefix(char)', 'Set new prefix'),
 (
  'stopDiverting()', 'Stop diverting; data sent directly to output'),
 (
  'createDiversion(name)', 'Create a diversion but do not divert to it'),
 (
  'retrieveDiversion(name)', 'Retrieve the actual named diversion object'),
 (
  'startDiversion(name)', 'Start diverting to given diversion'),
 (
  'playDiversion(name)', 'Recall diversion and then eliminate it'),
 (
  'replayDiversion(name)', 'Recall diversion but retain it'),
 (
  'purgeDiversion(name)', 'Erase diversion'),
 (
  'playAllDiversions()', 'Stop diverting and play all diversions in order'),
 (
  'replayAllDiversions()', 'Stop diverting and replay all diversions'),
 (
  'purgeAllDiversions()', 'Stop diverting and purge all diversions'),
 (
  'getFilter()', 'Get current filter'),
 (
  'resetFilter()', 'Reset filter; no filtering'),
 (
  'nullFilter()', 'Install null filter'),
 (
  'setFilter(shortcut)', 'Install new filter or filter chain'),
 (
  'attachFilter(shortcut)', 'Attach single filter to end of current chain'),
 (
  'areHooksEnabled()', 'Return whether or not hooks are enabled'),
 (
  'enableHooks()', 'Enable hooks (default)'),
 (
  'disableHooks()', 'Disable hook invocation'),
 (
  'getHooks()', 'Get all the hooks'),
 (
  'clearHooks()', 'Clear all hooks'),
 (
  'addHook(hook, [i])', 'Register the hook (optionally insert)'),
 (
  'removeHook(hook)', 'Remove an already-registered hook from name'),
 (
  'invokeHook(name_, ...)', 'Manually invoke hook'),
 (
  'getCallback()', 'Get interpreter callback'),
 (
  'registerCallback(callback)', 'Register callback with interpreter'),
 (
  'deregisterCallback()', 'Deregister callback from interpreter'),
 (
  'invokeCallback(contents)', 'Invoke the callback directly'),
 (
  'Interpreter', 'The interpreter class')]
ENVIRONMENT_INFO = [
 (
  OPTIONS_ENV, 'Specified options will be included'),
 (
  PREFIX_ENV, 'Specify the default prefix: -p <value>'),
 (
  PSEUDO_ENV, 'Specify name of pseudomodule: -m <value>'),
 (
  FLATTEN_ENV, 'Flatten empy pseudomodule if defined: -f'),
 (
  RAW_ENV, 'Show raw errors if defined: -r'),
 (
  INTERACTIVE_ENV, 'Enter interactive mode if defined: -i'),
 (
  BUFFERED_ENV, 'Fully buffered output if defined: -b'),
 (
  NO_OVERRIDE_ENV, 'Do not override sys.stdout if defined: -n'),
 (
  UNICODE_ENV, 'Enable Unicode subsystem: -n'),
 (
  INPUT_ENCODING_ENV, 'Unicode input encoding'),
 (
  OUTPUT_ENCODING_ENV, 'Unicode output encoding'),
 (
  INPUT_ERRORS_ENV, 'Unicode input error handler'),
 (
  OUTPUT_ERRORS_ENV, 'Unicode output error handler')]

class Error(Exception):
    """The base class for all EmPy errors."""
    pass


EmpyError = EmPyError = Error

class DiversionError(Error):
    """An error related to diversions."""
    pass


class FilterError(Error):
    """An error related to filters."""
    pass


class StackUnderflowError(Error):
    """A stack underflow."""
    pass


class SubsystemError(Error):
    """An error associated with the Unicode subsystem."""
    pass


class FlowError(Error):
    """An exception related to control flow."""
    pass


class ContinueFlow(FlowError):
    """A continue control flow."""
    pass


class BreakFlow(FlowError):
    """A break control flow."""
    pass


class ParseError(Error):
    """A parse error occurred."""
    pass


class TransientParseError(ParseError):
    """A parse error occurred which may be resolved by feeding more data.
    Such an error reaching the toplevel is an unexpected EOF error."""
    pass


class MetaError(Exception):
    """A wrapper around a real Python exception for including a copy of
    the context."""

    def __init__(self, contexts, exc):
        Exception.__init__(self, exc)
        self.contexts = contexts
        self.exc = exc

    def __str__(self):
        backtrace = map(lambda x: str(x), self.contexts)
        return '%s: %s (%s)' % (self.exc.__class__, self.exc,
         string.join(backtrace, ', '))


class Subsystem():
    """The subsystem class defers file creation so that it can create
    Unicode-wrapped files if desired (and possible)."""

    def __init__(self):
        self.useUnicode = False
        self.inputEncoding = None
        self.outputEncoding = None
        self.errors = None
        return

    def initialize(self, inputEncoding=None, outputEncoding=None, inputErrors=None, outputErrors=None):
        self.useUnicode = True
        try:
            unicode
            import codecs
        except (NameError, ImportError):
            raise SubsystemError, 'Unicode subsystem unavailable'

        defaultEncoding = sys.getdefaultencoding()
        if inputEncoding is None:
            inputEncoding = defaultEncoding
        self.inputEncoding = inputEncoding
        if outputEncoding is None:
            outputEncoding = defaultEncoding
        self.outputEncoding = outputEncoding
        if inputErrors is None:
            inputErrors = DEFAULT_ERRORS
        self.inputErrors = inputErrors
        if outputErrors is None:
            outputErrors = DEFAULT_ERRORS
        self.outputErrors = outputErrors
        return

    def assertUnicode(self):
        if not self.useUnicode:
            raise SubsystemError, 'Unicode subsystem unavailable'

    def open(self, name, mode=None):
        if self.useUnicode:
            return self.unicodeOpen(name, mode)
        else:
            return self.defaultOpen(name, mode)

    def defaultOpen(self, name, mode=None):
        if mode is None:
            mode = 'r'
        return open(name, mode)

    def unicodeOpen(self, name, mode=None):
        import codecs
        if mode is None:
            mode = 'rb'
        if mode.find('w') >= 0 or mode.find('a') >= 0:
            encoding = self.outputEncoding
            errors = self.outputErrors
        else:
            encoding = self.inputEncoding
            errors = self.inputErrors
        return codecs.open(name, mode, encoding, errors)


theSubsystem = Subsystem()

class Stack():
    """A simple stack that behaves as a sequence (with 0 being the top
    of the stack, not the bottom)."""

    def __init__(self, seq=None):
        if seq is None:
            seq = []
        self.data = seq
        return

    def top(self):
        """Access the top element on the stack."""
        try:
            return self.data[(-1)]
        except IndexError:
            raise StackUnderflowError, 'stack is empty for top'

    def pop(self):
        """Pop the top element off the stack and return it."""
        try:
            return self.data.pop()
        except IndexError:
            raise StackUnderflowError, 'stack is empty for pop'

    def push(self, object):
        """Push an element onto the top of the stack."""
        self.data.append(object)

    def filter(self, function):
        """Filter the elements of the stack through the function."""
        self.data = filter(function, self.data)

    def purge(self):
        """Purge the stack."""
        self.data = []

    def clone(self):
        """Create a duplicate of this stack."""
        return self.__class__(self.data[:])

    def __nonzero__(self):
        return len(self.data) != 0

    def __len__(self):
        return len(self.data)

    def __getitem__(self, index):
        return self.data[(-(index + 1))]

    def __repr__(self):
        return '<%s instance at 0x%x [%s]>' % (
         self.__class__, id(self),
         string.join(map(repr, self.data), ', '))


class AbstractFile():
    """An abstracted file that, when buffered, will totally buffer the
    file, including even the file open."""

    def __init__(self, filename, mode='w', buffered=False):
        self.done = True
        self.filename = filename
        self.mode = mode
        self.buffered = buffered
        if buffered:
            self.bufferFile = StringIO.StringIO()
        else:
            self.bufferFile = theSubsystem.open(filename, mode)
        self.done = False

    def __del__(self):
        self.close()

    def write(self, data):
        self.bufferFile.write(data)

    def writelines(self, data):
        self.bufferFile.writelines(data)

    def flush(self):
        self.bufferFile.flush()

    def close(self):
        if not self.done:
            self.commit()
            self.done = True

    def commit(self):
        if self.buffered:
            file = theSubsystem.open(self.filename, self.mode)
            file.write(self.bufferFile.getvalue())
            file.close()
        else:
            self.bufferFile.close()

    def abort(self):
        if self.buffered:
            self.bufferFile = None
        else:
            self.bufferFile.close()
            self.bufferFile = None
        self.done = True
        return


class Diversion():
    """The representation of an active diversion.  Diversions act as
    (writable) file objects, and then can be recalled either as pure
    strings or (readable) file objects."""

    def __init__(self):
        self.file = StringIO.StringIO()

    def write(self, data):
        self.file.write(data)

    def writelines(self, lines):
        for line in lines:
            self.write(line)

    def flush(self):
        self.file.flush()

    def close(self):
        self.file.close()

    def asString(self):
        """Return the diversion as a string."""
        return self.file.getvalue()

    def asFile(self):
        """Return the diversion as a file."""
        return StringIO.StringIO(self.file.getvalue())


class Stream():
    """A wrapper around an (output) file object which supports
    diversions and filtering."""

    def __init__(self, file):
        self.file = file
        self.currentDiversion = None
        self.diversions = {}
        self.filter = file
        self.done = False
        return

    def write(self, data):
        if self.currentDiversion is None:
            self.filter.write(data)
        else:
            self.diversions[self.currentDiversion].write(data)
        return

    def writelines(self, lines):
        for line in lines:
            self.write(line)

    def flush(self):
        self.filter.flush()

    def close(self):
        if not self.done:
            self.undivertAll(True)
            self.filter.close()
            self.done = True

    def shortcut(self, shortcut):
        """Take a filter shortcut and translate it into a filter, returning
        it.  Sequences don't count here; these should be detected
        independently."""
        if shortcut == 0:
            return NullFilter()
        elif type(shortcut) is types.FunctionType or type(shortcut) is types.BuiltinFunctionType or type(shortcut) is types.BuiltinMethodType or type(shortcut) is types.LambdaType:
            return FunctionFilter(shortcut)
        elif type(shortcut) is types.StringType:
            return StringFilter(filter)
        elif type(shortcut) is types.DictType:
            raise NotImplementedError, 'mapping filters not yet supported'
        else:
            return shortcut

    def last(self):
        """Find the last filter in the current filter chain, or None if
        there are no filters installed."""
        if self.filter is None:
            return None
        thisFilter, lastFilter = self.filter, None
        while thisFilter is not None and thisFilter is not self.file:
            lastFilter = thisFilter
            thisFilter = thisFilter.next()

        return lastFilter

    def install(self, shortcut=None):
        """Install a new filter; None means no filter.  Handle all the
        special shortcuts for filters here."""
        self.filter.flush()
        if shortcut is None or shortcut == [] or shortcut == ():
            self.filter = self.file
        else:
            if type(shortcut) in (types.ListType, types.TupleType):
                shortcuts = list(shortcut)
            else:
                shortcuts = [
                 shortcut]
            filters = []
            for shortcut in shortcuts:
                filters.append(self.shortcut(shortcut))

            if len(filters) > 1:
                lastFilter = None
                for filter in filters:
                    if lastFilter is not None:
                        lastFilter.attach(filter)
                    lastFilter = filter

                lastFilter.attach(self.file)
                self.filter = filters[0]
            else:
                filter = filters[0]
                lastFilter = filter.last()
                lastFilter.attach(self.file)
                self.filter = filter
        return

    def attach(self, shortcut):
        """Attached a solitary filter (no sequences allowed here) at the
        end of the current filter chain."""
        lastFilter = self.last()
        if lastFilter is None:
            self.install(shortcut)
        else:
            filter = self.shortcut(shortcut)
            lastFilter.attach(filter)
            filter.attach(self.file)
        return

    def revert(self):
        """Reset any current diversions."""
        self.currentDiversion = None
        return

    def create(self, name):
        """Create a diversion if one does not already exist, but do not
        divert to it yet."""
        if name is None:
            raise DiversionError, 'diversion name must be non-None'
        if not self.diversions.has_key(name):
            self.diversions[name] = Diversion()
        return

    def retrieve(self, name):
        """Retrieve the given diversion."""
        if name is None:
            raise DiversionError, 'diversion name must be non-None'
        if self.diversions.has_key(name):
            return self.diversions[name]
        else:
            raise DiversionError, 'nonexistent diversion: %s' % name
        return

    def divert(self, name):
        """Start diverting."""
        if name is None:
            raise DiversionError, 'diversion name must be non-None'
        self.create(name)
        self.currentDiversion = name
        return

    def undivert(self, name, purgeAfterwards=False):
        """Undivert a particular diversion."""
        if name is None:
            raise DiversionError, 'diversion name must be non-None'
        if self.diversions.has_key(name):
            diversion = self.diversions[name]
            self.filter.write(diversion.asString())
            if purgeAfterwards:
                self.purge(name)
        else:
            raise DiversionError, 'nonexistent diversion: %s' % name
        return

    def purge(self, name):
        """Purge the specified diversion."""
        if name is None:
            raise DiversionError, 'diversion name must be non-None'
        if self.diversions.has_key(name):
            del self.diversions[name]
            if self.currentDiversion == name:
                self.currentDiversion = None
        return

    def undivertAll(self, purgeAfterwards=True):
        """Undivert all pending diversions."""
        if self.diversions:
            self.revert()
            names = self.diversions.keys()
            names.sort()
            for name in names:
                self.undivert(name)
                if purgeAfterwards:
                    self.purge(name)

    def purgeAll(self):
        """Eliminate all existing diversions."""
        if self.diversions:
            self.diversions = {}
        self.currentDiversion = None
        return


class NullFile():
    """A simple class that supports all the file-like object methods
    but simply does nothing at all."""

    def __init__(self):
        pass

    def write(self, data):
        pass

    def writelines(self, lines):
        pass

    def flush(self):
        pass

    def close(self):
        pass


class UncloseableFile():
    """A simple class which wraps around a delegate file-like object
    and lets everything through except close calls."""

    def __init__(self, delegate):
        self.delegate = delegate

    def write(self, data):
        self.delegate.write(data)

    def writelines(self, lines):
        self.delegate.writelines(data)

    def flush(self):
        self.delegate.flush()

    def close(self):
        """Eat this one."""
        pass


class ProxyFile():
    """The proxy file object that is intended to take the place of
    sys.stdout.  The proxy can manage a stack of file objects it is
    writing to, and an underlying raw file object."""

    def __init__(self, bottom):
        self.stack = Stack()
        self.bottom = bottom

    def current(self):
        """Get the current stream to write to."""
        if self.stack:
            return self.stack[(-1)][1]
        else:
            return self.bottom

    def push(self, interpreter):
        self.stack.push((interpreter, interpreter.stream()))

    def pop(self, interpreter):
        result = self.stack.pop()
        assert interpreter is result[0]

    def clear(self, interpreter):
        self.stack.filter(lambda x, i=interpreter: x[0] is not i)

    def write(self, data):
        self.current().write(data)

    def writelines(self, lines):
        self.current().writelines(lines)

    def flush(self):
        self.current().flush()

    def close(self):
        """Close the current file.  If the current file is the bottom, then
        close it and dispose of it."""
        current = self.current()
        if current is self.bottom:
            self.bottom = None
        current.close()
        return

    def _testProxy(self):
        pass


class Filter():
    """An abstract filter."""

    def __init__(self):
        if self.__class__ is Filter:
            raise NotImplementedError
        self.sink = None
        return

    def next(self):
        """Return the next filter/file-like object in the sequence, or None."""
        return self.sink

    def write(self, data):
        """The standard write method; this must be overridden in subclasses."""
        raise NotImplementedError

    def writelines(self, lines):
        """Standard writelines wrapper."""
        for line in lines:
            self.write(line)

    def _flush(self):
        """The _flush method should always flush the sink and should not
        be overridden."""
        self.sink.flush()

    def flush(self):
        """The flush method can be overridden."""
        self._flush()

    def close(self):
        """Close the filter.  Do an explicit flush first, then close the
        sink."""
        self.flush()
        self.sink.close()

    def attach(self, filter):
        """Attach a filter to this one."""
        if self.sink is not None:
            self.detach()
        self.sink = filter
        return

    def detach(self):
        """Detach a filter from its sink."""
        self.flush()
        self._flush()
        self.sink = None
        return

    def last(self):
        """Find the last filter in this chain."""
        this, last = self, self
        while this is not None:
            last = this
            this = this.next()

        return last


class NullFilter(Filter):
    """A filter that never sends any output to its sink."""

    def write(self, data):
        pass


class FunctionFilter(Filter):
    """A filter that works simply by pumping its input through a
    function which maps strings into strings."""

    def __init__(self, function):
        Filter.__init__(self)
        self.function = function

    def write(self, data):
        self.sink.write(self.function(data))


class StringFilter(Filter):
    """A filter that takes a translation string (256 characters) and
    filters any incoming data through it."""

    def __init__(self, table):
        if not (type(table) == types.StringType and len(table) == 256):
            raise FilterError, 'table must be 256-character string'
        Filter.__init__(self)
        self.table = table

    def write(self, data):
        self.sink.write(string.translate(data, self.table))


class BufferedFilter(Filter):
    """A buffered filter is one that doesn't modify the source data
    sent to the sink, but instead holds it for a time.  The standard
    variety only sends the data along when it receives a flush
    command."""

    def __init__(self):
        Filter.__init__(self)
        self.buffer = ''

    def write(self, data):
        self.buffer = self.buffer + data

    def flush(self):
        if self.buffer:
            self.sink.write(self.buffer)
        self._flush()


class SizeBufferedFilter(BufferedFilter):
    """A size-buffered filter only in fixed size chunks (excepting the
    final chunk)."""

    def __init__(self, bufferSize):
        BufferedFilter.__init__(self)
        self.bufferSize = bufferSize

    def write(self, data):
        BufferedFilter.write(self, data)
        while len(self.buffer) > self.bufferSize:
            chunk, self.buffer = self.buffer[:self.bufferSize], self.buffer[self.bufferSize:]
            self.sink.write(chunk)


class LineBufferedFilter(BufferedFilter):
    """A line-buffered filter only lets data through when it sees
    whole lines."""

    def __init__(self):
        BufferedFilter.__init__(self)

    def write(self, data):
        BufferedFilter.write(self, data)
        chunks = string.split(self.buffer, '\n')
        for chunk in chunks[:-1]:
            self.sink.write(chunk + '\n')

        self.buffer = chunks[(-1)]


class MaximallyBufferedFilter(BufferedFilter):
    """A maximally-buffered filter only lets its data through on the final
    close.  It ignores flushes."""

    def __init__(self):
        BufferedFilter.__init__(self)

    def flush(self):
        pass

    def close(self):
        if self.buffer:
            BufferedFilter.flush(self)
            self.sink.close()


class Context():
    """An interpreter context, which encapsulates a name, an input
    file object, and a parser object."""
    DEFAULT_UNIT = 'lines'

    def __init__(self, name, line=0, units=DEFAULT_UNIT):
        self.name = name
        self.line = line
        self.units = units
        self.pause = False

    def bump(self, quantity=1):
        if self.pause:
            self.pause = False
        else:
            self.line = self.line + quantity

    def identify(self):
        return (self.name, self.line)

    def __str__(self):
        if self.units == self.DEFAULT_UNIT:
            return '%s:%s' % (self.name, self.line)
        else:
            return '%s:%s[%s]' % (self.name, self.line, self.units)


class Hook():
    """The base class for implementing hooks."""

    def __init__(self):
        self.interpreter = None
        return

    def register(self, interpreter):
        self.interpreter = interpreter

    def deregister(self, interpreter):
        if interpreter is not self.interpreter:
            raise Error, 'hook not associated with this interpreter'
        self.interpreter = None
        return

    def push(self):
        self.interpreter.push()

    def pop(self):
        self.interpreter.pop()

    def null(self):
        pass

    def atStartup(self):
        pass

    def atReady(self):
        pass

    def atFinalize(self):
        pass

    def atShutdown(self):
        pass

    def atParse(self, scanner, locals):
        pass

    def atToken(self, token):
        pass

    def atHandle(self, meta):
        pass

    def atInteract(self):
        pass

    def beforeInclude(self, name, file, locals):
        pass

    def afterInclude(self):
        pass

    def beforeExpand(self, string, locals):
        pass

    def afterExpand(self, result):
        pass

    def beforeFile(self, name, file, locals):
        pass

    def afterFile(self):
        pass

    def beforeBinary(self, name, file, chunkSize, locals):
        pass

    def afterBinary(self):
        pass

    def beforeString(self, name, string, locals):
        pass

    def afterString(self):
        pass

    def beforeQuote(self, string):
        pass

    def afterQuote(self, result):
        pass

    def beforeEscape(self, string, more):
        pass

    def afterEscape(self, result):
        pass

    def beforeControl(self, type, rest, locals):
        pass

    def afterControl(self):
        pass

    def beforeSignificate(self, key, value, locals):
        pass

    def afterSignificate(self):
        pass

    def beforeAtomic(self, name, value, locals):
        pass

    def afterAtomic(self):
        pass

    def beforeMulti(self, name, values, locals):
        pass

    def afterMulti(self):
        pass

    def beforeImport(self, name, locals):
        pass

    def afterImport(self):
        pass

    def beforeClause(self, catch, locals):
        pass

    def afterClause(self, exception, variable):
        pass

    def beforeSerialize(self, expression, locals):
        pass

    def afterSerialize(self):
        pass

    def beforeDefined(self, name, locals):
        pass

    def afterDefined(self, result):
        pass

    def beforeLiteral(self, text):
        pass

    def afterLiteral(self):
        pass

    def beforeEvaluate(self, expression, locals):
        pass

    def afterEvaluate(self, result):
        pass

    def beforeExecute(self, statements, locals):
        pass

    def afterExecute(self):
        pass

    def beforeSingle(self, source, locals):
        pass

    def afterSingle(self):
        pass


class VerboseHook(Hook):
    """A verbose hook that reports all information received by the
    hook interface.  This class dynamically scans the Hook base class
    to ensure that all hook methods are properly represented."""
    EXEMPT_ATTRIBUTES = [
     'register', 'deregister', 'push', 'pop']

    def __init__(self, output=sys.stderr):
        Hook.__init__(self)
        self.output = output
        self.indent = 0

        class FakeMethod:
            """This is a proxy method-like object."""

            def __init__(self, hook, name):
                self.hook = hook
                self.name = name

            def __call__(self, **keywords):
                self.hook.output.write('%s%s: %s\n' % (
                 ' ' * self.hook.indent,
                 self.name, repr(keywords)))

        for attribute in dir(Hook):
            if attribute[:1] != '_' and attribute not in self.EXEMPT_ATTRIBUTES:
                self.__dict__[attribute] = FakeMethod(self, attribute)


class Token():
    """An element of expansion."""

    def run(self, interpreter, locals):
        raise NotImplementedError

    def string(self):
        raise NotImplementedError

    def __str__(self):
        return self.string()


class NullToken(Token):
    """A chunk of data not containing markups."""

    def __init__(self, data):
        self.data = data

    def run(self, interpreter, locals):
        interpreter.write(self.data)

    def string(self):
        return self.data


class ExpansionToken(Token):
    """A token that involves an expansion."""

    def __init__(self, prefix, first):
        self.prefix = prefix
        self.first = first

    def scan(self, scanner):
        pass

    def run(self, interpreter, locals):
        pass


class WhitespaceToken(ExpansionToken):
    """A whitespace markup."""

    def string(self):
        return '%s%s' % (self.prefix, self.first)


class LiteralToken(ExpansionToken):
    """A literal markup."""

    def run(self, interpreter, locals):
        interpreter.write(self.first)

    def string(self):
        return '%s%s' % (self.prefix, self.first)


class PrefixToken(ExpansionToken):
    """A prefix markup."""

    def run(self, interpreter, locals):
        interpreter.write(interpreter.prefix)

    def string(self):
        return self.prefix * 2


class CommentToken(ExpansionToken):
    """A comment markup."""

    def scan(self, scanner):
        loc = scanner.find('\n')
        if loc >= 0:
            self.comment = scanner.chop(loc, 1)
        else:
            raise TransientParseError, 'comment expects newline'

    def string(self):
        return '%s#%s\n' % (self.prefix, self.comment)


class ContextNameToken(ExpansionToken):
    """A context name change markup."""

    def scan(self, scanner):
        loc = scanner.find('\n')
        if loc >= 0:
            self.name = string.strip(scanner.chop(loc, 1))
        else:
            raise TransientParseError, 'context name expects newline'

    def run(self, interpreter, locals):
        context = interpreter.context()
        context.name = self.name


class ContextLineToken(ExpansionToken):
    """A context line change markup."""

    def scan(self, scanner):
        loc = scanner.find('\n')
        if loc >= 0:
            try:
                self.line = int(scanner.chop(loc, 1))
            except ValueError:
                raise ParseError, 'context line requires integer'

        else:
            raise TransientParseError, 'context line expects newline'

    def run(self, interpreter, locals):
        context = interpreter.context()
        context.line = self.line
        context.pause = True


class EscapeToken(ExpansionToken):
    """An escape markup."""

    def scan(self, scanner):
        try:
            code = scanner.chop(1)
            result = None
            if code in '()[]{}\'"\\':
                result = code
            elif code == '0':
                result = '\x00'
            elif code == 'a':
                result = '\x07'
            elif code == 'b':
                result = '\x08'
            elif code == 'd':
                decimalCode = scanner.chop(3)
                result = chr(string.atoi(decimalCode, 10))
            elif code == 'e':
                result = '\x1b'
            elif code == 'f':
                result = '\x0c'
            elif code == 'h':
                result = '\x7f'
            elif code == 'n':
                result = '\n'
            elif code == 'N':
                theSubsystem.assertUnicode()
                import unicodedata
                if scanner.chop(1) != '{':
                    raise ParseError, 'Unicode name escape should be \\N{...}'
                i = scanner.find('}')
                name = scanner.chop(i, 1)
                try:
                    result = unicodedata.lookup(name)
                except KeyError:
                    raise SubsystemError, 'unknown Unicode character name: %s' % name

            elif code == 'o':
                octalCode = scanner.chop(3)
                result = chr(string.atoi(octalCode, 8))
            elif code == 'q':
                quaternaryCode = scanner.chop(4)
                result = chr(string.atoi(quaternaryCode, 4))
            elif code == 'r':
                result = '\r'
            elif code in 's ':
                result = ' '
            elif code == 't':
                result = '\t'
            elif code in 'u':
                theSubsystem.assertUnicode()
                hexCode = scanner.chop(4)
                result = unichr(string.atoi(hexCode, 16))
            elif code in 'U':
                theSubsystem.assertUnicode()
                hexCode = scanner.chop(8)
                result = unichr(string.atoi(hexCode, 16))
            elif code == 'v':
                result = '\x0b'
            elif code == 'x':
                hexCode = scanner.chop(2)
                result = chr(string.atoi(hexCode, 16))
            elif code == 'z':
                result = '\x04'
            elif code == '^':
                controlCode = string.upper(scanner.chop(1))
                if controlCode >= '@' and controlCode <= '`':
                    result = chr(ord(controlCode) - ord('@'))
                elif controlCode == '?':
                    result = '\x7f'
                else:
                    raise ParseError, 'invalid escape control code'
            else:
                raise ParseError, 'unrecognized escape code'
            assert result is not None
            self.code = result
        except ValueError:
            raise ParseError, 'invalid numeric escape code'

        return

    def run(self, interpreter, locals):
        interpreter.write(self.code)

    def string(self):
        return '%s\\x%02x' % (self.prefix, ord(self.code))


class SignificatorToken(ExpansionToken):
    """A significator markup."""

    def scan(self, scanner):
        loc = scanner.find('\n')
        if loc >= 0:
            line = scanner.chop(loc, 1)
            if not line:
                raise ParseError, 'significator must have nonblank key'
            if line[0] in ' \t\x0b\n':
                raise ParseError, 'no whitespace between % and key'
            fields = string.split(string.strip(line), None, 1)
            if len(fields) == 2 and fields[1] == '':
                fields.pop()
            self.key = fields[0]
            if len(fields) < 2:
                fields.append(None)
            (self.key, self.valueCode) = fields
        else:
            raise TransientParseError, 'significator expects newline'
        return

    def run(self, interpreter, locals):
        value = self.valueCode
        if value is not None:
            value = interpreter.evaluate(string.strip(value), locals)
        interpreter.significate(self.key, value)
        return

    def string(self):
        if self.valueCode is None:
            return '%s%%%s\n' % (self.prefix, self.key)
        else:
            return '%s%%%s %s\n' % (self.prefix, self.key, self.valueCode)
        return


class ExpressionToken(ExpansionToken):
    """An expression markup."""

    def scan(self, scanner):
        z = scanner.complex('(', ')', 0)
        try:
            q = scanner.next('$', 0, z, True)
        except ParseError:
            q = z

        try:
            i = scanner.next('?', 0, q, True)
            try:
                j = scanner.next('!', i, q, True)
            except ParseError:
                try:
                    j = scanner.next(':', i, q, True)
                except ParseError:
                    j = q

        except ParseError:
            i = j = q

        code = scanner.chop(z, 1)
        self.testCode = code[:i]
        self.thenCode = code[i + 1:j]
        self.elseCode = code[j + 1:q]
        self.exceptCode = code[q + 1:z]

    def run(self, interpreter, locals):
        try:
            result = interpreter.evaluate(self.testCode, locals)
            if self.thenCode:
                if result:
                    result = interpreter.evaluate(self.thenCode, locals)
                elif self.elseCode:
                    result = interpreter.evaluate(self.elseCode, locals)
                else:
                    result = None
        except SyntaxError:
            raise
        except:
            if self.exceptCode:
                result = interpreter.evaluate(self.exceptCode, locals)
            else:
                raise

        if result is not None:
            interpreter.write(str(result))
        return

    def string(self):
        result = self.testCode
        if self.thenCode:
            result = result + '?' + self.thenCode
        if self.elseCode:
            result = result + '!' + self.elseCode
        if self.exceptCode:
            result = result + '$' + self.exceptCode
        return '%s(%s)' % (self.prefix, result)


class StringLiteralToken(ExpansionToken):
    """A string token markup."""

    def scan(self, scanner):
        scanner.retreat()
        assert scanner[0] == self.first
        i = scanner.quote()
        self.literal = scanner.chop(i)

    def run(self, interpreter, locals):
        interpreter.literal(self.literal)

    def string(self):
        return '%s%s' % (self.prefix, self.literal)


class SimpleExpressionToken(ExpansionToken):
    """A simple expression markup."""

    def scan(self, scanner):
        i = scanner.simple()
        self.code = self.first + scanner.chop(i)

    def run(self, interpreter, locals):
        interpreter.serialize(self.code, locals)

    def string(self):
        return '%s%s' % (self.prefix, self.code)


class ReprToken(ExpansionToken):
    """A repr markup."""

    def scan(self, scanner):
        i = scanner.next('`', 0)
        self.code = scanner.chop(i, 1)

    def run(self, interpreter, locals):
        interpreter.write(repr(interpreter.evaluate(self.code, locals)))

    def string(self):
        return '%s`%s`' % (self.prefix, self.code)


class InPlaceToken(ExpansionToken):
    """An in-place markup."""

    def scan(self, scanner):
        i = scanner.next(':', 0)
        j = scanner.next(':', i + 1)
        self.code = scanner.chop(i, j - i + 1)

    def run(self, interpreter, locals):
        interpreter.write('%s:%s:' % (interpreter.prefix, self.code))
        try:
            interpreter.serialize(self.code, locals)
        finally:
            interpreter.write(':')

    def string(self):
        return '%s:%s::' % (self.prefix, self.code)


class StatementToken(ExpansionToken):
    """A statement markup."""

    def scan(self, scanner):
        i = scanner.complex('{', '}', 0)
        self.code = scanner.chop(i, 1)

    def run(self, interpreter, locals):
        interpreter.execute(self.code, locals)

    def string(self):
        return '%s{%s}' % (self.prefix, self.code)


class CustomToken(ExpansionToken):
    """A custom markup."""

    def scan(self, scanner):
        i = scanner.complex('<', '>', 0)
        self.contents = scanner.chop(i, 1)

    def run(self, interpreter, locals):
        interpreter.invokeCallback(self.contents)

    def string(self):
        return '%s<%s>' % (self.prefix, self.contents)


class ControlToken(ExpansionToken):
    """A control token."""
    PRIMARY_TYPES = [
     'if', 'for', 'while', 'try', 'def']
    SECONDARY_TYPES = ['elif', 'else', 'except', 'finally']
    TERTIARY_TYPES = ['continue', 'break']
    GREEDY_TYPES = ['if', 'elif', 'for', 'while', 'def', 'end']
    END_TYPES = ['end']
    IN_RE = re.compile('\\bin\\b')

    def scan(self, scanner):
        scanner.acquire()
        i = scanner.complex('[', ']', 0)
        self.contents = scanner.chop(i, 1)
        fields = string.split(string.strip(self.contents), ' ', 1)
        if len(fields) > 1:
            (self.type, self.rest) = fields
        else:
            self.type = fields[0]
            self.rest = None
        self.subtokens = []
        if self.type in self.GREEDY_TYPES and self.rest is None:
            raise ParseError, "control '%s' needs arguments" % self.type
        if self.type in self.PRIMARY_TYPES:
            self.subscan(scanner, self.type)
            self.kind = 'primary'
        elif self.type in self.SECONDARY_TYPES:
            self.kind = 'secondary'
        elif self.type in self.TERTIARY_TYPES:
            self.kind = 'tertiary'
        elif self.type in self.END_TYPES:
            self.kind = 'end'
        else:
            raise ParseError, "unknown control markup: '%s'" % self.type
        scanner.release()
        return

    def subscan(self, scanner, primary):
        """Do a subscan for contained tokens."""
        while True:
            token = scanner.one()
            if token is None:
                raise TransientParseError, "control '%s' needs more tokens" % primary
            if isinstance(token, ControlToken) and token.type in self.END_TYPES:
                if token.rest != primary:
                    raise ParseError, "control must end with 'end %s'" % primary
                break
            self.subtokens.append(token)

        return

    def build(self, allowed=None):
        """Process the list of subtokens and divide it into a list of
        2-tuples, consisting of the dividing tokens and the list of
        subtokens that follow them.  If allowed is specified, it will
        represent the list of the only secondary markup types which
        are allowed."""
        if allowed is None:
            allowed = SECONDARY_TYPES
        result = []
        latest = []
        result.append((self, latest))
        for subtoken in self.subtokens:
            if isinstance(subtoken, ControlToken) and subtoken.kind == 'secondary':
                if subtoken.type not in allowed:
                    raise ParseError, "control unexpected secondary: '%s'" % subtoken.type
                latest = []
                result.append((subtoken, latest))
            else:
                latest.append(subtoken)

        return result

    def run--- This code section failed: ---

 L.1504         0  LOAD_FAST             1  'interpreter'
                3  LOAD_ATTR             0  'invoke'
                6  LOAD_CONST               'beforeControl'
                9  LOAD_CONST               'type'
               12  LOAD_FAST             0  'self'
               15  LOAD_ATTR             1  'type'
               18  LOAD_CONST               'rest'
               21  LOAD_FAST             0  'self'
               24  LOAD_ATTR             2  'rest'
               27  LOAD_CONST               'locals'

 L.1505        30  LOAD_FAST             2  'locals'
               33  CALL_FUNCTION_769   769  None
               36  POP_TOP          

 L.1506        37  LOAD_FAST             0  'self'
               40  LOAD_ATTR             1  'type'
               43  LOAD_CONST               'if'
               46  COMPARE_OP            2  ==
               49  JUMP_IF_FALSE       210  'to 262'
               52  POP_TOP          

 L.1507        53  LOAD_FAST             0  'self'
               56  LOAD_ATTR             3  'build'
               59  LOAD_CONST               'elif'
               62  LOAD_CONST               'else'
               65  BUILD_LIST_2          2 
               68  CALL_FUNCTION_1       1  None
               71  STORE_FAST            3  'info'

 L.1508        74  LOAD_CONST               None
               77  STORE_FAST            4  'elseTokens'

 L.1509        80  LOAD_FAST             3  'info'
               83  LOAD_CONST               -1
               86  BINARY_SUBSCR    
               87  LOAD_CONST               0
               90  BINARY_SUBSCR    
               91  LOAD_ATTR             1  'type'
               94  LOAD_CONST               'else'
               97  COMPARE_OP            2  ==
              100  JUMP_IF_FALSE        20  'to 123'
            103_0  THEN                     124
              103  POP_TOP          

 L.1510       104  LOAD_FAST             3  'info'
              107  LOAD_ATTR             5  'pop'
              110  CALL_FUNCTION_0       0  None
              113  LOAD_CONST               1
              116  BINARY_SUBSCR    
              117  STORE_FAST            4  'elseTokens'
              120  JUMP_FORWARD          1  'to 124'
            123_0  COME_FROM           100  '100'
              123  POP_TOP          
            124_0  COME_FROM           120  '120'

 L.1511       124  SETUP_LOOP         1458  'to 1585'
              127  LOAD_FAST             3  'info'
              130  GET_ITER         
              131  FOR_ITER             94  'to 228'
              134  UNPACK_SEQUENCE_2     2 
              137  STORE_FAST            5  'secondary'
              140  STORE_FAST            6  'subtokens'

 L.1512       143  LOAD_FAST             5  'secondary'
              146  LOAD_ATTR             1  'type'
              149  LOAD_CONST               ('if', 'elif')
              152  COMPARE_OP            7  not-in
              155  JUMP_IF_FALSE        20  'to 178'
            158_0  THEN                     179
              158  POP_TOP          

 L.1513       159  LOAD_GLOBAL           6  'ParseError'

 L.1514       162  LOAD_CONST               "control 'if' unexpected secondary: '%s'"
              165  LOAD_FAST             5  'secondary'
              168  LOAD_ATTR             1  'type'
              171  BINARY_MODULO    
              172  RAISE_VARARGS_2       2  None
              175  JUMP_FORWARD          1  'to 179'
            178_0  COME_FROM           155  '155'
              178  POP_TOP          
            179_0  COME_FROM           175  '175'

 L.1515       179  LOAD_FAST             1  'interpreter'
              182  LOAD_ATTR             7  'evaluate'
              185  LOAD_FAST             5  'secondary'
              188  LOAD_ATTR             2  'rest'
              191  LOAD_FAST             2  'locals'
              194  CALL_FUNCTION_2       2  None
              197  JUMP_IF_FALSE        24  'to 224'
              200  POP_TOP          

 L.1516       201  LOAD_FAST             0  'self'
              204  LOAD_ATTR             8  'subrun'
              207  LOAD_FAST             6  'subtokens'
              210  LOAD_FAST             1  'interpreter'
              213  LOAD_FAST             2  'locals'
              216  CALL_FUNCTION_3       3  None
              219  POP_TOP          

 L.1517       220  BREAK_LOOP       
              221  JUMP_BACK           131  'to 131'
            224_0  COME_FROM           197  '197'
              224  POP_TOP          
              225  JUMP_BACK           131  'to 131'
              228  POP_BLOCK        

 L.1519       229  LOAD_FAST             4  'elseTokens'
              232  JUMP_IF_FALSE        23  'to 258'
              235  POP_TOP          

 L.1520       236  LOAD_FAST             0  'self'
              239  LOAD_ATTR             8  'subrun'
              242  LOAD_FAST             4  'elseTokens'
              245  LOAD_FAST             1  'interpreter'
              248  LOAD_FAST             2  'locals'
              251  CALL_FUNCTION_3       3  None
              254  POP_TOP          
              255  JUMP_ABSOLUTE      1585  'to 1585'
            258_0  COME_FROM           232  '232'
              258  POP_TOP          
              259  JUMP_FORWARD       1323  'to 1585'
            262_0  COME_FROM            49  '49'
              262  POP_TOP          

 L.1521       263  LOAD_FAST             0  'self'
              266  LOAD_ATTR             1  'type'
              269  LOAD_CONST               'for'
              272  COMPARE_OP            2  ==
              275  JUMP_IF_FALSE       331  'to 609'
              278  POP_TOP          

 L.1522       279  LOAD_FAST             0  'self'
              282  LOAD_ATTR             9  'IN_RE'
              285  LOAD_ATTR            10  'split'
              288  LOAD_FAST             0  'self'
              291  LOAD_ATTR             2  'rest'
              294  LOAD_CONST               1
              297  CALL_FUNCTION_2       2  None
              300  STORE_FAST            7  'sides'

 L.1523       303  LOAD_GLOBAL          11  'len'
              306  LOAD_FAST             7  'sides'
              309  CALL_FUNCTION_1       1  None
              312  LOAD_CONST               2
              315  COMPARE_OP            3  !=
              318  JUMP_IF_FALSE        13  'to 334'
            321_0  THEN                     335
              321  POP_TOP          

 L.1524       322  LOAD_GLOBAL           6  'ParseError'
              325  LOAD_CONST               "control expected 'for x in seq'"
              328  RAISE_VARARGS_2       2  None
              331  JUMP_FORWARD          1  'to 335'
            334_0  COME_FROM           318  '318'
              334  POP_TOP          
            335_0  COME_FROM           331  '331'

 L.1525       335  LOAD_FAST             7  'sides'
              338  UNPACK_SEQUENCE_2     2 
              341  STORE_FAST            8  'iterator'
              344  STORE_FAST            9  'sequenceCode'

 L.1526       347  LOAD_FAST             0  'self'
              350  LOAD_ATTR             3  'build'
              353  LOAD_CONST               'else'
              356  BUILD_LIST_1          1 
              359  CALL_FUNCTION_1       1  None
              362  STORE_FAST            3  'info'

 L.1527       365  LOAD_CONST               None
              368  STORE_FAST            4  'elseTokens'

 L.1528       371  LOAD_FAST             3  'info'
              374  LOAD_CONST               -1
              377  BINARY_SUBSCR    
              378  LOAD_CONST               0
              381  BINARY_SUBSCR    
              382  LOAD_ATTR             1  'type'
              385  LOAD_CONST               'else'
              388  COMPARE_OP            2  ==
              391  JUMP_IF_FALSE        20  'to 414'
            394_0  THEN                     415
              394  POP_TOP          

 L.1529       395  LOAD_FAST             3  'info'
              398  LOAD_ATTR             5  'pop'
              401  CALL_FUNCTION_0       0  None
              404  LOAD_CONST               1
              407  BINARY_SUBSCR    
              408  STORE_FAST            4  'elseTokens'
              411  JUMP_FORWARD          1  'to 415'
            414_0  COME_FROM           391  '391'
              414  POP_TOP          
            415_0  COME_FROM           411  '411'

 L.1530       415  LOAD_GLOBAL          11  'len'
              418  LOAD_FAST             3  'info'
              421  CALL_FUNCTION_1       1  None
              424  LOAD_CONST               1
              427  COMPARE_OP            3  !=
              430  JUMP_IF_FALSE        13  'to 446'
            433_0  THEN                     447
              433  POP_TOP          

 L.1531       434  LOAD_GLOBAL           6  'ParseError'
              437  LOAD_CONST               "control 'for' expects at most one 'else'"
              440  RAISE_VARARGS_2       2  None
              443  JUMP_FORWARD          1  'to 447'
            446_0  COME_FROM           430  '430'
              446  POP_TOP          
            447_0  COME_FROM           443  '443'

 L.1532       447  LOAD_FAST             1  'interpreter'
              450  LOAD_ATTR             7  'evaluate'
              453  LOAD_FAST             9  'sequenceCode'
              456  LOAD_FAST             2  'locals'
              459  CALL_FUNCTION_2       2  None
              462  STORE_FAST           10  'sequence'

 L.1533       465  SETUP_LOOP         1117  'to 1585'
              468  LOAD_FAST            10  'sequence'
              471  GET_ITER         
              472  FOR_ITER            100  'to 575'
              475  STORE_FAST           11  'element'

 L.1534       478  SETUP_EXCEPT         50  'to 531'

 L.1535       481  LOAD_FAST             1  'interpreter'
              484  LOAD_ATTR            12  'assign'
              487  LOAD_FAST             8  'iterator'
              490  LOAD_FAST            11  'element'
              493  LOAD_FAST             2  'locals'
              496  CALL_FUNCTION_3       3  None
              499  POP_TOP          

 L.1536       500  LOAD_FAST             0  'self'
              503  LOAD_ATTR             8  'subrun'
              506  LOAD_FAST             3  'info'
              509  LOAD_CONST               0
              512  BINARY_SUBSCR    
              513  LOAD_CONST               1
              516  BINARY_SUBSCR    
              517  LOAD_FAST             1  'interpreter'
              520  LOAD_FAST             2  'locals'
              523  CALL_FUNCTION_3       3  None
              526  POP_TOP          
              527  POP_BLOCK        
              528  JUMP_BACK           472  'to 472'
            531_0  COME_FROM           478  '478'

 L.1537       531  DUP_TOP          
              532  LOAD_GLOBAL          13  'ContinueFlow'
              535  COMPARE_OP           10  exception-match
              538  JUMP_IF_FALSE        10  'to 551'
              541  POP_TOP          
              542  POP_TOP          
              543  POP_TOP          
              544  POP_TOP          

 L.1538       545  CONTINUE            472  'to 472'
              548  JUMP_BACK           472  'to 472'
              551  POP_TOP          

 L.1539       552  DUP_TOP          
              553  LOAD_GLOBAL          14  'BreakFlow'
              556  COMPARE_OP           10  exception-match
              559  JUMP_IF_FALSE         8  'to 570'
              562  POP_TOP          
              563  POP_TOP          
              564  POP_TOP          
              565  POP_TOP          

 L.1540       566  BREAK_LOOP       
              567  JUMP_BACK           472  'to 472'
            570_0  COME_FROM           559  '559'
              570  POP_TOP          
              571  END_FINALLY      
              572  JUMP_BACK           472  'to 472'
              575  POP_BLOCK        

 L.1542       576  LOAD_FAST             4  'elseTokens'
              579  JUMP_IF_FALSE        23  'to 605'
              582  POP_TOP          

 L.1543       583  LOAD_FAST             0  'self'
              586  LOAD_ATTR             8  'subrun'
              589  LOAD_FAST             4  'elseTokens'
              592  LOAD_FAST             1  'interpreter'
              595  LOAD_FAST             2  'locals'
              598  CALL_FUNCTION_3       3  None
              601  POP_TOP          
              602  JUMP_ABSOLUTE      1585  'to 1585'
            605_0  COME_FROM           579  '579'
              605  POP_TOP          
              606  JUMP_FORWARD        976  'to 1585'
            609_0  COME_FROM           275  '275'
              609  POP_TOP          

 L.1544       610  LOAD_FAST             0  'self'
              613  LOAD_ATTR             1  'type'
              616  LOAD_CONST               'while'
              619  COMPARE_OP            2  ==
              622  JUMP_IF_FALSE       277  'to 902'
              625  POP_TOP          

 L.1545       626  LOAD_FAST             0  'self'
              629  LOAD_ATTR             2  'rest'
              632  STORE_FAST           12  'testCode'

 L.1546       635  LOAD_FAST             0  'self'
              638  LOAD_ATTR             3  'build'
              641  LOAD_CONST               'else'
              644  BUILD_LIST_1          1 
              647  CALL_FUNCTION_1       1  None
              650  STORE_FAST            3  'info'

 L.1547       653  LOAD_CONST               None
              656  STORE_FAST            4  'elseTokens'

 L.1548       659  LOAD_FAST             3  'info'
              662  LOAD_CONST               -1
              665  BINARY_SUBSCR    
              666  LOAD_CONST               0
              669  BINARY_SUBSCR    
              670  LOAD_ATTR             1  'type'
              673  LOAD_CONST               'else'
              676  COMPARE_OP            2  ==
              679  JUMP_IF_FALSE        20  'to 702'
            682_0  THEN                     703
              682  POP_TOP          

 L.1549       683  LOAD_FAST             3  'info'
              686  LOAD_ATTR             5  'pop'
              689  CALL_FUNCTION_0       0  None
              692  LOAD_CONST               1
              695  BINARY_SUBSCR    
              696  STORE_FAST            4  'elseTokens'
              699  JUMP_FORWARD          1  'to 703'
            702_0  COME_FROM           679  '679'
              702  POP_TOP          
            703_0  COME_FROM           699  '699'

 L.1550       703  LOAD_GLOBAL          11  'len'
              706  LOAD_FAST             3  'info'
              709  CALL_FUNCTION_1       1  None
              712  LOAD_CONST               1
              715  COMPARE_OP            3  !=
              718  JUMP_IF_FALSE        13  'to 734'
            721_0  THEN                     735
              721  POP_TOP          

 L.1551       722  LOAD_GLOBAL           6  'ParseError'
              725  LOAD_CONST               "control 'while' expects at most one 'else'"
              728  RAISE_VARARGS_2       2  None
              731  JUMP_FORWARD          1  'to 735'
            734_0  COME_FROM           718  '718'
              734  POP_TOP          
            735_0  COME_FROM           731  '731'

 L.1552       735  LOAD_GLOBAL          15  'False'
              738  STORE_FAST           13  'atLeastOnce'

 L.1553       741  SETUP_LOOP          117  'to 861'
              744  LOAD_GLOBAL          16  'True'
              747  JUMP_IF_FALSE       109  'to 859'
              750  POP_TOP          

 L.1554       751  SETUP_EXCEPT         61  'to 815'

 L.1555       754  LOAD_FAST             1  'interpreter'
              757  LOAD_ATTR             7  'evaluate'
              760  LOAD_FAST            12  'testCode'
              763  LOAD_FAST             2  'locals'
              766  CALL_FUNCTION_2       2  None
              769  JUMP_IF_TRUE          5  'to 777'
            772_0  THEN                     778
              772  POP_TOP          

 L.1556       773  BREAK_LOOP       
              774  JUMP_FORWARD          1  'to 778'
            777_0  COME_FROM           769  '769'
              777  POP_TOP          
            778_0  COME_FROM           774  '774'

 L.1557       778  LOAD_GLOBAL          16  'True'
              781  STORE_FAST           13  'atLeastOnce'

 L.1558       784  LOAD_FAST             0  'self'
              787  LOAD_ATTR             8  'subrun'
              790  LOAD_FAST             3  'info'
              793  LOAD_CONST               0
              796  BINARY_SUBSCR    
              797  LOAD_CONST               1
              800  BINARY_SUBSCR    
              801  LOAD_FAST             1  'interpreter'
              804  LOAD_FAST             2  'locals'
              807  CALL_FUNCTION_3       3  None
              810  POP_TOP          
              811  POP_BLOCK        
              812  JUMP_BACK           744  'to 744'
            815_0  COME_FROM           751  '751'

 L.1559       815  DUP_TOP          
              816  LOAD_GLOBAL          13  'ContinueFlow'
              819  COMPARE_OP           10  exception-match
              822  JUMP_IF_FALSE        10  'to 835'
              825  POP_TOP          
              826  POP_TOP          
              827  POP_TOP          
              828  POP_TOP          

 L.1560       829  CONTINUE            744  'to 744'
              832  JUMP_BACK           744  'to 744'
              835  POP_TOP          

 L.1561       836  DUP_TOP          
              837  LOAD_GLOBAL          14  'BreakFlow'
              840  COMPARE_OP           10  exception-match
              843  JUMP_IF_FALSE         8  'to 854'
              846  POP_TOP          
              847  POP_TOP          
              848  POP_TOP          
              849  POP_TOP          

 L.1562       850  BREAK_LOOP       
              851  JUMP_BACK           744  'to 744'
            854_0  COME_FROM           843  '843'
              854  POP_TOP          
              855  END_FINALLY      
              856  JUMP_BACK           744  'to 744'
              859  POP_TOP          
              860  POP_BLOCK        
            861_0  COME_FROM           741  '741'

 L.1563       861  LOAD_FAST            13  'atLeastOnce'
              864  UNARY_NOT        
              865  JUMP_IF_FALSE        30  'to 898'
              868  POP_TOP          
              869  LOAD_FAST             4  'elseTokens'
              872  JUMP_IF_FALSE        23  'to 898'
              875  POP_TOP          

 L.1564       876  LOAD_FAST             0  'self'
              879  LOAD_ATTR             8  'subrun'
              882  LOAD_FAST             4  'elseTokens'
              885  LOAD_FAST             1  'interpreter'
              888  LOAD_FAST             2  'locals'
              891  CALL_FUNCTION_3       3  None
              894  POP_TOP          
              895  JUMP_ABSOLUTE      1585  'to 1585'
            898_0  COME_FROM           872  '872'
            898_1  COME_FROM           865  '865'
              898  POP_TOP          
              899  JUMP_FORWARD        683  'to 1585'
            902_0  COME_FROM           622  '622'
              902  POP_TOP          

 L.1565       903  LOAD_FAST             0  'self'
              906  LOAD_ATTR             1  'type'
              909  LOAD_CONST               'try'
              912  COMPARE_OP            2  ==
              915  JUMP_IF_FALSE       481  'to 1399'
              918  POP_TOP          

 L.1566       919  LOAD_FAST             0  'self'
              922  LOAD_ATTR             3  'build'
              925  LOAD_CONST               'except'
              928  LOAD_CONST               'finally'
              931  BUILD_LIST_2          2 
              934  CALL_FUNCTION_1       1  None
              937  STORE_FAST            3  'info'

 L.1567       940  LOAD_GLOBAL          11  'len'
              943  LOAD_FAST             3  'info'
              946  CALL_FUNCTION_1       1  None
              949  LOAD_CONST               1
              952  COMPARE_OP            2  ==
              955  JUMP_IF_FALSE        13  'to 971'
            958_0  THEN                     972
              958  POP_TOP          

 L.1568       959  LOAD_GLOBAL           6  'ParseError'
              962  LOAD_CONST               "control 'try' needs 'except' or 'finally'"
              965  RAISE_VARARGS_2       2  None
              968  JUMP_FORWARD          1  'to 972'
            971_0  COME_FROM           955  '955'
              971  POP_TOP          
            972_0  COME_FROM           968  '968'

 L.1569       972  LOAD_FAST             3  'info'
              975  LOAD_CONST               -1
              978  BINARY_SUBSCR    
              979  LOAD_CONST               0
              982  BINARY_SUBSCR    
              983  LOAD_ATTR             1  'type'
              986  STORE_FAST           14  'type'

 L.1570       989  LOAD_FAST            14  'type'
              992  LOAD_CONST               'except'
              995  COMPARE_OP            2  ==
              998  JUMP_IF_FALSE        60  'to 1061'
             1001  POP_TOP          

 L.1571      1002  SETUP_LOOP          109  'to 1114'
             1005  LOAD_FAST             3  'info'
             1008  LOAD_CONST               1
             1011  SLICE+1          
             1012  GET_ITER         
             1013  FOR_ITER             41  'to 1057'
             1016  UNPACK_SEQUENCE_2     2 
             1019  STORE_FAST            5  'secondary'
             1022  STORE_FAST           15  '_tokens'

 L.1572      1025  LOAD_FAST             5  'secondary'
             1028  LOAD_ATTR             1  'type'
             1031  LOAD_CONST               'except'
             1034  COMPARE_OP            3  !=
             1037  JUMP_IF_FALSE        13  'to 1053'
             1040  POP_TOP          

 L.1573      1041  LOAD_GLOBAL           6  'ParseError'

 L.1574      1044  LOAD_CONST               "control 'try' cannot have 'except' and 'finally'"
             1047  RAISE_VARARGS_2       2  None
             1050  JUMP_BACK          1013  'to 1013'
           1053_0  COME_FROM          1037  '1037'
             1053  POP_TOP          
             1054  JUMP_BACK          1013  'to 1013'
             1057  POP_BLOCK        
             1058  JUMP_FORWARD         53  'to 1114'
           1061_0  COME_FROM           998  '998'
             1061  POP_TOP          

 L.1576      1062  LOAD_FAST            14  'type'
             1065  LOAD_CONST               'finally'
             1068  COMPARE_OP            2  ==
             1071  JUMP_IF_TRUE          7  'to 1081'
             1074  POP_TOP          
             1075  LOAD_ASSERT              AssertionError
             1078  RAISE_VARARGS_1       1  None
           1081_0  COME_FROM          1071  '1071'
             1081  POP_TOP          

 L.1577      1082  LOAD_GLOBAL          11  'len'
             1085  LOAD_FAST             3  'info'
             1088  CALL_FUNCTION_1       1  None
             1091  LOAD_CONST               2
             1094  COMPARE_OP            3  !=
             1097  JUMP_IF_FALSE        13  'to 1113'
           1100_0  THEN                     1114
             1100  POP_TOP          

 L.1578      1101  LOAD_GLOBAL           6  'ParseError'

 L.1579      1104  LOAD_CONST               "control 'try' can only have one 'finally'"
             1107  RAISE_VARARGS_2       2  None
             1110  JUMP_FORWARD          1  'to 1114'
           1113_0  COME_FROM          1097  '1097'
             1113  POP_TOP          
           1114_0  COME_FROM          1002  '1002'

 L.1580      1114  LOAD_FAST            14  'type'
             1117  LOAD_CONST               'except'
             1120  COMPARE_OP            2  ==
             1123  JUMP_IF_FALSE       207  'to 1333'
             1126  POP_TOP          

 L.1581      1127  SETUP_EXCEPT         31  'to 1161'

 L.1582      1130  LOAD_FAST             0  'self'
             1133  LOAD_ATTR             8  'subrun'
             1136  LOAD_FAST             3  'info'
             1139  LOAD_CONST               0
             1142  BINARY_SUBSCR    
             1143  LOAD_CONST               1
             1146  BINARY_SUBSCR    
             1147  LOAD_FAST             1  'interpreter'
             1150  LOAD_FAST             2  'locals'
             1153  CALL_FUNCTION_3       3  None
             1156  POP_TOP          
             1157  POP_BLOCK        
             1158  JUMP_ABSOLUTE      1396  'to 1396'
           1161_0  COME_FROM          1127  '1127'

 L.1583      1161  DUP_TOP          
             1162  LOAD_GLOBAL          18  'FlowError'
             1165  COMPARE_OP           10  exception-match
             1168  JUMP_IF_FALSE        10  'to 1181'
             1171  POP_TOP          
             1172  POP_TOP          
             1173  POP_TOP          
             1174  POP_TOP          

 L.1584      1175  RAISE_VARARGS_0       0  None
             1178  JUMP_ABSOLUTE      1396  'to 1396'
             1181  POP_TOP          

 L.1585      1182  DUP_TOP          
             1183  LOAD_GLOBAL          19  'Exception'
             1186  COMPARE_OP           10  exception-match
             1189  JUMP_IF_FALSE       136  'to 1328'
             1192  POP_TOP          
             1193  POP_TOP          
             1194  STORE_FAST           16  'e'
             1197  POP_TOP          

 L.1586      1198  SETUP_LOOP          129  'to 1330'
             1201  LOAD_FAST             3  'info'
             1204  LOAD_CONST               1
             1207  SLICE+1          
             1208  GET_ITER         
             1209  FOR_ITER            109  'to 1321'
             1212  UNPACK_SEQUENCE_2     2 
             1215  STORE_FAST            5  'secondary'
             1218  STORE_FAST           17  'tokens'

 L.1587      1221  LOAD_FAST             1  'interpreter'
             1224  LOAD_ATTR            20  'clause'
             1227  LOAD_FAST             5  'secondary'
             1230  LOAD_ATTR             2  'rest'
             1233  CALL_FUNCTION_1       1  None
             1236  UNPACK_SEQUENCE_2     2 
             1239  STORE_FAST           18  'exception'
             1242  STORE_FAST           19  'variable'

 L.1588      1245  LOAD_FAST            19  'variable'
             1248  LOAD_CONST               None
             1251  COMPARE_OP            9  is-not
             1254  JUMP_IF_FALSE        20  'to 1277'
           1257_0  THEN                     1278
             1257  POP_TOP          

 L.1589      1258  LOAD_FAST             1  'interpreter'
             1261  LOAD_ATTR            12  'assign'
             1264  LOAD_FAST            19  'variable'
             1267  LOAD_FAST            16  'e'
             1270  CALL_FUNCTION_2       2  None
             1273  POP_TOP          
             1274  JUMP_FORWARD          1  'to 1278'
           1277_0  COME_FROM          1254  '1254'
             1277  POP_TOP          
           1278_0  COME_FROM          1274  '1274'

 L.1590      1278  LOAD_GLOBAL          21  'isinstance'
             1281  LOAD_FAST            16  'e'
             1284  LOAD_FAST            18  'exception'
             1287  CALL_FUNCTION_2       2  None
             1290  JUMP_IF_FALSE        24  'to 1317'
             1293  POP_TOP          

 L.1591      1294  LOAD_FAST             0  'self'
             1297  LOAD_ATTR             8  'subrun'
             1300  LOAD_FAST            17  'tokens'
             1303  LOAD_FAST             1  'interpreter'
             1306  LOAD_FAST             2  'locals'
             1309  CALL_FUNCTION_3       3  None
             1312  POP_TOP          

 L.1592      1313  BREAK_LOOP       
             1314  JUMP_BACK          1209  'to 1209'
           1317_0  COME_FROM          1290  '1290'
             1317  POP_TOP          
             1318  JUMP_BACK          1209  'to 1209'
             1321  POP_BLOCK        

 L.1594      1322  RAISE_VARARGS_0       0  None
             1325  JUMP_ABSOLUTE      1396  'to 1396'
           1328_0  COME_FROM          1198  '1198'
           1328_1  COME_FROM          1189  '1189'
             1328  POP_TOP          
             1329  END_FINALLY      
             1330  JUMP_ABSOLUTE      1585  'to 1585'
           1333_0  COME_FROM          1123  '1123'
             1333  POP_TOP          

 L.1596      1334  SETUP_FINALLY        31  'to 1368'

 L.1597      1337  LOAD_FAST             0  'self'
             1340  LOAD_ATTR             8  'subrun'
             1343  LOAD_FAST             3  'info'
             1346  LOAD_CONST               0
             1349  BINARY_SUBSCR    
             1350  LOAD_CONST               1
             1353  BINARY_SUBSCR    
             1354  LOAD_FAST             1  'interpreter'
             1357  LOAD_FAST             2  'locals'
             1360  CALL_FUNCTION_3       3  None
             1363  POP_TOP          
             1364  POP_BLOCK        
             1365  LOAD_CONST               None
           1368_0  COME_FROM          1334  '1334'

 L.1599      1368  LOAD_FAST             0  'self'
             1371  LOAD_ATTR             8  'subrun'
             1374  LOAD_FAST             3  'info'
             1377  LOAD_CONST               1
             1380  BINARY_SUBSCR    
             1381  LOAD_CONST               1
             1384  BINARY_SUBSCR    
             1385  LOAD_FAST             1  'interpreter'
             1388  LOAD_FAST             2  'locals'
             1391  CALL_FUNCTION_3       3  None
             1394  POP_TOP          
             1395  END_FINALLY      
             1396  JUMP_FORWARD        186  'to 1585'
           1399_0  COME_FROM           915  '915'
             1399  POP_TOP          

 L.1600      1400  LOAD_FAST             0  'self'
             1403  LOAD_ATTR             1  'type'
             1406  LOAD_CONST               'continue'
             1409  COMPARE_OP            2  ==
             1412  JUMP_IF_FALSE        13  'to 1428'
             1415  POP_TOP          

 L.1601      1416  LOAD_GLOBAL          13  'ContinueFlow'
             1419  LOAD_CONST               "control 'continue' without 'for', 'while'"
             1422  RAISE_VARARGS_2       2  None
             1425  JUMP_FORWARD        157  'to 1585'
           1428_0  COME_FROM          1412  '1412'
             1428  POP_TOP          

 L.1602      1429  LOAD_FAST             0  'self'
             1432  LOAD_ATTR             1  'type'
             1435  LOAD_CONST               'break'
             1438  COMPARE_OP            2  ==
             1441  JUMP_IF_FALSE        13  'to 1457'
             1444  POP_TOP          

 L.1603      1445  LOAD_GLOBAL          14  'BreakFlow'
             1448  LOAD_CONST               "control 'break' without 'for', 'while'"
             1451  RAISE_VARARGS_2       2  None
             1454  JUMP_FORWARD        128  'to 1585'
           1457_0  COME_FROM          1441  '1441'
             1457  POP_TOP          

 L.1604      1458  LOAD_FAST             0  'self'
             1461  LOAD_ATTR             1  'type'
             1464  LOAD_CONST               'def'
             1467  COMPARE_OP            2  ==
             1470  JUMP_IF_FALSE        66  'to 1539'
             1473  POP_TOP          

 L.1605      1474  LOAD_FAST             0  'self'
             1477  LOAD_ATTR             2  'rest'
             1480  STORE_FAST           20  'signature'

 L.1606      1483  LOAD_FAST             0  'self'
             1486  LOAD_ATTR            22  'substring'
             1489  CALL_FUNCTION_0       0  None
             1492  STORE_FAST           21  'definition'

 L.1607      1495  LOAD_CONST               'def %s:\n r"""%s"""\n return %s.expand(r"""%s""", locals())\n'

 L.1610      1498  LOAD_FAST            20  'signature'
             1501  LOAD_FAST            21  'definition'
             1504  LOAD_FAST             1  'interpreter'
             1507  LOAD_ATTR            23  'pseudo'
             1510  LOAD_FAST            21  'definition'
             1513  BUILD_TUPLE_4         4 
             1516  BINARY_MODULO    
             1517  STORE_FAST           22  'code'

 L.1611      1520  LOAD_FAST             1  'interpreter'
             1523  LOAD_ATTR            24  'execute'
             1526  LOAD_FAST            22  'code'
             1529  LOAD_FAST             2  'locals'
             1532  CALL_FUNCTION_2       2  None
             1535  POP_TOP          
             1536  JUMP_FORWARD         46  'to 1585'
           1539_0  COME_FROM          1470  '1470'
             1539  POP_TOP          

 L.1612      1540  LOAD_FAST             0  'self'
             1543  LOAD_ATTR             1  'type'
             1546  LOAD_CONST               'end'
             1549  COMPARE_OP            2  ==
             1552  JUMP_IF_FALSE        13  'to 1568'
             1555  POP_TOP          

 L.1613      1556  LOAD_GLOBAL           6  'ParseError'
             1559  LOAD_CONST               "control 'end' requires primary markup"
             1562  RAISE_VARARGS_2       2  None
             1565  JUMP_FORWARD         17  'to 1585'
           1568_0  COME_FROM          1552  '1552'
             1568  POP_TOP          

 L.1615      1569  LOAD_GLOBAL           6  'ParseError'

 L.1616      1572  LOAD_CONST               "control '%s' cannot be at this level"
             1575  LOAD_FAST             0  'self'
             1578  LOAD_ATTR             1  'type'
             1581  BINARY_MODULO    
             1582  RAISE_VARARGS_2       2  None
           1585_0  COME_FROM           465  '465'
           1585_1  COME_FROM           124  '124'

 L.1617      1585  LOAD_FAST             1  'interpreter'
             1588  LOAD_ATTR             0  'invoke'
             1591  LOAD_CONST               'afterControl'
             1594  CALL_FUNCTION_1       1  None
             1597  POP_TOP          
             1598  LOAD_CONST               None
             1601  RETURN_VALUE     

Parse error at or near `COME_FROM' instruction at offset 1328_1

    def subrun(self, tokens, interpreter, locals):
        """Execute a sequence of tokens."""
        for token in tokens:
            token.run(interpreter, locals)

    def substring(self):
        return string.join(map(str, self.subtokens), '')

    def string(self):
        if self.kind == 'primary':
            return '%s[%s]%s%s[end %s]' % (
             self.prefix, self.contents, self.substring(),
             self.prefix, self.type)
        else:
            return '%s[%s]' % (self.prefix, self.contents)


class Scanner():
    """A scanner holds a buffer for lookahead parsing and has the
    ability to scan for special symbols and indicators in that
    buffer."""
    TOKEN_MAP = [
     (
      None, PrefixToken),
     (
      ' \t\x0b\r\n', WhitespaceToken),
     (
      ')]}', LiteralToken),
     (
      '\\', EscapeToken),
     (
      '#', CommentToken),
     (
      '?', ContextNameToken),
     (
      '!', ContextLineToken),
     (
      '%', SignificatorToken),
     (
      '(', ExpressionToken),
     (
      IDENTIFIER_FIRST_CHARS, SimpleExpressionToken),
     (
      '\'"', StringLiteralToken),
     (
      '`', ReprToken),
     (
      ':', InPlaceToken),
     (
      '[', ControlToken),
     (
      '{', StatementToken),
     (
      '<', CustomToken)]

    def __init__(self, prefix, data=''):
        self.prefix = prefix
        self.pointer = 0
        self.buffer = data
        self.lock = 0

    def __nonzero__(self):
        return self.pointer < len(self.buffer)

    def __len__(self):
        return len(self.buffer) - self.pointer

    def __getitem__(self, index):
        return self.buffer[(self.pointer + index)]

    def __getslice__(self, start, stop):
        if stop > len(self):
            stop = len(self)
        return self.buffer[self.pointer + start:self.pointer + stop]

    def advance(self, count=1):
        """Advance the pointer count characters."""
        self.pointer = self.pointer + count

    def retreat(self, count=1):
        self.pointer = self.pointer - count
        if self.pointer < 0:
            raise ParseError, "can't retreat back over synced out chars"

    def set(self, data):
        """Start the scanner digesting a new batch of data; start the pointer
        over from scratch."""
        self.pointer = 0
        self.buffer = data

    def feed(self, data):
        """Feed some more data to the scanner."""
        self.buffer = self.buffer + data

    def chop(self, count=None, slop=0):
        """Chop the first count + slop characters off the front, and return
        the first count.  If count is not specified, then return
        everything."""
        if count is None:
            assert slop == 0
            count = len(self)
        if count > len(self):
            raise TransientParseError, 'not enough data to read'
        result = self[:count]
        self.advance(count + slop)
        return result

    def acquire(self):
        """Lock the scanner so it doesn't destroy data on sync."""
        self.lock = self.lock + 1

    def release(self):
        """Unlock the scanner."""
        self.lock = self.lock - 1

    def sync(self):
        """Sync up the buffer with the read head."""
        if self.lock == 0 and self.pointer != 0:
            self.buffer = self.buffer[self.pointer:]
            self.pointer = 0

    def unsync(self):
        """Undo changes; reset the read head."""
        if self.pointer != 0:
            self.lock = 0
            self.pointer = 0

    def rest(self):
        """Get the remainder of the buffer."""
        return self[:]

    def read(self, i=0, count=1):
        """Read count chars starting from i; raise a transient error if
        there aren't enough characters remaining."""
        if len(self) < i + count:
            raise TransientParseError, 'need more data to read'
        else:
            return self[i:i + count]

    def check(self, i, archetype=None):
        """Scan for the next single or triple quote, with the specified
        archetype.  Return the found quote or None."""
        quote = None
        if self[i] in '\'"':
            quote = self[i]
            if len(self) - i < 3:
                for j in range(i, len(self)):
                    if self[i] == quote:
                        return quote
                else:
                    raise TransientParseError, 'need to scan for rest of quote'
            if self[(i + 1)] == self[(i + 2)] == quote:
                quote = quote * 3
        if quote is not None:
            if archetype is None:
                return quote
            elif archetype == quote:
                return quote
            elif len(archetype) < len(quote) and archetype[0] == quote[0]:
                return archetype
            else:
                return
        else:
            return
        return

    def find(self, sub, start=0, end=None):
        """Find the next occurrence of the character, or return -1."""
        if end is not None:
            return string.find(self.rest(), sub, start, end)
        else:
            return string.find(self.rest(), sub, start)
        return

    def last(self, char, start=0, end=None):
        """Find the first character that is _not_ the specified character."""
        if end is None:
            end = len(self)
        i = start
        while i < end:
            if self[i] != char:
                return i
            i = i + 1
        else:
            raise TransientParseError, 'expecting other than %s' % char

        return

    def next(self, target, start=0, end=None, mandatory=False):
        """Scan for the next occurrence of one of the characters in
        the target string; optionally, make the scan mandatory."""
        if mandatory:
            assert end is not None
        quote = None
        if end is None:
            end = len(self)
        i = start
        while i < end:
            newQuote = self.check(i, quote)
            if newQuote:
                if newQuote == quote:
                    quote = None
                else:
                    quote = newQuote
                i = i + len(newQuote)
            else:
                c = self[i]
                if quote:
                    if c == '\\':
                        i = i + 1
                elif c in target:
                    return i
                i = i + 1
        else:
            if mandatory:
                raise ParseError, 'expecting %s, not found' % target
            else:
                raise TransientParseError, 'expecting ending character'

        return

    def quote(self, start=0, end=None, mandatory=False):
        """Scan for the end of the next quote."""
        assert self[start] in '\'"'
        quote = self.check(start)
        if end is None:
            end = len(self)
        i = start + len(quote)
        while i < end:
            newQuote = self.check(i, quote)
            if newQuote:
                i = i + len(newQuote)
                if newQuote == quote:
                    return i
            else:
                c = self[i]
                if c == '\\':
                    i = i + 1
                i = i + 1
        else:
            if mandatory:
                raise ParseError, 'expecting end of string literal'
            else:
                raise TransientParseError, 'expecting end of string literal'

        return

    def nested(self, enter, exit, start=0, end=None):
        """Scan from i for an ending sequence, respecting entries and exits
        only."""
        depth = 0
        if end is None:
            end = len(self)
        i = start
        while i < end:
            c = self[i]
            if c == enter:
                depth = depth + 1
            elif c == exit:
                depth = depth - 1
                if depth < 0:
                    return i
            i = i + 1
        else:
            raise TransientParseError, 'expecting end of complex expression'

        return

    def complex(self, enter, exit, start=0, end=None, skip=None):
        """Scan from i for an ending sequence, respecting quotes,
        entries and exits."""
        quote = None
        depth = 0
        if end is None:
            end = len(self)
        last = None
        i = start
        while i < end:
            newQuote = self.check(i, quote)
            if newQuote:
                if newQuote == quote:
                    quote = None
                else:
                    quote = newQuote
                i = i + len(newQuote)
            else:
                c = self[i]
                if quote:
                    if c == '\\':
                        i = i + 1
                elif skip is None or last != skip:
                    if c == enter:
                        depth = depth + 1
                    elif c == exit:
                        depth = depth - 1
                        if depth < 0:
                            return i
                last = c
                i = i + 1
        else:
            raise TransientParseError, 'expecting end of complex expression'

        return

    def word(self, start=0):
        """Scan from i for a simple word."""
        length = len(self)
        i = start
        while i < length:
            if self[i] not in IDENTIFIER_CHARS:
                return i
            i = i + 1
        else:
            raise TransientParseError, 'expecting end of word'

    def phrase(self, start=0):
        """Scan from i for a phrase (e.g., 'word', 'f(a, b, c)', 'a[i]', or
        combinations like 'x[i](a)'."""
        i = self.word(start)
        while i < len(self) and self[i] in '([{':
            enter = self[i]
            if enter == '{':
                raise ParseError, "curly braces can't open simple expressions"
            exit = ENDING_CHARS[enter]
            i = self.complex(enter, exit, i + 1) + 1

        return i

    def simple(self, start=0):
        """Scan from i for a simple expression, which consists of one 
        more phrases separated by dots."""
        i = self.phrase(start)
        length = len(self)
        while i < length and self[i] == '.':
            i = self.phrase(i)

        while i > 0 and self[(i - 1)] == '.':
            i = i - 1

        return i

    def one(self):
        """Parse and return one token, or None if the scanner is empty."""
        if not self:
            return None
        if not self.prefix:
            loc = -1
        else:
            loc = self.find(self.prefix)
        if loc < 0:
            loc = len(self)
        if loc == 0:
            prefix = self.chop(1)
            assert prefix == self.prefix
            first = self.chop(1)
            if first == self.prefix:
                first = None
            for (firsts, factory) in self.TOKEN_MAP:
                if firsts is None:
                    if first is None:
                        break
                elif first in firsts:
                    break
            else:
                raise ParseError, 'unknown markup: %s%s' % (self.prefix, first)

            token = factory(self.prefix, first)
            try:
                token.scan(self)
            except TransientParseError:
                self.unsync()
                raise

        else:
            data = self.chop(loc)
            token = NullToken(data)
        self.sync()
        return token


class Interpreter():
    """An interpreter can process chunks of EmPy code."""
    VERSION = __version__
    SIGNIFICATOR_RE_SUFFIX = SIGNIFICATOR_RE_SUFFIX
    SIGNIFICATOR_RE_STRING = None
    Interpreter = None
    Hook = Hook
    Filter = Filter
    NullFilter = NullFilter
    FunctionFilter = FunctionFilter
    StringFilter = StringFilter
    BufferedFilter = BufferedFilter
    SizeBufferedFilter = SizeBufferedFilter
    LineBufferedFilter = LineBufferedFilter
    MaximallyBufferedFilter = MaximallyBufferedFilter
    ESCAPE_CODES = {0: '0', 7: 'a', 8: 'b', 27: 'e', 12: 'f', 127: 'h', 
       10: 'n', 13: 'r', 9: 't', 11: 'v', 4: 'z'}
    ASSIGN_TOKEN_RE = re.compile('[_a-zA-Z][_a-zA-Z0-9]*|\\(|\\)|,')
    DEFAULT_OPTIONS = {BANGPATH_OPT: True, BUFFERED_OPT: False, 
       RAW_OPT: False, 
       EXIT_OPT: True, 
       FLATTEN_OPT: False, 
       OVERRIDE_OPT: True, 
       CALLBACK_OPT: False}
    _wasProxyInstalled = False

    def __init__(self, output=None, argv=None, prefix=DEFAULT_PREFIX, pseudo=None, options=None, globals=None, hooks=None):
        self.interpreter = self
        if output is None:
            output = UncloseableFile(sys.__stdout__)
        self.output = output
        self.prefix = prefix
        if pseudo is None:
            pseudo = DEFAULT_PSEUDOMODULE_NAME
        self.pseudo = pseudo
        if argv is None:
            argv = [
             DEFAULT_SCRIPT_NAME]
        self.argv = argv
        self.args = argv[1:]
        if options is None:
            options = {}
        self.options = options
        self.hooksEnabled = None
        self.hooks = []
        if hooks is None:
            hooks = []
        for hook in hooks:
            self.register(hook)

        self.callback = None
        self.finals = []
        self.contexts = Stack()
        self.streams = Stack()
        self.globals = globals
        self.fix()
        self.history = Stack()
        self.installProxy()
        self.reset()
        if self.options.get(FLATTEN_OPT, False):
            self.flatten()
        if prefix is None:
            self.SIGNIFICATOR_RE_STRING = None
        else:
            self.SIGNIFICATOR_RE_STRING = prefix + self.SIGNIFICATOR_RE_SUFFIX
        self.Interpreter = self.__class__
        self.invoke('atStartup')
        return

    def __del__(self):
        self.shutdown()

    def __repr__(self):
        return '<%s pseudomodule/interpreter at 0x%x>' % (
         self.pseudo, id(self))

    def ready(self):
        """Declare the interpreter ready for normal operations."""
        self.invoke('atReady')

    def fix(self):
        """Reset the globals, stamping in the pseudomodule."""
        if self.globals is None:
            self.globals = {}
        if self.globals.has_key(self.pseudo):
            if self.globals[self.pseudo] is not self:
                raise Error, 'interpreter globals collision'
        self.globals[self.pseudo] = self
        return

    def unfix(self):
        """Remove the pseudomodule (if present) from the globals."""
        UNWANTED_KEYS = [
         self.pseudo, '__builtins__']
        for unwantedKey in UNWANTED_KEYS:
            if self.globals.has_key(unwantedKey):
                del self.globals[unwantedKey]

    def update(self, other):
        """Update the current globals dictionary with another dictionary."""
        self.globals.update(other)
        self.fix()

    def clear(self):
        """Clear out the globals dictionary with a brand new one."""
        self.globals = {}
        self.fix()

    def save(self, deep=True):
        if deep:
            copyMethod = copy.deepcopy
        else:
            copyMethod = copy.copy
        self.unfix()
        self.history.push(copyMethod(self.globals))
        self.fix()

    def restore(self, destructive=True):
        """Restore the topmost historic globals."""
        if destructive:
            fetchMethod = self.history.pop
        else:
            fetchMethod = self.history.top
        self.unfix()
        self.globals = fetchMethod()
        self.fix()

    def shutdown(self):
        """Declare this interpreting session over; close the stream file
        object.  This method is idempotent."""
        if self.streams is not None:
            try:
                self.finalize()
                self.invoke('atShutdown')
                while self.streams:
                    stream = self.streams.pop()
                    stream.close()

            finally:
                self.streams = None

        return

    def ok(self):
        """Is the interpreter still active?"""
        return self.streams is not None

    def write(self, data):
        self.stream().write(data)

    def writelines(self, stuff):
        self.stream().writelines(stuff)

    def flush(self):
        self.stream().flush()

    def close(self):
        self.shutdown()

    def context(self):
        return self.contexts.top()

    def stream(self):
        return self.streams.top()

    def reset(self):
        self.contexts.purge()
        self.streams.purge()
        self.streams.push(Stream(self.output))
        if self.options.get(OVERRIDE_OPT, True):
            sys.stdout.clear(self)

    def push(self):
        if self.options.get(OVERRIDE_OPT, True):
            sys.stdout.push(self)

    def pop(self):
        if self.options.get(OVERRIDE_OPT, True):
            sys.stdout.pop(self)

    def include(self, fileOrFilename, locals=None):
        """Do an include pass on a file or filename."""
        if type(fileOrFilename) is types.StringType:
            filename = fileOrFilename
            name = filename
            file = theSubsystem.open(filename, 'r')
        else:
            file = fileOrFilename
            name = '<%s>' % str(file.__class__)
        self.invoke('beforeInclude', name=name, file=file, locals=locals)
        self.file(file, name, locals)
        self.invoke('afterInclude')

    def expand(self, data, locals=None):
        """Do an explicit expansion on a subordinate stream."""
        outFile = StringIO.StringIO()
        stream = Stream(outFile)
        self.invoke('beforeExpand', string=data, locals=locals)
        self.streams.push(stream)
        try:
            self.string(data, '<expand>', locals)
            stream.flush()
            expansion = outFile.getvalue()
            self.invoke('afterExpand', result=expansion)
            return expansion
        finally:
            self.streams.pop()

    def quote(self, data):
        """Quote the given string so that if it were expanded it would
        evaluate to the original."""
        self.invoke('beforeQuote', string=data)
        scanner = Scanner(self.prefix, data)
        result = []
        i = 0
        try:
            j = scanner.next(self.prefix, i)
            result.append(data[i:j])
            result.append(self.prefix * 2)
            i = j + 1
        except TransientParseError:
            pass

        result.append(data[i:])
        result = string.join(result, '')
        self.invoke('afterQuote', result=result)
        return result

    def escape(self, data, more=''):
        """Escape a string so that nonprintable characters are replaced
        with compatible EmPy expansions."""
        self.invoke('beforeEscape', string=data, more=more)
        result = []
        for char in data:
            if char < ' ' or char > '~':
                charOrd = ord(char)
                if Interpreter.ESCAPE_CODES.has_key(charOrd):
                    result.append(self.prefix + '\\' + Interpreter.ESCAPE_CODES[charOrd])
                else:
                    result.append(self.prefix + '\\x%02x' % charOrd)
            elif char in more:
                result.append(self.prefix + '\\' + char)
            else:
                result.append(char)

        result = string.join(result, '')
        self.invoke('afterEscape', result=result)
        return result

    def wrap(self, callable, args):
        """Wrap around an application of a callable and handle errors.
        Return whether no error occurred."""
        try:
            apply(callable, args)
            self.reset()
            return True
        except KeyboardInterrupt, e:
            self.fail(e, True)
        except Exception, e:
            self.fail(e)
        except:
            e = sys.exc_type
            self.fail(e)

        self.reset()
        return False

    def interact(self):
        """Perform interaction."""
        self.invoke('atInteract')
        done = False
        while not done:
            result = self.wrap(self.file, (sys.stdin, '<interact>'))
            if self.options.get(EXIT_OPT, True):
                done = True
            elif result:
                done = True
            else:
                self.reset()

    def fail(self, error, fatal=False):
        """Handle an actual error that occurred."""
        if self.options.get(BUFFERED_OPT, False):
            try:
                self.output.abort()
            except AttributeError:
                pass

        meta = self.meta(error)
        self.handle(meta)
        if self.options.get(RAW_OPT, False):
            raise
        if fatal or self.options.get(EXIT_OPT, True):
            sys.exit(FAILURE_CODE)

    def file(self, file, name='<file>', locals=None):
        """Parse the entire contents of a file-like object, line by line."""
        context = Context(name)
        self.contexts.push(context)
        self.invoke('beforeFile', name=name, file=file, locals=locals)
        scanner = Scanner(self.prefix)
        first = True
        done = False
        while not done:
            self.context().bump()
            line = file.readline()
            if first:
                if self.options.get(BANGPATH_OPT, True) and self.prefix:
                    if string.find(line, BANGPATH) == 0:
                        line = self.prefix + '#' + line[2:]
                first = False
            if line:
                scanner.feed(line)
            else:
                done = True
            self.safe(scanner, done, locals)

        self.invoke('afterFile')
        self.contexts.pop()

    def binary(self, file, name='<binary>', chunkSize=0, locals=None):
        """Parse the entire contents of a file-like object, in chunks."""
        if chunkSize <= 0:
            chunkSize = DEFAULT_CHUNK_SIZE
        context = Context(name, units='bytes')
        self.contexts.push(context)
        self.invoke('beforeBinary', name=name, file=file, chunkSize=chunkSize, locals=locals)
        scanner = Scanner(self.prefix)
        done = False
        while not done:
            chunk = file.read(chunkSize)
            if chunk:
                scanner.feed(chunk)
            else:
                done = True
            self.safe(scanner, done, locals)
            self.context().bump(len(chunk))

        self.invoke('afterBinary')
        self.contexts.pop()

    def string(self, data, name='<string>', locals=None):
        """Parse a string."""
        context = Context(name)
        self.contexts.push(context)
        self.invoke('beforeString', name=name, string=data, locals=locals)
        context.bump()
        scanner = Scanner(self.prefix, data)
        self.safe(scanner, True, locals)
        self.invoke('afterString')
        self.contexts.pop()

    def safe(self, scanner, final=False, locals=None):
        """Do a protected parse.  Catch transient parse errors; if
        final is true, then make a final pass with a terminator,
        otherwise ignore the transient parse error (more data is
        pending)."""
        try:
            self.parse(scanner, locals)
        except TransientParseError:
            if final:
                buffer = scanner.rest()
                if buffer and buffer[(-1)] != '\n':
                    scanner.feed(self.prefix + '\n')
                self.parse(scanner, locals)

    def parse(self, scanner, locals=None):
        """Parse and run as much from this scanner as possible."""
        self.invoke('atParse', scanner=scanner, locals=locals)
        while True:
            token = scanner.one()
            if token is None:
                break
            self.invoke('atToken', token=token)
            token.run(self, locals)

        return

    def tokenize(self, name):
        """Take an lvalue string and return a name or a (possibly recursive)
        list of names."""
        result = []
        stack = [
         result]
        for garbage in self.ASSIGN_TOKEN_RE.split(name):
            garbage = string.strip(garbage)
            if garbage:
                raise ParseError, "unexpected assignment token: '%s'" % garbage

        tokens = self.ASSIGN_TOKEN_RE.findall(name)
        for token in tokens:
            if token == '(':
                stack.append([])
            elif token == ')':
                top = stack.pop()
                if len(top) == 1:
                    top = top[0]
                elif top[0] is None:
                    del top[0]
                stack[(-1)].append(top)
            elif token == ',':
                if len(stack[(-1)]) == 1:
                    stack[(-1)].insert(0, None)
            else:
                stack[(-1)].append(token)

        if result and result[0] is None:
            result = [
             result[1:]]
        if len(result) == 1:
            return result[0]
        else:
            return result
        return

    def significate(self, key, value=None, locals=None):
        """Declare a significator."""
        self.invoke('beforeSignificate', key=key, value=value, locals=locals)
        name = '__%s__' % key
        self.atomic(name, value, locals)
        self.invoke('afterSignificate')

    def atomic(self, name, value, locals=None):
        """Do an atomic assignment."""
        self.invoke('beforeAtomic', name=name, value=value, locals=locals)
        if locals is None:
            self.globals[name] = value
        else:
            locals[name] = value
        self.invoke('afterAtomic')
        return

    def multi(self, names, values, locals=None):
        """Do a (potentially recursive) assignment."""
        self.invoke('beforeMulti', names=names, values=values, locals=locals)
        i = 0
        try:
            values = tuple(values)
        except TypeError:
            raise TypeError, 'unpack non-sequence'

        if len(names) != len(values):
            raise ValueError, 'unpack tuple of wrong size'
        for i in range(len(names)):
            name = names[i]
            if type(name) is types.StringType:
                self.atomic(name, values[i], locals)
            else:
                self.multi(name, values[i], locals)

        self.invoke('afterMulti')

    def assign(self, name, value, locals=None):
        """Do a potentially complex (including tuple unpacking) assignment."""
        left = self.tokenize(name)
        if type(left) is types.StringType:
            self.atomic(left, value, locals)
        else:
            self.multi(left, value, locals)

    def import_(self, name, locals=None):
        """Do an import."""
        self.invoke('beforeImport', name=name, locals=locals)
        self.execute('import %s' % name, locals)
        self.invoke('afterImport')

    def clause(self, catch, locals=None):
        """Given the string representation of an except clause, turn it into
        a 2-tuple consisting of the class name, and either a variable name
        or None."""
        self.invoke('beforeClause', catch=catch, locals=locals)
        if catch is None:
            exceptionCode, variable = None, None
        elif string.find(catch, ',') >= 0:
            (exceptionCode, variable) = string.split(string.strip(catch), ',', 1)
            variable = string.strip(variable)
        else:
            exceptionCode, variable = string.strip(catch), None
        if not exceptionCode:
            exception = Exception
        else:
            exception = self.evaluate(exceptionCode, locals)
        self.invoke('afterClause', exception=exception, variable=variable)
        return (exception, variable)

    def serialize(self, expression, locals=None):
        """Do an expansion, involving evaluating an expression, then
        converting it to a string and writing that string to the
        output if the evaluation is not None."""
        self.invoke('beforeSerialize', expression=expression, locals=locals)
        result = self.evaluate(expression, locals)
        if result is not None:
            self.write(str(result))
        self.invoke('afterSerialize')
        return

    def defined(self, name, locals=None):
        """Return a Boolean indicating whether or not the name is
        defined either in the locals or the globals."""
        self.invoke('beforeDefined', name=name, local=local)
        if locals is not None:
            if locals.has_key(name):
                result = True
            else:
                result = False
        elif self.globals.has_key(name):
            result = True
        else:
            result = False
        self.invoke('afterDefined', result=result)
        return

    def literal(self, text):
        """Process a string literal."""
        self.invoke('beforeLiteral', text=text)
        self.serialize(text)
        self.invoke('afterLiteral')

    def evaluate(self, expression, locals=None):
        """Evaluate an expression."""
        if expression in ('1', 'True'):
            return True
        if expression in ('0', 'False'):
            return False
        self.push()
        try:
            self.invoke('beforeEvaluate', expression=expression, locals=locals)
            if locals is not None:
                result = eval(expression, self.globals, locals)
            else:
                result = eval(expression, self.globals)
            self.invoke('afterEvaluate', result=result)
            return result
        finally:
            self.pop()

        return

    def execute(self, statements, locals=None):
        """Execute a statement."""
        if string.find(statements, '\r') >= 0:
            statements = string.replace(statements, '\r', '')
        if string.find(statements, '\n') < 0:
            statements = string.strip(statements)
        self.push()
        try:
            self.invoke('beforeExecute', statements=statements, locals=locals)
            if locals is not None:
                exec statements in self.globals, locals
            else:
                exec statements in self.globals
            self.invoke('afterExecute')
        finally:
            self.pop()

        return

    def single(self, source, locals=None):
        """Execute an expression or statement, just as if it were
        entered into the Python interactive interpreter."""
        self.push()
        try:
            self.invoke('beforeSingle', source=source, locals=locals)
            code = compile(source, '<single>', 'single')
            if locals is not None:
                exec code in self.globals, locals
            else:
                exec code in self.globals
            self.invoke('afterSingle')
        finally:
            self.pop()

        return

    def register(self, hook, prepend=False):
        """Register the provided hook."""
        hook.register(self)
        if self.hooksEnabled is None:
            self.hooksEnabled = True
        if prepend:
            self.hooks.insert(0, hook)
        else:
            self.hooks.append(hook)
        return

    def deregister(self, hook):
        """Remove an already registered hook."""
        hook.deregister(self)
        self.hooks.remove(hook)

    def invoke(self, _name, **keywords):
        """Invoke the hook(s) associated with the hook name, should they
        exist."""
        if self.hooksEnabled:
            for hook in self.hooks:
                hook.push()
                try:
                    method = getattr(hook, _name)
                    apply(method, (), keywords)
                finally:
                    hook.pop()

    def finalize(self):
        """Execute any remaining final routines."""
        self.push()
        self.invoke('atFinalize')
        try:
            while self.finals:
                final = self.finals.pop()
                final()

        finally:
            self.pop()

    def meta(self, exc=None):
        """Construct a MetaError for the interpreter's current state."""
        return MetaError(self.contexts.clone(), exc)

    def handle(self, meta):
        """Handle a MetaError."""
        first = True
        self.invoke('atHandle', meta=meta)
        for context in meta.contexts:
            if first:
                if meta.exc is not None:
                    desc = 'error: %s: %s' % (meta.exc.__class__, meta.exc)
                else:
                    desc = 'error'
            else:
                desc = 'from this context'
            first = False
            sys.stderr.write('%s: %s\n' % (context, desc))

        return

    def installProxy(self):
        """Install a proxy if necessary."""
        try:
            sys.stdout._testProxy()
        except AttributeError:
            if Interpreter._wasProxyInstalled:
                raise Error, 'interpreter stdout proxy lost'
            else:
                sys.stdout = ProxyFile(sys.stdout)
                Interpreter._wasProxyInstalled = True

    def identify(self):
        """Identify the topmost context with a 2-tuple of the name and
        line number."""
        return self.context().identify()

    def atExit(self, callable):
        """Register a function to be called at exit."""
        self.finals.append(callable)

    def pushContext(self, name='<unnamed>', line=0):
        """Create a new context and push it."""
        self.contexts.push(Context(name, line))

    def popContext(self):
        """Pop the top context."""
        self.contexts.pop()

    def setContextName(self, name):
        """Set the name of the topmost context."""
        context = self.context()
        context.name = name

    def setContextLine(self, line):
        """Set the name of the topmost context."""
        context = self.context()
        context.line = line

    setName = setContextName
    setLine = setContextLine

    def getGlobals(self):
        """Retrieve the globals."""
        return self.globals

    def setGlobals(self, globals):
        """Set the globals to the specified dictionary."""
        self.globals = globals
        self.fix()

    def updateGlobals(self, otherGlobals):
        """Merge another mapping object into this interpreter's globals."""
        self.update(otherGlobals)

    def clearGlobals(self):
        """Clear out the globals with a brand new dictionary."""
        self.clear()

    def saveGlobals(self, deep=True):
        """Save a copy of the globals off onto the history stack."""
        self.save(deep)

    def restoreGlobals(self, destructive=True):
        """Restore the most recently saved copy of the globals."""
        self.restore(destructive)

    def areHooksEnabled(self):
        """Return whether or not hooks are presently enabled."""
        if self.hooksEnabled is None:
            return True
        else:
            return self.hooksEnabled
        return

    def enableHooks(self):
        """Enable hooks."""
        self.hooksEnabled = True

    def disableHooks(self):
        """Disable hooks."""
        self.hooksEnabled = False

    def getHooks(self):
        """Get the current hooks."""
        return self.hooks[:]

    def clearHooks(self):
        """Clear all hooks."""
        self.hooks = []

    def addHook(self, hook, prepend=False):
        """Add a new hook; optionally insert it rather than appending it."""
        self.register(hook, prepend)

    def removeHook(self, hook):
        """Remove a preexisting hook."""
        self.deregister(hook)

    def invokeHook(self, _name, **keywords):
        """Manually invoke a hook."""
        apply(self.invoke, (_name,), keywords)

    def getCallback(self):
        """Get the callback registered with this interpreter, or None."""
        return self.callback

    def registerCallback(self, callback):
        """Register a custom markup callback with this interpreter."""
        self.callback = callback

    def deregisterCallback(self):
        """Remove any previously registered callback with this interpreter."""
        self.callback = None
        return

    def invokeCallback(self, contents):
        """Invoke the callback."""
        if self.callback is None:
            if self.options.get(CALLBACK_OPT, False):
                raise Error, 'custom markup invoked with no defined callback'
        else:
            self.callback(contents)
        return

    def flatten(self, keys=None):
        """Flatten the contents of the pseudo-module into the globals
        namespace."""
        if keys is None:
            keys = self.__dict__.keys() + self.__class__.__dict__.keys()
        dict = {}
        for key in keys:
            dict[key] = getattr(self, key)

        self.globals.update(dict)
        return

    def getPrefix(self):
        """Get the current prefix."""
        return self.prefix

    def setPrefix(self, prefix):
        """Set the prefix."""
        self.prefix = prefix

    def stopDiverting(self):
        """Stop any diverting."""
        self.stream().revert()

    def createDiversion(self, name):
        """Create a diversion (but do not divert to it) if it does not
        already exist."""
        self.stream().create(name)

    def retrieveDiversion(self, name):
        """Retrieve the diversion object associated with the name."""
        return self.stream().retrieve(name)

    def startDiversion(self, name):
        """Start diverting to the given diversion name."""
        self.stream().divert(name)

    def playDiversion(self, name):
        """Play the given diversion and then purge it."""
        self.stream().undivert(name, True)

    def replayDiversion(self, name):
        """Replay the diversion without purging it."""
        self.stream().undivert(name, False)

    def purgeDiversion(self, name):
        """Eliminate the given diversion."""
        self.stream().purge(name)

    def playAllDiversions(self):
        """Play all existing diversions and then purge them."""
        self.stream().undivertAll(True)

    def replayAllDiversions(self):
        """Replay all existing diversions without purging them."""
        self.stream().undivertAll(False)

    def purgeAllDiversions(self):
        """Purge all existing diversions."""
        self.stream().purgeAll()

    def getCurrentDiversion(self):
        """Get the name of the current diversion."""
        return self.stream().currentDiversion

    def getAllDiversions(self):
        """Get the names of all existing diversions."""
        names = self.stream().diversions.keys()
        names.sort()
        return names

    def resetFilter(self):
        """Reset the filter so that it does no filtering."""
        self.stream().install(None)
        return

    def nullFilter(self):
        """Install a filter that will consume all text."""
        self.stream().install(0)

    def getFilter(self):
        """Get the current filter."""
        filter = self.stream().filter
        if filter is self.stream().file:
            return
        else:
            return filter
        return

    def setFilter(self, shortcut):
        """Set the filter."""
        self.stream().install(shortcut)

    def attachFilter(self, shortcut):
        """Attach a single filter to the end of the current filter chain."""
        self.stream().attach(shortcut)


class Document():
    """A representation of an individual EmPy document, as used by a
    processor."""

    def __init__(self, ID, filename):
        self.ID = ID
        self.filename = filename
        self.significators = {}


class Processor():
    """An entity which is capable of processing a hierarchy of EmPy
    files and building a dictionary of document objects associated
    with them describing their significator contents."""
    DEFAULT_EMPY_EXTENSIONS = ('.em', )
    SIGNIFICATOR_RE = re.compile(SIGNIFICATOR_RE_STRING)

    def __init__(self, factory=Document):
        self.factory = factory
        self.documents = {}

    def identifier(self, pathname, filename):
        return filename

    def clear(self):
        self.documents = {}

    def scan(self, basename, extensions=DEFAULT_EMPY_EXTENSIONS):
        if type(extensions) is types.StringType:
            extensions = (
             extensions,)

        def _noCriteria(x):
            return True

        def _extensionsCriteria(pathname, extensions=extensions):
            if extensions:
                for extension in extensions:
                    if pathname[-len(extension):] == extension:
                        return True

                return False
            else:
                return True

        self.directory(basename, _noCriteria, _extensionsCriteria, None)
        self.postprocess()
        return

    def postprocess(self):
        pass

    def directory(self, basename, dirCriteria, fileCriteria, depth=None):
        if depth is not None:
            if depth <= 0:
                return
            else:
                depth = depth - 1
        filenames = os.listdir(basename)
        for filename in filenames:
            pathname = os.path.join(basename, filename)
            if os.path.isdir(pathname):
                if dirCriteria(pathname):
                    self.directory(pathname, dirCriteria, fileCriteria, depth)
            elif os.path.isfile(pathname):
                if fileCriteria(pathname):
                    documentID = self.identifier(pathname, filename)
                    document = self.factory(documentID, pathname)
                    self.file(document, open(pathname))
                    self.documents[documentID] = document

        return

    def file(self, document, file):
        while True:
            line = file.readline()
            if not line:
                break
            self.line(document, line)

    def line(self, document, line):
        match = self.SIGNIFICATOR_RE.search(line)
        if match:
            (key, valueS) = match.groups()
            valueS = string.strip(valueS)
            if valueS:
                value = eval(valueS)
            else:
                value = None
            document.significators[key] = value
        return


def expand(_data, _globals=None, _argv=None, _prefix=DEFAULT_PREFIX, _pseudo=None, _options=None, **_locals):
    """Do an atomic expansion of the given source data, creating and
    shutting down an interpreter dedicated to the task.  The sys.stdout
    object is saved off and then replaced before this function
    returns."""
    if len(_locals) == 0:
        _locals = None
    output = NullFile()
    interpreter = Interpreter(output, argv=_argv, prefix=_prefix, pseudo=_pseudo, options=_options, globals=_globals)
    if interpreter.options.get(OVERRIDE_OPT, True):
        oldStdout = sys.stdout
    try:
        result = interpreter.expand(_data, _locals)
    finally:
        interpreter.shutdown()
        if _globals is not None:
            interpreter.unfix()
        if interpreter.options.get(OVERRIDE_OPT, True):
            sys.stdout = oldStdout

    return result


def environment(name, default=None):
    """Get data from the current environment.  If the default is True
    or False, then presume that we're only interested in the existence
    or non-existence of the environment variable."""
    if os.environ.has_key(name):
        if default == False or default == True:
            return True
        else:
            return os.environ[name]
    else:
        return default


def info(table):
    DEFAULT_LEFT = 28
    maxLeft = 0
    maxRight = 0
    for (left, right) in table:
        if len(left) > maxLeft:
            maxLeft = len(left)
        if len(right) > maxRight:
            maxRight = len(right)

    FORMAT = '  %%-%ds  %%s\n' % max(maxLeft, DEFAULT_LEFT)
    for (left, right) in table:
        if right.find('\n') >= 0:
            for right in right.split('\n'):
                sys.stderr.write(FORMAT % (left, right))
                left = ''

        else:
            sys.stderr.write(FORMAT % (left, right))


def usage(verbose=True):
    """Print usage information."""
    programName = sys.argv[0]

    def warn(line=''):
        sys.stderr.write('%s\n' % line)

    warn("Usage: %s [options] [<filename, or '-' for stdin> [<argument>...]]\nWelcome to EmPy version %s." % (programName, __version__))
    warn()
    warn('Valid options:')
    info(OPTION_INFO)
    if verbose:
        warn()
        warn('The following markups are supported:')
        info(MARKUP_INFO)
        warn()
        warn('Valid escape sequences are:')
        info(ESCAPE_INFO)
        warn()
        warn('The %s pseudomodule contains the following attributes:' % DEFAULT_PSEUDOMODULE_NAME)
        info(PSEUDOMODULE_INFO)
        warn()
        warn('The following environment variables are recognized:')
        info(ENVIRONMENT_INFO)
        warn()
        warn(USAGE_NOTES)
    else:
        warn()
        warn('Type %s -H for more extensive help.' % programName)


def invoke(args):
    """Run a standalone instance of an EmPy interpeter."""
    _output = None
    _options = {BUFFERED_OPT: environment(BUFFERED_ENV, False), RAW_OPT: environment(RAW_ENV, False), 
       EXIT_OPT: True, 
       FLATTEN_OPT: environment(FLATTEN_ENV, False), 
       OVERRIDE_OPT: not environment(NO_OVERRIDE_ENV, False), 
       CALLBACK_OPT: False}
    _preprocessing = []
    _prefix = environment(PREFIX_ENV, DEFAULT_PREFIX)
    _pseudo = environment(PSEUDO_ENV, None)
    _interactive = environment(INTERACTIVE_ENV, False)
    _extraArguments = environment(OPTIONS_ENV)
    _binary = -1
    _unicode = environment(UNICODE_ENV, False)
    _unicodeInputEncoding = environment(INPUT_ENCODING_ENV, None)
    _unicodeOutputEncoding = environment(OUTPUT_ENCODING_ENV, None)
    _unicodeInputErrors = environment(INPUT_ERRORS_ENV, None)
    _unicodeOutputErrors = environment(OUTPUT_ERRORS_ENV, None)
    _hooks = []
    _pauseAtEnd = False
    _relativePath = False
    if _extraArguments is not None:
        _extraArguments = string.split(_extraArguments)
        args = _extraArguments + args
    (pairs, remainder) = getopt.getopt(args, 'VhHvkp:m:frino:a:buBP:I:D:E:F:', ['version', 'help', 'extended-help', 'verbose', 'null-hook', 'suppress-errors', 'prefix=', 'no-prefix', 'module=', 'flatten', 'raw-errors', 'interactive', 'no-override-stdout', 'binary', 'chunk-size=', 'output=append=', 'preprocess=', 'import=', 'define=', 'execute=', 'execute-file=', 'buffered-output', 'pause-at-end', 'relative-path', 'no-callback-error', 'no-bangpath-processing', 'unicode', 'unicode-encoding=', 'unicode-input-encoding=', 'unicode-output-encoding=', 'unicode-errors=', 'unicode-input-errors=', 'unicode-output-errors='])
    for (option, argument) in pairs:
        if option in ('-V', '--version'):
            sys.stderr.write('%s version %s\n' % (__program__, __version__))
            return
        elif option in ('-h', '--help'):
            usage(False)
            return
        elif option in ('-H', '--extended-help'):
            usage(True)
            return
        elif option in ('-v', '--verbose'):
            _hooks.append(VerboseHook())
        elif option in ('--null-hook', ):
            _hooks.append(Hook())
        elif option in ('-k', '--suppress-errors'):
            _options[EXIT_OPT] = False
            _interactive = True
        elif option in ('-m', '--module'):
            _pseudo = argument
        elif option in ('-f', '--flatten'):
            _options[FLATTEN_OPT] = True
        elif option in ('-p', '--prefix'):
            _prefix = argument
        elif option in ('--no-prefix', ):
            _prefix = None
        elif option in ('-r', '--raw-errors'):
            _options[RAW_OPT] = True
        elif option in ('-i', '--interactive'):
            _interactive = True
        elif option in ('-n', '--no-override-stdout'):
            _options[OVERRIDE_OPT] = False
        elif option in ('-o', '--output'):
            _output = (
             argument, 'w', _options[BUFFERED_OPT])
        elif option in ('-a', '--append'):
            _output = (
             argument, 'a', _options[BUFFERED_OPT])
        elif option in ('-b', '--buffered-output'):
            _options[BUFFERED_OPT] = True
        elif option in ('-B', ):
            _options[BUFFERED_OPT] = True
        elif option in ('--binary', ):
            _binary = 0
        elif option in ('--chunk-size', ):
            _binary = int(argument)
        elif option in ('-P', '--preprocess'):
            _preprocessing.append(('pre', argument))
        elif option in ('-I', '--import'):
            for module in string.split(argument, ','):
                module = string.strip(module)
                _preprocessing.append(('import', module))

        elif option in ('-D', '--define'):
            _preprocessing.append(('define', argument))
        elif option in ('-E', '--execute'):
            _preprocessing.append(('exec', argument))
        elif option in ('-F', '--execute-file'):
            _preprocessing.append(('file', argument))
        elif option in ('-u', '--unicode'):
            _unicode = True
        elif option in ('--pause-at-end', ):
            _pauseAtEnd = True
        elif option in ('--relative-path', ):
            _relativePath = True
        elif option in ('--no-callback-error', ):
            _options[CALLBACK_OPT] = True
        elif option in ('--no-bangpath-processing', ):
            _options[BANGPATH_OPT] = False
        elif option in ('--unicode-encoding', ):
            _unicodeInputEncoding = _unicodeOutputEncoding = argument
        elif option in ('--unicode-input-encoding', ):
            _unicodeInputEncoding = argument
        elif option in ('--unicode-output-encoding', ):
            _unicodeOutputEncoding = argument
        elif option in ('--unicode-errors', ):
            _unicodeInputErrors = _unicodeOutputErrors = argument
        elif option in ('--unicode-input-errors', ):
            _unicodeInputErrors = argument
        elif option in ('--unicode-output-errors', ):
            _unicodeOutputErrors = argument

    if _unicode or _unicodeInputEncoding or _unicodeOutputEncoding or _unicodeInputErrors or _unicodeOutputErrors:
        theSubsystem.initialize(_unicodeInputEncoding, _unicodeOutputEncoding, _unicodeInputErrors, _unicodeOutputErrors)
    if _output is not None:
        _output = apply(AbstractFile, _output)
    if not remainder:
        remainder.append('-')
    filename, arguments = remainder[0], remainder[1:]
    if _options[BUFFERED_OPT] and _output is None:
        raise ValueError, '-b only makes sense with -o or -a arguments'
    if _prefix == 'None':
        _prefix = None
    if _prefix and type(_prefix) is types.StringType and len(_prefix) != 1:
        raise Error, 'prefix must be single-character string'
    interpreter = Interpreter(output=_output, argv=remainder, prefix=_prefix, pseudo=_pseudo, options=_options, hooks=_hooks)
    try:
        i = 0
        for (which, thing) in _preprocessing:
            if which == 'pre':
                command = interpreter.file
                target = theSubsystem.open(thing, 'r')
                name = thing
            elif which == 'define':
                command = interpreter.string
                if string.find(thing, '=') >= 0:
                    target = '%s{%s}' % (_prefix, thing)
                else:
                    target = '%s{%s = None}' % (_prefix, thing)
                name = '<define:%d>' % i
            elif which == 'exec':
                command = interpreter.string
                target = '%s{%s}' % (_prefix, thing)
                name = '<exec:%d>' % i
            elif which == 'file':
                command = interpreter.string
                name = '<file:%d (%s)>' % (i, thing)
                target = '%s{execfile("""%s""")}' % (_prefix, thing)
            elif which == 'import':
                command = interpreter.string
                name = '<import:%d>' % i
                target = '%s{import %s}' % (_prefix, thing)
            else:
                assert 0
            interpreter.wrap(command, (target, name))
            i = i + 1

        interpreter.ready()
        if filename == '-':
            if not _interactive:
                name = '<stdin>'
                path = ''
                file = sys.stdin
            else:
                (name, file) = (None, None)
        else:
            name = filename
            file = theSubsystem.open(filename, 'r')
            path = os.path.split(filename)[0]
            if _relativePath:
                sys.path.insert(0, path)
        if file is not None:
            if _binary < 0:
                interpreter.wrap(interpreter.file, (file, name))
            else:
                chunkSize = _binary
                interpreter.wrap(interpreter.binary, (file, name, chunkSize))
        if _interactive:
            interpreter.interact()
    finally:
        interpreter.shutdown()

    if _pauseAtEnd:
        try:
            raw_input()
        except EOFError:
            pass

    return


def main():
    invoke(sys.argv[1:])


if __name__ == '__main__':
    main()