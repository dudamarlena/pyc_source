# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.11-intel/egg/filebrowser/base.py
# Compiled at: 2014-11-22 02:35:13
import os, re, datetime
from time import gmtime, strftime
from django.conf import settings
from filebrowser.settings import *
from filebrowser.conf import fb_settings
from filebrowser.functions import get_file_type, url_join, is_selectable, get_version_path
from django.utils.encoding import force_unicode
if STRICT_PIL:
    from PIL import Image
else:
    try:
        from PIL import Image
    except ImportError:
        import Image

class FileObject(object):
    """
    The FileObject represents a File on the Server.
    
    PATH has to be relative to MEDIA_ROOT.
    """

    def __init__(self, path):
        """
        `os.path.split` Split the pathname path into a pair, (head, tail) where tail is the last pathname component and head is everything leading up to that. The tail part will never contain a slash; if path ends in a slash, tail will be empty. If there is no slash in path, head will be empty. If path is empty, both head and tail are empty.
        """
        self.path = path
        self.url_rel = path.replace('\\', '/')
        self.head, self.filename = os.path.split(path)
        self.filename_lower = self.filename.lower()
        self.filetype = get_file_type(self.filename)

    def _filesize(self):
        """
        Filesize.
        """
        path = force_unicode(self.path)
        if os.path.isfile(os.path.join(fb_settings.MEDIA_ROOT, path)) or os.path.isdir(os.path.join(fb_settings.MEDIA_ROOT, path)):
            return os.path.getsize(os.path.join(fb_settings.MEDIA_ROOT, path))
        return ''

    filesize = property(_filesize)

    def _date(self):
        """
        Date.
        """
        if os.path.isfile(os.path.join(fb_settings.MEDIA_ROOT, self.path)) or os.path.isdir(os.path.join(fb_settings.MEDIA_ROOT, self.path)):
            return os.path.getmtime(os.path.join(fb_settings.MEDIA_ROOT, self.path))
        return ''

    date = property(_date)

    def _datetime(self):
        """
        Datetime Object.
        """
        return datetime.datetime.fromtimestamp(self.date)

    datetime = property(_datetime)

    def _extension(self):
        """
        Extension.
        """
        return '%s' % os.path.splitext(self.filename)[1]

    extension = property(_extension)

    def _filetype_checked(self):
        if self.filetype == 'Folder' and os.path.isdir(self.path_full):
            return self.filetype
        else:
            if self.filetype != 'Folder' and os.path.isfile(self.path_full):
                return self.filetype
            return ''

    filetype_checked = property(_filetype_checked)

    def _path_full(self):
        """
        Full server PATH including MEDIA_ROOT.
        """
        return os.path.join(fb_settings.MEDIA_ROOT, self.path)

    path_full = property(_path_full)

    def _path_relative(self):
        return self.path

    path_relative = property(_path_relative)

    def _path_relative_directory(self):
        """
        Path relative to initial directory.
        """
        directory_re = re.compile('^(%s)' % fb_settings.DIRECTORY)
        value = directory_re.sub('', self.path)
        return '%s' % value

    path_relative_directory = property(_path_relative_directory)

    def _url_relative(self):
        return self.url_rel

    url_relative = property(_url_relative)

    def _url_full(self):
        """
        Full URL including MEDIA_URL.
        """
        return force_unicode(url_join(fb_settings.MEDIA_URL, self.url_rel))

    url_full = property(_url_full)

    def _url_save(self):
        """
        URL used for the filebrowsefield.
        """
        if SAVE_FULL_URL:
            return self.url_full
        else:
            return self.url_rel

    url_save = property(_url_save)

    def _url_thumbnail(self):
        """
        Thumbnail URL.
        """
        if self.filetype == 'Image':
            return '%s' % url_join(fb_settings.MEDIA_URL, get_version_path(self.path, ADMIN_THUMBNAIL))
        else:
            return ''

    url_thumbnail = property(_url_thumbnail)

    def url_admin(self):
        if self.filetype_checked == 'Folder':
            directory_re = re.compile('^(%s)' % fb_settings.DIRECTORY)
            value = directory_re.sub('', self.path)
            return '%s' % value
        else:
            return '%s' % url_join(fb_settings.MEDIA_URL, self.path)

    def _dimensions(self):
        """
        Image Dimensions.
        """
        if self.filetype == 'Image':
            try:
                im = Image.open(os.path.join(fb_settings.MEDIA_ROOT, self.path))
                return im.size
            except:
                pass

        else:
            return False

    dimensions = property(_dimensions)

    def _width(self):
        """
        Image Width.
        """
        return self.dimensions[0]

    width = property(_width)

    def _height(self):
        """
        Image Height.
        """
        return self.dimensions[1]

    height = property(_height)

    def _orientation(self):
        """
        Image Orientation.
        """
        if self.dimensions:
            if self.dimensions[0] >= self.dimensions[1]:
                return 'Landscape'
            else:
                return 'Portrait'

        else:
            return
        return

    orientation = property(_orientation)

    def _is_empty(self):
        """
        True if Folder is empty, False if not.
        """
        if os.path.isdir(self.path_full):
            if not os.listdir(self.path_full):
                return True
            else:
                return False

        else:
            return
        return

    is_empty = property(_is_empty)

    def __repr__(self):
        return force_unicode(self.url_save)

    def __str__(self):
        return force_unicode(self.url_save)

    def __unicode__(self):
        return force_unicode(self.url_save)