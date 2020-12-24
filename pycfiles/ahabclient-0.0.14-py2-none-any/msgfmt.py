# uncompyle6 version 3.6.7
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/aha/i18n/msgfmt.py
# Compiled at: 2010-10-20 22:45:45
__doc__ = 'Generate binary message catalog from textual translation description.\n\nThis program converts a textual Uniforum-style message catalog (.po file) into\na binary GNU catalog (.mo file).  This is essentially the same function as the\nGNU msgfmt program, however, it is a simpler implementation.\n\nUsage: msgfmt.py [OPTIONS] filename.po\n\nOptions:\n    -o file\n    --output-file = file\n        Specify the output file to write to.  If omitted, output will go to a\n        file named filename.mo (based off the input file name).\n\n    -h\n    --help\n        Print this message and exit.\n\n    -V\n    --version\n        Display version information and exit.\n'
import sys, os, getopt, struct, array
__version__ = '1.1'
MESSAGES = {}

def usage(code, msg=''):
    print >> sys.stderr, __doc__
    if msg:
        print >> sys.stderr, msg
    sys.exit(code)


def add(id, str, fuzzy):
    """Add a non-fuzzy translation to the dictionary."""
    global MESSAGES
    if not fuzzy and str:
        MESSAGES[id] = str


def generate():
    """Return the generated output."""
    keys = MESSAGES.keys()
    keys.sort()
    offsets = []
    ids = strs = ''
    for id in keys:
        offsets.append((len(ids), len(id), len(strs), len(MESSAGES[id])))
        ids += id + '\x00'
        strs += MESSAGES[id] + '\x00'

    output = ''
    keystart = 28 + 16 * len(keys)
    valuestart = keystart + len(ids)
    koffsets = []
    voffsets = []
    for (o1, l1, o2, l2) in offsets:
        koffsets += [l1, o1 + keystart]
        voffsets += [l2, o2 + valuestart]

    offsets = koffsets + voffsets
    output = struct.pack('Iiiiiii', 2500072158, 0, len(keys), 28, 28 + len(keys) * 8, 0, 0)
    output += array.array('i', offsets).tostring()
    output += ids
    output += strs
    return output


def make(filename, outfile):
    ID = 1
    STR = 2
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
    for l in lines:
        lno += 1
        if l[0] == '#' and section == STR:
            add(msgid, msgstr, fuzzy)
            section = None
            fuzzy = 0
        if l[:2] == '#,' and 'fuzzy' in l:
            fuzzy = 1
        if l[0] == '#':
            continue
        if l.startswith('msgid'):
            if section == STR:
                add(msgid, msgstr, fuzzy)
            section = ID
            l = l[5:]
            msgid = msgstr = ''
        elif l.startswith('msgstr'):
            section = STR
            l = l[6:]
        l = l.strip()
        if not l:
            continue
        l = eval(l)
        if section == ID:
            msgid += l
        elif section == STR:
            msgstr += l
        else:
            print >> sys.stderr, 'Syntax error on %s:%d' % (infile, lno), 'before:'
            print >> sys.stderr, l
            sys.exit(1)

    if section == STR:
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
         'help', 'version', 'output-file = '])
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