# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/bauble/paths.py
# Compiled at: 2016-10-03 09:39:22
"""
Access to standard paths used by Ghini.
"""
import os, sys

def main_is_frozen():
    """
    Returns True/False if Ghini is being run from a py2exe
    executable.  This method duplicates bauble.main_is_frozen in order
    to make paths.py not depend on any other Bauble modules.
    """
    import imp
    return hasattr(sys, 'frozen') or hasattr(sys, 'importers') or imp.is_frozen('__main__')


def main_dir():
    """
    Returns the path of the bauble executable.
    """
    if main_is_frozen():
        d = os.path.dirname(sys.executable)
    else:
        d = os.path.dirname(sys.argv[0])
    if d == '':
        d = os.curdir
    return os.path.abspath(d)


def lib_dir():
    """
    Returns the path of the bauble module.
    """
    if main_is_frozen():
        d = os.path.join(main_dir(), 'bauble')
    else:
        d = os.path.dirname(__file__)
    return os.path.abspath(d)


def locale_dir():
    """
    Returns the root path of the locale files
    """
    the_installation_directory = installation_dir()
    d = os.path.join(the_installation_directory, 'share', 'locale')
    return os.path.abspath(d)


def installation_dir():
    """
    Returns the root path of the installation target
    """
    if sys.platform in ('linux4', 'linux3', 'linux2', 'darwin'):
        this_file_location = __file__.split(os.path.sep)
        try:
            index_of_lib = this_file_location.index('lib')
        except ValueError:
            index_of_lib = 0

        d = os.path.sep.join(this_file_location[:-index_of_lib - 1])
    elif sys.platform == 'win32':
        d = os.path.dirname(main_dir())
    else:
        raise NotImplementedError('This platform does not support translations: %s' % sys.platform)
    return os.path.abspath(d)


def user_dir():
    """Returns the path to where user data are saved.

    this is not the same as Application Data, for app_data is going to be
    replaced at each new installation or upgrade of the software. user_data
    is responsibility of the user and the software should use it, not
    overrule it. 

    not implemented yet. will be a configuration item.

    """
    return appdata_dir()


def appdata_dir():
    """Returns the path to where Ghini application data and settings are saved.

    """
    if sys.platform == 'win32':
        if 'APPDATA' in os.environ:
            d = os.path.join(os.environ['APPDATA'], 'Bauble')
        elif 'USERPROFILE' in os.environ:
            d = os.path.join(os.environ['USERPROFILE'], 'Application Data', 'Bauble')
        else:
            raise Exception('Could not get path for user settings: no APPDATA or USERPROFILE variable')
    elif sys.platform in ('linux4', 'linux3', 'linux2', 'darwin'):
        try:
            d = os.path.join(os.path.expanduser('~%s' % os.environ['USER']), '.bauble')
        except Exception:
            raise Exception('Could not get path for user settings: could not expand $HOME for user %(username)s' % dict(username=os.environ['USER']))

    else:
        raise Exception('Could not get path for user settings: unsupported platform')
    return os.path.abspath(d)


if __name__ == '__main__':
    print 'main: %s' % main_dir()
    print 'lib: %s' % lib_dir()
    print 'locale: %s' % locale_dir()
    print 'application: %s' % appdata_dir()
    print 'user: %s' % user_dir()