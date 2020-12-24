# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/site-packages/onesky/client.py
# Compiled at: 2014-06-05 12:21:15
import hashlib, os, requests, time
DEFAULT_API_URL = 'https://platform.api.onesky.io/1/'

class Client:

    def __init__(self, api_key, api_secret, api_url=DEFAULT_API_URL, download_dir='.', request_callback=None):
        self.api_url = api_url
        self.api_key = api_key
        self.api_secret = api_secret
        self.download_dir = download_dir
        self.request_callback = request_callback

    def create_auth_variables(self):
        timestamp = str(int(time.time()))
        dev_hash = hashlib.md5()
        dev_hash.update(timestamp)
        dev_hash.update(self.api_secret)
        return {'api_key': self.api_key, 
           'timestamp': timestamp, 
           'dev_hash': dev_hash.hexdigest()}

    def do_http_request(self, relative_url, parameters=None, method='GET', upload_file_stream=None):
        absolute_url = self.api_url + relative_url
        if parameters is None:
            url_parameters = {}
        else:
            url_parameters = dict([ (k, v) for k, v in parameters.items() if v is not None
                                  ])
        url_parameters.update(self.create_auth_variables())
        if upload_file_stream is not None:
            files = {'file': upload_file_stream}
        else:
            files = None
        if self.request_callback:
            self.request_callback(method, absolute_url, url_parameters)
        request_function = getattr(requests, method.lower())
        response = request_function(absolute_url, params=url_parameters, files=files)
        if response.headers.get('content-disposition', '').startswith('attachment;'):
            short_filename = response.headers['content-disposition'].split('=')[1]
            absolute_filename = os.path.join(self.download_dir, short_filename)
            with open(absolute_filename, 'wb') as (f):
                for chunk in response.iter_content():
                    f.write(chunk)

            response_dict = {'downloaded_filename': absolute_filename}
        else:
            try:
                response_dict = response.json()
            except ValueError:
                response_dict = {}

        return (
         response.status_code, response_dict)

    def project_group_list(self, page=None, per_page=None):
        relative_url = 'project-groups'
        params = {'page': page, 'per_page': per_page}
        return self.do_http_request(relative_url, params)

    def project_group_show(self, project_group_id):
        relative_url = ('project-groups/{}').format(project_group_id)
        return self.do_http_request(relative_url)

    def project_group_create(self, name, locale=None):
        relative_url = 'project-groups'
        params = {'name': name, 'locale': locale}
        return self.do_http_request(relative_url, params, method='POST')

    def project_group_delete(self, project_group_id):
        relative_url = ('project-groups/{}').format(project_group_id)
        return self.do_http_request(relative_url, method='DELETE')

    def project_group_languages(self, project_group_id):
        relative_url = ('project-groups/{}/languages').format(project_group_id)
        return self.do_http_request(relative_url)

    def project_list(self, project_group_id, page=None, per_page=None):
        relative_url = ('project-groups/{}/projects').format(project_group_id)
        params = {'page': page, 'per_page': per_page}
        return self.do_http_request(relative_url, params)

    def project_show(self, project_id):
        relative_url = ('projects/{}').format(project_id)
        return self.do_http_request(relative_url)

    def project_create(self, project_group_id, project_type, name=None, description=None):
        relative_url = ('project-groups/{}/projects').format(project_group_id)
        params = {'project_type': project_type, 'name': name, 
           'description': description}
        return self.do_http_request(relative_url, params, method='POST')

    def project_update(self, project_id, name=None, description=None):
        relative_url = ('projects/{}').format(project_id)
        params = {'name': name, 'description': description}
        return self.do_http_request(relative_url, params, method='PUT')

    def project_delete(self, project_id):
        relative_url = ('projects/{}').format(project_id)
        return self.do_http_request(relative_url, method='DELETE')

    def project_languages(self, project_id):
        relative_url = ('projects/{}/languages').format(project_id)
        return self.do_http_request(relative_url)

    def project_type_list(self):
        return self.do_http_request('project-types')

    def file_list(self, project_id, page=None, per_page=None):
        relative_url = ('projects/{}/files').format(project_id)
        params = {'page': page, 'per_page': per_page}
        return self.do_http_request(relative_url, params)

    def file_upload(self, project_id, file_name, file_format, locale=None, is_keeping_all_strings=None):
        relative_url = ('projects/{}/files').format(project_id)
        params = {'file_format': file_format, 'locale': locale, 'is_keeping_all_strings': is_keeping_all_strings}
        with open(file_name, 'rb') as (file_stream):
            return self.do_http_request(relative_url, params, method='POST', upload_file_stream=file_stream)

    def file_delete(self, project_id, file_name):
        relative_url = ('projects/{}/files').format(project_id)
        params = {'file_name': file_name}
        return self.do_http_request(relative_url, params, method='DELETE')

    def translation_export(self, project_id, locale, source_file_name, export_file_name=None):
        relative_url = ('projects/{}/translations').format(project_id)
        params = {'locale': locale, 'source_file_name': source_file_name, 'export_file_name': export_file_name}
        return self.do_http_request(relative_url, params)

    def translation_status(self, project_id, file_name, locale):
        relative_url = ('projects/{}/translations/status').format(project_id)
        params = {'file_name': file_name, 'locale': locale}
        return self.do_http_request(relative_url, params)

    def import_task_list(self, project_id, page=None, per_page=None, status=None):
        relative_url = ('projects/{}/import-tasks').format(project_id)
        params = {'page': page, 'per_page': per_page, 'status': status}
        return self.do_http_request(relative_url, params)

    def import_task_show(self, project_id, import_id):
        relative_url = ('projects/{}/import-tasks/{}').format(project_id, import_id)
        return self.do_http_request(relative_url)

    def screenshot_upload(self, project_id, screenshots):
        pass

    def quotation_show(self, project_id, files, to_locale, is_including_not_translated=None, is_including_not_approved=None, is_including_outdated=None, specialization=None):
        relative_url = ('projects/{}/quotations').format(project_id)
        params = {'files': str(files), 'to_locale': to_locale, 
           'is_including_not_translated': is_including_not_translated, 
           'is_including_not_approved': is_including_not_approved, 
           'is_including_outdated': is_including_outdated, 
           'specialization': specialization}
        return self.do_http_request(relative_url, params)

    def order_list(self, project_id, page=None, per_page=None):
        relative_url = ('projects/{}/orders').format(project_id)
        params = {'page': page, 'per_page': per_page}
        return self.do_http_request(relative_url, params)

    def order_show(self, project_id, order_id):
        relative_url = ('projects/{}/orders/{}').format(project_id, order_id)
        return self.do_http_request(relative_url)

    def order_create(self, project_id, files, to_locale, order_type=None, is_including_not_translated=None, is_including_not_approved=None, is_including_outdated=None, translator_type=None, tone=None, specialization=None, note=None):
        relative_url = ('projects/{}/orders').format(project_id)
        params = {'files': files, 'to_locale': to_locale, 
           'order_type': order_type, 
           'is_including_not_translated': is_including_not_translated, 
           'is_including_not_approved': is_including_not_approved, 
           'is_including_outdated': is_including_outdated, 
           'translator_type': translator_type, 
           'tone': tone, 
           'specialization': specialization, 
           'note': note}
        return self.do_http_request(relative_url, params, 'POST')

    def locale_list(self):
        return self.do_http_request('locales')