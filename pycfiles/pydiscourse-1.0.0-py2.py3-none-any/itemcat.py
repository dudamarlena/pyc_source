# uncompyle6 version 3.6.7
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build\bdist.win32\egg\disc\crawler\itemcat.py
# Compiled at: 2009-04-28 19:37:09
__doc__ = '\nCreated on 2009-4-19\n\n@author: mingqi\n'
from datetime import datetime
from disc import sip
from disc.sip.sipproxy import SIPTaobaoProxy
import simplejson as json
from disc.crawler import dbsource
from disc import commutil
logger = commutil.get_logger('disc.sip.itemcat')

class ItemCategory:
    """
    Attributes:
        cid
        parent_cid: 0-no paremtn
        name
        is_parent: boolean
        status:[0:normal, 1:deleted]
        sort_order: int
    """


class TaobaoItemCatsResult:
    """
    Attributes:
        last_modified: datetime
        item_cats: ItemCategory[]
    """


def crawl_item_cats(from_date=datetime.strptime('2008-01-01 00:00:00', '%Y-%m-%d %H:%M:%S')):
    _proxy = SIPTaobaoProxy(sip.APP_CODE, sip.APP_SECRET)
    _res = _proxy.call_sip('taobao.itemcats.get.v2', fields='cid,parent_cid,is_parent,name,status,sort_order', datetime=from_date.strftime('%Y-%m-%d %H:%M:%S'))
    _json_res = json.loads(_res)
    _result = TaobaoItemCatsResult()
    _result.last_modified = datetime.strptime(_json_res['rsp']['lastModified'], '%Y-%m-%d %H:%M:%S')
    _result.item_cats = []
    for _cat in _json_res['rsp']['item_cats']:
        _o = TaobaoItemCatsResult()
        _o.cid = _cat['cid']
        _parent_id = int(_cat['parent_cid'])
        _o.parent_cid = _parent_id or None
        _o.name = _cat['name']
        _o.is_parent = bool(_cat['is_parent'])
        _o.sort_order = _cat['sort_order']
        if _cat['status'] == 'normal':
            _o.status = 0
        else:
            _o.status = 1
        _result.item_cats.append(_o)

    return _result


def insert_item_cat(item_cat):
    _conn = dbsource.get_conn()
    _cursor = _conn.cursor()
    _sql = '\n        insert into tb_item_categories(\n            CATEGORY_ID,\n            NAME,\n            IS_PARENT,\n            PARENT_CATEGORY_ID,\n            STATUS,\n            SORT_ORDER,\n            CREATION_DATE,\n            LAST_UPDATE_DATE)\n        values(\n            %(cid)s,\n            %(name)s,\n            %(is_parent)s,\n            %(parent_cid)s,\n            %(status)s,\n            %(sort_order)s,\n            now(),\n            now()\n        )\n        '
    _cursor.execute(_sql, vars(item_cat))
    if _cursor.rowcount == 1:
        return True
    return False


def is_exists(cid):
    _conn = dbsource.get_conn()
    _cursor = _conn.cursor()
    _sql = '\n        select count(*) from tb_item_categories where category_id=%s\n        '
    _cursor.execute(_sql, cid)
    _count = _cursor.fetchone()[0]
    return _count > 0


def update_item_cat(item_cat):
    _conn = dbsource.get_conn()
    _cursor = _conn.cursor()
    _sql = '\n        update tb_item_categories set\n            NAME=%(name)s,\n            IS_PARENT=%(is_parent)s,\n            PARENT_CATEGORY_ID=%(parent_cid)s,\n            STATUS=%(status)s,\n            SORT_ORDER=%(sort_order)s,\n            LAST_UPDATE_DATE=now()\n        where CATEGORY_ID=%(cid)s\n        '
    _cursor.execute(_sql, vars(item_cat))
    if _cursor.rowcount == 0:
        return insert_item_cat(item_cat)
    return True


if __name__ == '__main__':
    _res = crawl_item_cats()
    logger.debug('Total category is %d' % len(_res.item_cats))
    for _item_cat in _res.item_cats:
        update_item_cat(_item_cat)

    print "success to update item's categories data"