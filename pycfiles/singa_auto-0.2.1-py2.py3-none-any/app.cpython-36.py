# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /root/singa_auto/predictor/app.py
# Compiled at: 2020-04-15 05:36:06
# Size of source mod 2**32: 2288 bytes
import os, logging
from flask import Flask, jsonify, g, request
from flask_cors import CORS
from .predictor import Predictor
from singa_auto.model import utils
import traceback
service_id = os.environ['SINGA_AUTO_SERVICE_ID']
logger = logging.getLogger(__name__)
app = Flask(__name__)
CORS(app)

class InvalidQueryFormatError(Exception):
    pass


def get_predictor() -> Predictor:
    if not hasattr(g, 'predictor'):
        g.predictor = Predictor(service_id)
    return g.predictor


@app.route('/')
def index():
    return 'Predictor is up.'


@app.route('/predict', methods=['POST'])
def predict():
    if request.files.getlist('img'):
        img_stores = request.files.getlist('img')
        img_bytes = [img for img in [img_store.read() for img_store in img_stores] if img]
        print('img_stores', img_stores)
        print('img_bytes', img_bytes)
        return img_bytes or (
         jsonify({'ErrorMsg': 'No image provided'}), 400)
    else:
        return (
         jsonify({'ErrorMsg': 'No image provided'}), 400)
        try:
            predictor = get_predictor()
            queries = utils.dataset.load_images_from_bytes(img_bytes).tolist()
            predictions = predictor.predict(queries)
            return (jsonify(predictions), 200)
        except:
            traceback.print_exc()
            logging.error(traceback.format_exc())
            return (jsonify({'ErrorMsg': 'Server Error'}), 500)