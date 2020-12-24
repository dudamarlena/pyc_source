# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/dan/working/eventum/eventum/models/Image.py
# Compiled at: 2016-04-19 10:38:51
"""
.. module:: Image
    :synopsis: A image database model.

.. moduleauthor:: Dan Schlosser <dan@schlosser.io>
"""
import re, os
from flask import url_for, current_app
from datetime import datetime
from mongoengine import Document, DateTimeField, StringField, ReferenceField, DictField, ValidationError, signals
from eventum.models import BaseEventumDocument
from eventum.lib.regex import Regex
now = datetime.now

class Image(Document, BaseEventumDocument):
    """
    :ivar date_created: :class:`mongoengine.fields.DateTimeField` - The date
        when the document was created, localized to the server.
    :ivar date_modified: :class:`mongoengine.fields.DateTimeField` - The date
        when the document was last modified, localized to the server.
    :ivar filename: :class:`mongoengine.fields.StringField` - The filename with
        extension of the image.
    :ivar creator: :class:`mongoengine.fields.ReferenceField` - Reference to
        the User that uploaded the photo.
    :ivar caption: :class:`mongoengine.fields.StringField` - A caption for the
        photo.
    :ivar source: :class:`mongoengine.fields.StringField` - A source credit for
        the picture, if one is needed.
    :ivar default_path: :class:`mongoengine.fields.StringField` - The path to
        the image that should be used.
    """
    meta = {'allow_inheritance': True, 
       'indexes': [
                 'creator'], 
       'ordering': [
                  '-date_created']}
    date_created = DateTimeField(default=now, required=True)
    date_modified = DateTimeField(default=now, required=True)
    filename = StringField(unique=True, max_length=255, required=True, regex=Regex.FULL_FILENAME_REGEX)
    creator = ReferenceField('User', required=True)
    caption = StringField()
    source = StringField()
    default_path = StringField(required=True)

    def url(self):
        """Returns the URL path that points to the image.

        :returns: The URL path like ``"/static/img/cat.jpg"``.
        :rtype: str
        """
        return url_for('media.file', filename=self.filename)

    def clean(self):
        """Called by Mongoengine on every ``.save()`` to the object.

        Update date_modified.

        :raises: :class:`wtforms.validators.ValidationError`
        """
        self.date_modified = now()
        if not re.compile(Regex.VALID_PATHS).match(self.default_path):
            self.default_path = os.path.join(current_app.config['EVENTUM_BASEDIR'], self.default_path)

    @classmethod
    def post_delete(cls, sender, document, **kwargs):
        """Called by Mongoengine after the object has been delted.

        Moves the deleted image's assocaited files to the DELETED_FOLDER.
        """
        old_path = document.default_path
        _, filename = os.path.split(document.default_path)
        delete_folder = current_app.config['EVENTUM_DELETE_FOLDER']
        if not os.path.isdir(delete_folder):
            os.mkdir(delete_folder)
        new_path = os.path.join(delete_folder, filename)
        try:
            os.rename(old_path, new_path)
        except IOError:
            pass

    def __unicode__(self):
        """This image, as a unicode string.

        :returns: The filename of the image.
        :rtype: str
        """
        return self.filename

    def __repr__(self):
        """The representation of this image.

        :returns: The image's details.
        :rtype: str
        """
        rep = ('Photo(filename={}, default_path={}, caption={})').format(self.filename, self.default_path, self.caption)
        return rep


signals.post_delete.connect(Image.post_delete, sender=Image)