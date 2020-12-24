# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\debug_a\rest_api.py
# Compiled at: 2018-06-02 23:42:01
# Size of source mod 2**32: 1708 bytes
"""
基于flask的Restful-API
=====================================================================
"""
from flask import Flask
from flask import request
from flask import jsonify
from gevent.wsgi import WSGIServer
from debug_a.collector.realtime import bars
app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False
apis = {'/hq': {'desc':'获取个股行情', 
         'example':'/hq?code=600122', 
         'success_count':0, 
         'fail_count':0}}

@app.route('/', methods=['GET'])
def index():
    return jsonify({'info':'欢迎使用 debug_a Restful-API！',  'apis':apis})


@app.route('/hq', methods=['GET', 'POST'])
def get_hq():
    """获取个股行情"""
    try:
        code = request.args.get('code')
        bar = bars(code)
        hq = dict(bar.iloc[0])
        msg_template1 = '截止{date}，{name}（{code}）的最新价格是{price}元，上一交易日收盘价是{pre_close}元，当日成交量{vol}万元，请知悉。'
        msg_1 = msg_template1.format(date=(hq['date']),
          name=(hq['name']),
          code=(hq['code']),
          pre_close=(hq['pre_close']),
          price=(hq['price']),
          vol=(round(float(hq['amount']) / 10000, 4)))
        apis['/hq']['success_count'] += 1
        return jsonify({'info':'success',  'hq':hq,  'msg':msg_1})
    except Exception as e:
        apis['/hq']['fail_count'] += 1
        return jsonify({'info':'fail',  'error_msg':'行情获取失败，原因：%s' % str(e)})


def start_api(host='0.0.0.0', port=5000):
    WSGIServer((host, port), app).serve_forever()


if __name__ == '__main__':
    start_api()