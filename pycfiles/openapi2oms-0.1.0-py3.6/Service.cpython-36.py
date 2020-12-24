# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/openapi2oms/Service.py
# Compiled at: 2019-10-16 02:14:28
# Size of source mod 2**32: 944 bytes
import json
from flask import Flask, make_response, request
from openapi2oms.Converter import Converter

class Service:
    app = Flask(__name__)

    def convert(self):
        req = request.get_json()
        spec = req.get('spec')
        props = req.get('properties')
        try:
            c = Converter(contents=spec, properties=props)
            return self.end({'spec': c.convert()})
        except BaseException as e:
            return self.end({'error':str(e),  'spec':None})

    @staticmethod
    def end(res, response_code=200):
        resp = make_response(json.dumps(res), response_code)
        resp.headers['Content-Type'] = 'application/json; charset=utf-8'
        return resp


if __name__ == '__main__':
    service = Service()
    service.app.add_url_rule('/convert', 'convert', (service.convert), methods=[
     'post'])
    service.app.run(host='0.0.0.0', port=9000)