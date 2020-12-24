# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\HuoYan_monitoring\dash_app.py
# Compiled at: 2020-05-11 04:07:10
# Size of source mod 2**32: 5798 bytes
import dash, dash_table, pandas as pd, dash_core_components as dcc, dash_html_components as html, dash_auth, os, sys, re, argparse, numpy as np, pandas as pd
from collections import defaultdict
import json, sqlite3, logging, time, yaml, datetime
from pathlib import Path
import importlib
if __name__ == '__main__':
    if __package__ is None:
        sys.path[0] = str(Path(sys.path[0]).resolve().parent)
        __package__ = 'HuoYan_monitoring'
        importlib.import_module(__package__)
from .HuoYan_monitoring import HuoYan_monitoring
parser = argparse.ArgumentParser(description='HuoYan laboratory COVID-19 samples testing lifetime monitoring')
parser.add_argument('--db', type=str,
  help='sqlite3 database file path, create if not exists',
  default='HuoYan_records.db')
parser.add_argument('--config', type=str,
  help='path of config file, yaml format',
  default='config.yaml')
parser.add_argument('--auth', type=str,
  help='path of file contains user and passwd in yaml format',
  default='auth.yaml')
parser = parser.parse_args()
if not os.path.exists(parser.config):
    raise ValueError('无效的config文件', parser.config)
if not os.path.exists(parser.auth):
    raise ValueError('无效的auth文件', parser.config)
with open((parser.config), 'r', encoding='utf-8') as (f):
    config = yaml.load(f.read())
today = str(datetime.datetime.now()).split(' ')[0]
with open((parser.auth), 'r', encoding='utf-8') as (f):
    auth_info = yaml.load(f.read())
    auth_info = [[x, auth_info[x]] for x in auth_info.keys()]
external_stylesheets = [
 'https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
auth = dash_auth.BasicAuth(app, auth_info)
app.layout = html.Div(children=[
 html.H1(f"{config['laboratory_ch']}全流程监控系统\n"),
 html.H1(f"{config['laboratory']} COVID-19 Test Monitoring"),
 html.Button(id='submit-button', n_clicks=0, children='刷新'),
 html.Div([
  html.H2('Statistics'),
  html.Div(id='statistics')]),
 html.Div([
  html.H2('在检样本详情'),
  dcc.RadioItems(id='category',
    options=[
   {'label':'有样无单', 
    'value':'no_info'},
   {'label':'有单无样', 
    'value':'no_sample'},
   {'label':'未发报告', 
    'value':'no_report'}],
    value='no_report',
    labelStyle={'display': 'inline-block'}),
  dash_table.DataTable(id='table')]),
 html.Footer('CopyrightⒸ BGI 2020 版权所有 深圳华大基因股份有限公司 all rights reserved. ')])

@app.callback(dash.dependencies.Output('statistics', 'children'), [
 dash.dependencies.Input('submit-button', 'n_clicks')])
def get_statistics(n_clicks):
    hy = HuoYan_monitoring(configfile=(parser.config))
    try:
        hy.collect_infos()
        statistics = ''
    except Exception as e:
        try:
            statistics = e
            print(e)
        finally:
            e = None
            del e

    df = pd.read_sql('select * from test_lifetime', con=(hy.con))
    today_test_df = df[df['test'].str.contains(today).fillna(False)]
    today_report_df = df[df['report'].str.contains(today).fillna(False)]
    statistics += f"\n\t当日到样：{len(today_test_df)}\t当日已发报告：{len(today_report_df)}\n\n\n\t累计到样：{len(df)}\t累计发送报告：{len(df[df['report'].notnull()])}\t累计异常结束：{len(df[(df['finished'].notnull() & df['exception'].notnull())])}\t检测中：\t{len(df[df['finished'].isnull()])}\n\n\n\t"
    return statistics


@app.callback(dash.dependencies.Output('table', 'columns'), [
 dash.dependencies.Input('submit-button', 'n_clicks')])
def get_table_columns(n_clicks):
    hy = HuoYan_monitoring(configfile=(parser.config))
    df = pd.read_sql('select * from test_lifetime', con=(hy.con))
    return [{'name':i,  'id':i} for i in df.columns]


@app.callback(dash.dependencies.Output('table', 'data'), [
 dash.dependencies.Input('submit-button', 'n_clicks'),
 dash.dependencies.Input('category', 'value'),
 dash.dependencies.Input('statistics', 'children')])
def get_table_data(n_clicks, cate_value, state):
    hy = HuoYan_monitoring(configfile=(parser.config))
    df = pd.read_sql('select * from test_lifetime', con=(hy.con))
    if cate_value == 'no_info':
        df = df[(df.test.notnull() & df['sample'].isnull() & df.finished.isnull())]
    else:
        if cate_value == 'no_sample':
            df = df[(df.finished.isnull() & df['sample'].notnull() & df['test'].isnull() & df['exception'].isnull())]
        else:
            if cate_value == 'no_report':
                df = df[(df.finished.isnull() & df['sample'].notnull() & df.test.notnull() & df.report.isnull())]
            else:
                raise ValueError('不支持的类别', cate_value)
    return df.to_dict('rows')


if __name__ == '__main__':
    app.run_server(debug=False, port=8080)