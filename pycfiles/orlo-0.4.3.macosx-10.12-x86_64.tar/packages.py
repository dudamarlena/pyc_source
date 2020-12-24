# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/site-packages/orlo/routes/packages.py
# Compiled at: 2017-05-17 09:41:21
from __future__ import print_function
from flask import jsonify, request, Response, json, g
from orlo.app import app
from orlo import queries
from orlo.exceptions import InvalidUsage
from orlo.user_auth import token_auth
from orlo.orm import db, Release, Package, PackageResult, ReleaseNote, ReleaseMetadata, Platform
from orlo.util import validate_request_json, create_release, validate_release_input, validate_package_input, fetch_release, create_package, fetch_package, stream_json_list, str_to_bool, is_uuid
from orlo.user_auth import conditional_auth
__author__ = 'alforbes'

@app.route('/packages', methods=['GET'])
@app.route('/packages/<package_id>', methods=['GET'])
def get_packages(package_id=None):
    """
    Return a list of packages to the client

    :param package_id:
    :return:
    """
    booleans = ('rollback', )
    if package_id:
        if not is_uuid(package_id):
            raise InvalidUsage('Package ID given is not a valid UUID')
        query = queries.get_package(package_id)
    else:
        args = {'limit': 100}
        for k in request.args.keys():
            if k in booleans:
                args[k] = str_to_bool(request.args.get(k))
            else:
                args[k] = request.args.get(k)

        query = queries.build_query(Package, **args)
    db.session.execute(query)
    if query.count() == 0:
        response = jsonify(message='No packages found', packages=[])
        return (
         response, 404)
    return Response(stream_json_list('packages', query), content_type='application/json')