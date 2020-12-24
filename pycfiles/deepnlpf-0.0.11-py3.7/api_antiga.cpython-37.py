# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/deepnlpf/core/api_antiga.py
# Compiled at: 2020-04-01 09:29:39
# Size of source mod 2**32: 9359 bytes
"""
    Software: API Server
    Description: 
    Date: 13/02/2019
"""
import os, sys, json, datetime
from bson import json_util
from bson.json_util import dumps
from bson.objectid import ObjectId
from flask import Flask, request, jsonify
from flask_socketio import SocketIO, emit
from deepnlpf.pipeline import Pipeline
from deepnlpf.core.util import Util
from deepnlpf.core.plugin_manager import PluginManager
from deepnlpf.models.logs import Logs
from deepnlpf.models.mongodb import DataBase
from deepnlpf.models.dataset import Dataset
from deepnlpf.models.document import Document
from deepnlpf.models.analysis import Analysis
from deepnlpf.mongoflask import MongoJSONEncoder, ObjectIdConverter
app = Flask(__name__, instance_relative_config=True)
app.config['SECRET_KEY'] = 'JebwpwqaiXdmqteOmjUxpJdVufWJyneL'
app.json_encoder = MongoJSONEncoder
app.url_map.converters['objectid'] = ObjectIdConverter
socketio = SocketIO(app)
db = DataBase()

@socketio.on('connect')
def connect():
    emit('message', {'hello': 'Hello'})


@app.route('/annotation', methods=['POST'])
def annotation():
    response = {'corpus':db.select_all(),  'plugins':PluginManager().loadManifest()}
    return jsonify(response)


@app.route('/annotation_processing', methods=['POST', 'GET'])
def annotation_processing():
    if request.method == 'POST':
        jsondata = request.get_json()
        custom_pipeline = json.loads(jsondata)
        annotation = Pipeline(custom_pipeline['id_corpus'], custom_pipeline, True)
    else:
        id_corpus = request.args.get('id_corpus')
        tools = request.args.get('tools')
        custom_pipeline = json.loads(tools)
        annotation = Pipeline(id_corpus, custom_pipeline, True)
    response = annotation.annotate()
    return jsonify(response)


@app.route('/corpus', methods=['POST'])
def corpus():
    response = {'corpus': db.select_all()}
    return jsonify(response)


@app.route('/corpus_view', methods=['POST'])
def corpus_view():
    jsondata = request.get_json()
    data = json.loads(jsondata)
    response_datase = Dataset().select({'_id': ObjectId(data['_id'])})
    response_documents = Document().select_all({'_id_dataset': ObjectId(data['_id'])})
    return jsonify({'corpus':response_datase, 
     'documents':response_documents})


@app.route('/corpus_statistic', methods=['POST'])
def corpus_statistic():
    jsondata = request.get_json()
    data = json.loads(jsondata)
    response_db_corpus = Dataset().select({'_id': ObjectId(data['_id'])})
    response_db_statistics = db.select_statistics({'_id_dataset': data['_id']})
    dt = {'corpus':response_db_corpus, 
     'statistics':response_db_statistics}
    if response_db_corpus:
        if response_db_statistics:
            return jsonify(dt)
    from deepnlpf.statistics import Statistics
    statistics = Statistics(data['_id'])
    response_statistics = statistics.full_statistics(save=True)
    if response_statistics:
        dt = {'corpus':response_db_corpus,  'statistics':db.select_statistics({'_id_dataset': data['_id']})}
        return jsonify(dt)


@app.route('/corpus_analysis', methods=['POST'])
def corpus_analysis():
    jsondata = request.get_json()
    data = json.loads(jsondata)
    response_corpus = Dataset().select({'_id': ObjectId(data['_id'])})
    response_documents = Analysis().select_all({'_id_dataset': ObjectId(data['_id'])})
    return jsonify({'corpus':response_corpus,  'annotations':response_documents})


@app.route('/corpus_upload', methods=['POST', 'GET'])
def corpus_upload():
    if request.method == 'POST':
        jsondata = request.get_json()
        data = json.loads(jsondata)
        path_corpus = data['path_corpus']
        _id_dataset = ''
        if os.path.isdir(path_corpus):
            if os.listdir(path_corpus) == []:
                print('Folder empty!')
            else:
                corpus_name = os.path.basename(os.path.normpath(path_corpus))
                _id_dataset = Dataset().save({'name':corpus_name, 
                 'data_time':datetime.datetime.now()})
                print('corpus: {}'.format(corpus_name))
                dirContents = os.listdir(path_corpus)
                files = []
                subfolders = []
                for filename in dirContents:
                    if os.path.isdir(os.path.join(os.path.abspath(path_corpus), filename)):
                        subfolders.append(filename)

                if subfolders:
                    data = []
                    for folders_type in subfolders:
                        print('├── {}:'.format(folders_type))
                        folders_labels = os.listdir(path_corpus + '/' + folders_type)
                        for _label in folders_labels:
                            cont_doc = 0
                            if os.path.isdir(os.path.join(os.path.abspath(path_corpus + '/' + folders_type), _label)):
                                for doc_name in os.listdir(path_corpus + '/' + folders_type + '/' + _label + '/'):
                                    cont_doc += 1
                                    text_raw = Util().open_txt(path_corpus + '/' + folders_type + '/' + _label + '/' + doc_name)
                                    item = {'_id_dataset':_id_dataset, 
                                     'name':doc_name, 
                                     'type':folders_type, 
                                     'label':_label, 
                                     'sentences':text_raw}
                                    Document().save(item)

                                f = {'type':folders_type, 
                                 'label':_label, 
                                 'doc':cont_doc}
                                data.append(f)

                    log = {'_id_dataset':_id_dataset, 
                     'info':'Save corpus.', 
                     'data':data, 
                     'data_time':datetime.datetime.now()}
                else:
                    if files:
                        data = []
                        cont_doc = 0
                        for doc_name in os.listdir(path_corpus):
                            cont_doc += 1
                            text_raw = Util().open_txt(path_corpus + '/' + doc_name)
                            item = {'_id_dataset':_id_dataset, 
                             'name':doc_name, 
                             'sentences':text_raw}
                            Document().save(item)

                        data.append({'doc': cont_doc})
                        log = {'_id_dataset':_id_dataset, 
                         'info':'Save corpus.', 
                         'data':data, 
                         'data_time':datetime.datetime.now()}
                    Logs().save(log)
                    print('└── _id_dataset:', _id_dataset)
        else:
            print('This path does not contain a valid directory!')
    else:
        path_corpus = request.args.get('path_corpus')
        base = os.path.basename(path_corpus)
        name = os.path.splitext(base)[0]
        entries = os.listdir(path_corpus)
        corpus_name = os.path.basename(os.path.normpath(path_corpus))
    return jsonify({'corpus': _id_dataset})


@app.route('/corpus_download', methods=['POST'])
def corpus_download():
    jsondata = request.get_json()
    data = json.loads(jsondata)
    response = db.select({'_id': ObjectId(data['_id'])})
    return jsonify(response)


@app.route('/corpus_delete', methods=['POST'])
def corpus_delete():
    jsondata = request.get_json()
    data = json.loads(jsondata)
    response = db.delete(data['_id'])
    return jsonify(response)


@app.route('/')
def index():
    from flask import render_template
    return render_template('index.html')


app.config['DEBUG'] = True
app.jinja_env.auto_reload = True
app.config['TEMPLATES_AUTO_RELOAD'] = True