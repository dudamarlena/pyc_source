# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/reviewboard/webapi/tests/mixins_extra_data.py
# Compiled at: 2020-02-11 04:03:57
"""Mixins for adding extra_data unit tests for API resources."""
from __future__ import unicode_literals
import json
from djblets.features.testing import override_feature_checks
from djblets.webapi.errors import INVALID_FORM_DATA
from djblets.webapi.testing.decorators import webapi_test_template
from reviewboard.webapi.base import ExtraDataAccessLevel

class ExtraDataListMixin(object):
    """Mixin for adding extra_data tests for list resources."""

    @webapi_test_template
    def test_post_with_extra_data_simple(self):
        """Testing the POST <URL> API with extra_data.key=value"""
        self.load_fixtures(self.basic_post_fixtures)
        if self.basic_post_use_admin:
            self._login_user(admin=True)
        extra_fields = {b'extra_data.foo': 123, 
           b'extra_data.bar': 456, 
           b'extra_data.baz': b'', 
           b'ignored': b'foo'}
        url, mimetype, data, objs = self.setup_basic_post_test(self.user, False, None, True)
        data.update(extra_fields)
        with override_feature_checks(self.override_features):
            rsp = self.api_post(url, data, expected_mimetype=mimetype)
        self.assertEqual(rsp[b'stat'], b'ok')
        item_rsp = rsp[self.resource.item_result_key]
        obj = self.resource.model.objects.get(pk=item_rsp[b'id'])
        self.assertIn(b'foo', obj.extra_data)
        self.assertIn(b'bar', obj.extra_data)
        self.assertNotIn(b'baz', obj.extra_data)
        self.assertNotIn(b'ignored', obj.extra_data)
        self.assertEqual(obj.extra_data[b'foo'], extra_fields[b'extra_data.foo'])
        self.assertEqual(obj.extra_data[b'bar'], extra_fields[b'extra_data.bar'])
        return

    @webapi_test_template
    def test_post_with_extra_data_json(self):
        """Testing the POST <URL> API with extra_data:json"""
        self.load_fixtures(self.basic_post_fixtures)
        if self.basic_post_use_admin:
            self._login_user(admin=True)
        url, mimetype, data, objs = self.setup_basic_post_test(self.user, False, None, True)
        data[b'extra_data:json'] = json.dumps({b'foo': {b'bar': {b'num': 123, 
                             b'string': b'hi!', 
                             b'bool': True}}, 
           b'test': [
                   1, 2, 3], 
           b'not_saved': None})
        with override_feature_checks(self.override_features):
            rsp = self.api_post(url, data, expected_mimetype=mimetype)
        self.assertEqual(rsp[b'stat'], b'ok')
        item_rsp = rsp[self.resource.item_result_key]
        obj = self.resource.model.objects.get(pk=item_rsp[b'id'])
        self.assertIn(b'foo', obj.extra_data)
        self.assertIn(b'test', obj.extra_data)
        self.assertNotIn(b'not_saved', obj.extra_data)
        self.assertEqual(obj.extra_data[b'foo'], {b'bar': {b'num': 123, 
                    b'string': b'hi!', 
                    b'bool': True}})
        self.assertEqual(obj.extra_data[b'test'], [1, 2, 3])
        return

    @webapi_test_template
    def test_post_with_extra_data_json_patch(self):
        """Testing the POST <URL> API with extra_data:json-patch"""
        self.load_fixtures(self.basic_post_fixtures)
        if self.basic_post_use_admin:
            self._login_user(admin=True)
        url, mimetype, data, objs = self.setup_basic_post_test(self.user, False, None, True)
        data[b'extra_data:json-patch'] = json.dumps([
         {b'op': b'add', 
            b'path': b'/a', 
            b'value': {b'array': [
                                1, 2, 3]}},
         {b'op': b'add', 
            b'path': b'/a/b', 
            b'value': b'test'},
         {b'op': b'add', 
            b'path': b'/c', 
            b'value': None}])
        with override_feature_checks(self.override_features):
            rsp = self.api_post(url, data, expected_mimetype=mimetype)
        self.assertEqual(rsp[b'stat'], b'ok')
        item_rsp = rsp[self.resource.item_result_key]
        obj = self.resource.model.objects.get(pk=item_rsp[b'id'])
        self.assertIn(b'a', obj.extra_data)
        self.assertIn(b'c', obj.extra_data)
        self.assertEqual(obj.extra_data[b'a'], {b'array': [
                    1, 2, 3], 
           b'b': b'test'})
        self.assertIsNone(obj.extra_data[b'c'])
        return

    @webapi_test_template
    def test_post_with_private_extra_data_simple(self):
        """Testing the POST <URL> API with private extra_data.__key=value"""
        self.load_fixtures(self.basic_post_fixtures)
        if self.basic_post_use_admin:
            self._login_user(admin=True)
        extra_fields = {b'extra_data.__private_key': b'private_data'}
        url, mimetype, data, objs = self.setup_basic_post_test(self.user, False, None, True)
        data.update(extra_fields)
        with override_feature_checks(self.override_features):
            rsp = self.api_post(url, data, expected_mimetype=mimetype)
        self.assertEqual(rsp[b'stat'], b'ok')
        item_rsp = rsp[self.resource.item_result_key]
        obj = self.resource.model.objects.get(pk=item_rsp[b'id'])
        self.assertNotIn(b'__private_key', obj.extra_data)
        return


class ExtraDataItemMixin(object):
    """Mixin for adding extra_data tests for item resources."""

    @webapi_test_template
    def test_put_with_extra_data_in_simple_form(self):
        """Testing the PUT <URL> API with extra_data.key=value"""
        self.load_fixtures(getattr(self, b'basic_put_fixtures', []))
        if self.basic_put_use_admin:
            self._login_user(admin=True)
        extra_fields = {b'extra_data.foo': 123, 
           b'extra_data.bar': 456, 
           b'extra_data.baz': b'', 
           b'ignored': b'foo'}
        url, mimetype, data, obj, objs = self.setup_basic_put_test(self.user, False, None, True)
        data.update(extra_fields)
        with override_feature_checks(self.override_features):
            rsp = self.api_put(url, data, expected_mimetype=mimetype)
        self.assertEqual(rsp[b'stat'], b'ok')
        item_rsp = rsp[self.resource.item_result_key]
        obj = self.resource.model.objects.get(pk=item_rsp[b'id'])
        self.assertIn(b'foo', obj.extra_data)
        self.assertIn(b'bar', obj.extra_data)
        self.assertNotIn(b'baz', obj.extra_data)
        self.assertNotIn(b'ignored', obj.extra_data)
        self.assertEqual(obj.extra_data[b'foo'], extra_fields[b'extra_data.foo'])
        self.assertEqual(obj.extra_data[b'bar'], extra_fields[b'extra_data.bar'])
        return

    @webapi_test_template
    def test_put_with_private_extra_data_in_simple_form(self):
        """Testing the PUT <URL> API with private extra_data.__key=value"""
        self.load_fixtures(getattr(self, b'basic_put_fixtures', []))
        if self.basic_put_use_admin:
            self._login_user(admin=True)
        extra_fields = {b'extra_data.__private_key': b'private_data'}
        url, mimetype, data, obj, objs = self.setup_basic_put_test(self.user, False, None, True)
        data.update(extra_fields)
        with override_feature_checks(self.override_features):
            rsp = self.api_put(url, data, expected_mimetype=mimetype)
        self.assertEqual(rsp[b'stat'], b'ok')
        item_rsp = rsp[self.resource.item_result_key]
        obj = self.resource.model.objects.get(pk=item_rsp[b'id'])
        self.assertNotIn(b'__private_key', obj.extra_data)
        return

    @webapi_test_template
    def test_put_with_extra_data_json(self):
        """Testing the PUT <URL> API with extra_data:json"""
        self.load_fixtures(getattr(self, b'basic_put_fixtures', []))
        if self.basic_put_use_admin:
            self._login_user(admin=True)
        url, mimetype, data, obj, objs = self.setup_basic_put_test(self.user, False, None, True)
        obj.extra_data[b'removed'] = b'test'
        data = {b'extra_data:json': json.dumps({b'foo': {b'bar': {b'num': 123, 
                                                  b'string': b'hi!', 
                                                  b'bool': True}}, 
                                b'test': [
                                        1, 2, 3], 
                                b'removed': None})}
        with override_feature_checks(self.override_features):
            rsp = self.api_put(url, data, expected_mimetype=mimetype)
        self.assertEqual(rsp[b'stat'], b'ok')
        item_rsp = rsp[self.resource.item_result_key]
        obj = self.resource.model.objects.get(pk=item_rsp[b'id'])
        self.assertIn(b'foo', obj.extra_data)
        self.assertIn(b'test', obj.extra_data)
        self.assertNotIn(b'removed', obj.extra_data)
        self.assertEqual(obj.extra_data[b'foo'], {b'bar': {b'num': 123, 
                    b'string': b'hi!', 
                    b'bool': True}})
        self.assertEqual(obj.extra_data[b'test'], [1, 2, 3])
        return

    @webapi_test_template
    def test_put_with_extra_data_json_with_private_keys(self):
        """Testing the PUT <URL> API with extra_data:json with private keys"""
        self.load_fixtures(getattr(self, b'basic_put_fixtures', []))
        if self.basic_put_use_admin:
            self._login_user(admin=True)
        url, mimetype, data, obj, objs = self.setup_basic_put_test(self.user, False, None, True)
        data[b'extra_data:json'] = json.dumps({b'foo': {b'__bar': {b'num': 123, 
                               b'string': b'hi!', 
                               b'bool': True}, 
                    b'baz': 456}})
        with override_feature_checks(self.override_features):
            rsp = self.api_put(url, data, expected_mimetype=mimetype)
        self.assertEqual(rsp[b'stat'], b'ok')
        item_rsp = rsp[self.resource.item_result_key]
        obj = self.resource.model.objects.get(pk=item_rsp[b'id'])
        self.assertIn(b'foo', obj.extra_data)
        self.assertEqual(obj.extra_data[b'foo'], {b'baz': 456})
        return

    @webapi_test_template
    def test_put_with_extra_data_json_with_access_levels(self):
        """Testing the PUT <URL> API with extra_data:json with access levels"""

        def _access_cb(path):
            if path == ('parent', 'private'):
                return ExtraDataAccessLevel.ACCESS_STATE_PRIVATE
            else:
                if path == ('public-readonly', ):
                    return ExtraDataAccessLevel.ACCESS_STATE_PUBLIC_READONLY
                return ExtraDataAccessLevel.ACCESS_STATE_PUBLIC

        self.load_fixtures(getattr(self, b'basic_put_fixtures', []))
        if self.basic_put_use_admin:
            self._login_user(admin=True)
        url, mimetype, data, obj, objs = self.setup_basic_put_test(self.user, False, None, True)
        obj.extra_data = {b'public-readonly': b'orig'}
        obj.save()
        try:
            self.resource.extra_data_access_callbacks.register(_access_cb)
            data = {b'extra_data:json': json.dumps({b'parent': {b'private': 1}, 
                                    b'public-readonly': 2, 
                                    b'test': 3})}
            with override_feature_checks(self.override_features):
                rsp = self.api_put(url, data, expected_mimetype=mimetype)
        finally:
            self.resource.extra_data_access_callbacks.unregister(_access_cb)

        self.assertEqual(rsp[b'stat'], b'ok')
        item_rsp = rsp[self.resource.item_result_key]
        obj = self.resource.model.objects.get(pk=item_rsp[b'id'])
        self.assertEqual(obj.extra_data, {b'parent': {}, b'public-readonly': b'orig', 
           b'test': 3})
        return

    @webapi_test_template
    def test_put_with_extra_data_json_with_override_root(self):
        """Testing the PUT <URL> API with extra_data:json with attempting to
        override root of extra_data
        """
        self.load_fixtures(getattr(self, b'basic_put_fixtures', []))
        if self.basic_put_use_admin:
            self._login_user(admin=True)
        url, mimetype, data, obj, objs = self.setup_basic_put_test(self.user, False, None, True)
        obj.extra_data = {b'a': 1, 
           b'b': 2}
        obj.save()
        data[b'extra_data:json'] = json.dumps([1, 2, 3])
        with override_feature_checks(self.override_features):
            rsp = self.api_put(url, data, expected_status=400)
        self.assertEqual(rsp[b'stat'], b'fail')
        self.assertEqual(rsp[b'err'], {b'code': INVALID_FORM_DATA.code, 
           b'msg': b'One or more fields had errors'})
        self.assertEqual(rsp[b'fields'], {b'extra_data': [
                         b'extra_data:json cannot replace extra_data with a non-dictionary type']})
        obj = self.resource.model.objects.get(pk=obj.pk)
        self.assertEqual(obj.extra_data, {b'a': 1, 
           b'b': 2})
        return

    @webapi_test_template
    def test_put_with_extra_data_json_patch(self):
        """Testing the PUT <URL> API with extra_data:json-patch"""
        self.load_fixtures(getattr(self, b'basic_put_fixtures', []))
        if self.basic_put_use_admin:
            self._login_user(admin=True)
        url, mimetype, data, obj, objs = self.setup_basic_put_test(self.user, False, None, True)
        obj.extra_data = {b'a': 1, 
           b'b': {b'c': 2}}
        obj.save()
        data = {b'extra_data:json-patch': json.dumps([
                                    {b'op': b'add', 
                                       b'path': b'/b/d', 
                                       b'value': 3},
                                    {b'op': b'remove', 
                                       b'path': b'/a'},
                                    {b'op': b'copy', 
                                       b'from': b'/b/c', 
                                       b'path': b'/e'}])}
        with override_feature_checks(self.override_features):
            rsp = self.api_put(url, data, expected_mimetype=mimetype)
        self.assertEqual(rsp[b'stat'], b'ok')
        item_rsp = rsp[self.resource.item_result_key]
        obj = self.resource.model.objects.get(pk=item_rsp[b'id'])
        self.assertEqual(obj.extra_data, {b'b': {b'c': 2, 
                  b'd': 3}, 
           b'e': 2})
        return

    @webapi_test_template
    def test_put_with_extra_data_json_patch_with_private_keys(self):
        """Testing the PUT <URL> API with extra_data:json-patch with private
        keys
        """
        self.load_fixtures(getattr(self, b'basic_put_fixtures', []))
        if self.basic_put_use_admin:
            self._login_user(admin=True)
        url, mimetype, data, obj, objs = self.setup_basic_put_test(self.user, False, None, True)
        obj.extra_data = {b'a': 1, 
           b'b': {b'__c': 2}}
        obj.save()
        data[b'extra_data:json-patch'] = json.dumps([
         {b'op': b'remove', 
            b'path': b'/b/__c'}])
        with override_feature_checks(self.override_features):
            rsp = self.api_put(url, data, expected_status=400)
        self.assertEqual(rsp[b'stat'], b'fail')
        self.assertEqual(rsp[b'err'], {b'code': INVALID_FORM_DATA.code, 
           b'msg': b'One or more fields had errors'})
        self.assertEqual(rsp[b'fields'], {b'extra_data': [
                         b'Failed to patch JSON data: Cannot write to path "/b/__c" for patch entry 0']})
        obj = self.resource.model.objects.get(pk=obj.pk)
        self.assertEqual(obj.extra_data, {b'a': 1, 
           b'b': {b'__c': 2}})
        return

    @webapi_test_template
    def test_put_with_extra_data_json_patch_with_private_access_level(self):
        """Testing the PUT <URL> API with extra_data:json-patch with private
        access level
        """

        def _access_cb(path):
            if path == ('a', ):
                return ExtraDataAccessLevel.ACCESS_STATE_PRIVATE
            return ExtraDataAccessLevel.ACCESS_STATE_PUBLIC

        self.load_fixtures(getattr(self, b'basic_put_fixtures', []))
        if self.basic_put_use_admin:
            self._login_user(admin=True)
        url, mimetype, data, obj, objs = self.setup_basic_put_test(self.user, False, None, True)
        obj.extra_data = {b'a': 1}
        obj.save()
        try:
            self.resource.extra_data_access_callbacks.register(_access_cb)
            data[b'extra_data:json-patch'] = json.dumps([
             {b'op': b'add', 
                b'path': b'/b', 
                b'value': 1},
             {b'op': b'remove', 
                b'path': b'/a'}])
            with override_feature_checks(self.override_features):
                rsp = self.api_put(url, data, expected_status=400)
        finally:
            self.resource.extra_data_access_callbacks.unregister(_access_cb)

        self.assertEqual(rsp[b'stat'], b'fail')
        self.assertEqual(rsp[b'err'], {b'code': INVALID_FORM_DATA.code, 
           b'msg': b'One or more fields had errors'})
        self.assertEqual(rsp[b'fields'], {b'extra_data': [
                         b'Failed to patch JSON data: Cannot write to path "/a" for patch entry 1']})
        obj = self.resource.model.objects.get(pk=obj.pk)
        self.assertEqual(obj.extra_data, {b'a': 1})
        return

    @webapi_test_template
    def test_put_with_extra_data_json_patch_with_read_only_access_level(self):
        """Testing the PUT <URL> API with extra_data:json-patch with read-only
        access level
        """

        def _access_cb(path):
            if path == ('a', ):
                return ExtraDataAccessLevel.ACCESS_STATE_PUBLIC_READONLY
            return ExtraDataAccessLevel.ACCESS_STATE_PUBLIC

        self.load_fixtures(getattr(self, b'basic_put_fixtures', []))
        if self.basic_put_use_admin:
            self._login_user(admin=True)
        url, mimetype, data, obj, objs = self.setup_basic_put_test(self.user, False, None, True)
        obj.extra_data = {b'a': 1}
        obj.save()
        try:
            self.resource.extra_data_access_callbacks.register(_access_cb)
            data[b'extra_data:json-patch'] = json.dumps([
             {b'op': b'test', 
                b'path': b'/a', 
                b'value': 1},
             {b'op': b'copy', 
                b'from': b'/a', 
                b'path': b'/b'},
             {b'op': b'remove', 
                b'path': b'/a'}])
            with override_feature_checks(self.override_features):
                rsp = self.api_put(url, data, expected_status=400)
        finally:
            self.resource.extra_data_access_callbacks.unregister(_access_cb)

        self.assertEqual(rsp[b'stat'], b'fail')
        self.assertEqual(rsp[b'err'], {b'code': INVALID_FORM_DATA.code, 
           b'msg': b'One or more fields had errors'})
        self.assertEqual(rsp[b'fields'], {b'extra_data': [
                         b'Failed to patch JSON data: Cannot write to path "/a" for patch entry 2']})
        obj = self.resource.model.objects.get(pk=obj.pk)
        self.assertEqual(obj.extra_data, {b'a': 1})
        return

    @webapi_test_template
    def test_put_with_extra_data_json_patch_with_override_root(self):
        """Testing the PUT <URL> API with extra_data:json-patch with
        attempting to override root of extra_data
        """
        self.load_fixtures(getattr(self, b'basic_put_fixtures', []))
        if self.basic_put_use_admin:
            self._login_user(admin=True)
        url, mimetype, data, obj, objs = self.setup_basic_put_test(self.user, False, None, True)
        obj.extra_data = {b'a': 1, 
           b'b': 2}
        obj.save()
        data[b'extra_data:json-patch'] = json.dumps([
         {b'op': b'replace', 
            b'path': b'', 
            b'value': {b'new': b'values'}}])
        with override_feature_checks(self.override_features):
            rsp = self.api_put(url, data, expected_status=400)
        self.assertEqual(rsp[b'stat'], b'fail')
        self.assertEqual(rsp[b'err'], {b'code': INVALID_FORM_DATA.code, 
           b'msg': b'One or more fields had errors'})
        self.assertEqual(rsp[b'fields'], {b'extra_data': [
                         b'Failed to patch JSON data: Cannot write to path "" for patch entry 0']})
        obj = self.resource.model.objects.get(pk=obj.pk)
        self.assertEqual(obj.extra_data, {b'a': 1, 
           b'b': 2})
        return

    @webapi_test_template
    def test_get_with_private_extra_data_in_key_form(self):
        """Testing the GET <URL> API with private extra_data in __key form"""
        self.load_fixtures(getattr(self, b'basic_put_fixtures', []))
        if self.basic_get_use_admin:
            self._login_user(admin=True)
        extra_fields = {b'__private_key': b'private_data', 
           b'public_key': {b'__another_private_key': b'foo', 
                           b'another_public_key': b'bar'}}
        url, mimetype, item = self.setup_basic_get_test(self.user, False, None)
        obj = self.resource.model.objects.get(pk=item.id)
        obj.extra_data = extra_fields
        obj.save(update_fields=[b'extra_data'])
        with override_feature_checks(self.override_features):
            rsp = self.api_get(url, expected_mimetype=mimetype, expected_json=self.basic_get_returns_json)
        item_rsp = rsp[self.resource.item_result_key]
        self.assertNotIn(b'__private_key', item_rsp[b'extra_data'])
        self.assertNotIn(b'__another_private_key', item_rsp[b'extra_data'][b'public_key'])
        self.assertIn(b'another_public_key', item_rsp[b'extra_data'][b'public_key'])
        return