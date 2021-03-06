# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /var/makina/pasteStage/pasteFunBot/Paste-1.7.2-py2.6.egg/paste/debug/doctest_webapp.py
# Compiled at: 2009-07-20 09:44:04
"""
These are functions for use when doctest-testing a document.
"""
try:
    import subprocess
except ImportError:
    from paste.util import subprocess24 as subprocess

import doctest, os, sys, shutil, re, cgi, rfc822
from cStringIO import StringIO
from paste.util import PySourceColor
here = os.path.abspath(__file__)
paste_parent = os.path.dirname(os.path.dirname(os.path.dirname(here)))

def run(command):
    data = run_raw(command)
    if data:
        print data


def run_raw(command):
    """
    Runs the string command, returns any output.
    """
    proc = subprocess.Popen(command, shell=True, stderr=subprocess.STDOUT, stdout=subprocess.PIPE, env=_make_env())
    data = proc.stdout.read()
    proc.wait()
    while data.endswith('\n') or data.endswith('\r'):
        data = data[:-1]

    if data:
        data = ('\n').join([ l for l in data.splitlines() if l ])
        return data
    else:
        return ''


def run_command(command, name, and_print=False):
    output = run_raw(command)
    data = '$ %s\n%s' % (command, output)
    show_file('shell-command', name, description='shell transcript', data=data)
    if and_print and output:
        print output


def _make_env():
    env = os.environ.copy()
    env['PATH'] = env.get('PATH', '') + ':' + os.path.join(paste_parent, 'scripts') + ':' + os.path.join(paste_parent, 'paste', '3rd-party', 'sqlobject-files', 'scripts')
    env['PYTHONPATH'] = env.get('PYTHONPATH', '') + ':' + paste_parent
    return env


def clear_dir(dir):
    """
    Clears (deletes) the given directory
    """
    shutil.rmtree(dir, True)


def ls(dir=None, recurse=False, indent=0):
    """
    Show a directory listing
    """
    dir = dir or os.getcwd()
    fns = os.listdir(dir)
    fns.sort()
    for fn in fns:
        full = os.path.join(dir, fn)
        if os.path.isdir(full):
            fn = fn + '/'
        print ' ' * indent + fn
        if os.path.isdir(full) and recurse:
            ls(dir=full, recurse=True, indent=indent + 2)


default_app = None
default_url = None

def set_default_app(app, url):
    global default_app
    global default_url
    default_app = app
    default_url = url


def resource_filename(fn):
    """
    Returns the filename of the resource -- generally in the directory
    resources/DocumentName/fn
    """
    return os.path.join(os.path.dirname(sys.testing_document_filename), 'resources', os.path.splitext(os.path.basename(sys.testing_document_filename))[0], fn)


def show(path_info, example_name):
    fn = resource_filename(example_name + '.html')
    out = StringIO()
    assert default_app is not None, 'No default_app set'
    url = default_url + path_info
    out.write('<span class="doctest-url"><a href="%s">%s</a></span><br>\n' % (
     url, url))
    out.write('<div class="doctest-example">\n')
    proc = subprocess.Popen([
     'paster', 'serve--server=console', '--no-verbose',
     '--url=' + path_info], stderr=subprocess.PIPE, stdout=subprocess.PIPE, env=_make_env())
    (stdout, errors) = proc.communicate()
    stdout = StringIO(stdout)
    headers = rfc822.Message(stdout)
    content = stdout.read()
    for (header, value) in headers.items():
        if header.lower() == 'status' and int(value.split()[0]) == 200:
            continue
        if header.lower() in ('content-type', 'content-length'):
            continue
        if header.lower() == 'set-cookie' and value.startswith('_SID_'):
            continue
        out.write('<span class="doctest-header">%s: %s</span><br>\n' % (
         header, value))

    lines = [ l for l in content.splitlines() if l.strip() ]
    for line in lines:
        out.write(line + '\n')

    if errors:
        out.write('<pre class="doctest-errors">%s</pre>' % errors)
    out.write('</div>\n')
    result = out.getvalue()
    if not os.path.exists(fn):
        f = open(fn, 'wb')
        f.write(result)
        f.close()
    else:
        f = open(fn, 'rb')
        expected = f.read()
        f.close()
        if not html_matches(expected, result):
            print 'Pages did not match.  Expected from %s:' % fn
            print '-' * 60
            print expected
            print '=' * 60
            print 'Actual output:'
            print '-' * 60
            print result
    return


def html_matches(pattern, text):
    regex = re.escape(pattern)
    regex = regex.replace('\\.\\.\\.', '.*')
    regex = re.sub('0x[0-9a-f]+', '.*', regex)
    regex = '^%s$' % regex
    return re.search(regex, text)


def convert_docstring_string(data):
    if data.startswith('\n'):
        data = data[1:]
    lines = data.splitlines()
    new_lines = []
    for line in lines:
        if line.rstrip() == '.':
            new_lines.append('')
        else:
            new_lines.append(line)

    data = ('\n').join(new_lines) + '\n'
    return data


def create_file(path, version, data):
    data = convert_docstring_string(data)
    write_data(path, data)
    show_file(path, version)


def append_to_file(path, version, data):
    data = convert_docstring_string(data)
    f = open(path, 'a')
    f.write(data)
    f.close()
    if path.endswith('.py'):
        pyc_file = path + 'c'
        if os.path.exists(pyc_file):
            os.unlink(pyc_file)
    show_file(path, version, description='added to %s' % path, data=data)


def show_file(path, version, description=None, data=None):
    ext = os.path.splitext(path)[1]
    if data is None:
        f = open(path, 'rb')
        data = f.read()
        f.close()
    if ext == '.py':
        html = '<div class="source-code">%s</div>' % PySourceColor.str2html(data, PySourceColor.dark)
    else:
        html = '<pre class="source-code">%s</pre>' % cgi.escape(data, 1)
    html = '<span class="source-filename">%s</span><br>%s' % (
     description or path, html)
    write_data(resource_filename('%s.%s.gen.html' % (path, version)), html)
    return


def call_source_highlight(input, format):
    proc = subprocess.Popen(['source-highlight', '--out-format=html',
     '--no-doc', '--css=none',
     '--src-lang=%s' % format], shell=False, stdout=subprocess.PIPE)
    (stdout, stderr) = proc.communicate(input)
    result = stdout
    proc.wait()
    return result


def write_data(path, data):
    dir = os.path.dirname(os.path.abspath(path))
    if not os.path.exists(dir):
        os.makedirs(dir)
    f = open(path, 'wb')
    f.write(data)
    f.close()


def change_file(path, changes):
    f = open(os.path.abspath(path), 'rb')
    lines = f.readlines()
    f.close()
    for (change_type, line, text) in changes:
        if change_type == 'insert':
            lines[line:line] = [
             text]
        elif change_type == 'delete':
            lines[line:text] = []
        else:
            assert 0, 'Unknown change_type: %r' % change_type

    f = open(path, 'wb')
    f.write(('').join(lines))
    f.close()


class LongFormDocTestParser(doctest.DocTestParser):
    """
    This parser recognizes some reST comments as commands, without
    prompts or expected output, like:

    .. run:

        do_this(...
        ...)
    """
    _EXAMPLE_RE = re.compile("\n        # Source consists of a PS1 line followed by zero or more PS2 lines.\n        (?: (?P<source>\n                (?:^(?P<indent> [ ]*) >>>    .*)    # PS1 line\n                (?:\\n           [ ]*  \\.\\.\\. .*)*)  # PS2 lines\n            \\n?\n            # Want consists of any non-blank lines that do not start with PS1.\n            (?P<want> (?:(?![ ]*$)    # Not a blank line\n                         (?![ ]*>>>)  # Not a line starting with PS1\n                         .*$\\n?       # But any other line\n                      )*))\n        | \n        (?: # This is for longer commands that are prefixed with a reST\n            # comment like '.. run:' (two colons makes that a directive).\n            # These commands cannot have any output.\n\n            (?:^\\.\\.[ ]*(?P<run>run):[ ]*\\n) # Leading command/command\n            (?:[ ]*\\n)?         # Blank line following\n            (?P<runsource>\n                (?:(?P<runindent> [ ]+)[^ ].*$)\n                (?:\\n [ ]+ .*)*)\n            )\n        |\n        (?: # This is for shell commands\n\n            (?P<shellsource>\n                (?:^(P<shellindent> [ ]*) [$] .*)   # Shell line\n                (?:\\n               [ ]*  [>] .*)*) # Continuation\n            \\n?\n            # Want consists of any non-blank lines that do not start with $\n            (?P<shellwant> (?:(?![ ]*$)\n                              (?![ ]*[$]$)\n                              .*$\\n?\n                           )*))\n        ", re.MULTILINE | re.VERBOSE)

    def _parse_example(self, m, name, lineno):
        r"""
        Given a regular expression match from `_EXAMPLE_RE` (`m`),
        return a pair `(source, want)`, where `source` is the matched
        example's source code (with prompts and indentation stripped);
        and `want` is the example's expected output (with indentation
        stripped).

        `name` is the string's name, and `lineno` is the line number
        where the example starts; both are used for error messages.

        >>> def parseit(s):
        ...     p = LongFormDocTestParser()
        ...     return p._parse_example(p._EXAMPLE_RE.search(s), '<string>', 1)
        >>> parseit('>>> 1\n1')
        ('1', {}, '1', None)
        >>> parseit('>>> (1\n... +1)\n2')
        ('(1\n+1)', {}, '2', None)
        >>> parseit('.. run:\n\n    test1\n    test2\n')
        ('test1\ntest2', {}, '', None)
        """
        runner = m.group('run') or ''
        indent = len(m.group('%sindent' % runner))
        source_lines = m.group('%ssource' % runner).split('\n')
        if runner:
            self._check_prefix(source_lines[1:], ' ' * indent, name, lineno)
        else:
            self._check_prompt_blank(source_lines, indent, name, lineno)
            self._check_prefix(source_lines[2:], ' ' * indent + '.', name, lineno)
        if runner:
            source = ('\n').join([ sl[indent:] for sl in source_lines ])
        else:
            source = ('\n').join([ sl[indent + 4:] for sl in source_lines ])
        if runner:
            want = ''
            exc_msg = None
        else:
            want = m.group('want')
            want_lines = want.split('\n')
            if len(want_lines) > 1 and re.match(' *$', want_lines[(-1)]):
                del want_lines[-1]
            self._check_prefix(want_lines, ' ' * indent, name, lineno + len(source_lines))
            want = ('\n').join([ wl[indent:] for wl in want_lines ])
            m = self._EXCEPTION_RE.match(want)
            if m:
                exc_msg = m.group('msg')
            else:
                exc_msg = None
        options = self._find_options(source, name, lineno)
        return (
         source, options, want, exc_msg)

    def parse(self, string, name='<string>'):
        """
        Divide the given string into examples and intervening text,
        and return them as a list of alternating Examples and strings.
        Line numbers for the Examples are 0-based.  The optional
        argument `name` is a name identifying this string, and is only
        used for error messages.
        """
        string = string.expandtabs()
        min_indent = self._min_indent(string)
        if min_indent > 0:
            string = ('\n').join([ l[min_indent:] for l in string.split('\n') ])
        output = []
        (charno, lineno) = (0, 0)
        for m in self._EXAMPLE_RE.finditer(string):
            output.append(string[charno:m.start()])
            lineno += string.count('\n', charno, m.start())
            (source, options, want, exc_msg) = self._parse_example(m, name, lineno)
            if not self._IS_BLANK_OR_COMMENT(source):
                output.append(doctest.Example(source, want, exc_msg, lineno=lineno, indent=min_indent + len(m.group('indent') or m.group('runindent')), options=options))
            lineno += string.count('\n', m.start(), m.end())
            charno = m.end()

        output.append(string[charno:])
        return output


if __name__ == '__main__':
    if sys.argv[1:] and sys.argv[1] == 'doctest':
        doctest.testmod()
        sys.exit()
    if paste_parent not in sys.path:
        sys.path.append(paste_parent)
    for fn in sys.argv[1:]:
        fn = os.path.abspath(fn)
        sys.testing_document_filename = fn
        doctest.testfile(fn, module_relative=False, optionflags=doctest.ELLIPSIS | doctest.REPORT_ONLY_FIRST_FAILURE, parser=LongFormDocTestParser())
        new = os.path.splitext(fn)[0] + '.html'
        assert new != fn
        os.system('rst2html.py %s > %s' % (fn, new))