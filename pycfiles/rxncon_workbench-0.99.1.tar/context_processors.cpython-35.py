# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/mathias/tbp/django_rxncon_site/src/rxncon_site/context_processors.py
# Compiled at: 2018-06-27 10:02:27
# Size of source mod 2**32: 2444 bytes
try:
    from fileTree.models import File
    from quick_format.models import Quick
except ImportError:
    from src.fileTree.models import File
    from src.quick_format.models import Quick

from django.conf import settings

def file_list(request):
    queryset_list = File.objects.all().order_by('-updated')
    slug_list = []
    for file in queryset_list:
        current_slug = file.get_project_slug()
        if current_slug not in slug_list:
            slug_list.append(current_slug)

    projects = [queryset_list.filter(slug=slug).order_by('-updated') for slug in slug_list]
    return {'object_list': queryset_list, 
     'title': 'Projects', 
     'slug_list': slug_list, 
     'projects': projects, 
     'projects_length': len(projects)}


def quick_list(request):
    quick_definitions = Quick.objects.all().order_by('-updated')
    return {'quick_definitions': quick_definitions, 
     'quick_definitions_length': len(quick_definitions), 
     'title': 'Quick definitions'}


def get_loaded_system(request):
    context = {}
    loaded_system_list = File.objects.filter(loaded=True)
    if len(loaded_system_list) == 0:
        loaded_system_list = Quick.objects.filter(loaded=True)
        if len(loaded_system_list) == 1:
            system_type = 'Quick'
            instance = loaded_system_list[0]
            name = instance.name
            slug = instance.slug
            filename = ''
    else:
        system_type = 'File'
        instance = loaded_system_list[0]
        name = instance.project_name
        filename = instance.get_filename()
        slug = instance.slug
    if len(loaded_system_list) > 1:
        raise LookupError('Corrupted database, multiple systems had loaded flag set to true.')
    if len(loaded_system_list) != 0:
        request.loaded = system_type
        context = {'loaded_system': instance, 
         'loaded_type': system_type, 
         'loaded_project_name': name, 
         'loaded_project_slug': slug}
        if filename:
            context['loaded_file'] = filename
    return context


def admin_media(request):
    return {'MEDIA_ROOT': settings.MEDIA_ROOT}