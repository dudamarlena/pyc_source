# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/deepnlpf/dashboard/app/views/views.py
# Compiled at: 2019-11-20 18:51:04
# Size of source mod 2**32: 8363 bytes
import sys, json, requests
from flask import render_template, request, jsonify, Response, send_file
from app import app
import plotly
import plotly.graph_objs as go
from plotly.graph_objs import *
from collections import Counter
import pandas as pd, numpy as np
server = 'http://127.0.0.1:5000'

@app.route('/', methods=['GET', 'POST'])
def annotation():
    page = 'DeepNLP / Annotation'
    if request.method == 'POST':
        option_selected = {}
        data = request.form['form-options']
        option_selected['dataset'] = request.form.get('name_dataset')
    conv = [{'input':'hi',  'topic':'Greeting'}]
    s = json.dumps(conv)
    response = requests.post((server + '/annotation'), json=s).json()
    return render_template('annotation.html', page=page, corpus=(response['corpus']), plugins=(response['plugins']))


@app.route('/annotation_processing', methods=['GET', 'POST'])
def annotation_processing():
    page = 'DeepNLP | Annotation'
    if request.method == 'POST':
        response = request.get_json()
        properties = {'tools': []}
        tools_name = set()
        id_corpus = ''
        for index, item in enumerate(response['options']):
            if index == 0:
                id_corpus = item['value']
            if index > 0:
                tool, analyze = item['name'].split('-')
                tools_name.add(tool)

        for tool in tools_name:
            analyze = {'pipeline': []}
            for index, item in enumerate(response['options']):
                if index > 0:
                    t, a = item['name'].split('-')
                    if tool == t:
                        analyze['pipeline'].append(a)
                    item = {tool: analyze}
                    properties['tools'].append(item)
                conv = {'id_corpus':id_corpus,  'properties':properties}
                s = json.dumps(conv)
                res = requests.post((server + '/annotation_processing'), json=s).json()

    return jsonify(response)


@app.route('/corpus')
def Dataset():
    conv = [{'input':'hi',  'topic':'Greeting'}]
    s = json.dumps(conv)
    response = requests.post((server + '/corpus'), json=s).json()
    return render_template('corpus.html', corpus=(response['corpus']))


@app.route('/corpus_view', methods=['GET'])
def corpus_view():
    page = 'DeepNLP | View Corpus'
    conv = {'_id': request.args.get('_id')}
    s = json.dumps(conv)
    response = requests.post((server + '/corpus_view'), json=s).json()
    return render_template('corpus_view.html', page=page, corpus=(response['corpus']))


@app.route('/corpus_statistic', methods=['GET'])
def corpus_statistic():
    page = 'DeepNLP | Corpus Statistic'
    conv = {'_id': request.args.get('_id')}
    s = json.dumps(conv)
    response = requests.post((server + '/corpus_statistic'), json=s).json()
    if response:
        feature = 'word_cloud'
        wordcloud = create_plot('word_cloud', response['statistics'])
        bar = create_plot('token_frequency_by_class_grammtical', response['statistics'])
        bar_2 = create_plot('token_frequency_by_sentences', response['statistics'])
        return render_template('corpus_statistic.html', page=page,
          corpus=(response['corpus']),
          statistics=(response['statistics']),
          bar=bar,
          bar_2=bar_2,
          wordcloud=wordcloud)


def create_plot(feature, dt):
    x = []
    y = []
    for item in dt['words_frequency']:
        x.append(item['freq'])
        y.append(item['word'])
    else:
        if feature == 'Bar':
            df = pd.DataFrame({'x':x,  'y':y})
            data = [
             go.Bar(x=(df['x']),
               y=(df['y']))]
        else:
            if feature == 'FreqWords':
                trace = {'x':x,  'y':y, 
                 'marker':{'color': 'rgb(84, 172, 234)'}, 
                 'orientation':'h', 
                 'type':'bar'}
                data = Data([trace])
            else:
                if feature == 'token_frequency_by_class_grammtical':
                    fig = go.Figure()
                    for item in dt['post_tag_frequency']:
                        cont = []
                        for _ in range(int(item['freq'])):
                            cont.append(item['pos'])
                        else:
                            fig.add_trace(go.Histogram(x=cont, name=(item['pos'])))

                    else:
                        fig.update_layout(xaxis_title_text='Grammatical Class',
                          yaxis_title_text='Words Frequency',
                          bargap=0.2,
                          bargroupgap=0.1,
                          showlegend=True)
                        data = fig

                else:
                    if feature == 'token_frequency_by_sentences':
                        fig = go.Figure(data=[
                         go.Histogram(x=(dt['tokens_frequency_to_sentences']))])
                        fig.update_layout(xaxis_title_text='Number Tokens',
                          yaxis_title_text='Sentences Frequency',
                          bargap=0.2,
                          bargroupgap=0.1)
                        data = fig
                    else:
                        if feature == 'word_cloud':
                            import random
                            words = y
                            size = 30
                            colors = [plotly.colors.DEFAULT_PLOTLY_COLORS[random.randrange(1, 10)] for i in range(size)]
                            weights = [random.randint(15, 35) for i in range(size)]
                            data = go.Scatter(x=[random.random() for i in range(size)],
                              y=random.choices((range(30)), k=30),
                              mode='text',
                              text=words,
                              marker={'opacity': 0.3},
                              textfont={'size':weights, 
                             'color':colors})
                            layout = go.Layout({'xaxis':{'showgrid':False, 
                              'showticklabels':False,  'zeroline':False}, 
                             'yaxis':{'showgrid':False, 
                              'showticklabels':False,  'zeroline':False}})
                            data = go.Figure(data=[data], layout=layout)
                        else:
                            data = [
                             go.Scatter(x=x,
                               y=y,
                               mode='markers')]
        graphJSON = json.dumps(data, cls=(plotly.utils.PlotlyJSONEncoder))
        return graphJSON


@app.route('/bar', methods=['GET', 'POST'])
def change_features():
    feature = request.args['selected']
    graphJSON = self.create_plot(feature)
    return graphJSON


@app.route('/corpus_analysis', methods=['GET'])
def corpus_analysis():
    page = 'DeepNLP | Corpus Analysis Tools'
    conv = {'_id': request.args.get('_id')}
    s = json.dumps(conv)
    response = requests.post((server + '/corpus_analysis'), json=s).json()
    return render_template('corpus_analysis.html', page=page, annotations=(response['annotations']))


@app.route('/corpus_upload', methods=['GET', 'POST'])
def corpus_upload():
    headers = {'accept': 'application/json'}
    conv = {'path_corpus': request.args.get('path_corpus')}
    s = json.dumps(conv)
    response = requests.post((server + '/corpus_upload'), headers=headers,
      json=s).json()
    return jsonify(response)


@app.route('/corpus_download', methods=['GET'])
def corpus_download():
    headers = {'accept': 'application/json'}
    conv = {'_id': request.args.get('_id')}
    s = json.dumps(conv)
    response = requests.post((server + '/corpus_download'), headers=headers,
      json=s).json()
    generator = (cell for row in response['sentences'] for cell in row + '\n')
    file_name = response['name']
    return Response(generator,
      mimetype='text/txt',
      headers={'Content-Disposition': 'attachment; filename=' + file_name + '.txt'})


@app.route('/corpus_delete', methods=['GET'])
def corpus_delete():
    headers = {'accept': 'application/json'}
    conv = {'_id': request.args.get('_id')}
    s = json.dumps(conv)
    response = requests.post((server + '/corpus_delete'), headers=headers,
      json=s).json()
    return jsonify(response)


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/configurations')
def configurations():
    return render_template('configurations.html')