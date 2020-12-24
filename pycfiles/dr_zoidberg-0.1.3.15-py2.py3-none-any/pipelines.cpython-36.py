# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ginopalazzo/Magic/zoidberg/zoidberg/scraper/pipelines.py
# Compiled at: 2018-03-09 10:51:35
# Size of source mod 2**32: 1731 bytes
from scrapy.exporters import JsonLinesItemExporter, CsvItemExporter
from pathlib import Path

class CleanItemsPipeline(object):
    __doc__ = '\n    Function to clean the items\n    TODO: make uniform data format\n    '

    def process_item(self, item, spider):
        item['text'] = item['text'].replace('\r', '').replace('\n', '').replace('\t', '')
        print('object: ')
        print(object)
        item['date'] = item['date']
        return item


class JsonPipeline(object):
    __doc__ = '\n    PipeLine that writes a jsonline file\n    '

    def open_spider(self, spider):
        self.file = open(spider.path, 'ab')
        self.exporter = JsonLinesItemExporter((self.file), encoding='utf-8', ensure_ascii=False)
        self.exporter.start_exporting()

    def close_spider(self, spider):
        self.exporter.finish_exporting()
        self.file.close()

    def process_item(self, item, spider):
        self.exporter.export_item(item)
        return item


class CsvPipeline(object):
    __doc__ = '\n    PipeLine that writes a csv file\n    '

    def open_spider(self, spider):
        include_headers_line = not Path(spider.path).is_file()
        self.file = open(spider.path, 'ab')
        self.exporter = CsvItemExporter((self.file), include_headers_line=include_headers_line, encoding='utf-8')
        self.exporter.start_exporting()

    def close_spider(self, spider):
        self.exporter.finish_exporting()
        self.file.close()

    def process_item(self, item, spider):
        self.exporter.export_item(item)
        return item