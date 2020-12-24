# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/afshari9978/Projects/namaki_backend/avishan/models.py
# Compiled at: 2020-05-12 01:17:40
# Size of source mod 2**32: 63656 bytes
import random
from inspect import Parameter
from typing import List, Type, Union, Tuple, Dict
import requests, stringcase
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.db.models import NOT_PROVIDED
from avishan import current_request
from avishan.configure import get_avishan_config, AvishanConfigFather
from avishan.libraries.faker import AvishanFaker
from avishan.misc import status
from avishan.misc.translation import AvishanTranslatable
import datetime
from typing import Optional
from avishan.misc.bch_datetime import BchDatetime
from django.db import models

class AvishanModel(models.Model, AvishanFaker):

    class Meta:
        abstract = True

    UNCHANGED = '__UNCHANGED__'
    private_fields = []
    private_fields: List[Union[(models.Field, str)]]
    export_ignore: bool = False
    django_admin_date_hierarchy = None
    django_admin_date_hierarchy: Optional[str]
    django_admin_list_display = []
    django_admin_list_display: List[models.Field]
    django_admin_list_filter = []
    django_admin_list_filter: List[models.Field]
    django_admin_list_max_show_all: int = 300
    django_admin_list_per_page: int = 100
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
            if avishan_raise_400:
                raise ErrorMessageException(AvishanTranslatable(EN=('Chosen ' + cls.__name__ + ' doesnt exist'),
                  FA=f"{cls.__name__} انتخاب شده موجود نیست"))
            raise e

    @classmethod
    def filter(cls, avishan_to_dict: bool=False, **kwargs):
        if avishan_to_dict:
            return [item.to_dict() for item in (cls.filter)(**kwargs)]
        else:
            if 'request' in current_request.keys():
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

            created.save()
        for after_create in after_creation:
            for target_object in after_create['target_objects']:
                (after_create['target_model'].create)(**{**{after_create['created_for_field'].name: created}, **target_object})

        return created

    def update(self, **kwargs):
        unchanged_list = []
        for key, value in kwargs.items():
            if value == self.UNCHANGED:
                unchanged_list.append(key)

        for key in unchanged_list:
            del kwargs[key]

        base_kwargs, many_to_many_kwargs, _ = (self.__class__._clean_model_data_kwargs)(**kwargs)
        for key, value in base_kwargs.items():
            self.__setattr__(key, value)

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
        else:
            result = cls.objects.none()
            for field in cls.get_fields():
                if isinstance(field, models.CharField):
                    result = (query_set.filter)(**{f"{field.name}__icontains": search_text}) | result

            return result.distinct()

    @classmethod
    def create_or_update(cls, fixed_kwargs: dict, new_additional_kwargs: dict):
        """
        Create object if doesnt exists. Else update it
        :param fixed_kwargs: key values to find object in db
        :param new_additional_kwargs: new changing kwargs
        :return: found/created object and True if created, False if found
        """
        try:
            found = (cls.objects.get)(**fixed_kwargs)
            for key, value in new_additional_kwargs.items():
                found.__setattr__(key, value)

            found.save()
            return (found, False)
        except cls.DoesNotExist:
            return (
             (cls.objects.create)(**{**fixed_kwargs, **new_additional_kwargs}),
             True)

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
                else:
                    if isinstance(field, models.DateField):
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

                    if isinstance(field, (models.OneToOneField, models.ForeignKey)):
                        dicted[field.name] = value.to_dict()
                    else:
                        if isinstance(field, models.ManyToManyField):
                            dicted[field.name] = [item.to_dict() for item in value.all()]
                        else:
                            if isinstance(value, datetime.time):
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
                if cls.is_field_required(field):
                    if not on_update:
                        if field.name not in kwargs.keys():
                            raise ErrorMessageException(AvishanTranslatable(EN=f"Field {field.name} not found in object {cls.class_name()}, and it's required."))
                if field.name not in kwargs.keys():
                    continue
                if isinstance(field, (models.OneToOneField, models.ForeignKey)):
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
                else:
                    if isinstance(field, models.ManyToManyField):
                        many_to_many_kwargs[field.name] = []
                        for input_item in kwargs[field.name]:
                            if isinstance(input_item, models.Model):
                                item_object = input_item
                            else:
                                item_object = field.related_model._AvishanModel__get_object_from_dict(input_item)
                            many_to_many_kwargs[field.name].append(item_object)

                    else:
                        base_kwargs[field.name] = cls.cast_field_data(kwargs[field.name], field)

        try:
            added_related_model_names = [item.class_snake_case_name() for item in cls.admin_related_models()]
        except:
            added_related_model_names = []

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

                    after_creation.append({'created_for_field':target_related_field, 
                     'target_objects':kwargs[related_name], 
                     'target_model':related_model})

        return (
         base_kwargs, many_to_many_kwargs, after_creation)

    @classmethod
    def _clean_form_post(cls, kwargs: dict) -> dict:
        output = {}
        try:
            added_related_model_names = [item.class_snake_case_name() for item in cls.admin_related_models()]
        except:
            added_related_model_names = []

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

                    for key in related_name_pack:
                        for i, final_pack in enumerate(kwargs[related_name]):
                            final_pack[key[len(related_name):]] = kwargs[key][i]

                for key in related_name_pack:
                    del kwargs[key]

        for key, value in kwargs.items():
            output[key] = value

        return output

    @classmethod
    def class_name(cls) -> str:
        return cls.__name__

    @classmethod
    def class_plural_name(cls) -> str:
        return cls.class_name() + 's'

    @classmethod
    def class_snake_case_name(cls) -> str:
        return stringcase.snakecase(cls.class_name())

    @classmethod
    def class_plural_snake_case_name(cls) -> str:
        return stringcase.snakecase(cls.class_plural_name())

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

            return subs

        total = []
        if not app_name:
            for model in AvishanModel.__subclasses__():
                total += get_sub_classes(model)

            return list(set(total))
        else:
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
        from django.apps import apps
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
            if field.auto_now or field.auto_now_add:
                return True
        if field.primary_key:
            return True
        else:
            return False

    @staticmethod
    def is_field_required(field: models.Field) -> bool:
        """
        Checks if field is required and create-blocking for model
        :param field:
        :return: True if required
        """
        if field.name == 'id' or field.default != NOT_PROVIDED or isinstance(field, models.DateField) or isinstance(field, models.TimeField) and (field.auto_now or field.auto_now_add):
            return False
        else:
            if isinstance(field, models.ManyToManyField):
                return False
            if field.blank or field.null:
                return False
            return True

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
        else:
            if isinstance(field, (models.CharField, models.TextField)):
                cast_class = str
            else:
                if isinstance(field, (models.IntegerField, models.AutoField)):
                    cast_class = int
                else:
                    if isinstance(field, models.FloatField):
                        cast_class = float
                    elif isinstance(field, models.TimeField):
                        if not isinstance(data, datetime.time):
                            cast_class = datetime.time
                        else:
                            cast_class = None
                    elif isinstance(field, models.DateTimeField):
                        if not isinstance(data, datetime.datetime):
                            cast_class = datetime.datetime
                        else:
                            cast_class = None
                    elif isinstance(field, models.DateField):
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
                        else:
                            if isinstance(cast_class, datetime.datetime):
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

            raise ErrorMessageException(AvishanTranslatable(EN=f"Incorrect Data entered for field {field.name} in model {self.class_name()}",
              FA=f"اطلاعات نامعتبر برای فیلد {field.name} مدل {self.class_name()}"))
        if string_format_dates:
            if string_format_dates:
                if isinstance(field, models.DateTimeField):
                    if get_avishan_config().USE_JALALI_DATETIME:
                        return BchDatetime(self.__getattribute__(field.name)).to_str('%Y/%m/%d %H:%M:%S')
                    else:
                        return self.__getattribute__(field.name).strftime('%Y/%m/%d %H:%M:%S')
                else:
                    if isinstance(field, models.DateField):
                        if get_avishan_config().USE_JALALI_DATETIME:
                            return BchDatetime(self.__getattribute__(field.name)).to_str('%Y/%m/%d')
                        else:
                            return self.__getattribute__(field.name).strftime('%Y/%m/%d')
                    if isinstance(field, models.TimeField):
                        return self.__getattribute__(field.name).strftime('%H:%M:%S')
            return self.__getattribute__(field.name)
        else:
            if isinstance(field, models.ManyToManyField):
                return self.__getattribute__(field.name).all()
            return self.__getattribute__(field.name)

    @staticmethod
    def get_sum_on_field(query_set: models.QuerySet, field_name: str) -> int:
        from django.db.models import Sum
        total = query_set.aggregate(Sum(field_name))[(field_name + '__sum')]
        if total:
            return total
        else:
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

    @classmethod
    def create(cls):
        return super().create(language=(get_avishan_config().NEW_USERS_LANGUAGE if get_avishan_config().NEW_USERS_LANGUAGE is not None else get_avishan_config().LANGUAGE))

    def add_to_user_group(self, user_group: 'UserGroup') -> 'UserUserGroup':
        return user_group.add_user_to_user_group(self)

    def __str__(self):
        if hasattr(self, 'user'):
            return str(self.user)
        else:
            return super().__str__()


class UserGroup(AvishanModel):
    __doc__ = "\n    Every user most have at least one user group. User group controls it's member's overall activities. Every user have\n    an models.authentication.UserUserGroup to manage it's group membership.\n    "
    title = models.CharField(max_length=255, unique=True)
    token_valid_seconds = models.BigIntegerField(default=1800, blank=True)
    private_fields = [
     token_valid_seconds,
     'id']

    @classmethod
    def create(cls, title, token_valid_seconds):
        return super().create(title=title, token_valid_seconds=token_valid_seconds)

    def add_user_to_user_group(self, base_user: BaseUser) -> 'UserUserGroup':
        """
        Create UUG or return it if available
        """
        try:
            return UserUserGroup.objects.get(base_user=base_user,
              user_group=self)
        except UserUserGroup.DoesNotExist:
            return UserUserGroup.objects.create(user_group=self,
              base_user=base_user)

    def __str__(self):
        return self.title


class UserUserGroup(AvishanModel):
    __doc__ = '\n    Link between user and user group. Recommended object for addressing user and system models. It contains user group\n    and you can distinguish between multiple user accounts.\n\n    Token objects will contain address to this object, for having multiple-role login/logout without any interrupts.\n    '
    base_user = models.ForeignKey(BaseUser, on_delete=(models.CASCADE), related_name='user_user_groups')
    user_group = models.ForeignKey(UserGroup, on_delete=(models.CASCADE), related_name='user_user_groups')
    date_created = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True, blank=True)

    @classmethod
    def create(cls, user_group, base_user=None):
        if base_user is None:
            base_user = BaseUser.create()
        return super().create(user_group=user_group, base_user=base_user)

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
        else:
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
        else:
            return max(dates)

    def __str__(self):
        return f"{self.base_user} - {self.user_group}"


class Email(AvishanModel):
    address = models.CharField(max_length=255, unique=True)
    date_verified = models.DateTimeField(default=None, null=True, blank=True)

    @classmethod
    def direct_non_authenticated_callable_methods(cls):
        return super().direct_non_authenticated_callable_methods() + ['start_verification', 'check_verification']

    @classmethod
    def create(cls, address):
        return super().create(address=(cls.validate_signature(address)))

    def start_verification(self):
        self.send_verification_email(EmailVerification.create_verification(self).verification_code)
        return self

    def check_verification(self, code: str):
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
        from avishan.libraries.mailgun.functions import send_mail as mailgun_send_mail
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
    def get_or_create_email(email_address: str) -> 'Email':
        try:
            return Email.get(address=email_address)
        except Email.DoesNotExist:
            return Email.create(address=email_address)
        except Exception as e:
            a = 1

    @classmethod
    def get(cls, address=None, avishan_to_dict=False, avishan_raise_400=False, **kwargs):
        if address is not None:
            kwargs['address'] = cls.validate_signature(address)
        return (super().get)(avishan_to_dict, avishan_raise_400, **kwargs)

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
    export_ignore = True

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
        return str(random.randint(10 ** (get_avishan_config().POA_VERIFICATION_CODE_LENGTH - 1), 10 ** get_avishan_config().POA_VERIFICATION_CODE_LENGTH - 1))


class Phone(AvishanModel):
    number = models.CharField(max_length=255, unique=True)
    date_verified = models.DateTimeField(default=None, null=True, blank=True)

    @classmethod
    def direct_non_authenticated_callable_methods(cls):
        return super().direct_non_authenticated_callable_methods() + ['start_verification', 'check_verification']

    @classmethod
    def create(cls, number):
        return super().create(number=(cls.validate_signature(number)))

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

    def check_verification(self, code: str):
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
    def get_or_create_phone(phone_number: str) -> 'Phone':
        try:
            return Phone.get(number=phone_number)
        except Phone.DoesNotExist:
            return Phone.create(number=phone_number)

    @classmethod
    def get(cls, number=None, avishan_to_dict=False, avishan_raise_400=False, **kwargs):
        if number is not None:
            kwargs['number'] = cls.validate_signature(number)
        return (super().get)(avishan_to_dict, avishan_raise_400, **kwargs)

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

    @classmethod
    def create(cls, phone, verification_code):
        return super().create(phone=phone, verification_code=verification_code)

    @staticmethod
    def create_verification(phone: Phone) -> 'PhoneVerification':
        from avishan.exceptions import ErrorMessageException
        if hasattr(phone, 'verification'):
            previous = phone.verification
            if (datetime.datetime.now() - previous.verification_date).total_seconds() < get_avishan_config().PHONE_VERIFICATION_GAP_SECONDS:
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

        if (BchDatetime() - BchDatetime(item.verification_date)).total_seconds() > get_avishan_config().POA_VERIFICATION_VALID_SECONDS:
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
        return str(random.randint(10 ** (get_avishan_config().POA_VERIFICATION_CODE_LENGTH - 1), 10 ** get_avishan_config().POA_VERIFICATION_CODE_LENGTH - 1))


class AuthenticationType(AvishanModel):
    user_user_group = models.OneToOneField(UserUserGroup, on_delete=(models.CASCADE))
    last_used = models.DateTimeField(default=None, blank=True, null=True)
    last_login = models.DateTimeField(default=None, blank=True, null=True)
    last_logout = models.DateTimeField(default=None, blank=True, null=True)
    export_ignore = True

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

        try:
            (cls.objects.get)(**{cls.key_field().name: key_item, 'user_user_group': user_user_group})
            raise AuthException(AuthException.DUPLICATE_AUTHENTICATION_IDENTIFIER)
        except cls.DoesNotExist:
            if hasattr(user_user_group, cls.key_field().name + 'passwordauthenticate'):
                raise AuthException(AuthException.DUPLICATE_AUTHENTICATION_TYPE)

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
        else:
            return False

    @classmethod
    def login(cls, key: str, password: str, user_group: UserGroup=None) -> Union[('EmailPasswordAuthenticate', 'PhonePasswordAuthenticate')]:
        from avishan.exceptions import AuthException
        try:
            found_object = (cls.objects.get)(**{cls.key_field().name: cls.key_field().related_model.get(key), 
             'user_user_group__user_group': user_group})
        except (cls.DoesNotExist, cls.key_field().related_model.DoesNotExist):
            raise AuthException(AuthException.ACCOUNT_NOT_FOUND)

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
            else:
                return founds


class EmailPasswordAuthenticate(KeyValueAuthentication):
    email = models.ForeignKey(Email, on_delete=(models.CASCADE), related_name='password_authenticates')
    django_admin_list_display = [email, 'user_user_group', 'last_used', 'last_login', 'last_logout']

    @classmethod
    def create(cls, email, password):
        return super().create(email)

    @classmethod
    def key_field(cls) -> Union[(models.ForeignKey, models.Field)]:
        return cls.get_field('email')


class PhonePasswordAuthenticate(KeyValueAuthentication):
    phone = models.ForeignKey(Phone, on_delete=(models.CASCADE), related_name='password_authenticates')
    django_admin_list_display = ['user_user_group', phone]

    @classmethod
    def key_field(cls) -> Union[(models.ForeignKey, models.Field)]:
        return cls.get_field('phone')


class OtpAuthentication(AuthenticationType):
    code = models.CharField(max_length=255, blank=True, null=True)
    date_sent = models.DateTimeField(null=True, blank=True, default=None)
    tried_codes = models.TextField(blank=True, default='')

    class Meta:
        abstract = True

    @classmethod
    def create_new(cls, user_user_group: UserUserGroup, key: str) -> 'OtpAuthentication':
        from avishan.exceptions import AuthException
        try:
            key_item = cls.key_field().related_model.get(key)
        except cls.key_field().related_model.DoesNotExist:
            key_item = cls.key_field().related_model.create(key)

        try:
            (cls.objects.get)(**{cls.key_field().name: key_item, 'user_user_group': user_user_group})
            raise AuthException(AuthException.DUPLICATE_AUTHENTICATION_IDENTIFIER)
        except cls.DoesNotExist:
            if hasattr(user_user_group, cls.key_field().name + 'otpauthenticate'):
                raise AuthException(AuthException.DUPLICATE_AUTHENTICATION_TYPE)

        return (cls.objects.create)(**{'user_user_group': user_user_group, 
         cls.key_field().name: key_item})

    @classmethod
    def key_field(cls) -> models.ForeignKey:
        raise NotImplementedError()

    @staticmethod
    def create_otp_code() -> str:
        return str(random.randint(10 ** (get_avishan_config().POA_VERIFICATION_CODE_LENGTH - 1), 10 ** get_avishan_config().POA_VERIFICATION_CODE_LENGTH - 1))

    def check_verification_code(self, entered_code: str) -> bool:
        from avishan.exceptions import ErrorMessageException
        if self.code is None:
            raise ErrorMessageException(AvishanTranslatable(EN='Code not found for this account',
              FA='برای این حساب کدی پیدا نشد'))
        if (BchDatetime() - BchDatetime(self.date_sent)).total_seconds() > get_avishan_config().POA_VERIFICATION_VALID_SECONDS:
            self.code = None
            self.save()
            raise ErrorMessageException(AvishanTranslatable(EN='Code Expired',
              FA='کد منقضی شده است'))
        if self.code != entered_code:
            self.tried_codes += f"{BchDatetime().to_datetime()} -> {entered_code}\n"
            self.save()
            return False
        else:
            self.code = None
            self.tried_codes = ''
            self.save()
            return True

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

        if not item.check_verification_code(entered_code):
            raise AuthException(AuthException.INCORRECT_PASSWORD)
        else:
            if item.last_login is None:
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

        if exact:
            return exact.verify_account()
        else:
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
    def create(cls, key):
        return super().create(key=key)

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

        found_object._login()
        return found_object

    def __str__(self):
        return self.key


class Image(AvishanModel):
    file = models.ImageField(blank=True, null=True)
    base_user = models.ForeignKey(BaseUser, on_delete=(models.SET_NULL), null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)
    export_ignore = True

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
    export_ignore = True

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
    export_ignore = True

    def __str__(self):
        return self.view_name

    def create_exec_infos(self, data: list):
        dates = {}
        for part in data:
            dates[part['title']] = part['now']

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
    export_ignore = True

    @classmethod
    def create(cls, request_track, title, start_time, end_time, milliseconds):
        return super().create(request_track=request_track, title=title, start_time=start_time, end_time=end_time, milliseconds=milliseconds)

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
    export_ignore = True

    @classmethod
    def create(cls, request_track, class_title, args, traceback):
        return super().create(request_track=request_track,
          class_title=class_title,
          args=args,
          traceback=traceback)


class TranslatableChar(AvishanModel):
    en = models.CharField(max_length=255, blank=True, null=True, default=None)
    fa = models.CharField(max_length=255, blank=True, null=True, default=None)
    export_ignore = True

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
            return {'en':self.en, 
             'fa':self.fa}
        else:
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
    export_ignore = True

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
    def class_plural_name(cls) -> str:
        return 'Activities'

    def __str__(self):
        return self.title