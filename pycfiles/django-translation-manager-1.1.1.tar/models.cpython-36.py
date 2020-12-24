# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/hansek/projects/django-translation-manager/translation_manager/models.py
# Compiled at: 2020-01-20 12:29:58
# Size of source mod 2**32: 4990 bytes
import polib, os
from django.db import models
from django.template.defaultfilters import capfirst as cf
from django.utils.translation import ugettext_lazy as _
from .settings import get_settings

class TranslationEntry(models.Model):
    created = models.DateTimeField(auto_now_add=True, verbose_name=(_('admin-translation_entry-created-label')))
    changed = models.DateTimeField(auto_now=True, verbose_name=(_('admin-translation_entry-changed-label')))
    language = models.CharField(db_index=True, max_length=7, verbose_name=(_('admin-translation_entry-language-label')))
    original = models.TextField(verbose_name=(_('admin-translation_entry-original-label')))
    translation = models.TextField(blank=True, verbose_name=(_('admin-translation_entry-translation-label')))
    occurrences = models.TextField(blank=True, verbose_name=(_('admin-translation_entry-occurrences-label')))
    is_published = models.BooleanField(default=True, editable=False, verbose_name=(_('admin-translation_entry-is_published-label')))
    locale_path = models.CharField(db_index=True, max_length=256, verbose_name=(_('admin-translation_entry-locale_path-label')))
    locale_parent_dir = models.CharField(db_index=True, max_length=256, verbose_name=(_('admin-translation_entry-locale_parent_dir-label')))
    domain = models.CharField(db_index=True, max_length=256, verbose_name=(_('admin-translation_entry-domain-label')))

    class Meta:
        verbose_name = cf(_('admin-translation_entry-singular'))
        verbose_name_plural = cf(_('admin-translation_entry-plural'))
        ordering = ('original', )
        permissions = (
         (
          'load', _('admin-translation_entry-load-from-po')),)

    def __unicode__(self):
        return '(%s:%s:%s:%s)' % (self.pk, self.original[:64], self.language, self.locale_path)

    def __str__(self):
        return '(%s:%s:%s:%s)' % (self.pk, self.original[:64], self.language, self.locale_path)

    def get_hint(self):
        self.hint = ''
        if not self.hint:
            if hasattr(self, '_hint'):
                self.hint = self._hint
            else:
                try:
                    self.hint = self._meta.model.objects.get(domain=(self.domain), locale_path=(self.locale_path), original=(self.original), language=(get_settings('TRANSLATIONS_HINT_LANGUAGE'))).translation
                except self._meta.model.DoesNotExist:
                    pass

        return self.hint

    get_hint.short_description = cf(_('admin-translation_entry-hint-label'))


class RemoteTranslationEntry(models.Model):
    translation = models.TextField(blank=True, verbose_name=(_('admin-remote_translation_entry-remote_translation-label')))
    changed = models.DateTimeField(auto_now=True, verbose_name=(_('admin-remote_translation_entry-changed-label')))
    translation_entry = models.OneToOneField(TranslationEntry, related_name='remote_translation_entry', on_delete=(models.PROTECT))

    class Meta:
        permissions = (
         (
          'sync', _('admin-translation_entry-sync')),)


class ProxyTranslationEntry(TranslationEntry):

    class Meta:
        proxy = True


class TranslationBackup(models.Model):
    created = models.DateTimeField(auto_now_add=True, verbose_name=(_('admin-translation_backup-created-label')))
    changed = models.DateTimeField(auto_now=True, verbose_name=(_('admin-translation_backup-changed-label')))
    language = models.CharField(db_index=True, max_length=5, verbose_name=(_('admin-translation_backup-language-label')))
    locale_path = models.CharField(db_index=True, max_length=256, verbose_name=(_('admin-translation_backup-locale_path-label')))
    locale_parent_dir = models.CharField(db_index=True, max_length=256, verbose_name=(_('admin-translation_backup-locale_parent_dir-label')))
    domain = models.CharField(db_index=True, max_length=256, verbose_name=(_('admin-translation_backup-domain-label')))
    content = models.TextField(verbose_name=(_('admin-translation_backup-content')))

    class Meta:
        verbose_name = cf(_('admin-translation_backup-singular'))
        verbose_name_plural = cf(_('admin-translation_backup-plural'))
        ordering = ('-created', )

    def restore(self):
        po_filename = os.path.join(self.locale_path, self.language, 'LC_MESSAGES', self.domain + '.mo')
        mo_filename = os.path.join(self.locale_path, self.language, 'LC_MESSAGES', self.domain + '.mo')
        with open(po_filename, 'w') as (output):
            output.write(self.content.encode('utf-8'))
        po = polib.pofile(po_filename)
        po.save_as_mofile(mo_filename)

    def __unicode__(self):
        return '(%s:%s:%s)' % (self.pk, self.language, self.locale_path)

    def __str__(self):
        return '(%s:%s:%s)' % (self.pk, self.language, self.locale_path)