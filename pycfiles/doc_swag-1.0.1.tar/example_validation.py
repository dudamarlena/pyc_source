# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-build-dgUSur/flasgger/flasgger/example_validation.py
# Compiled at: 2017-06-27 07:41:04
from flask import Flask, jsonify, request
from flasgger import Swagger
from flasgger.utils import swag_from, validate, ValidationError
app = Flask(__name__)
Swagger(app)

@app.route('/', methods=['POST'])
@swag_from('test_validation.yml')
def index():
    data = request.json
    try:
        validate(data, 'user', 'test_validation.yml', __file__)
    except ValidationError as e:
        return (
         'Validation Error: %s' % e, 400)

    return jsonify(data)


app.run(debug=True)