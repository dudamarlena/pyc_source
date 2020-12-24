# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /mnt/develop/NodeDefender/NodeDefender/frontend/views/data.py
# Compiled at: 2018-01-09 06:06:44
# Size of source mod 2**32: 2571 bytes
from NodeDefender.frontend.views import data_view
from flask import request, render_template
from flask_login import login_required, current_user
import NodeDefender

@data_view.route('/data/power')
@login_required
def data_power():
    if request.method == 'GET':
        groups = NodeDefender.db.group.list(current_user.email)
        return render_template('frontend/data/power.html', groups=groups)


@data_view.route('/data/power/group/<name>')
@login_required
def power_group(name):
    name = NodeDefender.serializer.loads(name)
    if request.method == 'GET':
        group = NodeDefender.db.group.get(name)
        if group is None:
            pass
        return render_template('frontend/data/group/power.html', group=group)


@data_view.route('/data/power/node/<name>')
@login_required
def power_node(name):
    name = NodeDefender.serializer.loads(name)
    if request.method == 'GET':
        node = NodeDefender.db.node.get(name)
        return render_template('frontend/data/node/power.html', node=node)


@data_view.route('/data/power/sensor/<icpe>/<sensor>')
@login_required
def power_sensor(icpe, sensor):
    icpe = NodeDefender.serializer.loads(icpe)
    if request.method == 'GET':
        sensor = NodeDefender.db.sensor.get(icpe, sensor)
        return render_template('frontend/data/sensor/power.html', sensor=sensor)


@data_view.route('/data/heat')
@login_required
def data_heat():
    if request.method == 'GET':
        groups = NodeDefender.db.group.list(current_user.email)
        return render_template('frontend/data/heat.html', groups=groups)


@data_view.route('/data/heat/group/<name>')
@login_required
def heat_group(name):
    name = NodeDefender.serializer.loads(name)
    if request.method == 'GET':
        group = NodeDefender.db.group.get(name)
        if group is None:
            pass
        return render_template('frontend/data/group/heat.html', group=group)


@data_view.route('/data/heat/node/<name>')
@login_required
def heat_node(name):
    name = NodeDefender.serializer.loads(name)
    if request.method == 'GET':
        node = NodeDefender.db.node.get(name)
        return render_template('frontend/data/node/heat.html', node=node)


@data_view.route('/data/heat/sensor/<icpe>/<sensor>')
@login_required
def heat_sensor(icpe, sensor):
    icpe = NodeDefender.serializer.loads(icpe)
    if request.method == 'GET':
        sensor = NodeDefender.db.sensor.get(icpe, sensor)
        return render_template('frontend/data/sensor/heat.html', sensor=sensor)