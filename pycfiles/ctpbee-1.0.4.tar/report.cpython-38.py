# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/somewheve/PycharmProjects/ctpbee/ctpbee/looper/report.py
# Compiled at: 2019-12-10 01:06:48
# Size of source mod 2**32: 1971 bytes
"""
此模块是用来帮助ctpbee的回测来生成指定的策略报告，UI本身采用

"""
import os, webbrowser
from jinja2 import Environment, PackageLoader, select_autoescape
from ctpbee import get_ctpbee_path
from datetime import datetime
from ctpbee.func import join_path
env = Environment(loader=(PackageLoader('ctpbee', 'looper/templates')),
  autoescape=(select_autoescape(['html', 'xml'])))
main_template = env.get_template('looper.html')
trade_template = env.get_template('trade_record.html')

def render_result(result, kline=None, trades=None, datetimed=None, trade_data=None, strategy=[], account_data=None, net_pnl=None, cost_time=None, **kwargs):
    """
    渲染结果并写入到本地html文件， 并返回htmk文件地址
    """
    datetimed = str(datetimed.strftime('%Y-%m-%d_%H_%M_%S'))
    code_string = main_template.render(result=result, strategy=strategy, account_data=account_data,
      net_pnl=net_pnl,
      cost_time=cost_time,
      datetime=datetimed)
    trade_code_string = trade_template.render(trade_data=trade_data)
    file_path = kwargs.get('file_path', None)
    trade_path = kwargs.get('trade_file_path', None)
    path = join_path(get_ctpbee_path(), 'looper')
    if not file_path:
        if not os.path.isdir(path):
            os.mkdir(path)
        file_path = join_path(path, datetimed + '.html')
    if not trade_path:
        trade_path = join_path(path, datetimed + '-trade.html')
    with open(file_path, 'w', encoding='utf8') as (f):
        f.write(code_string)
    with open(trade_path, 'w', encoding='utf8') as (f):
        f.write(trade_code_string)
    if kwargs.get('auto_open', None):
        webbrowser.open(file_path)
    return file_path