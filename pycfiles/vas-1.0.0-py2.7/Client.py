# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.8-x86_64/egg/vas/util/Client.py
# Compiled at: 2012-11-01 11:36:39
import json, os, requests, time
from vas.util.LinkUtils import LinkUtils
from vas.VFabricAdministrationServerError import VFabricAdministrationServerError

class Client:
    __CONTENT_TYPE_JSON = 'application/json'
    __CONTENT_TYPE_ZIP = 'application/zip'
    __CONTENT_TYPE_MULTIPART = 'multipart/mixed'
    __CONTENT_TYPE_TEXT_PLAIN = 'text/plain'
    __HEADER_CONTENT_TYPE = 'Content-Type'
    __HEADER_LOCATION = 'Location'
    __TASK_POLLING_INTERVAL = 1

    def __init__(self, username, password):
        self.__username = username
        self.__password = password

    def get(self, location):
        response = self.__do_request('GET', location)
        status_code = response.status_code
        if status_code == requests.codes.OK:
            content_type = response.headers[self.__HEADER_CONTENT_TYPE]
            if content_type == self.__CONTENT_TYPE_JSON:
                return response.json
            if content_type == self.__CONTENT_TYPE_ZIP:
                return response.content
            if content_type == self.__CONTENT_TYPE_TEXT_PLAIN:
                return response.text
            raise VFabricAdministrationServerError('Unknown payload type: ' + content_type)
        else:
            raise VFabricAdministrationServerError('Unexpected status code: ' + status_code)

    def delete(self, location):
        response = self.__do_request('DELETE', location)
        if response.status_code == requests.codes.OK:
            return
        if response.status_code == requests.codes.ACCEPTED:
            self.__await_task(response.headers[self.__HEADER_LOCATION])
        else:
            self.__raise_exception(response)

    def post(self, location, payload, rel=None):
        if isinstance(payload, dict) or isinstance(payload, list):
            headers = {self.__HEADER_CONTENT_TYPE: self.__CONTENT_TYPE_JSON}
            encoded_body = json.dumps(payload)
        elif isinstance(payload, str) or isinstance(payload, unicode):
            headers = {self.__HEADER_CONTENT_TYPE: self.__CONTENT_TYPE_TEXT_PLAIN}
            encoded_body = payload
        else:
            raise VFabricAdministrationServerError(('Unknown payload type: {}').format(type(payload)))
        response = self.__do_request('POST', location, headers=headers, body=encoded_body)
        if response.status_code == requests.codes.OK:
            return
        else:
            if response.status_code == requests.codes.ACCEPTED:
                return self.__await_task(response.headers[self.__HEADER_LOCATION], rel)
            self.__raise_exception(response)
            return

    def post_multipart(self, location, content, metadata=None):
        files = {}
        if metadata is not None:
            files['metadata'] = (
             'metadata.json', json.dumps(metadata))
        if os.path.isfile(content):
            with open(content, 'rb') as (data):
                files['data'] = data
                response = self.__do_request('POST', location, files=files)
        else:
            files['data'] = content
            response = self.__do_request('POST', location, files=files)
        if response.status_code == requests.codes.CREATED:
            return response.headers[self.__HEADER_LOCATION]
        else:
            self.__raise_exception(response)
            return

    def __do_request(self, method, location, headers=None, body=None, files=None):
        return requests.request(method, location, headers=headers, data=body, files=files, auth=(
         self.__username, self.__password), verify=False)

    def __await_task(self, task_location, rel=None):
        while True:
            task = self.get(task_location)
            status = task['status']
            if 'PENDING' == status or 'IN_PROGRESS' == status:
                time.sleep(self.__TASK_POLLING_INTERVAL)
            elif 'SUCCESS' == status:
                self.delete(task_location)
                if rel is not None:
                    return LinkUtils.get_link_href(task, rel)
                return
            else:
                raise VFabricAdministrationServerError(task['message'], task['detail'])

        return

    def __raise_exception(self, response):
        reasons = []
        body = response.content
        try:
            for reason in response.json['reasons']:
                reasons.append(reason['message'])

        except ValueError:
            reasons.append(body)

        raise VFabricAdministrationServerError(code=response.status_code, *reasons)

    def __repr__(self):
        return ('{}(username={}, password={})').format(self.__class__.__name__, repr(self.__username), repr(self.__password))