# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /var/www/transmanager/transmanager/models.py
# Compiled at: 2016-09-19 04:59:30
# Size of source mod 2**32: 9935 bytes
import logging, uuid
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import pre_save
from transmanager.signals import SignalBlocker
from django.utils.translation import gettext as _
from .utils import get_num_words
logger = logging.getLogger(__name__)

class TransLanguage(models.Model):
    code = models.CharField(max_length=2, verbose_name=_('Código'), help_text=_('Código ISO del idioma'))
    name = models.CharField(max_length=40, verbose_name=_('Nombre'))
    main_language = models.BooleanField(default=False, verbose_name=_('Idioma principal'), help_text=_('¿Es el idioma principal?'))

    class Meta:
        verbose_name = _('Idioma')
        verbose_name_plural = _('Idiomas')

    def __str__(self):
        return '{0}'.format(self.name)

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        """
        Overwrite of the save method in order that when setting the language
        as main we deactivate any other model selected as main before

        :param force_insert:
        :param force_update:
        :param using:
        :param update_fields:
        :return:
        """
        super().save(force_insert, force_update, using, update_fields)
        if self.main_language:
            TransLanguage.objects.exclude(pk=self.pk).update(main_language=False)


class TransUser(models.Model):
    user = models.OneToOneField(User, verbose_name=_('Usuario'), related_name='translator_user')
    languages = models.ManyToManyField(TransLanguage, verbose_name=_('Idiomas'))
    active = models.BooleanField(default=True, verbose_name=_('Activo'))

    class Meta:
        verbose_name = _('Traductor')
        verbose_name_plural = _('Traductores')

    def __str__(self):
        return '{0} - {1}'.format(self.user, _('Activo') if self.active else _('No activo'))

    def _languages(self):
        return ', '.join([lang.name for lang in self.languages.order_by('name')])

    _languages.short_description = _('Idiomas')


class TransTask(models.Model):
    user = models.ForeignKey(TransUser, verbose_name=_('Usuario'), related_name='tasks')
    language = models.ForeignKey(TransLanguage, verbose_name=_('Idioma'))
    object_class = models.CharField(verbose_name=_('Clase'), max_length=100, help_text=_('Clase del objeto'))
    object_pk = models.IntegerField(verbose_name=_('Clave'), help_text=_('Clave primária del objeto'))
    date_creation = models.DateTimeField(auto_now_add=True, verbose_name=_('Fecha creación'))
    date_modification = models.DateTimeField(auto_now=True, verbose_name=_('Fecha modificación'))
    notified = models.BooleanField(default=False, verbose_name=_('Notificada'), help_text=_('Si la tarea ya ha sido notificada o no al usuario'))
    date_notified = models.DateTimeField(blank=True, null=True, verbose_name=_('Fecha notificacion'))
    content_type = models.ForeignKey(ContentType, verbose_name=_('Modelo'), blank=True, null=True)
    object_name = models.CharField(verbose_name=_('Nombre objeto'), max_length=200)
    object_field = models.CharField(verbose_name=_('Nombre campo'), max_length=200, help_text=_('Nombre del atributo en el modelo'))
    object_field_label = models.CharField(verbose_name=_('Descripción campo'), max_length=200, help_text=_('Etiqueta del campo'))
    object_field_value = models.TextField(verbose_name=_('Valor'), help_text=_('Valor del campo en el idioma principal'))
    object_field_value_translation = models.TextField(verbose_name=_('Valor traducido'), blank=True, null=True, help_text=_('Valor traducido del campo en el idioma principal'))
    number_of_words = models.IntegerField(verbose_name=_('Número palabras'), default=0, help_text=_('Número de palabras a traducir en el idioma original'))
    done = models.BooleanField(default=False, verbose_name=_('Hecho'))

    class Meta:
        verbose_name = _('Tarea')
        verbose_name_plural = _('Tareas')
        ordering = [
         '-id']

    def __str__(self):
        return '{0} - {1} - {2} - {3} - {4}'.format(self.user, self.language, self.object_name, self.object_field, self.object_field_value)

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        self.number_of_words = get_num_words(self.object_field_value)
        super().save(force_insert, force_update, using, update_fields)
        if self.object_field_value_translation:
            if self.object_field_value_translation != '':
                app_label, model = self.get_natural_key()
                ct = ContentType.objects.get_by_natural_key(app_label, model)
                try:
                    item = ct.model_class().objects.language(self.language.code).get(pk=self.object_pk)
                except ObjectDoesNotExist:
                    try:
                        item = ct.model_class().objects.untranslated().get(pk=self.object_pk)
                    except ObjectDoesNotExist:
                        return

                    item.translate(self.language.code)

                with SignalBlocker(pre_save):
                    setattr(item, self.object_field, self.object_field_value_translation)
                    item.save()

    def get_natural_key(self):
        return (
         self.object_name.split('-')[0].strip(), self.object_class.lower().strip())

    def get_model_class(self):
        app_label, model = self.get_natural_key()
        try:
            ct = ContentType.objects.get_by_natural_key(app_label, model)
        except ContentType.DoesNotExist:
            return

        return ct.model_class()

    @property
    def has_value(self):
        return self.object_field_value_translation != '' and self.object_field_value_translation is not None


class TransApplicationLanguage(models.Model):
    application = models.CharField(max_length=100, verbose_name=_('Aplicación'), unique=True)
    languages = models.ManyToManyField(TransLanguage, verbose_name=_('Idiomas'), help_text=_('Idiomas por defecto de la aplicación'))

    class Meta:
        verbose_name = _('Idiomas por aplicación')
        verbose_name_plural = _('Idiomas por aplicaciones')

    def __str__(self):
        return self.application

    def _languages(self):
        return ', '.join([lang.name for lang in self.languages.order_by('name')])

    _languages.short_description = _('Idiomas')


class TransModelLanguage(models.Model):
    model = models.CharField(max_length=100, verbose_name=_('Modelo'), unique=True)
    languages = models.ManyToManyField(TransLanguage, verbose_name=_('Idiomas'), help_text=_('Idiomas por defecto del modelo'))

    class Meta:
        verbose_name = _('Idiomas por modelo')
        verbose_name_plural = _('Idiomas por modelos')

    def __str__(self):
        return self.model

    def _languages(self):
        return ', '.join([lang.name for lang in self.languages.order_by('name')])

    _languages.short_description = _('Idiomas')

    def get_model_class(self):
        app_label, model = self.model.split(' - ')
        try:
            ct_model = ContentType.objects.get_by_natural_key(app_label, model)
        except ContentType.DoesNotExist:
            return

        return ct_model.model_class()


class TransItemLanguage(models.Model):
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, verbose_name=_('Modelo'))
    object_id = models.PositiveIntegerField(verbose_name=_('Identificador'))
    content_object = GenericForeignKey('content_type', 'object_id')
    languages = models.ManyToManyField(TransLanguage, verbose_name=_('Idiomas'), help_text=_('Idiomas por defecto del item'))

    class Meta:
        verbose_name = _('Idiomas por item')
        verbose_name_plural = _('Idiomas por item')

    def __str__(self):
        return '{}'.format(self.content_object)

    def _languages(self):
        return ', '.join([lang.name for lang in self.languages.order_by('name')])

    _languages.short_description = _('Idiomas')


class TransUserExport(models.Model):

    def upload_path(self, filename):
        return 'user-exports/{}/{}'.format(self.user.id, filename)

    user = models.ForeignKey(User, verbose_name=_('user'), related_name='exports')
    file = models.FileField(upload_to=upload_path, blank=True, null=True, max_length=255)
    creation_date = models.DateTimeField(_('creation date'), auto_now_add=True)
    uuid = models.UUIDField(default=uuid.uuid4, verbose_name=_('Unique identifier'), unique=True)

    class Meta:
        verbose_name = _('User export')
        verbose_name_plural = _('User exports')

    def __str__(self):
        return '{} - {}'.format(self.user.id, self.file.name)