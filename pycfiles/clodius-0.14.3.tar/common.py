# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/MyKings/Documents/github/clocwalk/clocwalk/libs/core/common.py
# Compiled at: 2019-12-11 02:42:48
import os, re, sys, inspect, fnmatch, glob
from clocwalk.libs.core.log import LOGGER_HANDLER
from clocwalk.libs.core.settings import BANNER

def banner():
    _ = BANNER
    if not getattr(LOGGER_HANDLER, 'is_tty', False):
        _ = re.sub('\x1b.+?m', '', _)
    print _


def modulePath():
    """
    This will get us the program's directory, even if we are frozen
    using py2exe
    """
    try:
        _ = sys.executable if weAreFrozen() else __file__
    except NameError:
        _ = inspect.getsourcefile(modulePath)

    return os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(_))))


def weAreFrozen():
    """
    Returns whether we are frozen via py2exe.
    This will affect how we find out where we are located.
    Reference: http://www.py2exe.org/index.cgi/WhereAmI
    """
    return hasattr(sys, 'frozen')


def recursive_search_files(search_dir, file_info):
    """

    :param search_dir: /etc/nginx
    :param file_info: *.conf
    :return:
    """
    file_list = []
    for p in glob.glob(os.path.join(search_dir, '*')):
        if fnmatch.fnmatch(p, file_info):
            file_list.append(p)
        elif os.path.isdir(p):
            file_list.extend(recursive_search_files(p, file_info))

    return file_list