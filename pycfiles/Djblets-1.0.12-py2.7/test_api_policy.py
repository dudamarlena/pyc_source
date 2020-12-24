# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.11-x86_64/egg/djblets/webapi/tests/test_api_policy.py
# Compiled at: 2019-06-12 01:17:17
from __future__ import unicode_literals
from django.utils import six
from djblets.testing.testcases import TestCase
from djblets.webapi.resources.base import WebAPIResource
from djblets.webapi.resources.mixins.api_tokens import ResourceAPITokenMixin
from djblets.webapi.resources.root import RootResource
from djblets.webapi.models import BaseWebAPIToken

class PolicyTestResource(ResourceAPITokenMixin, WebAPIResource):
    policy_id = b'test'


class SomeObjectResource(ResourceAPITokenMixin, WebAPIResource):
    policy_id = b'someobject'


root_resource = RootResource([
 SomeObjectResource()])

class APIPolicyWebAPIToken(BaseWebAPIToken):

    @classmethod
    def get_root_resource(self):
        return root_resource


class APIPolicyTests(TestCase):
    """Tests API policy through WebAPITokens."""

    def setUp(self):
        super(APIPolicyTests, self).setUp()
        self.resource = PolicyTestResource()

    def test_default_policy(self):
        """Testing API policy enforcement with default policy"""
        self.assert_policy({}, allowed_methods=[
         b'HEAD', b'GET', b'POST', b'PATCH', b'PUT', b'DELETE'])

    def test_global_allow_all(self):
        """Testing API policy enforcement with *.allow=*"""
        self.assert_policy({b'*': {b'allow': [
                           b'*']}}, allowed_methods=[
         b'HEAD', b'GET', b'POST', b'PATCH', b'PUT', b'DELETE'])

    def test_global_block_all(self):
        """Testing API policy enforcement with *.block=*"""
        self.assert_policy({b'*': {b'block': [
                           b'*']}}, blocked_methods=[
         b'HEAD', b'GET', b'POST', b'PATCH', b'PUT', b'DELETE'])

    def test_global_block_all_and_resource_allow_all(self):
        """Testing API policy enforcement with *.block=* and
        <resource>.*.allow=*
        """
        self.assert_policy({b'*': {b'block': [
                           b'*']}, 
           b'test': {b'*': {b'allow': [
                                     b'*']}}}, allowed_methods=[
         b'HEAD', b'GET', b'POST', b'PATCH', b'PUT', b'DELETE'])

    def test_global_allow_all_and_resource_block_all(self):
        """Testing API policy enforcement with *.allow=* and
        <resource>.*.block=*
        """
        self.assert_policy({b'*': {b'allow': [
                           b'*']}, 
           b'test': {b'*': {b'block': [
                                     b'*']}}}, blocked_methods=[
         b'HEAD', b'GET', b'POST', b'PATCH', b'PUT', b'DELETE'])

    def test_global_block_all_and_resource_all_allow_methods(self):
        """Testing API policy enforcement with *.block=* and
        <resource>.*.allow=[methods]
        """
        self.assert_policy({b'*': {b'block': [
                           b'*']}, 
           b'test': {b'*': {b'allow': [
                                     b'GET', b'PUT']}}}, allowed_methods=[
         b'GET', b'PUT'], blocked_methods=[
         b'HEAD', b'POST', b'PATCH', b'DELETE'])

    def test_global_allow_all_and_resource_all_block_specific(self):
        """Testing API policy enforcement with *.allow=* and
        <resource>.*.block=[methods]
        """
        self.assert_policy({b'*': {b'allow': [
                           b'*']}, 
           b'test': {b'*': {b'block': [
                                     b'GET', b'PUT']}}}, allowed_methods=[
         b'HEAD', b'POST', b'PATCH', b'DELETE'], blocked_methods=[
         b'GET', b'PUT'])

    def test_resource_block_all_and_allow_methods(self):
        """Testing API policy enforcement with <resource>.*.block=* and
        <resource>.*.allow=[methods] for specific methods
        """
        self.assert_policy({b'test': {b'*': {b'block': [
                                     b'*'], 
                            b'allow': [
                                     b'GET', b'PUT']}}}, allowed_methods=[
         b'GET', b'PUT'], blocked_methods=[
         b'HEAD', b'POST', b'PATCH', b'DELETE'])

    def test_resource_allow_all_and_block_methods(self):
        """Testing API policy enforcement with <resource>.*.allow=* and
        <resource>.*.block=[methods] for specific methods
        """
        self.assert_policy({b'test': {b'*': {b'allow': [
                                     b'*'], 
                            b'block': [
                                     b'GET', b'PUT']}}}, allowed_methods=[
         b'HEAD', b'POST', b'DELETE'], blocked_methods=[
         b'GET', b'PUT'])

    def test_id_allow_all(self):
        """Testing API policy enforcement with <resource>.<id>.allow=*"""
        self.assert_policy({b'test': {b'42': {b'allow': [
                                      b'*']}}}, resource_id=42, allowed_methods=[
         b'HEAD', b'GET', b'POST', b'PUT', b'DELETE'])

    def test_id_block_all(self):
        """Testing API policy enforcement with <resource>.<id>.block=*"""
        policy = {b'test': {b'42': {b'block': [
                                      b'*']}}}
        self.assert_policy(policy, resource_id=42, blocked_methods=[
         b'HEAD', b'GET', b'POST', b'PUT', b'DELETE'])
        self.assert_policy(policy, resource_id=100, allowed_methods=[
         b'HEAD', b'GET', b'POST', b'PUT', b'DELETE'])

    def test_resource_block_all_and_id_allow_all(self):
        """Testing API policy enforcement with <resource>.*.block=* and
        <resource>.<id>.allow=*
        """
        policy = {b'test': {b'*': {b'block': [
                                     b'*']}, 
                     b'42': {b'allow': [
                                      b'*']}}}
        self.assert_policy(policy, resource_id=42, allowed_methods=[
         b'HEAD', b'GET', b'POST', b'PUT', b'DELETE'])
        self.assert_policy(policy, resource_id=100, blocked_methods=[
         b'HEAD', b'GET', b'POST', b'PUT', b'DELETE'])

    def test_resource_allow_all_and_id_block_all(self):
        """Testing API policy enforcement with <resource>.<id>.allow=* and
        <resource>.<id>.block=*
        """
        policy = {b'test': {b'*': {b'allow': [
                                     b'*']}, 
                     b'42': {b'block': [
                                      b'*']}}}
        self.assert_policy(policy, resource_id=42, blocked_methods=[
         b'HEAD', b'GET', b'POST', b'PUT', b'DELETE'])
        self.assert_policy(policy, resource_id=100, allowed_methods=[
         b'HEAD', b'GET', b'POST', b'PUT', b'DELETE'])

    def test_global_block_all_and_id_allow_all(self):
        """Testing API policy enforcement with *.<id>.block=* and
        <resource>.<id>.allow=*
        """
        self.assert_policy({b'*': {b'block': [
                           b'*']}, 
           b'test': {b'42': {b'allow': [
                                      b'*']}}}, resource_id=42, allowed_methods=[
         b'HEAD', b'GET', b'POST', b'PUT', b'DELETE'])

    def test_global_allow_all_and_id_block_all(self):
        """Testing API policy enforcement with *.<id>.allow=* and
        <resource>.<id>.block=*"""
        policy = {b'*': {b'allow': [
                           b'*']}, 
           b'test': {b'42': {b'block': [
                                      b'*']}}}
        self.assert_policy(policy, resource_id=42, blocked_methods=[
         b'HEAD', b'GET', b'POST', b'PUT', b'DELETE'])
        self.assert_policy(policy, resource_id=100, allowed_methods=[
         b'HEAD', b'GET', b'POST', b'PUT', b'DELETE'])

    def test_policy_methods_conflict(self):
        """Testing API policy enforcement with methods conflict"""
        self.assert_policy({b'test': {b'*': {b'allow': [
                                     b'*'], 
                            b'block': [
                                     b'*']}}}, blocked_methods=[
         b'HEAD', b'GET', b'POST', b'PUT', b'DELETE'])

    def assert_policy(self, policy, allowed_methods=[], blocked_methods=[], resource_id=None):
        if resource_id is not None:
            resource_id = six.text_type(resource_id)
        for method in allowed_methods:
            allowed = self.resource.is_resource_method_allowed(policy, method, resource_id)
            if not allowed:
                self.fail(b'Expected %s to be allowed, but was blocked' % method)

        for method in blocked_methods:
            allowed = self.resource.is_resource_method_allowed(policy, method, resource_id)
            if allowed:
                self.fail(b'Expected %s to be blocked, but was allowed' % method)

        return


class APIPolicyValidationTests(TestCase):
    """Tests API policy validation."""

    def test_empty(self):
        """Testing BaseWebAPIToken.validate_policy with empty policy"""
        APIPolicyWebAPIToken.validate_policy({})

    def test_not_object(self):
        """Testing BaseWebAPIToken.validate_policy without JSON object"""
        self.assertRaisesValidationError(b'The policy must be a JSON object.', APIPolicyWebAPIToken.validate_policy, [])

    def test_no_resources_section(self):
        """Testing BaseWebAPIToken.validate_policy with non-empty policy and
        no resources section
        """
        self.assertRaisesValidationError(b'The policy is missing a "resources" section.', APIPolicyWebAPIToken.validate_policy, {b'foo': {}})

    def test_resources_empty(self):
        """Testing BaseWebAPIToken.validate_policy with empty resources section
        """
        self.assertRaisesValidationError(b'The policy\'s "resources" section must not be empty.', APIPolicyWebAPIToken.validate_policy, {b'resources': {}})

    def test_resources_invalid_format(self):
        """Testing BaseWebAPIToken.validate_policy with resources not an object
        """
        self.assertRaisesValidationError(b'The policy\'s "resources" section must be a JSON object.', APIPolicyWebAPIToken.validate_policy, {b'resources': []})

    def test_global_valid(self):
        """Testing BaseWebAPIToken.validate_policy with valid '*' section"""
        APIPolicyWebAPIToken.validate_policy({b'resources': {b'*': {b'allow': [
                                          b'*'], 
                                 b'block': [
                                          b'POST']}}})

    def test_empty_global(self):
        """Testing BaseWebAPIToken.validate_policy with empty '*' section"""
        self.assertRaisesValidationError(b'The "resources.*" section must have "allow" and/or "block" rules.', APIPolicyWebAPIToken.validate_policy, {b'resources': {b'*': {}}})

    def test_global_not_object(self):
        """Testing BaseWebAPIToken.validate_policy with '*' section not a
        JSON object
        """
        self.assertRaisesValidationError(b'The "resources.*" section must be a JSON object.', APIPolicyWebAPIToken.validate_policy, {b'resources': {b'*': []}})

    def test_global_allow_not_list(self):
        """Testing BaseWebAPIToken.validate_policy with *.allow not a list"""
        self.assertRaisesValidationError(b'The "resources.*" section\'s "allow" rule must be a list.', APIPolicyWebAPIToken.validate_policy, {b'resources': {b'*': {b'allow': {}}}})

    def test_global_block_not_list(self):
        """Testing BaseWebAPIToken.validate_policy with *.block not a list"""
        self.assertRaisesValidationError(b'The "resources.*" section\'s "block" rule must be a list.', APIPolicyWebAPIToken.validate_policy, {b'resources': {b'*': {b'block': {}}}})

    def test_resource_global_valid(self):
        """Testing BaseWebAPIToken.validate_policy with <resource>.* valid"""
        APIPolicyWebAPIToken.validate_policy({b'resources': {b'someobject': {b'*': {b'allow': [
                                                          b'*'], 
                                                 b'block': [
                                                          b'POST']}}}})

    def test_resource_global_empty(self):
        """Testing BaseWebAPIToken.validate_policy with <resource>.* empty"""
        self.assertRaisesValidationError(b'The "resources.someobject.*" section must have "allow" and/or "block" rules.', APIPolicyWebAPIToken.validate_policy, {b'resources': {b'someobject': {b'*': {}}}})

    def test_resource_global_invalid_policy_id(self):
        """Testing BaseWebAPIToken.validate_policy with <resource>.* with
        invalid policy ID
        """
        self.assertRaisesValidationError(b'"foobar" is not a valid resource policy ID.', APIPolicyWebAPIToken.validate_policy, {b'resources': {b'foobar': {b'*': {b'allow': [
                                                      b'*']}}}})

    def test_resource_global_not_object(self):
        """Testing BaseWebAPIToken.validate_policy with <resource>.* not an
        object
        """
        self.assertRaisesValidationError(b'The "resources.someobject.*" section must be a JSON object.', APIPolicyWebAPIToken.validate_policy, {b'resources': {b'someobject': {b'*': []}}})

    def test_resource_global_allow_not_list(self):
        """Testing BaseWebAPIToken.validate_policy with <resource>.*.allow not
        a list
        """
        self.assertRaisesValidationError(b'The "resources.someobject.*" section\'s "allow" rule must be a list.', APIPolicyWebAPIToken.validate_policy, {b'resources': {b'someobject': {b'*': {b'allow': {}}}}})

    def test_resource_global_block_not_list(self):
        """Testing BaseWebAPIToken.validate_policy with <resource>.*.block not
        a list
        """
        self.assertRaisesValidationError(b'The "resources.someobject.*" section\'s "block" rule must be a list.', APIPolicyWebAPIToken.validate_policy, {b'resources': {b'someobject': {b'*': {b'block': {}}}}})

    def test_resource_id_valid(self):
        """Testing BaseWebAPIToken.validate_policy with <resource>.<id> valid
        """
        APIPolicyWebAPIToken.validate_policy({b'resources': {b'someobject': {b'42': {b'allow': [
                                                           b'*'], 
                                                  b'block': [
                                                           b'POST']}}}})

    def test_resource_id_empty(self):
        """Testing BaseWebAPIToken.validate_policy with <resource>.<id> empty
        """
        self.assertRaisesValidationError(b'The "resources.someobject.42" section must have "allow" and/or "block" rules.', APIPolicyWebAPIToken.validate_policy, {b'resources': {b'someobject': {b'42': {}}}})

    def test_resource_id_invalid_id_type(self):
        """Testing BaseWebAPIToken.validate_policy with <resource>.<id> with
        invalid ID type
        """
        self.assertRaisesValidationError(b'42 must be a string in "resources.someobject"', APIPolicyWebAPIToken.validate_policy, {b'resources': {b'someobject': {42: {b'allow': [
                                                        b'*']}}}})

    def test_resource_id_not_object(self):
        """Testing BaseWebAPIToken.validate_policy with <resource>.<id> not an
        object
        """
        self.assertRaisesValidationError(b'The "resources.someobject.42" section must be a JSON object.', APIPolicyWebAPIToken.validate_policy, {b'resources': {b'someobject': {b'42': []}}})

    def test_resource_id_allow_not_list(self):
        """Testing BaseWebAPIToken.validate_policy with <resource>.<id>.allow
        not a list
        """
        self.assertRaisesValidationError(b'The "resources.someobject.42" section\'s "allow" rule must be a list.', APIPolicyWebAPIToken.validate_policy, {b'resources': {b'someobject': {b'42': {b'allow': {}}}}})

    def test_resource_id_block_not_list(self):
        """Testing BaseWebAPIToken.validate_policy with <resource>.<id>.block
        not a list
        """
        self.assertRaisesValidationError(b'The "resources.someobject.42" section\'s "block" rule must be a list.', APIPolicyWebAPIToken.validate_policy, {b'resources': {b'someobject': {b'42': {b'block': {}}}}})