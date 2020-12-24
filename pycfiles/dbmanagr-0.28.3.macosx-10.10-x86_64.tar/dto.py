# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/site-packages/dbmanagr/command/navigator/dto.py
# Compiled at: 2015-10-11 07:17:06
from dbmanagr.jsonable import Jsonable, from_json
from dbmanagr import utils

def to_dto(model):
    if type(model) is dict:
        return dict(map(lambda (k, v): (k, to_dto(v)), model.iteritems()))
    if type(model) in (tuple, list, set):
        return map(to_dto, model)
    from dbmanagr.model.baseitem import BaseItem
    if isinstance(model, BaseItem):
        return Item(title=model.title(), subtitle=model.subtitle(), autocomplete=model.autocomplete(), validity=model.validity(), icon=model.icon(), value=model.value(), uid=model.uid(), format_=model.format())
    return model


class Item(Jsonable):

    def __init__(self, title=None, subtitle=None, autocomplete=None, uid=None, icon=None, value=None, validity=None, format_=None):
        self.title_ = title
        self.subtitle_ = subtitle
        self.autocomplete_ = autocomplete
        self.uid_ = uid
        self.icon_ = icon
        self.value_ = value
        self.validity_ = validity
        self.format_ = format_

    def __hash__(self):
        return utils.hash_(utils.freeze(self.__dict__))

    def __eq__(self, o):
        return utils.hash_(self) == utils.hash_(o)

    def autocomplete(self):
        return self.autocomplete_

    def title(self):
        return self.title_

    def subtitle(self):
        return self.subtitle_

    def value(self):
        return self.value_

    def validity(self):
        return self.validity_

    def uid(self):
        if self.uid_ is not None:
            return self.uid_
        else:
            return utils.hash_(self.autocomplete())

    def icon(self):
        if self.icon_ is not None:
            return self.icon_
        else:
            return 'images/icon.png'

    def format(self):
        return self.format_

    @staticmethod
    def from_json(d):
        return Item(title=from_json(d['title']), subtitle=from_json(d['subtitle']), autocomplete=from_json(d['autocomplete']), uid=from_json(d['uid']), icon=from_json(d['icon']), value=from_json(d['value']), validity=from_json(d['validity']), format_=from_json(d['format_']))