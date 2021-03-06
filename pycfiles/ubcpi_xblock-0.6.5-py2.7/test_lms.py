# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.11-x86_64/egg/ubcpi/test/test_lms.py
# Compiled at: 2015-08-31 13:55:15
import json, os
from ddt import ddt, file_data
from django.core.exceptions import PermissionDenied
from django.test import TestCase
from mock import patch, Mock
from workbench.test_utils import scenario, XBlockHandlerTestCaseMixin
from ubcpi.persistence import Answers, VOTE_KEY, RATIONALE_KEY

@ddt
class LmsTest(XBlockHandlerTestCaseMixin, TestCase):

    @scenario(os.path.join(os.path.dirname(__file__), 'data/basic_scenario.xml'), user_id='Bob')
    def test_render_student_view(self, xblock):
        frag = self.runtime.render(xblock, 'student_view')
        self.assertNotEqual(frag.body_html().find('Question:'), -1)

    @patch('ubcpi.persistence.get_answers_for_student', return_value=Answers([{VOTE_KEY: 0, RATIONALE_KEY: 'my rationale'}]))
    @scenario(os.path.join(os.path.dirname(__file__), 'data/basic_scenario.xml'), user_id='Bob')
    def test_render_student_view_with_original_answer(self, xblock, mock):
        frag = self.runtime.render(xblock, 'student_view')
        self.assertNotEqual(frag.body_html().find('"other_answers":'), -1)

    @patch('ubcpi.persistence.get_answers_for_student', return_value=Answers([{VOTE_KEY: 0, RATIONALE_KEY: 'my rationale'}, {VOTE_KEY: 1, RATIONALE_KEY: 'my revised rationale'}]))
    @scenario(os.path.join(os.path.dirname(__file__), 'data/basic_scenario.xml'), user_id='Bob')
    def test_render_student_view_with_revised_answer(self, xblock, mock):
        frag = self.runtime.render(xblock, 'student_view')
        self.assertEqual(frag.body_html().find('"other_answers":'), -1)
        self.assertNotEqual(frag.body_html().find('"correct_answer":'), -1)

    @patch('ubcpi.ubcpi.get_other_answers')
    @file_data('data/submit_answer.json')
    @scenario(os.path.join(os.path.dirname(__file__), 'data/basic_scenario.xml'), user_id='Bob')
    def test_submit_answer(self, xblock, data, mock):
        mock.return_value = data['expect1']['other_answers']
        resp = self.request(xblock, 'submit_answer', json.dumps(data['post1']), response_format='json')
        self.assertEqual(resp, data['expect1'])
        answers = xblock.get_answers_for_student()
        self.assertTrue(answers.has_revision(0))
        self.assertFalse(answers.has_revision(1))
        self.assertEqual(answers.get_rationale(0), data['post1']['rationale'])
        self.assertEqual(xblock.stats['original'][data['post1']['q']], 1)
        resp = self.request(xblock, 'submit_answer', json.dumps(data['post2']), response_format='json')
        self.assertEqual(resp, data['expect2'])
        answers = xblock.get_answers_for_student()
        self.assertTrue(answers.has_revision(0))
        self.assertTrue(answers.has_revision(1))
        self.assertEqual(answers.get_rationale(0), data['post1']['rationale'])
        self.assertEqual(answers.get_rationale(1), data['post2']['rationale'])
        self.assertEqual(xblock.stats['original'][data['post1']['q']], 1)
        self.assertEqual(xblock.stats['revised'][data['post2']['q']], 1)

    @file_data('data/submit_answer_errors.json')
    @scenario(os.path.join(os.path.dirname(__file__), 'data/basic_scenario.xml'), user_id='Bob')
    def test_submit_answer_errors(self, xblock, data):
        with self.assertRaises(PermissionDenied):
            self.request(xblock, 'submit_answer', json.dumps(data['post1']), response_format='json')

    @scenario(os.path.join(os.path.dirname(__file__), 'data/basic_scenario.xml'), user_id='Bob')
    def test_get_stats(self, xblock):
        stats = {'revised': {'1': 1}, 'original': {'0': 1}}
        xblock.stats = stats
        resp = self.request(xblock, 'get_stats', '{}', response_format='json')
        self.assertEqual(resp, stats)

    @patch('ubcpi.ubcpi.PeerInstructionXBlock.resource_string')
    @scenario(os.path.join(os.path.dirname(__file__), 'data/basic_scenario.xml'), user_id='Bob')
    def test_get_asset(self, xblock, mock):
        mock.return_value = 'test'
        resp = self.request(xblock, 'get_asset', 'f=test.html', request_method='POST')
        self.assertEqual(resp, 'test')

    @scenario(os.path.join(os.path.dirname(__file__), 'data/basic_scenario.xml'), user_id='Bob')
    def test_get_student_item_dict(self, xblock):
        student_item = xblock.get_student_item_dict()
        self.assertEqual(student_item, {'student_id': 'Bob', 
           'item_id': '.ubcpi.d3.u0', 
           'course_id': 'edX/Enchantment_101/April_1', 
           'item_type': 'ubcpi'})
        xblock.scope_ids = Mock()
        xblock.scope_ids.usage_id = 'usage_id'
        xblock.scope_ids.user_id = None
        student_item = xblock.get_student_item_dict()
        self.assertEqual(student_item, {'student_id': None, 
           'item_id': 'usage_id', 
           'course_id': 'edX/Enchantment_101/April_1', 
           'item_type': 'ubcpi'})
        xblock.course_id = 'course 101'
        xblock.xmodule_runtime = Mock()
        xblock.xmodule_runtime.anonymous_student_id = 'anonymous'
        student_item = xblock.get_student_item_dict()
        self.assertEqual(student_item, {'student_id': 'anonymous', 
           'item_id': 'usage_id', 
           'course_id': 'course 101', 
           'item_type': 'ubcpi'})
        student_item = xblock.get_student_item_dict('anonymous_1')
        self.assertEqual(student_item, {'student_id': 'anonymous_1', 
           'item_id': 'usage_id', 
           'course_id': 'course 101', 
           'item_type': 'ubcpi'})
        return

    @scenario(os.path.join(os.path.dirname(__file__), 'data/basic_scenario.xml'), user_id='Bob')
    def test_has_dynamic_children(self, xblock):
        self.assertFalse(xblock.has_dynamic_children())

    @scenario(os.path.join(os.path.dirname(__file__), 'data/basic_scenario.xml'), user_id='Bob')
    def test_max_score(self, xblock):
        self.assertEqual(xblock.max_score(), 1)

    @scenario(os.path.join(os.path.dirname(__file__), 'data/basic_scenario.xml'), user_id='Bob')
    def test_get_asset_url(self, xblock):
        self.assertEqual(xblock.get_asset_url('http://example.com/image'), 'http://example.com/image', 'non asset URL should return as it is')
        self.assertEqual(xblock.get_asset_url('/static/cat.jpg'), '/static/cat.jpg', 'in workbench env, it should return as it it')
        xblock.xmodule_runtime = Mock()
        for_branch = Mock(return_value='/c4x://test/course/')
        make_asset_key = Mock()
        make_asset_key.for_branch = for_branch
        xblock.course_id = Mock()
        xblock.course_id.make_asset_key = Mock(return_value=make_asset_key)
        self.assertEqual(xblock.get_asset_url('/static/cat.jpg'), '/c4x://test/course/cat.jpg', 'in edx env, it should return converted asset URL')
        for_branch = Mock(return_value='c4x://test/course/')
        make_asset_key = Mock()
        make_asset_key.for_branch = for_branch
        xblock.course_id = Mock()
        xblock.course_id.make_asset_key = Mock(return_value=make_asset_key)
        self.assertEqual(xblock.get_asset_url('/static/cat.jpg'), '/c4x://test/course/cat.jpg', 'in edx env, it should return converted asset URL')

    def check_fields(self, xblock, data):
        for key, value in data.iteritems():
            self.assertIsNotNone(getattr(xblock, key))
            self.assertEqual(getattr(xblock, key), value)