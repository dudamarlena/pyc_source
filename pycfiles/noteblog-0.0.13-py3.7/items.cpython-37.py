# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/noteblog/fzutils/items.py
# Compiled at: 2019-05-05 05:26:25
# Size of source mod 2**32: 5137 bytes
from scrapy.item import Item
from scrapy import Field
from pprint import pformat
from collections import MutableMapping
import six
from scrapy.utils.trackref import object_ref
__all__ = [
 'DictItem']

class GoodsItem(Item):
    __doc__ = '\n    商品关系对象\n    '
    goods_id = Field()
    create_time = Field()
    modify_time = Field()
    username = Field()
    goods_url = Field()
    shop_name = Field()
    title = Field()
    sub_title = Field()
    link_name = Field()
    account = Field()
    price = Field()
    taobao_price = Field()
    price_info = Field()
    detail_name_list = Field()
    price_info_list = Field()
    all_sell_count = Field()
    all_img_url = Field()
    p_info = Field()
    div_desc = Field()
    is_delete = Field()
    site_id = Field()
    schedule = Field()
    my_shelf_and_down_time = Field()
    miaosha_time = Field()
    miaosha_begin_time = Field()
    miaosha_end_time = Field()
    pintuan_time = Field()
    pintuan_begin_time = Field()
    pintuan_end_time = Field()
    shelf_time = Field()
    delete_time = Field()
    is_price_change = Field()
    price_change_info = Field()
    main_goods_id = Field()
    parent_dir = Field()
    sku_info_trans_time = Field()
    gender = Field()
    page = Field()
    tab_id = Field()
    tab = Field()
    sort = Field()
    stock_info = Field()
    pid = Field()
    event_time = Field()
    fcid = Field()
    spider_time = Field()
    session_id = Field()
    block_id = Field()
    father_sort = Field()
    child_sort = Field()
    is_spec_change = Field()
    spec_trans_time = Field()
    is_stock_change = Field()
    stock_trans_time = Field()
    stock_change_info = Field()


class BaseItem(object_ref):
    __doc__ = 'Base class for all scraped items.'


class DictItem(MutableMapping, BaseItem):
    fields = {}

    def __init__(self, *args, **kwargs):
        self._values = {}
        if args or kwargs:
            for k, v in six.iteritems(dict(*args, **kwargs)):
                self[k] = v

    def __getitem__(self, key):
        return self._values[key]

    def __setitem__(self, key, value):
        if key in self.fields:
            self._values[key] = value
        else:
            raise KeyError('%s does not support field: %s' % (
             self.__class__.__name__, key))

    def __delitem__(self, key):
        del self._values[key]

    def __getattr__(self, name):
        if name in self.fields:
            raise AttributeError('Use item[%r] to get field value' % name)
        raise AttributeError(name)

    def __setattr__(self, name, value):
        if not name.startswith('_'):
            raise AttributeError('Use item[%r] = %r to set field value' % (
             name, value))
        super(DictItem, self).__setattr__(name, value)

    def __len__(self):
        return len(self._values)

    def __iter__(self):
        return iter(self._values)

    __hash__ = BaseItem.__hash__

    def keys(self):
        return self._values.keys()

    def __repr__(self):
        return pformat(dict(self))

    def copy(self):
        return self.__class__(self)