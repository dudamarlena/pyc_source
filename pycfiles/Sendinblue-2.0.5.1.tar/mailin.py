# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/ekta/Downloads/mailin-api-python/mailin.py
# Compiled at: 2016-12-30 00:22:26
import requests, json

class Mailin:
    """ This is the Mailin client class
  """

    def __init__(self, base_url, api_key, timeout=None):
        self.base_url = base_url
        self.api_key = api_key
        self.timeout = timeout

    def do_request(self, resource, method, indata):
        url = self.base_url + '/' + resource
        if self.timeout is not None:
            self.timeout = self.timeout
        else:
            self.timeout = 30
        if self.timeout is not None and (self.timeout <= 0 or self.timeout > 60):
            raise Exception('value not allowed for timeout')
        content_type = 'application/json'
        headers = {'api-key': self.api_key, 
           'content-type': content_type}
        response = requests.request(method.lower(), url, data=indata, headers=headers, timeout=self.timeout)
        return response.json()

    def get(self, resource, indata):
        return self.do_request(resource, 'GET', indata)

    def post(self, resource, indata):
        return self.do_request(resource, 'POST', indata)

    def put(self, resource, indata):
        return self.do_request(resource, 'PUT', indata)

    def delete(self, resource, indata):
        return self.do_request(resource, 'DELETE', indata)

    def get_account(self):
        return self.get('account', '')

    def get_smtp_details(self):
        return self.get('account/smtpdetail', '')

    def create_child_account(self, data):
        return self.post('account', json.dumps(data))

    def update_child_account(self, data):
        return self.put('account', json.dumps(data))

    def delete_child_account(self, data):
        return self.delete('account/' + data['auth_key'], '')

    def get_reseller_child(self, data):
        return self.post('account/getchildv2', json.dumps(data))

    def add_remove_child_credits(self, data):
        return self.post('account/addrmvcredit', json.dumps(data))

    def send_sms(self, data):
        return self.post('sms', json.dumps(data))

    def create_sms_campaign(self, data):
        return self.post('sms', json.dumps(data))

    def update_sms_campaign(self, data):
        id = str(data['id'])
        return self.put('sms/' + id, json.dumps(data))

    def send_bat_sms(self, data):
        id = str(data['id'])
        return self.get('sms/' + id, json.dumps(data))

    def get_campaigns_v2(self, data):
        type = data.get('type')
        status = data.get('status')
        page = data.get('page')
        page_limit = data.get('page_limit')
        if type is None and status is None and page is None and page_limit is None:
            return self.get('campaign/detailsv2/', '')
        else:
            return self.get('campaign/detailsv2/type/' + type + '/status/' + status + '/page/' + str(page) + '/page_limit/' + str(page_limit) + '/', '')
            return

    def get_campaign_v2(self, data):
        id = str(data['id'])
        return self.get('campaign/' + id + '/detailsv2/', '')

    def create_campaign(self, data):
        return self.post('campaign', json.dumps(data))

    def delete_campaign(self, data):
        id = str(data['id'])
        return self.delete('campaign/' + id, '')

    def update_campaign(self, data):
        id = str(data['id'])
        return self.put('campaign/' + id, json.dumps(data))

    def campaign_report_email(self, data):
        id = str(data['id'])
        return self.post('campaign/' + id + '/report', json.dumps(data))

    def campaign_recipients_export(self, data):
        id = str(data['id'])
        return self.post('campaign/' + id + '/recipients', json.dumps(data))

    def send_bat_email(self, data):
        id = str(data['id'])
        return self.post('campaign/' + id + '/test', json.dumps(data))

    def create_trigger_campaign(self, data):
        return self.post('campaign', json.dumps(data))

    def update_trigger_campaign(self, data):
        id = str(data['id'])
        return self.put('campaign/' + id, json.dumps(data))

    def share_campaign(self, data):
        return self.post('campaign/sharelinkv2', json.dumps(data))

    def update_campaign_status(self, data):
        id = str(data['id'])
        return self.put('campaign/' + id + '/updatecampstatus', json.dumps(data))

    def get_processes(self, data):
        return self.get('process', json.dumps(data))

    def get_process(self, data):
        id = str(data['id'])
        return self.get('process/' + id, '')

    def get_lists(self, data):
        return self.get('list', json.dumps(data))

    def get_list(self, data):
        id = str(data['id'])
        return self.get('list/' + id, '')

    def create_list(self, data):
        return self.post('list', json.dumps(data))

    def delete_list(self, data):
        id = str(data['id'])
        return self.delete('list/' + id, '')

    def update_list(self, data):
        id = str(data['id'])
        return self.put('list/' + id, json.dumps(data))

    def display_list_users(self, data):
        return self.post('list/display', json.dumps(data))

    def add_users_list(self, data):
        id = str(data['id'])
        return self.post('list/' + id + '/users', json.dumps(data))

    def delete_users_list(self, data):
        id = str(data['id'])
        return self.delete('list/' + id + '/delusers', json.dumps(data))

    def send_email(self, data):
        return self.post('email', json.dumps(data))

    def get_webhooks(self, data):
        return self.get('webhook', json.dumps(data))

    def get_webhook(self, data):
        id = str(data['id'])
        return self.get('webhook/' + id, '')

    def create_webhook(self, data):
        return self.post('webhook', json.dumps(data))

    def delete_webhook(self, data):
        id = str(data['id'])
        return self.delete('webhook/' + id, '')

    def update_webhook(self, data):
        id = str(data['id'])
        return self.put('webhook/' + id, json.dumps(data))

    def get_statistics(self, data):
        return self.post('statistics', json.dumps(data))

    def get_user(self, data):
        id = data['email']
        return self.get('user/' + id, '')

    def delete_user(self, data):
        id = data['email']
        return self.delete('user/' + id, '')

    def import_users(self, data):
        return self.post('user/import', json.dumps(data))

    def export_users(self, data):
        return self.post('user/export', json.dumps(data))

    def create_update_user(self, data):
        return self.post('user/createdituser', json.dumps(data))

    def get_attributes(self):
        return self.get('attribute', '')

    def get_attribute(self, data):
        type = data['type']
        return self.get('attribute/' + type, '')

    def create_attribute(self, data):
        return self.post('attribute', json.dumps(data))

    def delete_attribute(self, data):
        type = data['type']
        return self.post('attribute/' + type, json.dumps(data))

    def get_report(self, data):
        return self.post('report', json.dumps(data))

    def get_folders(self, data):
        return self.get('folder', json.dumps(data))

    def get_folder(self, data):
        id = str(data['id'])
        return self.get('folder/' + id, '')

    def create_folder(self, data):
        return self.post('folder', json.dumps(data))

    def delete_folder(self, data):
        id = str(data['id'])
        return self.delete('folder/' + id, '')

    def update_folder(self, data):
        id = str(data['id'])
        return self.put('folder/' + id, json.dumps(data))

    def delete_bounces(self, data):
        return self.post('bounces', json.dumps(data))

    def send_transactional_template(self, data):
        id = str(data['id'])
        return self.put('template/' + id, json.dumps(data))

    def create_template(self, data):
        return self.post('template', json.dumps(data))

    def update_template(self, data):
        id = str(data['id'])
        return self.put('template/' + id, json.dumps(data))

    def get_senders(self, data):
        return self.get('advanced', json.dumps(data))

    def create_sender(self, data):
        return self.post('advanced', json.dumps(data))

    def update_sender(self, data):
        id = str(data['id'])
        return self.put('advanced/' + id, json.dumps(data))

    def delete_sender(self, data):
        id = str(data['id'])
        return self.delete('advanced/' + id, '')