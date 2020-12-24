# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/yhat/deployment/reindenter.py
# Compiled at: 2017-04-26 17:15:42
from __future__ import print_function
import tokenize, os, shutil, sys
verbose = False
recurse = False
dryrun = False
makebackup = True

def usage(msg=None):
    if msg is None:
        msg = __doc__
    print(msg, file=sys.stderr)
    return


def errprint(*args):
    sys.stderr.write((' ').join(str(arg) for arg in args))
    sys.stderr.write('\n')


def main():
    global dryrun
    global makebackup
    global recurse
    global verbose
    import getopt
    try:
        opts, args = getopt.getopt(sys.argv[1:], 'drnvh', [
         'dryrun', 'recurse', 'nobackup', 'verbose', 'help'])
    except getopt.error as msg:
        usage(msg)
        return

    for o, a in opts:
        if o in ('-d', '--dryrun'):
            dryrun = True
        elif o in ('-r', '--recurse'):
            recurse = True
        elif o in ('-n', '--nobackup'):
            makebackup = False
        elif o in ('-v', '--verbose'):
            verbose = True
        elif o in ('-h', '--help'):
            usage()
            return

    if not args:
        r = Reindenter(sys.stdin)
        r.run()
        r.write(sys.stdout)
        return
    for arg in args:
        check(arg)


def check(file):
    if os.path.isdir(file) and not os.path.islink(file):
        if verbose:
            print('listing directory', file)
        names = os.listdir(file)
        for name in names:
            fullname = os.path.join(file, name)
            if recurse and os.path.isdir(fullname) and not os.path.islink(fullname) and not os.path.split(fullname)[1].startswith('.') or name.lower().endswith('.py'):
                check(fullname)

        return
    if verbose:
        print('checking', file, '...', end=' ')
    with open(file, 'rb') as (f):
        encoding, _ = tokenize.detect_encoding(f.readline)
    try:
        with open(file, encoding=encoding) as (f):
            r = Reindenter(f)
    except IOError as msg:
        errprint('%s: I/O Error: %s' % (file, str(msg)))
        return

    newline = r.newlines
    if isinstance(newline, tuple):
        errprint('%s: mixed newlines detected; cannot process file' % file)
        return
    else:
        if r.run():
            if verbose:
                print('changed.')
                if dryrun:
                    print('But this is a dry run, so leaving it alone.')
            if not dryrun:
                bak = file + '.bak'
                if makebackup:
                    shutil.copyfile(file, bak)
                    if verbose:
                        print('backed up', file, 'to', bak)
                with open(file, 'w', encoding=encoding, newline=newline) as (f):
                    r.write(f)
                if verbose:
                    print('wrote new', file)
            return True
        if verbose:
            print('unchanged.')
        return False


def _rstrip(line, JUNK='\n \t'):
    """Return line stripped of trailing spaces, tabs, newlines.
    Note that line.rstrip() instead also strips sundry control characters,
    but at least one known Emacs user expects to keep junk like that, not
    mentioning Barry by name or anything <wink>.
    """
    i = len(line)
    while i > 0 and line[(i - 1)] in JUNK:
        i -= 1

    return line[:i]


class Reindenter:

    def __init__(self, f):
        self.find_stmt = 1
        self.level = 0
        self.raw = f.readlines()
        self.lines = [ _rstrip(line).expandtabs() + '\n' for line in self.raw
                     ]
        self.lines.insert(0, None)
        self.index = 1
        self.stats = []
        self.newlines = f.newlines
        return

    def run(self):
        tokens = tokenize.generate_tokens(self.getline)
        for _token in tokens:
            self.tokeneater(*_token)

        lines = self.lines
        while lines and lines[(-1)] == '\n':
            lines.pop()

        stats = self.stats
        stats.append((len(lines), 0))
        have2want = {}
        after = self.after = []
        i = stats[0][0]
        after.extend(lines[1:i])
        for i in range(len(stats) - 1):
            thisstmt, thislevel = stats[i]
            nextstmt = stats[(i + 1)][0]
            have = getlspace(lines[thisstmt])
            want = thislevel * 4
            if want < 0:
                if have:
                    want = have2want.get(have, -1)
                    if want < 0:
                        for j in range(i + 1, len(stats) - 1):
                            jline, jlevel = stats[j]
                            if jlevel >= 0:
                                if have == getlspace(lines[jline]):
                                    want = jlevel * 4
                                break

                    if want < 0:
                        for j in range(i - 1, -1, -1):
                            jline, jlevel = stats[j]
                            if jlevel >= 0:
                                want = have + (getlspace(after[(jline - 1)]) - getlspace(lines[jline]))
                                break

                    if want < 0:
                        want = have
                else:
                    want = 0
            assert want >= 0
            have2want[have] = want
            diff = want - have
            if diff == 0 or have == 0:
                after.extend(lines[thisstmt:nextstmt])
            else:
                for line in lines[thisstmt:nextstmt]:
                    if diff > 0:
                        if line == '\n':
                            after.append(line)
                        else:
                            after.append(' ' * diff + line)
                    else:
                        remove = min(getlspace(line), -diff)
                        after.append(line[remove:])

        return self.raw != self.after

    def write(self, f):
        f.writelines(self.after)

    def getline(self):
        if self.index >= len(self.lines):
            line = ''
        else:
            line = self.lines[self.index]
            self.index += 1
        return line

    def tokeneater(self, type, token, slinecol, end, line, INDENT=tokenize.INDENT, DEDENT=tokenize.DEDENT, NEWLINE=tokenize.NEWLINE, COMMENT=tokenize.COMMENT, NL=tokenize.NL):
        if type == NEWLINE:
            self.find_stmt = 1
        elif type == INDENT:
            self.find_stmt = 1
            self.level += 1
        elif type == DEDENT:
            self.find_stmt = 1
            self.level -= 1
        elif type == COMMENT:
            if self.find_stmt:
                self.stats.append((slinecol[0], -1))
        elif type == NL:
            pass
        elif self.find_stmt:
            self.find_stmt = 0
            if line:
                self.stats.append((slinecol[0], self.level))


def getlspace(line):
    i, n = 0, len(line)
    while i < n and line[i] == ' ':
        i += 1

    return i


if __name__ == '__main__':
    main()