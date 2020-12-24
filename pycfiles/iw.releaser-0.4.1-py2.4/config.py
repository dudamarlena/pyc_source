# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-fat/egg/iw/releaser/config.py
# Compiled at: 2008-04-29 08:14:25
import os
from StringIO import StringIO
from zc.buildout.buildout import _open
from zc.buildout.buildout import _update

def get_config():
    """
    >>> 'pypi' in get_config()
    True
    """
    home = os.path.expanduser('~')
    files = [(home, 'pypirc'), (home, '.pypirc'), (home, 'iw-releaser.cfg'), (os.getcwd(), 'setup.cfg')]
    seen = []
    result = dict()
    for args in files:
        if os.path.isfile(os.path.join(*args)):
            args += ([],)
            result = _update(_open(*args), result)

    return result


_marker = object()

def get_option(section, option, default=_marker):
    """
    >>> print get_option('pypi', 'username')
    ingeniweb
    """
    section = get_section(section)
    try:
        return section[option]
    except KeyError, e:
        if default is _marker:
            raise
        else:
            return default


def get_section(section):
    config = get_config()
    return config[section]


def get_sections():
    """
    >>> len(get_sections()) > 0
    True
    """
    config = get_config()
    return config.keys()


def get_options(section):
    """
    >>> len(get_options('pypi')) > 0
    True
    """
    section = get_section(section)
    return section.keys()


if __name__ == '__main__':
    import doctest
    doctest.testmod()