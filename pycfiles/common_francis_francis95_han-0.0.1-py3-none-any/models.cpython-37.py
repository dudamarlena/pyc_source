# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/marc/Git/common-framework/common/models.py
# Compiled at: 2019-11-25 04:25:34
# Size of source mod 2**32: 91592 bytes
import logging, pickle, time, uuid
import django.apps as apps
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractBaseUser, Group
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.core import serializers
import django.core.cache as cache
from django.core.exceptions import ValidationError, FieldDoesNotExist
from django.db import models
from django.db.models import query, Q
from django.db.models.deletion import Collector
from django.db.models.signals import m2m_changed, post_init, post_save, pre_delete, pre_save
from django.dispatch import receiver
import django.forms.models as django_model_to_dict
from django.utils.text import camel_case_to_spaces
from django.utils.timezone import now
import django.utils.translation as _
from rest_framework.renderers import JSONRenderer
try:
    from rest_framework_xml.renderers import XMLRenderer
except ImportError:
    XMLRenderer = None

try:
    from rest_framework_yaml.renderers import YAMLRenderer
except ImportError:
    YAMLRenderer = None

from common.fields import JsonField, PickleField, json_encode
import common.settings as settings
from common.utils import get_current_app, get_current_user, get_pk_field, merge_dict, timed_cache
logger = logging.getLogger(__name__)
app = get_current_app()

def to_boolean(label_field, sort_order=None):
    """
    Transforme une méthode en attribut booléen
    :param label_field: Libellé du champ affiché par l'administration
    :param sort_order: Champ utilisé pour trier cette donnée (facultatif)
    :return: Wrapper
    """

    def wrapper(boolean_field):
        boolean_field.boolean = True
        boolean_field.short_description = label_field
        if sort_order:
            boolean_field.admin_order_field = sort_order
        return boolean_field

    return wrapper


def get_content_type(model):
    """
    Récupère le content type d'un modèle
    :param model: Instance de modèle
    :return: Content type
    """
    content_type = getattr(model, '_content_type', None)
    if not content_type or content_type.model_class is not model:
        content_type = ContentType.objects.get_for_model(model)
        model._content_type = content_type
    return content_type


class Serialized(object):
    """Serialized"""

    def __init__(self, value, format='json'):
        self.format = format
        if isinstance(value, query.QuerySet):
            self.meta = value.model._meta
            self.count = value.count()
            self.query = str(value.query or ) or 
            self.single = False
        elif isinstance(value, models.Model):
            self.meta = value._meta
            self.count = 1
            self.query = None
            self.single = True
            value = [value]
        self.data = serializers.serialize(format, value)

    def deserialize(self):
        data = serializers.deserialize(self.format, self.data)
        objects = [item.object for item in data]
        if self.single:
            return next(iter(objects), None)
        return objects

    def __str__(self):
        return self.data

    def __repr__(self):
        return '[{format}] {object} ({count})'.format(format=(self.format),
          count=(self.count),
          object=(self.meta.object_name))


class CustomGenericForeignKey(GenericForeignKey):
    """CustomGenericForeignKey"""

    def __set__(self, instance, value):
        if value is None:
            ct = getattr(instance, self.ct_field, None)
            fk = getattr(instance, self.fk_field, None)
        else:
            ct = self.get_content_type(obj=value)
            fk = value._get_pk_val()
        setattr(instance, self.ct_field, ct)
        setattr(instance, self.fk_field, fk)
        self.set_cached_value(instance, value)


class MetaDataQuerySet(models.QuerySet):
    """MetaDataQuerySet"""

    def search(self, *, id=None, type=None, key=None, value=None, date=None, valid=True):
        """
        Effectue une recherche multi-critères dans les métadonnées
        :param id: instance de l'entité
        :param type: Type de l'entité concernée
        :param key: Clé de recherche
        :param value: Valeur après déserialisation
        :param date: Date de vérification (facultatif)
        :param valid: Uniquement les métadonnées valides ?
        :return: QuerySet
        """
        queryset = self
        if id:
            queryset = queryset.filter(object_id=id)
        elif type:
            if isinstance(type, int):
                queryset = queryset.filter(content_type_id=type)
            else:
                content_type = get_content_type(type)
                queryset = queryset.filter(content_type=content_type)
        if key:
            queryset = queryset.filter(key=key)
        if value:
            from common.utils import json_encode
            queryset = queryset.filter(value=json_encode(value, sort_keys=True))
        return queryset.select_valid(date=date, valid=valid)

    def select_valid(self, date=None, valid=True):
        """
        Sélectionne les éléments valides du QuerySet
        :param date: Date de vérification (facultatif)
        :param valid: Retourne les éléments valides ou invalides (valides par défaut)
        :return: QuerySet
        """
        if valid is None:
            return self
        function = self.filter if valid else self.exclude
        return function(Q(deletion_date__isnull=True) | Q(deletion_date__gte=(date or )))

    valid = property(select_valid)


class MetaData(models.Model):
    """MetaData"""
    content_type = models.ForeignKey(ContentType,
      on_delete=(models.CASCADE),
      related_name='+',
      verbose_name=(_("type d'entité")))
    object_id = models.TextField(verbose_name=(_('identifiant')))
    entity = CustomGenericForeignKey()
    key = models.CharField(max_length=100,
      verbose_name=(_('clé')))
    value = JsonField(blank=True,
      null=True,
      verbose_name=(_('valeur')))
    creation_date = models.DateTimeField(auto_now_add=True,
      verbose_name=(_('date de création')))
    modification_date = models.DateTimeField(auto_now=True,
      verbose_name=(_('date de modification')))
    deletion_date = models.DateTimeField(blank=True,
      null=True,
      verbose_name=(_('date de suppression')))
    objects = MetaDataQuerySet.as_manager()

    def __str__(self):
        return _('{key}: {value}').format(key=(self.key), value=(self.value))

    @property
    def valid(self):
        """
        Validité dans le temps de la métadonnée
        """
        return not self.deletion_date or 

    @staticmethod
    def get(instance, key=None, valid=True, raw=False, queryset=None):
        """
        Permet de récupérer une valeur de métadonnée à partir de sa clé depuis une instance
        :param instance: Instance du modèle
        :param key: Clé de recherche
        :param valid: Uniquement les données valides ?
        :param raw: Retourner les entités à la place des valeurs ?
        :param queryset: QuerySet de récupération des métadonnées
        :return: Valeur ou entité
        """
        assert getattr(instance, 'pk', None), _('Unable to get metadata from an unsaved model instance.')
        content_type = get_content_type(instance.__class__)
        queryset = queryset or 
        if valid:
            queryset = queryset.filter(Q(deletion_date=None) | Q(deletion_date__gte=(now())))
        if key:
            only = ('key', 'value', 'deletion_date') if raw else ('value', )
            metadata = (queryset.filter(key=key).only)(*only).first()
            return raw or metadata or 
            return metadata.value
        queryset = queryset.only('key', 'value').order_by('key')
        if raw:
            return queryset
        return {m.key:m.value for m in queryset}

    @staticmethod
    def set(instance, key, value, date=None, queryset=None):
        """
        Permet d'ajouter ou modifier une métadonnée
        :param instance: Instance du modèle
        :param key: Clé
        :param value: Valeur
        :param date: Date de péremption de la métadonnée
        :param queryset: QuerySet de récupération des métadonnées
        :return: Vrai en cas de succès, faux sinon
        """
        assert getattr(instance, 'pk', None), _('Unable to set metadata for an unsaved model instance.')
        content_type = get_content_type(instance.__class__)
        try:
            queryset = queryset or 
            metadata = queryset.only('value', 'deletion_date').get(key=key)
            metadata.deletion_date = date
            metadata.value = value
            metadata.save(update_fields=('value', 'deletion_date'))
        except MetaData.DoesNotExist:
            metadata = MetaData(content_type=content_type,
              object_id=(instance.pk),
              key=key,
              value=value,
              deletion_date=date)
            metadata.save()

        return metadata

    @staticmethod
    def add(instance, key, value, allow_duplicate=True, queryset=None):
        """
        Permet d'ajouter une valeur à une métadonnée existante
        :param instance: Instance du modèle
        :param key: Clé
        :param value: Valeur
        :param allow_duplicate: Autorise l'ajout de doublons dans les listes de valeur (par défaut)
        :param queryset: QuerySet de récupération des métadonnées
        :return: Métadonnée
        """
        assert getattr(instance, 'pk', None), _('Unable to set metadata for an unsaved model instance.')
        metadata = MetaData.get(instance, key=key, queryset=queryset, raw=True)
        if metadata:
            if isinstance(value, dict) and isinstance(metadata.value, dict):
                metadata.value.update(value)
            elif isinstance(metadata.value, list):
                values = metadata.value
                if isinstance(value, (list, tuple, set, frozenset)):
                    values.extend(list(value))
                else:
                    values.append(value)
                metadata.value = values if allow_duplicate else set(values)
            else:
                metadata.value += value
            metadata.save(update_fields=('value', ))
            return metadata
        value = value if isinstance(value, (list, tuple, set, frozenset, dict)) else [value]
        return MetaData.set(instance, key=key, value=value, queryset=queryset)

    @staticmethod
    def remove(instance, key=None, logic=False, date=None, queryset=None):
        """
        Permet de supprimer une ou toutes les métadonnées
        :param instance: Instance du modèle
        :param key: Clé
        :param logic: Suppression logique ?
        :param date: Date de péremption de la métadonnée
        :param queryset: QuerySet de récupération des métadonnées
        :return: Vrai en cas de succès, faux sinon
        """
        assert getattr(instance, 'pk', None), _('Unable to delete metadata from an unsaved model instance.')
        content_type = get_content_type(instance.__class__)
        queryset = queryset or 
        if key:
            queryset = queryset.filter(key=key)
        if logic:
            date = date or 
            for metadata in queryset.only('deletion_date').all():
                metadata.deletion_date = date
                metadata.save(update_fields=('deletion_date', ))

        else:
            queryset.all().delete()

    class Meta:
        verbose_name = _('métadonnée')
        verbose_name_plural = _('métadonnées')
        unique_together = ('content_type', 'object_id', 'key')
        index_together = (('content_type', 'object_id'), ('content_type', 'object_id', 'deletion_date'),
                          ('content_type', 'object_id', 'deletion_date', 'key'))


class CommonQuerySet(models.QuerySet):
    """CommonQuerySet"""

    def serialize(self, format='json'):
        """
        Permet de serialiser le QuerySet
        :param format: Format de sérialisation
        :return: QuerySet serialisée
        """
        return Serialized(self, format=format)

    def to_dict(self, *args, **kwargs):
        """
        Retourne l'ensemble des entités du QuerySet sous forme de dictionnaire
        :return: Liste de dictionnaires
        """
        return [(item.to_dict)(*args, **kwargs) if isinstance(item, CommonModel) else item for item in self]

    def __json__(self):
        """
        Représentation de l'instance sous forme de dictionnaire pour sérialisation JSON
        :return: dict
        """
        return [item.__json__() if isinstance(item, CommonModel) else item for item in self]


class CommonModel(models.Model):
    """CommonModel"""
    metadata = GenericRelation(MetaData)
    objects = CommonQuerySet.as_manager()
    _copy = {}
    _copy_m2m = {}
    _content_type = None

    def validate_unique(self, exclude=None):
        """
        Surcharge de la validation de l'unicité pour les index uniques composés de champs nuls
        :param exclude: Champs à exclure de la validation
        """
        model = type(self)
        for unique_together in model._meta.unique_together:
            queryset = model.objects.exclude(pk=(self.pk)) if self.pk else model.objects.all()
            fields = []
            has_null = False
            for field_name in unique_together:
                fields.append(field_name)
                value = getattr(self, field_name, None)
                field = model._meta.get_field(field_name)
                if field.null and value is None:
                    queryset = (queryset.filter)(**{field_name + '__isnull': True})
                    has_null = True
                else:
                    queryset = (queryset.filter)(**{field_name: value})

            if has_null and queryset.count() > 0:
                raise ValidationError(self.unique_error_message(model, fields))

        super().validate_unique(exclude)

    def update(self, exclude=None):
        """
        Permet de mettre à jour un enregistrement existant à partir des données d'une instance
        :param exclude: Champs à exclure de la modification
        :return: Nombre d'enregistrements modifiés
        """
        exclude = exclude or 
        non_unique_fields = set()
        unique_fields = set()
        model = type(self)
        for unique_together in model._meta.unique_together:
            unique_fields.update(unique_together)

        for field in model._meta.fields:
            if field.auto_created or field.editable:
                if field.name in exclude:
                    continue
                if field.unique:
                    unique_fields.add(field.name)
                else:
                    non_unique_fields.add(field.name)

        assert unique_fields, _('Unable to update an instance which have no unique fields.')
        queryset = (model.objects.filter)(**)
        count = (queryset.update)(**)
        if count:
            self.pk = queryset.first().pk
            self.refresh_from_db()
        return count

    def save(self, *args, force_insert=False, _full_update=False, **kwargs):
        """
        Sauvegarde l'instance du modèle
        """
        if not self._state.adding:
            if not _full_update:
                if not force_insert:
                    if self._meta.pk.name not in self.modified:
                        kwargs['update_fields'] = update_fields = set(kwargs.pop('update_fields', self.modified.keys()))
                        update_fields.update([field.name for field in self._meta.fields if getattr(field, 'auto_now', None)])
        return (super().save)(args, force_insert=force_insert, **kwargs)

    def get_metadata(self, key=None, valid=True, raw=False):
        """
        Permet de récupérer une valeur de métadonnée à partir de sa clé
        :param key: Clé de recherche
        :param valid: Uniquement les données valides ?
        :param raw: Retourner les entités à la place des valeurs ?
        :return: Valeur ou entité
        """
        return MetaData.get(self, key=key, valid=valid, raw=raw, queryset=(self.metadata))

    def set_metadata(self, key, value, date=None):
        """
        Permet d'ajouter ou modifier une métadonnée
        :param key: Clé
        :param value: Valeur
        :param date: Date de péremption de la métadonnée
        :return: Vrai en cas de succès, faux sinon
        """
        return MetaData.set(self, key=key, value=value, date=date, queryset=(self.metadata))

    def add_metadata(self, key, value, allow_duplicate=True):
        """
        Permet d'ajouter une valeur à une métadonnée existante
        :param key: Clé
        :param value: Valeur
        :param default: Valeur par défaut si la métadonnée n'existe pas (facultatif)
        :param allow_duplicate: Autorise l'ajout de doublons dans les listes de valeur (par défaut)
        :return: Métadonnée
        """
        return MetaData.add(self, key=key, value=value, allow_duplicate=allow_duplicate, queryset=(self.metadata))

    def del_metadata(self, key=None, logic=False, date=None):
        """
        Permet de supprimer une métadonnée
        :param key: Clé
        :param logic: Suppression logique ?
        :param date: Date de péremption de la métadonnée
        :return: Vrai en cas de succès, faux sinon
        """
        return MetaData.remove(self, key=key, logic=logic, date=date, queryset=(self.metadata))

    def to_dict(self, includes=None, excludes=None, editables=False, uids=False, metadata=False, names=False, types=False, display=False, labels=False, fks=False, m2m=False, no_ids=False, no_empty=False, functions=None, extra=None, raw=False, **kwargs):
        """
        Retourne la représentation d'une entité sous forme de dictionnaire
        :param includes: Attributs à inclure (liste ou dictionnaire)
        :param excludes: Attributs à exclure (liste ou dictionnaire)
        :param editables: Inclure les valeurs des attributs non éditables ?
        :param uids: Inclure les identifiants uniques de toutes les entités liées ?
        :param metadata: Inclure les métadonnées ?
        :param names: Inclure les informations textuelles du modèle ?
        :param types: Inclure le type d'entité ?
        :param display: Inclure le libellé de l'attribut s'il existe ?
        :param labels: Utiliser le libellé du champ à la place de son code ?
        :param fks: Inclure les éléments liés via les clés étrangères ?
        :param m2m: Inclure les identifiants des relations ManyToMany liées ?
        :param no_ids: Ne pas inclure les identifiants des clés primaires et les identifiants des clés étrangères ?
        :param no_empty: Ne pas inclure les données vides ou nulles ?
        :param functions: Exécuter et inclure le résultat d'une ou plusieurs fonctions ?
        Les fonctions doivent être de la forme suivante :
        [ (nom_champ, nom_fonction, [arg1, arg2, ...], {kwarg1: valeur, kwargs2: valeur, ...} ]
        :param extra: Liste d'attributs supplémentaires à récupérer (ou vrai pour tous les attributs hors modèle)
        :param raw: Ne pas chercher à retourner des valeurs serialisables ?
        :return: Dictionnaire
        """
        data = {}
        meta = self._meta
        keywords = dict(editables=editables,
          uids=uids,
          metadata=metadata,
          names=names,
          types=types,
          display=display,
          labels=labels,
          fks=fks,
          m2m=m2m,
          no_ids=no_ids,
          no_empty=no_empty)
        if isinstance(includes, dict):
            keywords.update(includes=includes)
            includes = set(includes.get('__all__') or ) | set(includes.get(meta.model) or )
        if isinstance(excludes, dict):
            keywords.update(excludes=excludes)
            excludes = set(excludes.get('__all__') or ) | set(excludes.get(meta.model) or )
        keywords.update(kwargs)
        is_empty = lambda value:         if isinstance(value, (int, float, complex, bool)):
False # Avoid dead code: not bool(value)
        if names:
            data.update(_label=(str(self)),
              _model=dict(object_name=(meta.object_name),
              model_name=(meta.model_name),
              app_label=(meta.app_label),
              verbose_name=(str(meta.verbose_name) if meta.verbose_name else None),
              verbose_name_plural=(str(meta.verbose_name_plural) if meta.verbose_name_plural else None)))
        if types:
            data_type = model_to_dict((get_content_type(self)), **keywords)
            data_type.pop('_state', None)
            data.update(_content_type=data_type)
        deferred_fields = self.get_deferred_fields()
        for field in meta.concrete_fields + meta.many_to_many:
            if field.attname in deferred_fields:
                continue
            elif not editables:
                if not getattr(field, 'editable', editables):
                    continue
                else:
                    if includes:
                        if field.name not in includes:
                            continue
                    if excludes:
                        if field.name in excludes:
                            continue
                        field_name = str(field.verbose_name or ) if labels else field.name
                        if isinstance(field, models.ManyToManyField):
                            if not m2m:
                                continue
                    else:
                        if self.pk is None:
                            data[field_name] = []
                    value = field.value_from_object(self)
                    related = field.related_model
                    if not no_ids:
                        result = [v.pk for v in value]
                        data[field_name + str(_(' (IDs)') if labels else '_ids')] = result or no_empty or 
                    if fks:
                        result = [model_to_dict(v, **keywords) for v in value]
                        data[field_name] = result or no_empty or 
                        for item in result:
                            item.pop('_state', None)

                if uids:
                    if issubclass(related, Entity):
                        result = [v.uuid for v in value]
                        data[field_name + str(_(' (UIDs)') if labels else '_uids')] = result or no_empty or 
                    else:
                        value = field.value_from_object(self)
                        if field.primary_key:
                            if no_ids:
                                continue
                        if isinstance(field, (models.ForeignKey, models.OneToOneField)):
                            if not no_ids:
                                data[field_name + str(_(' (ID)')) if labels else field.attname] = value
                            if fks or uids:
                                fk = getattr(self, field.name, None)
                                if fks:
                                    if fk:
                                        data[field_name] = model_to_dict(fk, **keywords)
                                        data[field_name].pop('_state', None)
                                if uids and isinstance(fk, Entity):
                                    data[field_name + str(_(' (UID)') if labels else '_uid')] = fk.uuid
            elif value is None:
                data[field_name] = no_empty or None
            elif isinstance(field, JsonField):
                result = value if raw else json_encode(value, sort_keys=True)
                data[field_name] = result or no_empty or 
            elif isinstance(field, PickleField):
                result = value if raw else pickle.dumps(value)
                data[field_name] = result or no_empty or 
            elif isinstance(field, (models.FileField, models.ImageField)):
                result = (value if raw else getattr(value, 'url', None)) if value else None
                data[field_name] = result or no_empty or 
            elif isinstance(value, (list, set, tuple)):
                result = list(value) if raw else ','.join((str(val) for val in value))
                data[field_name] = result or no_empty or 
            elif hasattr(self, 'get_{}_json'.format(field.name)):
                result = getattr(self, 'get_{}_json'.format(field.name))()
                data[field_name] = result or no_empty or 
            else:
                data[field_name] = is_empty(value) and no_empty or 
            if display:
                if hasattr(self, 'get_{}_display'.format(field.name)):
                    result = getattr(self, 'get_{}_display'.format(field.name))()
                    data[field_name + str(_(' (libellé)') if labels else '_display')] = result or no_empty or 

        if metadata:
            current_metadata = self.get_metadata()
            data['metadata'] = current_metadata or no_empty or 
        if functions:
            for key, func_name, func_args, func_kwargs in functions:
                result = (getattr(self, func_name))(*func_args, **func_kwargs)
                if is_empty(result):
                    data[key] = no_empty or 

        if extra:
            if extra is True:
                extra = set(self.__dict__) - set(meta.model().__dict__)
            for field in extra:
                if field in data:
                    continue
                item = getattr(self, field, None)
                if isinstance(item, list):
                    if item:
                        if isinstance(item[0], Entity):
                            data[field] = [(i.to_dict)(**keywords) for i in item]
                if isinstance(item, (CommonModel, CommonQuerySet)):
                    data[field] = (item.to_dict)(**keywords)
                elif isinstance(item, dict):
                    for key, value in item.items():
                        if key in data:
                            if is_empty(value):
                                if not no_empty:
                                    continue
                            if isinstance(value, (CommonModel, CommonQuerySet)):
                                data[key] = (value.to_dict)(**keywords)
                            else:
                                data[key] = value

                else:
                    data[field] = is_empty(item) and no_empty or 

        return data

    def m2m_to_dict(self, raw=False):
        """
        Retourne toutes les relations de type ManyToMany classées par attribut
        :param raw:
        :return: Dictionnaire
        """
        data = {}
        if self.pk is None:
            return data
        meta = self._meta
        for field in meta.many_to_many:
            if raw:
                value = field.value_from_object(self)
                data[field.name] = value
            else:
                data[field.name] = list(getattr(self, field.name).values_list('pk', flat=True))

        return data

    def related_to_dict(self, includes=None, excludes=None, valid=True, date=None, **kwargs):
        """
        Retourne toutes les relations de type related set classées par attribut
        :param includes: Relations à inclure
        :param excludes: Relations à exclure
        :param valid: Récupérer les éléments valides ?
        (entités périssables uniquement, la valeur nulle pour tous)
        :param date: Date de référence pour la validation des éléments
        (entités périssables uniquement, la valeur nulle pour la date et l'heure du jour)
        :param kwargs: Arguments complémentaires, principalement pour l'appel interne à 'to_dict()'
        :return: Dictionnaire
        """
        data = {}
        if self.pk is None:
            return data
        meta = self._meta
        for field in meta.get_fields():
            if not field.one_to_many:
                if field.one_to_one:
                    if not field.auto_created:
                        continue
                    else:
                        field_name = field.get_accessor_name()
                        model = field.model
                        if includes:
                            if field_name not in includes:
                                continue
                        if excludes and field_name in excludes:
                            continue
                    queryset = getattr(self, field_name)
                    if issubclass(model, PerishableEntity):
                        queryset = queryset.select_valid(valid=valid, date=date)
                data[field_name] = (queryset.all().to_dict)(**kwargs)

        return data

    def serialize(self, format='json'):
        """
        Permet de serialiser l'entité
        :param format: Format de sérialisation
        :return: Entité serialisée
        """
        return Serialized(self, format=format)

    def get_modified(self, **options):
        """
        Retourne l'ensemble des modifications effectuées sur l'entité
        :param options: Paramètres de la fonction .to_dict()
        :return: Set structuré par (champ, (valeur avant, valeur après))
        """
        old_data = self._copy
        if options:
            old_data = ((type(self))(**self._copy).to_dict)(**options)
        new_data = (self.to_dict)(**options)
        keys = set(old_data.keys()) | set(new_data.keys())
        return {k:(old_data.get(k), new_data.get(k)) for k in keys if old_data.get(k) != new_data.get(k)}

    @property
    def modified(self):
        """
        Retourne l'ensemble des modifications effectuées sur l'entité
        """
        return self.get_modified(editables=True)

    @property
    def m2m_modified(self):
        """
        Retourne les identifiants modifiés sur les relations de type many-to-many de l'entité
        """
        old_data, new_data = self._copy_m2m, self.m2m_to_dict()
        keys = set(old_data.keys()) | set(new_data.keys())
        return {k:(old_data.get(k), new_data.get(k)) for k in keys if old_data.get(k) != new_data.get(k)}

    @staticmethod
    def _model_type(obj):
        obj._content_type = obj._content_type or 
        return obj._content_type

    @property
    def model_type(self):
        return self._model_type(self.__class__)

    @classmethod
    def get_model_type(cls):
        return cls._model_type(cls)

    def has_webhook(self, status=None):
        """
        Permet de déterminer si ce type d'entité est couvert par un ou plusieurs webhooks
        :param status: (Facultatif) Statut
        :return: Vrai ou faux
        """
        key = 'WEBHOOK_{}_{}_{}'.format(self._meta.app_label, self._meta.object_name, status or )
        result = cache.get(key)
        if not result:
            filters = dict(types__in=[self.model_type])
            if status:
                filters.update({Webhook.STATUS_FILTERS.get(status): True})
            result = (Webhook.objects.filter)(**filters).exists()
            cache.set(key, result, timeout=3600)
        return result

    def __json__(self):
        """
        Représentation de l'instance sous forme de dictionnaire pour sérialisation JSON
        :return: dict
        """
        data = self.to_dict(editables=True, types=True)
        data.update(_copy=(self._copy), _copy_m2m=(self._copy_m2m))
        return data

    class Meta:
        abstract = True


class HistoryCommon(CommonModel):
    """HistoryCommon"""
    creation_date = models.DateTimeField(auto_now_add=True,
      editable=False,
      verbose_name=(_('date')))
    restoration_date = models.DateTimeField(blank=True,
      null=True,
      editable=False,
      verbose_name=(_('dernière restauration')))
    restored = models.NullBooleanField(editable=False,
      verbose_name=(_('restauré')))
    data = JsonField(blank=True,
      null=True,
      editable=False,
      verbose_name=(_('données')))
    data_size = models.PositiveIntegerField(editable=False,
      verbose_name=(_('taille données')))

    class Meta:
        abstract = True


class History(HistoryCommon):
    """History"""
    CREATE = 'C'
    UPDATE = 'U'
    DELETE = 'D'
    RESTORE = 'R'
    M2M = 'M'
    LOG_STATUS = (
     (
      CREATE, _('Création')),
     (
      UPDATE, _('Modification')),
     (
      DELETE, _('Suppression')),
     (
      RESTORE, _('Restauration')),
     (
      M2M, _('Many-to-many')))
    user = models.ForeignKey((settings.AUTH_USER_MODEL),
      blank=True,
      null=True,
      editable=False,
      on_delete=(models.SET_NULL),
      related_name='histories',
      verbose_name=(_('utilisateur')))
    status = models.CharField(max_length=1,
      choices=LOG_STATUS,
      editable=False,
      verbose_name=(_('statut')))
    content_type = models.ForeignKey(ContentType,
      blank=True,
      null=True,
      editable=False,
      on_delete=(models.CASCADE),
      related_name='+',
      verbose_name=(_("type d'entité")))
    object_id = models.TextField(editable=False,
      verbose_name=(_('identifiant')))
    object_uid = models.UUIDField(editable=False,
      verbose_name=(_('UUID')))
    object_str = models.TextField(editable=False,
      verbose_name=(_('entité')))
    reason = models.TextField(blank=True,
      null=True,
      editable=False,
      verbose_name=(_('motif')))
    admin = models.BooleanField(default=False,
      editable=False,
      verbose_name=(_('admin')))
    collector_update = JsonField(blank=True,
      null=True,
      editable=False,
      verbose_name=(_('mises à jour')))
    collector_delete = JsonField(blank=True,
      null=True,
      editable=False,
      verbose_name=(_('suppressions')))
    entity = CustomGenericForeignKey()
    _model = None

    @property
    def model(self):
        if self.content_type:
            self._model = self._model or 
            return self._model

    def __str__(self):
        return _('[{status}] {content_type} #{object_id}').format(status=(self.get_status_display()),
          content_type=(self.content_type),
          object_id=(self.object_id))

    def restore(self, *, ignore_log=None, current_user=None, reason=None, force_default=False, from_admin=None, all_fields=False, override=None):
        """
        Permet de restaurer complètement une entité
        :param ignore_log: Ignorer l'historisation ?
        :param current_user: Utilisateur à l'origine de la restauration
        :param reason: Message d'information associé à l'historique de restauration
        :param force_default: Force le comportement par défaut de la sauvegarde ?
        :param from_admin: Indique que la restauration a été demandée via l'interface d'administration ?
        :param all_fields: Restaurer également les données non éditables ?
        :param override: Surcharge des données de la restauration
        """
        try:
            try:
                data = self.data
                data.update(override or )
                entity = self.entity
                if not entity:
                    entity = self.content_type.model_class()()
                if not data:
                    self.restored = False
                    return self.restored
                for field_name, value in data.items():
                    try:
                        field = entity._meta.get_field(field_name)
                        if not all_fields:
                            if not field.editable:
                                continue
                        value = field.to_python(value)
                    except FieldDoesNotExist:
                        continue

                    setattr(entity, field_name, value)

                entity._from_admin = from_admin
                entity._restore = True
                entity.save(_current_user=(current_user or ), _ignore_log=ignore_log,
                  _reason=reason,
                  _force_default=force_default)
                if entity.pk:
                    for field in entity._meta.many_to_many:
                        try:
                            value = data.get(field.name, []) or 
                            if not value:
                                continue
                            getattr(entity, field.name).set(value)
                        except Exception as error:
                            try:
                                logger.warning(error, exc_info=True)
                                continue
                            finally:
                                error = None
                                del error

                    for model_label, fields in (self.collector_update or ).items():
                        try:
                            model = apps.get_model(model_label)
                            for field_name, values in fields.items():
                                filters = Q(**{field_name + '__isnull': True})
                                if all((isinstance(v, str) for v in values)):
                                    filters |= Q(**{field_name: ''})
                                (model.objects.filter(filters, pk__in=values).update)(**{field_name: entity.pk})

                        except Exception as error:
                            try:
                                logger.warning(error, exc_info=True)
                                continue
                            finally:
                                error = None
                                del error

                    for model_label, datas in (self.collector_delete or ).items():
                        try:
                            model = apps.get_model(model_label)
                            for data in datas:
                                data = {key if key.endswith('_id') else key + '_id':value for key, value in data.items()}
                                (model.objects.get_or_create)(**data)

                        except Exception as error:
                            try:
                                logger.warning(error, exc_info=True)
                                continue
                            finally:
                                error = None
                                del error

                self.restored = True
            except Exception as error:
                try:
                    logger.warning(error, exc_info=True)
                    self.restored = False
                    raise
                finally:
                    error = None
                    del error

        finally:
            self.restoration_date = now()
            self.save()

        return self.restored

    class Meta:
        verbose_name = _('historique')
        verbose_name_plural = _('historiques')
        index_together = ('content_type', 'object_id')


class HistoryField(HistoryCommon):
    """HistoryField"""
    CLEAR_M2M = 'C'
    ADD_M2M = 'A'
    REMOVE_M2M = 'R'
    LOG_STATUS_M2M = (
     (
      CLEAR_M2M, _('Purge')),
     (
      ADD_M2M, _('Ajout')),
     (
      REMOVE_M2M, _('Suppression')))
    history = models.ForeignKey('History',
      editable=False,
      on_delete=(models.CASCADE),
      related_name='fields',
      verbose_name=(_('historique')))
    field_name = models.CharField(max_length=100,
      editable=False,
      verbose_name=(_('nom du champ')))
    old_value = models.TextField(blank=True,
      null=True,
      editable=False,
      verbose_name=(_('ancienne valeur')))
    new_value = models.TextField(blank=True,
      null=True,
      editable=False,
      verbose_name=(_('nouvelle valeur')))
    status_m2m = models.CharField(max_length=1,
      blank=True,
      null=True,
      editable=False,
      choices=LOG_STATUS_M2M,
      verbose_name=(_('statut M2M')))
    editable = models.BooleanField(default=True,
      editable=False,
      verbose_name=(_('éditable')))
    _field = None

    @property
    def field(self):
        if self.history.model:
            self._field = self._field or 
            return self._field

    @property
    def old_inner_value(self):
        return self._get_inner_value(self.old_value)

    @property
    def new_inner_value(self):
        return self._get_inner_value(self.new_value)

    def _get_inner_value(self, value):
        if value is None:
            return
        try:
            if self.field.many_to_many:
                model = self.field.related_model
                return [self.get_instance(model, val) or  for val in value.split(' | ')]
            value = self.field.to_python(value)
            if isinstance(value, str):
                if not value:
                    return
            if self.field.choices:
                instance = (self.history.model)(**{self.field_name: value})
                return getattr(instance, 'get_{}_display'.format(self.field_name))() or 
            if self.field.related_model:
                instance = self.get_instance(self.field.related_model, value)
                return instance or 
        except Exception as error:
            try:
                logger.warning(error, exc_info=True)
            finally:
                error = None
                del error

        return value

    @staticmethod
    @timed_cache(days=1)
    def get_instance(model, value):
        return model.objects.filter(pk=value).first()

    def __str__(self):
        return _('[{entity}] ({field}) {old} ~ {new}').format(entity=(self.history.content_type),
          field=(self.field_name),
          old=(self.old_value),
          new=(self.new_value))

    def restore(self, *, ignore_log=None, current_user=None, reason=None, force_default=False, from_admin=None, override=None, **kwargs):
        """
        Permet de restaurer un champ d'une entité
        :param ignore_log: Ignorer l'historisation ?
        :param current_user: Utilisateur à l'origine de la restauration
        :param reason: Message d'information associé à l'historique de restauration
        :param force_default: Force le comportement par défaut de la sauvegarde ?
        :param from_admin: Indique que la restauration a été demandée via l'interface d'administration ?
        :param override: Surcharge des données de la restauration
        """
        try:
            try:
                data = self.data
                if isinstance(data, dict):
                    data.update(override or )
                elif override:
                    data = override
                entity = self.history.entity
                if not entity:
                    self.restored = False
                    return self.restored
                else:
                    field = entity._meta.get_field(self.field_name)
                    value = field.to_python(data)
                    if self.status_m2m:
                        getattr(entity, self.field_name).set(value)
                    else:
                        setattr(entity, self.field_name, value)
                entity._from_admin = from_admin
                entity._restore = True
                entity.save(_current_user=(current_user or ), _ignore_log=ignore_log,
                  _reason=reason,
                  _force_default=force_default)
                self.restored = True
            except Exception as error:
                try:
                    logger.warning(error, exc_info=True)
                    self.restored = False
                    raise
                finally:
                    error = None
                    del error

        finally:
            self.restoration_date = now()
            self.save()

        return self.restored

    class Meta:
        verbose_name = _('historique de champ modifié')
        verbose_name_plural = _('historiques de champs modifiés')


class GlobalManager(models.Manager):
    """GlobalManager"""

    def entity(self, uuid):
        """
        Récupération directe d'une entité à partir de son identifiant unique
        """
        try:
            return self.get(object_uid=uuid).entity
        except Exception:
            return


class Global(models.Model):
    """Global"""
    content_type = models.ForeignKey(ContentType,
      editable=False,
      on_delete=(models.CASCADE),
      related_name='+',
      verbose_name=(_("type d'entité")))
    object_id = models.TextField(editable=False,
      verbose_name=(_('identifiant')))
    object_uid = models.UUIDField(unique=True,
      editable=False,
      verbose_name=(_('UUID')))
    entity = CustomGenericForeignKey()
    objects = GlobalManager()

    def __str__(self):
        return _('({object_uid}) {content_type} #{object_id}').format(object_uid=(self.object_uid),
          content_type=(self.content_type),
          object_id=(self.object_id))

    class Meta:
        verbose_name = _('globale')
        verbose_name_plural = _('globales')
        unique_together = ('content_type', 'object_id')


class EntityQuerySet(CommonQuerySet):
    """EntityQuerySet"""
    _ignore_log = False
    _current_user = None
    _reason = None
    _from_admin = False
    _force_default = False

    def delete(self, _ignore_log=None, _current_user=None, _reason=None, _force_default=False):
        """
        Surcharge de la suppression des entités du QuerySet
        :param _ignore_log: Ignorer l'historique de suppression ?
        :param _current_user: Utilisateur à l'origine de la suppression
        :param _reason: Raison de la suppression
        :param _force_default: Force la suppression directe ?
        """
        if _force_default or self._force_default:
            return super().delete()
        assert self.query.can_filter(), _("Cannot use 'limit' or 'offset' with delete.")
        if self._fields is not None:
            raise TypeError(_('Cannot call delete() after .values() or .values_list()'))
        del_query = self._clone()
        for element in del_query:
            element._ignore_log = _ignore_log or 
            element._current_user = _current_user or 
            element._reason = _reason or 
            element._from_admin = self._from_admin

        del_query._for_write = True
        del_query.query.select_for_update = False
        del_query.query.select_related = False
        del_query.query.clear_ordering(force_empty=True)
        collector = Collector(using=(del_query.db))
        collector.collect(del_query)
        self._collector_update = {key._meta.label:{field.name:[instance.pk for instance in instances] for (field, value), instances in value.items()} for key, value in collector.field_updates.items()}
        self._collector_delete = {key._meta.label:[model_to_dict(value, exclude='id') for value in values] for key, values in collector.data.items() if key._meta.auto_created if key._meta.auto_created}
        deleted, _rows_count = collector.delete()
        self._result_cache = None
        return (
         deleted, _rows_count)

    def create(self, _ignore_log=None, _current_user=None, _reason=None, _force_default=False, **kwargs):
        """
        Surcharge de la création d'entités
        :param _ignore_log: Ignorer l'historique de création ?
        :param _current_user: Utilisateur à l'origine de la création
        :param _reason: Raison de la création
        :param _force_default: Force la suppression directe ?
        """
        if _force_default:
            return (super().create)(**kwargs)
        obj = (self.model)(**kwargs)
        obj.save(force_insert=True, using=(self.db), _ignore_log=_ignore_log,
          _current_user=(_current_user or ),
          _reason=_reason)
        return obj

    def distinct_on_fields(self, *fields, order_by=False):
        """
        Permet de faire un distinct sur un/des champs précis du modèle sur tous les backends
        (pgsql est le seul backend à supporter le distinct on fields, cependant, il ne permet pas l'order_by ensuite)
        :param fields: Liste des champs sur lequel appliquer le distinct
        :param order_by: Indique si le QuerySet sera suivi ou non d'un order_by sur des champs différents
        :return: QuerySet
        """
        from django.db import connection
        if not order_by:
            if connection.vendor == 'postgresql':
                return (self.distinct)(*fields)
        from django.db.models import Max, Q
        groups = (self.values)(*fields).annotate(max_modification_date=(Max('modification_date')))
        filters = Q()
        for item in groups:
            field_filter = {field:item[field] for field in fields if field != 'modification_date'}
            filters |= Q(modification_date=item['max_modification_date'], **field_filter)

        return self.filter(filters)

    def get_by_natural_key(self, *args, **kwargs):
        """
        Recherche une instance du modèle par sa clé naturelle
        :param natural_key: Clé naturelle (par défaut l'UUID de l'instance)
        :return: Instance du modèle
        """
        return (self.get)(**dict(zip(self.model._natural_key, args)))


class Entity(CommonModel):
    """Entity"""
    uuid = models.UUIDField(default=(uuid.uuid4),
      editable=False,
      unique=True,
      verbose_name=(_('UUID')))
    creation_date = models.DateTimeField(auto_now_add=True,
      verbose_name=(_('date de création')))
    modification_date = models.DateTimeField(auto_now=True,
      verbose_name=(_('date de modification')))
    current_user = models.ForeignKey((settings.AUTH_USER_MODEL),
      blank=True,
      null=True,
      editable=False,
      on_delete=(models.SET_NULL),
      related_name='+',
      verbose_name=(_('dernier utilisateur')))
    globals = GenericRelation(Global)
    objects = EntityQuerySet.as_manager()
    _ignore_log = False
    _ignore_global = False
    _current_user = None
    _reason = None
    _from_admin = False
    _restore = False
    _force_default = False
    _history = None
    _init = False
    _collector_update, _collector_delete = (None, None)
    _natural_key = ('uuid', )

    def save(self, *args, _ignore_log=None, _current_user=None, _reason=None, _force_default=False, force_insert=False, **kwargs):
        """
        Surcharge de la sauvegarde de l'entité
        :param _ignore_log: Ignorer l'historique de modification ?
        :param _current_user: Utilisateur à l'origine de la modification
        :param _reason: Raison de la modification
        :param _force_default: Force le comportement par défaut ?
        :param force_insert: Force l'insertion même en cas de présence d'une PK ?
        """
        self.uuid = self.uuid or 
        if _force_default or self._force_default:
            return (super().save)(args, force_insert=force_insert, **kwargs)
        self._ignore_log = _ignore_log or 
        self._current_user = self.current_user = _current_user or 
        self._reason = _reason or 
        self._force_default = _force_default or 
        if force_insert:
            self.pk = self.id = None
            self.uuid = uuid.uuid4()
        return (super().save)(args, force_insert=force_insert, **kwargs)

    def delete(self, *args, _ignore_log=None, _current_user=None, _reason=None, _force_default=False, keep_parents=False, **kwargs):
        """
        Surcharge de la suppression de l'entité
        :param _ignore_log: Ignorer l'historique de suppression ?
        :param _current_user: Utilisateur à l'origine de la suppression
        :param _reason: Raison de la suppression
        :param _force_default: Force le comportement par défaut ?
        :param keep_parents: Préserve la suppression des entitées parentes ?
        """
        if _force_default:
            return (super().delete)(*args, **kwargs)
        assert self.pk is not None, _("{} can't be deleted because it doesn't exists in database.").format(self._meta.object_name)
        self._ignore_log = _ignore_log or 
        self._current_user = self.current_user = _current_user or 
        self._reason = _reason or 
        self._force_default = _force_default or 
        from django.db import router
        using = kwargs.get('using', False) or 
        collector = Collector(using=using)
        collector.collect([self], keep_parents=keep_parents)
        self._collector_update = {key._meta.label:{field.name:[instance.pk for instance in instances] for (field, value), instances in value.items()} for key, value in collector.field_updates.items()}
        self._collector_delete = {key._meta.label:[model_to_dict(value, exclude='id') for value in values] for key, values in collector.data.items() if key._meta.auto_created if key._meta.auto_created}
        for instances in collector.data.values():
            for instance in instances:
                instance._ignore_log = self._ignore_log
                instance._current_user = self._current_user
                instance._reason = self._reason
                instance._force_default = self._force_default
                instance._from_admin = self._from_admin

        return collector.delete()

    def __init__(self, *args, **kwargs):
        if not self.__class__._init:
            for field in self._meta.concrete_fields + self._meta.many_to_many:
                if field.remote_field:
                    if field.related_model is Global:
                        continue
                    if isinstance(field, models.ForeignKey):
                        suffix = '_uid'
                        fget = lambda self, field_name=field.name: self._get_uid(field_name)
                        fset = lambda self, value, field_name=field.name: self._set_uid(field_name, value)
                    elif isinstance(field, models.ManyToManyField):
                        suffix = '_uids'
                        fget = lambda self, field_name=field.name: self._get_uids(field_name)
                        fset = lambda self, values, field_name=field.name: self._set_uids(field_name, values)
                    else:
                        continue
                    setattr(self.__class__, field.name + suffix, property(fget, fset))

            self.__class__._init = True
        (super().__init__)(*args, **kwargs)

    def _get_uid(self, fk_field):
        return getattr(self, fk_field).uuid

    def _set_uid(self, fk_field, value):
        field = self._meta.get_field(fk_field)
        unique = Global.objects.select_related().get(object_uid=value)
        model_from = unique.content_type.model_class()
        model_to = field.related_model
        assert model_from == model_to, _("Unexpected model '{}' used instead of expected model '{}'.").format(model_from._meta.verbose_name_raw, model_to._meta.verbose_name_raw)
        setattr(self, fk_field + '_id', unique.object_id)

    def _get_uids(self, m2m_field):
        return getattr(self, m2m_field).values_list('uuid', flat=True)

    def _set_uids(self, m2m_field, values):
        if not values:
            getattr(self, m2m_field).clear()
            return
        field = self._meta.get_field(m2m_field)
        uniques = Global.objects.select_related().filter(object_uid__in=values)
        assert uniques.values_list('content_type', flat=True).distinct().count() == 1, _('Multiple model types are found in values.')
        model_from = uniques.first().content_type.model_class()
        model_to = field.related_model
        assert model_from == model_to, _("Unexpected model '{}' used instead of expected model '{}'.").format(model_from._meta.verbose_name_raw, model_to._meta.verbose_name_raw)
        ids = uniques.values_list('object_id', flat=True)
        getattr(self, m2m_field).set(ids)

    def __json__(self):
        data = super().__json__()
        data.update(_current_user=(get_data_from_object(self._current_user or )),
          _reason=(self._reason),
          _from_admin=(self._from_admin),
          _restore=(self._restore),
          _ignore_log=(self._ignore_log),
          _force_default=(self._force_default))
        return data

    @staticmethod
    def from_uuid(uuid):
        """
        Permet de récupérer une instance d'entité à partir de son UUID
        :param uuid: UUID
        :return: Instance
        """
        reference = Global.objects.filter(object_uid=uuid).first()
        if reference:
            return reference.entity

    class Meta:
        abstract = True


class PerishableEntityQuerySet(EntityQuerySet):
    """PerishableEntityQuerySet"""

    def select_valid(self, date=None, valid=True):
        """
        Sélectionne les éléments valides du QuerySet
        :param date: Date de référence (facultatif)
        :param valid: Retourne les éléments valides ou invalides (valides par défaut)
        :return: QuerySet
        """
        if valid is None:
            return self
        else:
            date = date or 
            query = Q(start_date__lte=date, end_date__gte=date)
            query |= Q(start_date__lte=date, end_date__isnull=True)
            return valid or self.exclude(query)
        return self.filter(query)

    valid = property(select_valid)


class PerishableEntity(Entity):
    """PerishableEntity"""
    start_date = models.DateTimeField(blank=True,
      null=True,
      verbose_name=(_("date d'effet")))
    end_date = models.DateTimeField(blank=True,
      null=True,
      verbose_name=(_('date de fin')))
    objects = PerishableEntityQuerySet.as_manager()

    def save(self, *args, _force_default=False, force_insert=False, force_update=False, **kwargs):
        """
        Surcharge de la sauvegarde de l'entité périssable
        :param _force_default: Force le comportement par défaut ?
        :param force_insert: Force l'insertion des données ?
        :param force_update: Force la mise à jour des données ?
        """
        current_date = now()
        self.start_date = self.start_date or 
        if _force_default or self._force_default:
            kwargs.update(_force_default=True, force_insert=force_insert, force_update=force_update)
            return (super().save)(*args, **kwargs)
        if not force_update:
            previous = None
            if self.pk:
                previous = self.__class__.objects.get(pk=(self.pk))
                previous.end_date = self.end_date or 
                (previous.save)(force_update=True, **kwargs)
                self.pk = self.id = self.end_date = self.uuid = None
                self.start_date = previous.end_date or 
            result = (super().save)(force_insert=True, **kwargs)
            if previous:
                for metadata in previous.metadata.all():
                    metadata.pk = metadata.id = None
                    metadata.entity = self
                    metadata.save(force_insert=True)

            return result
        return (super().save)(args, force_insert=force_insert, force_update=force_update, **kwargs)

    def delete(self, *args, _force_default=False, **kwargs):
        """
        Surcharge de la suppression de l'entité périssable
        :param _force_default: Force le comportement par défaut ?
        """
        if _force_default or self._force_default:
            return (super().delete)(args, _force_default=True, **kwargs)
        if self.pk:
            self.end_date = self.end_date or 
            return (self.save)(args, force_update=True, **kwargs)
        return (super().delete)(*args, **kwargs)

    def clean(self):
        if self.start_date:
            if self.end_date:
                if self.end_date < self.start_date:
                    raise ValidationError((_("La date de fin doit être ultérieure à la date d'effet.")), code='incorrect_dates')

    @to_boolean(_('Valide'))
    def valid(self):
        return self.start_date <= now() and (self.end_date is None or )

    class Meta:
        abstract = True
        index_together = ['start_date', 'end_date']


class BaseWebhook(CommonModel):
    """BaseWebhook"""
    FORMAT_JSON = 'json'
    FORMAT_XML = 'xml'
    FORMAT_YAML = 'yaml'
    FORMATS = (
     (
      FORMAT_JSON, _('JSON')),
     (
      FORMAT_XML, _('XML')),
     (
      FORMAT_YAML, _('YAML')))
    METHOD_POST = 'post'
    METHOD_PUT = 'put'
    METHOD_PATCH = 'patch'
    METHODS = (
     (
      METHOD_POST, _('POST')),
     (
      METHOD_PUT, _('PUT')),
     (
      METHOD_PATCH, _('PATCH')))
    AUTHORIZATION_BASIC = 'Basic'
    AUTHORIZATION_DIGEST = 'Digest'
    AUTHORIZATION_TOKEN = 'Token'
    AUTHORIZATION_BEARER = 'Bearer'
    AUTHORIZATION_JWT = 'JWT'
    AUTHORIZATIONS = (
     (
      AUTHORIZATION_BASIC, _('Basic')),
     (
      AUTHORIZATION_DIGEST, _('Digest')),
     (
      AUTHORIZATION_TOKEN, _('Token')),
     (
      AUTHORIZATION_BEARER, _('Bearer')),
     (
      AUTHORIZATION_JWT, _('JWT')))
    SERIALIZERS = {FORMAT_JSON: JSONRenderer(), 
     FORMAT_XML: XMLRenderer() if XMLRenderer else None, 
     FORMAT_YAML: YAMLRenderer() if YAMLRenderer else None}
    CONTENT_TYPES = {FORMAT_JSON: 'application/json', 
     FORMAT_XML: 'application/xml', 
     FORMAT_YAML: 'application/x-yaml'}
    STATUS_FILTERS = {History.CREATE: 'is_create', 
     History.UPDATE: 'is_update', 
     History.DELETE: 'is_delete', 
     History.RESTORE: 'is_restore', 
     History.M2M: 'is_m2m'}
    name = models.CharField(max_length=100,
      blank=True,
      null=True,
      verbose_name=(_('nom')))
    url = models.URLField(verbose_name=(_('url')))
    method = models.CharField(max_length=5,
      default=METHOD_POST,
      choices=METHODS,
      verbose_name=(_('method')))
    format = models.CharField(max_length=4,
      default=FORMAT_JSON,
      choices=FORMATS,
      verbose_name=(_('format')))
    authorization = models.CharField(max_length=6,
      blank=True,
      null=True,
      choices=AUTHORIZATIONS,
      verbose_name=(_('authentification')))
    token = models.TextField(blank=True,
      null=True,
      verbose_name=(_('token')))
    timeout = models.PositiveSmallIntegerField(default=30,
      verbose_name=(_("délai d'attente")))
    retries = models.PositiveSmallIntegerField(default=0,
      verbose_name=(_('tentatives')))
    delay = models.PositiveSmallIntegerField(default=0,
      verbose_name=(_('délai entre tentatives')))

    def serialize_data(self, data):
        """
        Serialize les données fournies en fonction du type attendu
        :param data: Données brutes à sérializer
        :return: Données sérializées
        """
        if self.format in self.SERIALIZERS:
            serializer = self.SERIALIZERS.get(self.format)
            if not serializer:
                return
            return serializer.render(data)
        return data

    @staticmethod
    def send_websocket(data):
        """
        Broadcast du message par websocket (si activé)
        :param data: Données à transmettre
        :return: Rien
        """
        try:
            from common.websocket import send_message
            from common.utils import json_encode
            send_message(json_encode(data))
        except Exception as error:
            try:
                logger.error(error, exc_info=True)
            finally:
                error = None
                del error

    def send_http(self, data):
        """
        Transmission du message par requête HTTP aux différentes APIs référencées
        :param data: Données à transmettre
        :return: Rien
        """
        try:
            from requests import request, RequestException
        except ImportError:
            return
        else:
            headers = {}
            if self.authorization:
                if self.token:
                    headers['Authorization'] = '{type} {token}'.format(type=(self.authorization), token=(self.token))
            headers['Content-Type'] = self.CONTENT_TYPES.get(self.format, 'application/x-www-form-urlencoded')
            for retries in range(self.retries + 1):
                try:
                    serialized_data = self.serialize_data(data)
                    request((self.method), (self.url), data=serialized_data, headers=headers, timeout=(self.timeout))
                    break
                except RequestException as error:
                    try:
                        logger.warning(error)
                        time.sleep(self.delay)
                        continue
                    finally:
                        error = None
                        del error

                except Exception as error:
                    try:
                        logger.error(error, exc_info=True)
                        break
                    finally:
                        error = None
                        del error

    def __str__(self):
        return self.name

    class Meta:
        abstract = True


class Webhook(BaseWebhook):
    """Webhook"""
    types = models.ManyToManyField(ContentType,
      blank=True, verbose_name=(_('types')))
    is_create = models.BooleanField(default=True,
      verbose_name=(_('création')))
    is_update = models.BooleanField(default=True,
      verbose_name=(_('modification')))
    is_delete = models.BooleanField(default=True,
      verbose_name=(_('suppression')))
    is_restore = models.BooleanField(default=True,
      verbose_name=(_('restauration')))
    is_m2m = models.BooleanField(default=True,
      verbose_name=(_('many-to-many')))

    class Meta(BaseWebhook.Meta):
        verbose_name = _('webhook')
        verbose_name_plural = _('webhooks')


@receiver(post_init)
def post_init_receiver(sender, instance, *args, **kwargs):
    """
    Exécuté après chaque initialisation d'entité
    :param sender: Type d'entité
    :param instance: Instance de l'entité
    :return: Rien
    """
    if isinstance(instance, CommonModel):
        instance._copy = instance.to_dict(editables=True)


@receiver(pre_save)
def pre_save_receiver(sender, instance, raw, *args, **kwargs):
    """
    Exécuté avant chaque sauvegarde d'entité
    :param sender: Type d'entité
    :param instance: Instance de l'entité
    :param raw: Entité créée depuis les fixtures ?
    :return: Rien
    """
    if raw:
        if isinstance(instance, Entity):
            instance._ignore_log = True
            instance._force_default = True
            return


@receiver(post_save)
def post_save_receiver(sender, instance, created, raw, *args, **kwargs):
    """
    Exécuté après chaque sauvegarde d'entité
    :param sender: Type d'entité
    :param instance: Instance de l'entité
    :param created: Entité nouvellement créée ?
    :param raw: Entité créée depuis les fixtures ?
    :return: Rien
    """
    if isinstance(instance, Entity):
        if not settings.IGNORE_GLOBAL:
            if not instance._ignore_global:
                if created:
                    if instance.uuid:
                        if not instance._meta.pk.remote_field:
                            Global.objects.create(content_type=(instance.model_type), object_id=(instance.pk), object_uid=(instance.uuid))
        else:
            if raw:
                instance._ignore_log = True
                instance._force_default = True
                return
            if not settings.IGNORE_LOG:
                if not instance._ignore_log:
                    log_save.apply_async(args=(instance, created), retry=False)
    if isinstance(instance, CommonModel):
        status = History.CREATE if created else History.UPDATE
        run_notify_changes(instance, status)
        instance._copy = instance.to_dict(editables=True)


@app.task(ignore_result=True, name='common.log_save')
def log_save(instance, created):
    """
    Enregistre un historique de création/modification de l'entité
    :param instance: Instance de l'entité
    :param created: Entité nouvellement créée ?
    :return: Rien
    """
    if not settings.IGNORE_LOG:
        if instance._ignore_log:
            return
        user = instance._current_user or 
        if user:
            if not user.pk:
                user = None
        old_data = instance._copy
        new_data = instance.to_dict(editables=True)
        diff = set(new_data.items()) ^ set(old_data.items())
        if not diff:
            return
    else:
        history = instance._history
        if not history:
            history = History.objects.create(user=user,
              status=(History.RESTORE if instance._restore else [History.UPDATE, History.CREATE][created]),
              content_type=(instance.model_type),
              object_id=(instance.pk),
              object_uid=(instance.uuid),
              object_str=(str(instance)),
              reason=(instance._reason),
              data=old_data,
              data_size=(len(json_encode(old_data))),
              admin=(instance._from_admin),
              collector_update=(instance._collector_update),
              collector_delete=(instance._collector_delete))
            instance._history = history
        if history.status in (History.UPDATE, History.RESTORE) and old_data.get(instance._meta.pk.name):
            fields = []
            for key in new_data:
                old_value = old_data.get(key, None)
                new_value = new_data.get(key, None)
                if old_value == new_value:
                    continue
                try:
                    editable = instance._meta.get_field(key).editable
                except Exception as error:
                    try:
                        logger.warning(error, exc_info=True)
                        editable = True
                    finally:
                        error = None
                        del error

                fields.append(HistoryField(history=history,
                  field_name=key,
                  old_value=(None if old_value is None else str(old_value)),
                  new_value=(None if new_value is None else str(new_value)),
                  data=old_value,
                  data_size=(len(json_encode(old_value))),
                  editable=editable))

            HistoryField.objects.bulk_create(fields)
    logger.debug('Create/update log saved for entity {} #{} ({})'.format(instance._meta.object_name, instance.pk, instance.uuid))


COPY_M2M_ACTIONS = [
 'pre_clear', 'pre_add', 'pre_remove']
LOG_M2M_ACTIONS = {'post_clear':HistoryField.CLEAR_M2M, 
 'post_add':HistoryField.ADD_M2M, 
 'post_remove':HistoryField.REMOVE_M2M}

@receiver(m2m_changed)
def m2m_changed_receiver(sender, instance, model, action, *args, **kwargs):
    """
    Exécuté après chaque sauvegarde d'entité contenant des champs many-to-many
    :param sender: Type de l'entité de liaison
    :param instance: Instance de l'entité porteuse de la relation
    :param model: Modèle lié à la relation many-to-many
    :param action: Action exécutée
    :return: Rien
    """
    status_m2m = LOG_M2M_ACTIONS.get(action)
    if isinstance(instance, Entity):
        if status_m2m:
            if not settings.IGNORE_LOG:
                if not instance._ignore_log:
                    log_m2m.apply_async(args=(instance, model, status_m2m), retry=False)
    if isinstance(instance, CommonModel):
        if action in COPY_M2M_ACTIONS:
            instance._copy_m2m = instance.m2m_to_dict()
        if status_m2m:
            run_notify_changes(instance, History.M2M, status_m2m)


@app.task(ignore_result=True, name='common.log_m2m')
def log_m2m(instance, model, status_m2m):
    """
    Enregistre un historique de modification des relations de type ManyToMany de l'entité
    :param instance: Instance de l'entité
    :param model: Modèle lié à la relation ManyToMany
    :param status: Statut de modification de la relation
    :return: Rien
    """
    if settings.IGNORE_LOG or instance._ignore_log:
        return
    user = instance._current_user or 
    if user:
        if not user.pk:
            user = None
    old_m2m = instance._copy_m2m
    new_m2m = instance.m2m_to_dict()
    for field in set(old_m2m) | set(new_m2m):
        old_value = old_m2m.get(field, [])
        new_value = new_m2m.get(field, [])
        diff = set(old_value) ^ set(new_value)
        if not diff:
            continue
        else:
            history = instance._history
            if not history:
                history = History.objects.create(user=user,
                  status=(History.M2M),
                  content_type=(instance.model_type),
                  object_id=(instance.pk),
                  object_uid=(instance.uuid),
                  object_str=(str(instance)),
                  reason=(instance._reason),
                  data=old_m2m,
                  data_size=(len(json_encode(old_m2m))),
                  admin=(instance._from_admin),
                  collector_update=(instance._collector_update),
                  collector_delete=(instance._collector_delete))
                instance._history = history
            else:
                history.data.update(old_m2m)
                history.data_size = len(json_encode(history.data))
                history.save(update_fields=('data', 'data_size'))
        try:
            editable = instance._meta.get_field(field).editable
        except Exception as error:
            try:
                logger.warning(error, exc_info=True)
                editable = True
            finally:
                error = None
                del error

        field = HistoryField.objects.create(history=history,
          field_name=field,
          old_value=(' | '.join((str(value) for value in old_value)) if old_value else None),
          new_value=(' | '.join((str(value) for value in new_value)) if new_value else None),
          data=old_value,
          data_size=(len(json_encode(old_value))),
          status_m2m=status_m2m,
          editable=editable)
        logger.debug("Many-to-many log saved for field '{}' in entity {} #{} ({})".format(field, instance._meta.object_name, instance.pk, instance.uuid))


@receiver(pre_delete)
def pre_delete_receiver(sender, instance, *args, **kwargs):
    """
    Exécuté avant chaque suppression d'entité
    :param sender: Type de l'entité
    :param instance: Instance de l'entité
    :return: Rien
    """
    if isinstance(instance, Entity):
        if not settings.IGNORE_LOG:
            if not instance._ignore_log:
                log_delete.apply_async(args=(instance,), retry=False)
    if isinstance(instance, CommonModel):
        run_notify_changes(instance, History.DELETE)


@app.task(ignore_result=True, name='common.log_delete')
def log_delete(instance):
    """
    Enregistre un historique de suppression de l'entité
    :param instance: Instance de l'entité
    :return: Rien
    """
    if settings.IGNORE_LOG or instance._ignore_log:
        return
    user = instance._current_user or 
    if user:
        if not user.pk:
            user = None
    data = instance.to_dict(m2m=True, editables=True)
    history = History.objects.create(user=user,
      status=(History.DELETE),
      content_type=(instance.model_type),
      object_id=(instance.pk),
      object_uid=(instance.uuid),
      object_str=(str(instance)),
      reason=(instance._reason),
      data=data,
      data_size=(len(json_encode(data))),
      admin=(instance._from_admin),
      collector_update=(instance._collector_update),
      collector_delete=(instance._collector_delete))
    instance._history = history
    logger.debug('Delete log saved for entity {} #{} ({})'.format(instance._meta.object_name, instance.pk, instance.uuid))


def run_notify_changes(instance, status, status_m2m=None):
    """
    Notification des changements sur une entité (par broadcast websocket et/ou API callback)
    :param instance: Instance de l'entité
    :param status: Statut général du changement
    :param status_m2m: Sous-statut concernant un changement sur les champs many-to-many
    :return: Rien
    """
    filters = {Webhook.STATUS_FILTERS.get(status): True}
    filters.update(dict(types__in=[instance.model_type]))
    if settings.NOTIFY_CHANGES:
        if settings.WEBSOCKET_ENABLED or instance.has_webhook(status):
            return notify_changes.apply_async(args=(instance, status, status_m2m), retry=False)


@app.task(ignore_result=True, name='common.notify_changes')
def notify_changes(instance, status, status_m2m=None):
    """
    Notification des changements sur une entité (par broadcast websocket et/ou API callback)
    :param instance: Instance de l'entité
    :param status: Statut général du changement
    :param status_m2m: Sous-statut concernant un changement sur les champs many-to-many
    :return: Rien
    """
    diff_data_prev, diff_data_next = (None, None)
    if status in [History.UPDATE, History.RESTORE]:
        old_data = instance._copy.items()
        new_data = instance.to_dict(editables=True).items()
        if set(new_data) ^ set(old_data):
            diff_data_prev = dict(set(old_data) - set(new_data))
            diff_data_next = dict(set(new_data) - set(old_data))
    has_diff_data = diff_data_prev and diff_data_next
    diff_m2m_prev, diff_m2m_next = {}, {}
    if status == History.M2M:
        old_m2m = instance._copy_m2m
        new_m2m = instance.m2m_to_dict()
        for field in set(old_m2m) | set(new_m2m):
            old_value = old_m2m.get(field, ())
            new_value = new_m2m.get(field, ())
            if set(old_value) ^ set(new_value):
                diff_m2m_prev[field] = list(set(old_value) - set(new_value))
                diff_m2m_next[field] = list(set(new_value) - set(old_value))

    has_diff_m2m = diff_m2m_prev and diff_m2m_next
    get_data = getattr(instance, 'get_webhook_data', lambda *a, **k: (instance.to_dict)(**settings.NOTIFY_OPTIONS))
    data = {'id':str(uuid.uuid4()), 
     'date':now(), 
     'meta':{'id':instance.pk, 
      'uuid':getattr(instance, 'uuid', None), 
      'type':model_to_dict(get_content_type(instance)), 
      'status':status, 
      'status_display':str(dict(History.LOG_STATUS).get(status, '')) or , 
      'status_m2m':status_m2m, 
      'status_m2m_display':str(dict(HistoryField.LOG_STATUS_M2M).get(status_m2m, '')) or }, 
     'changes':{'data':{'previous':diff_data_prev,  'current':diff_data_next} if has_diff_data else None,  'm2m':{'previous':diff_m2m_prev,  'current':diff_m2m_next} if has_diff_m2m else None} if has_diff_data or has_diff_m2m else None, 
     'data':get_data(status=status, status_m2m=status_m2m)}
    if settings.WEBSOCKET_ENABLED:
        Webhook.send_websocket(data)
    filters = {Webhook.STATUS_FILTERS.get(status): True}
    filters.update(dict(types__in=[instance.model_type]))
    for webhook in (Webhook.objects.filter)(**filters):
        webhook.send_http(data)

    return data


@receiver(post_save)
def create_token_and_metadata(sender, instance=None, created=False, **kwargs):
    """
    Génération du jeton d'authentification pour Django REST Framework
    """
    if created:
        if issubclass(sender, get_user_model()):
            try:
                from rest_framework.authtoken.models import Token
                Token.objects.create(user=instance)
            except (AttributeError, ImportError):
                logger.warning('Unable to create API Token, are django-rest-framework with authtoken installed?')

            UserMetaData.objects.create(user=instance, data={})
        elif issubclass(sender, Group):
            GroupMetaData.objects.create(group=instance, data={})


class UserMetaData(CommonModel):
    """UserMetaData"""
    user = models.OneToOneField((settings.AUTH_USER_MODEL),
      on_delete=(models.CASCADE),
      verbose_name=(_('utilisateur')),
      related_name='metadata')
    data = JsonField(blank=True,
      null=True,
      verbose_name=(_('données')))

    @staticmethod
    def set(user, **data):
        meta = user.metadata
        (meta.data.update)(**data)
        meta.save()
        return meta.data

    @staticmethod
    def get(user, key=None, groups=True):
        data = {}
        if groups:
            for group in user.groups.select_related('metadata').all():
                try:
                    merge_dict(data, group.metadata.data or )
                except GroupMetaData.DoesNotExist:
                    continue

        try:
            merge_dict(data, user.metadata.data or )
        except UserMetaData.DoesNotExist:
            pass

        if key:
            return data.get(key)
        return data

    @staticmethod
    def remove(user, key):
        meta = user.metadata
        meta.data.pop(key, None)
        meta.save()
        return meta.data

    @staticmethod
    def merge(user, *idict, **data):
        meta = user.metadata
        merge_dict(meta.data, *idict, **data)
        meta.save()
        return meta.data

    def __str__(self):
        return str(self.user)

    class Meta:
        verbose_name = _("métadonnées d'utilisateur")
        verbose_name_plural = _("métadonnées d'utilisateurs")


class GroupMetaData(CommonModel):
    """GroupMetaData"""
    group = models.OneToOneField('auth.Group',
      on_delete=(models.CASCADE),
      verbose_name=(_('groupe')),
      related_name='metadata')
    data = JsonField(blank=True,
      null=True,
      verbose_name=(_('données')))

    @staticmethod
    def set(group, **data):
        meta = group.metadata
        (meta.data.update)(**data)
        meta.save()
        return meta.data

    @staticmethod
    def get(group, key=None):
        meta = group.metadata
        if key:
            return meta.data.get(key)
        return meta.data

    @staticmethod
    def remove(group, key):
        meta = group.metadata
        meta.data.pop(key, None)
        meta.save()
        return meta.data

    @staticmethod
    def merge(group, *idict, **data):
        meta = group.metadata
        merge_dict(meta.data, *idict, **data)
        meta.save()
        return meta.data

    def __str__(self):
        return str(self.group)

    class Meta:
        verbose_name = _('métadonnées de groupe')
        verbose_name_plural = _('métadonnées de groupes')


class ServiceUsage(CommonModel):
    """ServiceUsage"""
    RESET_HOURLY = 'H'
    RESET_DAILY = 'D'
    RESET_WEEKLY = 'W'
    RESET_MONTHLY = 'M'
    RESET_YEARLY = 'Y'
    RESETS = (
     (
      RESET_HOURLY, _('Toutes les heures')),
     (
      RESET_DAILY, _('Tous les jours')),
     (
      RESET_WEEKLY, _('Toutes les semaines')),
     (
      RESET_MONTHLY, _('Tous les mois')),
     (
      RESET_YEARLY, _('Tous les ans')))
    RESET_DELTA = {RESET_HOURLY: dict(hours=1), 
     RESET_DAILY: dict(days=1), 
     RESET_WEEKLY: dict(weeks=1), 
     RESET_MONTHLY: dict(months=1), 
     RESET_YEARLY: dict(years=1)}
    name = models.CharField(max_length=200,
      verbose_name=(_('nom')))
    user = models.ForeignKey((settings.AUTH_USER_MODEL),
      on_delete=(models.CASCADE),
      related_name='usages',
      verbose_name=(_('utilisateur')))
    count = models.PositiveIntegerField(default=0,
      verbose_name=(_('nombre')))
    limit = models.PositiveIntegerField(blank=True,
      null=True,
      verbose_name=(_('limite')))
    reset = models.CharField(max_length=1,
      blank=True,
      choices=RESETS,
      verbose_name=(_('réinitialisation')))
    reset_date = models.DateTimeField(blank=True,
      null=True,
      verbose_name=(_('date réinitialisation')))
    address = models.CharField(max_length=40,
      verbose_name=(_('adresse')))
    date = models.DateTimeField(auto_now=True,
      verbose_name=(_('date')))

    def save(self, *args, **kwargs):
        if self.limit is not None:
            if self.reset:
                self.reset_date = self.reset_date or 
                if now() >= self.reset_date:
                    import dateutil.relativedelta as relativedelta
                    delta = self.RESET_DELTA.get(self.reset)
                    self.reset_date = now() + relativedelta(**delta)
                    self.count = 0
        return (super().save)(*args, **kwargs)

    def __str__(self):
        return _('{} ({} : {})').format(self.name, self.address, self.count)

    class Meta:
        verbose_name = _('utilisation de service')
        verbose_name_plural = _('utilisation des services')
        unique_together = ('name', 'user')


def get_object_from_data(data, from_db=False):
    """
    Permet de construire une instance d'un modèle quelconque à partir de sa représentation JSON
    :param data: Dictionnaire de données
    :param from_db: Récupérer l'instance depuis la base de données ?
    :return: Instance (si possible)
    """
    model = None
    if not isinstance(data, dict):
        return data
    if from_db:
        if 'uuid' in data:
            return Entity.from_uuid(data['uuid'])
    if '_content_type' in data:
        content_type = ContentType(**data.pop('_content_type'))
        model = content_type.model_class()
        pk_field = get_pk_field(model).name
        if from_db:
            if pk_field in data:
                return (model.objects.filter)(**{pk_field: data[pk_field]}).first()
    if model:
        instance = model()
        for key, value in data.items():
            setattr(instance, key, get_object_from_data(value))

        return instance


def get_data_from_object(instance, types=True, **options):
    """
    Tente d'extraire les données de l'instance d'un modèle
    :param instance: Instance
    :param types: Ajouter le type du modèle ?
    :param options: Options complémentaires de la méthode .to_dict()
    :return: Dictionnaire de données (si possible)
    """
    data = {}
    if not instance:
        return
    elif isinstance(instance, CommonModel):
        data = (instance.to_dict)(types=types, **options)
    elif isinstance(instance, models.Model):
        data = model_to_dict(instance)
        data.pop('_state', None)
        if types:
            content_type = ContentType.objects.get_for_model(instance)
            data.update(_content_type=get_data_from_object(content_type, types=False))
    elif hasattr(instance, '__dict__'):
        data = instance.__dict__
    return data


def model_to_dict(instance, fields=None, exclude=None, **kwargs):
    """
    Equivalent récursif du `model_to_dict` de Django
    :param instance: Instance
    :param fields: Champs à inclures (organisés par modèle)
    :param exclude: Champs à inclures (organisés par modèle)
    :return: Dictionnaire
    """
    model = instance._meta.model
    _includes, _excludes = fields or , exclude or 
    fields = _includes.get(model) if isinstance(_includes, dict) else _includes
    exclude = _excludes.get(model) if isinstance(_excludes, dict) else _excludes
    if isinstance(instance, CommonModel):
        data = (instance.to_dict)(includes=_includes, excludes=_excludes, **kwargs)
    else:
        data = django_model_to_dict(instance, fields=fields, exclude=exclude)
        for key, value in data.items():
            if isinstance(value, models.Model):
                data[key] = model_to_dict(value, fields=fields, exclude=exclude)

    return data


setattr(AbstractBaseUser, 'set_metadata', lambda self, **metas: (UserMetaData.set)(self, **metas))
setattr(AbstractBaseUser, 'get_metadata', lambda self, key=None, groups=True: UserMetaData.get(self, key=key, groups=groups))
setattr(AbstractBaseUser, 'del_metadata', lambda self, key: UserMetaData.remove(self, key))
setattr(AbstractBaseUser, 'merge_metadata', lambda self, *idict, **metas: (UserMetaData.merge)(self, *idict, **metas))
setattr(Group, 'set_metadata', lambda self, **metas: (GroupMetaData.set)(self, **metas))
setattr(Group, 'get_metadata', lambda self, key=None: GroupMetaData.get(self, key=key))
setattr(Group, 'del_metadata', lambda self, key: GroupMetaData.remove(self, key))
setattr(Group, 'merge_metadata', lambda self, *idict, **metas: (GroupMetaData.merge)(self, *idict, **metas))
MODELS = [
 Global,
 MetaData,
 History,
 HistoryField,
 Webhook,
 UserMetaData,
 GroupMetaData]