# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/afshari9978/Projects/namaki_backend/avishan/models.py
# Compiled at: 2020-04-27 00:25:09
# Size of source mod 2**32: 61979 bytes
import random
from inspect import Parameter
from typing import List, Type, Union, Tuple, Dict
import requests
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.db.models import NOT_PROVIDED
from avishan import current_request
from avishan.configure import get_avishan_config, AvishanConfigFather
from avishan.misc import status
from avishan.misc.translation import AvishanTranslatable
import datetime
from typing import Optional
from avishan.misc.bch_datetime import BchDatetime
from django.db import models

class AvishanModel(models.Model):

    class Meta:
        abstract = True

    UNCHANGED = '__UNCHANGED__'
    private_fields = []
    private_fields: List[Union[(models.Field, str)]]
    django_admin_date_hierarchy = None
    django_admin_date_hierarchy: Optional[str]
    django_admin_list_display = []
    django_admin_list_display: List[models.Field]
    django_admin_list_filter = []
    django_admin_list_filter: List[models.Field]
    django_admin_list_max_show_all = 300
    django_admin_list_max_show_all: int
    django_admin_list_per_page = 100
    django_admin_list_per_page: int
    django_admin_raw_id_fields = []
    django_admin_raw_id_fields: List[models.Field]
    django_admin_readonly_fields = []
    django_admin_readonly_fields: List[models.Field]
    django_admin_search_fields = []
    django_admin_search_fields: List[models.Field]

    @classmethod
    def direct_callable_methods(cls) -> List[str]:
        return []

    @classmethod
    def direct_non_authenticated_callable_methods(cls) -> List[str]:
        return []

    @classmethod
    def get(cls, avishan_to_dict: bool=False, avishan_raise_400: bool=False, **kwargs):
        from avishan.exceptions import ErrorMessageException
        if avishan_to_dict:
            return (cls.get)(avishan_to_dict=False, avishan_raise_400=avishan_raise_400, **kwargs).to_dict()
        try:
            return (cls.objects.get)(**kwargs)
            except cls.DoesNotExist as e:
            try:
                if avishan_raise_400:
                    raise ErrorMessageException(AvishanTranslatable(EN=('Chosen ' + cls.__name__ + ' doesnt exist'),
                      FA=f"{cls.__name__} انتخاب شده موجود نیست"))
                raise e
            finally:
                e = None
                del e

    @classmethod
    def filter(cls, avishan_to_dict: bool=False, **kwargs):
        if avishan_to_dict:
            return [item.to_dict() for item in (cls.filter)(**kwargs)]
        if current_request != {}:
            for item in current_request['request'].GET.keys():
                if item.startswith('filter_'):
                    field = cls.get_field(item[7:])
                    kwargs[field.name] = field.related_model.get(id=(current_request['request'].GET[item]))

        if len(kwargs.items()) > 0:
            return (cls.objects.filter)(**kwargs)
        return cls.objects.all()

    @classmethod
    def all(cls, avishan_to_dict: bool=False):
        return cls.filter(avishan_to_dict=avishan_to_dict)

    @classmethod
    def create(cls, **kwargs):
        create_kwargs, many_to_many_objects, after_creation = (cls._clean_model_data_kwargs)(**kwargs)
        created = (cls.objects.create)(**create_kwargs)
        if many_to_many_objects:
            for key, value in many_to_many_objects.items():
                for item in value:
                    created.__getattribute__(key).add(item)

            else:
                created.save()

        for after_create in after_creation:
            for target_object in after_create['target_objects']:
                (after_create['target_model'].create)(**{**{after_create['created_for_field'].name: created}, **target_object})
            else:
                return created

    def update(self, **kwargs):
        unchanged_list = []
        for key, value in kwargs.items():
            if value == self.UNCHANGED:
                unchanged_list.append(key)

        for key in unchanged_list:
            del kwargs[key]
        else:
            base_kwargs, many_to_many_kwargs, _ = (self.__class__._clean_model_data_kwargs)(**kwargs)
            for key, value in base_kwargs.items():
                self.__setattr__(key, value)
            else:
                if many_to_many_kwargs:
                    for key, value in many_to_many_kwargs.items():
                        self.__getattribute__(key).clear()
                        for item in value:
                            self.__getattribute__(key).add(item)

                self.save()
                return self

    def remove(self) -> dict:
        temp = self.to_dict()
        self.delete()
        return temp

    @classmethod
    def update_properties(cls) -> Dict[(str, Parameter)]:
        from avishan.libraries.openapi3 import get_functions_properties
        data = dict(get_functions_properties(getattr(cls, 'update')))
        del data['self']
        return data

    @classmethod
    def search(cls, query_set: models.QuerySet, search_text: str=None) -> models.QuerySet:
        if search_text is None:
            return query_set
        result = cls.objects.none()
        for field in cls.get_fields():
            if isinstance(field, models.CharField):
                result = (query_set.filter)(**{f"{field.name}__icontains": search_text}) | result
            return result.distinct()

    @classmethod
    def create_or_update--- This code section failed: ---

 L. 172         0  SETUP_FINALLY        64  'to 64'

 L. 173         2  LOAD_FAST                'cls'
                4  LOAD_ATTR                objects
                6  LOAD_ATTR                get
                8  BUILD_TUPLE_0         0 
               10  LOAD_FAST                'fixed_kwargs'
               12  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
               14  STORE_FAST               'found'

 L. 174        16  LOAD_FAST                'new_additional_kwargs'
               18  LOAD_METHOD              items
               20  CALL_METHOD_0         0  ''
               22  GET_ITER         
               24  FOR_ITER             46  'to 46'
               26  UNPACK_SEQUENCE_2     2 
               28  STORE_FAST               'key'
               30  STORE_FAST               'value'

 L. 175        32  LOAD_FAST                'found'
               34  LOAD_METHOD              __setattr__
               36  LOAD_FAST                'key'
               38  LOAD_FAST                'value'
               40  CALL_METHOD_2         2  ''
               42  POP_TOP          
               44  JUMP_BACK            24  'to 24'

 L. 176        46  LOAD_FAST                'found'
               48  LOAD_METHOD              save
               50  CALL_METHOD_0         0  ''
               52  POP_TOP          

 L. 177        54  LOAD_FAST                'found'
               56  LOAD_CONST               False
               58  BUILD_TUPLE_2         2 
               60  POP_BLOCK        
               62  RETURN_VALUE     
             64_0  COME_FROM_FINALLY     0  '0'

 L. 178        64  DUP_TOP          
               66  LOAD_FAST                'cls'
               68  LOAD_ATTR                DoesNotExist
               70  COMPARE_OP               exception-match
               72  POP_JUMP_IF_FALSE   106  'to 106'
               74  POP_TOP          
               76  POP_TOP          
               78  POP_TOP          

 L. 179        80  LOAD_FAST                'cls'
               82  LOAD_ATTR                objects
               84  LOAD_ATTR                create
               86  BUILD_TUPLE_0         0 

 L. 180        88  LOAD_FAST                'fixed_kwargs'
               90  LOAD_FAST                'new_additional_kwargs'
               92  BUILD_MAP_UNPACK_2     2 

 L. 179        94  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'

 L. 181        96  LOAD_CONST               True

 L. 179        98  BUILD_TUPLE_2         2 
              100  ROT_FOUR         
              102  POP_EXCEPT       
              104  RETURN_VALUE     
            106_0  COME_FROM            72  '72'
              106  END_FINALLY      

Parse error at or near `POP_TOP' instruction at offset 76

    def to_dict(self, exclude_list: List[Union[(models.Field, str)]]=()) -> dict:
        """
        Convert object to dict
        :return:
        """
        dicted = {}
        for field in self.get_full_fields():
            if field not in self.private_fields and field.name not in self.private_fields and field not in exclude_list and field.name not in exclude_list:
                value = self.get_data_from_field(field)
                if value is None:
                    dicted[field.name] = None
                elif isinstance(field, models.DateField):
                    try:
                        if get_avishan_config().USE_JALALI_DATETIME:
                            dicted[field.name] = BchDatetime(value).to_dict(full=True)
                        else:
                            if value is None:
                                dicted[field.name] = {}
                            else:
                                dicted[field.name] = {'year':value.year, 
                                 'month':value.month, 
                                 'day':value.day}
                                if isinstance(field, models.DateTimeField):
                                    dicted[field.name] = {**{'hour':value.hour,  'minute':value.minute, 
                                     'second':value.second, 
                                     'microsecond':value.microsecond}, **(dicted[field.name])}
                    except:
                        dicted[field.name] = {}

                elif isinstance(field, (models.OneToOneField, models.ForeignKey)):
                    dicted[field.name] = value.to_dict()
                elif isinstance(field, models.ManyToManyField):
                    dicted[field.name] = [item.to_dict() for item in value.all()]
                elif isinstance(value, datetime.time):
                    dicted[field.name] = {'hour':value.hour,  'minute':value.minute,  'second':value.second,  'microsecond':value.microsecond}
                else:
                    dicted[field.name] = value
            return dicted

    @classmethod
    def _clean_model_data_kwargs(cls, on_update: bool=False, **kwargs):
        from avishan.exceptions import ErrorMessageException
        base_kwargs = {}
        many_to_many_kwargs = {}
        if 'is_api' in current_request.keys():
            if not current_request['is_api']:
                kwargs = cls._clean_form_post(kwargs)
        for field in cls.get_full_fields():
            if cls.is_field_readonly(field):
                pass
            else:
                if cls.is_field_required(field) and (on_update or field.name) not in kwargs.keys():
                    raise ErrorMessageException(AvishanTranslatable(EN=f"Field {field.name} not found in object {cls.class_name()}, and it's required."))
                else:
                    pass
                if field.name not in kwargs.keys():
                    pass
                elif isinstance(field, (models.OneToOneField, models.ForeignKey)):
                    if isinstance(kwargs[field.name], models.Model):
                        base_kwargs[field.name] = kwargs[field.name]
                    else:
                        if kwargs[field.name] == {'id': 0} or kwargs[field.name] is None:
                            base_kwargs[field.name] = None
                        else:
                            if field.related_model == TranslatableChar:
                                if isinstance(kwargs[field.name], dict):
                                    en = kwargs[field.name].get('en', None)
                                    fa = kwargs[field.name].get('fa', None)
                                else:
                                    if isinstance(kwargs[field.name], str):
                                        en = kwargs[field.name]
                                        fa = kwargs[field.name]
                                    else:
                                        en = 'NOT TRANSLATED'
                                        fa = 'NOT TRANSLATED'
                                base_kwargs[field.name] = TranslatableChar.create(en=en, fa=fa)
                            else:
                                base_kwargs[field.name] = field.related_model._AvishanModel__get_object_from_dict(kwargs[field.name])
                elif isinstance(field, models.ManyToManyField):
                    many_to_many_kwargs[field.name] = []
                    for input_item in kwargs[field.name]:
                        if isinstance(input_item, models.Model):
                            item_object = input_item
                        else:
                            item_object = field.related_model._AvishanModel__get_object_from_dict(input_item)
                        many_to_many_kwargs[field.name].append(item_object)

                else:
                    base_kwargs[field.name] = cls.cast_field_data(kwargs[field.name], field)
        else:
            try:
                added_related_model_names = [item.class_snake_case_name() for item in cls.admin_related_models()]
            except:
                added_related_model_names = []
            else:
                after_creation = []
                if not on_update:
                    for related_name in added_related_model_names:
                        if related_name not in kwargs.keys():
                            pass
                        else:
                            related_model = AvishanModel.get_model_by_snake_case_name(related_name)
                            for related_model_field in related_model.get_full_fields():
                                if isinstance(related_model_field, models.ForeignKey) and related_model_field.related_model == cls:
                                    target_related_field = related_model_field

                    else:
                        after_creation.append({'created_for_field':target_related_field, 
                         'target_objects':kwargs[related_name], 
                         'target_model':related_model})

                else:
                    return (
                     base_kwargs, many_to_many_kwargs, after_creation)

    @classmethod
    def _clean_form_post(cls, kwargs: dict) -> dict:
        output = {}
        try:
            added_related_model_names = [item.class_snake_case_name() for item in cls.admin_related_models()]
        except:
            added_related_model_names = []
        else:
            for related_name in added_related_model_names:
                related_name_pack = []

        for key, value in kwargs.items():
            if key.startswith(related_name):
                related_name_pack.append(key)
            if len(related_name_pack) == 0:
                pass
            else:
                kwargs[related_name] = []

        if isinstance(kwargs[related_name_pack[0]], str):
            kwargs[related_name].append({})
            for esme in related_name_pack:
                kwargs[related_name][0][esme[len(related_name):]] = kwargs[esme]

        else:
            for i in range(kwargs[related_name_pack[0]].__len__()):
                kwargs[related_name].append({})
            else:
                for key in related_name_pack:
                    for i, final_pack in enumerate(kwargs[related_name]):
                        final_pack[key[len(related_name):]] = kwargs[key][i]
                    else:
                        for key in related_name_pack:
                            del kwargs[key]
                        else:
                            for key, value in kwargs.items():
                                output[key] = value
                            else:
                                return output

    @classmethod
    def class_name(cls) -> str:
        return cls.__name__

    @classmethod
    def class_snake_case_name(cls) -> str:
        import re
        s1 = re.sub('(.)([A-Z][a-z]+)', '\\1_\\2', cls.class_name())
        return re.sub('([a-z0-9])([A-Z])', '\\1_\\2', s1).lower()

    @classmethod
    def class_plural_snake_case_name(cls) -> str:
        return cls.class_snake_case_name() + 's'

    @classmethod
    def app_name(cls) -> str:
        return cls._meta.app_label

    @staticmethod
    def get_non_abstract_models(app_name: str=None) -> List[Type['AvishanModel']]:
        return [x for x in AvishanModel.get_models(app_name) if x._meta.abstract is False]

    @staticmethod
    def get_models(app_name: str=None) -> List[Type['AvishanModel']]:

        def get_sub_classes(parent):
            subs = [
             parent]
            for child in parent.__subclasses__():
                subs += get_sub_classes(child)
            else:
                return subs

        total = []
        for model in app_name or AvishanModel.__subclasses__():
            total += get_sub_classes(model)
        else:
            return list(set(total))
            return [x for x in AvishanModel.get_models() if x._meta.app_label == app_name]

    @staticmethod
    def get_model_with_class_name(class_name: str) -> Optional[Type['AvishanModel']]:
        for item in AvishanModel.get_models():
            if item.class_name() == class_name:
                return item

    @staticmethod
    def get_model_by_plural_snake_case_name(name: str) -> Optional[Type['AvishanModel']]:
        for model in AvishanModel.get_non_abstract_models():
            if model.class_plural_snake_case_name() == name:
                return model

    @staticmethod
    def get_model_by_snake_case_name(name: str) -> Optional[Type['AvishanModel']]:
        for model in AvishanModel.get_non_abstract_models():
            if model.class_snake_case_name() == name:
                return model

    @staticmethod
    def get_app_names() -> List[str]:
        import django.apps as apps
        return [key.name for key in apps.get_app_configs() if key.name in get_avishan_config().MONITORED_APPS_NAMES]

    @classmethod
    def get_fields(cls) -> List[models.Field]:
        return list(cls._meta.fields)

    @classmethod
    def get_full_fields(cls) -> List[models.Field]:
        return list(cls._meta.fields + cls._meta.many_to_many)

    @classmethod
    def get_field(cls, field_name: str) -> models.Field:
        for item in cls.get_fields():
            if item.name == field_name:
                return item
        else:
            raise ValueError(AvishanTranslatable(EN=f"field {field_name} not found in model {cls.class_name()}"))

    @classmethod
    def is_field_identifier_for_model(cls, field: models.Field) -> bool:
        """
        Checks if field is enough for finding an object from db.
        :param field: for example for 'id' or other unique fields, it will be True
        :return:
        """
        return field.primary_key or field.unique

    @staticmethod
    def is_field_readonly(field: models.Field) -> bool:
        """
        Checks if field is read-only type and must not entered by user
        :param field: for example auto create date-times
        :return:
        """
        if isinstance(field, models.DateField) or isinstance(field, models.DateTimeField) or isinstance(field, models.TimeField):
            if not field.auto_now:
                if field.auto_now_add:
                    return True
        if field.primary_key:
            return True
        return False

    @staticmethod
    def is_field_required--- This code section failed: ---

 L. 461         0  LOAD_FAST                'field'
                2  LOAD_ATTR                name
                4  LOAD_STR                 'id'
                6  COMPARE_OP               ==
                8  POP_JUMP_IF_TRUE     56  'to 56'
               10  LOAD_FAST                'field'
               12  LOAD_ATTR                default
               14  LOAD_GLOBAL              NOT_PROVIDED
               16  COMPARE_OP               !=
               18  POP_JUMP_IF_TRUE     56  'to 56'

 L. 462        20  LOAD_GLOBAL              isinstance
               22  LOAD_FAST                'field'
               24  LOAD_GLOBAL              models
               26  LOAD_ATTR                DateField
               28  CALL_FUNCTION_2       2  ''

 L. 461        30  POP_JUMP_IF_TRUE     56  'to 56'

 L. 462        32  LOAD_GLOBAL              isinstance
               34  LOAD_FAST                'field'
               36  LOAD_GLOBAL              models
               38  LOAD_ATTR                TimeField
               40  CALL_FUNCTION_2       2  ''

 L. 461        42  POP_JUMP_IF_FALSE    60  'to 60'

 L. 463        44  LOAD_FAST                'field'
               46  LOAD_ATTR                auto_now

 L. 461        48  POP_JUMP_IF_TRUE     56  'to 56'

 L. 463        50  LOAD_FAST                'field'
               52  LOAD_ATTR                auto_now_add

 L. 461        54  POP_JUMP_IF_FALSE    60  'to 60'
             56_0  COME_FROM            48  '48'
             56_1  COME_FROM            30  '30'
             56_2  COME_FROM            18  '18'
             56_3  COME_FROM             8  '8'

 L. 464        56  LOAD_CONST               False
               58  RETURN_VALUE     
             60_0  COME_FROM            54  '54'
             60_1  COME_FROM            42  '42'

 L. 465        60  LOAD_GLOBAL              isinstance
               62  LOAD_FAST                'field'
               64  LOAD_GLOBAL              models
               66  LOAD_ATTR                ManyToManyField
               68  CALL_FUNCTION_2       2  ''
               70  POP_JUMP_IF_FALSE    76  'to 76'

 L. 466        72  LOAD_CONST               False
               74  RETURN_VALUE     
             76_0  COME_FROM            70  '70'

 L. 468        76  LOAD_FAST                'field'
               78  LOAD_ATTR                blank
               80  POP_JUMP_IF_TRUE     88  'to 88'
               82  LOAD_FAST                'field'
               84  LOAD_ATTR                null
               86  POP_JUMP_IF_FALSE    92  'to 92'
             88_0  COME_FROM            80  '80'

 L. 469        88  LOAD_CONST               False
               90  RETURN_VALUE     
             92_0  COME_FROM            86  '86'

 L. 471        92  LOAD_CONST               True
               94  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `RETURN_VALUE' instruction at offset 94

    @classmethod
    def cast_field_data(cls, data, field: models.Field):
        """
        Cast data to it's appropriate form
        :param data: entered data
        :param field: target field
        :return: after cast data
        """
        if data is None:
            return
            if isinstance(field, (models.CharField, models.TextField)):
                cast_class = str
            else:
                if isinstance(field, (models.IntegerField, models.AutoField)):
                    cast_class = int
                else:
                    if isinstance(field, models.FloatField):
                        cast_class = float
                    else:
                        if isinstance(field, models.TimeField):
                            if not isinstance(data, datetime.time):
                                cast_class = datetime.time
                            else:
                                cast_class = None
                        else:
                            if isinstance(field, models.DateTimeField):
                                if not isinstance(data, datetime.datetime):
                                    cast_class = datetime.datetime
                                else:
                                    cast_class = None
                            else:
                                if isinstance(field, models.DateField):
                                    if not isinstance(data, datetime.date):
                                        cast_class = datetime.date
                                    else:
                                        cast_class = None
                                else:
                                    if isinstance(field, models.BooleanField):
                                        cast_class = bool
                                    else:
                                        if isinstance(field, models.ManyToManyField):
                                            cast_class = field.related_model
                                        else:
                                            if isinstance(field, models.ForeignKey):
                                                cast_class = field.related_model
                                            else:
                                                raise NotImplementedError(AvishanTranslatable(EN='cast_field_data not defined cast type'))
            if cast_class is None:
                return data
            if isinstance(cast_class, AvishanModel):
                if not isinstance(data, dict):
                    raise ValueError('ForeignKey or ManyToMany relation should contain dict with id')
                output = cast_class.objects.get(id=(int(data['id'])))
        elif isinstance(cast_class, datetime.datetime):
            if not isinstance(data, dict):
                raise ValueError('Datetime should contain dict')
            output = BchDatetime(data).to_datetime()
        else:
            if isinstance(cast_class, datetime.date):
                if not isinstance(data, dict):
                    raise ValueError('Date should contain dict')
                output = BchDatetime(data).to_date()
            else:
                output = cast_class(data)
        return output

    @classmethod
    def __get_object_from_dict(cls, input_dict: dict) -> 'AvishanModel':
        return (cls.get)(**input_dict)

    def get_data_from_field(self, field: models.Field, string_format_dates: bool=False):
        from avishan.exceptions import ErrorMessageException
        if field.choices is not None:
            for k, v in field.choices:
                if k == self.__getattribute__(field.name):
                    return v
            else:
                raise ErrorMessageException(AvishanTranslatable(EN=f"Incorrect Data entered for field {field.name} in model {self.class_name()}",
                  FA=f"اطلاعات نامعتبر برای فیلد {field.name} مدل {self.class_name()}"))

        if string_format_dates:
            if string_format_dates:
                if isinstance(field, models.DateTimeField):
                    if get_avishan_config().USE_JALALI_DATETIME:
                        return BchDatetime(self.__getattribute__(field.name)).to_str('%Y/%m/%d %H:%M:%S')
                    return self.__getattribute__(field.name).strftime('%Y/%m/%d %H:%M:%S')
                if isinstance(field, models.DateField):
                    if get_avishan_config().USE_JALALI_DATETIME:
                        return BchDatetime(self.__getattribute__(field.name)).to_str('%Y/%m/%d')
                    return self.__getattribute__(field.name).strftime('%Y/%m/%d')
                if isinstance(field, models.TimeField):
                    return self.__getattribute__(field.name).strftime('%H:%M:%S')
            return self.__getattribute__(field.name)
        if isinstance(field, models.ManyToManyField):
            return self.__getattribute__(field.name).all()
        return self.__getattribute__(field.name)

    @staticmethod
    def get_sum_on_field(query_set: models.QuerySet, field_name: str) -> int:
        from django.db.models import Sum
        total = query_set.aggregate(Sum(field_name))[(field_name + '__sum')]
        if total:
            return total
        return 0

    @staticmethod
    def all_subclasses(cls):
        return set(cls.__subclasses__()).union([s for c in cls.__subclasses__() for s in AvishanModel.all_subclasses(c)])


class BaseUser(AvishanModel):
    __doc__ = '\n    Avishan user object. Name changed to "BaseUser" instead of "User" to make this model name available for app models.\n    '
    is_active = models.BooleanField(default=True, blank=True)
    language = models.CharField(max_length=255, default=(AvishanConfigFather.LANGUAGES.EN))
    date_created = models.DateTimeField(auto_now_add=True)
    private_fields = [
     date_created, 'id']

    def add_to_user_group(self, user_group: 'UserGroup') -> 'UserUserGroup':
        return user_group.add_user_to_user_group(self)

    @classmethod
    def create(cls, is_active=True):
        return super().create(is_active=is_active,
          language=(get_avishan_config().NEW_USERS_LANGUAGE if get_avishan_config().NEW_USERS_LANGUAGE is not None else get_avishan_config().LANGUAGE))

    def __str__(self):
        if hasattr(self, 'user'):
            return str(self.user)
        return super().__str__()


class UserGroup(AvishanModel):
    __doc__ = "\n    Every user most have at least one user group. User group controls it's member's overall activities. Every user have\n    an models.authentication.UserUserGroup to manage it's group membership.\n    "
    title = models.CharField(max_length=255, unique=True)
    token_valid_seconds = models.BigIntegerField(default=1800, blank=True)
    private_fields = [
     token_valid_seconds,
     'id']

    def add_user_to_user_group--- This code section failed: ---

 L. 639         0  SETUP_FINALLY        20  'to 20'

 L. 640         2  LOAD_GLOBAL              UserUserGroup
                4  LOAD_ATTR                objects
                6  LOAD_ATTR                get

 L. 641         8  LOAD_FAST                'base_user'

 L. 642        10  LOAD_FAST                'self'

 L. 640        12  LOAD_CONST               ('base_user', 'user_group')
               14  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
               16  POP_BLOCK        
               18  RETURN_VALUE     
             20_0  COME_FROM_FINALLY     0  '0'

 L. 644        20  DUP_TOP          
               22  LOAD_GLOBAL              UserUserGroup
               24  LOAD_ATTR                DoesNotExist
               26  COMPARE_OP               exception-match
               28  POP_JUMP_IF_FALSE    56  'to 56'
               30  POP_TOP          
               32  POP_TOP          
               34  POP_TOP          

 L. 645        36  LOAD_GLOBAL              UserUserGroup
               38  LOAD_ATTR                objects
               40  LOAD_ATTR                create

 L. 646        42  LOAD_FAST                'self'

 L. 647        44  LOAD_FAST                'base_user'

 L. 645        46  LOAD_CONST               ('user_group', 'base_user')
               48  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
               50  ROT_FOUR         
               52  POP_EXCEPT       
               54  RETURN_VALUE     
             56_0  COME_FROM            28  '28'
               56  END_FINALLY      

Parse error at or near `POP_TOP' instruction at offset 32

    def __str__(self):
        return self.title


class UserUserGroup(AvishanModel):
    __doc__ = '\n    Link between user and user group. Recommended object for addressing user and system models. It contains user group\n    and you can distinguish between multiple user accounts.\n\n    Token objects will contain address to this object, for having multiple-role login/logout without any interrupts.\n    '
    base_user = models.ForeignKey(BaseUser, on_delete=(models.CASCADE), related_name='user_user_groups')
    user_group = models.ForeignKey(UserGroup, on_delete=(models.CASCADE), related_name='user_user_groups')
    date_created = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True, blank=True)

    @property
    def last_used(self) -> Optional[datetime.datetime]:
        """
        Last used datetime. it will caught throw user devices. If never used, returns None
        """
        dates = []
        if hasattr(self, 'emailpasswordauthenticate'):
            dates.append(self.emailpasswordauthenticate.last_used)
        if hasattr(self, 'phonepasswordauthenticate'):
            dates.append(self.phonepasswordauthenticate.last_used)
        if len(dates) == 0:
            return
        return max(dates)

    @property
    def last_login(self) -> Optional[datetime.datetime]:
        """
        Last login comes from this user user group authorization types.
        """
        dates = []
        if hasattr(self, 'emailpasswordauthenticate'):
            dates.append(self.emailpasswordauthenticate.last_login)
        if hasattr(self, 'phonepasswordauthenticate'):
            dates.append(self.phonepasswordauthenticate.last_login)
        if len(dates) == 0:
            return
        return max(dates)

    @classmethod
    def create(cls, user_group, base_user=None):
        if base_user is None:
            base_user = BaseUser.create()
        return super().create(user_group=user_group, base_user=base_user)

    def __str__(self):
        return f"{self.base_user} - {self.user_group}"


class Email(AvishanModel):
    address = models.CharField(max_length=255, unique=True)
    date_verified = models.DateTimeField(default=None, null=True, blank=True)

    @classmethod
    def direct_non_authenticated_callable_methods(cls):
        return super().direct_non_authenticated_callable_methods() + ['start_verification', 'check_verification']

    def start_verification(self):
        self.send_verification_email(EmailVerification.create_verification(self).verification_code)
        return self

    def check_verification(self, code):
        if EmailVerification.check_email(self, code):
            self.date_verified = datetime.datetime.now()
            self.save()
        return self

    def send_verification_email(self, verification_code):
        from avishan.libraries.mailgun.functions import send_mail
        send_mail(recipient_list=[self.address], subject='Cayload Verification Code', message=f"Your verification code is: {verification_code}")

    @staticmethod
    def send_bulk_mail(subject: str, message: str, recipient_list: List[str], html_message: str=None):
        from django.core.mail import send_mail
        if html_message is not None:
            send_mail(subject, message, get_avishan_config().EMAIL_SENDER_ADDRESS, recipient_list, html_message)
        else:
            send_mail(subject, message, get_avishan_config().EMAIL_SENDER_ADDRESS, recipient_list)

    def send_mail(self, subject: str, message: str, html_message: str=None):
        from avishan.exceptions import ErrorMessageException
        import avishan.libraries.mailgun.functions as mailgun_send_mail
        if get_avishan_config().EMAIL_SENDER_ADDRESS is not None:
            self.send_bulk_mail(subject, message, [self.address], html_message)
        else:
            if get_avishan_config().MAILGUN_API_KEY is not None:
                mailgun_send_mail(recipient_list=[self.address], subject=subject, message=message)
            else:
                raise ErrorMessageException(AvishanTranslatable(EN='Email Provider not found'))

    def send_verification_code(self):
        email_verification = EmailVerification.create_verification(email=self)
        self.send_mail(subject='Cayload Verification Code',
          message=f"Your verification code is: {email_verification.verification_code}")

    def verify(self, code: str):
        if EmailVerification.check_email(self, code):
            self.date_verified = datetime.datetime.now()
            self.save()

    def __str__(self):
        return self.address

    @staticmethod
    def validate_signature(email: str) -> str:
        return email

    @staticmethod
    def get_or_create_email--- This code section failed: ---

 L. 785         0  SETUP_FINALLY        16  'to 16'

 L. 786         2  LOAD_GLOBAL              Email
                4  LOAD_ATTR                get
                6  LOAD_FAST                'email_address'
                8  LOAD_CONST               ('address',)
               10  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
               12  POP_BLOCK        
               14  RETURN_VALUE     
             16_0  COME_FROM_FINALLY     0  '0'

 L. 787        16  DUP_TOP          
               18  LOAD_GLOBAL              Email
               20  LOAD_ATTR                DoesNotExist
               22  COMPARE_OP               exception-match
               24  POP_JUMP_IF_FALSE    48  'to 48'
               26  POP_TOP          
               28  POP_TOP          
               30  POP_TOP          

 L. 788        32  LOAD_GLOBAL              Email
               34  LOAD_ATTR                create
               36  LOAD_FAST                'email_address'
               38  LOAD_CONST               ('address',)
               40  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
               42  ROT_FOUR         
               44  POP_EXCEPT       
               46  RETURN_VALUE     
             48_0  COME_FROM            24  '24'

 L. 789        48  DUP_TOP          
               50  LOAD_GLOBAL              Exception
               52  COMPARE_OP               exception-match
               54  POP_JUMP_IF_FALSE    84  'to 84'
               56  POP_TOP          
               58  STORE_FAST               'e'
               60  POP_TOP          
               62  SETUP_FINALLY        72  'to 72'

 L. 790        64  LOAD_CONST               1
               66  STORE_FAST               'a'
               68  POP_BLOCK        
               70  BEGIN_FINALLY    
             72_0  COME_FROM_FINALLY    62  '62'
               72  LOAD_CONST               None
               74  STORE_FAST               'e'
               76  DELETE_FAST              'e'
               78  END_FINALLY      
               80  POP_EXCEPT       
               82  JUMP_FORWARD         86  'to 86'
             84_0  COME_FROM            54  '54'
               84  END_FINALLY      
             86_0  COME_FROM            82  '82'

Parse error at or near `POP_TOP' instruction at offset 28

    @classmethod
    def get(cls, address=None, avishan_to_dict=False, avishan_raise_400=False, **kwargs):
        if address is not None:
            kwargs['address'] = cls.validate_signature(address)
        return (super().get)(avishan_to_dict, avishan_raise_400, **kwargs)

    @classmethod
    def create(cls, address=None):
        return super().create(address=(cls.validate_signature(address)))

    def update(self, address=None):
        return super().update(address=(self.validate_signature(address)))

    @classmethod
    def filter(cls, avishan_to_dict=False, **kwargs):
        data = {**{'avishan_to_dict': avishan_to_dict}, **kwargs}
        if 'address' in data.keys():
            data['address'] = cls.validate_signature(kwargs['address'])
        return (super().filter)(**data)


class EmailVerification(AvishanModel):
    email = models.OneToOneField(Email, on_delete=(models.CASCADE), related_name='verification')
    verification_code = models.CharField(max_length=255, blank=True, null=True, default=None)
    verification_date = models.DateTimeField(auto_now_add=True)
    tried_codes = models.TextField(blank=True, default='')
    private_fields = [
     verification_code, verification_date, tried_codes]

    @staticmethod
    def create_verification(email: Email) -> 'EmailVerification':
        from avishan.exceptions import ErrorMessageException
        if hasattr(email, 'verification'):
            previous = email.verification
            if (BchDatetime() - BchDatetime(previous.verification_date)).total_seconds() < get_avishan_config().EMAIL_VERIFICATION_GAP_SECONDS:
                raise ErrorMessageException(AvishanTranslatable(EN='Verification Code sent recently, Please try again later'),
                  status_code=(status.HTTP_401_UNAUTHORIZED))
            previous.remove()
        return EmailVerification.create(email=email, verification_code=(EmailVerification.create_verification_code()))

    @staticmethod
    def check_email(email: Email, code: str) -> bool:
        from avishan.exceptions import ErrorMessageException
        try:
            item = EmailVerification.get(email=email)
        except EmailVerification.DoesNotExist:
            raise ErrorMessageException(AvishanTranslatable(EN=f"Email Verification not found for email {email}"))
        else:
            if (BchDatetime() - BchDatetime(item.verification_date)).total_seconds() > get_avishan_config().EMAIL_VERIFICATION_VALID_SECONDS:
                item.remove()
                raise ErrorMessageException(AvishanTranslatable(EN='Code Expired, Request new one'))
            if item.verification_code == code:
                item.remove()
                return True
            if len(item.tried_codes.splitlines()) > get_avishan_config().EMAIL_VERIFICATION_TRIES_COUNT - 1:
                item.remove()
                raise ErrorMessageException(AvishanTranslatable(EN=f"Incorrect code repeated {get_avishan_config().EMAIL_VERIFICATION_TRIES_COUNT} times, request new code"))
            item.tried_codes += f"{code}\n"
            item.save()
            raise ErrorMessageException(AvishanTranslatable(EN='Incorrect code'))

    @staticmethod
    def create_verification_code() -> str:
        import random
        return str(random.randint(10 ** (get_avishan_config().PHONE_VERIFICATION_CODE_LENGTH - 1), 10 ** get_avishan_config().PHONE_VERIFICATION_CODE_LENGTH - 1))


class Phone(AvishanModel):
    number = models.CharField(max_length=255, unique=True)
    date_verified = models.DateTimeField(default=None, null=True, blank=True)

    @classmethod
    def direct_non_authenticated_callable_methods(cls):
        return super().direct_non_authenticated_callable_methods() + ['start_verification', 'check_verification']

    @staticmethod
    def send_bulk_sms():
        pass

    def send_sms(self):
        pass

    def send_verification_sms(self, code):
        self.send_template_sms((get_avishan_config().SMS_SIGN_IN_TEMPLATE), token=code)

    def send_signup_verification_sms(self, code):
        self.send_template_sms((get_avishan_config().SMS_SIGN_UP_TEMPLATE), token=code)

    def send_template_sms(self, template_name, **kwargs):
        url = 'https://api.kavenegar.com/v1/' + get_avishan_config().KAVENEGAR_API_TOKEN + '/verify/lookup.json'
        querystring = {**{'receptor':self.number,  'template':template_name}, **kwargs}
        requests.request('GET', url, data='', headers={}, params=querystring)

    def start_verification(self):
        self.send_verification_sms(PhoneVerification.create_verification(self).verification_code)
        return self

    def check_verification(self, code):
        if PhoneVerification.check_phone(self, code):
            self.date_verified = datetime.datetime.now()
            self.save()
        return self

    def verify(self, code: str):
        if PhoneVerification.check_phone(self, code):
            self.date_verified = datetime.datetime.now()
            self.save()

    def __str__(self):
        return self.number

    @staticmethod
    def validate_signature(phone: str) -> str:
        from .utils import en_numbers
        phone = en_numbers(phone)
        phone = phone.replace(' ', '')
        phone = phone.replace('-', '')
        if phone.startswith('+'):
            phone = '00' + phone[1:]
        return phone

    @staticmethod
    def get_or_create_phone--- This code section failed: ---

 L. 934         0  SETUP_FINALLY        16  'to 16'

 L. 935         2  LOAD_GLOBAL              Phone
                4  LOAD_ATTR                get
                6  LOAD_FAST                'phone_number'
                8  LOAD_CONST               ('number',)
               10  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
               12  POP_BLOCK        
               14  RETURN_VALUE     
             16_0  COME_FROM_FINALLY     0  '0'

 L. 936        16  DUP_TOP          
               18  LOAD_GLOBAL              Phone
               20  LOAD_ATTR                DoesNotExist
               22  COMPARE_OP               exception-match
               24  POP_JUMP_IF_FALSE    48  'to 48'
               26  POP_TOP          
               28  POP_TOP          
               30  POP_TOP          

 L. 937        32  LOAD_GLOBAL              Phone
               34  LOAD_ATTR                create
               36  LOAD_FAST                'phone_number'
               38  LOAD_CONST               ('number',)
               40  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
               42  ROT_FOUR         
               44  POP_EXCEPT       
               46  RETURN_VALUE     
             48_0  COME_FROM            24  '24'
               48  END_FINALLY      

Parse error at or near `POP_TOP' instruction at offset 28

    @classmethod
    def get(cls, number=None, avishan_to_dict=False, avishan_raise_400=False, **kwargs):
        if number is not None:
            kwargs['number'] = cls.validate_signature(number)
        return (super().get)(avishan_to_dict, avishan_raise_400, **kwargs)

    @classmethod
    def create(cls, number=None):
        return super().create(number=(cls.validate_signature(number)))

    def update(self, number=None):
        return super().update(number=(self.validate_signature(number)))

    @classmethod
    def filter(cls, avishan_to_dict=False, **kwargs):
        data = {**{'avishan_to_dict': avishan_to_dict}, **kwargs}
        if 'number' in data.keys():
            data['number'] = cls.validate_signature(kwargs['number'])
        return (super().filter)(**data)


class PhoneVerification(AvishanModel):
    phone = models.OneToOneField(Phone, on_delete=(models.CASCADE), related_name='verification')
    verification_code = models.CharField(max_length=255, blank=True, null=True, default=None)
    verification_date = models.DateTimeField(auto_now_add=True)
    tried_codes = models.TextField(blank=True, default='')
    private_fields = [
     verification_code, verification_date, tried_codes]

    @staticmethod
    def create_verification(phone: Phone) -> 'PhoneVerification':
        from avishan.exceptions import ErrorMessageException
        if hasattr(phone, 'verification'):
            previous = phone.verification
            if (BchDatetime() - BchDatetime(previous.verification_date)).total_seconds() < get_avishan_config().PHONE_VERIFICATION_GAP_SECONDS:
                raise ErrorMessageException(AvishanTranslatable(EN='Verification Code sent recently, Please try again later',
                  FA='برای ارسال مجدد کد، کمی صبر کنید'))
            previous.remove()
        return PhoneVerification.create(phone=phone, verification_code=(PhoneVerification.create_verification_code()))

    @staticmethod
    def check_phone(phone: Phone, code: str) -> bool:
        from avishan.exceptions import ErrorMessageException
        try:
            item = PhoneVerification.get(phone=phone)
        except PhoneVerification.DoesNotExist:
            raise ErrorMessageException(AvishanTranslatable(EN=f"Phone Verification not found for phone {phone}"))
        else:
            if (BchDatetime() - BchDatetime(item.verification_date)).total_seconds() > get_avishan_config().PHONE_VERIFICATION_VALID_SECONDS:
                item.remove()
                raise ErrorMessageException(AvishanTranslatable(EN='Code Expired, Request new one'))
            if item.verification_code == code:
                item.remove()
                return True
            if len(item.tried_codes.splitlines()) > get_avishan_config().PHONE_VERIFICATION_TRIES_COUNT - 1:
                item.remove()
                raise ErrorMessageException(AvishanTranslatable(EN=f"Incorrect Code repeated {get_avishan_config().PHONE_VERIFICATION_TRIES_COUNT} times, request new code"))
            item.tried_codes += f"{code}\n"
            item.save()
            raise ErrorMessageException(AvishanTranslatable(EN='Incorrect Code'))

    @staticmethod
    def create_verification_code() -> str:
        import random
        return str(random.randint(10 ** (get_avishan_config().PHONE_VERIFICATION_CODE_LENGTH - 1), 10 ** get_avishan_config().PHONE_VERIFICATION_CODE_LENGTH - 1))


class AuthenticationType(AvishanModel):
    user_user_group = models.OneToOneField(UserUserGroup, on_delete=(models.CASCADE))
    last_used = models.DateTimeField(default=None, blank=True, null=True)
    last_login = models.DateTimeField(default=None, blank=True, null=True)
    last_logout = models.DateTimeField(default=None, blank=True, null=True)

    class Meta:
        abstract = True

    def _logout(self):
        self.last_logout = BchDatetime().to_datetime()
        self.save()
        current_request['authentication_object'] = None
        current_request['add_token'] = False

    def _login(self):
        from avishan.utils import populate_current_request
        self.last_login = BchDatetime().to_datetime()
        self.last_logout = None
        self.save()
        populate_current_request(self)

    @classmethod
    def key_field(cls) -> models.ForeignKey:
        raise NotImplementedError()


class KeyValueAuthentication(AuthenticationType):
    hashed_password = models.CharField(max_length=255, blank=True, null=True, default=None)

    class Meta:
        abstract = True

    @classmethod
    def key_field(cls) -> models.ForeignKey:
        raise NotImplementedError()

    @staticmethod
    def _hash_password(password: str) -> str:
        """
        Hash entered password
        :param password:
        :return: hashed password in string
        """
        import bcrypt
        return bcrypt.hashpw(password.encode('utf8'), bcrypt.gensalt()).decode('utf8')

    @staticmethod
    def _check_password(password: str, hashed_password: str) -> bool:
        """
        compares password with hashed instance.
        :param password:
        :param hashed_password:
        :return: True if match
        """
        import bcrypt
        return bcrypt.checkpw(password.encode('utf8'), hashed_password.encode('utf8'))

    @classmethod
    def register(cls, user_user_group: UserUserGroup, key: str, password: Optional[str]=None) -> Union[('EmailPasswordAuthenticate', 'PhonePasswordAuthenticate')]:
        """
        Registration process for key-value authentications
        :param user_user_group:
        :param key: email, phone, ...
        :param password:
        :param kwargs:
        :return:
        """
        from avishan.exceptions import AuthException
        try:
            key_item = cls.key_field().related_model.get(key)
        except cls.key_field().related_model.DoesNotExist:
            key_item = cls.key_field().related_model.create(key)
        else:
            try:
                (cls.objects.get)(**{cls.key_field().name: key_item, 'user_user_group': user_user_group})
                raise AuthException(AuthException.DUPLICATE_AUTHENTICATION_IDENTIFIER)
            except cls.DoesNotExist:
                if hasattr(user_user_group, cls.key_field().name + 'passwordauthenticate'):
                    raise AuthException(AuthException.DUPLICATE_AUTHENTICATION_TYPE)
            else:
                data = {'user_user_group': user_user_group, 
                 cls.key_field().name: key_item}
                if password is not None:
                    data['hashed_password'] = cls._hash_password(password)
                return (cls.objects.create)(**data)

    def add_password(self, password: str) -> bool:
        if self.hashed_password is None:
            self.hashed_password = self._hash_password(password)
            self.save()
            return True
        return False

    @classmethod
    def login(cls, key: str, password: str, user_group: UserGroup=None) -> Union[('EmailPasswordAuthenticate', 'PhonePasswordAuthenticate')]:
        from avishan.exceptions import AuthException
        try:
            found_object = (cls.objects.get)(**{cls.key_field().name: cls.key_field().related_model.get(key), 
             'user_user_group__user_group': user_group})
        except (cls.DoesNotExist, cls.key_field().related_model.DoesNotExist):
            raise AuthException(AuthException.ACCOUNT_NOT_FOUND)
        else:
            if not cls._check_password(password, found_object.hashed_password):
                raise AuthException(AuthException.INCORRECT_PASSWORD)
            found_object._login()
            return found_object

    @classmethod
    def find(cls, key: str, password: str=None, user_group: UserGroup=None) -> List[Union[('EmailPasswordAuthenticate', 'PhonePasswordAuthenticate')]]:
        key = cls.key_field().related_model.validate_signature(key)
        kwargs = {}
        if user_group:
            kwargs['user_user_group__user_group'] = user_group
        try:
            kwargs[cls.key_field().name] = cls.key_field().related_model.get(key)
        except cls.key_field().related_model.DoesNotExist:
            return []
        else:
            founds = (cls.objects.filter)(**kwargs)
            if password:
                for found in founds:
                    if found._check_password(password, found.hashed_password):
                        return [
                         found]
                    return []

            return founds


class EmailPasswordAuthenticate(KeyValueAuthentication):
    email = models.ForeignKey(Email, on_delete=(models.CASCADE), related_name='password_authenticates')
    django_admin_list_display = [email, 'user_user_group', 'last_used', 'last_login', 'last_logout']

    @classmethod
    def key_field(cls) -> Union[(models.ForeignKey, models.Field)]:
        return cls.get_field('email')


class PhonePasswordAuthenticate(KeyValueAuthentication):
    phone = models.ForeignKey(Phone, on_delete=(models.CASCADE), related_name='password_authenticates')
    django_admin_list_display = ['user_user_group', phone]

    @classmethod
    def key_field(self) -> Union[(models.ForeignKey, models.Field)]:
        return self.get_field('phone')


class OtpAuthentication(AuthenticationType):
    code = models.CharField(max_length=255, blank=True, null=True)
    date_sent = models.DateTimeField(null=True, blank=True, default=None)
    tried_codes = models.TextField(blank=True, default='')

    class Meta:
        abstract = True

    @classmethod
    def key_field(cls) -> models.ForeignKey:
        raise NotImplementedError()

    @staticmethod
    def create_otp_code() -> str:
        return str(random.randint(10 ** (get_avishan_config().PHONE_VERIFICATION_CODE_LENGTH - 1), 10 ** get_avishan_config().PHONE_VERIFICATION_CODE_LENGTH - 1))

    def check_verification_code(self, entered_code: str) -> bool:
        from avishan.exceptions import ErrorMessageException
        if self.code is None:
            raise ErrorMessageException(AvishanTranslatable(EN='Code not found for this account',
              FA='برای این حساب کدی پیدا نشد'))
        if (BchDatetime() - BchDatetime(self.date_sent)).total_seconds() > get_avishan_config().PHONE_VERIFICATION_VALID_SECONDS:
            self.code = None
            self.save()
            raise ErrorMessageException(AvishanTranslatable(EN='Code Expired',
              FA='کد منقضی شده است'))
        if self.code != entered_code:
            self.tried_codes += f"{BchDatetime().to_datetime()} -> {entered_code}\n"
            self.save()
            return False
        self.code = None
        self.tried_codes = ''
        self.save()
        return True

    @classmethod
    def create_new(cls, user_user_group: UserUserGroup, key: str) -> 'PhoneOtpAuthenticate':
        from avishan.exceptions import AuthException
        try:
            key_item = cls.key_field().related_model.get(key)
        except cls.key_field().related_model.DoesNotExist:
            key_item = cls.key_field().related_model.create(key)
        else:
            try:
                (cls.objects.get)(**{cls.key_field().name: key_item, 'user_user_group': user_user_group})
                raise AuthException(AuthException.DUPLICATE_AUTHENTICATION_IDENTIFIER)
            except cls.DoesNotExist:
                if hasattr(user_user_group, cls.key_field().name + 'otpauthenticate'):
                    raise AuthException(AuthException.DUPLICATE_AUTHENTICATION_TYPE)
            else:
                return (cls.objects.create)(**{'user_user_group': user_user_group, 
                 cls.key_field().name: key_item})

    def verify_account(self) -> Union[('OtpAuthentication', 'PhoneOtpAuthenticate')]:
        self.send_otp_code()
        return self

    @classmethod
    def check_authentication(cls, key: str, entered_code: str, user_group: UserGroup) -> Tuple[(
 'PhoneOtpAuthenticate', bool)]:
        from avishan.exceptions import AuthException
        try:
            item = cls.find(key, user_group)[0]
        except IndexError:
            raise AuthException(AuthException.ACCOUNT_NOT_FOUND)
        else:
            if not item.check_verification_code(entered_code):
                raise AuthException(AuthException.INCORRECT_PASSWORD)
            elif item.last_login is None:
                created = True
                item.user_user_group.base_user.is_active = True
                item.user_user_group.base_user.save()
            else:
                created = False
            item._login()
            return (item, created)

    def send_otp_code(self):
        self.code = self.create_otp_code()
        self.date_sent = BchDatetime().to_datetime()
        self.tried_codes = ''
        self.save()

    @classmethod
    def find(cls, key: str, user_group: UserGroup=None) -> List['PhoneOtpAuthenticate']:
        key = cls.key_field().related_model.validate_signature(key)
        kwargs = {}
        if user_group:
            kwargs['user_user_group__user_group'] = user_group
        try:
            kwargs[cls.key_field().name] = cls.key_field().related_model.get(key)
        except cls.key_field().related_model.DoesNotExist:
            return []
        else:
            return (cls.objects.filter)(**kwargs)

    @classmethod
    def start_challenge(cls, key: str, user_group: UserGroup) -> Union[('OtpAuthentication', 'PhoneOtpAuthenticate')]:
        key = cls.key_field().related_model.validate_signature(key)
        found = cls.find(key)
        exact = None
        same_user = None
        for item in found:
            if item.user_user_group.user_group == user_group:
                exact = item
                break
            else:
                same_user = item
        else:
            if exact:
                return exact.verify_account()
            return cls.create_new(user_user_group=UserUserGroup.create(user_group=user_group,
              base_user=(same_user.user_user_group.base_user if same_user else None)),
              key=key).verify_account()

    @classmethod
    def complete_challenge(cls, key: str, code: str, user_group: UserGroup) -> Union[('OtpAuthentication', 'PhoneOtpAuthenticate')]:
        return cls.check_authentication(key, code, user_group)[0]


class PhoneOtpAuthenticate(OtpAuthentication):
    phone = models.ForeignKey(Phone, on_delete=(models.CASCADE), related_name='otp_authenticates')
    django_admin_list_display = [
     'user_user_group', 'phone', 'code']

    @classmethod
    def create(cls, phone, user_user_group):
        return super().create(phone=phone, user_user_group=user_user_group)

    @classmethod
    def key_field(cls) -> Union[(models.Field, models.ForeignKey)]:
        return cls.get_field('phone')

    def send_otp_code(self):
        super().send_otp_code()
        self.phone.send_verification_sms(self.code)
        self.save()


class VisitorKey(AuthenticationType):
    key = models.CharField(max_length=255, unique=True)
    django_admin_list_display = (
     key,)
    django_admin_search_fields = (key,)

    @classmethod
    def key_field(cls) -> models.Field:
        return cls.get_field('key')

    @staticmethod
    def create_key() -> str:
        import secrets
        return secrets.token_urlsafe(get_avishan_config().VISITOR_KEY_LENGTH)

    @classmethod
    def register(cls, user_user_group: UserUserGroup) -> 'VisitorKey':
        key = cls.create_key()
        while True:
            try:
                cls.get(key=key)
                key = cls.create_key()
            except cls.DoesNotExist:
                break

        data = {'user_user_group':user_user_group, 
         'key':key}
        return (cls.objects.create)(**data)

    @classmethod
    def login(cls, key: str, user_group: UserGroup) -> 'VisitorKey':
        from avishan.exceptions import AuthException
        try:
            found_object = (cls.objects.get)(key=key, 
             user_user_group__user_group=user_group)
        except cls.DoesNotExist:
            raise AuthException(AuthException.ACCOUNT_NOT_FOUND)
        else:
            found_object._login()
            return found_object

    def __str__(self):
        return self.key


class Image(AvishanModel):
    file = models.ImageField(blank=True, null=True)
    base_user = models.ForeignKey(BaseUser, on_delete=(models.SET_NULL), null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.file.url

    @classmethod
    def direct_callable_methods(cls):
        return super().direct_callable_methods() + ['image_from_multipart_form_data_request']

    @staticmethod
    def image_from_url(url: str) -> 'Image':
        """
        :param url: like "core/init_files/blue-car.png"
        """
        from django.core.files import File
        name = url.split('/')[(-1)]
        if '.' not in name:
            name = url.split('/')[(-2)]
        image = Image.objects.create()
        image.file.save(name, (File(open(url, 'rb'))), save=True)
        image.save()
        return image

    def to_dict(self, exclude_list: List[Union[(models.Field, str)]]=()) -> dict:
        return {'id':self.id, 
         'file':self.file.url}

    @classmethod
    def image_from_in_memory_upload(cls, file: InMemoryUploadedFile) -> 'Image':
        from avishan.exceptions import ErrorMessageException
        if file is None:
            raise ErrorMessageException(AvishanTranslatable(EN='File not found',
              FA='فایل ارسال نشده است'))
        created = Image.create(base_user=(current_request['base_user']))
        created.file.save(('uploaded_images/' + file.name), file, save=True)
        created.save()
        return created

    @classmethod
    def image_from_multipart_form_data_request(cls, name: str='file') -> 'Image':
        return cls.image_from_in_memory_upload(file=(current_request['request'].FILES.get(name)))


class File(AvishanModel):
    file = models.FileField(blank=True, null=True)
    base_user = models.ForeignKey(BaseUser, on_delete=(models.SET_NULL), null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)

    def to_dict(self, exclude_list: List[Union[(models.Field, str)]]=()) -> dict:
        return {'id':self.id, 
         'file':self.file.url}


class RequestTrack(AvishanModel):
    view_name = models.CharField(max_length=255, blank=True, null=True, default='NOT_AVAILABLE')
    url = models.TextField(blank=True, null=True)
    status_code = models.IntegerField(null=True, blank=True)
    method = models.CharField(max_length=255, null=True, blank=True)
    json_unsafe = models.BooleanField(null=True, blank=True)
    is_api = models.BooleanField(null=True, blank=True)
    add_token = models.BooleanField(null=True, blank=True)
    user_user_group = models.ForeignKey(UserUserGroup, on_delete=(models.SET_NULL), null=True, blank=True)
    request_data = models.TextField(null=True, blank=True)
    request_headers = models.TextField(null=True, blank=True)
    response_data = models.TextField(null=True, blank=True)
    start_time = models.DateTimeField(blank=True, null=True)
    end_time = models.DateTimeField(blank=True, null=True)
    total_execution_milliseconds = models.BigIntegerField(null=True, blank=True)
    view_execution_milliseconds = models.BigIntegerField(null=True, blank=True)
    authentication_type_class_title = models.CharField(max_length=255, blank=True, null=True)
    authentication_type_object_id = models.IntegerField(blank=True, null=True)
    django_admin_search_fields = [
     url]
    django_admin_list_display = [
     view_name, method, status_code, user_user_group, start_time,
     total_execution_milliseconds, url]

    def __str__(self):
        return self.view_name

    def create_exec_infos(self, data: list):
        dates = {}
        for part in data:
            dates[part['title']] = part['now']
        else:
            for part in data:
                if part['title'] == 'begin':
                    pass
                else:
                    RequestTrackExecInfo.create(request_track=self,
                      title=(part['title']),
                      start_time=(dates[part['from_title']]),
                      end_time=(part['now']),
                      milliseconds=((part['now'] - dates[part['from_title']]).total_seconds() * 1000))


class RequestTrackExecInfo(AvishanModel):
    request_track = models.ForeignKey(RequestTrack, on_delete=(models.CASCADE), related_name='exec_infos')
    title = models.CharField(max_length=255)
    start_time = models.DateTimeField(blank=True, null=True)
    end_time = models.DateTimeField(blank=True, null=True)
    milliseconds = models.FloatField(default=None, null=True, blank=True)
    django_admin_list_display = (
     request_track, title, start_time, milliseconds)
    django_admin_list_filter = (request_track, title)
    django_admin_list_max_show_all = 500
    django_admin_search_fields = (title,)

    @classmethod
    def create_dict(cls, title: str, from_title: str='begin'):
        current_request['request_track_exec'].append({'title':title, 
         'from_title':from_title, 
         'now':datetime.datetime.now()})

    def __str__(self):
        return self.title


class RequestTrackException(AvishanModel):
    request_track = models.OneToOneField(RequestTrack, on_delete=(models.CASCADE), related_name='exception')
    class_title = models.CharField(max_length=255, null=True, blank=True)
    args = models.TextField(null=True, blank=True)
    traceback = models.TextField(null=True, blank=True)
    django_admin_list_display = [
     request_track, class_title, args]


class TranslatableChar(AvishanModel):
    en = models.CharField(max_length=255, blank=True, null=True, default=None)
    fa = models.CharField(max_length=255, blank=True, null=True, default=None)

    @classmethod
    def create(cls, en=None, fa=None, auto=None):
        if en is not None:
            en = str(en)
            if len(en) == 0:
                en = None
        if fa is not None:
            fa = str(fa)
            if len(fa) == 0:
                fa = None
        return super().create(en=en, fa=fa)

    def to_dict(self, exclude_list: List[Union[(models.Field, str)]]=()) -> Union[(str, dict)]:
        if current_request['language'] == 'all':
            return {'en':self.en,  'fa':self.fa}
        return str(self)

    def __str__(self):
        try:
            return self.__getattribute__(current_request['language'].lower())
        except:
            return self.__getattribute__(get_avishan_config().LANGUAGE.lower())


class Activity(AvishanModel):
    title = models.CharField(max_length=255)
    user_user_group = models.ForeignKey(UserUserGroup, on_delete=(models.CASCADE))
    request_track = models.ForeignKey(RequestTrack, on_delete=(models.SET_NULL), null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)
    object_class = models.CharField(max_length=255, blank=True, null=True)
    object_id = models.BigIntegerField(default=None, null=True, blank=True)
    data = models.TextField(blank=True, null=True)
    django_admin_list_display = [
     user_user_group, title, data, object_class, object_id, date_created]

    @classmethod
    def create(cls, title, object_class=None, object_id=None, data=None):
        request_track = current_request['request_track_object']
        user_user_group = current_request['user_user_group']
        if not request_track:
            if not user_user_group:
                return
        return super().create(title=title,
          user_user_group=(user_user_group if user_user_group else request_track.user_user_group),
          request_track=request_track,
          object_class=object_class,
          object_id=object_id,
          data=data)

    @classmethod
    def class_plural_snake_case_name(cls) -> str:
        return 'activities'

    def __str__(self):
        return self.title