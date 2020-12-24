# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/svdgraaf/Projects/nl.focusmedia/application/eloqua/lib.py
# Compiled at: 2013-02-19 10:25:59
from eloqua import settings
import requests, base64, json

class EloquaBaseClient(object):
    headers = ''
    base_url = settings.BASE_URL

    def __init__(self):
        key = ('{site}\\{username}:{password}').format(site=settings.SITE, username=settings.USERNAME, password=settings.PASSWORD)
        authKey = base64.b64encode(key)
        self.headers = {'Content-Type': 'application/json', 'Authorization': 'Basic ' + authKey}

    def get(self, identifier):
        """Return the asset by the given id"""
        return self._get_by_id(identifier)

    def _get_by_id(self, identifier):
        url = self.base_url + '/' + str(identifier)
        response = requests.get(url, headers=self.headers)
        return response.json()

    def _delete_by_id(self, identifier):
        url = self.base_url + '/' + str(identifier)
        response = requests.delete(url, headers=self.headers)
        if response.status_code == 200:
            return True
        else:
            return False

    def delete(self, identifier):
        """Deletes the asset by the given id"""
        return self._delete_by_id(identifier)


class EloquaClient(EloquaBaseClient):
    headers = ''
    base_url = settings.BASE_URL

    @property
    def emails(self):
        return EloquaEmailClient()

    @property
    def contacts(self):
        return EloquaContactsClient()

    @property
    def landingpages(self):
        return EloquaLandingPagesClient()


class EloquaEmailClient(EloquaBaseClient):
    base_url = settings.BASE_URL + '/assets/email'

    def create(self, name, subject, body, body_plaintext=None, is_tracked=False, folder_id=None, sender_name=None, sender_email=None, reply_to_email=None, reply_to_name=None):
        """Creates an email with the given parameters, returns a json representation"""
        payload = {'htmlContent': {'html': body, 
                           'type': 'RawHtmlContent'}, 
           'sendPlainTextOnly': False, 
           'name': name, 
           'subject': subject, 
           'id': None, 
           'isTracked': is_tracked}
        if folder_id:
            payload['folderId'] = folder_id
        if body_plaintext:
            payload['body_plaintext'] = body_plaintext
        if sender_email:
            payload['senderEmail'] = sender_email
        if sender_name:
            payload['senderName'] = sender_name
        if reply_to_email:
            payload['replyToEmail'] = reply_to_email
        if reply_to_name:
            payload['replyToName'] = reply_to_name
        print payload
        r = requests.post(self.base_url, data=json.dumps(payload), headers=self.headers)
        if r.status_code == 201:
            return r.json()
        else:
            raise Exception('error: %s' % r)
            return


class EloquaContactsClient(EloquaBaseClient):
    base_url = settings.BASE_URL + '/data/contact'

    def search(self, query, page=1, count=100, depth='complete'):
        """Search all contacts for given email query, eg:

            from eloqua.lib import *
            e = EloquaClient()
            e.contacts.search('foobar@example.com')
                {u'elements': [{u'createdAt': u'1327661283',
                u'currentStatus': u'Awaiting action',
                u'depth': u'complete',
                u'emailAddress': u'foobar@example.com',
                ...

        """
        url = self.base_url + 's'
        payload = {'search': query, 
           'page': page, 
           'count': count, 
           'depth': depth}
        r = requests.get(url, params=payload, headers=self.headers)
        return r.json()