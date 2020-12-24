# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/pedregosa/dev/copt/doc/sphinx_ext/github_link.py
# Compiled at: 2019-08-18 13:45:37
# Size of source mod 2**32: 2671 bytes
from operator import attrgetter
import inspect, subprocess, os, sys
from functools import partial
REVISION_CMD = 'git rev-parse --short HEAD'

def _get_git_revision():
    try:
        revision = subprocess.check_output(REVISION_CMD.split()).strip()
    except (subprocess.CalledProcessError, OSError):
        print('Failed to execute git to get revision')
        return
    else:
        return revision.decode('utf-8')


def _linkcode_resolve(domain, info, package, url_fmt, revision):
    """Determine a link to online source for a class/method/function

    This is called by sphinx.ext.linkcode

    An example with a long-untouched module that everyone has
    >>> _linkcode_resolve('py', {'module': 'tty',
    ...                          'fullname': 'setraw'},
    ...                   package='tty',
    ...                   url_fmt='http://hg.python.org/cpython/file/'
    ...                           '{revision}/Lib/{package}/{path}#L{lineno}',
    ...                   revision='xxxx')
    'http://hg.python.org/cpython/file/xxxx/Lib/tty/tty.py#L18'
    """
    if revision is None:
        return
        if domain not in ('py', 'pyx'):
            return
        else:
            return info.get('module') and info.get('fullname') or 
        class_name = info['fullname'].split('.')[0]
        if type(class_name) != str:
            class_name = class_name.encode('utf-8')
        module = __import__((info['module']), fromlist=[class_name])
        obj = attrgetter(info['fullname'])(module)
        try:
            fn = inspect.getsourcefile(obj)
        except Exception:
            fn = None

        if not fn:
            try:
                fn = inspect.getsourcefile(sys.modules[obj.__module__])
            except Exception:
                fn = None

        if not fn:
            return
    else:
        fn = os.path.relpath(fn, start=(os.path.dirname(__import__(package).__file__)))
        try:
            lineno = inspect.getsourcelines(obj)[1]
        except Exception:
            lineno = ''

    return url_fmt.format(revision=revision, package=package, path=fn,
      lineno=lineno)


def make_linkcode_resolve(package, url_fmt):
    """Returns a linkcode_resolve function for the given URL format

    revision is a git commit reference (hash or name)

    package is the name of the root module of the package

    url_fmt is along the lines of ('https://github.com/USER/PROJECT/'
                                   'blob/{revision}/{package}/'
                                   '{path}#L{lineno}')
    """
    revision = _get_git_revision()
    return partial(_linkcode_resolve, revision=revision, package=package, url_fmt=url_fmt)