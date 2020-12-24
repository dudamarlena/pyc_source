# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ztfy/blog/browser/widget.py
# Compiled at: 2012-06-26 16:33:07
__docformat__ = 'restructuredtext'
from z3c.form.interfaces import IFieldWidget, ITextWidget
from z3c.language.switch.interfaces import II18n
from zope.intid.interfaces import IIntIds
from zope.schema.interfaces import IField
from ztfy.skin.layer import IZTFYBrowserLayer
from z3c.form.browser.text import TextWidget
from z3c.form.widget import FieldWidget
from zope.component import adapter, getUtility
from zope.i18n import translate
from zope.interface import implementer, implementsOnly
from zope.schema import TextLine
from ztfy.jqueryui import jquery_multiselect
from ztfy.blog import _

class IInternalReferenceWidget(ITextWidget):
    """Interface reference widget interface"""
    target_title = TextLine(title=_('Target title'), readonly=True)


class InternalReferenceWidget(TextWidget):
    """Internal reference selection widget"""
    implementsOnly(IInternalReferenceWidget)

    def render(self):
        jquery_multiselect.need()
        return super(InternalReferenceWidget, self).render()

    @property
    def target_title(self):
        if not self.value:
            return ''
        else:
            value = self.request.locale.numbers.getFormatter('decimal').parse(self.value)
            intids = getUtility(IIntIds)
            target = intids.queryObject(value)
            if target is not None:
                title = II18n(target).queryAttribute('title', request=self.request)
                return translate(_('%s (OID: %d)'), context=self.request) % (title, value)
            return translate(_('< missing target >'), context=self.request)
            return


@adapter(IField, IZTFYBrowserLayer)
@implementer(IFieldWidget)
def InternalReferenceFieldWidget(field, request):
    """IFieldWidget factory for InternalReferenceWidget"""
    return FieldWidget(field, InternalReferenceWidget(request))