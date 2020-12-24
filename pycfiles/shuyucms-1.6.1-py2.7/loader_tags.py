# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/shuyucms/template/loader_tags.py
# Compiled at: 2016-05-20 23:26:47
from __future__ import unicode_literals
import os
from django.template import Template, TemplateSyntaxError, TemplateDoesNotExist
from django.template.loader import find_template_loader
from django.template.loader_tags import ExtendsNode
from future.builtins import map
from shuyucms import template
register = template.Library()

class OverExtendsNode(ExtendsNode):
    """
    Allows the template ``foo/bar.html`` to extend ``foo/bar.html``,
    given that there is another version of it that can be loaded. This
    allows templates to be created in a project that extend their app
    template counterparts, or even app templates that extend other app
    templates with the same relative name/path.

    We use our own version of ``find_template``, that uses an explict
    list of template directories to search for the template, based on
    the directories that the known template loaders
    (``app_directories`` and ``filesystem``) use. This list gets stored
    in the template context, and each time a template is found, its
    absolute path gets removed from the list, so that subsequent
    searches for the same relative name/path can find parent templates
    in other directories, which allows circular inheritance to occur.

    Django's ``app_directories``, ``filesystem``, and ``cached``
    loaders are supported. The ``eggs`` loader, and any loader that
    implements ``load_template_source`` with a source string returned,
    should also theoretically work.
    """

    def find_template(self, name, context, peeking=False):
        """
        Replacement for Django's ``find_template`` that uses the current
        template context to keep track of which template directories it
        has used when finding a template. This allows multiple templates
        with the same relative name/path to be discovered, so that
        circular template inheritance can occur.
        """
        from django.template.loaders.app_directories import app_template_dirs
        from shuyucms.conf import settings
        context_name = b'OVEREXTENDS_DIRS'
        if context_name not in context:
            context[context_name] = {}
        if name not in context[context_name]:
            all_dirs = list(settings.TEMPLATE_DIRS) + list(app_template_dirs)
            context[context_name][name] = list(map(os.path.abspath, all_dirs))
        loaders = []
        for loader_name in settings.TEMPLATE_LOADERS:
            loader = find_template_loader(loader_name)
            loaders.extend(getattr(loader, b'loaders', [loader]))

        for loader in loaders:
            dirs = context[context_name][name]
            try:
                source, path = loader.load_template_source(name, dirs)
            except TemplateDoesNotExist:
                pass
            else:
                if not peeking:
                    remove_path = os.path.abspath(path[:-len(name) - 1])
                    context[context_name][name].remove(remove_path)
                return Template(source)

        raise TemplateDoesNotExist(name)

    def get_parent(self, context):
        """
        Load the parent template using our own ``find_template``, which
        will cause its absolute path to not be used again. Then peek at
        the first node, and if its parent arg is the same as the
        current parent arg, we know circular inheritance is going to
        occur, in which case we try and find the template again, with
        the absolute directory removed from the search list.
        """
        parent = self.parent_name.resolve(context)
        if hasattr(parent, b'render'):
            return parent
        template = self.find_template(parent, context)
        for node in template.nodelist:
            if isinstance(node, ExtendsNode) and node.parent_name.resolve(context) == parent:
                return self.find_template(parent, context, peeking=True)

        return template


@register.tag
def overextends(parser, token):
    """
    Extended version of Django's ``extends`` tag that allows circular
    inheritance to occur, eg a template can both be overridden and
    extended at once.
    """
    bits = token.split_contents()
    if len(bits) != 2:
        raise TemplateSyntaxError(b"'%s' takes one argument" % bits[0])
    parent_name = parser.compile_filter(bits[1])
    nodelist = parser.parse()
    if nodelist.get_nodes_by_type(ExtendsNode):
        raise TemplateSyntaxError(b"'%s' cannot appear more than once in the same template" % bits[0])
    return OverExtendsNode(nodelist, parent_name, None)