# uncompyle6 version 3.6.7
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/ahqapiclient/resources/incident.py
# Compiled at: 2017-08-23 10:41:46
# Size of source mod 2**32: 4193 bytes
__doc__ = '\n{\n    type: spam\n    complainant: no-reply@abusix.org\n    handled_on: null\n    client: 2999550572\n    date: 2013-04-05T22:19:05Z\n    report: {\n        storage: {\n            type: imap\n            params: [\n                {key: mailbox, value: Archive/2013-04-22}\n                {key: uid, value: 106108}\n            ]\n        }\n        send_date: 2013-04-05T22:19:05Z\n        received_date: 2013-04-05T22:19:05Z\n        format: marf\n    }\n    resources: {\n        incident_part: [\n            {key: original-envelope-id, value: 1uoeYp-4ftuc0-In}\n            {key: feedback-type, value: abuse}\n        ]\n        evidence_part: [\n            {\n                key: received\n                value: from ip-178-201-130-108.unitymediagroup.de ...\n            }\n            {\n                key: from\n                value: "Clarissa Campos" <bangsld@classprod.com>\n            }\n        ]\n        ip: [\n            {\n                source: incident\n                version: 4\n                hex: b2c9826c\n                value: 178.201.130.108\n            }\n        ]\n    }\n}\n'
from ahqapiclient.resources import Resource

class Incident(Resource):

    def __init__(self, http_client):
        super(Incident, self).__init__('/incidents', http_client)

    def make_incident_doc(self):
        return {'client': None, 
         'type': None, 
         'complainant': None, 
         'complaint_source': None, 
         'date': None, 
         'handled_on': None, 
         'report': {'storage': {'type': None, 
                                'params': []}, 
                    
                    'format': None, 
                    'received_date': None, 
                    'send_date': None}, 
         
         'resources': {'ip': [], 
                       'incident_part': [], 
                       'evidence_part': [], 
                       'malware': {}}, 
         
         'product_category': None, 
         'customer_type': None, 
         'brand_name': None, 
         'customer_number': None, 
         'resolver_data': {}, 
         'contract_id': None, 
         'contract_data': None}

    def create_incident(self, client, type, complainant, complaint_source, date, handled_on, report, resources, product_category, customer_type, brand_name, customer_number, resolver_data, contract_id, contract_data):
        return self.post(path=self.rurl(), data={'client': client, 
         'type': type, 
         'complainant': complainant, 
         'complaint_source': complaint_source, 
         'date': date, 
         'handled_on': handled_on, 
         'report': report, 
         'resources': resources, 
         'product_category': product_category, 
         'customer_type': customer_type, 
         'brand_name': brand_name, 
         'customer_number': customer_number, 
         'resolver_data': resolver_data, 
         'contract_id': contract_id, 
         'contract_data': contract_data})

    def get_incident(self, _id):
        return self.get(path=self.rurl(_id))

    def get_incidents(self, date_from, date_to, limit=10, offset=0, query='', include_handled=0, sort='date:desc', raw=False):
        return self.get(path=self.rurl(), params={'date_from': date_from, 
         'date_to': date_to, 
         'limit': limit, 
         'offset': offset, 
         'query': query, 
         'include_handled': include_handled, 
         'sort': sort}, raw=raw)

    def total(self, date_from, date_to):
        total = self.get_incidents(date_from, date_to, 0, 0, '', 0, 'date:desc', True)
        try:
            return total.headers['x-total']
        except KeyError:
            return