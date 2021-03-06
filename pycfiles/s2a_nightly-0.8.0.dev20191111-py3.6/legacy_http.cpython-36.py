# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/seq2annotation/server/legacy_http.py
# Compiled at: 2019-11-04 07:23:49
# Size of source mod 2**32: 1420 bytes
import sys
from flask import Flask, request, jsonify
from flask_cors import CORS
from seq2annotation.server.tensorflow_inference import Inference
app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False
CORS(app)
server = None

def load_predict_fn(export_dir):
    global server
    server = Inference(export_dir)
    return server


def sequence_to_response(text, seq):
    response = {'text':text, 
     'spans':[{'start':i.start,  'end':i.end,  'type':i.entity} for i in seq.span_set], 
     'ents':list({i.entity.lower() for i in seq.span_set})}
    return response


@app.route('/parse', methods=['GET'])
def single_tokenizer():
    text_msg = request.args.get('q')
    print(text_msg)
    raw_input_text, seq, tags, failed = server.infer(text_msg)
    print(tags)
    response = sequence_to_response(raw_input_text, seq)
    return jsonify(response)


@app.route('/parse', methods=['POST'])
def batch_infer():
    text_msg = request.get_json()
    print(text_msg)
    infer_results = server.batch_infer(text_msg)
    response = []
    for raw_input_text, seq, tags, failed in infer_results:
        response.append(sequence_to_response(raw_input_text, seq))

    return jsonify(response)


if __name__ == '__main__':
    load_predict_fn(sys.argv[1])
    app.run(host='0.0.0.0', port=5000)