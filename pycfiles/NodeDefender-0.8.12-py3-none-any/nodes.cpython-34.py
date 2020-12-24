# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /mnt/develop/NodeDefender/NodeDefender/frontend/views/nodes.py
# Compiled at: 2018-01-09 06:06:44
# Size of source mod 2**32: 4906 bytes
from NodeDefender.frontend.views import node_view
from flask import render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from NodeDefender.frontend.forms.node import LocationForm, iCPEForm, SensorForm, NodeCreateForm
import NodeDefender

@node_view.route('/nodes/list', methods=['GET', 'POST'])
@login_required
def nodes_list():
    if request.method == 'GET':
        groups = NodeDefender.db.group.list(current_user.email)
        nodes = NodeDefender.db.node.list(*[group.name for group in groups])
        if current_user.superuser:
            nodes = nodes + NodeDefender.db.node.unassigned()
        return render_template('frontend/nodes/list.html', nodes=nodes)
    else:
        CreateForm.validate_on_submit()
        try:
            node = NodeSQL.Create(CreateForm.Name.data, location)
            NodeDefender.db.node.location(CreateForm.Name.data, CreateForm.Street.data, CreateForm.City.data)
            iCPE = NodeDefender.db.icpe.get_sql(CreateForm.Mac.data)
            if iCPE:
                NodeDefender.db.node.add_icpe(node.name, iCPE.mac_address)
            if CreateForm.Group.data:
                NodeDefender.db.group.add_node(CreateForm.Group.data, node.name)
        except LookupError as e:
            flash('Error Creating Node: ' + str(e), 'danger')
            return redirect(url_for('node_view.NodesList'))

        url = url_for('node_view.nodes_node', name=NodeDefender.serializer.dumps(node.name))
        flash('Succesfully added node: ' + node.name, 'success')
        return redirect(url)


@node_view.route('/nodes/<name>', methods=['GET', 'POST'])
@login_required
def nodes_node(name):
    name = NodeDefender.serializer.loads(name)
    node = NodeDefender.db.node.get(name)
    if request.method == 'GET':
        return render_template('frontend/nodes/node.html', Node=node)
    if icpeform.Submit.data and icpeform.validate_on_submit():
        icpe.alias = BasicForm.alias.data
        icpe.comment = BasicForm.comment.data
    elif locationform.Submit.data:
        if locationform.validate_on_submit():
            icpe.location.street = AddressForm.street.data
            icpe.location.city = AddressForm.city.data
            icpe.location.geolat = AddressForm.geolat.data
            icpe.location.geolong = AddressForm.geolong.data
    db.session.add(icpe)
    db.session.commit()
    return render_template('frontend/nodes/node.html', Node=node)