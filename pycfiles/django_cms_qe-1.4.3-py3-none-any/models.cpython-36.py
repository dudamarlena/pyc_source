# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/tomas/git/euroix/django-cms-qe/cms_qe_video/models.py
# Compiled at: 2020-02-26 05:15:07
# Size of source mod 2**32: 8746 bytes
import re
from typing import Iterable
from cms.models import CMSPlugin
from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils.translation import ugettext
from djangocms_attributes_field.fields import AttributesField
from filer.fields.file import FilerFileField
from filer.fields.image import FilerImageField
ALLOWED_EXTENSIONS = getattr(settings, 'DJANGOCMS_VIDEO_ALLOWED_EXTENSIONS', [
 'mp4', 'webm', 'ogv'])

class AbstractVideoPlayer(CMSPlugin):
    __doc__ = '\n    Abstract configuration model for video player.\n    '
    label = models.CharField(verbose_name=(_('Label')),
      blank=True,
      max_length=255)
    poster = FilerImageField(verbose_name=(_('Poster')),
      blank=True,
      null=True,
      on_delete=(models.SET_NULL),
      related_name='+')
    width = models.IntegerField(verbose_name=(_('Width')),
      blank=True,
      null=True,
      help_text='Leave it blank to make a video player of the default width of video source')
    height = models.IntegerField(verbose_name=(_('Height')),
      blank=True,
      null=True,
      help_text='Leave it blank to make a video player of the default width of video source')
    controls = models.BooleanField(verbose_name=(_('Show controls')),
      default=True)
    autoplay = models.BooleanField(verbose_name=(_('Autoplay')),
      default=False)
    loop = models.BooleanField(verbose_name=(_('Loop')),
      default=False)
    other_attributes = AttributesField(verbose_name=(_('Other attributes')),
      blank=True)

    class Meta:
        abstract = True

    cmsplugin_ptr = models.OneToOneField(CMSPlugin,
      related_name='%(app_label)s_%(class)s',
      parent_link=True)

    def __str__(self):
        return self.label or str(self.pk)

    def copy_relations(self, old_instance):
        self.poster = old_instance.poster

    def _get_attributes_str_to_html(self, attributes: Iterable[str]) -> str:
        """
        Return string with attributes to add to HTML tag e.g.:
        width="500" autoplay mute
        """
        return ' '.join(['{}'.format(attribute) if isinstance(value, bool) else '{}={}'.format(attribute, value) for attribute, value in self.__dict__.items() if attribute in attributes if value])

    def _get_attributes_str_to_url(self, attributes: Iterable[str]) -> str:
        """
        Return string with attributes to add to URL e.g.:
        width=500&autoplay=0&mute=0
        """
        return '&'.join(['{}={}'.format(attribute, int(value)) for attribute, value in self.__dict__.items() if attribute in attributes if value])

    @property
    def attributes_str_to_html(self) -> str:
        """
        Return height and width attributes to put them to html tag. Looks like:
        height="{value}" width="{value}" etc
        """
        attributes_to_print = ('width', 'height', 'controls', 'autoplay', 'loop')
        return self._get_attributes_str_to_html(attributes_to_print)

    @property
    def attributes_str_to_url(self) -> str:
        """
        Return height and width attributes to put them to url. Looks like:
        controls={value}&width={value} etc.
        """
        attributes_to_print = ('controls', 'autoplay', 'loop')
        return self._get_attributes_str_to_url(attributes_to_print)


class SourceFileVideoPlayer(AbstractVideoPlayer):
    __doc__ = '\n    Configuration model for video player to play video from file on local disk.\n    '
    source_file = FilerFileField(verbose_name=(_('Source')),
      blank=False,
      null=True,
      on_delete=(models.SET_NULL),
      related_name='+')
    text_title = models.CharField(verbose_name=(_('Title')),
      blank=True,
      max_length=255)
    text_description = models.TextField(verbose_name=(_('Description')),
      blank=True)
    attributes = AttributesField(verbose_name=(_('Attributes')),
      blank=True)
    muted = models.BooleanField(verbose_name=(_('Mute')),
      default=False)

    def __str__(self):
        res = self.label or str(self.pk)
        if not self.source_file:
            res += ugettext(' <file is missing>')
        return res

    def clean(self):
        if self.source_file:
            if self.source_file.extension not in ALLOWED_EXTENSIONS:
                raise ValidationError(ugettext('Incorrect file type: {extension}.').format(extension=(self.source_file.extension)))

    def get_short_description(self):
        return self.__str__()

    def copy_relations(self, old_instance):
        self.source_file = old_instance.source_file

    @property
    def attributes_str_to_html(self):
        """
        Overloaded.
        Add mute attribute to base-class function.
        """
        attributes_to_print = ('muted', )
        return super().attributes_str_to_html + ' ' + self._get_attributes_str_to_html(attributes_to_print)


YOUTUBE = 1
VIMEO = 2
OTHERS = 3

class HostingVideoPlayer(AbstractVideoPlayer):
    __doc__ = '\n    Configuration model for video player to play video from video hosting services.\n    '
    VIDEO_HOSTING_SERVICES = (
     (
      YOUTUBE, 'YouTube'),
     (
      VIMEO, 'Vimeo'),
     (
      OTHERS, _('Others')))
    video_hosting_service = models.IntegerField(verbose_name=(_('Video hosting service')),
      choices=VIDEO_HOSTING_SERVICES,
      default=OTHERS)
    video_url = models.URLField(verbose_name=(_('Embed link')),
      max_length=255,
      help_text=(_('Use this field to embed videos from external services such as YouTube, Vimeo or others.')))

    @property
    def size_attributes_str_to_html(self) -> str:
        """
        Return height and width attributes to put them to html tag. Looks like:
        height="{value}" width="{value}"
        """
        attributes_to_print = ('height', 'width')
        return self._get_attributes_str_to_html(attributes_to_print)

    def clean(self):
        """
        Validation URLs. Function checks if URL belongs to selected video host service.
        """
        if self.video_hosting_service == VIMEO:
            if not re.search('(^|[/.])vimeo.com/', self.video_url):
                raise ValidationError(_('URL does not belong to Vimeo'))
            if not self.controls:
                raise ValidationError(_('Vimeo does not support hiding controls.'))
        elif self.video_hosting_service == YOUTUBE:
            if not re.search('(^|[/.])youtu.be/', self.video_url):
                if not re.search('(^|[/.])youtube.com/', self.video_url):
                    raise ValidationError(_('URL does not belong to YouTube'))


class VideoTrack(CMSPlugin):
    __doc__ = '\n    Renders the HTML <track> element inside <video>.\n    '
    KIND_CHOICES = [
     (
      'subtitles', _('Subtitles')),
     (
      'captions', _('Captions')),
     (
      'descriptions', _('Descriptions')),
     (
      'chapters', _('Chapters'))]
    kind = models.CharField(verbose_name=(_('Kind')),
      choices=KIND_CHOICES,
      max_length=255)
    src = FilerFileField(verbose_name=(_('Source file')),
      blank=False,
      null=True,
      on_delete=(models.SET_NULL),
      related_name='+')
    srclang = models.CharField(verbose_name=(_('Source language')),
      blank=True,
      max_length=255,
      help_text=(_('Examples: "en" or "de" etc.')))
    label = models.CharField(verbose_name=(_('Label')),
      blank=True,
      max_length=255)
    attributes = AttributesField(verbose_name=(_('Attributes')),
      blank=True)

    def __str__(self):
        label = self.kind
        if self.srclang:
            label += ' {}'.format(self.srclang)
        return label