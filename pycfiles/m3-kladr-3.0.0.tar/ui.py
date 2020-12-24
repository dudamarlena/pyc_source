# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/pirogov/.virtualenvs/paid/local/lib/python2.7/site-packages/kladr/ui.py
# Compiled at: 2014-05-26 05:22:26
from m3_ext.gears.edit_windows import GearEditWindow
from m3_ext.ui.fields.simple import ExtHiddenField, ExtStringField

class DictSimpleEditWindow(GearEditWindow):
    """ Базовое окно для всех справочников """

    def __init__(self, create_new=True, *args, **kwargs):
        super(DictSimpleEditWindow, self).__init__(*args, **kwargs)
        self.frozen_size(430, 123)
        self.modal = True
        self.create_new = create_new
        self.field_hidden = ExtHiddenField(name='id')
        self.field_code = ExtStringField(width=10, label='Код', name='code', anchor='60%', allow_blank=True)
        self.field_name = ExtStringField(width=200, label='Наименование', name='name', anchor='100%', allow_blank=False)
        self.form.items.extend([
         self.field_hidden,
         self.field_code,
         self.field_name])

    def configure_for_dictpack(self, **k):
        if self.create_new:
            self.title = 'Создание новой записи: ' + k['pack'].title
        else:
            self.title = 'Редактирование записи: ' + k['pack'].title


class KLADRGeoEditWindow(DictSimpleEditWindow):

    def __init__(self, *args, **kwargs):
        super(KLADRGeoEditWindow, self).__init__(*args, **kwargs)
        self.frozen_size(430, 280)
        self.field_name.label = 'Улица'
        self.field_code.width = 300
        self.form.items.extend([
         ExtStringField(width=300, label='Сокращение', name='socr'),
         ExtStringField(width=300, label='Индекс', name='zipcode'),
         ExtStringField(width=300, label='Код ИФНС', name='gni'),
         ExtStringField(width=300, label='Код тер.уч. ИФНС', name='uno'),
         ExtStringField(width=300, label='Код ОКАТО', name='okato')])
        self.form.items.append(ExtHiddenField(name='parent_id'))


class KLADRStreetEditWindow(DictSimpleEditWindow):

    def __init__(self, *args, **kwargs):
        super(KLADRStreetEditWindow, self).__init__(*args, **kwargs)
        self.frozen_size(430, 320)
        self.field_name.label = 'Геогр.пункт'
        self.field_code.width = 300
        self.form.items.extend([
         ExtStringField(width=300, label='Сокращение', name='socr'),
         ExtStringField(width=300, label='Индекс', name='zipcode'),
         ExtStringField(width=300, label='Код ИФНС', name='gni'),
         ExtStringField(width=300, label='Код тер.уч. ИФНС', name='uno'),
         ExtStringField(width=300, label='Код ОКАТО', name='okato'),
         ExtStringField(width=300, label='Статус', name='status')])
        self.form.items.append(ExtHiddenField(name='parent_id'))