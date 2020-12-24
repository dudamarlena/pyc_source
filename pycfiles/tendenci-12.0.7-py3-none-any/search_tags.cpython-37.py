# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/jennyq/.pyenv/versions/venv_t12/lib/python3.7/site-packages/tendenci/apps/search/templatetags/search_tags.py
# Compiled at: 2020-02-26 14:48:40
# Size of source mod 2**32: 3357 bytes
from django.template import TemplateSyntaxError, TemplateDoesNotExist, Variable
from django.template import Library
from django.template.loader_tags import IncludeNode
import django.utils.translation as _
from haystack.models import SearchResult
register = Library()

class SearchResultNode(IncludeNode):

    def __init__(self, result):
        self.result = Variable(result)

    def render(self, context):
        """
        This does not take into account preview themes.
        """
        try:
            result = self.result.resolve(context)
            if isinstance(result, SearchResult):
                result_object = result.object
            else:
                result_object = result
            return result_object and result_object._meta or ''
            var_name = result_object._meta.verbose_name.replace(' ', '_').lower()
            class_name = result_object.__class__.__name__.lower()
            if class_name == 'corporatemembership':
                var_name = 'corporate_membership'
            elif class_name == 'membership':
                var_name = 'membership'
            else:
                if var_name == 'user':
                    var_name = 'profile'
                if var_name == 'member':
                    var_name = 'membership'
                if var_name == 'corporate_member':
                    var_name = 'corporate_membership'
                if var_name == 'photo':
                    var_name = 'photo_set'
                if var_name == 'photo_album':
                    var_name = 'photo_set'
                    template_name = 'photos/photo-set/search-result.html'
                else:
                    if var_name == 'application_entry':
                        var_name = 'entry'
                        template_name = 'memberships/entries/search-result.html'
                    else:
                        template_name = '%s/search-result.html' % result_object._meta.app_label
            if result.__class__.__name__.lower() == 'contribution':
                var_name = 'contribution'
                template_name = 'contributions/search-result.html'
                result_object = result
            try:
                t = context.template.engine.get_template(template_name)
            except (TemplateDoesNotExist, IOError):
                t = context.template.engine.get_template('search/search-result.html')

            context.update({'result': result, 
             var_name: result_object})
            return t.render(context=context)
        except:
            return ''


def search_result(parser, token):
    """
    Loads the search-result.html and renders it with the current context
    and the given app name.
    {% search_result app %}
    """
    bits = token.split_contents()
    if len(bits) != 2:
        raise TemplateSyntaxError(_('%(bit)r tag takes one argument: the search result object' % {'bit': bits[0]}))
    return SearchResultNode(bits[1])


register.tag('search_result', search_result)