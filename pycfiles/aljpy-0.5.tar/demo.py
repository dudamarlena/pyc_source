# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.10-x86_64/egg/opensearchsdk/demo.py
# Compiled at: 2016-09-02 10:17:07
import json
from opensearchsdk.client import Client

def list_app(client):
    apps = client.app.list(page=1, page_size=1)
    print apps


def create_app(client):
    app = client.app.create('test_app', 'a')
    print app


def creat_data_process(client):
    table_name = 'test_table'
    items = [
     {'cmd': 'add', 
        'timestamp': 1401342874777, 
        'fields': {'id': '1', 
                   'title': 'This is the title', 
                   'body': 'This is the body'}},
     {'cmd': 'update', 
        'timestamp': 1401342874778, 
        'fields': {'id': '2', 
                   'title': 'This is the new title'}},
     {'cmd': 'delete', 
        'fields': {'id': '3'}}]
    items = json.dumps(items)
    data_ret = client.data.create('test_app', table_name, items)
    print data_ret


def search(client):
    body = dict(index_name='test_app', query='query=id:"0"', fetch_fields='testname', first_formula_name='default', formula_name='default', summary='summary_snipped:1,summary_field:title,summary_element:high,summary_len:32,summary_ellipsis:...;summary_snipped:2,summary_field:body,summary_element:high,summary_len:60,summary_ellipsis:...')

    def simple_search():
        res = client.search.search(**body)
        print res

    def combine_search_1():
        body['scroll'] = '1h'
        body['search_type'] = 'scan'
        res = client.search.search(**body)
        print res
        return res.get('result').get('scroll_id')

    def combine_search_2(scroll_id):
        del body['scroll']
        body['scroll_id'] = scroll_id
        res = client.search.search(**body)
        print res

    simple_search()
    scroll_id = combine_search_1()
    combine_search_2(scroll_id)


def suggest(client):
    res = client.suggest.suggest('的', 'test_app', 's2')
    print res


def index_refactor(client):

    def refactor_only():
        res = client.index.refactor('test_app')
        print res

    def refactor_import_data():
        res = client.index.refactor('test_app', 'import', 'id')
        print res

    refactor_import_data()


def get_error_log(client):
    res = client.log.get('test_app', '1', 1, 'ASC')
    print res


if __name__ == '__main__':
    import mykey, logging
    LOG = logging.basicConfig(level=logging.DEBUG, format='[%(asctime)s] %(name)s:%(levelname)s: %(message)s')
    url = 'http://opensearch-cn-hangzhou.aliyuncs.com'
    key = mykey.KEY['key_secrete']
    key_id = mykey.KEY['key_id']
    client = Client(url, key, key_id)