# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/imposeren/kava/42-kavyarnya/.env/lib/python2.7/site-packages/x_file_accel_redirects/models.py
# Compiled at: 2014-03-28 04:47:41
import os
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import ugettext_lazy as _
from model_utils import Choices
from x_file_accel_redirects.conf import settings

class AccelRedirect(models.Model):
    FILENAME_SOLVERS = Choices((
     1, 'remainder', _('Everything after last "/" is is threated as filename')), (
     2, 'none', _('Do not try processing filenames (e.g. for service)')))
    description = models.CharField(max_length=64)
    prefix = models.CharField(_('URL prefix'), help_text=_('URL prefix for accel_view that will be handled with this config'), default='media', max_length=64, unique=True)
    login_required = models.BooleanField(_('Login required'), help_text=_('Protect files with authentication'), default=True)
    internal_path = models.CharField(_('Internal path'), help_text=_("Path that is served by nginx as internal to use in X-Accel-Redirect header. Actual Accell will be '{internal_path}/{path_in_url_after_prefix}'"), max_length=64)
    serve_document_root = models.CharField(_('Document root'), help_text=_('Path with actual files to serve manualy when settings.X_FILE_ACCEL is False'), default='', blank=True, max_length=64)
    filename_solver = models.PositiveSmallIntegerField(choices=FILENAME_SOLVERS, default=FILENAME_SOLVERS.remainder)

    class Meta:
        verbose_name = _('Accel-Redirect config')
        verbose_name_plural = _('Accel-Redirect configs')
        db_table = 'xfar_accelredirect'

    def __unicode__(self):
        return self.description

    def clean(self):
        if settings.X_FILE_ACCEL and not self.serve_document_root:
            raise ValidationError(_('X_FILE_ACCEL is disabled! Please set serve_document_root field.'))
        if self.prefix.find('/') >= 0:
            raise ValidationError('prefix should not contain slashes')

    def get_filename(self, filepath):
        if self.filename_solver == self.FILENAME_SOLVERS.remainder:
            return filepath.split('/')[(-1)]
        else:
            if self.filename_solver == self.FILENAME_SOLVERS.none:
                return
            raise ValueError('Something wrong with filename_solver value! processing of filename_solver "%s" is not implemented' % self.filename_solver)
            return

    def process(self, filepath):
        self.filepath = filepath
        self.disposition_header = ('attachment; filename={0}').format(self.get_filename(filepath))
        self.accel_path = os.path.join(self.internal_path, filepath)