# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/rest_framework_extras/__init__.py
# Compiled at: 2017-05-03 08:53:06
import logging, re
from collections import OrderedDict
from django.conf import settings
from django.db.utils import OperationalError, ProgrammingError
from rest_framework.permissions import DjangoModelPermissions
from rest_framework_extras.serializers import HyperlinkedModelSerializer
logger = logging.getLogger('django')

def get_settings():
    """Due to app loading issues during startup provide a function to return
    settings only when needed."""
    from rest_framework.authentication import SessionAuthentication, BasicAuthentication
    return getattr(settings, 'REST_FRAMEWORK_EXTRAS', {'blacklist': {'sessions-session': {}, 'admin-logentry': {}}, 'authentication-classes': (
                                SessionAuthentication, BasicAuthentication), 
       'permission-classes': (
                            DjangoModelPermissions,)})


def discover(router, override=None, only=None, exclude=None):
    """Generate default serializers and viewsets. This function should be run
    before doing normal registration through the router."""
    from django.contrib.contenttypes.models import ContentType
    from rest_framework import viewsets
    try:
        list(ContentType.objects.all())
    except (OperationalError, ProgrammingError):
        return False

    filters = OrderedDict()
    if only is None:
        for app in reversed(settings.INSTALLED_APPS):
            for ct in ContentType.objects.filter(app_label=app.split('.')[(-1)]):
                filters['%s.%s' % (ct.app_label, ct.model)] = {'content_type': ct}

    for el in only or [] or override or []:
        pattern_or_name = form = admin = admin_site = None
        if isinstance(el, (list, tuple)):
            pattern_or_name, di = el
            form = di.get('form', None)
            admin = di.get('admin', None)
            admin_site = di.get('admin_site', None)
            if any((admin, admin_site)) and not all((admin, admin_site)):
                raise RuntimeError('admin and admin_site are mutually inclusive')
        else:
            pattern_or_name = el
        di = {}
        try:
            app_label, model = re.split('[\\.-]', pattern_or_name)
            di = {'app_label': app_label, 'model': model}
        except ValueError:
            di = {'app_label': pattern_or_name}

        for ct in ContentType.objects.filter(**di):
            filters['%s.%s' % (ct.app_label, ct.model)] = {'content_type': ct, 
               'form': form, 
               'admin': admin, 
               'admin_site': admin_site}

    if exclude is not None:
        raise NotImplementedError
    SETTINGS = get_settings()
    for di in filters.values():
        ct = di['content_type']
        pth = '%s-%s' % (ct.app_label, ct.model)
        if pth in SETTINGS['blacklist']:
            continue
        form = di.pop('form', None)
        admin = di.pop('admin', None)
        admin_site = di.pop('admin_site', None)
        model = ct.model_class()
        if not hasattr(model, 'objects'):
            continue
        prefix = '%s%s' % (ct.app_label.capitalize(), model.__name__)
        serializer_klass = type(str('%sSerializer' % prefix), (
         HyperlinkedModelSerializer,), {'model': model, 
           'form': form, 
           'admin': admin, 
           'admin_site': admin_site})
        viewset_klass = type(str('%sViewSet' % prefix), (
         viewsets.ModelViewSet,), {'serializer_class': serializer_klass, 
           'queryset': model.objects.all(), 
           'authentication_classes': SETTINGS['authentication-classes'], 
           'permission_classes': SETTINGS['permission-classes']})
        logger.info('DRFE: registering API url %s' % pth)
        router.register(pth, viewset_klass)

    return True


def register(router, mapping=None):
    """Register all viewsets known to app, overriding any items already
    registered with the same name."""
    from rest_framework_extras.users.viewsets import UsersViewSet
    if mapping is None:
        mapping = (('auth-user', UsersViewSet),)
    for pth, klass in mapping:
        keys = [ tu[0] for tu in router.registry ]
        try:
            i = keys.index(pth)
            del router.registry[i]
        except ValueError:
            pass

        router.register('%s' % pth, klass)
        router.register('%s' % pth, klass, base_name=pth)

    return