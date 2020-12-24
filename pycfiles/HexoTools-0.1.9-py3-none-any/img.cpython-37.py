# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: d:\projects\hexotools\hexotools\imgmanage\img.py
# Compiled at: 2019-10-12 03:54:06
# Size of source mod 2**32: 8640 bytes
import requests as rs, os, sys, re
from hashlib import md5
import sqlite3 as s3

class UpDownload:

    def __init__(self):
        self.url = 'https://sm.ms//api/upload'
        self.headers = {'Content-Type':'multipart/form-data', 
         'Authorization':'14ac5499cfdd2bb2859e4476d2e5b1d2bad079bf'}

    def urlUpload(self, url):
        pass

    def localUpload(self, path):
        data = {'format': 'json'}
        files = {'smfile': open(path, 'rb')}
        try:
            response = rs.post((self.url), data=data, files=files)
            result = response.json()
        except:
            result = {'code':'error', 
             'message':sys.exc_info()[0]}

        return result

    @staticmethod
    def evalResult(d):
        code = d['code']
        if code == 'success':
            return (
             code, d['data']['url'], d['data']['delete'])
        elif code == 'error':
            print(d.get('message', '错误'))
            return (code, '', '')
            if code == 'exception':
                if re.match('Image upload repeated limit.*', d.get('message', '错误')):
                    url = re.match('.*(https?://.*)', d['message']).group(1)
                    return (code, url, '')
        else:
            return ('unknown', '', '')

    @staticmethod
    def imgDelete(url):
        try:
            rs.get(url)
            return True
        except:
            return False


class Img:

    def __init__(self, path='', url='', description='图片描述'):
        self.id = 0
        self.path = os.path.normpath(path)
        self.url = url
        self.delete_url = ''
        self.local_exists = False
        self.web_access = False
        self.hash = ''
        self.size = 0
        self.description = description

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, id):
        self._id = id

    @property
    def url(self):
        return self._url

    def url(self, url, delete_url):
        self._url = url
        self._delete_url = delete_url
        self.web_access = True

    @property
    def path(self):
        return self._path

    @path.setter
    def path(self, value):
        if not isinstance(value, str):
            raise TypeError('path must be an str!')
        self._path = os.path.normpath(value)

    @property
    def size(self):
        return self._size

    @size.setter
    def size(self, size=0):
        if size:
            self._size = size
        else:
            if self.local_exists:
                if self.path:
                    self._size = os.path.getsize(self.path) / 1024 / 1024
            if self.web_access and self.url:
                self._size = 0
            else:
                self._size = 0

    def localExists(self):
        self.local_exists = os.path.exists(self.path)
        return self.local_exists

    @property
    def hash(self):
        return self._hash

    @hash.setter
    def hash(self, hash=''):
        if hash:
            self._hash = hash
            return 1
            if self.local_exists and self.path:
                result = md5()
                with open(self.path, 'rb') as (fo):
                    for line in fo:
                        result.update(line)

                self._hash = result.hexdigest()
        else:
            if self.web_access:
                if self.url:
                    response = rs.get(self.url)
                    self._hash = str(format(md5(response.content), 'X'))
                    return 1
            return 0

    def webAccess(self):
        try:
            r = rs.get(self.url)
            if r.status_code == rs.codes.ok:
                self.webAccess = True
        except:
            self.webAccess = False

    @property
    def description(self):
        return self._description

    @description.setter
    def description(self, description):
        self._description = description

    def data(self):
        d = {'id':self.id, 
         'path':self.path, 
         'url':self.url, 
         'delete_url':self.delete_url, 
         'local_exists':self.local_exists, 
         'web_access':self.web_access, 
         'description':self.description, 
         'size':self.size, 
         'hash':self.hash}
        return d


class Db:

    def __init__(self, db):
        """初始化函数
        :db: string, 数据库路径
        """
        self.db = db
        self.conn = s3.connect(self.db)
        self.cursor = self.conn.cursor()
        self.table = {'info': 'create table info(\n                id           integer primary key autoincrement,\n                path         text    not null,\n                hash         text    not null,\n                size         real    not null,\n                local_exists int     not null,\n                web_access   int     not null,\n                url          text    not null,\n                delete_url   text    not null,\n                description  text    not null\n                );'}
        self.column = {'id':'id', 
         'local_exists':'local_exist', 
         'web_access':'web_access', 
         'path':'path', 
         'size':'size', 
         'url':'url', 
         'hash':'hash'}

    def creatTable(self):
        try:
            self.cursor.execute(self.table['info'])
        except:
            return

    def setCursor(self):
        pass

    def closeCursor(self):
        if self.cursor:
            self.cursor.close()

    def closeConn(self):
        if self.conn:
            self.conn.close()

    def commit(self):
        if self.conn:
            self.conn.commit()

    def insertData(self, d, commit=True):
        ls = [
         None,
         d.get('path', ''),
         d.get('hash', ''),
         d.get('size', 0),
         d.get('local_exists', 0),
         d.get('web_access', 0),
         d.get('url', ''),
         d.get('delete_url', ''),
         d.get('description', '')]
        self.cursor.execute('insert into info values (?,?,?,?,?,?,?,?,?)', ls)
        if commit:
            self.commit()

    def select(self, limit='-1', column='id', condition='>=1'):
        for r in self.cursor.execute('select url, delete_url, description, path from info where ' + self.column.get(column, 'id') + '{};'.format(condition)):
            yield r

    def isRepeative(self, hash='', url=''):
        if hash:
            result = self.cursor.execute("select url, delete_url, description, path from info where {0}=='{1}'".format('hash', hash)).fetchall()
            if result:
                return result
            return False
        else:
            if url:
                result = self.cursor.execute("select url, delete_url, description, path from info where {0}=='{1}'".format('url', url)).fetchall()
                if result:
                    return result
                return False
            else:
                return False

    def _rawApi(self, command):
        try:
            for row in self.cursor.execute(command):
                yield row

        except Exception:
            return sys.exc_info()

    def deleteRow(self, hash='', url='', delete_url=''):
        try:
            if hash:
                self.cursor.execute("delete from info where {0}=='{1}'".format('hash', hash))
                return True
            if url:
                result = self.cursor.execute("delete from info where {0}=='{1}'".format('url', url))
                return True
            if delete_url:
                self.cursor.execute("delete from info where {0}=='{1}'".format('delete_url', delete_url))
                return True
            return False
        except:
            return False