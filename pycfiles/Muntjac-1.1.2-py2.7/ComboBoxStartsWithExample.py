# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/muntjac/demo/sampler/features/selects/ComboBoxStartsWithExample.py
# Compiled at: 2013-04-04 15:36:38
from muntjac.demo.sampler.ExampleUtil import ExampleUtil
from muntjac.api import VerticalLayout, ComboBox
from muntjac.data.property import IValueChangeListener
from muntjac.ui.abstract_select import AbstractSelect, IFiltering

class ComboBoxStartsWithExample(VerticalLayout, IValueChangeListener):

    def __init__(self):
        super(ComboBoxStartsWithExample, self).__init__()
        self.setSpacing(True)
        l = ComboBox('Please select your country', ExampleUtil.getISO3166Container())
        l.setItemCaptionPropertyId(ExampleUtil.iso3166_PROPERTY_NAME)
        l.setItemCaptionMode(AbstractSelect.ITEM_CAPTION_MODE_PROPERTY)
        l.setItemIconPropertyId(ExampleUtil.iso3166_PROPERTY_FLAG)
        l.setWidth(350, self.UNITS_PIXELS)
        l.setFilteringMode(IFiltering.FILTERINGMODE_STARTSWITH)
        l.setImmediate(True)
        l.addListener(self, IValueChangeListener)
        l.setNullSelectionAllowed(False)
        self.addComponent(l)

    def valueChange(self, event):
        selected = ExampleUtil.getISO3166Container().getContainerProperty(str(event.getProperty()), 'name')
        self.getWindow().showNotification('Selected country: ' + str(selected))