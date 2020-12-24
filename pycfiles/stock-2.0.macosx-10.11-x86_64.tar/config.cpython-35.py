# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python3.5/site-packages/stock/config.py
# Compiled at: 2017-02-06 08:16:29
# Size of source mod 2**32: 1901 bytes
import os, logging
from collections import OrderedDict

def set(**kw):
    g = globals()
    for k, v in kw.items():
        g[k.upper()] = v


ROOTDIR = '/'.join(os.path.abspath(__file__).split('/')[:-2])
HERE = os.path.dirname(__file__)
DEBUG = False
LOG_LEVEL = logging.INFO
HOST = 'localhost'
PORT = int(os.environ.get('PORT', 5000))
DATABASE_URL = os.environ.get('DATABASE_URL', 'sqlite:///%s/db.sqlite3' % HERE)
CREATE_ENGINE = {'encoding': 'utf-8', 
 'pool_recycle': 3600, 
 'echo': DEBUG}
QUANDL_CODE_API_KEY = os.environ.get('QUANDL_CODE_API_KEY')
STATIC_DIR = os.path.join(ROOTDIR, 'static')
GRAPH_DIR = os.path.join(STATIC_DIR, 'company')
FORMAT = {'image_dir': os.path.join(GRAPH_DIR, '{code}'), 
 'month': '{code}/{year}_{month}'}
COMPANY_XLS_URL = 'http://www.jpx.co.jp/markets/statistics-equities/misc/tvdivq0000001vg2-att/data_j.xls'
EXCEL_COMPANY_HEADER = OrderedDict([
 ('date', '日付'),
 ('code', 'コード'),
 ('name', '銘柄名'),
 ('_item', '市場・商品区分'),
 ('category33', '33業種コード'),
 ('label33', '33業種区分'),
 ('category17', '17業種コード'),
 ('label17', '17業種区分'),
 ('scale', '規模コード'),
 ('label_scale', '規模区分')])
SHEET_NAME = 'Sheet1'
DEFAULT_DAYS_PERIOD = 90
DEFAULT_ROLLING_MEAN_RATIO = 5
DATE_FORMATS = [
 '%Y/%m/%d', '%Y-%m-%d']
MAP_PRICE_COLUMNS = {}
for v in ['open', 'close', 'high', 'low']:
    p = 'price'
    keys = [v, v.title(), '%s %s' % (v, p), '%s %s' % (v.title(), p.title()), '%s%s' % (v.title(), p.title())]
    for k in keys:
        MAP_PRICE_COLUMNS[k] = v