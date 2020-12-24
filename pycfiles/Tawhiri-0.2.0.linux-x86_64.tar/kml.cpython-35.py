# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python3.5/site-packages/tawhiri/kml.py
# Compiled at: 2016-11-26 12:39:04
# Size of source mod 2**32: 589 bytes
import jinja2
loader = jinja2.PackageLoader('tawhiri', '')
env = jinja2.Environment(loader=loader, extensions=[
 'jinja2.ext.autoescape'], undefined=jinja2.StrictUndefined)
template = env.get_template('template.kml')

def kml(stages, markers, filename=None):
    points = stages[0]
    for stage in stages[1:]:
        assert points[(-1)] == stage[0]
        points += stage[1:]

    kwargs = {'points': points, 'markers': markers}
    if filename:
        template.stream(**kwargs).dump(filename)
    else:
        template.render(**kwargs)