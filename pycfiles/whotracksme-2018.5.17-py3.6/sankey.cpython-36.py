# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/whotracksme/website/plotting/sankey.py
# Compiled at: 2018-05-17 05:30:15
# Size of source mod 2**32: 1187 bytes
from whotracksme.website.plotting.utils import div_output, set_margins
from whotracksme.website.plotting.colors import cliqz_colors

def sankey_plot(sndata):
    data_trace = dict(type='sankey',
      domain=dict(x=[
     0, 1],
      y=[
     0, 1]),
      hoverinfo='none',
      orientation='h',
      node=dict(pad=10,
      thickness=30,
      label=(list(map(lambda x: x.replace('_', ' ').capitalize(), sndata['node']['label']))),
      color=(sndata['node']['color'])),
      link=dict(source=(sndata['link']['source']),
      target=(sndata['link']['target']),
      value=(sndata['link']['value']),
      label=(sndata['link']['label']),
      color=['#dedede' for _ in range(len(sndata['link']['source']))]))
    layout = dict(height=(max(len(sndata['link']['source']) * 13, 400)),
      font=dict(size=12),
      autosize=True,
      margin=set_margins(t=20, l=2, r=2))
    fig = dict(data=[data_trace], layout=layout)
    return div_output(fig)