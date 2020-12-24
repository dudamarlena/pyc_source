# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/chiararasi/Documents/work/GITs/patientMatcher/patientMatcher/match/handler.py
# Compiled at: 2019-04-23 03:57:58
# Size of source mod 2**32: 11128 bytes
import logging, datetime, requests, pymongo, json
from werkzeug.datastructures import Headers
from patientMatcher.match.genotype_matcher import match as genomatch
from patientMatcher.match.phenotype_matcher import match as phenomatch
from patientMatcher.parse.patient import json_patient
LOG = logging.getLogger(__name__)

def patient_matches(database, patient_id, type=None, with_results=True):
    """Retrieve all matches for a patient specified by an ID

    Args:
        database(pymongo.database.Database)
        patient_id(str): ID of a patient in database
        type(str): type of matching, external or internal
        with_results(bool): if True only matches with results are returned

    Returns:
        matches(list): a list of dictionaries = [ {match_obj1}, {match_obj2}, .. ]
    """
    query = {'$or': [
             {'data.patient.id': patient_id},
             {'results.patients.patient.id': patient_id}]}
    if type:
        query['match_type'] = type
    if with_results:
        query['has_matches'] = True
    matches = list(database['matches'].find(query))
    LOG.info(matches)
    return matches


def internal_matcher(database, patient_obj, max_pheno_score, max_geno_score, max_results=5):
    """Handles a query patient matching against the database of patients

    Args:
        database(pymongo.database.Database)
        patient_obj(dic): a mme formatted patient object
        max_pheno_score(float): a number between 0 and 1
        max_geno_score(float): a number between 0 and 1
        max_results(int): the maximum number of results that the server should return.

    Returns:
        internal_match(dict): a matching object with results(list) sorted by score
    """
    json_pat = json_patient(patient_obj)
    pheno_matches = []
    pheno_m_keys = []
    geno_matches = []
    geno_m_keys = []
    matches = []
    if patient_obj.get('features') or patient_obj.get('disorders'):
        LOG.info('Matching phenotypes against database patients..')
        pheno_matches = phenomatch(database, max_pheno_score, patient_obj.get('features', []), patient_obj.get('disorders', []))
        pheno_m_keys = list(pheno_matches.keys())
    if patient_obj.get('genomicFeatures'):
        if len(patient_obj['genomicFeatures']) > 0:
            LOG.info('Matching variants/genes against database patients..')
            geno_matches = genomatch(database, patient_obj['genomicFeatures'], max_geno_score)
            geno_m_keys = list(geno_matches.keys())
    unique_patients = list(set(pheno_m_keys + geno_m_keys))
    for key in unique_patients:
        pheno_score = 0
        geno_score = 0
        patient_obj = None
        if key in pheno_m_keys:
            pheno_score = pheno_matches[key]['pheno_score']
            patient_obj = pheno_matches[key]['patient_obj']
        if key in geno_m_keys:
            geno_score = geno_matches[key]['geno_score']
            patient_obj = geno_matches[key]['patient_obj']
        p_score = pheno_score + geno_score
        score = {'patient':p_score, 
         '_genotype':geno_score, 
         '_phenotype':pheno_score}
        match = {'patient':json_patient(patient_obj), 
         'score':score}
        if score['patient'] > 0:
            matches.append(match)

    sorted_matches = sorted(matches, key=(lambda k: k['score']['patient']), reverse=True)
    has_matches = False
    if sorted_matches:
        has_matches = True
    internal_match = {'created':datetime.datetime.now(), 
     'has_matches':has_matches, 
     'data':{'patient': json_pat}, 
     'results':[
      {'node':{'id':'patientMatcher', 
        'label':'patientMatcher server'}, 
       'patients':sorted_matches[:max_results]}], 
     'match_type':'internal'}
    return internal_match


def external_matcher(database, host, patient, node=None):
    """Handles a query patient matching against all connected MME nodes

    Args:
        database(pymongo.database.Database)
        host(str): Name of this server (MME_HOST in config file)
        patient(dict) : a MME patient entity
        node(str): id of the node to search in

    Returns:
        external_match(dict): a matching object containing a list of results in 'results' field
    """
    query = {}
    if node:
        query['_id'] = node
    connected_nodes = list(database['nodes'].find(query))
    if len(connected_nodes) == 0:
        LOG.error("Could't find any connected MME nodes. Aborting external matching.")
        return
    else:
        headers = Headers()
        data = {'patient': json_patient(patient)}
        external_match = {'created':datetime.datetime.now(), 
         'has_matches':False, 
         'data':data, 
         'results':[],  'errors':[],  'match_type':'external'}
        LOG.info('Matching patient against {} node(s)..'.format(len(connected_nodes)))
        for node in connected_nodes:
            server_name = node['_id']
            node_url = node['matching_url']
            token = node['auth_token']
            request_content_type = node['accepted_content']
            headers = {'Content-Type':request_content_type, 
             'Accept':'application/vnd.ga4gh.matchmaker.v1.0+json', 
             'X-Auth-Token':token, 
             'Host':host}
            LOG.info('sending HTTP request to server: "{}"'.format(server_name))
            json_response = None
            server_return = None
            try:
                server_return = requests.request(method='POST',
                  url=node_url,
                  headers=headers,
                  data=(json.dumps(data)))
                json_response = server_return.json()
            except Exception as json_exp:
                error = json_exp
                LOG.error('Server returned error:{}'.format(error))
                error_obj = {'node':{'id':node['_id'], 
                  'label':node['label']}, 
                 'error':str(error)}
                external_match['errors'].append(error_obj)

            if json_response:
                LOG.info('server returns the following response: {}'.format(json_response))
                result_obj = {'node':{'id':node['_id'], 
                  'label':node['label']}, 
                 'patients':[]}
                if 'results' in json_response:
                    results = json_response['results']
                    if len(results):
                        external_match['has_matches'] = True
                        for result in results:
                            result_obj['patients'].append(result)

                        external_match['results'].append(result_obj)
                else:
                    if 'query_id' in json_response:
                        LOG.info('Node {} is sending an async response, saving query id to server'.format(server_name))
                        save_async_response(database=database, node_obj=node, query_id=(json_response['query_id']), query_patient_id=(patient['_id']))
                    else:
                        LOG.error('JSON response from server was:{}'.format(json_response))

        return external_match


def async_match(database, response_data):
    """Creates a match object from data received from an asyc server

    Args:
        database(pymongo.database.Database)
        response_data(dict): data provided by async server in follow up request

    Returns:
        async_match(dict): a match object
    """
    query_id = response_data['query_id']
    async_response = database['async_responses'].find_one({'query_id': query_id})
    patient_id = async_response.get('query_patient_id')
    patient_obj = database['patients'].find_one({'_id': patient_id})
    node = async_response.get('node')
    if not patient_obj:
        LOG.error("Couldn't find a patient with id '{} in database.".format(patient_id))
        return
    else:
        if not node:
            LOG.error("Couldn't find node '{}' in database ".format(node.get('label')))
            return
        resp = response_data.get('response')
        results_obj = {'node':node, 
         'patients':resp.get('results')}
        async_match = {'created':datetime.datetime.now(), 
         'has_matches':True if len(results_obj.get('patients')) > 0 else False, 
         'data':{'patient': patient_obj}, 
         'errors':[],  'match_type':'external', 
         'async':True, 
         'results':[
          results_obj]}
        return async_match


def save_async_response(database, node_obj, query_id, query_patient_id):
    """Creates an async response object in the async_responses collection.
    This object stores info about the query patient sent to an async server and the
    query_id received from it. Async server does provide match results in a
    subsequent request, along with the same query_id string, to trace it back to the
    original request initiated by patienrMatcher.

    Args:
        database(pymongo.database.Database)
        node_obj(dict): an async node object
        query_id(str): an id returned by async server in its response
        query_patient_id(str): id of internal patient matched against patients
            in async server
    """
    async_response = {'query_id':query_id, 
     'query_patient_id':query_patient_id, 
     'node':{'id':node_obj['_id'], 
      'label':node_obj.get('label')}, 
     'created':datetime.datetime.now()}
    database['async_responses'].insert_one(async_response)