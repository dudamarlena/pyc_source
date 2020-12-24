# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/ZPTKit/ExceptionFormatter.py
# Compiled at: 2006-06-20 16:13:48
"""An exception formatter that shows traceback supplements and traceback info,
optionally in HTML.

$Id: ExceptionFormatter.py,v 1.4 2002/08/14 22:12:06 mj Exp $
"""
import sys, cgi
DEBUG_EXCEPTION_FORMATTER = 1

class TextExceptionFormatter:
    __module__ = __name__
    line_sep = '\n'
    show_revisions = 0

    def __init__(self, limit=None):
        self.limit = limit

    def escape(self, s):
        return s

    def getPrefix(self):
        return 'Traceback (innermost last):'

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

    def formatSupplementLine(self, line):
        return '   - %s' % line

    def formatObject(self, object):
        return [
         self.formatSupplementLine(repr(object))]

    def formatSourceURL(self, url):
        return [
         self.formatSupplementLine('URL: %s' % url)]

    def formatSupplement(self, supplement, tb):
        result = []
        fmtLine = self.formatSupplementLine
        object = getattr(supplement, 'object', None)
        if object is not None:
            result.extend(self.formatObject(object))
        url = getattr(supplement, 'source_url', None)
        if url is not None:
            result.extend(self.formatSourceURL(url))
        line = getattr(supplement, 'line', 0)
        if line == -1:
            line = tb.tb_lineno
        col = getattr(supplement, 'column', -1)
        if line:
            if col is not None and col >= 0:
                result.append(fmtLine('Line %s, Column %s' % (line, col)))
            else:
                result.append(fmtLine('Line %s' % line))
        elif col is not None and col >= 0:
            result.append(fmtLine('Column %s' % col))
        expr = getattr(supplement, 'expression', None)
        if expr:
            result.append(fmtLine('Expression: %s' % expr))
        warnings = getattr(supplement, 'warnings', None)
        if warnings:
            for warning in warnings:
                result.append(fmtLine('Warning: %s' % warning))

        extra = self.formatExtraInfo(supplement)
        if extra:
            result.append(extra)
        return result

    def formatExtraInfo(self, supplement):
        getInfo = getattr(supplement, 'getInfo', None)
        if getInfo is not None:
            extra = getInfo()
            if extra:
                return extra
        return

    def formatTracebackInfo(self, tbi):
        return self.formatSupplementLine('__traceback_info__: %s' % (tbi,))

    def formatLine(self, tb):
        f = tb.tb_frame
        lineno = tb.tb_lineno
        co = f.f_code
        filename = co.co_filename
        name = co.co_name
        locals = f.f_locals
        globals = f.f_globals
        modname = globals.get('__name__', filename)
        s = '  Module %s, line %d' % (modname, lineno)
        revision = self.getRevision(globals)
        if revision:
            s = s + ', rev. %s' % revision
        s = s + ', in %s' % name
        result = []
        result.append(self.escape(s))
        try:
            f = open(filename, 'r')
            for i in range(lineno):
                line = f.readline()

            f.close()
            result.append('    %s' % line.rstrip())
        except (IOError, OSError):
            pass

        if locals.has_key('__traceback_supplement__'):
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
                result.extend(self.formatSupplement(supp, tb))
            except:
                if DEBUG_EXCEPTION_FORMATTER:
                    import traceback
                    traceback.print_exc()

        try:
            tbi = locals.get('__traceback_info__', None)
            if tbi is not None:
                result.append(self.formatTracebackInfo(tbi))
        except:
            pass

        return self.line_sep.join(result)

    def formatExceptionOnly(self, etype, value):
        import traceback
        return self.line_sep.join(traceback.format_exception_only(etype, value))

    def formatLastLine(self, exc_line):
        return self.escape(exc_line)

    def formatException(self, etype, value, tb, limit=None):
        __exception_formatter__ = 1
        result = [self.getPrefix() + '\n']
        if limit is None:
            limit = self.getLimit()
        n = 0
        while tb is not None and (limit is None or n < limit):
            if tb.tb_frame.f_locals.get('__exception_formatter__'):
                result.append('(Recursive formatException() stopped)\n')
                break
            line = self.formatLine(tb)
            result.append(line + '\n')
            tb = tb.tb_next
            n = n + 1

        exc_line = self.formatExceptionOnly(etype, value)
        result.append(self.formatLastLine(exc_line))
        return result


class HTMLExceptionFormatter(TextExceptionFormatter):
    __module__ = __name__
    line_sep = '<br />\r\n'

    def escape(self, s):
        return cgi.escape(s)

    def getPrefix(self):
        return '<p>Traceback (innermost last):\r\n<ul>'

    def formatSupplementLine(self, line):
        return '<b>%s</b>' % self.escape(str(line))

    def formatTracebackInfo(self, tbi):
        s = self.escape(str(tbi))
        s = s.replace('\n', self.line_sep)
        return '__traceback_info__: %s' % s

    def formatLine(self, tb):
        line = TextExceptionFormatter.formatLine(self, tb)
        return '<li>%s</li>' % line

    def formatLastLine(self, exc_line):
        return '</ul>%s</p>' % self.escape(exc_line)

    def formatExtraInfo(self, supplement):
        getInfo = getattr(supplement, 'getInfo', None)
        if getInfo is not None:
            extra = getInfo(1)
            if extra:
                return extra
        return


limit = 200
if hasattr(sys, 'tracebacklimit'):
    limit = min(limit, sys.tracebacklimit)
text_formatter = TextExceptionFormatter(limit)
html_formatter = HTMLExceptionFormatter(limit)

def format_exception(t, v, tb, limit=None, as_html=0):
    if as_html:
        fmt = html_formatter
    else:
        fmt = text_formatter
    return fmt.formatException(t, v, tb, limit=limit)