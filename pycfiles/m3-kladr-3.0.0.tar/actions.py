# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/pirogov/.virtualenvs/paid/local/lib/python2.7/site-packages/kladr/actions.py
# Compiled at: 2014-05-26 05:22:26
from django.db.models.query_utils import Q
from django.conf import settings
from m3 import M3JSONEncoder
from m3.actions import Action, PreJsonResult, OperationResult, ActionPack, ActionController
from models import KladrGeo, KladrStreet
from ui import KLADRGeoEditWindow, KLADRStreetEditWindow
kladr_controller = ActionController(url='/m3-kladr')
if hasattr(settings, 'ROOT_URL'):
    kladr_controller.url = settings.ROOT_URL + kladr_controller.url

class BaseTreeDictionaryModelActions(ActionPack):
    pass


class Kladr_DictPack(BaseTreeDictionaryModelActions):
    """
    Пак для экшенов справочника КЛАДР
    """
    url = '/kladr'
    need_check_permission = True
    title = 'Классификатор адресов России (КЛАДР)'
    verbose_name = 'Классификатор адресов России (КЛАДР)'
    tree_model = KladrGeo
    list_model = KladrStreet
    list_columns = [
     ('socr', 'Сокращение', 20),
     ('name', 'Улица')]
    tree_columns = [('name', 'Геогр. пункт', 240),
     ('socr', 'Сокращение', 90),
     ('zipcode', 'Индекс', 60)]
    filter_fields = [
     'code', 'name']
    tree_filter_fields = ['name', 'zipcode']
    width, height = (910, 600)
    tree_width = 390
    edit_window = KLADRGeoEditWindow
    edit_node_window = KLADRStreetEditWindow


class KLADRPack(ActionPack):
    url = ''

    def __init__(self):
        super(KLADRPack, self).__init__()
        self.get_places_action = KLADRRowsAction()
        self.get_streets_action = StreetRowsAction()
        self.get_addr_action = KLADRGetAddrAction()
        self.actions = [self.get_places_action, self.get_streets_action, self.get_addr_action]

    @classmethod
    def get_place_name(self, code):
        place = KladrGeo.objects.select_related('parent').select_related('parent__parent').select_related('parent__parent__parent').filter(code=code)
        if place:
            return place[0].display_name()
        return ''

    @classmethod
    def get_place(self, code):
        place = KladrGeo.objects.select_related('parent').select_related('parent__parent').select_related('parent__parent__parent').filter(code=code)
        if place:
            return M3JSONEncoder().encode(place[0])
        else:
            return

    @classmethod
    def get_street_name(self, code):
        street = KladrStreet.objects.select_related('parent').filter(code=code)
        if street:
            return street[0].display_name()
        return ''

    @classmethod
    def get_street(self, code):
        street = KladrStreet.objects.select_related('parent').filter(code=code)
        if street:
            return M3JSONEncoder().encode(street[0])
        else:
            return


class KLADRRowsAction(Action):
    """
    Перечисление элементов КЛАДРа
    """
    url = '/kladr_rows$'

    def run(self, request, context):
        filter = request.REQUEST.get('filter')
        if filter:
            fields = [
             'name', 'code', 'socr']
            words = filter.strip().split(' ')
            condition = None
            for word in words:
                field_condition = None
                for field_name in fields:
                    field = Q(**{field_name + '__icontains': word})
                    field_condition = field_condition | field if field_condition else field

                condition = condition & field_condition if condition else field_condition

            places = KladrGeo.objects.filter(condition).select_related('parent').select_related('parent__parent').select_related('parent__parent__parent').order_by('level', 'name')[0:50]
            if len(places) == 0:
                condition = None
                for word in words:
                    field_condition = None
                    for field_name in fields:
                        field = Q(**{field_name + '__icontains': word}) | Q(**{'parent__' + field_name + '__icontains': word}) | Q(**{'parent__parent__' + field_name + '__icontains': word}) | Q(**{'parent__parent__parent__' + field_name + '__icontains': word})
                        field_condition = field_condition | field if field_condition else field

                    condition = condition & field_condition if condition else field_condition

                places = KladrGeo.objects.filter(condition).select_related('parent').select_related('parent__parent').select_related('parent__parent__parent').order_by('level', 'name')[0:50]
        else:
            places = []
        result = {'rows': list(places), 'total': len(places)}
        return PreJsonResult(result)


class StreetRowsAction(Action):
    """
    Перечисление улиц
    """
    url = '/street_rows$'
    MAX_DEPTH = 3

    def run(self, request, context):
        filt = request.REQUEST.get('filter')
        if filt:
            place_code = request.REQUEST.get('place_code')
            place_filter = Q()
            if place_code:
                try:
                    place_id = KladrGeo.objects.get(code=place_code)
                except (KladrGeo.DoesNotExist,
                 KladrGeo.MultipleObjectsReturned):
                    pass

                for depth in range(self.MAX_DEPTH):
                    place_filter |= Q(**{'%sparent' % ('parent__' * depth): place_id})

            fields = ['name', 'code', 'socr']
            words = filt.strip().split()

            def query_streets(condition):
                return KladrStreet.objects.filter(condition, place_filter).select_related('parent').order_by('name')[0:50]

            condition = Q()
            for word in words:
                field_condition = Q()
                for field_name in fields:
                    field_condition |= Q(**{field_name + '__icontains': word})

                condition &= field_condition

            places = query_streets(condition)
            if not places.exists():
                condition = Q()
                for word in words:
                    field_condition = Q()
                    for field_name in fields:
                        for depth in range(self.MAX_DEPTH + 1):
                            field_condition |= Q(**{'%s%s__icontains' % ('parent__' * depth, field_name): word})

                    condition &= field_condition

                places = query_streets(condition)
        else:
            places = []
        result = {'rows': list(places), 'total': len(places)}
        return PreJsonResult(result)


def GetAddr(place, street=None, house=None, flat=None, zipcode=None, corps=None):
    u"""
    Формирует строку полного адреса по выбранным значениям КЛАДРа
    """
    if not place:
        return ''
    else:
        if isinstance(place, (str, unicode)):
            qs = KladrGeo.objects.filter(code=place)
            if qs.count() > 0:
                place = qs.get()
            else:
                return ''
        else:
            if not isinstance(place, KladrGeo):
                raise TypeError()
            if isinstance(street, (str, unicode)):
                qs = KladrStreet.objects.filter(code=street)
                if qs.count() > 0:
                    street = qs.get()
                else:
                    street = None
            else:
                if street != None and not isinstance(street, KladrStreet):
                    raise TypeError()
                addr_type = 0
                curr_index = zipcode or ''
                addr_text = ''
                curr_level = 5
                if street:
                    curr_item = street
                else:
                    curr_item = place
                if addr_type == 0:
                    delim = ', '
                else:
                    delim = ','
                while curr_item:
                    if addr_type != 0 and curr_item.parent == None:
                        break
                    if curr_index == '' and curr_item.zipcode:
                        curr_index = curr_item.zipcode
                    if addr_type == 0:
                        addr_text = curr_item.socr + ' ' + curr_item.name + delim + addr_text
                    else:
                        if curr_item == street:
                            lv = 4
                        else:
                            lv = curr_item.level
                        while curr_level > lv:
                            curr_level -= 1
                            addr_text = delim + addr_text

                        addr_text = curr_item.socr + ' ' + curr_item.namebind_pack + delim + addr_text
                        curr_level -= 1
                    curr_item = curr_item.parent

            if addr_type == 0:
                if curr_index != '':
                    addr_text = curr_index + delim + addr_text
            else:
                while curr_level > 1:
                    curr_level -= 1
                    addr_text = delim + addr_text

            addr_text = 'регион' + delim + addr_text
            if curr_index != '':
                addr_text = curr_index + delim + addr_text
            else:
                addr_text = delim + delim + addr_text
        if not (house or corps or flat):
            addr_text = addr_text.rstrip(delim)
        else:
            if house:
                addr_text = addr_text + 'д. ' + house
            if corps:
                addr_text = '%s%sкорп. %s' % (addr_text, delim, corps)
            if flat:
                addr_text = addr_text + delim + 'кв. ' + flat
        return addr_text


class KLADRGetAddrAction(Action):
    """
    Расчет адреса по составляющим
    """
    url = '/kladr_getaddr$'

    def run(self, request, context):
        place = request.REQUEST.get('place')
        street = request.REQUEST.get('street')
        house = request.REQUEST.get('house')
        flat = request.REQUEST.get('flat')
        zipcode = request.REQUEST.get('zipcode')
        addr_cmp = request.REQUEST.get('addr_cmp', '')
        addr_text = GetAddr(place, street, house, flat, zipcode)
        result = '(function(){ Ext.getCmp("%s").setValue("%s");})()' % (addr_cmp, addr_text or '')
        return OperationResult(success=True, code=result)