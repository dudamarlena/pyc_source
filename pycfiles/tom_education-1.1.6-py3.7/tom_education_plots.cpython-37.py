# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/tom_education/templatetags/tom_education_plots.py
# Compiled at: 2020-05-01 08:14:06
# Size of source mod 2**32: 1088 bytes
from plotly import offline
import plotly.graph_objs as go
from django import template
import json
from astropy.time import Time
from tom_targets.models import Target
register = template.Library()

@register.inclusion_tag('tom_targets/partials/target_photometry.html')
def targets_reduceddata(targetid):
    target = Target.objects.get(id=targetid)
    x = []
    y = []
    for rd in target.reduceddatum_set.all():
        try:
            data = json.loads(rd.value)
        except json.JSONDecodeError:
            continue

        print(rd.timestamp.isoformat())
        x.append(rd.timestamp.isoformat())
        y.append(data['magnitude'])

    data = [
     go.Scatter(x=x, y=y, mode='markers')]
    fig = go.Figure(data=data)
    fig.update_yaxes(autorange='reversed')
    figure = offline.plot(fig, output_type='div', show_link=False)
    return {'figure': figure}