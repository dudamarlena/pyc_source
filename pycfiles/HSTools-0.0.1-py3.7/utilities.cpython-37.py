# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/hstools/utilities.py
# Compiled at: 2019-10-10 13:25:40
# Size of source mod 2**32: 5108 bytes
from __future__ import print_function
import os, glob
from .compat import *

def sizeof_fmt(num, suffix='B'):
    for unit in ('', 'Ki', 'Mi', 'Gi', 'Ti', 'Pi', 'Ei', 'Zi'):
        if abs(num) < 1024.0:
            return '%3.1f%s%s' % (num, unit, suffix)
        num /= 1024.0

    return '%.1f%s%s' % (num, 'Yi', suffix)


def get_hs_content(resid):
    resdir = find_resource_directory(resid)
    content = {}
    for f in glob.glob('%s/*/data/contents/*' % resdir):
        fname = os.path.basename(f)
        content[fname] = f

    return content


def find_resource_directory(resid):
    download_dir = os.environ.get('JUPYTER_DOWNLOADS', 'hs_downloads')
    for dirpath, dirnames, filenames in os.walk(download_dir):
        for dirname in [d for d in dirnames]:
            if dirname == resid:
                return os.path.join(dirpath, dirname)


def check_for_ipynb(content_files):
    links = {}
    for f, p in content_files.items():
        if f[-5:] == 'ipynb':
            fname = os.path.basename(p)
            url = urlencode(p)
            links[fname] = url

    return links


def display_resource_content_files(content_file_dictionary, text='Found the following content when parsing the HydroShare resource:'):
    nbs = check_for_ipynb(content_file_dictionary)
    if len(nbs.keys()) > 0:
        print('<b>Found the following notebook(s) associated with thisHydroShare resource.</b><br>Click the link(s) below to launchthe notebook.')
        for name, url in nbs.items():
            print('<a href=%s target="_blank">%s<a>' % (url, name))

    if len(content_file_dictionary.keys()) > 0:
        print('<b>Found the following file(s) associated with this HydroShare resource.</b>')
        text = '<br>'.join(content_file_dictionary.keys())
        print(text)
    if len(content_file_dictionary.keys()) + len(nbs.keys()) > 0:
        print('These files are stored in a dictionary called <b>hs.content</b> for your convenience.  To access a file, simply issue the following command where MY_FILE is one of the files listed above: <pre>hs.content["MY_FILE"] </pre> ')


def load_environment(env_path=None):
    if env_path is None:
        env_path = os.path.join(os.environ.get('NOTEBOOK_HOME', './'), '.env')
    else:
        return os.path.exists(env_path) or None
    with open(env_path, 'r') as (f):
        lines = f.readlines()
        print('Adding the following system variables:')
        for line in lines:
            k, v = line.strip().split('=')
            os.environ[k] = v
            print('   %s = %s' % (k, v))

        print('\nThese can be accessed using the following command: ')
        print('   os.environ[key]')
        print('\n   (e.g.)\n   os.environ["HS_USR_NAME"]  => %s' % os.environ['HS_USR_NAME'])


def get_env_var(varname):
    if varname in os.environ.keys():
        return os.environ[varname]
    return input('Could not find %s, please specify a value: ' % varname).strip()


def get_server_url_for_path(p):
    """
    gets the url corresponding to a given file or directory path
    p : path to convert into a url

    returns the url path for the filepath p
    """
    load_environment()
    rel_path = os.path.relpath(p, os.environ['NOTEBOOK_HOME'])
    url = urlencode(rel_path)
    return url


def get_relative_path(p):
    """
    gets the path relative to the jupyter home directory
    p: path to convert into relative path

    returns the path relative to the default jupyter home directory
    """
    return os.path.relpath(p, os.environ['NOTEBOOK_HOME'])


def _realname(path, root=None):
    if root is not None:
        path = os.path.join(root, path)
    result = os.path.basename(path)
    if os.path.islink(path):
        realpath = os.readlink(path)
        result = '%s -> %s' % (os.path.basename(path), realpath)
    return result


def tree(startpath, depth=-1):
    prefix = 0
    if startpath != '/':
        if startpath.endswith('/'):
            startpath = startpath[:-1]
        prefix = len(startpath)
    for root, dirs, files in os.walk(startpath):
        level = root[prefix:].count(os.sep)
        if depth > -1:
            if level > depth:
                continue
        indent = subindent = ''
        if level > 0:
            indent = '|   ' * (level - 1) + '|-- '
        subindent = '|   ' * level + '|-- '
        print('{}{}/'.format(indent, _realname(root)))
        for d in dirs:
            if os.path.islink(os.path.join(root, d)):
                print('{}{}'.format(subindent, _realname(d, root=root)))

        for f in files:
            print('{}{}'.format(subindent, _realname(f, root=root)))