# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/dummy/basedb.py
# Compiled at: 2019-08-16 02:55:35
# Size of source mod 2**32: 2487 bytes
import os, sqlite3, threading

class BaseDb(object):

    def __init__(self, db_path, check_thread_safe=False):
        """ 
            数据库连接初始化
            check_thread_safe:表示是否检查sqlite的多线程安全性
            sqlite默认时不支持多线程的,需要自己实现锁保证sqlite多线程操作安全
        """
        self.conn = sqlite3.connect(db_path, check_same_thread=check_thread_safe)
        self.conn.text_factory = str
        self.cursor = self.conn.cursor()
        self._lock = threading.Lock()

    def close(self):
        try:
            self.cursor.close()
        finally:
            self.conn.close()

    def create_table(self, sql, table_name):
        """
            创建数据库表
        """
        self.cursor.execute(sql)
        self.conn.commit()

    def save(self, sql, datas):
        """
            插入数据
        """
        with self._lock:
            if datas is not None:
                for data in datas:
                    self.cursor.execute(sql, data)

                self.conn.commit()
                return self.cursor.lastrowid

    def fetchall(self, sql):
        """
            查询所有数据
        """
        self.cursor.execute(sql)
        results = self.cursor.fetchall()
        return results

    def fetchone(self, sql, data=None):
        """
            查询一条数据
        """
        with self._lock:
            if data is not None:
                self.cursor.execute(sql, data)
                result = self.cursor.fetchone()
            else:
                self.cursor.execute(sql)
                result = self.cursor.fetchone()
            return result

    def update(self, sql, datas=None):
        """
            更新数据
        """
        with self._lock:
            if datas is not None:
                for data in datas:
                    self.cursor.execute(sql, data)
                    self.conn.commit()

            else:
                self.cursor.execute(sql)
                self.conn.commit()

    def delete(self, sql, datas=None):
        """
            删除数据
        """
        if datas is not None:
            for data in datas:
                self.cursor.execute(sql, data)
                self.conn.commit()

        else:
            self.cursor.execute(sql)
            self.conn.commit()