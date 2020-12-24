# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ztfy/i18n/browser/widget/widget.py
# Compiled at: 2014-01-23 03:40:58
from z3c.form.interfaces import IDataConverter
from z3c.language.negotiator.interfaces import INegotiatorManager
from ztfy.i18n.browser.widget.interfaces import II18nWidget
from ztfy.i18n.interfaces import II18nManager, II18nManagerInfo
from z3c.form.widget import Widget
from z3c.form.browser.widget import HTMLFormElement
from zope.component import queryUtility
from zope.interface import implements
from zope.schema.fieldproperty import FieldProperty
from zope.security.proxy import removeSecurityProxy
from ztfy.i18n.browser import ztfy_i18n
from ztfy.utils.traversing import getParent

class I18nWidgetProperty(object):
    """Base class for I18n widgets properties"""

    def __init__(self, name):
        self.__name = name

    def __get__(self, instance, klass):
        return instance.__dict__.get(self.__name, None)

    def __set__(self, instance, value):
        instance.__dict__[self.__name] = value
        for widget in instance.widgets.values():
            setattr(widget, self.__name, value)


class I18nWidget(HTMLFormElement, Widget):
    """Base class for all I18n widgets"""
    implements(II18nWidget)
    langs = FieldProperty(II18nWidget['langs'])
    original_widget = None
    klass = 'i18n-widget'
    style = I18nWidgetProperty('style')
    onclick = I18nWidgetProperty('onclick')
    ondblclick = I18nWidgetProperty('ondblclick')
    onmousedown = I18nWidgetProperty('onmousedown')
    onmouseup = I18nWidgetProperty('onmouseup')
    onmouseover = I18nWidgetProperty('onmouseover')
    onmousemove = I18nWidgetProperty('onmousemove')
    onmouseout = I18nWidgetProperty('onmouseout')
    onkeypress = I18nWidgetProperty('onkeypress')
    onkeydown = I18nWidgetProperty('onkeydown')
    onkeyup = I18nWidgetProperty('onkeyup')
    disabled = I18nWidgetProperty('disabled')
    tabindex = I18nWidgetProperty('tabindex')
    onfocus = I18nWidgetProperty('onfocus')
    onblur = I18nWidgetProperty('onblur')
    onchange = I18nWidgetProperty('onchange')

    def update(self):
        super(I18nWidget, self).update()
        manager = getParent(self.context, II18nManager)
        if manager is not None:
            self.langs = II18nManagerInfo(manager).availableLanguages
        else:
            manager = queryUtility(INegotiatorManager)
            if manager is not None:
                self.langs = manager.offeredLanguages
            else:
                self.langs = [
                 'en']
            self.widgets = {}
            for lang in self.langs:
                widget = self.widgets[lang] = self.original_widget(self.request)
                self.initWidget(widget, lang)

            for lang in self.langs:
                widget = self.widgets[lang]
                self.updateWidget(widget, lang)
                widget.update()

        return

    def initWidget(self, widget, language):
        widget.id = str('%s.%s' % (self.name, language))
        widget.form = self.form
        widget.mode = self.mode
        widget.ignoreContext = self.ignoreContext
        widget.ignoreRequest = self.ignoreRequest
        widget.field = self.field.value_type
        widget.name = str('%s:list' % self.name)
        widget.label = self.label
        widget.lang = language

    def updateWidget(self, widget, language):
        widget.value = self.getValue(language)

    def getWidget(self, language):
        widget = self.widgets[language]
        return widget.render()

    def getValue(self, language):
        self.value = removeSecurityProxy(self.value)
        if not isinstance(self.value, dict):
            converter = IDataConverter(self)
            try:
                self.value = converter.toFieldValue(self.value)
            except:
                self.value = {}

        return self.value.get(language)

    def hasValue(self, language):
        return bool(self.getValue(language))

    def render(self):
        ztfy_i18n.need()
        return super(I18nWidget, self).render()