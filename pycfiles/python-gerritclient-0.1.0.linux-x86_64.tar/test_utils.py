# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/machin/.virtualenvs/twine/lib/python2.7/site-packages/gerritclient/tests/unit/common/test_utils.py
# Compiled at: 2017-04-21 23:53:12
from oslotest import base as oslo_base
from gerritclient.common import utils

class TestUtils(oslo_base.BaseTestCase):

    def test_get_display_data_single(self):
        columns = ('id', 'name')
        data = {'id': 1, 'name': 'test_name'}
        self.assertEqual(utils.get_display_data_single(fields=columns, data=data), [
         1, 'test_name'])

    def test_get_display_data_single_with_non_existent_field(self):
        columns = ('id', 'name', 'non-existent')
        data = {'id': 1, 'name': 'test_name'}
        self.assertEqual(utils.get_display_data_single(fields=columns, data=data), [
         1, 'test_name', None])
        return

    def test_get_display_data_multi_wo_sorting(self):
        columns = ('id', 'name')
        data = [{'id': 1, 'name': 'test_name_1'}, {'id': 2, 'name': 'test_name_2'}]
        self.assertEqual(utils.get_display_data_multi(fields=columns, data=data), [
         [
          1, 'test_name_1'], [2, 'test_name_2']])

    def test_get_display_data_multi_w_sorting(self):
        columns = ('id', 'name', 'severity_level')
        data = [{'id': 3, 'name': 'twitter', 'severity_level': 'error'}, {'id': 15, 'name': 'google', 'severity_level': 'warning'}, {'id': 2, 'name': 'amazon', 'severity_level': 'error'}, {'id': 17, 'name': 'facebook', 'severity_level': 'note'}]
        self.assertEqual(utils.get_display_data_multi(fields=columns, data=data, sort_by=[
         'name']), [
         [
          2, 'amazon', 'error'],
         [
          17, 'facebook', 'note'],
         [
          15, 'google', 'warning'],
         [
          3, 'twitter', 'error']])
        self.assertEqual(utils.get_display_data_multi(fields=columns, data=data, sort_by=[
         'severity_level', 'id']), [
         [
          2, 'amazon', 'error'],
         [
          3, 'twitter', 'error'],
         [
          17, 'facebook', 'note'],
         [
          15, 'google', 'warning']])