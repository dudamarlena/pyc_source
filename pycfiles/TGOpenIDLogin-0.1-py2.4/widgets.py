# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/tgopenidlogin/widgets.py
# Compiled at: 2007-03-26 04:19:18
import pkg_resources
from turbogears.widgets import CSSLink, JSLink, Widget, WidgetDescription, register_static_directory
from turbogears import widgets
resource_dir = pkg_resources.resource_filename('tgopenidlogin', 'static')
register_static_directory('tgopenidlogin', resource_dir)
openidcss = CSSLink('tgopenidlogin', 'css/openid.css', media='screen')
import cherrypy

class OpenIDText(widgets.TextField):
    __module__ = __name__
    label = 'OpenID'
    name = 'identity_url'
    field_class = 'openid_login'
    attrs = {'size': 10, 'class': 'openid_login'}
    css = [openidcss]


class OpenIDLoginForm(widgets.Form):
    __module__ = __name__
    template = '\n    <form xmlns:py="http://purl.org/kid/ns#"\n        name="${name}"\n        action="${action}"\n        method="${method}"\n        class="tableform"\n        py:attrs="form_attrs"\n    >\n        <div py:for="field in hidden_fields" \n            py:replace="field.display(value_for(field), **params_for(field))" \n        />\n        <table border="0" cellspacing="0" cellpadding="2">\n            <tr py:for="i, field in enumerate(fields)" \n                class="${i%2 and \'odd\' or \'even\'}"\n            >\n                <th>\n                    <label class="fieldlabel" for="${field.field_id}" py:content="field.label" />\n                </th>\n                <td>\n                    <span py:replace="field.display(value_for(field), **params_for(field))" />\n                    <span py:if="error_for(field)" class="fielderror" py:content="error_for(field)" />\n                    <span py:if="field.help_text" class="fieldhelp" py:content="field.help_text" />\n                </td>\n            </tr>\n            <tr>\n                <td>&#160;</td>\n                <td py:content="submit.display(submit_text)" />\n            </tr>\n        </table>\n    </form>\n    '
    params = [
     'openidrequest']
    params_doc = {'openidrequest': 'An OpenID request object to carry through'}
    openidrequest = None
    submit_text = 'Log in'
    action = '/openid/loginBegin'

    def update_params(self, d):
        super(OpenIDLoginForm, self).update_params(d)
        hidden_fields = d.setdefault('hidden_fields', [])
        forward_url = widgets.HiddenField(name='forward_url', default=cherrypy.request.path)
        forward_url.hidden = True
        hidden_fields.append(forward_url)

    fields = [
     OpenIDText(name='identity_url')]