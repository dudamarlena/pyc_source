# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/vinergy/model.py
# Compiled at: 2011-06-15 13:52:27
"""
  vinergy.model
  ~~~~~~~~~~~~~

  Models of Vinergy
"""
__all__ = [
 'get_code_by_name',
 'get_code_by_oid',
 'get_count',
 'insert_code',
 'update_code']
from pymongo import Connection, DESCENDING
from config import DBURL
conn = Connection(**DBURL)
db = conn.vinergy
codebase = db.codebase

def get_code_by_name(name):
    """Get code by name"""
    code = codebase.find_one({'name': name})
    return code or None


def get_code_by_oid(oid):
    """Get code by oid (_id)"""
    code = codebase.find_one({'_id': oid})
    return code or None


def get_count():
    """Get count of latest snippet"""
    doc = codebase.find(None, {'content': 0}).sort('count', DESCENDING).limit(1)
    count = doc[0]['count']
    return int(count)


def insert_code(oid, name, content, count, date):
    """Insert new code to database"""
    code = {'_id': oid, 'name': name, 
       'content': [
                 (
                  'raw', content)], 
       'syntax': [
                'raw'], 
       'count': count, 
       'date': date}
    codebase.insert(code)


def update_code(name, content, syntax):
    """
    update doc with new rendered code.
  """
    code = {'content': [syntax, content], 'syntax': syntax}
    codebase.update({'name': name}, {'$push': code})