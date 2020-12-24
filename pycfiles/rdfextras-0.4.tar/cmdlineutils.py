# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/grimnes/projects/rdflib/rdfextras/rdfextras/utils/cmdlineutils.py
# Compiled at: 2012-10-05 10:22:19
import sys, time, getopt, rdflib, codecs
from rdfextras.utils.pathutils import guess_format

def _help():
    sys.stderr.write('\nprogram.py [-f <format>] [-o <output>] [files...]\nRead RDF files given on STDOUT - does something to the resulting graph\nIf no files are given, read from stdin\n-o specifies file for output, if not given stdout is used\n-f specifies parser to use, if not given it is guessed from extension\n\n')


def main(target, _help=_help, options='', stdin=True):
    """
    A main function for tools that read RDF from files given on commandline
    or from STDIN (if stdin parameter is true)
    """
    args, files = getopt.getopt(sys.argv[1:], 'hf:o:' + options)
    dargs = dict(args)
    if '-h' in dargs:
        _help()
        sys.exit(-1)
    g = rdflib.Graph()
    if '-f' in dargs:
        f = dargs['-f']
    else:
        f = None
    if '-o' in dargs:
        sys.stderr.write('Output to %s\n' % dargs['-o'])
        out = codecs.open(dargs['-o'], 'w', 'utf-8')
    else:
        out = sys.stdout
    start = time.time()
    if len(files) == 0 and stdin:
        sys.stderr.write('Reading from stdin as %s...' % f)
        g.load(sys.stdin, format=f)
        sys.stderr.write('[done]\n')
    else:
        size = 0
        for x in files:
            if f == None:
                f = guess_format(x)
            start1 = time.time()
            sys.stderr.write('Loading %s as %s... ' % (x, f))
            g.load(x, format=f)
            sys.stderr.write('done.\t(%d triples\t%.2f seconds)\n' % (len(g) - size, time.time() - start1))
            size = len(g)

    sys.stderr.write('Loaded a total of %d triples in %.2f seconds.\n' % (len(g), time.time() - start))
    target(g, out, args)
    return