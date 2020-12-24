# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: b'C:\\Users\\muchu\\Desktop\\caseWorkspace\\003-\xa5d\xa6\xcc\xba\xb8scrapy\\CAMEO_git_code\\cameo_api\\flaskrunner.py'
# Compiled at: 2016-05-09 10:39:43
__doc__ = '\nCopyright (C) 2015, MuChu Hsu\nContributed by Muchu Hsu (muchu1983@gmail.com)\nThis file is part of BSD license\n\n<https://opensource.org/licenses/BSD-3-Clause>\n'
import json, threading, logging
from flask import Flask
from flask import request
from flask import jsonify
from cameo_api.spiderForYahooCurrency import SpiderForYahooCurrency
import cameo_api.apis as apis
app = Flask(__name__.split('.')[0])

def start_flask_server():
    spider = SpiderForYahooCurrency()
    spiderThread = SpiderThread(spiderInstance=spider)
    spiderThread.start()
    app.run(host='0.0.0.0', port=5000, debug=True, use_reloader=False)


@app.route('/ex_currency', methods=['GET'])
def exchangeCurrency():
    strDate = request.args.get('date', None, type=str)
    fMoney = request.args.get('money', 0.0, type=float)
    strFromCurrency = request.args.get('from', 'TWD', type=str).upper()
    strToCurrency = request.args.get('to', 'TWD', type=str).upper()
    fResultMoney = apis.exchangeCurrency(fMoney=fMoney, strFrom=strFromCurrency, strTo=strToCurrency)
    return jsonify(fResultMoney=fResultMoney, form=strFromCurrency, to=strToCurrency)


class SpiderThread(threading.Thread):

    def __init__(self, spiderInstance=None):
        threading.Thread.__init__(self)
        self.spider = spiderInstance

    def run(self):
        try:
            try:
                logging.info('SpiderThread running...')
                self.spider.runSpider()
            except Exception as ex:
                logging.warning('spider did not work.')
                logging.warning(ex)

        finally:
            logging.info('SpiderThread stoped.')


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    start_flask_server()