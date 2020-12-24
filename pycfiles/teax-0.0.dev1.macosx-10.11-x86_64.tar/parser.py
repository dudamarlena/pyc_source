# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/site-packages/teax/system/parser.py
# Compiled at: 2016-02-03 14:17:50
import re, collections

class Message(collections.namedtuple('Message', 'typ filename lineno msg')):

    def emit(self):
        if self.filename:
            if self.filename.startswith('./'):
                finfo = self.filename[2:]
            else:
                finfo = self.filename
        else:
            finfo = '<no file>'
        if self.lineno is not None:
            finfo += ':' + str(self.lineno)
        finfo += ': '
        if self._color:
            terminfo.send('bold')
        sys.stdout.write(finfo)
        if self.typ != 'info':
            if self._color:
                terminfo.send(('setaf', 5 if self.typ == 'warning' else 1))
            sys.stdout.write(self.typ + ': ')
        if self._color:
            terminfo.send('sgr0')
        sys.stdout.write(self.msg + '\n')
        return


class LaTeXFilter:
    TRACE = False

    def __init__(self, nowarns=[]):
        self.__data = ''
        self.__restart_pos = 0
        self.__restart_file_stack = []
        self.__restart_messages_len = 0
        self.__messages = []
        self.__first_file = None
        self.__fatal_error = False
        self.__missing_includes = False
        self.__pageno = 1
        self.__restart_pageno = 1
        self.__suppress = {cls:0 for cls in nowarns}
        return

    def feed(self, data, eof=False):
        """Feed LaTeX log data to the parser.
        The log data can be from LaTeX's standard output, or from the
        log file.  If there will be no more data, set eof to True.
        """
        self.__data += data
        self.__data_complete = eof
        self.__pos = self.__restart_pos
        self.__file_stack = self.__restart_file_stack
        self.__messages = self.__messages[:self.__restart_messages_len]
        self.__lstart = self.__lend = -1
        self.__pageno = self.__restart_pageno
        while self.__pos < len(self.__data):
            self.__noise()

        if eof:
            msgs = [ '%d %s warning%s' % (count, cls, 's' if count > 1 else '') for cls, count in self.__suppress.items() if count ]
            if msgs:
                self.__message('info', None, '%s not shown (use -Wall to show them)' % (', ').join(msgs), filename=self.__first_file)
        if eof and len(self.__file_stack) and not self.__fatal_error:
            self.__message('warning', None, "unbalanced `(' in log; file names may be wrong")
        return self

    def get_messages(self):
        """Return a list of warning and error Messages."""
        return self.__messages

    def get_file_stack(self):
        """Return the file stack for the data that has been parsed.
        This results a list from outermost file to innermost file.
        The list may be empty.
        """
        return self.__file_stack

    def has_missing_includes(self):
        r"""Return True if the log reported missing \include files."""
        return self.__missing_includes

    def __save_restart_point(self):
        """Save the current state as a known-good restart point.
        On the next call to feed, the parser will reset to this point.
        """
        self.__restart_pos = self.__pos
        self.__restart_file_stack = self.__file_stack
        self.__restart_messages_len = len(self.__messages)
        self.__restart_pageno = self.__pageno

    def __message(self, typ, lineno, msg, cls=None, filename=None):
        if cls is not None and cls in self.__suppress:
            self.__suppress[cls] += 1
            return
        else:
            filename = filename or (self.__file_stack[(-1)] if self.__file_stack else self.__first_file)
            self.__messages.append(Message(typ, filename, lineno, msg))
            return

    def __ensure_line(self):
        """Update lstart and lend."""
        if self.__lstart <= self.__pos < self.__lend:
            return
        self.__lstart = self.__data.rfind('\n', 0, self.__pos) + 1
        self.__lend = self.__data.find('\n', self.__pos) + 1
        if self.__lend == 0:
            self.__lend = len(self.__data)

    @property
    def __col(self):
        """The 0-based column number of __pos."""
        self.__ensure_line()
        return self.__pos - self.__lstart

    @property
    def __avail(self):
        return self.__pos < len(self.__data)

    def __lookingat(self, needle):
        return self.__data.startswith(needle, self.__pos)

    def __lookingatre(self, regexp, flags=0):
        return re.compile(regexp, flags=flags).match(self.__data, self.__pos)

    def __skip_line(self):
        self.__ensure_line()
        self.__pos = self.__lend

    def __consume_line(self, unwrap=False):
        self.__ensure_line()
        data = self.__data[self.__pos:self.__lend]
        self.__pos = self.__lend
        if unwrap:
            while self.__lend - self.__lstart >= 80:
                if self.TRACE:
                    print ('<{}> wrapping').format(self.__pos)
                self.__ensure_line()
                data = data[:-1] + self.__data[self.__pos:self.__lend]
                self.__pos = self.__lend

        return data

    def __noise(self):
        lookingat, lookingatre = self.__lookingat, self.__lookingatre
        if self.__col == 0:
            if lookingat('! '):
                return self.__errmessage()
            if lookingat('!pdfTeX error: '):
                return self.__pdftex_fail()
            if lookingat('Runaway '):
                return self.__runaway()
            if lookingatre('(Overfull|Underfull|Loose|Tight) \\\\[hv]box \\('):
                return self.__bad_box()
            if lookingatre('(Package |Class |LaTeX |pdfTeX )?(\\w+ )?warning: ', re.I):
                return self.__generic_warning()
            if lookingatre('No file .*\\.tex\\.$', re.M):
                self.__message('warning', None, self.__simplify_message(self.__consume_line(unwrap=True).strip()))
                self.__missing_includes = True
                return
            if lookingatre('(Package|Class|LaTeX) (\\w+ )?info: ', re.I):
                return self.__generic_info()
            if lookingatre('(Document Class|File|Package): '):
                return self.__consume_line(unwrap=True)
            if lookingatre('\\\\\\w+=\\\\[a-z]+\\d+\\n'):
                return self.__consume_line(unwrap=True)
        m = re.compile('[(){}\\n]|(?<=[\\n ])\\[\\d+', re.M).search(self.__data, self.__pos)
        if m is None:
            self.__pos = len(self.__data)
            return
        else:
            self.__pos = m.start() + 1
            ch = self.__data[m.start()]
            if ch == '\n':
                self.__save_restart_point()
            elif ch == '[':
                self.__pageno = int(self.__lookingatre('\\d+').group(0)) + 1
            else:
                if (self.__data.startswith('`', m.start() - 1) or self.__data.startswith('`\\', m.start() - 2)) and self.__data.startswith("'", m.start() + 1):
                    return
                if ch == '(':
                    first = self.__first_file is None and self.__col == 1
                    filename = self.__filename()
                    self.__file_stack.append(filename)
                    if first:
                        self.__first_file = filename
                    if self.TRACE:
                        print ('<{}>{}enter {}').format(m.start(), ' ' * len(self.__file_stack), filename)
                elif ch == ')':
                    if len(self.__file_stack):
                        if self.TRACE:
                            print ('<{}>{}exit {}').format(m.start(), ' ' * len(self.__file_stack), self.__file_stack[(-1)])
                        self.__file_stack.pop()
                    else:
                        self.__message('warning', None, "extra `)' in log; file names may be wrong ")
                elif ch == '{':
                    epos = self.__data.find('}', self.__pos)
                    if epos != -1:
                        self.__pos = epos + 1
                    else:
                        self.__message('warning', None, "unbalanced `{' in log; file names may be wrong")
                elif ch == '}':
                    self.__message('warning', None, "extra `}' in log; file names may be wrong")
            return

    def __filename(self):
        initcol = self.__col
        first = True
        name = ''
        while first or initcol == 1 and self.__lookingat('\n') and self.__col >= 79:
            if not first:
                self.__pos += 1
            m = self.__lookingatre('[^(){} \\n]*')
            name += m.group()
            self.__pos = m.end()
            first = False

        return name

    def __simplify_message(self, msg):
        msg = re.sub('^(?:Package |Class |LaTeX |pdfTeX )?([^ ]+) (?:Error|Warning): ', '[\\1] ', msg, flags=re.I)
        msg = re.sub('\\.$', '', msg)
        msg = re.sub('has occurred (while \\\\output is active)', '\\1', msg)
        return msg

    def __errmessage(self):
        msg = self.__consume_line(unwrap=True)[1:].strip()
        is_fatal_error = msg == 'Emergency stop.'
        msg = self.__simplify_message(msg)
        lineno = None
        found_context = False
        stack = []
        while self.__avail:
            m1 = self.__lookingatre('<([a-z ]+|\\*|read [^ >]*)> |\\\\.*(->|...)')
            m2 = self.__lookingatre('l\\.[0-9]+ ')
            if m1:
                found_context = True
                pre = self.__consume_line().rstrip('\n')
                stack.append(pre)
            elif m2:
                found_context = True
                pre = self.__consume_line().rstrip('\n')
                info, rest = pre.split(' ', 1)
                lineno = int(info[2:])
                stack.append(rest)
            elif found_context:
                break
            if found_context:
                post = self.__consume_line().rstrip('\n')
                post = re.sub('\\^\\^M$', '', post)
                if post[:len(pre)].isspace() and not post.isspace():
                    stack.append(len(stack[(-1)]))
                    stack[(-2)] += post[len(pre):]
            else:
                self.__skip_line()

        stack_msg = ''
        for i, trace in enumerate(stack):
            stack_msg += '\n         ' + ' ' * trace + '^' if isinstance(trace, int) else '\n      at ' + trace.rstrip() if i == 0 else '\n    from ' + trace.rstrip()

        if is_fatal_error:
            info = self.__consume_line().strip()
            if info.startswith('*** '):
                info = info[4:]
            msg += ': ' + info.lstrip('(').rstrip(')')
        self.__message('error', lineno, msg + stack_msg)
        self.__fatal_error = True
        return

    def __pdftex_fail(self):
        msg = self.__consume_line(unwrap=True)[1:].strip()
        msg = self.__simplify_message(msg)
        self.__message('error', None, msg)
        return

    def __runaway(self):
        self.__skip_line()
        if not self.__lookingat('! ') and self.__avail:
            self.__skip_line()

    def __bad_box(self):
        origpos = self.__pos
        msg = self.__consume_line()
        m = re.search(' in (?:paragraph|alignment) at lines ([0-9]+)--([0-9]+)', msg) or re.search(' detected at line ([0-9]+)', msg)
        if m:
            lineno = min(int(m.group(1)), int(m.groups()[(-1)]))
            msg = msg[:m.start()]
        else:
            m = re.search(' while \\\\output is active', msg)
            if m:
                lineno = None
                msg = msg[:m.end()]
            else:
                self.__message('warning', None, 'malformed bad box message in log')
                return
        self.__pos = origpos + m.end()
        if self.__lookingat('\n'):
            self.__pos += 1
            if 'hbox' in msg and self.__lookingat('\\'):
                self.__consume_line(unwrap=True)
        msg = self.__simplify_message(msg) + (' (page {})').format(self.__pageno)
        cls = msg.split(None, 1)[0].lower()
        self.__message('warning', lineno, msg, cls=cls)
        return

    def __generic_warning(self):
        msg, cls = self.__generic_info()
        m = re.search(' on input line ([0-9]+)', msg)
        if m:
            lineno = int(m.group(1))
            msg = msg[:m.start()]
        else:
            lineno = None
        msg = self.__simplify_message(msg)
        self.__message('warning', lineno, msg, cls=cls)
        return

    def __generic_info(self):
        msg = self.__consume_line(unwrap=True).strip()
        pkg_name = msg.split(' ', 2)[1]
        prefix = '(' + pkg_name + ')            '
        while self.__lookingat(prefix):
            extra = self.__consume_line(unwrap=True)
            msg += ' ' + extra[len(prefix):].strip()

        return (
         msg, pkg_name.lower())