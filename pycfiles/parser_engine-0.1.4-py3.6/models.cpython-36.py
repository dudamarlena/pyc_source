# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/parser_engine/clue/models.py
# Compiled at: 2019-04-16 05:55:04
# Size of source mod 2**32: 1869 bytes
import time, simplejson as json
from peewee import Model, PrimaryKeyField, CharField, IntegerField
from parser_engine.config import mysqldb
from .constants import ClueStatus

class ClueModel(Model):
    id = PrimaryKeyField()
    status = IntegerField(verbose_name='状态', default=0)
    created_time = IntegerField(verbose_name='创建时间', default=0)
    modified_time = IntegerField(verbose_name='更新时间', default=0)
    finished_time = IntegerField(verbose_name='完成时间', default=0)
    channel = CharField(verbose_name='渠道名称', max_length=20, default='')
    name = CharField(verbose_name='业务名称', max_length=20, default='')
    url = CharField(verbose_name='爬取url', max_length=500, default='')
    from_clue_id = IntegerField(verbose_name='来源clue的id', default=0)
    req = CharField(verbose_name='请求体', max_length=2048, default='')
    dw_count = IntegerField(verbose_name='抓取的item数量', default=0)

    class Meta:
        table_name = 'clue'
        database = mysqldb

    @staticmethod
    def from_item(item):
        model = ClueModel()
        model.url = item.get('url', item.get('req', {}).get('url'))
        model.name = item.get('business') or item.get('spider') or ''
        model.channel = item.get('channel') or item.get('project') or ''
        model.created_time = int(time.time())
        model.modified_time = int(time.time())
        model.from_clue_id = item.get('from_clue_id', 0)
        model.req = json.dumps(item.get('req'))
        return model

    def success(self):
        self.finished_time = int(time.time())
        self.status = ClueStatus.SUCCESS

    def fail(self):
        if self.status >= ClueStatus.FAILED:
            self.status += 1
        else:
            self.status = ClueStatus.FAILED