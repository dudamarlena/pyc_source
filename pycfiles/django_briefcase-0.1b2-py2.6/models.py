# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\briefcase\models.py
# Compiled at: 2010-10-21 15:19:59
import mimetypes, os
from django.contrib.auth.models import User
from django.db import models
from django.db.models.fields.files import FieldFile
from django.utils.translation import ugettext_lazy as _
mime_file = os.path.join(os.path.realpath(os.path.dirname(__file__)), 'data/mime.types')
type_map = mimetypes.read_mime_types(mime_file)
for (extension, mime_type) in type_map.iteritems():
    mimetypes.add_type(mime_type, extension)

class DocumentStatus(models.Model):
    """
    Status of the document.
    
    Defines document's stage in the workflow or just marks it as some custom
    status, eg. draft, unreviewed, published, etc.
    """
    name = models.CharField(_('status name'), max_length=150, help_text=_("Displayed name of the document's status."))
    slug = models.SlugField(max_length=150, unique=True, help_text=_('Slug name - important for the programmers.'))
    description = models.CharField(_('status description'), max_length=250, blank=True, help_text=_('Status description - can be left empty.'))

    class Meta:
        verbose_name = _('Document status')
        verbose_name_plural = _('Document statuses')
        ordering = ['-name']

    def __unicode__(self):
        return self.name


class DocumentType(models.Model):
    """
    File type (eg. PDF file, MS Word file etc.).
    """
    extension = models.CharField(_('File extension'), max_length=12, blank=True, help_text="File extension for this type (without the dot, eg. 'jpg').")
    mimetype = models.CharField(_('MIME type'), max_length=127, default='application/octet-stream', help_text=_('File MIME type as defined by <a href="http://tools.ietf.org/html/rfc4288#section-4.2">RFC 4288</a>, for example: \'image/jpeg\''))
    name = models.CharField(_('Full name'), max_length=250, blank=True, help_text=_("Human-readable name of the type, for example 'JPG Image'"))

    class Meta:
        verbose_name = _('Document type')
        verbose_name_plural = _('Document types')
        ordering = ['name']

    def __unicode__(self):
        if self.name:
            return self.name
        return self.mimetype

    @classmethod
    def unknown_type(cls):
        """
        Returns a default document type - a generic "Unknown type".
        
        This provides a sensible default value for a Document before saving it.
        """
        (obj, created) = cls.objects.get_or_create(mimetype='application/octet-stream', name='Unknown type')
        return obj

    @classmethod
    def type_for_file(cls, file):
        """
        Finds an apropriate DocumentType for the given file.
        
        ``file`` can be a Django model field (of type ``FileField``, which is 
        accessed as ``FieldFile``), or simply a filename as a string.
        
        If there were no such document type in the database, a new one is
        created, with default name consisting of uppercase extension and the
        'Document' word, for example: 'XLS Document'. This name can be of course
        changed in the admin.
        """
        if isinstance(file, FieldFile):
            filename = file.name
        else:
            filename = file
        extension = os.path.splitext(filename)[1]
        extension = extension[1:].lower()
        (mimetype, encoding) = mimetypes.guess_type(filename)
        mimetype = mimetype or 'application/octet-stream'
        (obj, created) = cls.objects.get_or_create(extension=extension, mimetype=mimetype)
        if created:
            obj.name = extension.upper() + ' Document'
            obj.save()
        return obj


class Document(models.Model):
    """
    The document itself.
    """
    file = models.FileField(verbose_name=_('file'), upload_to='uploads/%Y/%m/%d/', help_text=_('This is the document itself - well, just a file.'))
    type = models.ForeignKey(DocumentType, verbose_name=_('document type'), blank=True, null=True, help_text=_("Document type, for example 'Microsoft Word Document' or 'PDF File'."))
    status = models.ForeignKey(DocumentStatus, verbose_name=_('document status'), null=True, blank=True)
    added_by = models.ForeignKey(User, verbose_name=_('added by'), null=True, blank=True, editable=False)
    added_at = models.DateTimeField(_('added at'), auto_now_add=True)
    updated_at = models.DateTimeField(_('recently changed at'), auto_now=True)

    class Meta:
        verbose_name = _('Document')
        verbose_name_plural = _('Documents')
        ordering = ['-added_at']

    def __unicode__(self):
        return os.path.basename(self.file.name)

    def save(self, *args, **kwargs):
        """
        Attaches a guessed DocumentType to the Document object.
        
        The check for id is a standard way to determine whether the object
        is created (no row in the database yet, hence no id) or updated.
        """
        if not self.id:
            self.type = DocumentType.type_for_file(self.file)
        super(Document, self).save(*args, **kwargs)

    def get_size(self):
        return self.file.size

    def get_filename(self):
        return os.path.basename(self.file.name)