# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/pirogov/.virtualenvs/paid/local/lib/python2.7/site-packages/kladr/addrfield.py
# Compiled at: 2014-05-23 05:50:14
from m3_ext.ui.containers.base import BaseExtContainer
from m3_ext.ui.fields.simple import ExtHiddenField

class ExtAddrComponent(BaseExtContainer):
    """
    Блок указания адреса
    """
    PLACE = 1
    STREET = 2
    HOUSE = 3
    FLAT = 4
    VIEW_0 = 0
    VIEW_1 = 1
    VIEW_2 = 2
    VIEW_3 = 3
    INVALID_CLASS = 'm3-form-invalid'
    INVALID_COMPOSITE_FIELD_CLASS = 'm3-composite-field-invalid'
    _xtype = 'm3-kladr'
    js_attrs = BaseExtContainer.js_attrs.extend('layout', 'height', invalid_class='params.invalid_class', read_only='params.read_only', place_label='params.place_label', street_label='params.street_label', house_label='params.house_label', corps_label='params.corps_label', flat_label='params.flat_label', addr_label='params.addr_label', place_field_name='params.place_field_name', street_field_name='params.street_field_name', house_field_name='params.house_field_name', corps_field_name='params.corps_field_name', flat_field_name='params.flat_field_name', zipcode_field_name='params.zipcode_field_name', addr_field_name='params.addr_field_name', place_allow_blank='params.place_allow_blank', street_allow_blank='params.street_allow_blank', house_allow_blank='params.house_allow_blank', corps_allow_blank='params.corps_allow_blank', flat_allow_blank='params.flat_allow_blank')
    deprecated_attrs = BaseExtContainer.deprecated_attrs + ('place_field_name', 'street_field_name',
                                                            'house_field_name', 'corps_field_name',
                                                            'flat_field_name', 'zipcode_field_name',
                                                            'addr_field_name', 'handler_change_place',
                                                            'handler_change_street',
                                                            'handler_change_house',
                                                            'handler_change_flat',
                                                            'handler_change_corps',
                                                            'handler_before_query')

    def __init__(self, *args, **kwargs):
        super(ExtAddrComponent, self).__init__(*args, **kwargs)
        self.setdefault('place_field_name', 'place')
        self.setdefault('street_field_name', 'street')
        self.setdefault('house_field_name', 'house')
        self.setdefault('corps_field_name', 'corps')
        self.setdefault('flat_field_name', 'flat')
        self.setdefault('zipcode_field_name', 'zipcode')
        self.setdefault('addr_field_name', 'addr')
        self.setdefault('place_label', 'Населенный пункт')
        self.setdefault('street_label', 'Улица')
        self.setdefault('house_label', 'Дом')
        self.setdefault('corps_label', 'Корпус')
        self.setdefault('flat_label', 'Квартира')
        self.setdefault('addr_label', 'Адрес')
        self.setdefault('place_allow_blank', True)
        self.setdefault('street_allow_blank', True)
        self.setdefault('house_allow_blank', True)
        self.setdefault('corps_allow_blank', True)
        self.setdefault('flat_allow_blank', True)
        self.setdefault('invalid_class', ExtAddrComponent.INVALID_CLASS)
        self.setdefault('invalid_composite_field_class', ExtAddrComponent.INVALID_COMPOSITE_FIELD_CLASS)
        self.setdefault('addr_visible', True)
        self.setdefault('read_only', False)
        self.setdefault('level', ExtAddrComponent.FLAT)
        self.setdefault('view_mode', ExtAddrComponent.VIEW_2)
        self.setdefault('use_corps', False)
        self.layout = 'form'
        self.addr = ExtHiddenField(name=self.addr_field_name)
        self.place = ExtHiddenField(name=self.place_field_name)
        self.street = ExtHiddenField(name=self.street_field_name)
        self.house = ExtHiddenField(name=self.house_field_name)
        self.corps = ExtHiddenField(name=self.corps_field_name)
        self.flat = ExtHiddenField(name=self.flat_field_name)
        self.zipcode = ExtHiddenField(name=self.zipcode_field_name)
        self.items.append(self.addr)
        self.items.append(self.place)
        self.items.append(self.street)
        self.items.append(self.house)
        self.items.append(self.corps)
        self.items.append(self.flat)
        self.items.append(self.zipcode)