# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/nailixing/PyProjects/nusdb_rafiki/singa_auto/admin/view/events.py
# Compiled at: 2020-04-15 05:36:06
# Size of source mod 2**32: 1659 bytes
from flask import jsonify, Blueprint, g
from singa_auto.utils.auth import auth
from singa_auto.utils.requests_params import param_check
events_bp = Blueprint('events', __name__)

@events_bp.route('/actions/stop_all_jobs', methods=['POST'])
@auth([])
def stop_all_jobs(auth):
    admin = g.admin
    with admin:
        train_jobs = admin.stop_all_train_jobs()
        inference_jobs = admin.stop_all_inference_jobs()
        return jsonify({'train_jobs':train_jobs, 
         'inference_jobs':inference_jobs})


@events_bp.route('/event/<name>', methods=['POST'])
@auth([])
@param_check(required_parameters={})
def handle_event(auth, params, name):
    admin = g.admin
    with admin:
        return jsonify((admin.handle_event)(name, **params))