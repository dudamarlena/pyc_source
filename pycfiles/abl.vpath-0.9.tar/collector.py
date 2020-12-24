# uncompyle6 version 3.6.7
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.6-x86_64/egg/errorreporter/collector.py
# Compiled at: 2012-01-03 09:44:45
__doc__ = '\nAn exception collector that finds traceback information plus\nsupplements\n'
import sys, traceback, time
try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO

import linecache
from util import source_encoding, serial_number_generator
DEBUG_EXCEPTION_FORMATTER = True
DEBUG_IDENT_PREFIX = 'E-'
__all__ = [
 'collect_exception', 'ExceptionCollector']

class ExceptionCollector(object):
    """
    Produces a data structure that can be used by formatters to
    display exception reports.

    Magic variables:

    If you define one of these variables in your local scope, you can
    add information to tracebacks that happen in that context.  This
    allows applications to add all sorts of extra information about
    the context of the error, including URLs, environmental variables,
    users, hostnames, etc.  These are the variables we look for:

    ``__traceback_supplement__``:
        You can define this locally or globally (unlike all the other
        variables, which must be defined locally).

        ``__traceback_supplement__`` is a tuple of ``(factory, arg1,
        arg2...)``.  When there is an exception, ``factory(arg1, arg2,
        ...)`` is called, and the resulting object is inspected for
        supplemental information.

    ``__traceback_info__``:
        This information is added to the traceback, usually fairly
        literally.

    ``__traceback_hide__``:
        If set and true, this indicates that the frame should be
        hidden from abbreviated tracebacks.  This way you can hide
        some of the complexity of the larger framework and let the
        user focus on their own errors.

        By setting it to ``'before'``, all frames before this one will
        be thrown away.  By setting it to ``'after'`` then all frames
        after this will be thrown away until ``'reset'`` is found.  In
        each case the frame where it is set is included, unless you
        append ``'_and_this'`` to the value (e.g.,
        ``'before_and_this'``).

        Note that formatters will ignore this entirely if the frame
        that contains the error wouldn't normally be shown according
        to these rules.

    ``__traceback_reporter__``:
        This should be a reporter object (see the reporter module),
        or a list/tuple of reporter objects.  All reporters found this
        way will be given the exception, innermost first.

    ``__traceback_decorator__``:
        This object (defined in a local or global scope) will get the
        result of this function (the CollectedException defined
        below).  It may modify this object in place, or return an
        entirely new object.  This gives the object the ability to
        manipulate the traceback arbitrarily.

    The actually interpretation of these values is largely up to the
    reporters and formatters.
    
    ``collect_exception(*sys.exc_info())`` will return an object with
    several attributes:

    ``frames``:
        A list of frames
    ``exception_formatted``:
        The formatted exception, generally a full traceback
    ``exception_type``:
        The type of the exception, like ``ValueError``
    ``exception_value``:
        The string value of the exception, like ``'x not in list'``
    ``identification_code``:
        A hash of the exception data meant to identify the general
        exception, so that it shares this code with other exceptions
        that derive from the same problem.  The code is a hash of
        all the module names and function names in the traceback,
        plus exception_type.  This should be shown to users so they
        can refer to the exception later. (@@: should it include a
        portion that allows identification of the specific instance
        of the exception as well?)
        
    The list of frames goes innermost first.  Each frame has these
    attributes; some values may be None if they could not be
    determined.

    ``modname``:
        the name of the module
    ``filename``:
        the filename of the module
    ``lineno``:
        the line of the error
    ``revision``:
        the contents of __version__ or __revision__
    ``name``:
        the function name
    ``supplement``:
        an object created from ``__traceback_supplement__``
    ``supplement_exception``:
        a simple traceback of any exception ``__traceback_supplement__``
        created
    ``traceback_info``:
        the str() of any ``__traceback_info__`` variable found in the local
        scope (@@: should it str()-ify it or not?)
    ``traceback_hide``:
        the value of any ``__traceback_hide__`` variable
    ``traceback_log``:
        the value of any ``__traceback_log__`` variable
    

    ``__traceback_supplement__`` is thrown away, but a fixed
    set of attributes are captured; each of these attributes is
    optional.

    ``object``:
        the name of the object being visited
    ``source_url``:
        the original URL requested
    ``line``:
        the line of source being executed (for interpreters, like ZPT)
    ``column``:
        the column of source being executed
    ``expression``:
        the expression being evaluated (also for interpreters)
    ``warnings``:
        a list of (string) warnings to be displayed
    ``getInfo``:
        a function/method that takes no arguments, and returns a string
        describing any extra information
    ``extraData``:
        a function/method that takes no arguments, and returns a
        dictionary.  The contents of this dictionary will not be
        displayed in the context of the traceback, but globally for
        the exception.  Results will be grouped by the keys in the
        dictionaries (which also serve as titles).  The keys can also
        be tuples of (importance, title); in this case the importance
        should be ``important`` (shows up at top), ``normal`` (shows
        up somewhere; unspecified), ``supplemental`` (shows up at
        bottom), or ``extra`` (shows up hidden or not at all).

    These are used to create an object with attributes of the same
    names (``getInfo`` becomes a string attribute, not a method).
    ``__traceback_supplement__`` implementations should be careful to
    produce values that are relatively static and unlikely to cause
    further errors in the reporting system -- any complex
    introspection should go in ``getInfo()`` and should ultimately
    return a string.

    Note that all attributes are optional, and under certain
    circumstances may be None or may not exist at all -- the collector
    can only do a best effort, but must avoid creating any exceptions
    itself.

    Formatters may want to use ``__traceback_hide__`` as a hint to
    hide frames that are part of the 'framework' or underlying system.
    There are a variety of rules about special values for this
    variables that formatters should be aware of.
    
    TODO:

    More attributes in __traceback_supplement__?  Maybe an attribute
    that gives a list of local variables that should also be
    collected?  Also, attributes that would be explicitly meant for
    the entire request, not just a single frame.  Right now some of
    the fixed set of attributes (e.g., source_url) are meant for this
    use, but there's no explicit way for the supplement to indicate
    new values, e.g., logged-in user, HTTP referrer, environment, etc.
    Also, the attributes that do exist are Zope/Web oriented.

    More information on frames?  cgitb, for instance, produces
    extensive information on local variables.  There exists the
    possibility that getting this information may cause side effects,
    which can make debugging more difficult; but it also provides
    fodder for post-mortem debugging.  However, the collector is not
    meant to be configurable, but to capture everything it can and let
    the formatters be configurable.  Maybe this would have to be a
    configuration value, or maybe it could be indicated by another
    magical variable (which would probably mean 'show all local
    variables below this frame')
    """
    show_revisions = 0

    def __init__(self, limit=None):
        self.limit = limit

    def getLimit(self):
        limit = self.limit
        if limit is None:
            limit = getattr(sys, 'tracebacklimit', None)
        return limit

    def getRevision(self, globals):
        if not self.show_revisions:
            return
        revision = globals.get('__revision__', None)
        if revision is None:
            revision = globals.get('__version__', None)
        if revision is not None:
            try:
                revision = str(revision).strip()
            except:
                revision = '???'

        return revision

    def collectSupplement(self, supplement, tb):
        result = {}
        for name in ('object', 'source_url', 'line', 'column', 'expression', 'warnings'):
            result[name] = getattr(supplement, name, None)

        func = getattr(supplement, 'getInfo', None)
        if func:
            result['info'] = func()
        else:
            result['info'] = None
        func = getattr(supplement, 'extraData', None)
        if func:
            result['extra'] = func()
        else:
            result['extra'] = None
        return SupplementaryData(**result)

    def collectLine(self, tb, extra_data):
        f = tb.tb_frame
        lineno = tb.tb_lineno
        co = f.f_code
        filename = co.co_filename
        name = co.co_name
        locals = f.f_locals
        globals = f.f_globals
        data = {}
        data['modname'] = globals.get('__name__', None)
        data['filename'] = filename
        data['lineno'] = lineno
        data['revision'] = self.getRevision(globals)
        data['name'] = name
        data['tbid'] = id(tb)
        data['locals'] = locals
        if '__traceback_supplement__' in locals:
            tbs = locals['__traceback_supplement__']
        elif globals.has_key('__traceback_supplement__'):
            tbs = globals['__traceback_supplement__']
        else:
            tbs = None
        if tbs is not None:
            factory = tbs[0]
            args = tbs[1:]
            try:
                supp = factory(*args)
                data['supplement'] = self.collectSupplement(supp, tb)
                if data['supplement'].extra:
                    for (key, value) in data['supplement'].extra.items():
                        extra_data.setdefault(key, []).append(value)

            except:
                if DEBUG_EXCEPTION_FORMATTER:
                    out = StringIO()
                    traceback.print_exc(file=out)
                    text = out.getvalue()
                    data['supplement_exception'] = text

        try:
            tbi = locals.get('__traceback_info__', None)
            if tbi is not None:
                data['traceback_info'] = str(tbi)
        except:
            pass

        marker = []
        for name in ('__traceback_hide__', '__traceback_log__', '__traceback_decorator__'):
            try:
                tbh = locals.get(name, globals.get(name, marker))
                if tbh is not marker:
                    data[name[2:-2]] = tbh
            except:
                pass

        return data

    def collectExceptionOnly(self, etype, value):
        return traceback.format_exception_only(etype, value)

    def collectException(self, etype, value, tb, limit=None):
        __exception_formatter__ = 1
        frames = []
        ident_data = []
        traceback_decorators = []
        if limit is None:
            limit = self.getLimit()
        n = 0
        extra_data = {}
        while tb is not None and (limit is None or n < limit):
            if tb.tb_frame.f_locals.get('__exception_formatter__'):
                frames.append('(Recursive formatException() stopped)\n')
                break
            data = self.collectLine(tb, extra_data)
            frame = ExceptionFrame(**data)
            frames.append(frame)
            if frame.traceback_decorator is not None:
                traceback_decorators.append(frame.traceback_decorator)
            ident_data.append(frame.modname or '?')
            ident_data.append(frame.name or '?')
            tb = tb.tb_next
            n = n + 1

        ident_data.append(str(etype))
        ident = serial_number_generator.hash_identifier((' ').join(ident_data), length=5, upper=True, prefix=DEBUG_IDENT_PREFIX)
        result = CollectedException(frames=frames, exception_formatted=self.collectExceptionOnly(etype, value), exception_type=etype, exception_value=self.safeStr(value), identification_code=ident, date=time.localtime(), extra_data=extra_data)
        if etype is ImportError:
            extra_data[('important', 'sys.path')] = [
             sys.path]
        for decorator in traceback_decorators:
            try:
                new_result = decorator(result)
                if new_result is not None:
                    result = new_result
            except:
                pass

        return result

    def safeStr(self, obj):
        try:
            return str(obj)
        except UnicodeEncodeError:
            try:
                return unicode(obj).encode(FALLBACK_ENCODING, 'replace')
            except UnicodeEncodeError:
                return repr(obj)

        except:
            try:
                extra = ' (exception showing exception: %s)' % str(sys.exc_info()[1])
            except:
                extra = ''
            else:
                return repr(obj) + extra


limit = 200

class Bunch(object):
    """
    A generic container
    """

    def __init__(self, **attrs):
        for (name, value) in attrs.items():
            setattr(self, name, value)

    def __repr__(self):
        name = '<%s ' % self.__class__.__name__
        try:
            name += (' ').join([ '%s=%r' % (name, str(value)[:30]) for (name, value) in self.__dict__.items() if not name.startswith('_')
                               ])
        except:
            name += ' UNABLE TO GET REPRESENTATION'

        return name + '>'


class CollectedException(Bunch):
    """
    This is the result of collection the exception; it contains copies
    of data of interest.
    """
    frames = []
    exception_formatted = None
    exception_type = None
    exception_value = None
    identification_code = None
    date = None
    extra_data = {}


class SupplementaryData(Bunch):
    """
    The result of __traceback_supplement__.  We don't keep the
    supplement object around, for fear of GC problems and whatnot.
    (@@: Maybe I'm being too superstitious about copying only specific
    information over)
    """
    object = None
    source_url = None
    line = None
    column = None
    expression = None
    warnings = None
    info = None


class ExceptionFrame(Bunch):
    """
    This represents one frame of the exception.  Each frame is a
    context in the call stack, typically represented by a line
    number and module name in the traceback.
    """
    modname = None
    filename = None
    lineno = None
    revision = None
    name = None
    supplement = None
    supplement_exception = None
    traceback_info = None
    traceback_hide = False
    traceback_decorator = None
    tbid = None
    _source_encoding = None

    def get_source_line(self, context=0):
        """
        Return the source of the current line of this frame.  You
        probably want to .strip() it as well, as it is likely to have
        leading whitespace.

        If context is given, then that many lines on either side will
        also be returned.  E.g., context=1 will give 3 lines.
        """
        if not self.filename or not self.lineno:
            return
        lines = []
        for lineno in range(self.lineno - context, self.lineno + context + 1):
            lines.append(linecache.getline(self.filename, lineno))

        return ('').join(lines)

    def _get_source_encoding(self):
        if self._source_encoding:
            return self._source_encoding
        lines = [
         linecache.getline(self.filename, 1),
         linecache.getline(self.filename, 2)]
        self._source_encoding = source_encoding.parse_encoding(lines) or 'ascii'
        return self._source_encoding

    source_encoding = property(_get_source_encoding)


if hasattr(sys, 'tracebacklimit'):
    limit = min(limit, sys.tracebacklimit)
col = ExceptionCollector()

def collect_exception(t, v, tb, limit=None):
    """
    Collection an exception from ``sys.exc_info()``.
    
    Use like::

      try:
          blah blah
      except:
          exc_data = collect_exception(*sys.exc_info())
    """
    return col.collectException(t, v, tb, limit=limit)