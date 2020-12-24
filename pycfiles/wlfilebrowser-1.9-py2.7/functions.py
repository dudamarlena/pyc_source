# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/wlfilebrowser/functions.py
# Compiled at: 2016-04-17 01:57:39
from __future__ import unicode_literals
from future.builtins import int
from future.builtins import range
from future.builtins import map
from future.builtins import str
import os, re, unicodedata
from time import gmtime, strftime, localtime, time
from django.contrib.sites.models import Site
from django.core.files.storage import default_storage
from wlfilebrowser.settings import *

def get_directory():
    """
    Returns FB's ``DIRECTORY`` setting, appending a directory using
    the site's ID if ``MEDIA_LIBRARY_PER_SITE`` is ``True``, and also
    creating the root directory if missing.
    """
    from wenlincms.conf import settings as mezz_settings
    dirname = DIRECTORY
    if getattr(mezz_settings, b'MEDIA_LIBRARY_PER_SITE', False):
        dirname = os.path.join(dirname, b'site-1')
    fullpath = os.path.join(mezz_settings.MEDIA_ROOT, dirname)
    if not default_storage.isdir(fullpath):
        default_storage.makedirs(fullpath)
    return dirname


def path_strip(path, root):
    if not path or not root:
        return path
    path = os.path.normcase(path)
    root = os.path.normcase(root)
    if path.startswith(root):
        return path[len(root):]
    return path


def url_to_path(value):
    """
    Change URL to PATH.
    Value has to be an URL relative to MEDIA URL or a full URL (including MEDIA_URL).

    Returns a PATH relative to MEDIA_ROOT.
    """
    mediaurl_re = re.compile(b'^(%s)' % MEDIA_URL)
    value = mediaurl_re.sub(b'', value)
    return value


def path_to_url(value):
    """
    Change PATH to URL.
    Value has to be a PATH relative to MEDIA_ROOT.

    Return an URL relative to MEDIA_ROOT.
    """
    mediaroot_re = re.compile(b'^(%s)' % MEDIA_ROOT)
    value = mediaroot_re.sub(b'', value)
    return url_join(MEDIA_URL, value)


def dir_from_url(value):
    """
    Get the relative server directory from a URL.
    URL has to be an absolute URL including MEDIA_URL or
    an URL relative to MEDIA_URL.
    """
    mediaurl_re = re.compile(b'^(%s)' % MEDIA_URL)
    value = mediaurl_re.sub(b'', value)
    directory_re = re.compile(b'^(%s)' % get_directory())
    value = directory_re.sub(b'', value)
    return os.path.split(value)[0]


def url_join(*args):
    """
    URL join routine.
    """
    if args[0].startswith(b'http://'):
        url = b'http://'
    else:
        url = b'/'
    for arg in args:
        arg = str(arg).replace(b'\\', b'/')
        arg_split = arg.split(b'/')
        for elem in arg_split:
            if elem != b'' and elem != b'http:':
                url = url + elem + b'/'

    if os.path.splitext(args[(-1)])[1]:
        url = url.rstrip(b'/')
    return url


def get_path(path):
    """
    Get Path.
    """
    if path.startswith(b'.') or os.path.isabs(path) or not default_storage.isdir(os.path.join(get_directory(), path)):
        return None
    return path


def get_file(path, filename):
    """
    Get File.
    """
    if not default_storage.exists(os.path.join(get_directory(), path, filename)):
        return None
    else:
        return filename


def get_breadcrumbs(query, path):
    """
    Get breadcrumbs.
    """
    breadcrumbs = []
    dir_query = b''
    if path:
        for item in path.split(os.sep):
            dir_query = os.path.join(dir_query, item)
            breadcrumbs.append([item, dir_query])

    return breadcrumbs


def get_filterdate(filterDate, dateTime):
    """
    Get filterdate.
    """
    returnvalue = b''
    dateYear = strftime(b'%Y', gmtime(dateTime))
    dateMonth = strftime(b'%m', gmtime(dateTime))
    dateDay = strftime(b'%d', gmtime(dateTime))
    if filterDate == (b'today' and int(dateYear) == int(localtime()[0]) and int(dateMonth) == int(localtime()[1]) and int(dateDay) == int(localtime()[2])):
        returnvalue = b'true'
    elif filterDate == b'thismonth' and dateTime >= time() - 2592000:
        returnvalue = b'true'
    elif filterDate == b'thisyear' and int(dateYear) == int(localtime()[0]):
        returnvalue = b'true'
    elif filterDate == b'past7days' and dateTime >= time() - 604800:
        returnvalue = b'true'
    elif filterDate == b'':
        returnvalue = b'true'
    return returnvalue


def get_settings_var():
    """
    Get settings variables used for WlFileBrowser listing.
    """
    settings_var = {}
    settings_var[b'DEBUG'] = DEBUG
    settings_var[b'MEDIA_ROOT'] = MEDIA_ROOT
    settings_var[b'MEDIA_URL'] = MEDIA_URL
    settings_var[b'DIRECTORY'] = get_directory()
    settings_var[b'URL_FILEBROWSER_MEDIA'] = URL_FILEBROWSER_MEDIA
    settings_var[b'PATH_FILEBROWSER_MEDIA'] = PATH_FILEBROWSER_MEDIA
    settings_var[b'URL_TINYMCE'] = URL_TINYMCE
    settings_var[b'PATH_TINYMCE'] = PATH_TINYMCE
    settings_var[b'EXTENSIONS'] = EXTENSIONS
    settings_var[b'SELECT_FORMATS'] = SELECT_FORMATS
    settings_var[b'VERSIONS_BASEDIR'] = VERSIONS_BASEDIR
    settings_var[b'VERSIONS'] = VERSIONS
    settings_var[b'ADMIN_VERSIONS'] = ADMIN_VERSIONS
    settings_var[b'ADMIN_THUMBNAIL'] = ADMIN_THUMBNAIL
    settings_var[b'MAX_UPLOAD_SIZE'] = MAX_UPLOAD_SIZE
    settings_var[b'CONVERT_FILENAME'] = CONVERT_FILENAME
    return settings_var


def get_file_type(filename):
    """
    Get file type as defined in EXTENSIONS.
    """
    file_extension = os.path.splitext(filename)[1].lower()
    file_type = b''
    for k, v in EXTENSIONS.items():
        for extension in v:
            if file_extension == extension.lower():
                file_type = k

    return file_type


def is_selectable(filename, selecttype):
    """
    Get select type as defined in FORMATS.
    """
    file_extension = os.path.splitext(filename)[1].lower()
    select_types = []
    for k, v in SELECT_FORMATS.items():
        for extension in v:
            if file_extension == extension.lower():
                select_types.append(k)

    return select_types


def convert_filename(value):
    """
    Convert Filename.
    https://github.com/sehmaschine/django-wlfilebrowser/blob/master/wlfilebrowser/functions.py
    """
    if NORMALIZE_FILENAME:
        chunks = value.split(os.extsep)
        normalized = []
        for v in chunks:
            v = unicodedata.normalize(b'NFKD', str(v)).encode(b'ascii', b'ignore')
            v = re.sub(b'[^\\w\\s-]', b'', v).strip()
            normalized.append(v)

        if len(normalized) > 1:
            value = (b'.').join(normalized)
        else:
            value = normalized[0]
    if CONVERT_FILENAME:
        value = value.replace(b' ', b'_').lower()
    return value