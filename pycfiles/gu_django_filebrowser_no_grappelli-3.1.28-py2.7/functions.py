# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.11-intel/egg/filebrowser/functions.py
# Compiled at: 2015-09-01 16:23:41
import os, re, decimal
from time import gmtime, strftime, localtime, mktime, time
from urlparse import urlparse
from django.utils.translation import ugettext as _
from django.utils.safestring import mark_safe
from django.core.files import File
from django.core.files.storage import default_storage
from django.utils.encoding import smart_str
from filebrowser.settings import *
from filebrowser.conf import fb_settings
if STRICT_PIL:
    from PIL import Image
else:
    try:
        from PIL import Image
    except ImportError:
        import Image

def url_to_path(value):
    """
    Change URL to PATH.
    Value has to be an URL relative to MEDIA URL or a full URL (including MEDIA_URL).
    
    Returns a PATH relative to MEDIA_ROOT.
    """
    mediaurl_re = re.compile('^(%s)' % fb_settings.MEDIA_URL)
    value = mediaurl_re.sub('', value)
    return value


def path_to_url(value):
    """
    Change PATH to URL.
    Value has to be a PATH relative to MEDIA_ROOT.
    
    Return an URL relative to MEDIA_ROOT.
    """
    mediaroot_re = re.compile('^(%s)' % fb_settings.MEDIA_ROOT)
    value = mediaroot_re.sub('', value)
    return url_join(fb_settings.MEDIA_URL, value)


def dir_from_url(value):
    """
    Get the relative server directory from a URL.
    URL has to be an absolute URL including MEDIA_URL or
    an URL relative to MEDIA_URL.
    """
    mediaurl_re = re.compile('^(%s)' % fb_settings.MEDIA_URL)
    value = mediaurl_re.sub('', value)
    directory_re = re.compile('^(%s)' % fb_settings.DIRECTORY)
    value = directory_re.sub('', value)
    return os.path.split(value)[0]


def get_version_path(value, version_prefix='', check_file=True):
    """
    Construct the PATH to an Image version.
    Value has to be server-path, relative to MEDIA_ROOT.
    
    version_filename = filename + version_prefix + ext
    if version_prefix is empty returns original file name

    if check_file is not True, then just manipulate file names, do not check actual
    file and versions existence

    Returns a path relative to MEDIA_ROOT.
    :type value: str|unicode
    :type version_prefix: str|unicode
    :type check_file: bool
    :rtype: unicode
    """
    if os.path.isfile(smart_str(os.path.join(fb_settings.MEDIA_ROOT, value))) or not check_file:
        path, filename = os.path.split(value)
        filename, ext = os.path.splitext(filename)
        version_name = None
        orig_filename = None
        for version in VERSIONS:
            if filename.endswith('_' + version):
                if not version_name or len(version) > len(version_name):
                    version_name = version
                    orig_filename = filename.replace('_' + version, '')

        if orig_filename:
            if version_prefix:
                new_filename = smart_str(os.path.join(fb_settings.MEDIA_ROOT, path, orig_filename + '_' + version_prefix + ext))
            else:
                new_filename = smart_str(os.path.join(fb_settings.MEDIA_ROOT, path, orig_filename + ext))
            if os.path.isfile(new_filename) or not check_file:
                filename = orig_filename
                if VERSIONS_BASEDIR != '':
                    path = path.replace(VERSIONS_BASEDIR + '/', '')
        if version_prefix:
            version_filename = filename + '_' + version_prefix + ext
        else:
            version_filename = filename + ext
        return os.path.join(VERSIONS_BASEDIR, path, version_filename)
    else:
        return
        return


def sort_by_attr(seq, attr):
    """
    Sort the sequence of objects by object's attribute
    
    Arguments:
    seq  - the list or any sequence (including immutable one) of objects to sort.
    attr - the name of attribute to sort by
    
    Returns:
    the sorted list of objects.
    """
    import operator
    intermed = map(None, map(getattr, seq, (attr,) * len(seq)), xrange(len(seq)), seq)
    intermed.sort()
    return map(operator.getitem, intermed, (-1, ) * len(intermed))


def url_join(*args):
    """
    URL join routine.
    """
    if args[0].startswith('http://'):
        url = 'http://'
    else:
        url = '/'
    for arg in args:
        arg = arg.replace('\\', '/')
        arg_split = arg.split('/')
        for elem in arg_split:
            if elem != '' and elem != 'http:':
                url = url + elem + '/'

    if os.path.splitext(args[(-1)])[1]:
        url = url.rstrip('/')
    return url


def get_path(path):
    """
    Get Path.
    """
    if path.startswith('.') or os.path.isabs(path) or not os.path.isdir(os.path.join(fb_settings.MEDIA_ROOT, fb_settings.DIRECTORY, path)):
        return None
    return path


def get_file(path, filename):
    """
    Get File.
    """
    converted_path = smart_str(os.path.join(fb_settings.MEDIA_ROOT, fb_settings.DIRECTORY, path, filename))
    if not os.path.isfile(converted_path) and not os.path.isdir(converted_path):
        return None
    else:
        return filename


def get_breadcrumbs(query, path):
    """
    Get breadcrumbs.
    """
    breadcrumbs = []
    dir_query = ''
    if path:
        for item in path.split(os.sep):
            dir_query = os.path.join(dir_query, item)
            breadcrumbs.append([item, dir_query])

    return breadcrumbs


def get_filterdate(filterDate, dateTime):
    """
    Get filterdate.
    """
    returnvalue = ''
    dateYear = strftime('%Y', gmtime(dateTime))
    dateMonth = strftime('%m', gmtime(dateTime))
    dateDay = strftime('%d', gmtime(dateTime))
    if filterDate == 'today' and int(dateYear) == int(localtime()[0]) and int(dateMonth) == int(localtime()[1]) and int(dateDay) == int(localtime()[2]):
        returnvalue = 'true'
    elif filterDate == 'thismonth' and dateTime >= time() - 2592000:
        returnvalue = 'true'
    elif filterDate == 'thisyear' and int(dateYear) == int(localtime()[0]):
        returnvalue = 'true'
    elif filterDate == 'past7days' and dateTime >= time() - 604800:
        returnvalue = 'true'
    elif filterDate == '':
        returnvalue = 'true'
    return returnvalue


def get_settings_var():
    """
    Get settings variables used for FileBrowser listing.
    """
    settings_var = {}
    settings_var['DEBUG'] = DEBUG
    settings_var['MEDIA_ROOT'] = fb_settings.MEDIA_ROOT
    settings_var['MEDIA_URL'] = fb_settings.MEDIA_URL
    settings_var['DIRECTORY'] = fb_settings.DIRECTORY
    settings_var['URL_FILEBROWSER_MEDIA'] = URL_FILEBROWSER_MEDIA
    settings_var['PATH_FILEBROWSER_MEDIA'] = PATH_FILEBROWSER_MEDIA
    settings_var['URL_TINYMCE'] = URL_TINYMCE
    settings_var['PATH_TINYMCE'] = PATH_TINYMCE
    settings_var['EXTENSIONS'] = EXTENSIONS
    settings_var['SELECT_FORMATS'] = SELECT_FORMATS
    settings_var['VERSIONS_BASEDIR'] = VERSIONS_BASEDIR
    settings_var['VERSIONS'] = VERSIONS
    settings_var['ADMIN_VERSIONS'] = ADMIN_VERSIONS
    settings_var['ADMIN_THUMBNAIL'] = ADMIN_THUMBNAIL
    settings_var['PREVIEW_VERSION'] = PREVIEW_VERSION
    settings_var['MAX_UPLOAD_SIZE'] = MAX_UPLOAD_SIZE
    settings_var['CONVERT_FILENAME'] = CONVERT_FILENAME
    return settings_var


def handle_file_upload(path, file):
    """
    Handle File Upload.
    """
    file_path = os.path.join(path, file.name)
    uploadedfile = default_storage.save(file_path, file)
    return uploadedfile


def get_file_type(filename):
    """
    Get file type as defined in EXTENSIONS.
    """
    file_extension = os.path.splitext(filename)[1].lower()
    file_type = ''
    for k, v in EXTENSIONS.iteritems():
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
    for k, v in SELECT_FORMATS.iteritems():
        for extension in v:
            if file_extension == extension.lower():
                select_types.append(k)

    return select_types


def version_generator(value, version_prefix, force=None):
    """
    Generate Version for an Image.
    value has to be a serverpath relative to MEDIA_ROOT.
    """
    if STRICT_PIL:
        from PIL import ImageFile
    else:
        try:
            from PIL import ImageFile
        except ImportError:
            import ImageFile

        ImageFile.MAXBLOCK = IMAGE_MAXBLOCK
        try:
            im = Image.open(smart_str(os.path.join(fb_settings.MEDIA_ROOT, value)))
            version_path = get_version_path(value, version_prefix)
            absolute_version_path = smart_str(os.path.join(fb_settings.MEDIA_ROOT, version_path))
            version_dir = os.path.split(absolute_version_path)[0]
            if not os.path.isdir(version_dir):
                os.makedirs(version_dir)
                os.chmod(version_dir, 509)
            version = scale_and_crop(im, VERSIONS[version_prefix]['width'], VERSIONS[version_prefix]['height'], VERSIONS[version_prefix]['opts'])
            try:
                version.save(absolute_version_path, quality=90, optimize=os.path.splitext(version_path)[1].lower() != '.gif')
            except IOError:
                version.save(absolute_version_path, quality=90)

            return version_path
        except:
            return

    return


def scale_and_crop(im, width, height, opts):
    """
    Scale and Crop.
    """
    x, y = [ float(v) for v in im.size ]
    if width:
        xr = float(width)
    else:
        xr = float(x * height / y)
    if height:
        yr = float(height)
    else:
        yr = float(y * width / x)
    if 'crop' in opts:
        r = max(xr / x, yr / y)
    else:
        r = min(xr / x, yr / y)
    if r < 1.0 or r > 1.0 and 'upscale' in opts:
        im = im.resize((int(x * r), int(y * r)), resample=Image.ANTIALIAS)
    if 'crop' in opts:
        x, y = [ float(v) for v in im.size ]
        ex, ey = (x - min(x, xr)) / 2, (y - min(y, yr)) / 2
        if ex or ey:
            im = im.crop((int(ex), int(ey), int(x - ex), int(y - ey)))
    return im


scale_and_crop.valid_options = ('crop', 'upscale')

def convert_filename(value):
    """
    Convert Filename.
    """
    if CONVERT_FILENAME:
        return value.replace(' ', '_').lower()
    else:
        return value