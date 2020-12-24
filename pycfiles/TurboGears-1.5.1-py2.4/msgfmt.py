# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\turbogears\i18n\pygettext\msgfmt.py
# Compiled at: 2011-07-14 05:59:45
"""Generate binary message catalog from textual translation description.

This program converts a textual Uniforum-style message catalog (.po file) into
a binary GNU catalog (.mo file).  This is essentially the same function as the
GNU msgfmt program, however, it is a simpler implementation.

Usage: msgfmt.py [OPTIONS] filename.po

Options:
    -o file
    --output-file=file
        Specify the output file to write to.  If omitted, output will go to a
        file named filename.mo (based off the input file name).

    -h
    --help
        Print this message and exit.

    -V
    --version
        Display version information and exit.
"""
import sys, os, getopt, struct, array
__version__ = '1.1'
MESSAGES = {}

def usage(code, msg=''):
    print >> sys.stderr, __doc__
    if msg:
        print >> sys.stderr, msg
    sys.exit(code)


def add(msgid, msgstr, fuzzy):
    """Add a non-fuzzy translation to the dictionary."""
    if not fuzzy and msgstr:
        MESSAGES[msgid] = msgstr


def generate():
    """Return the generated output."""
    keys = MESSAGES.keys()
    keys.sort()
    offsets = []
    msgids = msgstrs = ''
    for msgid in keys:
        offsets.append((len(msgids), len(msgid), len(msgstrs), len(MESSAGES[msgid])))
        msgids += msgid + '\x00'
        msgstrs += MESSAGES[msgid] + '\x00'

    keystart = 7 * 4 + 16 * len(keys)
    valuestart = keystart + len(msgids)
    koffsets = []
    voffsets = []
    for (offset1, len1, offset2, len2) in offsets:
        koffsets += [len1, offset1 + keystart]
        voffsets += [len2, offset2 + valuestart]

    offsets = koffsets + voffsets
    output = struct.pack('Iiiiiii', 2500072158, 0, len(keys), 7 * 4, 7 * 4 + len(keys) * 8, 0, 0)
    output += array.array('i', offsets).tostring()
    output += msgids
    output += msgstrs
    return output


def make(filename, outfile):
    """Generate the binary message catalog."""
    MESSAGES.clear()
    MSGID = 1
    MSGSTR = 2
    if filename.endswith('.po'):
        infile = filename
    else:
        infile = filename + '.po'
    if outfile is None:
        outfile = os.path.splitext(infile)[0] + '.mo'
    try:
        lines = open(infile).readlines()
    except IOError, msg:
        print >> sys.stderr, msg
        sys.exit(1)

    section = None
    fuzzy = 0
    lno = 0
    msgid = msgstr = ''
    for line in lines:
        lno += 1
        if line[0] == '#' and section == MSGSTR:
            add(msgid, msgstr, fuzzy)
            section = None
            fuzzy = 0
        if line[:2] == '#,' and line.find('fuzzy'):
            fuzzy = 1
        if line[0] == '#':
            continue
        if line.startswith('msgid'):
            if section == MSGSTR:
                add(msgid, msgstr, fuzzy)
            section = MSGID
            line = line[5:]
            msgid = msgstr = ''
        elif line.startswith('msgstr'):
            section = MSGSTR
            line = line[6:]
        line = line.strip()
        if not line:
            continue
        line = eval(line)
        if section == MSGID:
            msgid += line
        elif section == MSGSTR:
            msgstr += line
        else:
            print >> sys.stderr, 'Syntax error on %s:%d' % (infile, lno), 'before:'
            print >> sys.stderr, line
            sys.exit(1)

    if section == MSGSTR:
        add(msgid, msgstr, fuzzy)
    output = generate()
    try:
        open(outfile, 'wb').write(output)
    except IOError, msg:
        print >> sys.stderr, msg

    return


def main():
    try:
        (opts, args) = getopt.getopt(sys.argv[1:], 'hVo:', [
         'help', 'version', 'output-file='])
    except getopt.error, msg:
        usage(1, msg)

    outfile = None
    for (opt, arg) in opts:
        if opt in ('-h', '--help'):
            usage(0)
        elif opt in ('-V', '--version'):
            print >> sys.stderr, 'msgfmt.py', __version__
            sys.exit(0)
        elif opt in ('-o', '--output-file'):
            outfile = arg

    if not args:
        print >> sys.stderr, 'No input file given'
        print >> sys.stderr, "Try `msgfmt --help' for more information."
        return
    for filename in args:
        make(filename, outfile)

    return


if __name__ == '__main__':
    main()