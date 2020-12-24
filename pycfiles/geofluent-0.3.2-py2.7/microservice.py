# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/geofluent/microservice.py
# Compiled at: 2017-02-03 05:21:03
import sys, time
from flask import Flask, request, jsonify
from geofluent import GeoFluent
app = Flask(__name__)

@app.route('/', methods=['POST'])
def serve():
    data = request.get_data()
    charset = request.mimetype_params.get('charset') or 'UTF-8'
    data = data.decode(charset, 'replace')
    source = request.args.get('source')
    target = request.args.get('target')
    print data
    translation = app.gf.translate(data, source, target)
    print translation
    response = {'data': data, 
       'translation': {'text': translation, 
                       'source': source, 
                       'target': target}, 
       'timestamp': time.time()}
    return jsonify(response)


@app.route('/', methods=['HEAD'])
def head():
    return ''


if __name__ == '__main__':
    app.gf = GeoFluent(key=sys.argv[1], secret=sys.argv[2])
    port = int(sys.argv[3]) if len(sys.argv) > 3 else 5000
    app.run(host='0.0.0.0', port=port)