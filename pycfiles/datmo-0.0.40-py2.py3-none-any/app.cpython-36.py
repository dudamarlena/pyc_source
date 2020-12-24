# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/anandsampat/datmo/datmo/datmo/dashboard/app.py
# Compiled at: 2018-11-13 11:27:09
# Size of source mod 2**32: 12846 bytes
import os, math, shutil, uuid, json
from flask import Flask, url_for
from flask import render_template, request, jsonify
import plotly
from datetime import datetime
from datmo.config import Config
from datmo.core.entity.run import Run
from datmo.core.controller.base import BaseController
from datmo.core.util.misc_functions import prettify_datetime, printable_object
from datmo.monitoring import Monitoring
app = Flask(__name__)
base_controller = BaseController()
datmo_monitoring = Monitoring()
user = {'name':'Shabaz Patel', 
 'username':'shabazp', 
 'email':'shabaz@datmo.com', 
 'gravatar_url':'https://www.gravatar.com/avatar/' + str(uuid.uuid1()) + '?s=220&d=identicon&r=PG'}

@app.route('/')
def home():
    models = [base_controller.model.__dict__] if base_controller.model else []
    return render_template('profile.html', user=user, models=models)


@app.route('/<model_name>')
def model_summary(model_name):
    model = base_controller.model.__dict__
    snapshots = [
     {'id':'alfwokd', 
      'created_at':'Sun March 3rd, 2018', 
      'labels':[
       'cool', 'default'], 
      'config':{'algorithm': 'random forest'}, 
      'stats':{'accuracy': 0.98}}]
    config_keys = [
     'algorithm']
    stats_keys = ['accuracy']
    return render_template('model_summary.html',
      user=user,
      model=model,
      snapshots=snapshots,
      config_keys=config_keys,
      stats_keys=stats_keys)


@app.route('/<model_name>/experiments')
def model_experiments(model_name):
    model = base_controller.model.__dict__
    if model_name == model['name']:
        tasks = base_controller.dal.task.query({'model_id': model['id']})
        experiments = [Run(task) for task in tasks]
        for experiment in experiments:
            experiment.config_printable = printable_object(experiment.config)
            experiment.start_time_prettified = prettify_datetime(experiment.start_time)
            experiment.end_time_prettified = prettify_datetime(experiment.end_time)
            experiment.results_printable = printable_object(experiment.results)

    else:
        experiments = []
    return render_template('model_experiments.html',
      user=user,
      model=model,
      experiments=experiments)


@app.route('/<model_name>/snapshots')
def model_snapshots(model_name):
    model = base_controller.model.__dict__
    if model_name == model['name']:
        snapshots = base_controller.dal.snapshot.query({'model_id': model['id']})
        snapshots = [(snapshot, snapshot.to_dictionary(stringify=True)) for snapshot in snapshots]
    else:
        snapshots = []
    config_keys = set(item for sublist in [snapshot[0].__dict__['config'].keys() for snapshot in snapshots] for item in sublist)
    stats_keys = set(item for sublist in [snapshot[0].__dict__['stats'].keys() for snapshot in snapshots] for item in sublist)
    return render_template('model_snapshots.html',
      user=user,
      model=model,
      snapshots=snapshots,
      config_keys=config_keys,
      stats_keys=stats_keys)


@app.route('/data/<model_name>/deployments/<deployment_version_id>/<model_version_id>')
def model_deployment_data(model_name, deployment_version_id, model_version_id):
    start = request.args.get('start', 0)
    count = request.args.get('count', None)
    data_type = request.args.get('data_type', None)
    key_name = request.args.get('key_name', None)
    graph_type = request.args.get('graph_type', None)
    if not data_type:
        if not key_name:
            if not graph_type:
                return ('error', 400)
    filter = {'model_id':model_name,  'deployment_version_id':deployment_version_id, 
     'model_version_id':model_version_id, 
     'start':int(start)}
    if count:
        filter['count'] = int(count)
    new_data = datmo_monitoring.search_metadata(filter)
    num_new_results = len(new_data)
    if data_type not in ('input', 'prediction', 'feedback', 'system_metrics'):
        return ('error', 400)
    else:
        if graph_type == 'timeseries':
            new_time_data = [datum['updated_at'] if datum['updated_at'] else datum['created_at'] for datum in new_data]
            new_time_data_datetime = [datetime.fromtimestamp(float(t) / 1000).strftime('%Y-%m-%d %H:%M:%S') for t in new_time_data]
            new_feature_data = [datum[data_type][key_name] if datum[data_type] else None for datum in new_data]
            graph_data_output = {'new_data': {'x':[
                           new_time_data_datetime], 
                          'y':[
                           new_feature_data]}}
        else:
            if graph_type == 'histogram':
                filter = {'model_id':model_name,  'deployment_version_id':deployment_version_id, 
                 'model_version_id':model_version_id}
                cumulative_data = datmo_monitoring.search_metadata(filter)
                cumulative_feature_data = [datum[data_type][key_name] for datum in cumulative_data if datum[data_type] if key_name in datum[data_type].keys()]
                import numpy as np
                counts, binedges = np.histogram(cumulative_feature_data)
                binsize = binedges[1] - binedges[0]
                bin_names = [str(round(binedge, 2)) + ' : ' + str(round(binedge + binsize, 2)) for binedge in binedges]
                graph_data_output = {'cumulative_data': {'x':[
                                      bin_names], 
                                     'y':[
                                      counts]}}
            else:
                if graph_type == 'gauge':
                    new_feature_data = [datum[data_type][key_name] if datum[data_type] else None for datum in new_data]
                    if len(new_feature_data) > 0:
                        average = sum(new_feature_data) / float(len(new_feature_data))
                    else:
                        average = None
                    graph_data_output = {'average': average}
                else:
                    return ('error', 400)
        graph_data_outputJSON = json.dumps(graph_data_output,
          cls=(plotly.utils.PlotlyJSONEncoder))
        return jsonify(graph_data_output_json_str=graph_data_outputJSON,
          num_new_results=num_new_results)


@app.route('/<model_name>/deployments/<deployment_version_id>/<model_version_id>')
def model_deployment_detail(model_name, deployment_version_id, model_version_id):
    model = base_controller.model.__dict__
    filter = {'model_id':model_name, 
     'model_version_id':model_version_id, 
     'deployment_version_id':deployment_version_id}
    input_keys, prediction_keys, feedback_keys = [], [], []
    data = datmo_monitoring.search_metadata(filter)
    if data:
        max_index = 0
        for ind, datum in enumerate(data):
            if datum['feedback'] is not None:
                max_index = ind

        datum = data[max_index]
        input_keys = list(datum['input'].keys())
        prediction_keys = list(datum['prediction'].keys())
        feedback_keys = list(datum['feedback'].keys()) if datum['feedback'] is not None else []
    graph_dirpath = os.path.join(base_controller.home, Config().datmo_directory_name, 'deployments', deployment_version_id, model_version_id, 'graphs')
    if not os.path.exists(graph_dirpath):
        os.makedirs(graph_dirpath)
    deployment_info = datmo_monitoring.get_deployment_info(deployment_version_id=deployment_version_id)
    deployment_info['created_at'] = prettify_datetime(deployment_info['created_at'])
    deployment_info['endpoints'] = [endpoint for endpoint in deployment_info['endpoints'] if ''.join(model_version_id.split('_')) in endpoint]
    deployment_info['service_paths'] = [path for path in deployment_info['service_paths'] if ''.join(model_version_id.split('_')) in path]
    deployment_info['deployment_version_id'] = deployment_version_id
    deployment_info['model_version_id'] = model_version_id
    return render_template('model_deployment_detail.html',
      user=user,
      model=model,
      deployment=deployment_info,
      graph_dirpath=graph_dirpath,
      input_keys=input_keys,
      prediction_keys=prediction_keys,
      feedback_keys=feedback_keys)


@app.route('/<model_name>/deployments')
def model_deployments(model_name):
    model = base_controller.model.__dict__
    filter = {'model_id': model_name}
    all_data = datmo_monitoring.search_metadata(filter)
    model_version_ids = set(data['model_version_id'] for data in all_data)
    deployment_version_ids = set(data['deployment_version_id'] for data in all_data)
    deployments = []
    for deployment_version_id in deployment_version_ids:
        for model_version_id in model_version_ids:
            try:
                deployment_info = datmo_monitoring.get_deployment_info(deployment_version_id=deployment_version_id)
            except:
                break

            deployment_info['created_at'] = prettify_datetime(deployment_info['created_at'])
            deployment_info['endpoints'] = [endpoint for endpoint in deployment_info['endpoints'] if ''.join(model_version_id.split('_')) in endpoint]
            deployment_info['service_paths'] = [path for path in deployment_info['service_paths'] if ''.join(model_version_id.split('_')) in path]
            deployment_info['deployment_version_id'] = deployment_version_id
            deployment_info['model_version_id'] = model_version_id
            deployments.append(deployment_info)

    return render_template('model_deployments.html',
      user=user,
      model=model,
      deployments=deployments)


@app.route('/<model_name>/deployments/<deployment_version_id>/<model_version_id>/custom/create')
def model_deployment_script_create(model_name, deployment_version_id, model_version_id):
    content = request.args.get('content')
    filepath = request.args.get('filepath')
    dirpath, _ = os.path.split(filepath)
    if not os.path.exists(dirpath):
        os.makedirs(dirpath)
    with open(filepath, 'w') as (f):
        f.write(content)
    return ('complete', 200)


@app.route('/<model_name>/deployments/<deployment_version_id>/<model_version_id>/custom/run')
def model_deployment_script_run(model_name, deployment_version_id, model_version_id):
    filepath = request.args.get('filepath')
    if not os.path.isfile(filepath):
        return ('error', 400)
    else:
        os.system('python ' + filepath)
        return ('complete', 200)


@app.route('/hash/generate')
def generate_hash():
    string_to_hash = str(request.args.get('string_to_hash'))
    hash = str(uuid.uuid3(uuid.NAMESPACE_DNS, string_to_hash))
    return jsonify({'result': hash})


@app.route('/alias/create')
def create_alias():
    filepath = request.args.get('filepath')
    graph_id = request.args.get('graph_id')
    available_filepath = os.path.join(app.root_path, 'static', 'img', graph_id + '.jpg')
    print(filepath)
    if os.path.exists(available_filepath):
        os.remove(available_filepath)
    shutil.copy(src=filepath, dst=available_filepath)
    print(available_filepath)
    webpath = url_for('static', filename=('./img/' + graph_id + '.jpg'))
    return jsonify({'webpath': webpath})


if __name__ == '__main__':
    app.run(debug=True)