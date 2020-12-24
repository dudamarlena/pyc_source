# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
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