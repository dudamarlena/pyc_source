# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/parser_engine/clue/pipelines.py
# Compiled at: 2019-04-16 05:55:04
# Size of source mod 2**32: 977 bytes
from .items import ClueItem
from .models import ClueModel

class CluePersistentPipeline(object):

    def process_item(self, item, spider):
        if isinstance(item, ClueItem):
            if not ClueModel.table_exists():
                ClueModel.create_table()
            model = ClueModel.from_item(item)
            model.save()
            item['req'].meta['clue_id'] = model.id
            spider.info('CluePersistentPipeline save clue {clue_id} to database'.format(clue_id=(item['req'].meta.get('clue_id'))))
        return item


class CluePipeline(object):

    def process_item(self, item, spider):
        if isinstance(item, ClueItem):
            clue_id = item['req'].meta.get('clue_id')
            spider.info('CluePipeline route clue {clue_id} to queue'.format(clue_id=clue_id))
            spider.route('%s:%s:start_urls' % (item['project'], item['spider']), item['req'])
        return item