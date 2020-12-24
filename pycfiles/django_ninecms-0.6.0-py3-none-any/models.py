# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /media/dev-p5qc/workspace/python/team_reset/ninecms/models.py
# Compiled at: 2015-04-08 03:55:31
""" Module definition for Nine CMS """
__author__ = 'George Karakostas'
__copyright__ = 'Copyright 2015, George Karakostas'
__licence__ = 'BSD-3'
__email__ = 'gkarak@9-dev.com'
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.exceptions import ValidationError
from mptt.models import MPTTModel, TreeForeignKey
import os

class PageType(models.Model):
    """ Page Type Model: acts as a single page layout """
    name = models.CharField(max_length=100, unique=True)
    description = models.CharField(max_length=255)
    guidelines = models.CharField(max_length=255, blank=True)
    template = models.CharField(max_length=255, blank=True)
    url_pattern = models.CharField(max_length=255, blank=True)

    class Meta:
        ordering = [
         'id']

    def __str__(self):
        """ Get model name
        :return: model name
        """
        return self.name


class Node(models.Model):
    """ Node Model: basic content record """
    page_type = models.ForeignKey(PageType)
    language = models.CharField(max_length=2, blank=True)
    title = models.CharField(max_length=255)
    user = models.ForeignKey(User)
    status = models.BooleanField(default=1)
    promote = models.BooleanField(default=0)
    sticky = models.BooleanField(default=0)
    created = models.DateTimeField(default=timezone.now)
    changed = models.DateTimeField(auto_now=True)
    original_translation = models.ForeignKey('self', null=True, blank=True, related_name='Translations')
    summary = models.TextField(blank=True)
    body = models.TextField(blank=True)
    highlight = models.CharField(max_length=255, blank=True)
    link = models.URLField(max_length=255, blank=True)
    weight = models.IntegerField(default=0)

    def __str__(self):
        """ Get model name
        :return: model name
        """
        return self.title


class NodeRevision(models.Model):
    """ Node Revision Model: Basic content archive, Drupal style """
    node = models.ForeignKey(Node)
    user = models.ForeignKey(User)
    log_entry = models.CharField(max_length=255, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=255)
    status = models.BooleanField(default=1)
    promote = models.BooleanField(default=0)
    sticky = models.BooleanField(default=0)
    summary = models.TextField(blank=True)
    body = models.TextField(blank=True)
    highlight = models.CharField(max_length=255, blank=True)
    link = models.URLField(max_length=255, blank=True)

    def __str__(self):
        """ Get model name
        :return: model name
        """
        return self.title


class UrlAlias(models.Model):
    """ Url Alias Model: url alias index to node, language enabled """
    language = models.CharField(max_length=2, blank=True)
    alias = models.CharField(max_length=255, db_index=True)
    node = models.ForeignKey(Node)

    class Meta:
        """ Model meta """
        unique_together = ('language', 'alias')
        verbose_name_plural = 'Url aliases'

    def __str__(self):
        """ Get path by filtering out empty (None) list items (language basically)
        :return: model title
        """
        return ('/').join(filter(None, (self.language, self.alias)))


class MenuItem(MPTTModel):
    """ Menu Item Model: menu tree item in a single tree, paths can be empty for parents """
    parent = TreeForeignKey('self', null=True, blank=True, related_name='children')
    weight = models.IntegerField(default=0, db_index=True)
    language = models.CharField(max_length=2, blank=True)
    path = models.CharField(max_length=255, blank=True)
    title = models.CharField(max_length=255)
    disabled = models.BooleanField(default=False)

    def full_path(self):
        """ Get the full path including language (if any) and path
        :return: full path string
        """
        path = self.path
        if path.startswith('http:') or path.startswith('https:'):
            return path
        if path.startswith('/'):
            path = path[1:]
        path = '/' + ('/').join(filter(None, (self.language, path)))
        if path.find('#') == -1 and not path.endswith('/'):
            path += '/'
        elif path.find('#') >= 0 and path.find('/#') == -1:
            path = path.replace('#', '/#')
        return path

    def __str__(self):
        """ Get model name
        :return: model name
        """
        return str(self.title)

    class MPTTMeta:
        """ Set order when inserting items for mptt """
        order_inspection_by = [
         'weight']

        def __init__(self):
            """ Initialize or PyCharm complains because no init in parent
            :return: nothing
            """
            pass


class ContentBlock(models.Model):
    """ Content Block Model: basic block instance which can be used in several page layouts """
    BLOCK_TYPES = (
     ('static', 'Static: link to node'),
     ('menu', 'Menu: render a menu or submenu'),
     ('signal', 'Signal: call site-specific custom render'),
     ('language', 'Language: switch menu'),
     ('user-menu', 'User menu: render a menu with login/register and logout links'),
     ('login', 'Login: render login form'),
     ('search', 'Search: render search form'),
     ('contact', 'Contact: render contact form'))
    type = models.CharField(max_length=50, choices=BLOCK_TYPES, default='static')
    classes = models.CharField(max_length=255, blank=True)
    node = models.ForeignKey(Node, null=True, blank=True)
    menu_item = TreeForeignKey(MenuItem, null=True, blank=True)
    signal = models.CharField(max_length=100, blank=True)

    def __str__(self):
        """ Get title based on block type
        :return: model title
        """
        if self.type == 'static':
            return ('-').join((self.type, str(self.node)))
        if self.type == 'menu':
            return ('-').join((self.type, str(self.menu_item)))
        if self.type == 'signal':
            return ('-').join((self.type, str(self.signal)))
        return self.type


class PageLayoutElement(models.Model):
    """ Page Layout Element Model: a set of these records define the layout for each page type """
    page_type = models.ForeignKey(PageType)
    region = models.CharField(max_length=50, db_index=True)
    block = models.ForeignKey(ContentBlock)
    weight = models.IntegerField(default=0, db_index=True)

    class Meta:
        """ Model meta """
        unique_together = ('page_type', 'block')

    def __str__(self):
        """ Get model name
        :return: model name
        """
        return (' ').join((str(self.page_type), self.region))


def path_file_name(instance, context, filename):
    """ Get path file name
    Transliterate filename
    Filter out any empty component from list
    :param instance: the image field
    :param context: the context such as node field name
    :param filename: the file name
    :return: the path file name
    """
    filename = filename.replace(' ', '_').lower()
    return ('/').join(filter(None, ('ninecms', instance.node.page_type.name, context, instance.group, filename)))


def image_path_file_name(instance, filename):
    """ Callback for image node field to get path file name
    :param instance: the image field
    :param filename: the file name
    :return: the path file name
    """
    return path_file_name(instance, 'image', filename)


def file_path_file_name(instance, filename):
    """ Callback for file node field to get path file name
    :param instance: the image field
    :param filename: the file name
    :return: the path file name
    """
    return path_file_name(instance, 'file', filename)


def video_path_file_name(instance, filename):
    """ Callback for video node field to get path file name
    :param instance: the image field
    :param filename: the file name
    :return: the path file name
    """
    return path_file_name(instance, 'video', filename)


def validate_ext(value, valid):
    """ Validate a file field value for allowed extensions
    :param value: the field file value to validate extension
    :param valid: the allowed extensions to validate against
    :return: None
    """
    ext = os.path.splitext(value.name)[1]
    if ext not in valid:
        raise ValidationError('Unsupported file extension.')


def validate_file_ext(value):
    """ Validate a file field value for allowed file extensions
    :param value: the value to validate
    :return: None
    """
    validate_ext(value, ['.txt', '.pdf', '.doc', '.docx', '.odt', '.xls', '.xlsx', '.ods'])


def validate_video_ext(value):
    """ Validate a video field value for allowed file extensions
    :param value: the value to validate
    :return: None
    """
    validate_ext(value, ['.mp4', '.mpeg', '.m4v', '.webm', '.ogg', '.ogv', '.flv', '.jpg'])


class Media(models.Model):
    """ Media Model: abstract model for media, one node-many images relationship """
    node = models.ForeignKey(Node)
    title = models.CharField(max_length=255, blank=True)
    group = models.CharField(max_length=50, blank=True)

    class Meta:
        abstract = True

    def __str__(self):
        """ Get model name
        :return: model name
        """
        return str(self.node)


class Image(Media):
    """ Image Model: the basic image record """
    image = models.ImageField(upload_to=image_path_file_name, max_length=255)


class File(Media):
    """ File Model: a file field """
    file = models.FileField(upload_to=file_path_file_name, max_length=255, validators=[validate_file_ext])


class Video(Media):
    """ Video Model: a video file field """
    video = models.FileField(upload_to=video_path_file_name, max_length=255, validators=[validate_video_ext])
    VIDEO_TYPES = (
     ('mp4', 'video/mp4'),
     ('webm', 'video/webm'),
     ('ogg', 'video/ogg'),
     ('flv', 'video/flv'),
     ('swf', 'application/x-shockwave-flash'),
     ('jpg', 'image/jpeg'))
    type = models.CharField(max_length=5, choices=VIDEO_TYPES, null=True, blank=True)
    media = models.CharField(max_length=100, blank=True)


class TaxonomyTerm(MPTTModel):
    """ Taxonomy term model: the basic term record, m2m relationship with nodes """
    parent = TreeForeignKey('self', null=True, blank=True, related_name='children')
    name = models.CharField(max_length=50)
    weight = models.IntegerField(default=0, db_index=True)
    description_node = models.ForeignKey(Node, null=True, blank=True, related_name='+')
    nodes = models.ManyToManyField(Node, blank=True, related_name='terms')

    def __str__(self):
        """ Get model name
        :return: model name
        """
        return str(self.name)