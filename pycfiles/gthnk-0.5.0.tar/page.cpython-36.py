# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: ./gthnk/models/page.py
# Compiled at: 2017-11-21 20:58:03
# Size of source mod 2**32: 2127 bytes
from flask_diamond.mixins.crud import CRUDMixin
from .. import db
from PIL import Image
from io import BytesIO

class Page(db.Model, CRUDMixin):
    id = db.Column((db.Integer), primary_key=True)
    day_id = db.Column(db.Integer, db.ForeignKey('day.id'))
    sequence = db.Column(db.Integer)
    binary = db.Column(db.Binary)
    title = db.Column(db.Unicode(1024))
    thumbnail = db.Column(db.Binary)
    preview = db.Column(db.Binary)
    extension = db.Column(db.String(32))

    def set_image(self, binary):
        self.binary = binary
        with Image.open(BytesIO(self.binary)) as (img):
            self.extension = img.format.lower()
            flattened = img.copy().convert('RGB')
            size = (150, 200)
            thumb = flattened.copy()
            thumb.thumbnail(size)
            thumb_buf = BytesIO()
            thumb.save(thumb_buf, 'JPEG')
            self.thumbnail = thumb_buf.getvalue()
            size = (612, 792)
            preview = flattened.copy()
            preview.thumbnail(size)
            preview_buf = BytesIO()
            preview.save(preview_buf, 'JPEG')
            self.preview = preview_buf.getvalue()
        self.save()

    def filename(self, extension=None):
        if not extension:
            extension = self.extension
        return '{0}-{1}.{2}'.format(self.day.date, self.sequence, extension)

    def content_type(self):
        if self.extension == 'pdf':
            return 'application/pdf'
        else:
            if self.extension == 'gif':
                return 'image/gif'
            if self.extension == 'png':
                return 'image/png'
            if self.extension == 'jpg':
                return 'image/jpeg'

    def __repr__(self):
        if self.sequence is not None:
            return '<Page filename: %s-%d.pdf>' % (self.day.date, self.sequence)
        else:
            return '<Page filename: %s-xxx.pdf>' % self.day.date

    def __unicode__(self):
        return repr(self)