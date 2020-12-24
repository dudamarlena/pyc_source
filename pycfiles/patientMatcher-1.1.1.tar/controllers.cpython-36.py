# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/chiararasi/Documents/work/GITs/patientMatcher/patientMatcher/server/controllers.py
# Compiled at: 2019-04-23 03:57:58
# Size of source mod 2**32: 5586 bytes
import logging
from flask import jsonify
from jsonschema import ValidationError
from patientMatcher.constants import STATUS_CODES
from patientMatcher.utils.stats import general_metrics
from patientMatcher.utils.delete import delete_by_query
from patientMatcher.utils.patient import patients
from patientMatcher.parse.patient import json_patient, validate_api, mme_patient
from patientMatcher.auth.auth import authorize
from patientMatcher.match.handler import external_matcher
from patientMatcher.__version__ import __version__
LOG = logging.getLogger(__name__)

def heartbeat(disclaimer):
    """Return a heartbeat as defined here:https://github.com/ga4gh/mme-apis/blob/master/heartbeat-api.md"""
    hbeat = {'heartbeat':{'production':True, 
      'version':__version__, 
      'accept':[
       'application/vnd.ga4gh.matchmaker.v1.0+json', 'application/vnd.ga4gh.matchmaker.v1.1+json']}, 
     'disclaimer':disclaimer}
    return hbeat


def metrics(database):
    """return database metrics"""
    db_metrics = general_metrics(database)
    return db_metrics


def get_nodes(database):
    """Get all connected nodes as a list of objects with node_id and node_label as elements"""
    results = list(database['nodes'].find())
    nodes = []
    for node in results:
        nodes.append({'id':node['_id'],  'description':node['label']})

    return nodes


def patient(database, patient_id):
    """Return a mme-like patient from database by providing its ID"""
    query_patient = None
    query_result = list(patients(database, ids=[patient_id]))
    if query_result:
        query_patient = query_result[0]
    return query_patient


def match_external(database, host, query_patient, node=None):
    """Trigger an external patient matching for a given patient object"""
    matching_obj = external_matcher(database, host, query_patient, node)
    if matching_obj:
        database['matches'].insert_one(matching_obj)
    return matching_obj


def check_request(database, request):
    """Check if request is valid, if it is return MME formatted patient
       Otherwise return error code.
    """
    check_result = None
    if not authorize(database, request):
        LOG.info('Request is not authorized')
        return 401
    else:
        try:
            request_json = request.get_json(force=True)
        except Exception as err:
            LOG.info('Json data in request is not valid:{}'.format(err))
            return 400

        try:
            validate_api(json_obj=request_json, is_request=True)
        except Exception as err:
            LOG.info('Patient data does not conform to API:{}'.format(err))
            return 422

        formatted_patient = mme_patient(json_patient=(request_json['patient']))
        return formatted_patient


def check_async_request(database, request):
    """Check if an asynchronous request is valid.
    Basically json data must be valid and the query ID should be
    already present in async responses database collection"""
    data = None
    try:
        data = request.json
        LOG.info('Request data looks valid. Source is {}'.format(data.get('source')))
    except:
        LOG.error('Request data is not valid. Abort')
        return 400
    else:
        query_id = data.get('query_id')
        if query_id:
            async_response = database['async_responses'].find_one({'query_id': query_id})
            LOG.info('Async response is {}'.format(async_response))
        if query_id is None or async_response is None:
            LOG.error('Async request not authorized. Abort')
            return 401
        resp = data.get('response')
        if resp is None:
            LOG.error("Async server did not provide any 'response' object")
            return 400
        else:
            try:
                validate_api(json_obj=resp, is_request=False)
            except Exception as err:
                LOG.info('Patient data does not conform to API:{}'.format(err))
                return 422

            return data


def validate_response(matches):
    """Validates patient matching results before sending them away in a response"""
    try:
        validate_api(json_obj=matches, is_request=False)
    except ValidationError as err:
        LOG.info('Patient data does not conform to API:{}'.format(err))
        return 422

    return matches


def bad_request(error_code):
    """Crete an automatic response based on custom error codes"""
    message = STATUS_CODES[error_code]['message']
    resp = jsonify(message)
    resp.status_code = error_code
    return resp


def delete_patient(database, patient_id):
    """Remove a patient by ID"""
    message = ''
    query = {'data.patient.id': patient_id}
    deleted = delete_by_query(query, database, 'matches')
    LOG.info('deleted {} matche/s triggered by this patient'.format(deleted))
    query = {'_id': patient_id}
    deleted = delete_by_query(query, database, 'patients')
    message = {}
    if deleted == 1:
        message['message'] = 'Patient and its matches were successfully deleted from database'
    else:
        message['message'] = 'ERROR. Could not delete a patient with ID {} from database'.format(patient_id)
    return message