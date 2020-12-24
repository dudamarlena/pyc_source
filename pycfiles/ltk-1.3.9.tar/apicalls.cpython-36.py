# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/hectorlopez/.virtualenvs/lingotek36/lib/python3.6/site-packages/ltk/apicalls.py
# Compiled at: 2020-04-15 17:45:44
# Size of source mod 2**32: 25999 bytes
import requests
from ltk.api_uri import API_URI
from ltk.utils import restart
import ltk.utils
from ltk.exceptions import RequestFailedError, ConnectionFailed
from ltk.logger import logger
import sys, os, urllib.parse as parse

class ApiCalls:

    def __init__(self, host, access_token, watch=False, timeout=5):
        self.host = host
        self.headers = {'Authorization': 'bearer ' + access_token}
        self.watch = watch
        self.timeout = timeout
        self.cookie = ''
        self.access_token = access_token

    def handleError(self):
        if self.watch:
            logger.warning('Could not connect to Lingotek')
            restart('Restarting watch', self.timeout)
        else:
            raise ConnectionFailed('Could not connect to Lingotek')

    def access_login(self, host):
        try:
            uri = '/login'
            r = requests.get(host + uri)
            cookie = r.headers['set-cookie']
            log_api('GET', uri, r)
            if cookie and len(cookie) > 0:
                self.cookie = cookie
                return True
            else:
                return False
        except Exception as e:
            print('access_login', e)
            self.handleError()
            return False

    def login(self, host, username, password):
        output = self.access_login(host)
        if output == False:
            return False
        else:
            try:
                uri = '/login'
                payload = {'username':username,  'password':password}
                r = requests.post((host + uri), headers={'Cookie': self.cookie}, data=payload)
                log_api('POST', uri, r)
            except Exception as e:
                print('login', e)
                self.handleError()

            return output

    def authenticate(self, host):
        output = None
        try:
            start = self.startup(host)
            if not start.url:
                return
            else:
                query = parse.parse_qs(parse.urlparse(start.url).query)
                if 'client_id' in query.keys():
                    cid = query['client_id']
                else:
                    return
                uri = '/dialog/authorize'
                payload = {'redirect_uri':'https://myaccount.lingotek.com/tms-ui/html/portal/sso_redirect.html',  'response_type':'token',  'client_id':cid}
                r = requests.get((host + uri), headers={'Cookie': self.cookie}, params=payload)
                log_api('GET', uri, r)
                fragment = parse.parse_qs(parse.urlparse(r.url).fragment)
                if 'access_token' in fragment.keys():
                    if len(fragment['access_token']) > 0:
                        return fragment['access_token'][0]
                return
        except Exception as e:
            print('authenticate', e)
            self.handleError()
            return

    def startup(self, host):
        try:
            uri = '/lingopoint/portal/startup.action'
            r = requests.get((host + uri), headers={'Host': 'myaccount.lingotek.com'})
            log_api('GET', uri, r)
        except Exception as e:
            print('startup', e)
            self.handleError()

        return r

    def list_communities(self):
        """ gets the communities that a user is in """
        try:
            uri = API_URI['community']
            payload = {'limit': 1000}
            r = requests.get((self.host + uri), headers=(self.headers), params=payload)
            log_api('GET', uri, r)
        except requests.exceptions.ConnectionError:
            self.handleError()

        return r

    def list_document_formats(self):
        """ gets the communities that a user is in """
        try:
            uri = API_URI['document_format']
            payload = {'limit': 1000}
            r = requests.get((self.host + uri), headers=(self.headers), params=payload)
            log_api('GET', uri, r)
        except requests.exceptions.ConnectionError:
            self.handleError()

        return r

    def list_projects(self, community_id):
        """ gets the projects a user has """
        try:
            uri = API_URI['project']
            payload = {'community_id':community_id,  'limit':10000}
            r = requests.get((self.host + uri), headers=(self.headers), params=payload)
            log_api('GET', uri, r)
        except requests.exceptions.ConnectionError:
            self.handleError()

        return r

    def add_project(self, project_name, community_id, workflow_id):
        """ adds a project """
        try:
            uri = API_URI['project']
            payload = {'title':project_name,  'community_id':community_id,  'workflow_id':workflow_id}
            r = requests.post((self.host + uri), headers=(self.headers), data=payload)
            log_api('POST', uri, r)
        except requests.exceptions.ConnectionError:
            self.handleError()

        return r

    def get_project(self, project_id):
        """ Get a project which the active user has access to """
        try:
            uri = API_URI['project_id'] % locals()
            payload = {}
            r = requests.get((self.host + uri), headers=(self.headers), data=payload)
            log_api('GET', uri, r)
        except requests.exceptions.ConnectionError:
            self.handleError()

        return r

    def patch_project(self, project_id, workflow_id):
        """ updates a project """
        try:
            uri = API_URI['project_id'] % locals()
            payload = {'project_id': project_id}
            if workflow_id:
                payload['workflow_id'] = workflow_id
            r = requests.patch((self.host + uri), headers=(self.headers), data=payload)
            log_api('PATCH', uri, r)
        except requests.exceptions.ConnectionError:
            self.handleError()

        return r

    def project_add_target(self, project_id, locale, due_date):
        """ adds a target to all documents within a project """
        try:
            uri = API_URI['project_translation'] % locals()
            payload = {'id':project_id,  'locale_code':locale}
            if due_date:
                payload['due_date'] = due_date
            r = requests.post((self.host + uri), headers=(self.headers), data=payload)
            log_api('POST', uri, r)
        except requests.exceptions.ConnectionError:
            self.handleError()

        return r

    def project_status(self, project_id):
        """ gets the status of a project """
        try:
            uri = API_URI['project_status'] % locals()
            r = requests.get((self.host + uri), headers=(self.headers))
            log_api('GET', uri, r)
        except requests.exceptions.ConnectionError:
            self.handleError()

        return r

    def project_delete_target(self, project_id, locale):
        try:
            uri = API_URI['project_translation_locale'] % locals()
            r = requests.delete((self.host + uri), headers=(self.headers))
            log_api('DELETE', uri, r)
        except requests.exceptions.ConnectionError:
            self.handleError()

        return r

    def delete_project(self, project_id):
        """ deletes a project """
        try:
            uri = API_URI['project_id'] % locals()
            r = requests.delete((self.host + uri), headers=(self.headers))
            log_api('DELETE', uri, r)
        except requests.exceptions.ConnectionError:
            self.handleError()

        return r

    def get_document(self, document_id):
        """ gets a document by id """
        try:
            uri = API_URI['document_id'] % locals()
            r = requests.get((self.host + uri), headers=(self.headers))
            log_api('GET', uri, r)
        except requests.exceptions.ConnectionError:
            self.handleError()

        return r

    def get_latest_document(self, document_id):
        """ get latest version of a document """
        try:
            uri = API_URI['document_latest_version'] % locals()
            r = requests.get((self.host + uri), headers=(self.headers))
            log_api('GET', uri, r)
        except requests.exceptions.ConnectionError:
            self.handleError()

        return r

    def add_document(self, source_locale, file_name, project_id, title, doc_metadata={}, **kwargs):
        """ adds a document """
        try:
            uri = API_URI['document']
            payload = {'locale_code':source_locale,  'project_id':project_id,  'title':title}
            for field in doc_metadata:
                if doc_metadata[field]:
                    payload[field] = doc_metadata[field]

            for key in kwargs:
                if kwargs[key]:
                    if key == 'download_folder' or key == 'overwrite':
                        pass
                    else:
                        payload[key] = kwargs[key]

            detected_format = ltk.utils.detect_format(file_name)
            if 'format' not in kwargs or kwargs['format'] is None:
                payload['format'] = detected_format
            document = open(file_name, 'rb')
            files = {'content': (file_name, document)}
            if 'srx' in kwargs:
                if kwargs['srx'] is not None:
                    files.update({'srx': (kwargs['srx'], open(kwargs['srx'], 'rb'))})
            if 'its' in kwargs and kwargs['its'] is not None:
                files.update({'its': (kwargs['its'], open(kwargs['its'], 'rb'))})
            if 'fprm' in kwargs:
                if kwargs['fprm'] is not None:
                    fprm_file = open(kwargs['fprm'], 'rb')
                    files.update({'fprm': (kwargs['fprm'], fprm_file)})
            r = requests.post((self.host + uri), headers=(self.headers), data=payload, files=files)
            log_api('POST', uri, r)
            document.close()
        except requests.exceptions.ConnectionError:
            self.handleError()

        return r

    def document_add_reference(self, document_id, reference):
        """ adds reference material to a document """
        try:
            uri = API_URI['reference'] % locals()
            payload = {'id': document_id}
            document = open(reference['file'], 'rb')
            files = {'content': (reference['file'], document)}
            if 'name' in reference:
                if reference['name']:
                    payload.update({'name': reference['name']})
            if 'description' in reference:
                if reference['description']:
                    payload.update({'description': reference['description']})
            r = requests.post((self.host + uri), headers=(self.headers), data=payload, files=files)
            log_api('POST', uri, r)
            document.close()
        except requests.exceptions.ConnectionError:
            self.handleError()

        return r

    def document_list_reference(self, document_id):
        """ lists the reference material that is attached to a document """
        try:
            uri = API_URI['reference'] % locals()
            payload = {'id': document_id}
            r = requests.get((self.host + uri), headers=(self.headers), params=payload)
            log_api('GET', uri, r)
        except requests.exceptions.ConnectionError:
            self.handleError()

        return r

    def document_download_reference(self, document_id, reference_id):
        """ downloads reference material that is attached to a document """
        try:
            uri = API_URI['reference_id'] % locals()
            payload = {'id':document_id,  'reference_id':reference_id}
            r = requests.get((self.host + uri), headers=(self.headers), params=payload, stream=True)
            log_api('GET', uri, r)
        except requests.exceptions.ConnectionError:
            self.handleError()

        return r

    def document_remove_reference(self, document_id, reference_id):
        """ removes reference material from a document """
        try:
            uri = API_URI['reference_id'] % locals()
            r = requests.delete((self.host + uri), headers=(self.headers))
            log_api('DELETE', uri, r)
        except requests.exceptions.ConnectionError:
            self.handleError()

        return r

    def document_add_target(self, document_id, locale, workflow_id=None, due_date=None):
        """ adds a target to existing document, starts the workflow """
        try:
            uri = API_URI['document_translation'] % locals()
            payload = {'locale_code':locale,  'id':document_id}
            if workflow_id:
                payload['workflow_id'] = workflow_id
            if due_date:
                payload['due_date'] = due_date
            r = requests.post((self.host + uri), headers=(self.headers), data=payload)
            log_api('POST', uri, r)
        except requests.exceptions.ConnectionError:
            self.handleError()

        return r

    def list_documents(self, project_id):
        """ lists all documents a user has access to, could be filtered by project id """
        try:
            uri = API_URI['document']
            payload = {}
            if project_id:
                payload = {'project_id':project_id, 
                 'limit':10000}
            r = requests.get((self.host + uri), headers=(self.headers), params=payload)
            log_api('GET', uri, r)
        except requests.exceptions.ConnectionError:
            self.handleError()

        return r

    def document_status(self, document_id):
        """ gets the status of a document """
        try:
            uri = API_URI['document_status'] % locals()
            payload = {'document_id': document_id}
            r = requests.get((self.host + uri), headers=(self.headers), params=payload)
            log_api('GET', uri, r)
        except requests.exceptions.ConnectionError:
            self.handleError()

        return r

    def document_translation_status(self, document_id):
        """ gets the status of document translations """
        try:
            uri = API_URI['document_translation'] % locals()
            r = requests.get((self.host + uri), headers=(self.headers))
            log_api('GET', uri, r)
        except requests.exceptions.ConnectionError:
            self.handleError()

        return r

    def document_translation_locale_status(self, document_id, locale):
        """ gets the status of a specific target for a document translation """
        try:
            uri = API_URI['document_translation_locale'] % locals()
            r = requests.get((self.host + uri), headers=(self.headers))
            log_api('GET', uri, r)
        except requests.exceptions.ConnectionError:
            self.handleError()

        return r

    def document_content(self, document_id, locale_code, auto_format, xliff=False, finalized_file='off'):
        """ downloads the translated document """
        headers = self.headers
        try:
            uri = API_URI['document_content'] % locals()
            payload = {}
            payload['auto_format'] = auto_format
            if locale_code:
                payload['locale_code'] = locale_code
            if xliff:
                headers['Accept'] = 'application/x-xliff+xml'
            if finalized_file == 'on':
                payload['finalized_file'] = 'true'
            r = requests.get((self.host + uri), headers=headers, params=payload, stream=True)
            log_api('GET', uri, r)
        except requests.exceptions.ConnectionError:
            self.handleError()

        return r

    def document_update(self, document_id, file_name=None, doc_metadata={}, **kwargs):
        try:
            uri = API_URI['document_id'] % locals()
            payload = {'id': document_id}
            for field in doc_metadata:
                if doc_metadata[field]:
                    payload[field] = doc_metadata[field]

            for key in kwargs:
                if kwargs[key]:
                    payload[key] = kwargs[key]

            if file_name:
                document = open(file_name, 'rb')
                files = {'content': (file_name, document)}
                if 'srx' in kwargs:
                    if kwargs['srx'] is not None:
                        files.update({'srx': (kwargs['srx'], open(kwargs['srx'], 'rb'))})
                if 'its' in kwargs:
                    if kwargs['its'] is not None:
                        files.update({'its': (kwargs['its'], open(kwargs['its'], 'rb'))})
                if 'fprm' in kwargs and kwargs['fprm'] is not None:
                    files.update({'fprm': (kwargs['fprm'], open(kwargs['fprm'], 'rb'))})
                r = requests.patch((self.host + uri), headers=(self.headers), data=payload, files=files)
                document.close()
            else:
                r = requests.patch((self.host + uri), headers=(self.headers), data=payload)
            log_api('PATCH', uri, r)
        except requests.exceptions.ConnectionError:
            self.handleError()

        return r

    def document_delete_target(self, document_id, locale):
        try:
            uri = API_URI['document_translation_locale'] % locals()
            r = requests.delete((self.host + uri), headers=(self.headers))
            log_api('DELETE', uri, r)
        except requests.exceptions.ConnectionError:
            self.handleError()

        return r

    def document_cancel_target(self, document_id, locale):
        try:
            uri = API_URI['document_cancel_locale'] % locals()
            payload = {'id':document_id,  'locale':locale,  'cancelled_reason':'CANCELLED_BY_AUTHOR',  'mark_invoiceable':'true'}
            r = requests.post((self.host + uri), headers=(self.headers), data=payload)
            log_api('POST', uri, r)
        except requests.exceptions.ConnectionError:
            self.handleError()

        return r

    def document_delete(self, document_id):
        try:
            uri = API_URI['document_id'] % locals()
            r = requests.delete((self.host + uri), headers=(self.headers))
            log_api('DELETE', uri, r)
        except requests.exceptions.ConnectionError:
            self.handleError()

        return r

    def document_cancel(self, document_id):
        try:
            uri = API_URI['document_cancel'] % locals()
            payload = {'id':document_id,  'cancelled_reason':'CANCELLED_BY_AUTHOR'}
            r = requests.post((self.host + uri), headers=(self.headers), data=payload)
            log_api('POST', uri, r)
        except requests.exceptions.ConnectionError:
            self.handleError()

        return r

    def get_process(self, process_id):
        try:
            uri = API_URI['process'] % locals()
            payload = {'process_id': process_id}
            r = requests.get((self.host + uri), headers=(self.headers), params=payload)
            log_api('GET', uri, r)
        except requests.exceptions.ConnectionError:
            self.handleError()

        return r

    def list_workflows(self, community_id):
        try:
            uri = API_URI['workflow']
            payload = {'community_id':community_id,  'limit':1000}
            r = requests.get((self.host + uri), headers=(self.headers), params=payload)
            log_api('GET', uri, r)
        except requests.exceptions.ConnectionError:
            self.handleError()

        return r

    def list_locales(self):
        try:
            uri = 'http://gmc.lingotek.com/v1/locales'
            r = requests.get(uri)
        except requests.exceptions.ConnectionError:
            self.handleError()

        return r

    def list_filters(self):
        try:
            uri = API_URI['filter']
            r = requests.get((self.host + uri), headers=(self.headers), params={'limit': 1000})
            log_api('GET', uri, r)
        except requests.exceptions.ConnectionError:
            self.handleError()

        return r

    def get_filter_content(self, filter_id):
        """ gets a filter by id """
        try:
            uri = API_URI['filter_content'] % locals()
            r = requests.get((self.host + uri), headers=(self.headers))
            if r.status_code == 200:
                log_api('GET', uri, r)
            else:
                log_api('GET', uri, r)
        except requests.exceptions.ConnectionError:
            self.handleError()

        return r

    def get_filter_info(self, filter_id):
        """ gets a filter by id """
        try:
            uri = API_URI['filter_id'] % locals()
            r = requests.get((self.host + uri), headers=(self.headers))
            log_api('GET', uri, r)
        except requests.exceptions.ConnectionError:
            self.handleError()

        return r

    def patch_filter(self, filter_id, filename):
        """ update a filter by id """
        try:
            uri = API_URI['filter_id'] % locals()
            params = {'id': filter_id}
            content = open(filename, 'rb')
            files = {'content': (filename, content)}
            r = requests.patch((self.host + uri), headers=(self.headers), data=params, files=files)
            log_api('PATCH', uri, r)
        except requests.exceptions.ConnectionError:
            self.handleError()

        return r

    def post_filter(self, filename, filter_type='FPRM'):
        """ post a filter """
        try:
            uri = API_URI['filter']
            content = open(filename, 'rb')
            files = {'content': (filename, content)}
            if filter_type is None:
                extension = os.path.splitext(filename)[1]
                filter_type = extension[1:]
            filter_type = filter_type.lower()
            name = os.path.splitext(filename)[0]
            params = {'name':name,  'type':filter_type}
            r = requests.post((self.host + uri), headers=(self.headers), data=params, files=files)
            log_api('PATCH', uri, r)
        except requests.exceptions.ConnectionError:
            self.handleError()

        return r

    def delete_filter(self, filter_id):
        """ deletes a filter """
        try:
            uri = API_URI['filter_id'] % locals()
            r = requests.delete((self.host + uri), headers=(self.headers))
            log_api('DELETE', uri, r)
        except requests.exceptions.ConnectionError:
            self.handleError()

        return r

    def get_project_info(self, community_id):
        response = self.list_projects(community_id)
        info = {}
        if response.status_code == 200:
            if int(response.json()['properties']['total']) == 0:
                return info
            else:
                entities = response.json()['entities']
                for entity in entities:
                    info[entity['properties']['id']] = entity['properties']['title']

                return info
        if response.status_code == 204:
            return info
        raise RequestFailedError('Unable to get existing projects')

    def get_communities_info(self):
        response = self.list_communities()
        if response.status_code != 200:
            return
        else:
            entities = response.json()['entities']
            info = {}
            for entity in entities:
                info[entity['properties']['id']] = entity['properties']['title']

            return info

    def get_document_formats(self):
        response = self.list_document_formats()
        info = {}
        if response.status_code != 200:
            return info
        else:
            entities = response.json()['entities']
            for entity in entities:
                info[entity['properties']['type']] = entity['properties']['type']

            return info


def log_api(method, uri, response):
    try:
        content_length = response.headers['content-length']
    except KeyError:
        content_length = 'No content-length header'

    log = '{method} {uri} {status} {length}'.format(method=method, uri=uri, status=(response.status_code), length=content_length)
    logger.api_call(log)
    if 'content-type' in response.headers:
        if response.headers['content-type'].find('json') != -1:
            try:
                import json
                response_info = json.dumps((response.json()), indent=4, separators=(',',
                                                                                    ': '))
            except ValueError:
                response_info = 'No json response available'

            logger.api_response(response_info)
    if 'content-length' in response.headers:
        if response.headers['content-length'] != '0':
            if response.headers['content-type'] == 'application/zip':
                logger.api_response('Zip file')
            else:
                logger.api_response(response.content.decode('UTF-8'))