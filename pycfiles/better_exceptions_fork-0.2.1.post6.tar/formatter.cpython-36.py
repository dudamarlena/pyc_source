# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\adrie\Desktop\Programmation\better-exceptions\better_exceptions\formatter.py
# Compiled at: 2018-04-28 19:12:32
# Size of source mod 2**32: 14045 bytes
from __future__ import absolute_import
import distutils.sysconfig, inspect, linecache, os, platform, re, site, sys, sysconfig, traceback, ansimarkup
from pygments.token import Token
from .color import SUPPORTS_COLOR
from .highlighter import Highlighter
from .repl import get_repl
PY3 = sys.version_info[0] >= 3
THEME = {'introduction':'<y><b>{introduction}</b></y>', 
 'cause':'<b>{cause}</b>', 
 'context':'<b>{context}</b>', 
 'location':'  File "<g>{dirname}<b>{basename}</b></g>", line <y>{lineno}</y>, in <m>{source}</m>', 
 'short_location':'  File "<g>{dirname}<b>{basename}</b></g>", line <y>{lineno}</y>', 
 'exception':'<r><b>{type_}</b></r>:<b>{value}</b>', 
 'inspect':'    <c>{pipes}{cap} <b>{value}</b></c>'}
MAX_LENGTH = 128

class ExceptionFormatter(object):
    CMDLINE_REGXP = re.compile('(?:[^\\t ]*([\\\'"])(?:\\\\.|.)*(?:\\1))[^\\t ]*|([^\\t ]+)')

    def __init__(self, colored=SUPPORTS_COLOR, theme=THEME, max_length=MAX_LENGTH, encoding=None):
        self._colored = colored
        self._theme = theme
        self._max_length = max_length
        self._encoding = encoding or 'ascii'
        self._pipe_char = self.get_pipe_char()
        self._cap_char = self.get_cap_char()
        self._introduction = 'Traceback (most recent call last):'
        self._cause = getattr(traceback, '_cause_message', 'The above exception was the direct cause of the following exception:').strip()
        self._context = getattr(traceback, '_context_message', 'During handling of the above exception, another exception occurred:').strip()
        self._lib_dirs = self.get_lib_dirs()
        self._highlighter = Highlighter()

    def _get_char(self, value, default):
        try:
            value.encode(self._encoding)
        except UnicodeEncodeError:
            return default
        else:
            return value

    def get_pipe_char(self):
        return self._get_char('│', '|')

    def get_cap_char(self):
        return self._get_char('└', '->')

    def get_lib_dirs(self):
        lib_dirs = [
         sysconfig.get_path('stdlib'), site.USER_SITE, distutils.sysconfig.get_python_lib()]
        if hasattr(sys, 'real_prefix'):
            lib_dirs.append(sys.prefix)
            lib_dirs.append(sysconfig.get_path('stdlib').replace(sys.prefix, sys.real_prefix))
        if hasattr(sys, 'getsitepackages'):
            lib_dirs += site.getsitepackages()
        return [os.path.abspath(d) for d in lib_dirs]

    def get_relevant_names(self, source):
        source = self.sanitize(source)
        tokens = self._highlighter.get_tokens(source)
        names = []
        name = ''
        for index, tokentype, value in tokens:
            if tokentype in Token.Name:
                name += value
                names.append((index, name))
            elif tokentype in Token.Operator and value == '.':
                name += '.'
            else:
                if tokentype not in Token.Text:
                    name = ''

        return names

    def get_relevant_values(self, source, frame):
        names = self.get_relevant_names(source)
        values = []
        for index, name in names:
            vals = name.split('.')
            identifier, attrs = vals[0], vals[1:]
            for variables in (frame.f_locals, frame.f_globals, frame.f_builtins):
                try:
                    val = variables[identifier]
                except KeyError:
                    continue

                try:
                    for attr in attrs:
                        val = getattr(val, attr)

                except:
                    pass
                else:
                    values.append((index, self.format_value(val)))
                break

        values.sort()
        return values

    def format_value(self, v):
        try:
            v = repr(v)
        except:
            v = '<unprintable %s object>' % type(v).__name__

        max_length = self._max_length
        if max_length is not None:
            if len(v) > max_length:
                v = v[:max_length] + '...'
        return v

    def split_cmdline(self, cmdline):
        return [m.group(0) for m in self.CMDLINE_REGXP.finditer(cmdline)]

    def get_string_source(self):
        cmdline = None
        if platform.system() == 'Windows':
            return ''
        else:
            if platform.system() == 'Linux':
                pass
            if cmdline is None and os.name == 'posix':
                from subprocess import CalledProcessError, check_output as spawn
                try:
                    cmdline = spawn(['ps', '-ww', '-p', str(os.getpid()), '-o', 'command='])
                except CalledProcessError:
                    return ''
                else:
                    if PY3 and isinstance(cmdline, bytes) or not PY3 and isinstance(cmdline, str):
                        cmdline = cmdline.decode(sys.stdout.encoding or 'utf-8')
            else:
                return ''
            cmdline = cmdline.strip()
            cmdline = self.split_cmdline(cmdline)
            extra_args = sys.argv[1:]
            if len(extra_args) > 0:
                if cmdline[-len(extra_args):] != extra_args:
                    return ''
                cmdline = cmdline[1:-len(extra_args)]
            skip = 0
            for i in range(len(cmdline)):
                a = cmdline[i].strip()
                if not a.startswith('-c'):
                    skip += 1
                else:
                    a = a[2:].strip()
                    if len(a) > 0:
                        cmdline[i] = a
                    else:
                        skip += 1
                    break

            cmdline = cmdline[skip:]
            source = ' '.join(cmdline)
            return source

    def colorize(self, theme, **kwargs):
        template = self._theme[theme]
        if not self._colored:
            template = ansimarkup.strip(template)
        else:
            template = ansimarkup.parse(template)
        return (template.format)(**kwargs)

    def colorize_location(self, filepath, lineno, source=None):
        dirname, basename = os.path.split(filepath)
        if dirname:
            dirname += os.sep
        else:
            if source is None:
                theme = 'short_location'
            else:
                theme = 'location'
        return self.colorize(theme, dirname=dirname, basename=basename, lineno=lineno, source=source)

    def colorize_traceback(self, full_traceback):
        pipe = re.escape(self._pipe_char)
        cap = re.escape(self._cap_char)
        reg = re.compile('^(?P<location>  File "(?P<filepath>.*?)", line (?P<lineno>(?:\\d+|\\?))(?:, in (?P<source>.*))?)\\n((?P<code>    .*\\n(?:\\s*\\^)?)(?P<inspect>(?:    [\\s(?:{pipe})]*{cap} .*\\n)*))?'.format(pipe=pipe,
          cap=cap),
          flags=(re.M))
        local = {}

        def sub(match):
            dct = match.groupdict()
            location = dct['location']
            filepath, lineno, source = dct['filepath'], dct['lineno'], dct['source']
            code, inspect = dct['code'], dct['inspect']
            if code is None:
                code = ''
            else:
                if inspect is None:
                    inspect = ''
                if local:
                    init = False
                    is_previous_mine = local['is_previous_mine']
                else:
                    init = True
                is_previous_mine = True
            is_mine = self.is_file_mine(filepath)
            if is_mine is None:
                is_mine = is_previous_mine
            if is_mine:
                location = self.colorize_location(filepath=filepath, lineno=lineno, source=source)
                if code:
                    code = self.colorize_source(code)
                if inspect:
                    reg_inspect = '^    (?P<pipes>[\\s(?:{pipe})]*)(?P<cap>{cap}) (?P<value>.*)$'.format(pipe=pipe, cap=cap)
                    inspect = re.sub(reg_inspect, (lambda m: (self.colorize)(*('inspect', ), **m.groupdict())), inspect, flags=(re.M))
            if is_mine or is_previous_mine:
                if not init:
                    location = '\n' + location
            local['is_previous_mine'] = is_mine
            return '{}\n{}{}'.format(location, code, inspect)

        return reg.sub(sub, full_traceback)

    def colorize_source(self, source):
        if not self._colored:
            return source
        else:
            return self._highlighter.highlight(source)

    def is_file_mine(self, filepath):
        if filepath == '<string>':
            return
        else:
            filepath = os.path.abspath(filepath)
            if not os.path.isfile(filepath):
                return False
            return not any(filepath.lower().startswith(d.lower()) for d in self._lib_dirs)

    def get_traceback_information(self, tb):
        lineno = tb.tb_lineno
        filename = tb.tb_frame.f_code.co_filename
        function = tb.tb_frame.f_code.co_name
        repl = get_repl()
        if repl is not None and filename in repl.entries:
            _, filename, source = repl.entries[filename]
            source = source.replace('\r\n', '\n').split('\n')[(lineno - 1)]
        else:
            if filename == '<string>':
                source = self.get_string_source()
            else:
                source = linecache.getline(filename, lineno)
        if not PY3:
            if isinstance(source, str):
                source = source.decode('utf-8')
        source = source.strip()
        relevant_values = self.get_relevant_values(source, tb.tb_frame)
        return (
         filename, lineno, function, source, relevant_values)

    def format_traceback_frame(self, tb):
        traceback_information = self.get_traceback_information(tb)
        filename, lineno, function, source, relevant_values = traceback_information
        cap_char = self._cap_char
        lines = [
         source]
        for i in reversed(range(len(relevant_values))):
            col, val = relevant_values[i]
            pipe_cols = [pcol for pcol, _ in relevant_values[:i]]
            line = ''
            index = 0
            for pc in pipe_cols:
                line += ' ' * (pc - index) + self._pipe_char
                index = pc + 1

            line += ' ' * (col - index)
            first, *parts = val.split('\n')
            lines.append(line + cap_char + ' ' + first)
            preline = line + ' ' * (len(cap_char) + 1)
            for part in parts:
                lines.append(preline + part)

        formatted = '\n    '.join(lines)
        return (
         (
          filename, lineno, function, formatted), source)

    def format_traceback(self, tb=None):
        omit_last = False
        if not tb:
            try:
                raise Exception()
            except:
                omit_last = True
                _, _, tb = sys.exc_info()
                if not tb is not None:
                    raise AssertionError

        frames = []
        final_source = ''
        while tb:
            if omit_last:
                if not tb.tb_next:
                    break
            formatted, source = self.format_traceback_frame(tb)
            if not (os.path.basename(formatted[0]) == 'code.py' and formatted[2] == 'runcode'):
                final_source = source
                frames.append(formatted)
            tb = tb.tb_next

        lines = traceback.format_list(frames)
        return (
         ''.join(lines), final_source)

    def sanitize(self, string):
        encoding = self._encoding
        return string.encode(encoding, errors='backslashreplace').decode(encoding)

    def format_exception(self, exc, value, tb, _seen=None):
        if _seen is None:
            _seen = {
             None}
        else:
            exc = type(value)
            _seen.add(value)
            if value:
                if getattr(value, '__cause__', None) not in _seen:
                    for text in self.format_exception((type(value.__cause__)), (value.__cause__), (value.__cause__.__traceback__),
                      _seen=_seen):
                        yield text

                    yield '\n\n' + self.colorize('cause', cause=(self._cause)) + '\n\n\n'
                elif getattr(value, '__context__', None) not in _seen:
                    if not getattr(value, '__suppress_context__', True):
                        for text in self.format_exception((type(value.__context__)), (value.__context__),
                          (value.__context__.__traceback__),
                          _seen=_seen):
                            yield text

                        yield '\n\n' + self.colorize('context', context=(self._context)) + '\n\n\n'
            if tb is not None:
                yield self.colorize('introduction', introduction=(self._introduction)) + '\n\n'
            formatted, source = self.format_traceback(tb)
            if formatted:
                formatted += '\n'
            if not str(value):
                if exc is AssertionError:
                    colored_source = self.colorize_source(source)
                    value.args = (colored_source,)
            exception_only = traceback.format_exception_only(exc, value)
            if exception_only:
                if ':' in exception_only[(-1)]:
                    type_, value = exception_only[(-1)].split(':', 1)
                    exception_only[-1] = self.colorize('exception', type_=type_, value=value)
        full_traceback = formatted + ''.join(exception_only)
        full_traceback = self.colorize_traceback(full_traceback)
        yield self.sanitize(full_traceback)