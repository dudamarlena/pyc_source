# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /media/bkvaluemeal/Iron Bank/libenable/libenable/blueprints/api.py
# Compiled at: 2017-05-17 23:01:22
# Size of source mod 2**32: 4147 bytes
"""
RESTful API

This module defines the Flask blueprint for the RESTful API. See the
documentation for each object and their respective unit tests for more
information.
"""
from flask import Blueprint, render_template, request
from flask_restful import reqparse, Api, Resource
from libenable import internet
import json, libenable, sqlite3, sys, time
blueprint = Blueprint('api', __name__, template_folder='../templates')
api = Api(blueprint)

class Version(Resource):
    __doc__ = '\n\tReturns the version of the application\n\t'

    def get(self):
        return {'version': libenable.__version__}


class Statistics(Resource):
    __doc__ = '\n\tReturns statistics about the application and the Python interpreter\n\t'

    def get(self):
        return {'libenable': {'status': libenable.__status__.name, 
                       'running_tasks': libenable.__running_tasks__, 
                       'total_tasks': libenable.__total_tasks__, 
                       'status_code': libenable.__status__.value, 
                       'version': libenable.__version__}, 
         
         'python': {'platform': sys.platform, 
                    'version': '%i.%i.%i' % sys.version_info[:3]}, 
         
         'time': {'current': int(time.time()), 
                  'running': int(time.time()) - libenable.__start_time__, 
                  'start': libenable.__start_time__}}


class reCAPTCHA(Resource):
    __doc__ = '\n\tEnables access to reCAPTCHA protected domains\n\t'
    parser = reqparse.RequestParser()
    parser.add_argument('site_key', required=True)
    parser.add_argument('url', required=True)

    def post(self):
        args = self.parser.parse_args()
        agents = {}
        for key in libenable.config.sections():
            data = dict(libenable.config._sections[key])
            if all(value for value in data.values()):
                agents[key.lower()] = data

        if not agents:
            return {'result': None, 
             'error': 'No Agent defined'}
        for _ in range(5):
            result = internet.access_reCAPTCHA(args['site_key'], args['url'], **agents)
            with sqlite3.connect(libenable.__db__) as (database):
                database.cursor().execute('INSERT INTO activity_log (`origin`, `type`, `cost`)VALUES ("%s", "reCAPTCHA", %f)' % (
                 request.remote_addr, result[1]))
                database.commit()
            if result[0]['result']:
                return result[0]
        else:
            return {'result': None, 
             'error': 'Could not obtain access token'}


class SolveMedia(Resource):
    __doc__ = '\n\tEnables access to Solve Media protected domains\n\t'
    parser = reqparse.RequestParser()
    parser.add_argument('site_key', required=True)

    def post(self):
        args = self.parser.parse_args()
        agents = {}
        for key in libenable.config.sections():
            data = dict(libenable.config._sections[key])
            if all(value for value in data.values()):
                agents[key.lower()] = data

        if not agents:
            return {'result': None, 
             'error': 'No Agent defined'}
        for _ in range(5):
            result = internet.access_solve_media(args['site_key'], **agents)
            with sqlite3.connect(libenable.__db__) as (database):
                database.cursor().execute('INSERT INTO activity_log (`origin`, `type`, `cost`)VALUES ("%s", "Solve Media", %f)' % (
                 request.remote_addr, result[1]))
                database.commit()
            if result[0]['result']:
                return result[0]
        else:
            return {'result': None, 
             'error': 'Could not obtain access token'}


@blueprint.route('/')
def show():
    """
        The documentation for the API
        """
    return render_template('api.html', host=libenable.__host__, port=libenable.__port__, version=json.dumps(Version().get(), sort_keys=False, indent=2), stats=json.dumps(Statistics().get(), sort_keys=False, indent=2), reCAPTCHA=json.dumps({'result': '03AHJ_VusHdHs4pPNqGC95gyF...I5WsvJLzjwD-j4wFrUAaxju7o'}, sort_keys=False, indent=2), solve_media=json.dumps({'result': {'response': 'agree to disagree', 
                'challenge': '2@mlFwzmfg.OLZWwwByqjR...HEedbHGOTFGZrJkhFXIK0uoA'}}, sort_keys=False, indent=2))


api.add_resource(Version, '/version')
api.add_resource(Statistics, '/statistics')
api.add_resource(reCAPTCHA, '/reCAPTCHA')
api.add_resource(SolveMedia, '/solvemedia')