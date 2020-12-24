# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build\bdist.win-amd64\egg\tests\__init__.py
# Compiled at: 2017-09-26 22:42:09
__doc__ = ' Unittests for the pyqualtrics package\n'
import json, random, string, time, zipfile
from requests.exceptions import ConnectionError
from pyqualtrics import Qualtrics
from mock.mock import patch
import unittest, os
base_dir = os.path.dirname(os.path.abspath(__file__))

class MockResponse():

    def __init__(self, status_code=200, data=''):
        self.status_code = status_code
        self.text = data
        self.content = data

    def json(self):
        return json.loads(self.text)


class TestQualtrics(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.user = os.environ['QUALTRICS_USER']
        cls.token = os.environ['QUALTRICS_TOKEN']
        cls.qualtrics = Qualtrics(cls.user, cls.token)

    def setUp(self):
        self.library_id = os.environ['QUALTRICS_LIBRARY_ID']
        self.survey_id = os.environ.get('QUALTRICS_SURVEY_ID', None)
        self.message_id = os.environ.get('QUALTRICS_MESSAGE_ID', None)
        self.response_id = os.environ.get('QUALTRICS_RESPONSE_ID', None)
        return

    def test_str(self):
        self.assertEqual(str(self.qualtrics), self.user)

    def test_creation_errors(self):
        panel_id = self.qualtrics.createPanel(LibraryID='', Name='Hello', User='deadbeaf')
        self.assertIsNone(panel_id)
        self.assertIsNotNone(self.qualtrics.last_error_message)
        panel_id = self.qualtrics.createPanel(LibraryID='', Name='Hello')
        self.assertIsNone(panel_id)
        self.assertEqual(self.qualtrics.last_error_message, 'Invalid request. Missing or invalid parameter LibraryID.')

    def test_create_and_delete(self):
        panel_id = self.qualtrics.createPanel(LibraryID=self.library_id, Name='Test Panel created by pyqualtrics library (DELETE ME)')
        self.assertIsNone(self.qualtrics.last_error_message)
        self.assertIsNotNone(panel_id)
        self.assertIsNotNone(self.qualtrics.json_response)
        count = self.qualtrics.getPanelMemberCount(self.library_id, panel_id)
        self.assertEqual(count, 0)
        random_prefix = ('').join(random.choice(string.ascii_uppercase + string.digits) for _ in range(6))
        recipient_id = self.qualtrics.addRecipient(self.library_id, panel_id, FirstName='Fake', LastName='Subject', Email='PyQualtrics+%s@gmail.com' % random_prefix, ExternalDataRef=None, Language='EN', ED={'SubjectID': '123'})
        self.assertIsNone(self.qualtrics.last_error_message)
        self.assertIsNotNone(recipient_id)
        recipient = self.qualtrics.getRecipient(LibraryID=self.library_id, RecipientID=recipient_id)
        self.assertEqual(recipient['FirstName'], 'Fake')
        self.assertEqual(recipient['LastName'], 'Subject')
        self.assertEqual(recipient['Language'], 'EN')
        self.assertIsNone(recipient['ExternalDataReference'])
        self.assertEqual(recipient['EmbeddedData']['SubjectID'], '123')
        count = self.qualtrics.getPanelMemberCount(self.library_id, panel_id)
        self.assertEqual(count, 1)
        if self.survey_id is not None and self.message_id is not None:
            distribution_id = self.qualtrics.sendSurveyToIndividual(SendDate='2015-12-12 19:48:28', FromEmail='noreply@qemailserver.com', FromName='PyQualtrics Library', MessageID=self.message_id, MessageLibraryID=self.library_id, Subject='Why, hello there', SurveyID=self.survey_id, PanelID=panel_id, PanelLibraryID=self.library_id, RecipientID=recipient_id)
            self.assertIsNotNone(distribution_id)
            self.assertIsNone(self.qualtrics.last_error_message)
            self.assertIsNotNone(self.qualtrics.json_response)
            result = self.qualtrics.getDistributions(LibraryID=self.library_id, SurveyID=self.survey_id, DistributionID=distribution_id)
            self.assertIsNotNone(result)
            xml = self.qualtrics.getSurvey(SurveyID=self.survey_id)
            self.assertIsNotNone(xml)
            self.assertIsNone(self.qualtrics.json_response)
            self.assertIsNone(self.qualtrics.last_error_message)
            data = self.qualtrics.getLegacyResponseData(SurveyID=self.survey_id)
            self.assertIsNotNone(data)
            self.assertIsNotNone(self.qualtrics.json_response)
            self.assertIsNone(self.qualtrics.last_error_message)
        if self.response_id is not None and self.survey_id is not None:
            response = self.qualtrics.getResponse(SurveyID=self.survey_id, ResponseID=self.response_id)
            self.assertIsNotNone(response)
            self.assertIsNone(self.qualtrics.last_error_message)
            response = self.qualtrics.getResponse(SurveyID=self.survey_id, ResponseID='abc')
            self.assertIsNone(response)
            self.assertEqual(self.qualtrics.last_error_message, 'Invalid request. Missing or invalid parameter ResponseID.')
        result = self.qualtrics.removeRecipient(LibraryID=self.library_id, PanelID=panel_id, RecipientID=recipient_id)
        self.assertIsNone(self.qualtrics.last_error_message)
        self.assertEqual(result, True)
        count = self.qualtrics.getPanelMemberCount(self.library_id, panel_id)
        self.assertEqual(count, 0)
        result = self.qualtrics.deletePanel(LibraryID=self.library_id, PanelID=panel_id)
        self.assertEqual(result, True)
        self.assertIsNone(self.qualtrics.last_error_message)
        self.assertIsNotNone(self.qualtrics.json_response)
        return

    def test_send_survey_to_panel(self):
        panel_id = self.qualtrics.createPanel(LibraryID=self.library_id, Name='Test Panel for send_survey_to_panel pyqualtrics (DELETE ME)')
        random_prefix = ('').join(random.choice(string.ascii_uppercase + string.digits) for _ in range(6))
        recipient_id = self.qualtrics.addRecipient(self.library_id, panel_id, FirstName='Panel', LastName='Subject', Email='PyQualtrics+%s@gmail.com' % random_prefix, ExternalDataRef=None, Language='EN', ED={'SubjectID': '123'})
        email_distribution_id = self.qualtrics.sendSurveyToPanel(SendDate='2015-12-12 19:48:28', FromEmail='noreply@qemailserver.com', FromName='PyQualtrics Library', MessageID=self.message_id, MessageLibraryID=self.library_id, Subject='Why, hello there - sendSurveyToPanel', SurveyID=self.survey_id, PanelID=panel_id, PanelLibraryID=self.library_id, SentFromAddress=None, LinkType='Multiple')
        self.assertIsNotNone(email_distribution_id)
        self.qualtrics.deletePanel(self.library_id, panel_id)
        return

    def test_get_panels(self):
        result = self.qualtrics.getPanels(self.library_id)
        self.assertIsNotNone(result)

    def test_panel_errors(self):
        result = self.qualtrics.removeRecipient(LibraryID=self.library_id, PanelID='', RecipientID='')
        self.assertEqual(result, False)
        self.assertEqual(self.qualtrics.last_error_message, 'Invalid request. Missing or invalid parameter RecipientID.')

    def test_deletion_errors(self):
        result = self.qualtrics.deletePanel(LibraryID='', PanelID='', User='deadbeaf')
        self.assertEqual(result, False)
        self.assertIsNotNone(self.qualtrics.last_error_message)
        result = self.qualtrics.deletePanel(LibraryID='', PanelID='Hello')
        self.assertEqual(result, False)
        self.assertEqual(self.qualtrics.last_error_message, 'Invalid request. Missing or invalid parameter LibraryID.')

    def test_json_import(self):
        panel_id = self.qualtrics.importJsonPanel(self.library_id, Name='Panel for testing JSON Import', panel=[{'Email': 'pyqualtrics+1@gmail.com', 'FirstName': 'PyQualtrics', 'LastName': 'Library'}, {'Email': 'pyqualtrics+2@gmail.com', 'FirstName': 'PyQualtrics2', 'LastName': 'Library2'}])
        self.assertIsNone(self.qualtrics.last_error_message)
        self.assertIsNotNone(panel_id)
        self.assertIsNotNone(self.qualtrics.json_response)
        count = self.qualtrics.getPanelMemberCount(self.library_id, panel_id)
        self.assertEqual(count, 2)
        self.assertIsNone(self.qualtrics.last_error_message)
        self.assertIsNotNone(self.qualtrics.json_response)
        subjects = self.qualtrics.getPanel(self.library_id, panel_id)
        self.assertEqual(len(subjects), 2)
        self.assertEqual(subjects[0]['LastName'], 'Library')
        self.assertEqual(subjects[1]['FirstName'], 'PyQualtrics2')
        new_panel_id = self.qualtrics.importJsonPanel(self.library_id, Name='Panel for testing JSON Import', PanelID=panel_id, panel=[{'Email': 'pyqualtrics+3@gmail.com', 'FirstName': 'PyQualtrics', 'LastName': 'Library3'}, {'Email': 'pyqualtrics+4@gmail.com', 'FirstName': 'PyQualtrics2', 'LastName': 'Library4'}])
        count = self.qualtrics.getPanelMemberCount(self.library_id, panel_id)
        self.assertEqual(count, 4)
        self.assertEqual(new_panel_id, panel_id)
        self.assertIsNone(self.qualtrics.last_error_message)
        self.assertIsNotNone(self.qualtrics.json_response)
        result = self.qualtrics.importJsonPanel(self.library_id, Name='Panel for testing JSON Import', PanelID=panel_id, headers=[
         'FirstName', 'LastName'], panel=[{'FirstName': 'PyQualtrics', 'LastName': 'Library3'}, {'FirstName': 'PyQualtrics2', 'LastName': 'Library4'}])
        self.assertEqual(result, None)
        self.assertEqual(self.qualtrics.last_error_message, 'Invalid request. Missing or invalid parameter Email.')
        count = self.qualtrics.getPanelMemberCount(self.library_id, panel_id)
        self.assertEqual(count, 4)
        self.assertIsNone(self.qualtrics.last_error_message)
        self.assertIsNotNone(self.qualtrics.json_response)
        result = self.qualtrics.deletePanel(LibraryID=self.library_id, PanelID=panel_id)
        self.assertEqual(result, True)
        self.assertIsNone(self.qualtrics.last_error_message)
        self.assertIsNotNone(self.qualtrics.json_response)
        return

    def test_json_import_with_embedded_data(self):
        panel_id = self.qualtrics.importJsonPanel(self.library_id, Name='Panel for testing JSON Import', panel=[{'Email': 'pyqualtrics+1@gmail.com', 'FirstName': 'PyQualtrics', 'LastName': 'Library', 'SubjectID': 'SUBJ0001'}, {'Email': 'pyqualtrics+2@gmail.com', 'FirstName': 'PyQualtrics2', 'LastName': 'Library2'}], headers=[
         'Email', 'FirstName', 'LastName', 'ExternalRef', 'SubjectID'], AllED=1)
        self.assertIsNone(self.qualtrics.last_error_message)
        self.assertIsNotNone(panel_id)
        self.assertIsNotNone(self.qualtrics.json_response)
        count = self.qualtrics.getPanelMemberCount(self.library_id, panel_id)
        self.assertEqual(count, 2)
        self.assertIsNone(self.qualtrics.last_error_message)
        self.assertIsNotNone(self.qualtrics.json_response)
        subjects = self.qualtrics.getPanel(self.library_id, panel_id)
        self.assertEqual(len(subjects), 2)
        self.assertEqual(subjects[0]['LastName'], 'Library')
        self.assertEqual(subjects[1]['FirstName'], 'PyQualtrics2')
        self.assertEqual(subjects[0]['EmbeddedData']['SubjectID'], 'SUBJ0001')
        result = self.qualtrics.deletePanel(LibraryID=self.library_id, PanelID=panel_id)
        self.assertEqual(result, True)
        self.assertIsNone(self.qualtrics.last_error_message)
        self.assertIsNotNone(self.qualtrics.json_response)

    def test_import_survey_errors(self):
        result = self.qualtrics.importSurvey(ImportFormat='QSF', Name='Test survey import (DELETE ME - 1)', FileContents='123')
        self.assertFalse(result)
        self.assertEqual(self.qualtrics.last_error_message, 'Error parsing file: The file does not appear to be a valid survey')
        result = self.qualtrics.importSurvey(ImportFormat='_', Name='Test survey import (DELETE ME - 2)', FileContents='123')
        self.assertFalse(result)
        self.assertEqual(self.qualtrics.last_error_message, 'Invalid request. Missing or invalid parameter ImportFormat.')

    def test_import_survey(self):
        with open(os.path.join(base_dir, 'pyqualtrics.qsf')) as (fp):
            survey_id = self.qualtrics.importSurvey(ImportFormat='QSF', Name='Test survey import (DELETE ME - 3)', FileContents=fp.read())
        self.assertIsNotNone(survey_id)
        self.assertIsNone(self.qualtrics.last_error_message)
        time.sleep(2.0)
        self.assertIn(survey_id, self.qualtrics.getSurveys())
        self.assertIsNone(self.qualtrics.last_error_message)
        result = self.qualtrics.activateSurvey(SurveyID=survey_id)
        self.assertTrue(result)
        result = self.qualtrics.deactivateSurvey(SurveyID=survey_id)
        self.assertTrue(result)
        result = self.qualtrics.deleteSurvey(SurveyID=survey_id)
        self.assertTrue(result)

    def test_import_survey_from_url(self):
        survey_id = self.qualtrics.importSurvey(ImportFormat='QSF', Name='Test survey import (DELETE ME - curatend)', URL='https://github.com/Baguage/pyqualtrics/raw/master/tests/pyqualtrics.qsf')
        self.assertIsNone(self.qualtrics.last_error_message)
        self.assertIsNotNone(survey_id)
        self.assertIsNone(self.qualtrics.last_error_message)
        time.sleep(2.0)
        self.assertIn(survey_id, self.qualtrics.getSurveys())
        self.assertIsNone(self.qualtrics.last_error_message)
        result = self.qualtrics.deleteSurvey(SurveyID=survey_id)
        self.assertTrue(result)

    def test_delete_survey_fails(self):
        self.assertFalse(self.qualtrics.deleteSurvey(SurveyID='123'))

    def test_activate_survey_fails(self):
        self.assertFalse(self.qualtrics.activateSurvey(SurveyID='123'))
        self.assertFalse(self.qualtrics.deactivateSurvey(SurveyID='123'))

    def test_single_response_html(self):
        result = self.qualtrics.getSingleResponseHTML(SurveyID=self.survey_id, ResponseID=self.response_id)
        self.assertIsNotNone(result)
        self.assertTrue('DOCTYPE html PUBLIC' in result)

    def test_get_legacy_response_data(self):
        """
        WARNING!!!
        This test requires a partially completed response in "getLegacyData test" survey (SV_8pqqcl4sy2316ZL),
and it will closed after 6 month (max timeout allowed by Qualtrics). Thus every 6 month new
partially completed response should be created.
Use link https://nd.qualtrics.com/jfe/form/SV_8pqqcl4sy2316ZL and answer "Male". Don't answer the second question
        :return:
        """
        responses = self.qualtrics.getLegacyResponseData(SurveyID=self.survey_id)
        self.assertIsNotNone(responses)
        self.assertEqual(len(responses), 3)
        key, response = responses.popitem(last=False)
        self.assertEqual(response['SubjectID'], 'PY0001')
        self.assertEqual(response['Finished'], '1')
        self.assertEqual(response['Q1'], 1)
        self.assertEqual(response['Q2'], 3)
        key, response = responses.popitem(last=False)
        self.assertEqual(response['SubjectID'], '')
        self.assertEqual(response['Finished'], '1')
        self.assertEqual(response['Q1'], 1)
        self.assertEqual(response['Q2'], 3)
        key, response = responses.popitem(last=False)
        self.assertEqual(response['SubjectID'], 'TEST0001')
        self.assertEqual(response['Finished'], '1')
        self.assertEqual(response['Q1'], 2)
        self.assertEqual(response['Q2'], 1)
        responses = self.qualtrics.getLegacyResponseData(SurveyID=self.survey_id, ResponsesInProgress=1)
        self.assertIsNotNone(responses)
        self.assertEqual(len(responses), 1)
        for survey_session_id, response in iter(responses.items()):
            self.assertEqual(response['SubjectID'], '')
            self.assertEqual(response['Finished'], 0)
            self.assertEqual(response['Q1'], 1)
            self.assertEqual(response['Q2'], '')

    def test_get_legacy_response_data_wrong_last_response_id(self):
        responses = self.qualtrics.getLegacyResponseData(SurveyID=self.survey_id, LastResponseID='123')
        self.assertEqual(responses, None)
        self.assertEqual(self.qualtrics.last_error_message, 'Invalid request. Missing or invalid parameter LastResponseID.')
        return

    def test_get_response(self):
        response = self.qualtrics.getResponse(SurveyID=self.survey_id, ResponseID=self.response_id)
        self.assertIsNotNone(response)
        self.assertEqual(response['SubjectID'], 'PY0001')
        self.assertEqual(response['Finished'], '1')
        self.assertEqual(response['Q1'], 1)
        self.assertEqual(response['Q2'], 3)

    def test_get_response_wrong_response_id(self):
        response = self.qualtrics.getResponse(SurveyID=self.survey_id, ResponseID='AAAA')
        self.assertIsNone(response)
        self.assertEqual(self.qualtrics.last_error_message, 'Invalid request. Missing or invalid parameter ResponseID.')

    def test_get_response_deleted_response_id(self):
        response = self.qualtrics.getResponse(SurveyID=self.survey_id, ResponseID='R_1LjSIk8cLV7Y4eD')
        self.assertIsNone(response)
        self.assertEqual('Qualtrics error: ResponseID R_1LjSIk8cLV7Y4eD not in response (probably deleted)', self.qualtrics.last_error_message)

    def test_create_distribution(self):
        panel_id = self.qualtrics.createPanel(self.library_id, '(DELETE ME) Panel for testing distributions')
        distribution_id = self.qualtrics.createDistribution(SurveyID=self.survey_id, PanelID=panel_id, Description='Test distribution', PanelLibraryID=self.library_id)
        self.qualtrics.deletePanel(self.library_id, panel_id)
        self.assertIsNotNone(distribution_id)
        self.assertIsNone(self.qualtrics.last_error_message)

    def test_generate_unique_survey_link(self):
        panel_id = self.qualtrics.createPanel(self.library_id, '(DELETE ME) Panel for testing unique links')
        distribution_id = self.qualtrics.createDistribution(SurveyID=self.survey_id, PanelID=panel_id, Description='Test distribution', PanelLibraryID=self.library_id)
        link1 = self.qualtrics.generate_unique_survey_link(SurveyID=self.survey_id, LibraryID=self.library_id, PanelID=panel_id, DistributionID=distribution_id, FirstName='Py', LastName='Qualtrics', Email='pyqualtrics@gmail.com')
        self.assertIsNotNone(link1)
        self.assertIsNone(self.qualtrics.last_error_message)
        link2 = self.qualtrics.generate_unique_survey_link(SurveyID=self.survey_id, LibraryID=self.library_id, PanelID=panel_id, DistributionID=distribution_id, FirstName='Py', LastName='Qualtrics', Email='pyqualtrics@gmail.com')
        self.assertIsNotNone(link2)
        self.assertNotEqual(link1, link2)
        self.assertIsNone(self.qualtrics.last_error_message)
        link3 = self.qualtrics.generate_unique_survey_link(SurveyID=self.survey_id, LibraryID=self.library_id, PanelID=panel_id, DistributionID=distribution_id, FirstName='Py', LastName='Qualtrics', Email='pyqualtrics@gmail.com', EmbeddedData={'SubjectID': 'TEST0001'})
        self.assertIsNotNone(link3)
        self.assertNotEqual(link1, link3)
        self.assertNotEqual(link2, link3)
        self.assertIsNone(self.qualtrics.last_error_message)
        link4 = self.qualtrics.generate_unique_survey_link(SurveyID='', LibraryID=self.library_id, PanelID=panel_id, DistributionID=distribution_id, FirstName='Py', LastName='Qualtrics', Email='pyqualtrics@gmail.com')
        self.assertIsNone(link4)
        self.assertIsNotNone(self.qualtrics.last_error_message)
        link5 = self.qualtrics.generate_unique_survey_link(SurveyID=self.survey_id, LibraryID='', PanelID=panel_id, DistributionID=distribution_id, FirstName='Py', LastName='Qualtrics', Email='pyqualtrics@gmail.com')
        self.assertIsNone(link5)
        self.assertIsNotNone(self.qualtrics.last_error_message)
        self.qualtrics.deletePanel(self.library_id, panel_id)
        self.assertIsNone(self.qualtrics.last_error_message)

    def test_import_responses_and_update_embedded_data(self):
        with open(os.path.join(base_dir, 'pyqualtrics-ed.qsf')) as (fp):
            survey_id = self.qualtrics.importSurvey(ImportFormat='QSF', Name='Test importResponses (DELETE ME - 4)', FileContents=fp.read())
        self.assertIsNotNone(survey_id)
        self.assertIsNone(self.qualtrics.last_error_message)
        with open(os.path.join(base_dir, 'response.csv')) as (fp):
            result = self.qualtrics.importResponses(survey_id, FileContents=fp.read())
        self.assertIsNone(self.qualtrics.last_error_message)
        self.assertTrue(result)
        responses = self.qualtrics.getLegacyResponseData(survey_id)
        self.assertIsNone(self.qualtrics.last_error_message)
        self.assertEqual(len(responses), 1)
        for response_id in responses:
            response = responses[response_id]
            self.assertEqual(response['Finished'], '1')
            self.assertEqual(response['Q1'], 1)
            self.assertEqual(response['Q2'], 1)
            self.qualtrics.updateResponseEmbeddedData(survey_id, response_id, ED={'TEST': 'Yay!'})

        responses = self.qualtrics.getLegacyResponseData(survey_id)
        for response_id in responses:
            response = responses[response_id]
            self.assertEqual(response['TEST'], 'Yay!')
            self.assertIn(response['Q_ID'], '')

        self.qualtrics.deleteSurvey(survey_id)

    def test_import_responses_as_dict(self):
        with open(os.path.join(base_dir, 'pyqualtrics.qsf')) as (fp):
            survey_id = self.qualtrics.importSurvey(ImportFormat='QSF', Name='Test responses_as_dict import (DELETE ME - 4)', FileContents=fp.read())
        self.assertIsNotNone(survey_id)
        self.assertIsNone(self.qualtrics.last_error_message)
        result = self.qualtrics.importResponsesAsDict(survey_id, [{'startDate': '', 'endDate': '', 'QID1': 1, 'QID2': 2}])
        self.assertIsNone(self.qualtrics.last_error_message)
        self.assertTrue(result)
        responses = self.qualtrics.getLegacyResponseData(survey_id)
        self.assertIsNone(self.qualtrics.last_error_message)
        self.assertEqual(len(responses), 1)
        for response_id in responses:
            response = responses[response_id]
            self.assertEqual(response['Finished'], '1')
            self.assertEqual(response['Q1'], 1)
            self.assertEqual(response['Q2'], 2)

        self.qualtrics.deleteSurvey(survey_id)

    def test_connection_error_invalid_url(self):
        url = self.qualtrics.url
        self.qualtrics.url = 'http://blablabla.bla'
        responses = self.qualtrics.getLegacyResponseData(SurveyID=self.survey_id)
        self.assertIsNone(responses)
        self.assertIsNone(self.qualtrics.last_status_code)
        self.assertIn('Max retries exceeded with url', self.qualtrics.last_error_message)
        self.qualtrics.url = url

    def test_connection_error_invalid_ip_address(self):
        url = self.qualtrics.url
        self.qualtrics.url = 'http://0.0.0.777'
        responses = self.qualtrics.getLegacyResponseData(SurveyID=self.survey_id)
        self.qualtrics.url = url
        self.assertIsNone(responses)
        self.assertIsNone(self.qualtrics.last_status_code)
        self.assertIn('Max retries exceeded with url', self.qualtrics.last_error_message)

    def test_not_a_json_document_google_com(self):
        qualtrics = Qualtrics(self.user, '123')
        qualtrics.url = 'https://google.com'
        result = qualtrics.getLegacyResponseData(SurveyID=self.survey_id)
        self.assertEqual(qualtrics.last_error_message, 'Unexpected response from Qualtrics: not a JSON document')
        self.assertIsNone(qualtrics.json_response)
        self.assertIsNone(result)

    def test_ssl_error(self):
        qualtrics = Qualtrics(self.user, '123')
        qualtrics.url = 'https://129.74.247.12/'
        result = qualtrics.getLegacyResponseData(SurveyID=self.survey_id)
        self.assertIn('129.74.247.12', qualtrics.last_error_message)
        qualtrics.requests_kwargs = {'verify': False}
        result = qualtrics.getLegacyResponseData(SurveyID=self.survey_id)
        self.assertNotIn('CERTIFICATE_VERIFY_FAILED', qualtrics.last_error_message)

    def test_get_survey_unauthorized(self):
        qualtrics = Qualtrics(self.user, '123')
        result = qualtrics.getSurvey(self.survey_id)
        self.assertEqual(result, None)
        self.assertEqual(qualtrics.last_error_message, 'API Error: HTTP Code 401 (Unauthorized)')
        return

    def test_get_survey_no_permissions(self):
        result = self.qualtrics.getSurvey('SV_8FTHsivtrc1eG2h')
        self.assertEqual(result, None)
        self.assertEqual(self.qualtrics.last_error_message, 'This survey is Unknown to this user account.')
        return

    def test_CreateResponseExportCsv(self):
        responseExportId = self.qualtrics.CreateResponseExport(Qualtrics.CSV_FORMAT, self.survey_id)
        self.assertIsNone(self.qualtrics.last_error_message)
        self.assertIsNotNone(responseExportId)
        status = 'in progress'
        url = None
        while status == 'in progress':
            time.sleep(1)
            status, url = self.qualtrics.GetResponseExportProgress(responseExportId)

        self.assertEqual(status, 'complete')
        self.assertIsNotNone(url)
        self.assertIn('https://', url)
        fp = self.qualtrics.GetResponseExportFile(url)
        self.assertEqual(self.qualtrics.last_error_message, None)
        self.assertIsNotNone(fp)
        row = next(fp).strip()
        self.assertEqual(row, 'ResponseID,ResponseSet,IPAddress,StartDate,EndDate,RecipientLastName,RecipientFirstName,RecipientEmail,ExternalDataReference,Finished,Status,SubjectID,Q1,Q2,LocationLatitude,LocationLongitude,LocationAccuracy')
        row = next(fp)
        row = next(fp)
        row = next(fp).strip()
        self.assertEqual(row, 'R_2sPsOsGV0GSrLJb,Default Response Set,129.74.117.12,2016-04-08 12:04:00,2016-04-08 12:04:00,,,,,1,4,PY0001,1,3,,,-1')
        fp = self.qualtrics.GetResponseExportFile(responseExportId)
        row = next(fp).strip()
        self.assertEqual(row, 'ResponseID,ResponseSet,IPAddress,StartDate,EndDate,RecipientLastName,RecipientFirstName,RecipientEmail,ExternalDataReference,Finished,Status,SubjectID,Q1,Q2,LocationLatitude,LocationLongitude,LocationAccuracy')
        row = next(fp)
        row = next(fp)
        row = next(fp).strip()
        self.assertEqual(row, 'R_2sPsOsGV0GSrLJb,Default Response Set,129.74.117.12,2016-04-08 12:04:00,2016-04-08 12:04:00,,,,,1,4,PY0001,1,3,,,-1')
        return

    def test_CreateResponseExportJson(self):
        responseExportId = self.qualtrics.CreateResponseExport(Qualtrics.JSON_FORMAT, self.survey_id)
        self.assertIsNone(self.qualtrics.last_error_message)
        self.assertIsNotNone(responseExportId)
        status = 'in progress'
        url = None
        while status == 'in progress':
            time.sleep(1)
            status, url = self.qualtrics.GetResponseExportProgress(responseExportId)

        self.assertEqual(status, 'complete')
        self.assertIsNotNone(url)
        self.assertIn('https://', url)
        fp = self.qualtrics.GetResponseExportFile(url)
        self.assertEqual(self.qualtrics.last_error_message, None)
        self.assertIsNotNone(fp)
        data_json = fp.read()
        data = json.loads(data_json)
        self.assertEqual(data['responses'][0]['SubjectID'], 'PY0001')
        self.assertEqual(data['responses'][1]['SubjectID'], '')
        self.assertEqual(data['responses'][2]['SubjectID'], 'TEST0001')
        self.assertEqual(data['responses'][2]['Q1'], '2')
        self.assertEqual(data['responses'][2]['Q2'], '1')
        return

    def test_CreateResponseExportXml(self):
        responseExportId = self.qualtrics.CreateResponseExport(Qualtrics.XML_FORMAT, self.survey_id)
        self.assertIsNone(self.qualtrics.last_error_message)
        self.assertIsNotNone(responseExportId)
        status = 'in progress'
        url = None
        while status == 'in progress':
            time.sleep(1)
            status, url = self.qualtrics.GetResponseExportProgress(responseExportId)

        self.assertEqual(status, 'complete')
        self.assertIsNotNone(url)
        self.assertIn('https://', url)
        fp = self.qualtrics.GetResponseExportFile(url)
        self.assertEqual(self.qualtrics.last_error_message, None)
        self.assertIsNotNone(fp)
        data_xml = fp.read()
        self.assertIn('<SubjectID>PY0001</SubjectID>', data_xml)
        return

    def test_CreateResponseExport_includedQuestionIds(self):
        responseExportId = self.qualtrics.CreateResponseExport(Qualtrics.CSV_FORMAT, self.survey_id, includedQuestionIds=[
         'QID1'])
        self.assertIsNone(self.qualtrics.last_error_message)
        (self.assertIsNotNone(self.qualtrics.last_data),)
        self.assertIsNotNone(responseExportId)
        status = 'in progress'
        url = None
        while status == 'in progress':
            time.sleep(1)
            status, url = self.qualtrics.GetResponseExportProgress(responseExportId)

        self.assertEqual(status, 'complete')
        self.assertIsNotNone(url)
        self.assertIn('https://', url)
        fp = self.qualtrics.GetResponseExportFile(url)
        self.assertEqual(self.qualtrics.last_error_message, None)
        self.assertIsNone(self.qualtrics.last_data)
        self.assertEqual(self.qualtrics.last_url, url)
        self.assertIsNotNone(fp)
        row = next(fp).strip()
        self.assertEqual(row, 'ResponseID,ResponseSet,IPAddress,StartDate,EndDate,RecipientLastName,RecipientFirstName,RecipientEmail,ExternalDataReference,Finished,Status,Q1,LocationLatitude,LocationLongitude,LocationAccuracy')
        return

    def test_CreateResponseExport_parameters(self):
        responseExportId = self.qualtrics.CreateResponseExport(Qualtrics.CSV_FORMAT, self.survey_id, includedQuestionIds='["QID1"]', limit=1, lastResponseId=self.response_id)
        self.assertIsNone(self.qualtrics.last_error_message)
        (self.assertIsNotNone(self.qualtrics.last_data),)
        self.assertIsNotNone(responseExportId)
        status = 'in progress'
        url = None
        while status == 'in progress':
            time.sleep(1)
            status, url = self.qualtrics.GetResponseExportProgress(responseExportId)

        self.assertEqual(status, 'complete')
        self.assertIsNotNone(url)
        self.assertIn('https://', url)
        fp = self.qualtrics.GetResponseExportFile(url)
        self.assertEqual(self.qualtrics.last_error_message, None)
        self.assertIsNone(self.qualtrics.last_data)
        self.assertEqual(self.qualtrics.last_url, url)
        self.assertIsNotNone(fp)
        row = next(fp).strip()
        self.assertEqual(row, 'ResponseID,ResponseSet,IPAddress,StartDate,EndDate,RecipientLastName,RecipientFirstName,RecipientEmail,ExternalDataReference,Finished,Status,Q1,LocationLatitude,LocationLongitude,LocationAccuracy')
        row = next(fp)
        row = next(fp)
        row = next(fp).strip()
        self.assertEqual(row, 'R_Xj2NRqjlA2oxBgB,Default Response Set,,2016-04-19 23:19:41,2016-04-19 23:19:54,,,,,1,1,1,41.642807006836,-86.075302124023,-1')
        try:
            row = next(fp)
        except StopIteration:
            pass
        else:
            self.fail('More that one response is returned')

        return

    def test_CreateResponseExport_useLabels(self):
        responseExportId = self.qualtrics.CreateResponseExport(Qualtrics.CSV_FORMAT, self.survey_id, includedQuestionIds='["QID1"]', useLabels=True)
        self.assertIsNone(self.qualtrics.last_error_message)
        (self.assertIsNotNone(self.qualtrics.last_data),)
        self.assertIsNotNone(responseExportId)
        status = 'in progress'
        url = None
        while status == 'in progress':
            time.sleep(1)
            status, url = self.qualtrics.GetResponseExportProgress(responseExportId)

        self.assertEqual(status, 'complete')
        self.assertIsNotNone(url)
        self.assertIn('https://', url)
        fp = self.qualtrics.GetResponseExportFile(url)
        self.assertEqual(self.qualtrics.last_error_message, None)
        self.assertIsNone(self.qualtrics.last_data)
        self.assertEqual(self.qualtrics.last_url, url)
        self.assertIsNotNone(fp)
        row = next(fp).strip()
        self.assertEqual(row, 'ResponseID,ResponseSet,IPAddress,StartDate,EndDate,RecipientLastName,RecipientFirstName,RecipientEmail,ExternalDataReference,Finished,Status,Q1,LocationLatitude,LocationLongitude,LocationAccuracy')
        row = next(fp)
        row = next(fp)
        row = next(fp).strip()
        self.assertEqual(row, 'R_2sPsOsGV0GSrLJb,Default Response Set,129.74.117.12,2016-04-08 12:04:00,2016-04-08 12:04:00,,,,,1,4,Male,,,-1')
        return

    @patch('pyqualtrics.requests.get')
    def test_GetResponseExportProgress_percentComplete(self, get_func):
        data = '{"meta": {"httpStatus": "200 - OK", "requestId": "f53927df-d5d8-45eb-b6e3-de5542c7cd94"}, "result": {"status": "in progress", "percentComplete": 57.0,"file": "https://survey.qualtrics.com/API/v3/responseexports/ES_btvq507dddg6dcnvsq18tn0tl/file"}}'
        get_func.return_value = MockResponse(status_code=200, data=data)
        status, msg = self.qualtrics.GetResponseExportProgress('sdfasdfdsf')
        self.assertEqual(status, 'in progress')
        self.assertEqual(msg, 57.0)
        self.assertEqual(self.qualtrics.last_error_message, None)
        return

    def test_CreateResponseExport_fail(self):
        responseExportId = self.qualtrics.CreateResponseExport('csv', '123')
        self.assertIsNone(responseExportId)
        self.assertEqual(self.qualtrics.last_error_message, 'Invalid surveyId parameter.')

    def test_CreateResponseExport_fail_2(self):
        qualtrics = Qualtrics('234', '123')
        responseExportId = qualtrics.CreateResponseExport('csv', self.survey_id)
        self.assertIsNone(responseExportId)
        self.assertEqual(qualtrics.last_error_message, 'Unrecognized X-API-TOKEN.')

    @patch('pyqualtrics.requests.post')
    def test_CreateResponseExport_mailformed_response(self, get_func):
        get_func.return_value = MockResponse(status_code=200, data='')
        qualtrics = Qualtrics('234', '123')
        responseExportId = qualtrics.CreateResponseExport('csv', self.survey_id)
        self.assertIsNone(responseExportId)
        self.assertIn('Mailformed response from server:', qualtrics.last_error_message)

    def test_GetResponseExportProgress_fail(self):
        status, msg = self.qualtrics.GetResponseExportProgress('sdfasdfdsf')
        self.assertEqual(status, 'servfail')
        self.assertEqual(msg, 'Export id not found')
        self.assertEqual(self.qualtrics.last_error_message, 'Export id not found')

    def test_GetResponseExportProgress_fail_2(self):
        qualtrics = Qualtrics('234', '123')
        status, msg = qualtrics.GetResponseExportProgress('sdfasdfdsf')
        self.assertEqual(status, 'servfail')
        self.assertEqual(msg, 'Unrecognized X-API-TOKEN.')
        self.assertEqual(qualtrics.last_error_message, 'Unrecognized X-API-TOKEN.')

    @patch('pyqualtrics.requests.get')
    def test_GetResponseExportProgress_fail_3(self, get_func):
        get_func.return_value = MockResponse(status_code=200, data='')
        status, msg = self.qualtrics.GetResponseExportProgress('sdfasdfdsf')
        self.assertEqual(status, 'servfail')
        self.assertIn('Mailformed server response:', msg)
        self.assertIn('Mailformed server response:', self.qualtrics.last_error_message)

    @patch('pyqualtrics.requests.get')
    def test_GetResponseExportProgress_fail_4(self, get_func):
        get_func.return_value = MockResponse(status_code=200, data='{"result": ""}')
        status, msg = self.qualtrics.GetResponseExportProgress('sdfasdfdsf')
        self.assertEqual(status, 'servfail')
        self.assertEqual(msg, 'Mailformed server response: string indices must be integers')
        self.assertEqual(self.qualtrics.last_error_message, 'Mailformed server response: string indices must be integers')

    def test_GetResponseExportFile_fail(self):
        result = self.qualtrics.GetResponseExportFile('sdfasdfdsf')
        self.assertEqual(result, None)
        self.assertEqual(self.qualtrics.last_error_message, 'Export id not found')
        return

    def test_GetResponseExportFile_fail_2(self):
        qualtrics = Qualtrics('234', '123')
        result = qualtrics.GetResponseExportFile('kkkkkkkk')
        self.assertEqual(result, None)
        self.assertEqual(qualtrics.last_error_message, 'Unrecognized X-API-TOKEN.')
        return

    @patch('pyqualtrics.requests.get')
    def test_GetResponseExportFile_fail_bad_zip_file(self, get_func):
        get_func.return_value = MockResponse(status_code=200, data='')
        qualtrics = Qualtrics('234', '123')
        responseExportId = qualtrics.GetResponseExportFile('kkkkkkkk')
        self.assertIsNone(responseExportId)
        self.assertEqual(qualtrics.last_error_message, 'File is not a zip file')

    def test_DownloadResponseExportFileCsv(self):
        responseExportId = self.qualtrics.CreateResponseExport(Qualtrics.CSV2013_FORMAT, self.survey_id)
        self.assertIsNotNone(responseExportId)
        self.assertIsNotNone(responseExportId)
        status = 'in progress'
        url = None
        while status == 'in progress':
            time.sleep(1)
            status, url = self.qualtrics.GetResponseExportProgress(responseExportId)

        self.assertEqual(status, 'complete')
        self.assertIsNotNone(url)
        self.assertIn('https://', url)
        result = self.qualtrics.DownloadResponseExportFile(url, 'test.zip')
        self.assertEqual(self.qualtrics.last_error_message, None)
        self.assertTrue(result)
        with open('test.zip', 'rb') as (fp):
            archive = zipfile.ZipFile(fp)
            self.assertEqual(archive.namelist()[0], 'getLegacyResponseData test.csv')
        return

    def test_DownloadResponseExportFile_fail(self):
        result = self.qualtrics.DownloadResponseExportFile('bla-blah', 'bla.zip')
        self.assertEqual(self.qualtrics.last_error_message, 'Export id not found')
        self.assertEqual(result, None)
        return

    def test_request3_notimplemented(self):
        self.assertRaises(NotImplementedError, self.qualtrics.request3, '123', method='trace')

    @patch('pyqualtrics.requests.get')
    def test_request3_mock_connection_error(self, get_func):
        get_func.side_effect = ConnectionError('Connection Error')
        status, msg = self.qualtrics.GetResponseExportProgress('123')
        self.assertEqual(msg, 'Connection Error')
        self.assertEqual(status, 'servfail')

    @patch('pyqualtrics.requests.get')
    def test_request3_mailformed_response_from_server_3(self, get_func):
        mock_response = MockResponse(status_code=400)
        get_func.return_value = mock_response
        response = self.qualtrics.request3('123', method='get')
        self.assertEqual(self.qualtrics.last_error_message, 'HTTP Code 400')
        self.assertEqual(response, None)
        return

    def tearDown(self):
        pass

    @classmethod
    def tearDownClass(cls):
        for survey_id, survey in iter(cls.qualtrics.getSurveys().items()):
            if '(DELETE ME' in survey['SurveyName']:
                print 'Deleting survey %s' % survey['SurveyName']
                cls.qualtrics.deleteSurvey(SurveyID=survey_id)


if __name__ == '__main__':
    unittest.main()