# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: D:\Benutzer\haschtl\Dokumente\GIT\kellerlogger\RTOC\RTLogger\RTOC_Web_standalone.py
# Compiled at: 2019-06-12 22:05:11
# Size of source mod 2**32: 12892 bytes
"""
This is executed with `python3 -m RTOC.RTLogger -w`, if postgresql is active

This code is not documented. Read the Webserver documentation for more information: :doc:`WEBSERVER`

"""
import dash, dash_html_components as html, dash_core_components as dcc, dash_table, plotly, dash_daq as daq
from dash.dependencies import Input, Output, State
import time, datetime, logging as log
from gevent.pywsgi import WSGIServer
from flask import Flask
import copy
log.basicConfig(level=(log.WARNING))
logging = log.getLogger(__name__)
try:
    from PyQt5.QtCore import QCoreApplication
    translate = QCoreApplication.translate
except ImportError:

    def translate(id, text):
        return text


def _(text):
    return translate('web', text)


external_stylesheets = [
 'https://codepen.io/chriddyp/pen/bWLwgP.css']
server = Flask(__name__)
app = dash.Dash(__name__, external_stylesheets=external_stylesheets, sharing=True, server=server,
  url_base_pathname='/',
  csrf_protect=False)
app.config['suppress_callback_exceptions'] = True
eventTableTitle = [
 translate('RTOC', 'Time'), translate('RTOC', 'Type'), translate('RTOC', 'Device'), translate('RTOC', 'Signal'), translate('RTOC', 'Content'), translate('RTOC', 'ID'), translate('RTOC', 'Return')]
from .RT_data import RT_data
app.layout = html.Div([
 dcc.Tabs(id='tabs', children=[
  dcc.Tab(label=(translate('RTOC', 'Signals')), children=[
   html.Div([
    html.Div([
     dcc.Checklist(id='activeCheck',
       options=[
      {'label':translate('RTOC', 'Plot active'), 
       'value':'PLOT'}],
       values=[
      'PLOT']),
     daq.NumericInput(id='my-numeric-input',
       min=1,
       max=100000000,
       value=100),
     dcc.Dropdown(id='signal_dropdown',
       options=[],
       searchable=True,
       clearable=True,
       placeholder=(translate('RTOC', 'Select signals to be displayed.')),
       multi=True)],
      className='row'),
    dcc.Graph(id='live-update-graph'),
    dcc.Interval(id='interval-component',
      interval=60000,
      n_intervals=0)],
     id='signals_div')]),
  dcc.Tab(label=(translate('RTOC', 'Events')), children=[
   dash_table.DataTable(id='datatable-interactivity',
     columns=[{'name':i,  'id':i} for i in eventTableTitle],
     editable=False,
     filtering=True,
     sorting=True,
     pagination_mode='fe',
     pagination_settings={'displayed_pages':1, 
    'current_page':0, 
    'page_size':35},
     navigation='page'),
   dcc.Interval(id='interval-component2',
     interval=60000,
     n_intervals=0),
   html.Div(id='datatable-interactivity-container', style={'height': '100vh'})])])])
signals = [
 [
  [
   1, 2, 3, 4, 5], [4, 3, 2, 6, 7], 'Sensor.Temperature', '°C'],
 [
  [
   1, 2, 3, 4, 5], [4, 3, 2, 6, 7], 'Sensor.Humidity', '%'],
 [
  [
   1, 2, 3, 4, 5], [4, 3, 2, 6, 7], 'Sensor.Temperature3', '°C'],
 [
  [
   1, 2, 3, 4, 5], [4, 3, 2, 6, 7], 'Sensor.CO2', 'ppm'],
 [
  [
   1, 2, 3, 4, 5], [4, 3, 2, 6, 7], 'Sensor.Temperature2', '°C']]
events = [
 [
  'today', 'Warning', 'Sensor', 'Temperature', 'Temperature too high', '34666', '3']]
lastSignals = []
run = False
samplerate = 1
database = RT_data()
if database is None:
    logging.warning('No database connected to RTOC_Web')
    app.title = 'RTOC-Web'
else:
    app.title = database.config['global']['name']

def start(debug=False):
    global database
    global run
    run = True
    try:
        print('Starting webserver')
        try:
            port = database.config['global']['webserver_port']
        except Exception:
            port = 8050

        http_server = WSGIServer(('0.0.0.0', port), app.server)
        http_server.serve_forever()
    except KeyboardInterrupt:
        run = False
        database.close()
        logging.info('Server killed by user.')
    except Exception:
        logging.error('Webserver crashed!')


def stop():
    global run
    if run:
        run = False
    else:
        logging.warning('HTML-Server was not started. Could not stop')


@app.callback(dash.dependencies.Output('signal_dropdown', 'options'), [
 dash.dependencies.Input('interval-component', 'n_intervals')])
def update_date_dropdown(n_intervals):
    new_signals = []
    for sigID in database.signals().keys():
        name = database.getSignalName(sigID)
        unit = database.signals()[sigID][4]
        signame = '.'.join(name)
        new_signals.append([signame, unit])

    signals = new_signals
    return [{'label':i[0] + '[' + i[1] + ']',  'value':i[0]} for i in signals]


last_now = time.time()

@app.callback((Output('live-update-graph', 'figure')), [
 Input('interval-component', 'n_intervals')],
  state=[
 State('live-update-graph', 'figure'), State('activeCheck', 'values'),
 State('live-update-graph', 'relayoutData'), State('signal_dropdown', 'value'),
 State('my-numeric-input', 'value')])
def update_graph_live(n_intervals, lastPlot, active, relayout_data, selection, maxlength):
    global lastSignals
    global last_now
    if active == ['PLOT']:
        now = time.time()
        last_now = now
    else:
        now = last_now
    new_signals = []
    for sigID in database.signals().keys():
        signal = copy.deepcopy(database.signals()[sigID])
        name = database.getSignalName(sigID)
        unit = database.signals()[sigID][4]
        signame = '.'.join(name)
        if len(signal[2]) > 0:
            x = list(signal[2])
            y = list(signal[3])
            if len(x) != len(y):
                x = []
                y = []
                break
            if len(x) > maxlength:
                start = len(x) - maxlength
                x = x[start:-1]
                y = y[start:-1]
            if x[0] > 0:
                for idx, value in enumerate(x):
                    x[idx] = datetime.datetime.fromtimestamp(x[idx]).strftime('%Y-%m-%d %H:%M:%S')

            signame = '.'.join(name)
            new_signals.append([x, y, signame, unit])

    signals = new_signals
    sorted = {}
    if selection is None:
        selection = []
    else:
        if active == ['PLOT']:
            sig = signals
            lastSignals = signals
        else:
            sig = lastSignals
        for signal in sig:
            if signal[2] in selection:
                if signal[3] not in sorted.keys():
                    sorted[signal[3]] = []
                sorted[signal[3]].append(signal[0:3])

        if len(sorted) == 0:
            greater1 = 1
        else:
            greater1 = len(sorted)
    fig = plotly.tools.make_subplots(rows=greater1, cols=1, vertical_spacing=0.2)
    fig['layout']['margin'] = {'l':30, 
     'r':10,  'b':30,  't':10}
    fig['layout']['legend'] = {'x':0, 
     'y':1,  'xanchor':'left'}
    for idx, unit in enumerate(sorted.keys()):
        for signal in sorted[unit]:
            fig.append_trace({'x':signal[0], 
             'y':signal[1], 
             'name':signal[2] + ' [' + unit + ']', 
             'mode':'lines+markers', 
             'type':'scatter'}, idx + 1, 1)

        fig['layout'][('yaxis' + str(idx + 1))].update(title=('[' + unit + ']'), showgrid=True)
        fig['layout'][('xaxis' + str(idx + 1))].update(title=(translate('RTOC', 'Elapsed time [s]')), showgrid=True)
        fig['layout'][('xaxis' + str(idx + 1))]['tickformat'] = '%d.%m %H:%M'
        if relayout_data:
            if 'xaxis' + str(idx + 1) + '.range[0]' in relayout_data:
                fig['layout'][('xaxis' + str(idx + 1))]['range'] = [relayout_data[('xaxis' + str(idx + 1) + '.range[0]')],
                 relayout_data[('xaxis' + str(idx + 1) + '.range[1]')]]
            if 'yaxis' + str(idx + 1) + '.range[0]' in relayout_data:
                fig['layout'][('yaxis' + str(idx + 1))]['range'] = [relayout_data[('yaxis' + str(idx + 1) + '.range[0]')],
                 relayout_data[('yaxis' + str(idx + 1) + '.range[1]')]]
        if idx == 0:
            fig['layout']['xaxis']['tickformat'] = '%d.%m %H:%M'
            fig['layout']['yaxis'].update(title=('[' + unit + ']'), showgrid=True)
            fig['layout']['xaxis'].update(title=(translate('RTOC', 'Elapsed time [s]')), showgrid=True)
            if relayout_data:
                if 'xaxis.range[0]' in relayout_data:
                    fig['layout']['xaxis']['range'] = [relayout_data['xaxis.range[0]'],
                     relayout_data['xaxis.range[1]']]
                if 'yaxis.range[0]' in relayout_data:
                    fig['layout']['yaxis']['range'] = [relayout_data['yaxis.range[0]'],
                     relayout_data['yaxis.range[1]']]

    return fig


@app.callback(Output('datatable-interactivity', 'data'), [
 Input('interval-component2', 'n_intervals')])
def update_output(n_intervals):
    data = []
    for evID in database.events().keys():
        event = database.events()[evID]
        name = database.getEventName(evID)
        event_dict = {}
        event_dict[eventTableTitle[0]] = datetime.datetime.fromtimestamp(event[4]).strftime('%Y-%m-%d %H:%M:%S:%f')
        if event[6] == 0:
            text = translate('RTOC', 'Information')
        else:
            if event[6] == 1:
                text = translate('RTOC', 'Warning')
            else:
                text = translate('RTOC', 'Error')
        event_dict[eventTableTitle[1]] = text
        event_dict[eventTableTitle[2]] = name[0]
        event_dict[eventTableTitle[3]] = name[1]
        event_dict[eventTableTitle[4]] = event[3]
        event_dict[eventTableTitle[6]] = event[2]
        event_dict[eventTableTitle[5]] = event[5]
        data.append(event_dict)

    return data