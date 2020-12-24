# uncompyle6 version 3.7.4
# Python bytecode 2.3 (62011)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/kid/run.py
# Compiled at: 2007-07-16 07:02:52
"""Usage: kid [options] file [args]
Expand a Kid template file.

OPTIONS:

  -e enc, --encoding=enc
          Specify the output character encoding.
          Default: utf-8
  -o outfile, --output=outfile
          Specify the output file.
          Default: standard output
  -s host:port, --server=host:port
          Specify the server address if
          you want to start the HTTP server.
          Instead of the Kid template,
          you can specify a base directory.
  -h, --help
          Print this help message and exit.
  -V, --version
          Print the Kid version number and exit.

file:
  filename of the Kid template to be processed
  or "-" for reading the template from stdin.

args:
  key=value or other arguments passed to the template.
"""
__revision__ = '$Rev: 492 $'
__date__ = '$Date: 2007-07-06 21:38:45 -0400 (Fri, 06 Jul 2007) $'
__author__ = 'Ryan Tomayko (rtomayko@gmail.com)'
__copyright__ = 'Copyright 2004-2005, Ryan Tomayko'
__license__ = 'MIT <http://www.opensource.org/licenses/mit-license.php>'
import sys
from os.path import dirname, abspath
from getopt import getopt, GetoptError as gerror
try:
    from os import EX_OK, EX_DATAERR, EX_USAGE
except ImportError:
    (EX_OK, EX_DATAERR, EX_USAGE) = (
     0, 1, 2)

import kid

def main():
    try:
        (opts, args) = getopt(sys.argv[1:], 'e:o:s:hV', [
         'encoding=', 'output=', 'server=', 'help', 'version'])
    except gerror, e:
        sys.stderr.write(str(e) + '\n')
        sys.stdout.write(__doc__)
        sys.exit(EX_USAGE)

    enc = 'utf-8'
    outfile = server = None
    for (o, a) in opts:
        if o in ('-e', '--encoding'):
            enc = a
        elif o in ('-o', '--output'):
            outfile = a
        elif o in ('-s', '--server'):
            server = a
        elif o in ('-h', '--help'):
            sys.stdout.write(__doc__)
            sys.exit(EX_OK)
        elif o in ('-V', '--version'):
            from kid import __version__
            sys.stdout.write('Kid %s\n' % __version__)
            sys.exit(EX_OK)

    if server is None:
        if args:
            f = args.pop(0)
            sys.argv = [f]
            if f != '-':
                path = abspath(dirname(f))
                if not path in sys.path:
                    sys.path.insert(0, path)
            else:
                f = sys.stdin.read()
            kw = {}
            while args:
                a = args.pop(0).split('=', 1)
                if len(a) > 1:
                    kw[a[0]] = a[1]
                else:
                    sys.argv.append(a[0])

            sys.modules['__kid_main__'] = sys.modules['__main__']
            __name__ = '__kid_main__'
            del sys.modules['__main__']
            module = kid.load_template(f, name='__main__', cache=False)
            if not outfile:
                outfile = sys.stdout
            module.write(outfile, encoding=enc, **kw)
        else:
            sys.stderr.write('kid: No template file specified.\n')
            sys.stderr.write("     Try 'kid --help' for usage information.\n")
            sys.exit(EX_USAGE)
    elif len(args) < 2:
        if outfile:
            stderr = file(outfile, 'a', 1)
            sys.stderr = stderr
        sys.stdout.write('Starting HTTP server ...\n')
        if args:
            basedir = args.pop(0)
            from os import chdir
            chdir(basedir)
        from os import getcwd
        basedir = getcwd()
        sys.stdout.write('Base directory: %s\n' % basedir)
        if outfile:
            sys.stdout.write('Server log: %s\n' % outfile)
        if server == '-':
            server = 'localhost'
        sys.argv[1:] = [
         server]
        from kid.server import main
        main()
        if outfile:
            sys.stderr = sys.__stderr__
            stderr.close()
    else:
        sys.stderr.write('kid: Server does not need additional arguments.\n')
        sys.stderr.write("     Try 'kid --help' for usage information.\n")
        sys.exit(EX_USAGE)
    return


if __name__ == '__main__':
    main()