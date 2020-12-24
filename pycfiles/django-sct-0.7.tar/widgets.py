# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/herbert/dev/python/sctdev/simpleproject/simpleproject/../../communitytools/sphenecoll/sphene/community/widgets.py
# Compiled at: 2012-03-17 12:42:14
from django import forms
from django.conf import settings
from django.template.defaultfilters import filesizeformat
from django.utils.translation import ugettext as _
from django.utils.safestring import mark_safe
from sphene.community.templatetags.sph_extras import sph_basename
from sphene.community.sphutils import sph_reverse
from sphene.community.models import TagLabel

class TagWidget(forms.TextInput):

    def __init__(self, content_type_id=None, *args, **kwargs):
        super(TagWidget, self).__init__(*args, **kwargs)
        self.content_type_id = content_type_id

    def render(self, name, value, attrs=None):
        if not attrs:
            attrs = {}
        if isinstance(value, list):
            value = (', ').join([ tag_label.label for tag_label in value ])
        js = ''
        if self.content_type_id is not None:
            attrs['onfocus'] = '%s_init(this);' % name
            attrs['autocomplete'] = 'off'
            js = '\n<link rel="stylesheet" href="%(media_url)ssphene/community/jqac.css" />\n<script language="JavaScript">\n<!--\n  function %(name)s_get_autocomplete(string, callback) {\n    $.get("%(url)s", { content_type_id: "%(content_type_id)d", string: encodeURIComponent(string) },\n        function(data) {\n          var r=[];\n          $(data).find(\'taglabel\').each(function(){\n            r.push( { id: $(this).find(\'id\').text(),\n                      value: $(this).find(\'label\').text() } );\n          });\n          callback( r );\n        });\n  }\n  function %(name)s_init(input) {\n    //alert( "content_type_id: %(content_type_id)d" );\n    $(input).autocomplete({ ajax_get:%(name)s_get_autocomplete, minchars:1, multi:true });\n  }\n//-->\n</script>' % {'name': name, 'media_url': settings.STATIC_URL, 
               'content_type_id': self.content_type_id, 
               'url': sph_reverse('sph_tags_json_autocompletion', (), {})}
        widget = super(TagWidget, self).render(name, value, attrs)
        return '%s%s' % (js, widget)


class SPHFileWidget(forms.FileInput):
    """
    A FileField Widget that shows its current value if it has one.
    Based on AdminFileWidget
    """

    def __init__(self, attrs={}):
        super(SPHFileWidget, self).__init__(attrs)

    def render(self, name, value, attrs=None):
        output = []
        if value and hasattr(value, 'url'):
            output.append('<div class="current-sphfile">%s <a target="_blank" href="%s">%s</a> (%s)</div> %s ' % (
             _('Currently:'), value.url, sph_basename(value.url), filesizeformat(value.size), _('Change:')))
        output.append(super(SPHFileWidget, self).render(name, value, attrs))
        return mark_safe(('').join(output))