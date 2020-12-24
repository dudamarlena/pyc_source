# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\pycoon\__init__.py
# Compiled at: 2007-04-12 06:41:13
"""
Pycoon Web Development Framework.
Copyright (C) 2006/2007 Andrey Nordin, Richard Lewis

This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 2 of the License, or
(at your option) any later version.

See also:

 - Pycoon Subversion repository <U{http://pycoon.googlecode.com/svn/}>
 - Pycoon Project website <U{http://code.google.com/p/pycoon/}>
 - Pycoon at Cheese Shop <U{http://cheeseshop.python.org/pypi/pycoon/}>
"""
__license__ = 'Pycoon Web Development Framework\nCopyright (C) 2006/2007 Andrey Nordin, Richard Lewis\n\nThis program is free software; you can redistribute it and/or modify\nit under the terms of the GNU General Public License as published by\nthe Free Software Foundation; either version 2 of the License, or\n(at your option) any later version.\n\nThis program is distributed in the hope that it will be useful,\nbut WITHOUT ANY WARRANTY; without even the implied warranty of\nMERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the\nGNU General Public License for more details.\n\nYou should have received a copy of the GNU General Public License along\nwith this program; if not, write to the Free Software Foundation, Inc.,\n51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.'
__author__ = 'Andrey Nordin <http://claimid.com/anrienord>'
__version__ = '0.2a5'
usage = 'Pycoon Web Development Framework\nCopyright (C) 2006/2007 Andrey Nordin, Richard Lewis\nThis is free software, and you are welcome to redistribute it under certain\nconditions; use --license option for details.\n\nUsage: pycoon <options>\n\nOptions:\n    -s, --serve <srv>   , where srv is:\n    \n        cherrypy <host> <port> [<pycoon.xconf absolute file URI>]\n                        run Pycoon in CherryPy WSGI server\n    \n    --help              print help message\n    --license           print legal info'
ns = {'map': 'http://apache.org/cocoon/sitemap/1.0', 'py': 'http://pycoon.org/ns/pysitemap/0.1/'}

class ResourceNotFoundException(Exception):
    __module__ = __name__


class SitemapException(Exception):
    __module__ = __name__


def synchronized(func):
    """A Python decorator for synchronizing method calls.
    
    Adds an extra L{threading.RLock} attribute named C{_lock} to the
    dictionary of the object which method is decorated.
    
    @param func: a method to be synchronized.
    """

    def decorator(self, *args, **kwargs):
        try:
            rlock = self._lock
        except AttributeError:
            from threading import RLock
            rlock = self.__dict__.setdefault('_lock', RLock())

        rlock.acquire()
        try:
            return func(self, *args, **kwargs)
        finally:
            rlock.release()

    return decorator


def main():
    """The Pycoon command-line interface entry point."""
    import sys, getopt
    try:
        (opts, args) = getopt.getopt(sys.argv[1:], 's:', ['help', 'license', 'serve='])
        for (opt, arg) in opts:
            if opt == '--help':
                print usage
                sys.exit(0)
            elif opt == '--license':
                print __license__
                sys.exit(0)
            elif opt in ('-s', '--serve'):
                if arg == 'cherrypy':
                    from pycoon.wsgi.frontend import cherrypyserver
                    cherrypyserver.main(*args)
                    sys.exit(0)
                else:
                    raise getopt.GetoptError('')
            else:
                raise getopt.GetoptError('')

        print usage
        sys.exit(1)
    except getopt.GetoptError:
        print 'Wrong command line options, use --help'
        sys.exit(1)


if __name__ == '__main__':
    main()