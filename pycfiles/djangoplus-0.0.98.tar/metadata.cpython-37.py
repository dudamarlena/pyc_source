# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/breno/Envs/djangoplus/lib/python3.7/site-packages/djangoplus/utils/metadata.py
# Compiled at: 2019-08-10 20:06:45
# Size of source mod 2**32: 24921 bytes
import sys, inspect
import django.apps as apps
from django.utils.text import camel_case_to_spaces
from django.utils.safestring import mark_safe

def is_many_to_many(model, name):
    attr = hasattr(model, name) and getattr(model, name) or None
    return attr and hasattr(attr, 'field') and attr.field.__class__.__name__ == 'ManyToManyField' or False


def is_one_to_many(model, name):
    attr = hasattr(model, name) and getattr(model, name) or None
    return attr and hasattr(attr, 'field') and attr.field.__class__.__name__ == 'OneToManyField' or False


def is_one_to_one(model, name):
    attr = hasattr(model, name) and getattr(model, name) or None
    return attr and hasattr(attr, 'field') and attr.field.__class__.__name__ == 'OneToOneField' or False


def is_many_to_one(model, name):
    attr = hasattr(model, name) and getattr(model, name) or None
    return attr and attr.__class__.__name__ == 'ForwardManyToOneDescriptor' or False


def is_one_to_many_reverse(model, name):
    attr = hasattr(model, '{}_set'.format(name)) and getattr(model, '{}_set'.format(name)) or None
    return attr and attr.__class__.__name__ == 'ManyToManyDescriptor' or False


def list_m2m_fields_with_model(cls):
    return [(f, f.model if f.model != cls else None) for f in cls._meta.get_fields() if f.many_to_many if not f.auto_created]


def list_related_objects(cls):
    return [f for f in cls._meta.get_fields() if not f.one_to_many if f.one_to_one if f.auto_created]


def find_field_by_name(model, field_name):
    return model._meta.get_field(field_name)


def list_field_names(model, include_m2m=False):
    l = [field.name for field in model._meta.local_fields]
    if include_m2m:
        for field in model._meta.local_many_to_many:
            l.append(field.name)

    return l


def list_one_to_one_field_names(model):
    l = []
    for field_name in list_field_names(model):
        if is_one_to_one(model, field_name):
            l.append(field_name)

    return l


def get_field(model, lookup):
    tokens = lookup.split('__')
    tokens.reverse()
    field_name = tokens.pop()
    field = find_field_by_name(model, field_name)
    return get_field_recursively(field, tokens)


def get_field_recursively(field, tokens):
    if tokens:
        field_name = tokens.pop()
        if field.remote_field and field.remote_field.model:
            field = find_field_by_name(field.remote_field.model, field_name)
        else:
            field = find_field_by_name(field.related_model, field_name)
        return get_field_recursively(field, tokens)
    return field


def get_fieldsets(model, title='Dados Gerais'):
    fields = []
    for field in get_metadata(model, 'fields')[1:]:
        if not field.name.endswith('_ptr'):
            field.name == 'ascii' or field.name == 'tree_index' or fields.append(field.name)

    for field in get_metadata(model, 'local_many_to_many'):
        fields.append(field.name)

    fieldsets = ((title, dict(fields=fields)),)
    return fieldsets


def get_fiendly_name(model_or_field, lookup, as_tuple=False):
    l = []
    tokens = lookup.split('__')
    tokens.reverse()
    pronoun = None
    to = None
    while tokens:
        token = tokens.pop()
        if hasattr(model_or_field, token):
            field_or_function = getattr(model_or_field, token)
            if hasattr(field_or_function, 'field'):
                field_or_function = field_or_function.field
            elif hasattr(field_or_function, 'field_name'):
                field_or_function = model_or_field._meta.get_field(token)
        else:
            field_or_function = model_or_field
        if pronoun:
            if l:
                l.append(pronoun)
        if hasattr(field_or_function, 'remote_field') and field_or_function.remote_field and field_or_function.remote_field.model:
            pronoun = get_metadata(field_or_function.remote_field.model, 'verbose_female') and 'da' or 'do'
            if tokens:
                model_or_field = field_or_function.remote_field.model
                name = field_or_function.verbose_name
            else:
                model_or_field = field_or_function
                name = model_or_field.verbose_name
            sortable = True
            to = field_or_function.remote_field.model
        else:
            if hasattr(field_or_function, 'verbose_name'):
                model_or_field = field_or_function
                name = model_or_field.verbose_name
                sortable = True
            else:
                if hasattr(field_or_function, '_metadata'):
                    model_or_field = field_or_function
                    name = field_or_function._metadata['{}:verbose_name'.format(token)]
                    sortable = False
                else:
                    model_or_field = field_or_function
                    name = token
                    sortable = False
        l.append(str(name))

    l.reverse()
    verbose_name = ' '.join(l)
    verbose_name = l[0]
    return as_tuple and (verbose_name, lookup, sortable, to) or verbose_name


def set_metadata(cls, attr, value):
    if not hasattr(cls, '_metadata'):
        cls._metadata = dict()
    cls._metadata['{}:{}'.format(cls.__name__, attr)] = value


def get_metadata(model_or_func, attr, default=None, iterable=False):
    _metadata = None
    if hasattr(model_or_func, '_metadata'):
        _metadata = getattr(model_or_func, '_metadata')
        return _metadata.get('{}:{}'.format(model_or_func.__name__, attr))
    model = model_or_func
    metaclass = getattr(model_or_func, '_meta')
    field_attr = hasattr(metaclass, attr) or None
    if attr == 'search_fields':
        field_attr = 'search'
    else:
        if attr == 'exclude_fields':
            field_attr = 'exclude'
        else:
            if attr == 'list_filter':
                field_attr = 'filter'
            elif field_attr:
                _metadata = []
                fields = []
                for field in metaclass.fields:
                    fields.append(field)

                for m2m in list_m2m_fields_with_model(model):
                    fields.append(m2m[0])

                for field in fields:
                    if hasattr(field, field_attr):
                        value = getattr(field, field_attr)
                        if value:
                            if type(value) == bool:
                                if value:
                                    _metadata.append(field.name)
                            if type(value) in (list, tuple) and value:
                                for lookup in value:
                                    if lookup in ('pk', 'id'):
                                        _metadata.append(field.name)
                                    else:
                                        _metadata.append('{}__{}'.format(field.name, lookup))

                setattr(metaclass, field_attr, _metadata)
            else:
                _metadata = getattr(metaclass, attr)
                if callable(_metadata):
                    _metadata = _metadata()
                if _metadata is None:
                    if attr == 'list_display':
                        _metadata = []
                        fields = []
                        for field in metaclass.fields:
                            fields.append(field)

                        for field in metaclass.local_many_to_many:
                            fields.append(field)

                        for field in fields[1:6]:
                            if not field.name.endswith('_ptr'):
                                field.name == 'ascii' or field.name == 'tree_index' or _metadata.append(field.name)

                else:
                    _metadata = default
            if attr == 'fieldsets' and hasattr(model, 'fieldsets'):
                _metadata = model.fieldsets or default
            else:
                if attr == 'view_fieldsets':
                    if hasattr(model, 'view_fieldsets'):
                        _metadata = model.view_fieldsets
                    else:
                        _metadata = hasattr(model, 'fieldsets') and model.fieldsets or default
                else:
                    check_recursively = not _metadata
                    if attr in ('verbose_name', 'verbose_name_plural'):
                        if str(_metadata) in (camel_case_to_spaces(model.__name__), '{}s'.format(camel_case_to_spaces(model.__name__))):
                            check_recursively = True
                    if attr in ('list_menu', 'verbose_female', 'class_diagram'):
                        check_recursively = False
                    if check_recursively:
                        if hasattr(model, '__bases__'):
                            if model.__bases__:
                                if hasattr(model.__bases__[0], '_meta'):
                                    _metadata = get_metadata(model.__bases__[0], attr)
                    if iterable:
                        if _metadata:
                            if type(_metadata) not in (tuple, list):
                                _metadata = (
                                 _metadata,)
                        else:
                            _metadata = ()
                return _metadata


def get_scope(model, organization_model, unit_model):
    role_scope = get_metadata(model, 'role_scope')
    if role_scope:
        attr = getattr2(model, role_scope)
        if hasattr(attr, 'model'):
            return get_metadata(attr.model, 'verbose_name')
        field = get_field(model, role_scope)
        return get_metadata(field.remote_field.model, 'verbose_name')


def check_role(self, saving=True):
    role_name = get_metadata(self.__class__, 'role_name')
    role_username = get_metadata(self.__class__, 'role_username')
    verbose_name = get_metadata(self.__class__, 'verbose_name')
    role_email = get_metadata(self.__class__, 'role_email', '')
    role_scope = get_metadata(self.__class__, 'role_scope', False)
    role_notify = get_metadata(self.__class__, 'role_notify', False)
    if role_username:
        from django.conf import settings
        from django.contrib.auth.models import Group
        from djangoplus.admin.models import User, Role, Organization, Unit
        group_name = verbose_name
        username = getattr2(self, role_username)
        name = role_name and getattr2(self, role_name) or None
        email = role_email and getattr2(self, role_email) or ''
        scopes = []
        if username:
            if role_scope:
                value = getattr2(self, role_scope)
                if hasattr(value, 'all'):
                    for scope in value.all():
                        scopes.append(scope)

    elif value:
        scopes.append(value)
    group = Group.objects.get_or_create(name=group_name)[0]
    if saving:
        qs = User.objects.filter(username=username)
        if qs.exists():
            user = qs[0]
            user.email = email
            user.name = name or str(self)
            user.save()
        else:
            user = User()
            user.username = username
            user.name = name or str(self)
            user.email = email
            user.save()
            if user.email:
                if not settings.DEBUG:
                    if not 'test' in sys.argv:
                        user.send_access_invitation()
                already_in_group = user.groups.filter(pk=(group.pk)).exists()
                if not already_in_group:
                    user.groups.add(group)
                if scopes:
                    for scope in scopes:
                        Role.objects.get_or_create(user=user, group=group, scope=scope)

            else:
                Role.objects.get_or_create(user=user, group=group)
        if role_notify:
            already_in_group or user.send_access_invitation_for_group(group)
    else:
        user = User.objects.filter(username=username).first()
        if user:
            if scopes:
                for scope in scopes:
                    Role.objects.filter(user=user, group=group, scope=scope).delete()

            else:
                Role.objects.filter(user=user, group=group).delete()
            user.check_role_groups()


def iterable(string_or_iterable):
    if string_or_iterable is not None:
        if type(string_or_iterable) not in (list, tuple):
            return (
             string_or_iterable,)
    return string_or_iterable


def getattr2(obj, args):
    if args == '__str__':
        splitargs = [
         args]
    else:
        splitargs = args.split('__')
    return getattr_rec(obj, splitargs)


def getattr_rec(obj, args):
    if not obj:
        return
    if callable(obj):
        obj = obj()
    if len(args) > 1:
        attr = args.pop(0)
        return getattr_rec(getattr2(obj, attr), args)
    from django.core.exceptions import ObjectDoesNotExist
    try:
        model = type(obj)
        attr_name = args[0]
        attr = getattr(model, attr_name)
        value = None
        field = None
        if hasattr(attr, 'field_name'):
            field = getattr(model, '_meta').get_field(attr.field_name)
        else:
            if hasattr(attr, 'field'):
                field = attr.field
                if not obj.pk:
                    if is_many_to_many(model, attr_name):
                        value = field.related_model.objects.none()
                elif value is None:
                    value = getattr(obj, attr_name)
                elif field:
                    if hasattr(field, 'formatter'):
                        if field.formatter:
                            from djangoplus.cache import CACHE
                            func = CACHE['FORMATTERS'][field.formatter]
                            if count_parameters_names(func) == 1:
                                value = func(value)
                            else:
                                value = func(value, request=(obj.request), verbose_name=(field.verbose_name), instance=obj)
                            return mark_safe(str(value))
                        if hasattr(field, 'display') and field.display not in (True,
                                                                               False,
                                                                               None):
                            if hasattr(obj, field.display):
                                args[0] = field.display
                                return getattr_rec(obj, args)
                    else:
                        if hasattr(field, 'suffix'):
                            if field.suffix:
                                suffix = field.suffix
                                if hasattr(obj, field.suffix):
                                    suffix = getattr(obj, field.suffix)
                                    if callable(suffix):
                                        suffix = suffix()
                                return (
                                 value, suffix)
                        if hasattr(obj, 'get_{}_display'.format(args[0])):
                            return getattr(obj, 'get_{}_display'.format(args[0]))()
                else:
                    _metadata = hasattr(value, '_metadata') and getattr(value, '_metadata') or None
                    if _metadata:
                        return execute_and_format(obj.request, value)
                if callable(value):
                    if type(value).__name__ in ('ManyRelatedManager' or 'RelatedManager'):
                        value = value.all()
            else:
                value = value()
        return value
    except ObjectDoesNotExist:
        return


def get_can_execute(action):
    can_execute = []
    for group_name in action.get('can_execute_by_role') or ():
        can_execute.append(group_name)

    for group_name in action.get('can_execute_by_unit') or ():
        can_execute.append(group_name)

    for group_name in action.get('can_execute_by_organization') or ():
        can_execute.append(group_name)

    for group_name in action.get('can_execute') or ():
        can_execute.append(group_name)

    return can_execute


def should_add_action(action_inline, action_subsets, current_subset):
    subsets = []
    if current_subset == 'all':
        current_subset = None
    elif action_subsets:
        for subset_name in action_subsets:
            if subset_name == 'all':
                subsets.append(None)
            else:
                subsets.append(subset_name)

        if action_inline and None not in subsets:
            subsets.append(None)
    elif action_inline:
        subsets.append(None)
    return current_subset in subsets


def should_filter_or_display(request, model, to):
    if get_metadata(to, 'role_username'):
        can_view = list(get_metadata(model, 'can_admin', (), iterable=True) + get_metadata(model, 'can_admin_by_organization', (), iterable=True) + get_metadata(model, 'can_admin_by_unit', (), iterable=True) + get_metadata(model, 'can_admin_by_role', (), iterable=True) + get_metadata(model, 'can_list', (), iterable=True) + get_metadata(model, 'can_list_by_organization', (), iterable=True) + get_metadata(model, 'can_list_by_unit', (), iterable=True) + get_metadata(model, 'can_list_by_role', (), iterable=True) + get_metadata(model, 'can_view', (), iterable=True) + get_metadata(model, 'can_view_by_organization', (), iterable=True) + get_metadata(model, 'can_view_by_unit', (), iterable=True) + get_metadata(model, 'can_view_by_role', (), iterable=True))
        if not request.user.is_superuser:
            if can_view:
                if not (request.user.in_group)(*can_view):
                    return False
    return True


def find_action(model, action_name):
    from djangoplus.cache import CACHE
    for actions in (CACHE['INSTANCE_ACTIONS'], CACHE['QUERYSET_ACTIONS']):
        for action_group in actions[model]:
            for func_name, action in list(actions[model][action_group].items()):
                if action['verbose_name'] == action_name:
                    return action


def find_model_by_verbose_name(verbose_name):
    import django.apps as apps
    for model in apps.get_models():
        app_label = get_metadata(model, 'app_label')
        if app_label.startswith('admin') or get_metadata(model, 'verbose_name') == verbose_name.replace(' __ ', ' em '):
            return model


def find_model_by_verbose_name_plural(verbose_name_plural):
    import django.apps as apps
    for model in apps.get_models():
        app_label = get_metadata(model, 'app_label')
        if app_label.startswith('admin') or get_metadata(model, 'verbose_name_plural') == verbose_name_plural:
            return model


def find_subset_by_title(title, model):
    from djangoplus.cache import CACHE
    for subset in CACHE['SUBSETS'][model]:
        if subset['verbose_name'] == title:
            return subset


def find_model_by_add_label(add_label):
    import django.apps as apps
    for model in apps.get_models():
        if get_metadata(model, 'add_label') == add_label:
            return model


def find_model(model, key):
    tokens = key.split('__')
    tokens.reverse()
    return find_model_recursively(model, tokens)


def find_model_recursively(cls, tokens):
    if tokens:
        token = tokens.pop()
        try:
            attr = getattr(cls, token)
            if not hasattr(attr, 'field'):
                return cls
            return find_model_recursively(attr.field.remote_field.model, tokens)
        except AttributeError as e:
            try:
                for related_object in get_metadata(cls, 'related_objects'):
                    if related_object.name == token:
                        return find_model_recursively(related_object.related_model, tokens)

                raise e
            finally:
                e = None
                del e

    else:
        return cls


def check_condition(user, condition, obj):
    satisfied = True
    if obj.pk:
        if condition:
            model = type(obj)
            attr_name = condition.replace('not ', '')
            if hasattr(obj, attr_name):
                attr = getattr(obj, attr_name)
                if callable(attr):
                    satisfied = attr(*get_role_values_for_condition(attr, user))
                else:
                    satisfied = bool(attr)
            else:
                qs = model.objects.all()
                if hasattr(qs, attr_name):
                    attr = getattr(qs, attr_name)
                    satisfied = attr().filter(pk=(obj.pk)).exists()
                else:
                    raise Exception('The condition "{}" is invalid for {} because it is not an attribute or a method of {}, neither a method of its manager'.format(condition, obj, model))
            if 'not ' in condition:
                satisfied = not satisfied
    return satisfied


def get_parameters_names(func, include_annotated=False):
    parameters_names = []
    for name, parameter in inspect.signature(func).parameters.items():
        is_annotated = parameter.annotation is not None and parameter.annotation != inspect._empty
        if not is_annotated or include_annotated:
            parameters_names.append(name)

    return parameters_names


def count_parameters_names(func):
    return len(get_parameters_names(func))


def get_role_values_for_condition(func, user):
    parameters_values = []
    for name, parameter in inspect.signature(func).parameters.items():
        if parameter.annotation is not inspect.Parameter.empty:
            role_username = get_metadata(parameter.annotation, 'role_username')
            lookup = {role_username: user.username}
            role = (parameter.annotation.objects.filter)(**lookup).first()
            parameters_values.append(role)

    return parameters_values


def get_role_value_for_action(func, user, param_name):
    for name, parameter in inspect.signature(func).parameters.items():
        if name == param_name:
            role_username = get_metadata(parameter.annotation, 'role_username')
            lookup = {role_username: user.username}
            return (parameter.annotation.objects.filter)(**lookup).first()


def apply_formatter(value, formatter_name, **kwargs):
    from djangoplus.cache import CACHE
    formatter = CACHE['FORMATTERS'][formatter_name]
    if hasattr(formatter, '_formatter'):
        extra_parameter_names = get_parameters_names(formatter)[1:]
    else:
        extra_parameter_names = get_parameters_names(formatter.__init__)[2:]
    if extra_parameter_names:
        extra_parameter_values = {}
        for parameter_name in extra_parameter_names:
            if parameter_name in kwargs:
                extra_paramater_value = kwargs.get(parameter_name, None)
                extra_parameter_values[parameter_name] = extra_paramater_value

        f_return = formatter(value, **extra_parameter_values)
    else:
        f_return = formatter(value)
    return mark_safe(f_return)


def execute_and_format(request, func):
    verbose_name = get_metadata(func, 'verbose_name')
    formatter_name = get_metadata(func, 'formatter')
    icon = get_metadata(func, 'icon')
    params = request and get_role_values_for_condition(func, request.user) or []
    f_return = func(*params)
    if type(f_return).__name__ == 'QueryStatistics':
        if not formatter_name:
            formatter_name = 'statistics'
    if formatter_name:
        f_return = apply_formatter(f_return, formatter_name, request=request, title=verbose_name, icon=icon)
    return f_return


def get_parameters_details(model, func, input_name):
    input_params = []
    if func:
        param_provider = model
        if input_name:
            if '.' in input_name:
                param_provider = apps.get_model(input_name)
            else:
                module_name = model.__module__.replace('models', 'forms')
                forms_module = __import__(module_name, fromlist=(module_name.split('.')))
                param_provider = getattr(forms_module, input_name)
        for param_name in get_parameters_names(func, include_annotated=True):
            if hasattr(param_provider, 'pk'):
                field = get_field(model, param_name)
                verbose_name = field.verbose_name
                param_type = type(field)
                required = not field.blank
            else:
                field = param_provider.base_fields[param_name]
                verbose_name = field.label
                param_type = type(field)
                required = field.required
            help_text = field.help_text
            param_type = param_type.__name__.replace('Field', '')
            param = dict(verbose_name=verbose_name, name=param_name, type=param_type, required=required, help_text=help_text)
            input_params.append(param)

    return input_params


def get_register_parameters_details(model):
    input_params = []
    for field in get_metadata(model, 'fields'):
        if 'ptr' not in field.name and field.name != 'id':
            param = hasattr(field, 'exclude') and field.exclude or dict(verbose_name=(field.verbose_name),
              name=(field.name),
              type=(type(field).__name__.replace('Field', '')),
              required=(not field.blank),
              help_text=(field.help_text))
            input_params.append(param)

    return input_params