# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/downloads/models.py
# Compiled at: 2015-06-24 11:40:21
import os.path, uuid
from django.db import models
from django.conf import settings
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
from jmbo.models import ModelBase
from downloads.fields import ColourField
from downloads.managers import VisibleManager
DOWNLOAD_UPLOAD_FOLDER = 'downloads'
MOD_MEDIA_UPLOAD_FOLDER = os.path.join(DOWNLOAD_UPLOAD_FOLDER, 'mods')
TEMP_UPLOAD_FOLDER = os.path.join(DOWNLOAD_UPLOAD_FOLDER, 'tmp')

class Download(ModelBase):
    file = models.FileField(upload_to=DOWNLOAD_UPLOAD_FOLDER, max_length=255, null=True, blank=True)
    file_name = models.CharField(max_length=255, null=True, blank=True)
    visible = models.BooleanField(default=True)

    class Meta:
        ordering = [
         'primary_category', 'title']

    @models.permalink
    def get_absolute_url(self):
        return ('downloads.views.download_request', (self.slug,))

    def get_file(self, request):
        if self.file_name:
            return (self.file, self.file_name)
        else:
            return (
             self.file, os.path.basename(self.file.name))

    def delete(self):
        if self.file and os.path.exists(self.file.path):
            os.remove(self.file.path)
        super(Download, self).delete()


class TemporaryDownloadAbstract(Download):
    unique_per_user = models.BooleanField(default=False, editable=False)

    class Meta:
        abstract = True

    def make_file_name(self, request, extension=''):
        if self.unique_per_user:
            id = str(uuid.UUID(int=request.user.id))
        else:
            id = str(uuid.uuid4())
        return '%s_%s.%s' % (self.slug, id, extension)

    def create_file(self, file_path, request):
        raise NotImplementedError

    def get_file(self, request):
        file_name = self.make_file_name(request)
        file_path = os.path.join(settings.MEDIA_ROOT, TEMP_UPLOAD_FOLDER, file_name)
        try:
            f = open(file_path)
            f.close()
        except IOError:
            self.create_file(file_path, request)

        self.file.name = os.path.join(TEMP_UPLOAD_FOLDER, file_name)
        return super(TemporaryDownloadAbstract, self).get_file(request)


class TextOverlayTemporaryDownload(TemporaryDownloadAbstract):
    background_image = models.ImageField(upload_to=MOD_MEDIA_UPLOAD_FOLDER)
    text = models.TextField()
    x = models.PositiveIntegerField()
    y = models.PositiveIntegerField()
    width = models.PositiveIntegerField()
    height = models.PositiveIntegerField()
    font = models.FilePathField(path='/usr/share/fonts/truetype/', recursive=True)
    font_size = models.PositiveIntegerField()
    colour = ColourField()

    def make_file_name(self, request):
        return super(TextOverlayTemporaryDownload, self).make_file_name(request, 'jpg')

    def draw_text(self, drawable, pos, text):
        drawable.text(pos, text, font=self._font, fill=self._colour)

    def create_file(self, file_path, request):
        self._font = ImageFont.truetype(self.font, self.font_size)
        self._colour = str(self.colour)
        box = (self.x, self.y, self.width, self.height)
        line_height = int(self.font_size * 0.85)
        image = Image.open(self.background_image.path).copy()
        draw = ImageDraw.Draw(image)
        height = 0
        line = ''
        for word in self.text.split(' '):
            size = draw.textsize(line + word, font=self._font)
            if size[0] > box[2]:
                self.draw_text(draw, (box[0], box[1] + height), line[0:-1])
                line = word + ' '
                height += line_height
            else:
                line += word + ' '

        self.draw_text(draw, (box[0], box[1] + height), line[0:-1])
        del draw
        image.save(file_path)


def set_download_manager(cls):
    cls.add_to_class('permitted', VisibleManager())
    for c in cls.__subclasses__():
        set_download_manager(c)


set_download_manager(Download)