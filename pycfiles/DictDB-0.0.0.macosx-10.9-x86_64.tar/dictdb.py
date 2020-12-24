# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/toomore/app/dictDB/venv/lib/python2.7/site-packages/dictdb.py
# Compiled at: 2014-01-15 13:12:31
""" Python dict database """
import os, ujson as json, zlib
from datetime import datetime
from time import mktime

class DictDB(object):
    """ 資料庫存取基本功能

        :param path fname: 檔案位置
        :param str backupdirname: 備份檔案資料夾名稱
    """

    def __init__(self, fname='test.json', backupdirname='backup'):
        u""" 確認檔案是否存在，否則建立一個內容為 {} 的檔案
        """
        self.fname = fname
        self.dirname = os.path.dirname(os.path.abspath(__file__))
        self.files = os.path.join(self.dirname, fname)
        self.backupfilepath = os.path.join(self.dirname, backupdirname)
        if not os.path.exists(self.files):
            with file(self.files, 'w+') as (file_data):
                file_data.write(zlib.compress(json.dumps({}), 9))
        if not os.path.exists(self.backupfilepath):
            os.makedirs(self.backupfilepath)
        with file(self.files, 'r+') as (files):
            self.data = json.loads(zlib.decompress(files.read()))

    def __repr__(self):
        return "<DictDB '%s' Count:%s Size:%sB>" % (self.fname, len(self.data),
         os.path.getsize(self.files))

    @staticmethod
    def getunitime():
        u""" 取得一個微時間值

            :rtype: str
            :returns: timestamp
        """
        now = datetime.utcnow()
        return ('{0}{1:06}').format(int(mktime(now.timetuple())), now.microsecond)

    @staticmethod
    def getdatetime(timestamp):
        u""" 將 _id 轉回時間值

            :param str timestamp: timestamp
            :rtype: :mod:`datetime`
        """
        return datetime.fromtimestamp(int(timestamp) / 1000000.0)

    def save(self):
        u""" 將目前的資料寫入檔案 """
        with file(self.files, 'w+') as (files):
            files.write(zlib.compress(json.dumps(self.data), 9))
            self.backup()

    def backup(self):
        u""" 備份檔案 """
        file_name = datetime.strftime(datetime.utcnow(), '%Y%m%d%H%M%S_%f')
        with file(os.path.join(self.backupfilepath, '%s.%s' % (
         self.fname, file_name)), 'w+') as (files):
            files.write(zlib.compress(json.dumps(self.data), 9))

    def insert(self, i):
        u""" 建立資料

            :param dict i: 該筆相符資料
            :rtype: dict
            :returns: 建立完成的資料，包含 :py:attr:`_id`
        """
        assert isinstance(i, dict)
        unikey = self.getunitime()
        i.update({'_id': unikey})
        self.data[str(unikey)] = i
        self.save()
        return i

    def update(self, i, toupdate, more=0):
        u""" 更新資料

            :param dict i: 該筆相符資料
            :param dict toupdate: 欲新增的資料
            :param int more: 更新所有相符的資料，預設為一筆
        """
        assert isinstance(i, dict)
        assert isinstance(toupdate, dict)
        if more:
            for data in self.find(i):
                self.data[data.get('_id')].update(toupdate)

        else:
            getdata = self.find_one(i)
            self.data[getdata.get('_id')].update(toupdate)
        self.save()

    def find(self, tofind=None, reverse=True, style='AND'):
        u""" 尋找資料

            :param dict tofind: 欲尋找的資料
            :param bool reverse: 排序，新→舊
            :param str style: `AND` 或 `OR`
            :rtype: list
            :returns: A list of dict data.
        """
        if tofind:
            assert isinstance(tofind, dict)
        else:
            tofind = {}

        def all_in_dict(tofind, data):
            u""" 嚴格符合 """
            return all([ 0 if i not in data else 1 if tofind.get(i) == data.get(i) else 0 for i in tofind ])

        def or_in_dict(tofind, data):
            u""" 模糊符合 """
            return any([ 0 if i not in data else 1 if tofind.get(i) in data.get(i) else 0 for i in tofind ])

        ckstyle = all_in_dict if style == 'AND' else or_in_dict
        for i in sorted(self.data, reverse=reverse):
            if ckstyle(tofind, self.data.get(i)):
                yield self.data.get(i)

    def find_one(self, tofind):
        u""" 尋找資料，無資料回傳 None

            :param dict tofind: 欲尋找的資料
            :rtype: dict or None
        """
        assert isinstance(tofind, dict)
        getfind = [ i.get('_id') for i in list(self.find(tofind)) ]
        if getfind:
            last = max(getfind)
            return self.data.get(last)
        else:
            return
            return

    def remove(self, todel):
        u""" 刪除資料

            :param dict todel: 欲刪除的資料
        """
        assert isinstance(todel, dict)
        for i in [ i.get('_id') for i in self.find(todel) ]:
            del self.data[i]

        self.save()

    def clean(self, confirm=False):
        u""" 清空資料

            :param bool confirm: double check.
        """
        if confirm:
            self.data = {}
            self.save()


if __name__ == '__main__':

    def do_adddata():
        u""" 範例 新增資料 """
        data = {'name': 'eromoot', 'age': 28, 'info': '中文…'}
        result = DictDB().insert(data)
        print result
        data = {'name': 'toomore', 'age': 28}
        result = DictDB().insert(data)
        print result


    def do_find():
        u""" 範例 取所有資料 """
        print list(DictDB().find())


    def do_find_something():
        u""" 範例 取所有資料 """
        print list(DictDB().find({'name': 'toomore'}))


    def do_find_one():
        u""" 範例 取資料 """
        print DictDB().find_one({'name': 'toomore'})


    def do_update():
        u""" 範例 修改資料  """
        data = {'name': 'toomore2', 'age': 18}
        getinsert = DictDB().insert(data)
        print getinsert
        data = {'name': 'toomore_update', 'age': 28, 'loc': 'kaohsiung'}
        DictDB().update(getinsert, data)
        print DictDB().find_one({'_id': getinsert.get('_id')})


    def do_del():
        u""" 範例 刪除資料 """
        data = {'name': 'toomore_del', 'age': 18}
        getinsert = DictDB().insert(data)
        print DictDB().find_one({'_id': getinsert.get('_id')})
        DictDB().remove({'_id': getinsert.get('_id')})
        print DictDB().find_one({'_id': getinsert.get('_id')})
        print list(DictDB().find())


    def do_getdatetime():
        u""" 範例 轉換 _id 為時間值 """
        data = {'name': 'eromoot', 'age': 28, 'info': '中文…'}
        result = DictDB().insert(data)
        print result
        print DictDB.getdatetime(result.get('_id'))


    print ('{0:-^30}').format('do_adddata')
    do_adddata()
    print ('{0:-^30}').format('do_find')
    do_find()
    print ('{0:-^30}').format('do_find_something')
    do_find_something()
    print ('{0:-^30}').format('do_find_one')
    do_find_one()
    print ('{0:-^30}').format('do_update')
    do_update()
    print ('{0:-^30}').format('do_del')
    do_del()
    print ('{0:-^30}').format('do_getdatetime')
    do_getdatetime()