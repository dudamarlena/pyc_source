# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\ResultDashboard\Dashboard\DashPlot.py
# Compiled at: 2020-02-26 12:02:30
# Size of source mod 2**32: 3931 bytes
import plotly.graph_objects as go

class LinePlot:

    def __init__(self, DataDict, ylabel='', title=''):
        self.plot = []
        for keys, values in DataDict.items():
            if keys != 'x_val' and keys != 'Scenarios':
                self.plot.append(go.Scatter(x=(DataDict['x_val']), y=values, mode='lines+markers', name=keys, marker={'size': 10}))

        self.plot_layout = go.Layout(plot_bgcolor='#1e2130', paper_bgcolor='#1e2130',
          font={'color': '#7FDBFF'},
          xaxis={'tickvals':DataDict['x_val'], 
         'ticktext':DataDict['Scenarios'],  'showgrid':False,  'zerolinewidth':0.5},
          yaxis={'title':ylabel, 
         'showgrid':False,  'zerolinewidth':0.5},
          title=title,
          legend={'orientation':'h', 
         'y':1.2},
          margin=dict(r=20, t=60))

    def layout(self):
        return go.Figure(data=(self.plot), layout=(self.plot_layout))


class TimeSeriesLinePlot:

    def __init__(self, DataDict, stack=False, ylabel='', title='', marker={'size': 10}, mode='lines+markers'):
        self.plot = []
        for keys, values in DataDict.items():
            if keys != 'TimeStamp':
                if stack == True:
                    self.plot.append(go.Scatter(x=(DataDict['TimeStamp']), y=values, mode=mode, name=keys, marker=marker,
                      stackgroup='one'))
                else:
                    self.plot.append(go.Scatter(x=(DataDict['TimeStamp']), y=values, mode=mode, name=keys, marker={'size': 10}))

        self.plot_layout = go.Layout(plot_bgcolor='#1e2130', paper_bgcolor='#1e2130',
          font={'color': '#7FDBFF'},
          xaxis={'showgrid':False, 
         'zerolinewidth':0.5},
          yaxis={'title':ylabel, 
         'showgrid':False,  'zerolinewidth':0.5},
          title=title,
          legend={'orientation':'h', 
         'y':1.2},
          margin=dict(r=20, t=60))

    def layout(self):
        return go.Figure(data=(self.plot), layout=(self.plot_layout))


class GeoScatterMap:

    def __init__(self, NetworkDatalat, NetworkDatalatlon, ScatterDatax, ScatterDatay, centerx, centery, marker={'color':'#FF0000', 
 'opacity':1.0,  'size':10}, hoverinfo='all', hovertext='', height=400, zoom=13):
        self.plot = [
         go.Scattermapbox(lat=NetworkDatalat, lon=NetworkDatalatlon, mode='lines', line=dict(width=1.5, color='#FFFF00')),
         go.Scattermapbox(lat=ScatterDatax, lon=ScatterDatay, mode='markers',
           marker=marker,
           hovertext=hovertext,
           hoverinfo=hoverinfo)]
        self.plot_layout = go.Layout(autosize=True, height=height,
          margin=go.layout.Margin(l=0, r=0, t=0, b=0),
          mapbox=dict(center=dict(lat=centerx, lon=centery),
          style='carto-darkmatter',
          zoom=zoom),
          plot_bgcolor='#171b26',
          paper_bgcolor='#171b26',
          showlegend=False)

    def layout(self):
        return go.Figure(data=(self.plot), layout=(self.plot_layout))