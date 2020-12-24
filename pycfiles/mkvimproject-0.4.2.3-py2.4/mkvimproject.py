# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/inquant/tools/mkvimproject/mkvimproject.py
# Compiled at: 2007-09-20 07:50:04
__author__ = 'Stefan Eletzhofer <stefan.eletzhofer@inquant.de>'
__docformat__ = 'plaintext'
__revision__ = '$Revision: 2607 $'
import sys, os, logging
LOGGER = 'autotest.seleniumrcevent'

def info(msg):
    logging.getLogger(LOGGER).info(msg)


def debug(msg):
    logging.getLogger(LOGGER).debug(msg)


def error(msg):
    logging.getLogger(LOGGER).error(msg)


VIM = ' .vim .in'
TEXTFILES = ' .rst .txt .text .diff .patch'
PYTHON = ' .py'
ZPT = ' .pt .kss .vpy .cpt .cpy .metadata .dtml'
WEB = ' .html .css .xml .xsl'
C = ' .c .cpp .h .dbg .mk .in'
OBJC = C + ' .m .nib .applescript .plist .strings'
FILTERS = {'python': VIM + TEXTFILES + PYTHON, 'plone': VIM + TEXTFILES + PYTHON + ZPT + WEB + ' .zcml', 'c': VIM + TEXTFILES + C, 'objc': VIM + TEXTFILES + OBJC, 'none': ''}

class DirEntry(object):
    __module__ = __name__

    def __init__(self, dir, pattern=[]):
        self.dir = dir
        self.pattern = filter(len, pattern)
        self.children = []
        self.files = []

    def indent(self, level):
        return ' ' * level

    def addChild(self, child):
        self.children.append(child)

    def addFile(self, fn):
        if not len(self.pattern):
            self.files.append(fn)
        else:
            (_, ext) = os.path.splitext(fn)
            if not len(ext) or ext in self.pattern:
                self.files.append(fn)

    def getFilter(self):
        if len(self.pattern):
            return (' ').join([ '*%s' % f for f in self.pattern ])
        else:
            return '*'

    def sortEntries(self):
        self.files.sort()
        self.children.sort(lambda x, y: cmp(x.dir, y.dir))

    def scan(self, path):
        (root, dirs, files) = os.walk(path).next()
        for fn in files:
            self.addFile(fn)

        for dir in dirs:
            if dir.startswith('.'):
                continue
            entry = DirEntry(dir, self.pattern)
            entry.scan(os.path.join(root, dir))
            self.addChild(entry)

        self.sortEntries()

    def write(self, f, level):
        if level == 0:
            root = os.path.abspath(self.dir)
            name = os.path.basename(root).replace(' ', '_')
        else:
            root = name = self.dir
            name.replace(' ', '_')
        print >> f, '%s%s="%s" CD=. %s filter="%s" {' % (self.indent(level), name, root, 'in.vim' in self.files and 'in="in.vim"' or '', self.getFilter())
        for child in self.children:
            child.write(f, level + 1)

        for fn in self.files:
            print >> f, '%s%s' % (self.indent(level + 1), fn)

        print >> f, '%s}' % self.indent(level)


def run(dir, outfile, pattern):
    root = DirEntry(dir, pattern=pattern.split(' '))
    root.scan(dir)
    root.write(outfile, 0)


def main():
    import optparse
    parser = optparse.OptionParser()
    parser.add_option('-d', '--dir', dest='dir', default='.', help='the directory to scan')
    parser.add_option('-o', '--out', dest='out', help='The output file')
    parser.add_option('-f', '--filter', dest='filter', action='append', help='The extensions to allow.')
    parser.add_option('-s', '--filterset', dest='filterset', action='store', help='The filterset to use: one of %s' % (',').join(FILTERS.keys()))
    (options, args) = parser.parse_args()
    outfile = sys.stdout
    if options.out:
        if not options.out.endswith('.vpj'):
            options.out = '%s.vpj' % options.out
        outfile = file(options.out, 'w')
    pattern = FILTERS['plone']
    if options.filter:
        pattern = options.filter
    if options.filterset in FILTERS.keys():
        pattern = FILTERS[options.filterset]
    run(options.dir, outfile, pattern)


if __name__ == '__main__':
    main()