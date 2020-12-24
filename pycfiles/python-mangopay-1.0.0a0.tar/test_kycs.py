# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/thoas/Sites/Python/ulule/python-mangopay/tests/test_kycs.py
# Compiled at: 2015-06-08 06:37:42
from .resources import Document, Page, KYC
from .test_base import BaseTest
import responses, base64, sys, os

class KYCSTest(BaseTest):

    @responses.activate
    def test_create_documents(self):
        self.mock_natural_user()
        self.mock_legal_user()
        self.register_mock([
         {'method': responses.POST, 
            'url': 'https://api.sandbox.mangopay.com/v2/chouette/users/1169420/KYC/documents', 
            'body': {'Id': '1173359', 
                     'Tag': 'custom tag', 
                     'CreationDate': 1384450979, 
                     'Type': 'IDENTITY_PROOF', 
                     'Status': 'CREATED', 
                     'RefusedReasonType': None, 
                     'RefusedReasonMessage': None}, 
            'status': 200},
         {'method': responses.POST, 
            'url': 'https://api.sandbox.mangopay.com/v2/chouette/users/1169419/KYC/documents', 
            'body': {'Id': '1173360', 
                     'Tag': 'custom tag', 
                     'CreationDate': 1384450979, 
                     'Type': 'IDENTITY_PROOF', 
                     'Status': 'CREATED', 
                     'RefusedReasonType': None, 
                     'RefusedReasonMessage': None}, 
            'status': 200},
         {'method': responses.PUT, 
            'url': 'https://api.sandbox.mangopay.com/v2/chouette/users/1169420/KYC/documents/1173359', 
            'body': {'Id': '1173359', 
                     'Tag': 'My CNI', 
                     'CreationDate': 1382630599, 
                     'Type': 'IDENTITY_PROOF', 
                     'Status': 'VALIDATION_ASKED', 
                     'RefusedReasonType': None, 
                     'RefusedReasonMessage': None}, 
            'status': 200},
         {'method': responses.GET, 
            'url': 'https://api.sandbox.mangopay.com/v2/chouette/users/1169420/KYC/documents/1173359', 
            'body': {'Id': '1173359', 
                     'Tag': 'My CNI', 
                     'CreationDate': 1382630599, 
                     'Type': 'IDENTITY_PROOF', 
                     'Status': 'VALIDATION_ASKED', 
                     'RefusedReasonType': None, 
                     'RefusedReasonMessage': None}, 
            'status': 200},
         {'method': responses.POST, 
            'url': 'https://api.sandbox.mangopay.com/v2/chouette/users/1169420/KYC/documents', 
            'body': {'Id': '1173360', 
                     'Tag': 'My CNI', 
                     'CreationDate': 1384451319, 
                     'Type': 'IDENTITY_PROOF', 
                     'Status': 'VALIDATION_ASKED', 
                     'RefusedReasonType': None, 
                     'RefusedReasonMessage': None}, 
            'status': 200},
         {'method': responses.GET, 
            'url': 'https://api.sandbox.mangopay.com/v2/chouette/users/1169420/KYC/documents?user_id=1169420', 
            'body': [
                   {'Id': '1173360', 
                      'Tag': 'My CNI', 
                      'CreationDate': 1384451319, 
                      'Type': 'IDENTITY_PROOF', 
                      'Status': 'VALIDATION_ASKED', 
                      'RefusedReasonType': None, 
                      'RefusedReasonMessage': None}], 
            'status': 200, 
            'match_querystring': True},
         {'method': responses.GET, 
            'url': 'https://api.sandbox.mangopay.com/v2/chouette/users/1169420/KYC/documents?per_page=1&user_id=1169420&page=2', 
            'body': [
                   {'Id': '1173359', 
                      'Tag': 'custom tag', 
                      'CreationDate': 1384450979, 
                      'Type': 'IDENTITY_PROOF', 
                      'Status': 'CREATED', 
                      'RefusedReasonType': None, 
                      'RefusedReasonMessage': None},
                   {'Id': '1173359', 
                      'Tag': 'custom tag', 
                      'CreationDate': 1384450979, 
                      'Type': 'IDENTITY_PROOF', 
                      'Status': 'CREATED', 
                      'RefusedReasonType': None, 
                      'RefusedReasonMessage': None}], 
            'status': 200, 
            'match_querystring': True},
         {'method': responses.GET, 
            'url': 'https://api.sandbox.mangopay.com/v2/chouette/KYC/documents', 
            'body': [
                   {'Id': '1167831', 
                      'Tag': 'My CNI', 
                      'CreationDate': 1382630599, 
                      'Type': 'IDENTITY_PROOF', 
                      'Status': 'VALIDATED', 
                      'RefusedReasonType': None, 
                      'RefusedReasonMessage': None},
                   {'Id': '1263680', 
                      'Tag': 'My CNI', 
                      'CreationDate': 1582830854, 
                      'Type': 'REGISTRATION_PROOF', 
                      'Status': 'VALIDATED', 
                      'RefusedReasonType': None, 
                      'RefusedReasonMessage': None}], 
            'status': 200, 
            'match_querystring': True},
         {'method': responses.GET, 
            'url': 'https://api.sandbox.mangopay.com/v2/chouette/KYC/documents?per_page=2&page=1', 
            'body': [
                   {'Id': '1167831', 
                      'Tag': 'My CNI', 
                      'CreationDate': 1382630599, 
                      'Type': 'IDENTITY_PROOF', 
                      'Status': 'VALIDATED', 
                      'RefusedReasonType': None, 
                      'RefusedReasonMessage': None},
                   {'Id': '1263680', 
                      'Tag': 'My CNI', 
                      'CreationDate': 1582830854, 
                      'Type': 'REGISTRATION_PROOF', 
                      'Status': 'VALIDATED', 
                      'RefusedReasonType': None, 
                      'RefusedReasonMessage': None}], 
            'status': 200, 
            'match_querystring': True}])
        params = {'type': 'IDENTITY_PROOF', 
           'tag': 'custom tag', 
           'user': self.legal_user}
        document1 = Document(**params)
        self.assertIsNone(document1.get_pk())
        document1.save()
        self.assertIsInstance(document1, Document)
        for key, value in params.items():
            self.assertEqual(getattr(document1, key), value)

        self.assertIsNotNone(document1.get_pk())
        previous_pk = document1.get_pk()
        document1.status = 'VALIDATION_ASKED'
        document1.save()
        self.assertEqual(previous_pk, document1.get_pk())
        self.assertEqual(document1.status, 'VALIDATION_ASKED')
        retrieved_document = Document.get(document1.id, **{'user_id': self.legal_user.get_pk()})
        self.assertIsNotNone(retrieved_document.get_pk())
        self.assertIsInstance(retrieved_document, Document)
        self.assertEqual(getattr(retrieved_document, 'id'), document1.get_pk())
        documents = Document.all(**{'user_id': self.legal_user.get_pk()})
        self.assertIsInstance(documents, list)
        self.assertEqual(len(documents), 1)
        for document in documents:
            self.assertIsInstance(document, Document)

        params = {'type': 'IDENTITY_PROOF', 
           'tag': 'custom tag', 
           'user': self.legal_user}
        document2 = Document(**params)
        document2.save()
        Document.all(page=2, per_page=1, **{'user_id': self.legal_user.get_pk()})
        self.assertEqual(len(documents), 1)
        params = {'type': 'IDENTITY_PROOF', 
           'tag': 'custom tag', 
           'user': self.natural_user}
        document3 = Document(**params)
        document3.save()
        paginated_documents_all = KYC.all(page=1, per_page=2)
        self.assertEqual(len(paginated_documents_all), 2)
        return

    @responses.activate
    def test_create_pages(self):
        self.mock_legal_user()
        file_path = os.path.join(os.path.dirname(__file__), 'images', 'image.jpg')
        with open(file_path, 'rb') as (image_file):
            encoded_string = base64.b64encode(image_file.read())
        decoded_string = encoded_string if sys.version_info < (3, 0) else encoded_string.decode('utf-8')
        self.register_mock([
         {'method': responses.POST, 
            'url': 'https://api.sandbox.mangopay.com/v2/chouette/users/1169420/KYC/documents', 
            'body': {'Id': '1173359', 
                     'Tag': 'custom tag', 
                     'CreationDate': 1384450979, 
                     'Type': 'IDENTITY_PROOF', 
                     'Status': 'CREATED', 
                     'RefusedReasonType': None, 
                     'RefusedReasonMessage': None}, 
            'status': 200},
         {'method': responses.POST, 
            'url': 'https://api.sandbox.mangopay.com/v2/chouette/users/1169420/KYC/documents/1173359/pages', 
            'body': {'File': decoded_string}, 
            'status': 200}])
        params = {'type': 'IDENTITY_PROOF', 
           'tag': 'custom tag', 
           'user': self.legal_user}
        document = Document(**params)
        document.save()
        params = {'file': encoded_string, 
           'user': self.legal_user, 
           'document': document}
        page = Page(**params)
        self.assertIsNone(page.get_pk())
        page.save()
        self.assertIsInstance(page, Page)
        for key, value in params.items():
            self.assertEqual(getattr(page, key), value)

        return