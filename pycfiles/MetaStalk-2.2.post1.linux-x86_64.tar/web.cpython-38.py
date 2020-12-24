# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python3.8/site-packages/MetaStalk/utils/web.py
# Compiled at: 2020-05-08 18:09:31
# Size of source mod 2**32: 1970 bytes
"""Uses dash to create a webpage that contain all the graphs"""
import timeit, logging, webbrowser
from datetime import datetime
import dash, dash_html_components as html, dash_core_components as dcc
log = logging.getLogger('MetaStalk')

def graph(plots: dict, t_start: float, test: bool, no_open: bool):
    """graph

    Displays all the plots that are passed to it.

    Arguments:
        plots {dict} -- All the plot that get displayed
        t_start {float} -- The start time of MetaStalk
        test {bool} -- Whether or not to start web server (default: {False})
        no_open {bool} -- Whether or now to open with the browser (default: {False})
    """
    graphs = []
    for name, chart in plots.items():
        graphs.append(dcc.Graph(id=('graph-{}'.format(name)), figure=chart))
    else:
        external_stylesheets = [
         'https://codepen.io/chriddyp/pen/bWLwgP.css']
        app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
        app.logger.disabled = True
        app.title = 'MetaStalk'
        t_stop = timeit.default_timer()
        app.layout = html.Div([
         html.H1('MetaStalk', style={'textAlign': 'center'}),
         html.H6(html.A('Cyber Jake', href='https://twitter.com/Cyb3r_Jak3'), style={'textAlign': 'center'}),
         html.Div(children=graphs),
         html.Footer(('Time Taken = {0:.2f} seconds'.format(t_stop - t_start)), style={'textAlign': 'right'}),
         html.Footer(f"Run Time: {datetime.now().strftime('%m/%d/%Y, %H:%M:%S')}")])
        if not test:
            if not no_open:
                webbrowser.open('http://localhost:8052', new=2)
            app.run_server(port=8052)
        else:
            log.info('Test flag was set. No webpage will be shown.')
            log.info('Time Taken = {0:.2f} seconds'.format(t_stop - t_start))