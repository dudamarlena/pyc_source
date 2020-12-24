# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\transport_network_analysis\plot.py
# Compiled at: 2019-03-20 04:50:42
# Size of source mod 2**32: 13842 bytes
import pandas as pd, numpy as np, datetime
from plotly.offline import init_notebook_mode, iplot
import plotly.graph_objs as go
import matplotlib.pyplot as plt
import pyproj, shapely.geometry
from simplekml import Kml, Style
import networkx as nx

def vessel_planning(vessels, activities, colors, web=False):
    """create a plot of the planning of vessels"""

    def get_segments(series, activity, y_val):
        """extract 'start' and 'stop' of activities from log"""
        x = []
        y = []
        for i, v in series.iteritems():
            if v == activity + ' start':
                start = i
            if v == activity + ' stop':
                x.extend((start, start, i, i, i))
                y.extend((y_val, y_val, y_val, y_val, None))

        return (
         x, y)

    dataframes = []
    for vessel in vessels:
        df = pd.DataFrame({'log_value':vessel.log['Value'], 
         'log_string':vessel.log['Message']}, vessel.log['Timestamp'])
        dataframes.append(df)

    df = dataframes[0]
    traces = []
    for i, activity in enumerate(activities):
        x_combined = []
        y_combined = []
        for k, df in enumerate(dataframes):
            y_val = vessels[k].name
            x, y = get_segments((df['log_string']),
              activity=activity, y_val=y_val)
            x_combined.extend(x)
            y_combined.extend(y)

        traces.append(go.Scatter(name=activity,
          x=x_combined,
          y=y_combined,
          mode='lines',
          hoverinfo='y+name',
          line=dict(color=(colors[i]), width=10),
          connectgaps=False))

    layout = go.Layout(title='Vessel planning',
      hovermode='closest',
      legend=dict(x=0, y=(-0.2), orientation='h'),
      xaxis=dict(title='Time',
      titlefont=dict(family='Courier New, monospace',
      size=18,
      color='#7f7f7f'),
      range=[
     0, vessel.log['Timestamp'][(-1)]]),
      yaxis=dict(title='Vessels',
      titlefont=dict(family='Courier New, monospace',
      size=18,
      color='#7f7f7f')))
    init_notebook_mode(connected=True)
    fig = go.Figure(data=traces, layout=layout)
    return iplot(fig, filename='news-source')


def vessel_kml(env, vessels, fname='vessel_movements.kml', icon='http://maps.google.com/mapfiles/kml/shapes/sailing.png', size=1, scale=1, stepsize=120):
    """Create a kml visualisation of vessels. Env variable needs to contain 
        epoch to enable conversion of simulation time to real time. Vessels need
        logs that contain geometries in lat, lon as a function of time."""
    kml = Kml()
    fol = kml.newfolder(name='Vessels')
    shared_style = Style()
    shared_style.labelstyle.color = 'ffffffff'
    shared_style.labelstyle.scale = size
    shared_style.iconstyle.color = 'ffff0000'
    shared_style.iconstyle.scale = scale
    shared_style.iconstyle.icon.href = icon
    for vessel in vessels:
        geom_x = []
        geom_y = []
        for geom in vessel.log['Geometry']:
            geom_x.append(geom.x)
            geom_y.append(geom.y)

        vessel.log['Geometry - x'] = geom_x
        vessel.log['Geometry - y'] = geom_y
        time_stamp_min = min(vessel.log['Timestamp']).timestamp()
        time_stamp_max = max(vessel.log['Timestamp']).timestamp()
        steps = int(np.floor((time_stamp_max - time_stamp_min) / stepsize))
        timestamps_t = np.linspace(time_stamp_min, time_stamp_max, steps)
        times = []
        for t in vessel.log['Timestamp']:
            times.append(t.timestamp())

        vessel.log['timestamps_t'] = timestamps_t
        vessel.log['timestamps_x'] = np.interp(timestamps_t, times, vessel.log['Geometry - x'])
        vessel.log['timestamps_y'] = np.interp(timestamps_t, times, vessel.log['Geometry - y'])
        for log_index, value in enumerate(vessel.log['timestamps_t'][:-1]):
            begin = datetime.datetime.fromtimestamp(vessel.log['timestamps_t'][log_index])
            end = datetime.datetime.fromtimestamp(vessel.log['timestamps_t'][(log_index + 1)])
            pnt = fol.newpoint(name=(vessel.name), coords=[(vessel.log['timestamps_x'][log_index], vessel.log['timestamps_y'][log_index])])
            pnt.timespan.begin = begin.isoformat()
            pnt.timespan.end = end.isoformat()
            pnt.style = shared_style

        begin = datetime.datetime.fromtimestamp(vessel.log['timestamps_t'][(log_index + 1)])
        pnt = fol.newpoint(name=(vessel.name), coords=[(vessel.log['timestamps_x'][(log_index + 1)], vessel.log['timestamps_y'][(log_index + 1)])])
        pnt.timespan.begin = begin.isoformat()
        pnt.style = shared_style

    kml.save(fname)


def site_kml(env, sites, fname='site_development.kml', icon='http://maps.google.com/mapfiles/kml/shapes/square.png', size=1, scale=3, stepsize=120):
    """Create a kml visualisation of vessels. Env variable needs to contain 
        epoch to enable conversion of simulation time to real time. Vessels need
        logs that contain geometries in lat, lon as a function of time."""
    kml = Kml()
    fol = kml.newfolder(name='Sites')
    for site in sites:
        for log_index, value in enumerate(site.log['Timestamp'][:-1]):
            style = Style()
            style.labelstyle.color = 'ffffffff'
            style.labelstyle.scale = 1
            style.iconstyle.color = 'ff00ffff'
            style.iconstyle.scale = scale * (site.log['Value'][log_index] / site.container.capacity)
            style.iconstyle.icon.href = icon
            begin = site.log['Timestamp'][log_index]
            end = site.log['Timestamp'][(log_index + 1)]
            pnt = fol.newpoint(name=(site.name), coords=[
             (site.log['Geometry'][log_index].x,
              site.log['Geometry'][log_index].y)])
            pnt.timespan.begin = begin.isoformat()
            pnt.timespan.end = end.isoformat()
            pnt.style = style

        style = Style()
        style.labelstyle.color = 'ffffffff'
        style.labelstyle.scale = 1
        style.iconstyle.color = 'ff00ffff'
        style.iconstyle.scale = scale * (site.log['Value'][(log_index + 1)] / site.container.capacity)
        style.iconstyle.icon.href = icon
        begin = site.log['Timestamp'][(log_index + 1)]
        pnt = fol.newpoint(name=(site.name), coords=[
         (site.log['Geometry'][(log_index + 1)].x,
          site.log['Geometry'][(log_index + 1)].y)])
        pnt.timespan.begin = begin.isoformat()
        pnt.style = style

    kml.save(fname)


def graph_kml(env, fname='graph.kml', icon='http://maps.google.com/mapfiles/kml/shapes/donut.png', size=0.5, scale=0.5, width=5):
    """Create a kml visualisation of graph. Env variable needs to contain 
        graph."""
    kml = Kml()
    fol = kml.newfolder(name='Vessels')
    shared_style = Style()
    shared_style.labelstyle.color = 'ffffffff'
    shared_style.labelstyle.scale = size
    shared_style.iconstyle.color = 'ffffffff'
    shared_style.iconstyle.scale = scale
    shared_style.iconstyle.icon.href = icon
    shared_style.linestyle.color = 'ff0055ff'
    shared_style.linestyle.width = width
    nodes = list(env.FG.nodes)
    for log_index, value in enumerate(list(env.FG.nodes)[0:-2]):
        pnt = fol.newpoint(name='', coords=[
         (
          nx.get_node_attributes(env.FG, 'geometry')[nodes[log_index]].x,
          nx.get_node_attributes(env.FG, 'geometry')[nodes[log_index]].y)])
        pnt.style = shared_style

    edges = list(env.FG.edges)
    for log_index, value in enumerate(list(env.FG.edges)[0:-2]):
        lne = fol.newlinestring(name='', coords=[
         (
          nx.get_node_attributes(env.FG, 'geometry')[edges[log_index][0]].x,
          nx.get_node_attributes(env.FG, 'geometry')[edges[log_index][0]].y),
         (
          nx.get_node_attributes(env.FG, 'geometry')[edges[log_index][1]].x,
          nx.get_node_attributes(env.FG, 'geometry')[edges[log_index][1]].y)])
        lne.style = shared_style

    kml.save(fname)


def energy_use(vessel, testing=False):
    energy_use_loading = 0
    energy_use_sailing_full = 0
    energy_use_unloading = 0
    energy_use_sailing_empty = 0
    energy_use_waiting = 0
    for i in range(len(vessel.log['Message'])):
        if vessel.log['Message'][i] == 'Energy use loading':
            energy_use_loading += vessel.log['Value'][i]
        elif vessel.log['Message'][i] == 'Energy use sailing full':
            energy_use_sailing_full += vessel.log['Value'][i]
        elif vessel.log['Message'][i] == 'Energy use unloading':
            energy_use_unloading += vessel.log['Value'][i]
        else:
            if vessel.log['Message'][i] == 'Energy use sailing empty':
                energy_use_sailing_empty += vessel.log['Value'][i]

    fig, ax1 = plt.subplots(figsize=[15, 10])
    height = [
     energy_use_loading,
     energy_use_unloading,
     energy_use_sailing_full,
     energy_use_sailing_empty,
     energy_use_waiting]
    labels = ['Loading',
     'Unloading',
     'Sailing full',
     'Sailing empty',
     'Waiting']
    colors = [(0.21568627450980393, 0.49411764705882355, 0.7215686274509804),
     (0.3843137254901961, 0.7529411764705882, 0.47843137254901963),
     (1.0, 0.5882352941176471, 0.0),
     (0.3843137254901961, 0.5529411764705883, 0.47843137254901963),
     (0.48627450980392156, 0.0392156862745098, 0.00784313725490196)]
    positions = np.arange(len(labels))
    ax1.bar(positions, height, color=colors)
    total_use = sum([energy_use_loading,
     energy_use_unloading,
     energy_use_sailing_full,
     energy_use_sailing_empty,
     energy_use_waiting])
    energy_use_unloading += energy_use_loading
    energy_use_sailing_full += energy_use_unloading
    energy_use_sailing_empty += energy_use_sailing_full
    energy_use_waiting += energy_use_sailing_empty
    y = [energy_use_loading,
     energy_use_unloading,
     energy_use_sailing_full,
     energy_use_sailing_empty,
     energy_use_waiting]
    n = [energy_use_loading / total_use,
     energy_use_unloading / total_use,
     energy_use_sailing_full / total_use,
     energy_use_sailing_empty / total_use,
     energy_use_waiting / total_use]
    ax1.plot(positions, y, 'ko', markersize=10)
    ax1.plot(positions, y, 'k')
    for i, txt in enumerate(n):
        x_txt = positions[i] + 0.1
        y_txt = y[i] * 0.95
        ax1.annotate(('{:02.1f}%'.format(txt * 100)), (
         x_txt, y_txt),
          size=12)

    plt.ylabel('Energy useage in KWH', size=12)
    ax1.set_xticks(positions)
    ax1.set_xticklabels(labels, size=12)
    plt.title(('Energy use - {}'.format(vessel.name)), size=15)
    if testing == False:
        plt.show()