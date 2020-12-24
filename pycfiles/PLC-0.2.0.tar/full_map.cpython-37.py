# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/fsuba/Pictures/plbmng-0.3.7/plbmng/lib/full_map.py
# Compiled at: 2019-04-30 03:47:16
# Size of source mod 2**32: 2602 bytes
import pandas as pd
from vincent import Visualization, Scale, DataRef, Data, PropertySet, Axis, ValueRef, MarkRef, MarkProperties, Mark
import json, folium, csv

def plot_server_on_map(nodes=None):
    """
    Creates a map of every known node and generates chart with information about their's latency.

    :return: map_full.html file
    """
    df = pd.DataFrame({'Data 1':[1, 2, 3, 4, 5, 6, 7, 12],  'Data 2':[
      42, 27, 52, 18, 61, 19, 62, 33]})
    vis = Visualization(width=500, height=300)
    vis.padding = {'top':10,  'left':50,  'bottom':50,  'right':100}
    vis.data.append(Data.from_pandas(df, columns=['Data 2'], key_on='Data 1', name='table'))
    vis.scales.append(Scale(name='x', type='ordinal', range='width', domain=DataRef(data='table', field='data.idx')))
    vis.scales.append(Scale(name='y', range='height', nice=True, domain=DataRef(data='table', field='data.val')))
    vis.axes.extend([Axis(type='x', scale='x'), Axis(type='y', scale='y')])
    enter_props = PropertySet(x=ValueRef(scale='x', field='data.idx'), y=ValueRef(scale='y', field='data.val'),
      width=ValueRef(scale='x', band=True, offset=(-1)),
      y2=ValueRef(scale='y', value=0))
    update_props = PropertySet(fill=ValueRef(value='steelblue'))
    mark = Mark(type='rect', from_=MarkRef(data='table'), properties=MarkProperties(enter=enter_props, update=update_props))
    vis.marks.append(mark)
    vis.axis_titles(x='days', y='latency [ms]')
    vis.to_json('vega.json')
    map_full = folium.Map(location=[45.372, -121.6972], zoom_start=2)
    for node in nodes:
        name = node[2]
        if not node[(-2)] == 'unknown':
            if node[(-1)] == 'unknown':
                continue
            x = float(node[(-2)])
            y = float(node[(-1)])
            text = '\n            NODE: %s, IP: %s\n            URL: %s\n            FULL NAME: %s\n            LATITUDE: %s, LONGITUDE: %s\n            ' % (node[2],
             node[1],
             node[7],
             node[8],
             node[9],
             node[10])
            popup = folium.Popup((text.strip().replace('\n', '<br>')), max_width=1000)
            folium.Marker([x, y], popup=popup).add_to(map_full)

    map_full.save('plbmng_server_map.html')


if __name__ == '__main__':
    plot_server_on_map()