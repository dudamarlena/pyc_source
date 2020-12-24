# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.8-x86_64/egg/pypi_switcher/__init__.py
# Compiled at: 2013-09-14 05:42:10
__import__('pkg_resources').declare_namespace(__name__)
import sys, os
from infi.pyutils.contexts import contextmanager
try:
    from ConfigParser import ConfigParser
except ImportError:
    from configparser import ConfigParser

@contextmanager
def open_configparser_file(filepath, write_on_exit=False):
    parser = ConfigParser()
    if os.path.exists(filepath):
        parser.read(filepath)
    try:
        yield parser
    finally:
        if write_on_exit:
            dirpath = os.path.dirname(filepath)
            if not os.path.exists(dirpath):
                os.makedirs(dirpath)
            with open(filepath, 'w') as (fd):
                parser.write(fd)


def set_index_url_in_file(filepath, section_name, key, index_url):
    with open_configparser_file(os.path.expanduser(filepath), True) as (pydistutils):
        if not pydistutils.has_section(section_name):
            pydistutils.add_section(section_name)
        pydistutils.set(section_name, key, index_url)


def set_index_url(argv=sys.argv[1:]):
    index_url, = argv
    if os.name == 'nt':
        set_index_url_in_file('~/pydistutils.cfg', 'easy_install', 'index-url', index_url)
        set_index_url_in_file('~/pip/pip.ini', 'global', 'index-url', index_url)
    else:
        set_index_url_in_file('~/.pydistutils.cfg', 'easy_install', 'index-url', index_url)
        set_index_url_in_file('~/.pip/pip.conf', 'global', 'index-url', index_url)
    set_index_url_in_file('~/.buildout/default.cfg', 'buildout', 'index', index_url)