# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ztfy/security/browser/widget/principal.py
# Compiled at: 2017-01-05 04:30:58
__docformat__ = 'restructuredtext'
from z3c.form.interfaces import IFieldWidget
from zope.schema.interfaces import IField
from ztfy.security.browser.widget.interfaces import IPrincipalWidget, IPrincipalListWidget
from ztfy.skin.layer import IZTFYBrowserLayer
from z3c.form.browser.text import TextWidget
from z3c.form.widget import FieldWidget
from zope.component import adapter
from zope.interface import implementer, implementsOnly
from zope.schema.fieldproperty import FieldProperty
from ztfy.jqueryui import jquery_multiselect
from ztfy.security.search import getPrincipal

class PrincipalWidget(TextWidget):
    """Principal widget"""
    implementsOnly(IPrincipalWidget)
    query_name = 'findPrincipals'
    auth_plugins = ()

    @property
    def principal(self):
        return getPrincipal(self.value)

    @property
    def principal_map(self):
        if not self.value:
            return ''
        else:
            principal = self.principal
            if principal is None:
                return ''
            return "{ '%s': '%s' }" % (principal.id,
             principal.title.replace("'", '&#039;'))

    @property
    def auth_plugins_value(self):
        if self.auth_plugins:
            return ";;{'names':'%s'}" % (',').join(self.auth_plugins)
        return ''

    def render(self):
        jquery_multiselect.need()
        return super(PrincipalWidget, self).render()


@adapter(IField, IZTFYBrowserLayer)
@implementer(IFieldWidget)
def PrincipalFieldWidget(field, request):
    """IPrincipalWidget factory for Principal fields"""
    return FieldWidget(field, PrincipalWidget(request))


class PrincipalListWidget(TextWidget):
    """Principals list widget"""
    implementsOnly(IPrincipalListWidget)
    query_name = 'findPrincipals'
    auth_plugins = ()
    backspace_removes_last = FieldProperty(IPrincipalListWidget['backspace_removes_last'])

    @property
    def principals(self):
        if not hasattr(self, '_v_principals'):
            self._v_principals = sorted((getPrincipal(v) for v in self.value.split(',')), key=lambda x: x.title)
        return self._v_principals

    def get_value(self):
        return (',').join(principal.id for principal in self.principals)

    @property
    def principals_map(self):
        return '{ %s }' % (',\n').join("'%s': '%s'" % (principal.id, principal.title.replace("'", '&#039;')) for principal in self.principals)

    @property
    def auth_plugins_value(self):
        if self.auth_plugins:
            return ";;{'names':'%s'}" % (',').join(self.auth_plugins)
        return ''

    def render(self):
        jquery_multiselect.need()
        return super(PrincipalListWidget, self).render()


@adapter(IField, IZTFYBrowserLayer)
@implementer(IFieldWidget)
def PrincipalListFieldWidget(field, request):
    """IPrincipalListWidget factory for PrincipalList fields"""
    return FieldWidget(field, PrincipalListWidget(request))