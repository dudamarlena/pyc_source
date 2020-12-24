# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/apryor/projects/flaskerize/d/app/main/view.py
# Compiled at: 2019-08-26 10:32:50
# Size of source mod 2**32: 811 bytes
from flask import Blueprint, render_template, request, jsonify
bp = Blueprint('main', __name__, template_folder='templates')

def make_chart(title):
    import json
    import plotly.graph_objects as go
    import plotly
    layout = go.Layout(title=title)
    data = go.Scatter(x=[
     1, 2, 3, 4],
      y=[
     10, 11, 12, 13],
      mode='markers',
      marker=dict(size=[40, 60, 80, 100], color=[0, 1, 2, 3]))
    fig = go.Figure(data=data)
    fig = json.dumps(fig, cls=(plotly.utils.PlotlyJSONEncoder))
    layout = json.dumps(layout, cls=(plotly.utils.PlotlyJSONEncoder))
    return (fig, layout)


@bp.route('/', methods=['GET', 'POST'])
def route():
    message = ''
    fig, layout = make_chart(title='Test title')
    return render_template('plotly-chart.html', fig=fig, layout=layout)