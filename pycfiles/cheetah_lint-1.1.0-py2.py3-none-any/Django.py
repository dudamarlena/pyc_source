# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/lib.macosx-10.13-x86_64-2.7/Cheetah/Django.py
# Compiled at: 2019-09-22 10:12:27
import Cheetah.Template

def render(template_file, **kwargs):
    """
        Cheetah.Django.render() takes the template filename
        (the filename should be a file in your Django
        TEMPLATE_DIRS)

        Any additional keyword arguments are passed into the
        template are propogated into the template's searchList
    """
    import django.http, django.template.loader
    source, loader = django.template.loader.find_template_source(template_file)
    t = Cheetah.Template.Template(source, searchList=[kwargs])
    return django.http.HttpResponse(t.__str__())