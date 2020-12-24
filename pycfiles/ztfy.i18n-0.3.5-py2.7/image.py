# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ztfy/i18n/browser/widget/image.py
# Compiled at: 2013-03-04 04:51:20
from z3c.form.interfaces import IFieldWidget, NOT_CHANGED
from ztfy.file.interfaces import IThumbnailGeometry, IImageDisplay, ICthumbImageFieldData
from ztfy.i18n.browser.widget.interfaces import II18nImageWidget, II18nCthumbImageWidget
from ztfy.i18n.interfaces import II18nImageField, II18nCthumbImageField
from ztfy.skin.layer import IZTFYBrowserLayer
from z3c.form.widget import FieldWidget
from zope.component import adapter
from zope.interface import implementer, implementsOnly
from ztfy.i18n.browser.widget.file import I18nFileWidget
from ztfy.file.browser import ztfy_file
from ztfy.file.browser.widget import ImageWidget, CthumbImageWidget

class I18nImageWidget(I18nFileWidget):
    """I18n image input type implementation"""
    implementsOnly(II18nImageWidget)
    original_widget = ImageWidget


class I18nCthumbImageWidget(I18nImageWidget):
    """I18n image input with square thumbnails implementation"""
    implementsOnly(II18nCthumbImageWidget)
    original_widget = CthumbImageWidget

    def update(self):
        super(I18nCthumbImageWidget, self).update()
        self.widget_value = self.field.get(self.context)

    def render(self):
        ztfy_file.need()
        return super(I18nCthumbImageWidget, self).render()

    def getAdapter(self, lang):
        return IImageDisplay(self.widget_value.get(lang), None)

    def getGeometry(self, lang):
        return IThumbnailGeometry(self.widget_value.get(lang), None)

    def getPosition(self, lang):
        name, _ignore = self.name.split(':')
        return (int(self.request.form.get(name + '_' + lang + '__x', 0)),
         int(self.request.form.get(name + '_' + lang + '__y', 0)))

    def getSize(self, lang):
        name, _ignore = self.name.split(':')
        return (int(self.request.form.get(name + '_' + lang + '__w', 0)),
         int(self.request.form.get(name + '_' + lang + '__h', 0)))

    def hasValue(self, language):
        value = self.getValue(language)
        if ICthumbImageFieldData.providedBy(value):
            value = value.value
        if value is NOT_CHANGED:
            return bool(self.current_value.get(language))
        else:
            return bool(value)


@adapter(II18nImageField, IZTFYBrowserLayer)
@implementer(IFieldWidget)
def I18nImageFieldWidget(field, request):
    """IFieldWidget factory for I18nImageWidget"""
    return FieldWidget(field, I18nImageWidget(request))


@adapter(II18nCthumbImageField, IZTFYBrowserLayer)
@implementer(IFieldWidget)
def I18nCthumbImageFieldWidget(field, request):
    """IFieldWidget factory for I18nCthumbImageWidget"""
    return FieldWidget(field, I18nCthumbImageWidget(request))