# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/nwinter/PycharmProjects/photon_projects/photon_core/photonai/investigator/app/main/controller/helper.py
# Compiled at: 2019-09-11 10:06:06
# Size of source mod 2**32: 3087 bytes
from pymodm.connection import connect
from bson.objectid import ObjectId
from pymongo import DESCENDING
from flask import request
from pymodm.errors import DoesNotExist, ConnectionError, ValidationError
from photonai.processing.results_structure import MDBHyperpipe, MDBHelper
from ..main import application

def load_pipe_from_db(name):
    try:
        pipe = MDBHyperpipe.objects.order_by([('computation_start_time', DESCENDING)]).raw({'name': name}).first()
        return pipe
    except DoesNotExist as dne:
        return dne


def load_pipe_from_wizard(obj_id):
    try:
        connect('mongodb://trap-umbriel:27017/photon_results', alias='photon_core')
        pipe = MDBHyperpipe.objects.order_by([('computation_start_time', DESCENDING)]).raw({'wizard_object_id': ObjectId(obj_id)}).first()
        return pipe
    except DoesNotExist as dne:
        return dne


def load_pipe(storage, name):
    pipe = None
    error = 'Could not load pipeline'
    if storage == 'm':
        try:
            pipe = load_pipe_from_db(name)
        except ValueError as exc:
            connect((application.config['mongo_db_url']), alias='photon_core')
            pipe = load_pipe_from_db(name)

    if storage == 'w':
        pipe = load_pipe_from_wizard(name)
    else:
        if storage == 'a':
            try:
                pipe = application.config['pipe_objects'][name]
            except KeyError as ke:
                error = ke

    if storage == 'f':
        try:
            pipe_path = application.config['pipe_files'][name]
            pipe = MDBHelper.load_results(pipe_path)
        except KeyError as ke:
            error = ke
        except Exception as e:
            debug = True

        return pipe or error
    else:
        return pipe


def shutdown_server():
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()


def load_mongo_pipes(available_pipes):
    try:
        pipeline_list = list(MDBHyperpipe.objects.all())
        for item in pipeline_list:
            available_pipes['MONGO'].append(item.pk)

    except ValidationError as exc:
        return exc
    except ConnectionError as exc:
        return exc


def load_available_pipes():
    available_pipes = None
    return available_pipes