# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/seq2annotation/server/http.py
# Compiled at: 2019-11-05 02:23:26
# Size of source mod 2**32: 2233 bytes
import os, sys
from typing import Union, List
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from deliverable_model.builtin.processor.biluo_decode_processor import PredictResult
from deliverable_model.serving import SimpleModelInference
current_dir = os.path.dirname(__file__)
http_root_dir = os.path.join(current_dir, 'NLP_server_frontend')
app = Flask(__name__, static_url_path='', static_folder=http_root_dir)
app.config['JSON_AS_ASCII'] = False
CORS(app)
server = None

def load_predict_fn(export_dir):
    global server
    server = SimpleModelInference(export_dir)
    return server


def seq_to_http(predict: PredictResult):
    return {'text':''.join(predict.sequence.text), 
     'spans':[{'start':i.start,  'end':i.end,  'type':i.entity} for i in predict.sequence.span_set], 
     'ents':list({i.entity.lower() for i in predict.sequence.span_set})}


def compose_http_response(seq_or_seq_list: Union[(PredictResult, List[PredictResult])]):
    if isinstance(seq_or_seq_list, list):
        result = [seq_to_http(i) for i in seq_or_seq_list]
    else:
        result = seq_to_http(seq_or_seq_list)
    return jsonify(result)


@app.route('/', defaults={'path': 'NER.html'})
def send_static(path):
    return send_from_directory(http_root_dir, path)


@app.route('/parse', methods=['GET'])
def single_tokenizer():
    text_msg = request.args.get('q')
    predict_result = list(server.parse([text_msg]))[0]
    return compose_http_response(predict_result)


@app.route('/parse', methods=['POST'])
def batch_infer():
    text_msg = request.get_json()
    predict_result_list = list(server.parse(text_msg))
    return compose_http_response(predict_result_list)


def simple_test():
    text_msg = '今天拉萨的天气。'
    predict_result = list(server.parse([text_msg]))[0]
    print(predict_result)


if __name__ == '__main__':
    load_predict_fn(sys.argv[1])
    simple_test()
    app.run(host='0.0.0.0', port=5000, threaded=False)