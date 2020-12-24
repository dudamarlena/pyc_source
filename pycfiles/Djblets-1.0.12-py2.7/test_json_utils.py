# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.11-x86_64/egg/djblets/util/tests/test_json_utils.py
# Compiled at: 2019-06-12 01:17:17
"""Unit tests for djblets.util.json_utils."""
from __future__ import unicode_literals
from djblets.testing.testcases import TestCase
from djblets.util.json_utils import JSONPatchError, JSONPatchPathError, JSONPatchReadAccessError, JSONPatchTestError, JSONPatchWriteAccessError, JSONPointerEndOfList, JSONPointerLookupError, JSONPointerSyntaxError, json_get_pointer_info, json_merge_patch, json_patch, json_resolve_pointer

class JSONMergePatchTests(TestCase):
    """Unit tests for djblets.util.json_utils.json_merge_patch."""

    def test_with_change_dict_key_value(self):
        """Testing json_merge_patch with changing key's value in dictionary"""
        doc = {b'a': b'b', 
           b'b': [
                b'c'], 
           b'c': b'd', 
           b'd': [
                1, 2], 
           b'e': {b'f': 1, 
                  b'g': 2}}
        self.assertEqual(json_merge_patch(doc=doc, patch={b'a': b'c', 
           b'b': b'd', 
           b'c': [
                b'e'], 
           b'd': [
                3, 4], 
           b'e': {b'f': b'ef'}}), {b'a': b'c', 
           b'b': b'd', 
           b'c': [
                b'e'], 
           b'd': [
                3, 4], 
           b'e': {b'f': b'ef', 
                  b'g': 2}})
        self.assertEqual(doc, {b'a': b'b', 
           b'b': [
                b'c'], 
           b'c': b'd', 
           b'd': [
                1, 2], 
           b'e': {b'f': 1, 
                  b'g': 2}})

    def test_with_add_dict_key(self):
        """Testing json_merge_patch with adding a new key to a dictionary"""
        doc = {b'a': b'b'}
        self.assertEqual(json_merge_patch(doc=doc, patch={b'b': b'c', 
           b'c': [
                b'd'], 
           b'd': {b'e': 1, 
                  b'f': 2}}), {b'a': b'b', 
           b'b': b'c', 
           b'c': [
                b'd'], 
           b'd': {b'e': 1, 
                  b'f': 2}})
        self.assertEqual(doc, {b'a': b'b'})

    def test_with_delete_dict_key(self):
        """Testing json_merge_patch with deleting a key in a dictionary"""
        doc = {b'a': b'b', 
           b'b': b'c', 
           b'c': {b'e': 1, 
                  b'f': 2}, 
           b'd': None}
        self.assertEqual(json_merge_patch(doc=doc, patch={b'a': None, 
           b'c': {b'e': None}, 
           b'e': None}), {b'b': b'c', 
           b'c': {b'f': 2}, 
           b'd': None})
        self.assertEqual(doc, {b'a': b'b', 
           b'b': b'c', 
           b'c': {b'e': 1, 
                  b'f': 2}, 
           b'd': None})
        return

    def test_with_change_list(self):
        """Testing json_merge_patch with changing a list value"""
        doc = [
         1, 2, 3]
        self.assertEqual(json_merge_patch(doc=doc, patch=[
         4, 5, 6]), [
         4, 5, 6])
        self.assertEqual(doc, [1, 2, 3])

    def test_with_change_type(self):
        """Testing json_merge_patch with changing a value's type"""
        doc = [
         1, 2, 3]
        self.assertEqual(json_merge_patch(doc=doc, patch={b'a': 1}), {b'a': 1})
        self.assertEqual(doc, [1, 2, 3])

    def test_with_can_write_key_func(self):
        """Testing json_merge_patch with can_write_key_func"""

        def _can_write_key(doc, patch, path):
            return path != ('a', 'b', 'c')

        doc = {b'a': {b'b': {b'c': 123}, 
                  b'd': True}}
        self.assertEqual(json_merge_patch(doc=doc, patch={b'a': {b'b': {b'c': 100}, 
                  b'd': False}, 
           b'e': b'hi!'}, can_write_key_func=_can_write_key), {b'a': {b'b': {b'c': 123}, 
                  b'd': False}, 
           b'e': b'hi!'})
        self.assertEqual(doc, {b'a': {b'b': {b'c': 123}, 
                  b'd': True}})

    def test_with_can_write_key_func_not_callable(self):
        """Testing json_merge_patch with can_write_key_func not callable"""
        message = b'can_write_key_func must be callable'
        with self.assertRaisesMessage(ValueError, message):
            json_merge_patch(doc={}, patch={}, can_write_key_func=123)

    def test_with_can_write_key_func_with_patch_error(self):
        """Testing json_merge_patch with can_write_key_func raising
        JSONPatchError
        """

        def _can_write_key(doc, patch, path):
            if path == ('a', 'b', 'c'):
                raise JSONPatchError(b'Go away!', doc=doc, patch=patch)
            return True

        doc = {b'a': {b'b': {b'c': 123}, 
                  b'd': True}}
        with self.assertRaisesMessage(JSONPatchError, b'Go away!'):
            json_merge_patch(doc=doc, patch={b'a': {b'b': {b'c': 100}, 
                      b'd': False}, 
               b'e': b'hi!'}, can_write_key_func=_can_write_key)
        self.assertEqual(doc, {b'a': {b'b': {b'c': 123}, 
                  b'd': True}})


class JSONPatchTests(TestCase):
    """Unit tests for djblets.util.json_utils.json_patch."""

    def test_with_patch_not_list(self):
        """Testing json_patch with patch not a list"""
        message = b'The patch must be a list of operations to perform'
        with self.assertRaisesMessage(JSONPatchError, message) as (cm):
            json_patch(doc={}, patch={})
        e = cm.exception
        self.assertEqual(e.doc, {})
        self.assertEqual(e.patch, {})
        self.assertIsNone(e.patch_entry_index)

    def test_with_patch_entry_not_dict(self):
        """Testing json_patch with patch entry not a dictionary"""
        message = b'Patch entry 0 must be a dictionary instead of list'
        with self.assertRaisesMessage(JSONPatchError, message) as (cm):
            json_patch(doc={}, patch=[[]])
        e = cm.exception
        self.assertEqual(e.doc, {})
        self.assertEqual(e.patch, [[]])
        self.assertEqual(e.patch_entry_index, 0)

    def test_with_patch_entry_missing_op(self):
        """Testing json_patch with patch entry missing op"""
        message = b'Missing key "op" for patch entry 0'
        with self.assertRaisesMessage(JSONPatchError, message) as (cm):
            json_patch(doc={}, patch=[{}])
        e = cm.exception
        self.assertEqual(e.doc, {})
        self.assertEqual(e.patch, [{}])
        self.assertEqual(e.patch_entry_index, 0)

    def test_with_dict_and_empty_patch(self):
        """Testing json_patch with dictionary object and empty patch"""
        doc = {b'foo': 1}
        self.assertEqual(json_patch(doc=doc, patch=[]), {b'foo': 1})
        self.assertEqual(doc, {b'foo': 1})

    def test_with_list_and_empty_patch(self):
        """Testing json_patch with list object and empty patch"""
        doc = [
         b'foo']
        self.assertEqual(json_patch(doc=doc, patch=[]), [
         b'foo'])

    def test_add_replacing_field(self):
        """Testing json_patch with add op replacing existing field"""
        doc = {b'foo': None}
        self.assertEqual(json_patch(doc=doc, patch=[
         {b'op': b'add', 
            b'path': b'/foo', 
            b'value': 1}]), {b'foo': 1})
        self.assertEqual(doc, {b'foo': None})
        return

    def test_add_to_top_level_dict(self):
        """Testing json_patch with add op in top-level dictionary"""
        doc = {}
        self.assertEqual(json_patch(doc=doc, patch=[
         {b'op': b'add', 
            b'path': b'/foo', 
            b'value': b'bar'}]), {b'foo': b'bar'})
        self.assertEqual(doc, {})

    def test_add_to_top_level_array(self):
        """Testing json_patch with add op in top-level array"""
        doc = []
        self.assertEqual(json_patch(doc=doc, patch=[
         {b'op': b'add', 
            b'path': b'/0', 
            b'value': b'foo'}]), [
         b'foo'])
        self.assertEqual(doc, [])

    def test_add_with_append_to_top_level_array(self):
        """Testing json_patch with add op with appending to top-level array"""
        doc = [
         b'a', b'b']
        self.assertEqual(json_patch(doc=doc, patch=[
         {b'op': b'add', 
            b'path': b'/-', 
            b'value': b'c'}]), [
         b'a', b'b', b'c'])
        self.assertEqual(doc, [b'a', b'b'])

    def test_add_with_insert_to_top_level_array(self):
        """Testing json_patch with add op with inserting into top-level array
        """
        doc = [
         b'a', b'b']
        self.assertEqual(json_patch(doc=doc, patch=[
         {b'op': b'add', 
            b'path': b'/1', 
            b'value': b'c'}]), [
         b'a', b'c', b'b'])
        self.assertEqual(doc, [b'a', b'b'])

    def test_add_with_empty_key_on_top_level(self):
        """Testing json_patch with add op with top level and "/" path
        (signifying empty key)
        """
        doc = {}
        self.assertEqual(json_patch(doc=doc, patch=[
         {b'op': b'add', 
            b'path': b'/', 
            b'value': 1}]), {b'': 1})
        self.assertEqual(doc, {})

    def test_add_with_empty_key_on_child(self):
        """Testing json_patch with add op with child dictionary and "/" path
        (signifying empty key)
        """
        doc = {b'foo': {}}
        self.assertEqual(json_patch(doc=doc, patch=[
         {b'op': b'add', 
            b'path': b'/foo/', 
            b'value': 1}]), {b'foo': {b'': 1}})
        self.assertEqual(doc, {b'foo': {}})

    def test_add_with_complex_path(self):
        """Testing json_patch with add op with complex path"""
        doc = {b'a': 1, 
           b'b': [
                {b'c': 2}]}
        self.assertEqual(json_patch(doc=doc, patch=[
         {b'op': b'add', 
            b'path': b'/b/0/d', 
            b'value': 100}]), {b'a': 1, 
           b'b': [
                {b'c': 2, 
                   b'd': 100}]})
        self.assertEqual(doc, {b'a': 1, 
           b'b': [
                {b'c': 2}]})

    def test_add_with_dict_and_numeric_key(self):
        """Testing json_patch with add op with dictionary and numeric key"""
        doc = {b'foo': 1}
        self.assertEqual(json_patch(doc=doc, patch=[
         {b'op': b'add', 
            b'path': b'/0', 
            b'value': 2}]), {b'foo': 1, 
           b'0': 2})
        self.assertEqual(doc, {b'foo': 1})

    def test_add_with_array_and_index_0(self):
        """Testing json_patch with add op with array and inserting at index 0
        """
        doc = {b'a': [
                1, 2, 3]}
        self.assertEqual(json_patch(doc=doc, patch=[
         {b'op': b'add', 
            b'path': b'/a/0', 
            b'value': 100}]), {b'a': [
                100, 1, 2, 3]})
        self.assertEqual(doc, {b'a': [
                1, 2, 3]})

    def test_add_with_array_and_last_index_plus_1(self):
        """Testing json_patch with add op with array and inserting at last
        index + 1
        """
        doc = {b'a': [
                1, 2, 3]}
        self.assertEqual(json_patch(doc=doc, patch=[
         {b'op': b'add', 
            b'path': b'/a/3', 
            b'value': 100}]), {b'a': [
                1, 2, 3, 100]})
        self.assertEqual(doc, {b'a': [
                1, 2, 3]})

    def test_add_with_can_write_key_func_and_allowed(self):
        """Testing json_patch with add op and can_write_key_func and key
        allowed
        """

        def _can_write_key(doc, patch_entry, path):
            return path == ('a', 'c')

        doc = {b'a': {b'b': 1}}
        self.assertEqual(json_patch(doc=doc, patch=[
         {b'op': b'add', 
            b'path': b'/a/c', 
            b'value': 2}], can_write_key_func=_can_write_key), {b'a': {b'b': 1, 
                  b'c': 2}})

    def test_add_with_can_write_key_func_and_not_allowed(self):
        """Testing json_patch with add op and can_write_key_func and key
        not allowed
        """

        def _can_write_key(doc, patch_entry, path):
            return path == ('a', 'b')

        doc = {b'a': {b'b': 1}}
        patch = [
         {b'op': b'add', 
            b'path': b'/a/c', 
            b'value': 2}]
        message = b'Cannot write to path "/a/c" for patch entry 0'
        with self.assertRaisesMessage(JSONPatchWriteAccessError, message) as (cm):
            json_patch(doc=doc, patch=patch, can_write_key_func=_can_write_key)
        e = cm.exception
        self.assertEqual(e.doc, doc)
        self.assertEqual(e.patch, patch)
        self.assertEqual(e.patch_entry_index, 0)
        self.assertEqual(e.path, b'/a/c')

    def test_add_with_array_and_index_out_of_bounds(self):
        """Testing json_patch with add op with array and index out of bounds"""
        doc = {b'a': [
                1, 2, 3]}
        patch = [
         {b'op': b'add', 
            b'path': b'/a/4', 
            b'value': 100}]
        message = b'Cannot insert into index 4 in path "/a/4" for patch entry 0'
        with self.assertRaisesMessage(JSONPatchPathError, message) as (cm):
            json_patch(doc=doc, patch=patch)
        e = cm.exception
        self.assertEqual(e.doc, doc)
        self.assertEqual(e.patch, patch)
        self.assertEqual(e.patch_entry_index, 0)
        self.assertEqual(e.path, b'/a/4')
        self.assertEqual(doc, {b'a': [
                1, 2, 3]})

    def test_add_with_array_and_negative_index(self):
        """Testing json_patch with add op with array and negative index"""
        doc = {b'a': [
                1, 2, 3]}
        patch = [
         {b'op': b'add', 
            b'path': b'/a/-1', 
            b'value': 100}]
        message = b'Syntax error in path "/a/-1" for patch entry 0: Negative indexes into lists are not allowed'
        with self.assertRaisesMessage(JSONPatchPathError, message) as (cm):
            json_patch(doc=doc, patch=patch)
        e = cm.exception
        self.assertEqual(e.doc, doc)
        self.assertEqual(e.patch, patch)
        self.assertEqual(e.patch_entry_index, 0)
        self.assertEqual(e.path, b'/a/-1')
        self.assertEqual(doc, {b'a': [
                1, 2, 3]})

    def test_add_with_array_and_key(self):
        """Testing json_patch with add op with array and attempting to insert
        at key
        """
        doc = {b'a': [
                1, 2, 3]}
        patch = [
         {b'op': b'add', 
            b'path': b'/a/bad', 
            b'value': 100}]
        message = b'Syntax error in path "/a/bad" for patch entry 0: u\'bad\' is not a valid list index in "/a"'
        with self.assertRaisesMessage(JSONPatchPathError, message) as (cm):
            json_patch(doc=doc, patch=patch)
        e = cm.exception
        self.assertEqual(e.doc, doc)
        self.assertEqual(e.patch, patch)
        self.assertEqual(e.patch_entry_index, 0)
        self.assertEqual(e.path, b'/a/bad')
        self.assertEqual(doc, {b'a': [
                1, 2, 3]})

    def test_add_with_missing_path(self):
        """Testing json_patch with add op and missing path"""
        doc = {b'a': 1}
        patch = [
         {b'op': b'add', 
            b'value': 1}]
        message = b'Missing key "path" for patch entry 0'
        with self.assertRaisesMessage(JSONPatchError, message) as (cm):
            json_patch(doc=doc, patch=patch)
        e = cm.exception
        self.assertEqual(e.doc, doc)
        self.assertEqual(e.patch, patch)
        self.assertEqual(e.patch_entry_index, 0)
        self.assertEqual(doc, {b'a': 1})

    def test_add_with_missing_value(self):
        """Testing json_patch with add op and missing value"""
        doc = {b'a': 1}
        patch = [
         {b'op': b'add', 
            b'path': b'/a'}]
        message = b'Missing key "value" for patch entry 0'
        with self.assertRaisesMessage(JSONPatchError, message) as (cm):
            json_patch(doc=doc, patch=patch)
        e = cm.exception
        self.assertEqual(e.doc, doc)
        self.assertEqual(e.patch, patch)
        self.assertEqual(e.patch_entry_index, 0)
        self.assertEqual(doc, {b'a': 1})

    def test_add_with_bad_path(self):
        """Testing json_patch with add op and bad path"""
        doc = {b'a': 1}
        patch = [
         {b'op': b'add', 
            b'path': b'/b/c', 
            b'value': 100}]
        message = b'Invalid path "/b/c" for patch entry 0: Dictionary key "b" not found in "/"'
        with self.assertRaisesMessage(JSONPatchPathError, message) as (cm):
            json_patch(doc=doc, patch=patch)
        e = cm.exception
        self.assertEqual(e.doc, doc)
        self.assertEqual(e.patch, patch)
        self.assertEqual(e.patch_entry_index, 0)
        self.assertEqual(e.path, b'/b/c')
        self.assertEqual(doc, {b'a': 1})

    def test_add_with_invalid_path_syntax(self):
        """Testing json_patch with add op and invalid path syntax"""
        doc = {}
        patch = [
         {b'op': b'add', 
            b'path': b'b', 
            b'value': 100}]
        message = b'Syntax error in path "b" for patch entry 0: Paths must either be empty or start with a "/"'
        with self.assertRaisesMessage(JSONPatchPathError, message) as (cm):
            json_patch(doc=doc, patch=patch)
        e = cm.exception
        self.assertEqual(e.doc, doc)
        self.assertEqual(e.patch, patch)
        self.assertEqual(e.patch_entry_index, 0)
        self.assertEqual(e.path, b'b')

    def test_remove_with_dict_key(self):
        """Testing json_patch with remove op with dictionary key"""
        doc = {b'a': 1, 
           b'b': 2}
        self.assertEqual(json_patch(doc=doc, patch=[
         {b'op': b'remove', 
            b'path': b'/a'}]), {b'b': 2})
        self.assertEqual(doc, {b'a': 1, 
           b'b': 2})

    def test_remove_with_array_index_0(self):
        """Testing json_patch with remove op with array index 0"""
        doc = {b'a': [
                1, 2, 3], 
           b'b': 2}
        self.assertEqual(json_patch(doc=doc, patch=[
         {b'op': b'remove', 
            b'path': b'/a/0'}]), {b'a': [
                2, 3], 
           b'b': 2})
        self.assertEqual(doc, {b'a': [
                1, 2, 3], 
           b'b': 2})

    def test_remove_with_array_index_middle(self):
        """Testing json_patch with remove op with array index (middle of array)
        """
        doc = {b'a': [
                1, 2, 3], 
           b'b': 2}
        self.assertEqual(json_patch(doc=doc, patch=[
         {b'op': b'remove', 
            b'path': b'/a/1'}]), {b'a': [
                1, 3], 
           b'b': 2})
        self.assertEqual(doc, {b'a': [
                1, 2, 3], 
           b'b': 2})

    def test_remove_with_array_index_last(self):
        """Testing json_patch with remove op with array index (last in array)
        """
        doc = {b'a': [
                1, 2, 3], 
           b'b': 2}
        self.assertEqual(json_patch(doc=doc, patch=[
         {b'op': b'remove', 
            b'path': b'/a/2'}]), {b'a': [
                1, 2], 
           b'b': 2})
        self.assertEqual(doc, {b'a': [
                1, 2, 3], 
           b'b': 2})

    def test_remove_with_array_index_end(self):
        """Testing json_patch with remove op with array index `-` (end of
        array)
        """
        doc = {b'a': [
                1, 2, 3], 
           b'b': 2}
        patch = [
         {b'op': b'remove', 
            b'path': b'/a/-'}]
        message = b'Cannot perform operation "remove" on end of list at "/a/-" for patch entry 0'
        with self.assertRaisesMessage(JSONPatchPathError, message) as (cm):
            json_patch(doc=doc, patch=patch)
        e = cm.exception
        self.assertEqual(e.doc, doc)
        self.assertEqual(e.patch, patch)
        self.assertEqual(e.patch_entry_index, 0)
        self.assertEqual(e.path, b'/a/-')
        self.assertEqual(doc, {b'a': [
                1, 2, 3], 
           b'b': 2})

    def test_remove_with_complex_path(self):
        """Testing json_patch with remove op with complex path"""
        doc = {b'a': [
                {b'b': 1, 
                   b'c': 2}]}
        self.assertEqual(json_patch(doc=doc, patch=[
         {b'op': b'remove', 
            b'path': b'/a/0/b'}]), {b'a': [
                {b'c': 2}]})
        self.assertEqual(doc, {b'a': [
                {b'b': 1, 
                   b'c': 2}]})

    def test_remove_with_repeated_removes(self):
        """Testing json_patch with remove op multiple times with different
        paths
        """
        doc = [
         1, 2, 3, 4]
        self.assertEqual(json_patch(doc=doc, patch=[
         {b'op': b'remove', 
            b'path': b'/1'},
         {b'op': b'remove', 
            b'path': b'/2'}]), [
         1, 3])
        self.assertEqual(doc, [1, 2, 3, 4])

    def test_remove_with_can_write_key_func_and_allowed(self):
        """Testing json_patch with remove op and can_write_key_func and key
        allowed
        """

        def _can_write_key(doc, patch_entry, path):
            return path == ('a', 'b')

        doc = {b'a': {b'b': 1}}
        self.assertEqual(json_patch(doc=doc, patch=[
         {b'op': b'remove', 
            b'path': b'/a/b'}], can_write_key_func=_can_write_key), {b'a': {}})

    def test_remove_with_can_write_key_func_and_not_allowed(self):
        """Testing json_patch with remove op and can_write_key_func and key
        not allowed
        """

        def _can_write_key(doc, patch_entry, path):
            return path == ('a', 'c')

        doc = {b'a': {b'b': 1}}
        patch = [
         {b'op': b'remove', 
            b'path': b'/a/b'}]
        message = b'Cannot write to path "/a/b" for patch entry 0'
        with self.assertRaisesMessage(JSONPatchWriteAccessError, message) as (cm):
            json_patch(doc=doc, patch=patch, can_write_key_func=_can_write_key)
        e = cm.exception
        self.assertEqual(e.doc, doc)
        self.assertEqual(e.patch, patch)
        self.assertEqual(e.patch_entry_index, 0)
        self.assertEqual(e.path, b'/a/b')

    def test_remove_with_missing_path(self):
        """Testing json_patch with remove op and missing path"""
        doc = {b'a': 1}
        patch = [
         {b'op': b'remove', 
            b'value': 1}]
        message = b'Missing key "path" for patch entry 0'
        with self.assertRaisesMessage(JSONPatchError, message) as (cm):
            json_patch(doc=doc, patch=patch)
        e = cm.exception
        self.assertEqual(e.doc, doc)
        self.assertEqual(e.patch, patch)
        self.assertEqual(e.patch_entry_index, 0)
        self.assertEqual(doc, {b'a': 1})

    def test_remove_with_bad_path(self):
        """Testing json_patch with remove op and bad path"""
        doc = {b'a': 1}
        patch = [
         {b'op': b'remove', 
            b'path': b'/b'}]
        message = b'Invalid path "/b" for patch entry 0: Dictionary key "b" not found in "/"'
        with self.assertRaisesMessage(JSONPatchPathError, message) as (cm):
            json_patch(doc=doc, patch=patch)
        e = cm.exception
        self.assertEqual(e.doc, doc)
        self.assertEqual(e.patch, patch)
        self.assertEqual(e.patch_entry_index, 0)
        self.assertEqual(e.path, b'/b')
        self.assertEqual(doc, {b'a': 1})

    def test_remove_with_invalid_path_syntax(self):
        """Testing json_patch with remove op and invalid path syntax"""
        doc = {}
        patch = [
         {b'op': b'remove', 
            b'path': b'b'}]
        message = b'Syntax error in path "b" for patch entry 0: Paths must either be empty or start with a "/"'
        with self.assertRaisesMessage(JSONPatchPathError, message) as (cm):
            json_patch(doc=doc, patch=patch)
        e = cm.exception
        self.assertEqual(e.doc, doc)
        self.assertEqual(e.patch, patch)
        self.assertEqual(e.patch_entry_index, 0)
        self.assertEqual(e.path, b'b')

    def test_remove_with_array_and_index_out_of_bounds(self):
        """Testing json_patch with remove op with array and index out of bounds
        """
        doc = {b'a': [
                1, 2]}
        patch = [
         {b'op': b'remove', 
            b'path': b'/a/3'}]
        message = b'Invalid path "/a/3" for patch entry 0: 3 is outside the list in "/a"'
        with self.assertRaisesMessage(JSONPatchPathError, message) as (cm):
            json_patch(doc=doc, patch=patch)
        e = cm.exception
        self.assertEqual(e.doc, doc)
        self.assertEqual(e.patch, patch)
        self.assertEqual(e.patch_entry_index, 0)
        self.assertEqual(e.path, b'/a/3')
        self.assertEqual(doc, {b'a': [
                1, 2]})

    def test_replace_top_level_dict_with_array(self):
        """Testing json_patch with replace op replacing top-level dictionary
        with an array
        """
        doc = {}
        self.assertEqual(json_patch(doc=doc, patch=[
         {b'op': b'replace', 
            b'path': b'', 
            b'value': []}]), [])
        self.assertEqual(doc, {})

    def test_replace_top_level_array_with_dict(self):
        """Testing json_patch with replace op replacing top-level array with
        a dictionary
        """
        doc = []
        self.assertEqual(json_patch(doc=doc, patch=[
         {b'op': b'replace', 
            b'path': b'', 
            b'value': {}}]), {})
        self.assertEqual(doc, [])

    def test_replace_with_dict_key(self):
        """Testing json_patch with replace op replacing key in dictionary"""
        doc = {b'a': {b'b': 1}}
        self.assertEqual(json_patch(doc=doc, patch=[
         {b'op': b'replace', 
            b'path': b'/a/b', 
            b'value': 2}]), {b'a': {b'b': 2}})
        self.assertEqual(doc, {b'a': {b'b': 1}})

    def test_replace_with_array_index_0(self):
        """Testing json_patch with replace op with array index 0"""
        doc = {b'a': {b'b': [
                       1, 2, 3]}}
        self.assertEqual(json_patch(doc=doc, patch=[
         {b'op': b'replace', 
            b'path': b'/a/b/0', 
            b'value': 100}]), {b'a': {b'b': [
                       100, 2, 3]}})
        self.assertEqual(doc, {b'a': {b'b': [
                       1, 2, 3]}})

    def test_replace_with_array_index_middle(self):
        """Testing json_patch with replace op with array index (middle of
        array)
        """
        doc = {b'a': {b'b': [
                       1, 2, 3]}}
        self.assertEqual(json_patch(doc=doc, patch=[
         {b'op': b'replace', 
            b'path': b'/a/b/1', 
            b'value': 100}]), {b'a': {b'b': [
                       1, 100, 3]}})
        self.assertEqual(doc, {b'a': {b'b': [
                       1, 2, 3]}})

    def test_replace_with_array_index_last(self):
        """Testing json_patch with replace op with array index (last in array)
        """
        doc = {b'a': {b'b': [
                       1, 2, 3]}}
        self.assertEqual(json_patch(doc=doc, patch=[
         {b'op': b'replace', 
            b'path': b'/a/b/2', 
            b'value': 100}]), {b'a': {b'b': [
                       1, 2, 100]}})
        self.assertEqual(doc, {b'a': {b'b': [
                       1, 2, 3]}})

    def test_replace_with_array_index_end(self):
        """Testing json_patch with replace op with array index (end of array)
        """
        doc = {b'a': {b'b': [
                       1, 2, 3]}}
        patch = [
         {b'op': b'replace', 
            b'path': b'/a/b/-', 
            b'value': 100}]
        message = b'Cannot perform operation "replace" on end of list at "/a/b/-" for patch entry 0'
        with self.assertRaisesMessage(JSONPatchPathError, message) as (cm):
            json_patch(doc=doc, patch=patch)
        e = cm.exception
        self.assertEqual(e.doc, doc)
        self.assertEqual(e.patch, patch)
        self.assertEqual(e.patch_entry_index, 0)
        self.assertEqual(e.path, b'/a/b/-')
        self.assertEqual(doc, {b'a': {b'b': [
                       1, 2, 3]}})

    def test_replace_with_can_write_key_func_and_allowed(self):
        """Testing json_patch with replace op and can_write_key_func and key
        allowed
        """

        def _can_write_key(doc, patch_entry, path):
            return path == ('a', 'b')

        doc = {b'a': {b'b': 1}}
        self.assertEqual(json_patch(doc=doc, patch=[
         {b'op': b'replace', 
            b'path': b'/a/b', 
            b'value': 100}], can_write_key_func=_can_write_key), {b'a': {b'b': 100}})

    def test_replace_with_can_write_key_func_and_not_allowed(self):
        """Testing json_patch with replace op and can_write_key_func and key
        not allowed
        """

        def _can_write_key(doc, patch_entry, path):
            return path == ('a', 'c')

        doc = {b'a': {b'b': 1}}
        patch = [
         {b'op': b'replace', 
            b'path': b'/a/b', 
            b'value': 100}]
        message = b'Cannot write to path "/a/b" for patch entry 0'
        with self.assertRaisesMessage(JSONPatchWriteAccessError, message) as (cm):
            json_patch(doc=doc, patch=patch, can_write_key_func=_can_write_key)
        e = cm.exception
        self.assertEqual(e.doc, doc)
        self.assertEqual(e.patch, patch)
        self.assertEqual(e.patch_entry_index, 0)
        self.assertEqual(e.path, b'/a/b')

    def test_replace_with_missing_path(self):
        """Testing json_patch with replace op and missing path"""
        doc = {b'a': 1}
        patch = [
         {b'op': b'replace', 
            b'value': 1}]
        message = b'Missing key "path" for patch entry 0'
        with self.assertRaisesMessage(JSONPatchError, message) as (cm):
            json_patch(doc=doc, patch=patch)
        e = cm.exception
        self.assertEqual(e.doc, doc)
        self.assertEqual(e.patch, patch)
        self.assertEqual(e.patch_entry_index, 0)
        self.assertEqual(doc, {b'a': 1})

    def test_replace_with_bad_path(self):
        """Testing json_patch with replace op and bad path"""
        doc = {b'a': 1}
        patch = [
         {b'op': b'replace', 
            b'path': b'/b', 
            b'value': 100}]
        message = b'Cannot remove non-existent key "b" in path "/b" for patch entry 0'
        with self.assertRaisesMessage(JSONPatchPathError, message) as (cm):
            json_patch(doc=doc, patch=patch)
        e = cm.exception
        self.assertEqual(e.doc, doc)
        self.assertEqual(e.patch, patch)
        self.assertEqual(e.patch_entry_index, 0)
        self.assertEqual(e.path, b'/b')
        self.assertEqual(doc, {b'a': 1})

    def test_replace_with_invalid_path_syntax(self):
        """Testing json_patch with replace op and invalid path syntax"""
        doc = {}
        patch = [
         {b'op': b'replace', 
            b'path': b'b', 
            b'value': 100}]
        message = b'Syntax error in path "b" for patch entry 0: Paths must either be empty or start with a "/"'
        with self.assertRaisesMessage(JSONPatchPathError, message) as (cm):
            json_patch(doc=doc, patch=patch)
        e = cm.exception
        self.assertEqual(e.doc, doc)
        self.assertEqual(e.patch, patch)
        self.assertEqual(e.patch_entry_index, 0)
        self.assertEqual(e.path, b'b')

    def test_copy_with_dict_key(self):
        """Testing json_patch with copy op and dictionary key"""
        doc = {b'a': 1}
        self.assertEqual(json_patch(doc=doc, patch=[
         {b'op': b'copy', 
            b'from': b'/a', 
            b'path': b'/b'}]), {b'a': 1, 
           b'b': 1})
        self.assertEqual(doc, {b'a': 1})

    def test_copy_with_array_index(self):
        """Testing json_patch with copy op and array index"""
        doc = {b'a': [
                1, 2, 3]}
        self.assertEqual(json_patch(doc=doc, patch=[
         {b'op': b'copy', 
            b'from': b'/a/1', 
            b'path': b'/a/0'}]), {b'a': [
                2, 1, 2, 3]})
        self.assertEqual(doc, {b'a': [
                1, 2, 3]})

    def test_copy_with_array_index_end(self):
        """Testing json_patch with copy op and array index `-` (end of array)
        """
        doc = {b'a': [
                1, 2, 3]}
        self.assertEqual(json_patch(doc=doc, patch=[
         {b'op': b'copy', 
            b'from': b'/a/1', 
            b'path': b'/a/-'}]), {b'a': [
                1, 2, 3, 2]})
        self.assertEqual(doc, {b'a': [
                1, 2, 3]})

    def test_copy_with_from_array_index_end(self):
        """Testing json_patch with copy op and "from" array index `-` (end of
        array)
        """
        doc = {b'a': [
                1, 2, 3]}
        patch = [
         {b'op': b'copy', 
            b'from': b'/a/-', 
            b'path': b'/a/0'}]
        message = b'Cannot perform operation "copy" from end of list at "/a/-" for patch entry 0'
        with self.assertRaisesMessage(JSONPatchPathError, message) as (cm):
            json_patch(doc=doc, patch=patch)
        e = cm.exception
        self.assertEqual(e.doc, doc)
        self.assertEqual(e.patch, patch)
        self.assertEqual(e.patch_entry_index, 0)
        self.assertEqual(e.path, b'/a/-')
        self.assertEqual(doc, {b'a': [
                1, 2, 3]})

    def test_copy_with_array_index_to_dict_key(self):
        """Testing json_patch with copy op and array index copied to dictionary
        key
        """
        doc = {b'a': [
                1, 2, 3]}
        self.assertEqual(json_patch(doc=doc, patch=[
         {b'op': b'copy', 
            b'from': b'/a/1', 
            b'path': b'/b'}]), {b'a': [
                1, 2, 3], 
           b'b': 2})
        self.assertEqual(doc, {b'a': [
                1, 2, 3]})

    def test_copy_with_dict_key_to_array_index(self):
        """Testing json_patch with copy op and dictionary key copied to array
        index
        """
        doc = {b'a': [
                1, 2, 3], 
           b'b': 100}
        self.assertEqual(json_patch(doc=doc, patch=[
         {b'op': b'copy', 
            b'from': b'/b', 
            b'path': b'/a/1'}]), {b'a': [
                1, 100, 2, 3], 
           b'b': 100})
        self.assertEqual(doc, {b'a': [
                1, 2, 3], 
           b'b': 100})

    def test_copy_with_same_paths(self):
        """Testing json_patch with copy op and same source and destination
        paths
        """
        doc = {b'a': 1}
        self.assertEqual(json_patch(doc=doc, patch=[
         {b'op': b'copy', 
            b'from': b'/a', 
            b'path': b'/a'}]), {b'a': 1})
        self.assertEqual(doc, {b'a': 1})

    def test_copy_with_can_write_key_func_and_allowed(self):
        """Testing json_patch with copy op and can_write_key_func and key
        allowed
        """

        def _can_write_key(doc, patch_entry, path):
            return path == ('b', )

        doc = {b'a': {b'b': 1}}
        self.assertEqual(json_patch(doc=doc, patch=[
         {b'op': b'copy', 
            b'from': b'/a/b', 
            b'path': b'/b'}], can_write_key_func=_can_write_key), {b'a': {b'b': 1}, 
           b'b': 1})

    def test_copy_with_can_write_key_func_and_not_allowed(self):
        """Testing json_patch with copy op and can_write_key_func and key
        not allowed
        """

        def _can_write_key(doc, patch_entry, path):
            return path in ('a', 'c')

        doc = {b'a': {b'b': 1}}
        patch = [
         {b'op': b'copy', 
            b'from': b'/a/b', 
            b'path': b'/b'}]
        message = b'Cannot write to path "/b" for patch entry 0'
        with self.assertRaisesMessage(JSONPatchWriteAccessError, message) as (cm):
            json_patch(doc=doc, patch=patch, can_write_key_func=_can_write_key)
        e = cm.exception
        self.assertEqual(e.doc, doc)
        self.assertEqual(e.patch, patch)
        self.assertEqual(e.patch_entry_index, 0)
        self.assertEqual(e.path, b'/b')

    def test_copy_with_can_read_key_func_and_allowed(self):
        """Testing json_patch with copy op and can_read_key_func and key
        allowed
        """

        def _can_read_key(doc, patch_entry, path):
            return path in (('a', 'b'), ('b', ))

        doc = {b'a': {b'b': 1}}
        self.assertEqual(json_patch(doc=doc, patch=[
         {b'op': b'copy', 
            b'from': b'/a/b', 
            b'path': b'/b'}], can_read_key_func=_can_read_key), {b'a': {b'b': 1}, 
           b'b': 1})

    def test_copy_with_can_read_key_func_and_not_allowed(self):
        """Testing json_patch with copy op and can_read_key_func and key
        not allowed
        """

        def _can_read_key(doc, patch_entry, path):
            return path == ('b', )

        doc = {b'a': {b'b': 1}}
        patch = [
         {b'op': b'copy', 
            b'from': b'/a/b', 
            b'path': b'/b'}]
        message = b'Cannot read from path "/a/b" for patch entry 0'
        with self.assertRaisesMessage(JSONPatchReadAccessError, message) as (cm):
            json_patch(doc=doc, patch=patch, can_read_key_func=_can_read_key)
        e = cm.exception
        self.assertEqual(e.doc, doc)
        self.assertEqual(e.patch, patch)
        self.assertEqual(e.patch_entry_index, 0)
        self.assertEqual(e.path, b'/a/b')

    def test_copy_with_missing_path(self):
        """Testing json_patch with copy op and missing destination path"""
        doc = {b'a': 1}
        patch = [
         {b'op': b'copy', 
            b'from': b'/a'}]
        message = b'Missing key "path" for patch entry 0'
        with self.assertRaisesMessage(JSONPatchError, message) as (cm):
            json_patch(doc=doc, patch=patch)
        e = cm.exception
        self.assertEqual(e.doc, doc)
        self.assertEqual(e.patch, patch)
        self.assertEqual(e.patch_entry_index, 0)
        self.assertEqual(doc, {b'a': 1})

    def test_copy_with_missing_from(self):
        """Testing json_patch with copy op and missing from path"""
        doc = {b'a': 1}
        patch = [
         {b'op': b'copy', 
            b'path': b'/c'}]
        message = b'Missing key "from" for patch entry 0'
        with self.assertRaisesMessage(JSONPatchError, message) as (cm):
            json_patch(doc=doc, patch=patch)
        e = cm.exception
        self.assertEqual(e.doc, doc)
        self.assertEqual(e.patch, patch)
        self.assertEqual(e.patch_entry_index, 0)
        self.assertEqual(doc, {b'a': 1})

    def test_copy_with_bad_from_path(self):
        """Testing json_patch with copy op and bad from path"""
        doc = {b'a': 1}
        patch = [
         {b'op': b'copy', 
            b'from': b'/b', 
            b'path': b'/c'}]
        message = b'Invalid from path "/b" for patch entry 0: Dictionary key "b" not found in "/"'
        with self.assertRaisesMessage(JSONPatchPathError, message) as (cm):
            json_patch(doc=doc, patch=patch)
        e = cm.exception
        self.assertEqual(e.doc, doc)
        self.assertEqual(e.patch, patch)
        self.assertEqual(e.patch_entry_index, 0)
        self.assertEqual(e.path, b'/b')
        self.assertEqual(doc, {b'a': 1})

    def test_copy_with_bad_path(self):
        """Testing json_patch with copy op and bad destination path"""
        doc = {b'a': 1, 
           b'b': 2}
        patch = [
         {b'op': b'copy', 
            b'from': b'/a', 
            b'path': b'/b/bad'}]
        message = b'Unable to add key "bad" to a non-dictionary/list in path "/b/bad" for patch entry 0'
        with self.assertRaisesMessage(JSONPatchPathError, message) as (cm):
            json_patch(doc=doc, patch=patch)
        e = cm.exception
        self.assertEqual(e.doc, doc)
        self.assertEqual(e.patch, patch)
        self.assertEqual(e.patch_entry_index, 0)
        self.assertEqual(e.path, b'/b/bad')
        self.assertEqual(doc, {b'a': 1, 
           b'b': 2})

    def test_copy_with_invalid_from_path_syntax(self):
        """Testing json_patch with copy op and invalid from path syntax"""
        doc = {}
        patch = [
         {b'op': b'copy', 
            b'from': b'b', 
            b'path': b'/b'}]
        message = b'Syntax error in from path "b" for patch entry 0: Paths must either be empty or start with a "/"'
        with self.assertRaisesMessage(JSONPatchPathError, message) as (cm):
            json_patch(doc=doc, patch=patch)
        e = cm.exception
        self.assertEqual(e.doc, doc)
        self.assertEqual(e.patch, patch)
        self.assertEqual(e.patch_entry_index, 0)
        self.assertEqual(e.path, b'b')

    def test_copy_with_invalid_path_syntax(self):
        """Testing json_patch with copy op and invalid path syntax"""
        doc = {}
        patch = [
         {b'op': b'copy', 
            b'from': b'/b', 
            b'path': b'b'}]
        message = b'Syntax error in path "b" for patch entry 0: Paths must either be empty or start with a "/"'
        with self.assertRaisesMessage(JSONPatchPathError, message) as (cm):
            json_patch(doc=doc, patch=patch)
        e = cm.exception
        self.assertEqual(e.doc, doc)
        self.assertEqual(e.patch, patch)
        self.assertEqual(e.patch_entry_index, 0)
        self.assertEqual(e.path, b'b')

    def test_move_with_dict_key(self):
        """Testing json_patch with move op and dictionary key"""
        doc = {b'a': 1}
        self.assertEqual(json_patch(doc=doc, patch=[
         {b'op': b'move', 
            b'from': b'/a', 
            b'path': b'/b'}]), {b'b': 1})
        self.assertEqual(doc, {b'a': 1})

    def test_move_with_array_index(self):
        """Testing json_patch with move op and array index"""
        doc = {b'a': [
                1, 2, 3]}
        self.assertEqual(json_patch(doc=doc, patch=[
         {b'op': b'move', 
            b'from': b'/a/1', 
            b'path': b'/a/0'}]), {b'a': [
                2, 1, 3]})
        self.assertEqual(doc, {b'a': [
                1, 2, 3]})

    def test_move_with_array_index_end(self):
        """Testing json_patch with move op and array index `-` (end of array)
        """
        doc = {b'a': [
                1, 2, 3]}
        self.assertEqual(json_patch(doc=doc, patch=[
         {b'op': b'move', 
            b'from': b'/a/1', 
            b'path': b'/a/-'}]), {b'a': [
                1, 3, 2]})
        self.assertEqual(doc, {b'a': [
                1, 2, 3]})

    def test_move_with_from_array_index_end(self):
        """Testing json_patch with move op and "from" array index `-` (end of
        array)
        """
        doc = {b'a': [
                1, 2, 3]}
        patch = [
         {b'op': b'move', 
            b'from': b'/a/-', 
            b'path': b'/a/0'}]
        message = b'Cannot perform operation "move" from end of list at "/a/-" for patch entry 0'
        with self.assertRaisesMessage(JSONPatchPathError, message) as (cm):
            json_patch(doc=doc, patch=patch)
        e = cm.exception
        self.assertEqual(e.doc, doc)
        self.assertEqual(e.patch, patch)
        self.assertEqual(e.patch_entry_index, 0)
        self.assertEqual(e.path, b'/a/-')
        self.assertEqual(doc, {b'a': [
                1, 2, 3]})

    def test_move_with_array_index_to_dict_key(self):
        """Testing json_patch with move op and array index copied to dictionary
        key
        """
        doc = {b'a': [
                1, 2, 3]}
        self.assertEqual(json_patch(doc=doc, patch=[
         {b'op': b'move', 
            b'from': b'/a/1', 
            b'path': b'/b'}]), {b'a': [
                1, 3], 
           b'b': 2})
        self.assertEqual(doc, {b'a': [
                1, 2, 3]})

    def test_move_with_dict_key_to_array_index(self):
        """Testing json_patch with move op and dictionary key moved to array
        index
        """
        doc = {b'a': [
                1, 2, 3], 
           b'b': 100}
        self.assertEqual(json_patch(doc=doc, patch=[
         {b'op': b'move', 
            b'from': b'/b', 
            b'path': b'/a/1'}]), {b'a': [
                1, 100, 2, 3]})
        self.assertEqual(doc, {b'a': [
                1, 2, 3], 
           b'b': 100})

    def test_move_with_same_paths(self):
        """Testing json_patch with move op and same source and destination
        paths
        """
        doc = {b'a': 1}
        self.assertEqual(json_patch(doc=doc, patch=[
         {b'op': b'move', 
            b'from': b'/a', 
            b'path': b'/a'}]), {b'a': 1})
        self.assertEqual(doc, {b'a': 1})

    def test_move_with_can_write_key_func_and_allowed(self):
        """Testing json_patch with move op and can_write_key_func and key
        allowed
        """

        def _can_write_key(doc, patch_entry, path):
            return path in (('a', 'b'), ('b', ))

        doc = {b'a': {b'b': 1}}
        self.assertEqual(json_patch(doc=doc, patch=[
         {b'op': b'move', 
            b'from': b'/a/b', 
            b'path': b'/b'}], can_write_key_func=_can_write_key), {b'a': {}, b'b': 1})

    def test_move_with_can_write_key_func_and_not_allowed(self):
        """Testing json_patch with move op and can_write_key_func and key
        not allowed
        """

        def _can_write_key(doc, patch_entry, path):
            return path in ('a', 'c')

        doc = {b'a': {b'b': 1}}
        patch = [
         {b'op': b'move', 
            b'from': b'/a/b', 
            b'path': b'/b'}]
        message = b'Cannot write to path "/b" for patch entry 0'
        with self.assertRaisesMessage(JSONPatchWriteAccessError, message) as (cm):
            json_patch(doc=doc, patch=patch, can_write_key_func=_can_write_key)
        e = cm.exception
        self.assertEqual(e.doc, doc)
        self.assertEqual(e.patch, patch)
        self.assertEqual(e.patch_entry_index, 0)
        self.assertEqual(e.path, b'/b')

    def test_move_with_missing_path(self):
        """Testing json_patch with move op and missing destination path"""
        doc = {b'a': 1}
        patch = [
         {b'op': b'move', 
            b'from': b'/a'}]
        message = b'Missing key "path" for patch entry 0'
        with self.assertRaisesMessage(JSONPatchError, message) as (cm):
            json_patch(doc=doc, patch=patch)
        e = cm.exception
        self.assertEqual(e.doc, doc)
        self.assertEqual(e.patch, patch)
        self.assertEqual(e.patch_entry_index, 0)
        self.assertEqual(doc, {b'a': 1})

    def test_move_with_missing_from(self):
        """Testing json_patch with move op and missing from path"""
        doc = {b'a': 1}
        patch = [
         {b'op': b'move', 
            b'path': b'/c'}]
        message = b'Missing key "from" for patch entry 0'
        with self.assertRaisesMessage(JSONPatchError, message) as (cm):
            json_patch(doc=doc, patch=patch)
        e = cm.exception
        self.assertEqual(e.doc, doc)
        self.assertEqual(e.patch, patch)
        self.assertEqual(e.patch_entry_index, 0)
        self.assertEqual(doc, {b'a': 1})

    def test_move_with_bad_from_path(self):
        """Testing json_patch with move op and bad from path"""
        doc = {b'a': 1}
        patch = [
         {b'op': b'move', 
            b'from': b'/b', 
            b'path': b'/c'}]
        message = b'Invalid from path "/b" for patch entry 0: Dictionary key "b" not found in "/"'
        with self.assertRaisesMessage(JSONPatchPathError, message) as (cm):
            json_patch(doc=doc, patch=patch)
        e = cm.exception
        self.assertEqual(e.doc, doc)
        self.assertEqual(e.patch, patch)
        self.assertEqual(e.patch_entry_index, 0)
        self.assertEqual(e.path, b'/b')
        self.assertEqual(doc, {b'a': 1})

    def test_move_with_bad_path(self):
        """Testing json_patch with move op and bad destination path"""
        doc = {b'a': 1, 
           b'b': 2}
        patch = [
         {b'op': b'move', 
            b'from': b'/a', 
            b'path': b'/b/bad'}]
        message = b'Unable to add key "bad" to a non-dictionary/list in path "/b/bad" for patch entry 0'
        with self.assertRaisesMessage(JSONPatchPathError, message) as (cm):
            json_patch(doc=doc, patch=patch)
        e = cm.exception
        self.assertEqual(e.doc, doc)
        self.assertEqual(e.patch, patch)
        self.assertEqual(e.patch_entry_index, 0)
        self.assertEqual(e.path, b'/b/bad')
        self.assertEqual(doc, {b'a': 1, 
           b'b': 2})

    def test_move_with_invalid_from_path_syntax(self):
        """Testing json_patch with move op and invalid from path syntax"""
        doc = {}
        patch = [
         {b'op': b'move', 
            b'from': b'b', 
            b'path': b'/b'}]
        message = b'Syntax error in from path "b" for patch entry 0: Paths must either be empty or start with a "/"'
        with self.assertRaisesMessage(JSONPatchPathError, message) as (cm):
            json_patch(doc=doc, patch=patch)
        e = cm.exception
        self.assertEqual(e.doc, doc)
        self.assertEqual(e.patch, patch)
        self.assertEqual(e.patch_entry_index, 0)
        self.assertEqual(e.path, b'b')

    def test_move_with_invalid_path_syntax(self):
        """Testing json_patch with move op and invalid path syntax"""
        doc = {}
        patch = [
         {b'op': b'move', 
            b'from': b'/b', 
            b'path': b'b'}]
        message = b'Syntax error in path "b" for patch entry 0: Paths must either be empty or start with a "/"'
        with self.assertRaisesMessage(JSONPatchPathError, message) as (cm):
            json_patch(doc=doc, patch=patch)
        e = cm.exception
        self.assertEqual(e.doc, doc)
        self.assertEqual(e.patch, patch)
        self.assertEqual(e.patch_entry_index, 0)
        self.assertEqual(e.path, b'b')

    def test_move_with_moving_into_child(self):
        """Testing json_patch with move op and attempting to move into child of
        path
        """
        doc = {b'a': {b'b': {b'c': {}}}}
        patch = [
         {b'op': b'move', 
            b'from': b'/a/b', 
            b'path': b'/a/b/c'}]
        message = b'Cannot move values into their own children at patch entry 0'
        with self.assertRaisesMessage(JSONPatchPathError, message) as (cm):
            json_patch(doc=doc, patch=patch)
        e = cm.exception
        self.assertEqual(e.doc, doc)
        self.assertEqual(e.patch, patch)
        self.assertEqual(e.patch_entry_index, 0)
        self.assertEqual(e.path, b'/a/b')
        self.assertEqual(doc, {b'a': {b'b': {b'c': {}}}})

    def test_test_with_matching_value(self):
        """Testing json_patch with test op and matching value"""
        doc = {b'a': 1}
        self.assertEqual(json_patch(doc=doc, patch=[
         {b'op': b'test', 
            b'path': b'/a', 
            b'value': 1}]), {b'a': 1})
        self.assertEqual(doc, {b'a': 1})

    def test_test_with_missing_path(self):
        """Testing json_patch with test op and missing path"""
        doc = {b'a': 1}
        patch = [
         {b'op': b'test', 
            b'value': 1}]
        message = b'Missing key "path" for patch entry 0'
        with self.assertRaisesMessage(JSONPatchError, message) as (cm):
            json_patch(doc=doc, patch=patch)
        e = cm.exception
        self.assertEqual(e.doc, doc)
        self.assertEqual(e.patch, patch)
        self.assertEqual(e.patch_entry_index, 0)
        self.assertEqual(doc, {b'a': 1})

    def test_test_with_array_index_end(self):
        """Testing json_patch with test op and array index `-` (end of array)
        """
        doc = {b'a': [
                1, 2, 3]}
        patch = [
         {b'op': b'test', 
            b'path': b'/a/-', 
            b'value': 1}]
        message = b'Cannot perform operation "test" on end of list at "/a/-" for patch entry 0'
        with self.assertRaisesMessage(JSONPatchError, message) as (cm):
            json_patch(doc=doc, patch=patch)
        e = cm.exception
        self.assertEqual(e.doc, doc)
        self.assertEqual(e.patch, patch)
        self.assertEqual(e.patch_entry_index, 0)
        self.assertEqual(e.path, b'/a/-')
        self.assertEqual(doc, {b'a': [
                1, 2, 3]})

    def test_test_with_missing_value(self):
        """Testing json_patch with test op and missing value"""
        doc = {b'a': 1}
        patch = [
         {b'op': b'test', 
            b'path': b'/a'}]
        message = b'Missing key "value" for patch entry 0'
        with self.assertRaisesMessage(JSONPatchError, message) as (cm):
            json_patch(doc=doc, patch=patch)
        e = cm.exception
        self.assertEqual(e.doc, doc)
        self.assertEqual(e.patch, patch)
        self.assertEqual(e.patch_entry_index, 0)
        self.assertEqual(doc, {b'a': 1})

    def test_test_without_matching_value(self):
        """Testing json_patch with test op and non-matching value"""
        doc = {b'a': 1}
        patch = [
         {b'op': b'test', 
            b'path': b'/a', 
            b'value': 2}]
        message = b'Test failed for path "/a" at patch entry 0. Expected 2 and got 1.'
        with self.assertRaisesMessage(JSONPatchTestError, message) as (cm):
            json_patch(doc=doc, patch=patch)
        e = cm.exception
        self.assertEqual(e.doc, doc)
        self.assertEqual(e.patch, patch)
        self.assertEqual(e.patch_entry_index, 0)
        self.assertEqual(doc, {b'a': 1})

    def test_test_with_can_read_key_func_and_allowed(self):
        """Testing json_patch with test op and can_read_key_func and key
        allowed
        """

        def _can_read_key(doc, patch_entry, path):
            return path == ('a', 'b')

        doc = {b'a': {b'b': 1}}
        self.assertEqual(json_patch(doc=doc, patch=[
         {b'op': b'test', 
            b'path': b'/a/b', 
            b'value': 1}], can_read_key_func=_can_read_key), {b'a': {b'b': 1}})

    def test_test_with_can_read_key_func_and_not_allowed(self):
        """Testing json_patch with test op and can_read_key_func and key
        not allowed
        """

        def _can_read_key(doc, patch_entry, path):
            return path == ('a', 'c')

        doc = {b'a': {b'b': 1}}
        patch = [
         {b'op': b'test', 
            b'path': b'/a/b', 
            b'value': 1}]
        message = b'Cannot read from path "/a/b" for patch entry 0'
        with self.assertRaisesMessage(JSONPatchReadAccessError, message) as (cm):
            json_patch(doc=doc, patch=patch, can_read_key_func=_can_read_key)
        e = cm.exception
        self.assertEqual(e.doc, doc)
        self.assertEqual(e.patch, patch)
        self.assertEqual(e.patch_entry_index, 0)
        self.assertEqual(e.path, b'/a/b')

    def test_test_with_dict_missing_key(self):
        """Testing json_patch with test op and dictionary with missing key"""
        doc = {}
        patch = [
         {b'op': b'test', 
            b'path': b'/a', 
            b'value': 1}]
        message = b'Invalid path "/a" for patch entry 0: Dictionary key "a" not found in "/"'
        with self.assertRaisesMessage(JSONPatchPathError, message) as (cm):
            json_patch(doc=doc, patch=patch)
        e = cm.exception
        self.assertEqual(e.doc, doc)
        self.assertEqual(e.patch, patch)
        self.assertEqual(e.patch_entry_index, 0)
        self.assertEqual(e.path, b'/a')
        self.assertEqual(doc, {})

    def test_test_with_bad_path(self):
        """Testing json_patch with test op and bad destination path"""
        doc = {b'a': 1, 
           b'b': 2}
        patch = [
         {b'op': b'test', 
            b'path': b'/b/bad', 
            b'value': 1}]
        message = b'Cannot resolve path within unsupported type "int" at "/b"'
        with self.assertRaisesMessage(JSONPatchPathError, message) as (cm):
            json_patch(doc=doc, patch=patch)
        e = cm.exception
        self.assertEqual(e.doc, doc)
        self.assertEqual(e.patch, patch)
        self.assertEqual(e.patch_entry_index, 0)
        self.assertEqual(e.path, b'/b/bad')
        self.assertEqual(doc, {b'a': 1, 
           b'b': 2})

    def test_test_with_invalid_path_syntax(self):
        """Testing json_patch with test op and invalid path syntax"""
        doc = {}
        patch = [
         {b'op': b'test', 
            b'path': b'b', 
            b'value': 1}]
        message = b'Syntax error in path "b" for patch entry 0: Paths must either be empty or start with a "/"'
        with self.assertRaisesMessage(JSONPatchPathError, message) as (cm):
            json_patch(doc=doc, patch=patch)
        e = cm.exception
        self.assertEqual(e.doc, doc)
        self.assertEqual(e.patch, patch)
        self.assertEqual(e.patch_entry_index, 0)
        self.assertEqual(e.path, b'b')


class JSONGetPointerInfoTests(TestCase):
    """Unit tests for djblets.util.json_utils.json_get_pointer_info."""

    def test_with_relative_path(self):
        """Testing json_get_pointer_info with relative path"""
        message = b'Paths must either be empty or start with a "/"'
        with self.assertRaisesMessage(JSONPointerSyntaxError, message):
            json_get_pointer_info({}, b'a/')

    def test_with_dict(self):
        """Testing json_get_pointer_info with valid dictionary path"""
        obj = {b'': b'hi', 
           b'a': {b'b': {b'c': 123}}}
        self.assertEqual(json_get_pointer_info(obj, b''), {b'value': obj, 
           b'parent': None, 
           b'resolved_values': [
                              obj], 
           b'all_tokens': [], b'resolved_tokens': [], b'unresolved_tokens': [], b'lookup_error': None})
        self.assertEqual(json_get_pointer_info(obj, b'/'), {b'value': b'hi', 
           b'parent': obj, 
           b'resolved_values': [
                              obj, b'hi'], 
           b'all_tokens': [
                         b''], 
           b'resolved_tokens': [
                              b''], 
           b'unresolved_tokens': [], b'lookup_error': None})
        self.assertEqual(json_get_pointer_info(obj, b'/a'), {b'value': obj[b'a'], 
           b'parent': obj, 
           b'resolved_values': [
                              obj, obj[b'a']], 
           b'all_tokens': [
                         b'a'], 
           b'resolved_tokens': [
                              b'a'], 
           b'unresolved_tokens': [], b'lookup_error': None})
        self.assertEqual(json_get_pointer_info(obj, b'/a/b'), {b'value': obj[b'a'][b'b'], 
           b'parent': obj[b'a'], 
           b'resolved_values': [
                              obj,
                              obj[b'a'],
                              obj[b'a'][b'b']], 
           b'all_tokens': [
                         b'a', b'b'], 
           b'resolved_tokens': [
                              b'a', b'b'], 
           b'unresolved_tokens': [], b'lookup_error': None})
        self.assertEqual(json_get_pointer_info(obj, b'/a/b/c'), {b'value': obj[b'a'][b'b'][b'c'], 
           b'parent': obj[b'a'][b'b'], 
           b'resolved_values': [
                              obj,
                              obj[b'a'],
                              obj[b'a'][b'b'],
                              obj[b'a'][b'b'][b'c']], 
           b'all_tokens': [
                         b'a', b'b', b'c'], 
           b'resolved_tokens': [
                              b'a', b'b', b'c'], 
           b'unresolved_tokens': [], b'lookup_error': None})
        return

    def test_with_list_item(self):
        """Testing json_get_pointer_info with valid resulting list item"""
        obj = {b'a': {b'b': {b'c': [
                              1, 2, 3]}}}
        self.assertEqual(json_get_pointer_info(obj, b'/a/b/c/0'), {b'value': 1, 
           b'parent': obj[b'a'][b'b'][b'c'], 
           b'resolved_values': [
                              obj,
                              obj[b'a'],
                              obj[b'a'][b'b'],
                              obj[b'a'][b'b'][b'c'],
                              obj[b'a'][b'b'][b'c'][0]], 
           b'all_tokens': [
                         b'a', b'b', b'c', b'0'], 
           b'resolved_tokens': [
                              b'a', b'b', b'c', b'0'], 
           b'unresolved_tokens': [], b'lookup_error': None})
        self.assertEqual(json_get_pointer_info(obj, b'/a/b/c/1'), {b'value': 2, 
           b'parent': obj[b'a'][b'b'][b'c'], 
           b'resolved_values': [
                              obj,
                              obj[b'a'],
                              obj[b'a'][b'b'],
                              obj[b'a'][b'b'][b'c'],
                              obj[b'a'][b'b'][b'c'][1]], 
           b'all_tokens': [
                         b'a', b'b', b'c', b'1'], 
           b'resolved_tokens': [
                              b'a', b'b', b'c', b'1'], 
           b'unresolved_tokens': [], b'lookup_error': None})
        self.assertEqual(json_get_pointer_info(obj, b'/a/b/c/2'), {b'value': 3, 
           b'parent': obj[b'a'][b'b'][b'c'], 
           b'resolved_values': [
                              obj,
                              obj[b'a'],
                              obj[b'a'][b'b'],
                              obj[b'a'][b'b'][b'c'],
                              obj[b'a'][b'b'][b'c'][2]], 
           b'all_tokens': [
                         b'a', b'b', b'c', b'2'], 
           b'resolved_tokens': [
                              b'a', b'b', b'c', b'2'], 
           b'unresolved_tokens': [], b'lookup_error': None})
        return

    def test_with_list_item_end_of_list(self):
        """Testing json_get_pointer_info with valid resulting list item using
        "-" for end of list
        """
        obj = {b'a': {b'b': {b'c': [
                              1, 2, 3]}}}
        self.assertEqual(json_get_pointer_info(obj, b'/a/b/c/-'), {b'value': JSONPointerEndOfList([1, 2, 3]), 
           b'parent': obj[b'a'][b'b'][b'c'], 
           b'resolved_values': [
                              obj,
                              obj[b'a'],
                              obj[b'a'][b'b'],
                              obj[b'a'][b'b'][b'c'],
                              JSONPointerEndOfList([1, 2, 3])], 
           b'all_tokens': [
                         b'a', b'b', b'c', b'-'], 
           b'resolved_tokens': [
                              b'a', b'b', b'c', b'-'], 
           b'unresolved_tokens': [], b'lookup_error': None})
        return

    def test_with_nested_lists_dicts(self):
        """Testing json_get_pointer_info with valid path containing nested
        lists and dictionaries
        """
        obj = {b'a': [
                1,
                {b'b': [
                        2, 3, b'foo']}]}
        self.assertEqual(json_get_pointer_info(obj, b'/a/1/b/2'), {b'value': b'foo', 
           b'parent': obj[b'a'][1][b'b'], 
           b'resolved_values': [
                              obj,
                              obj[b'a'],
                              obj[b'a'][1],
                              obj[b'a'][1][b'b'],
                              obj[b'a'][1][b'b'][2]], 
           b'all_tokens': [
                         b'a', b'1', b'b', b'2'], 
           b'resolved_tokens': [
                              b'a', b'1', b'b', b'2'], 
           b'unresolved_tokens': [], b'lookup_error': None})
        return

    def test_with_escaped(self):
        """Testing json_get_pointer_info with valid escaped paths"""
        obj = {b'/': {b'~': {b'~/~': 123}}}
        self.assertEqual(json_get_pointer_info(obj, b'/~1/~0/~0~1~0'), {b'value': 123, 
           b'parent': obj[b'/'][b'~'], 
           b'resolved_values': [
                              obj,
                              obj[b'/'],
                              obj[b'/'][b'~'],
                              obj[b'/'][b'~'][b'~/~']], 
           b'all_tokens': [
                         b'/', b'~', b'~/~'], 
           b'resolved_tokens': [
                              b'/', b'~', b'~/~'], 
           b'unresolved_tokens': [], b'lookup_error': None})
        return

    def test_with_bad_key(self):
        """Testing json_get_pointer_info with invalid path containing a bad
        key
        """
        obj = {b'a': {b'b': 123}}
        self.assertEqual(json_get_pointer_info(obj, b'/a/c'), {b'value': None, 
           b'parent': obj[b'a'], 
           b'resolved_values': [
                              obj,
                              obj[b'a']], 
           b'all_tokens': [
                         b'a', b'c'], 
           b'resolved_tokens': [
                              b'a'], 
           b'unresolved_tokens': [
                                b'c'], 
           b'lookup_error': b'Dictionary key "c" not found in "/a"'})
        return

    def test_with_bad_list_index(self):
        """Testing json_get_pointer_info with invalid path containing a bad
        list index
        """
        obj = {b'a': {b'b': [
                       1, 2]}}
        self.assertEqual(json_get_pointer_info(obj, b'/a/b/3'), {b'value': None, 
           b'parent': obj[b'a'][b'b'], 
           b'resolved_values': [
                              obj,
                              obj[b'a'],
                              obj[b'a'][b'b']], 
           b'all_tokens': [
                         b'a', b'b', b'3'], 
           b'resolved_tokens': [
                              b'a', b'b'], 
           b'unresolved_tokens': [
                                b'3'], 
           b'lookup_error': b'3 is outside the list in "/a/b"'})
        return

    def test_with_non_traversable_path(self):
        """Testing json_get_pointer_info with invalid path containing a
        non-traversable item
        """
        obj = {b'a': {b'b': b'test'}}
        self.assertEqual(json_get_pointer_info(obj, b'/a/b/c'), {b'value': None, 
           b'parent': obj[b'a'][b'b'], 
           b'resolved_values': [
                              obj,
                              obj[b'a'],
                              obj[b'a'][b'b']], 
           b'all_tokens': [
                         b'a', b'b', b'c'], 
           b'resolved_tokens': [
                              b'a', b'b'], 
           b'unresolved_tokens': [
                                b'c'], 
           b'lookup_error': b'Cannot resolve path within unsupported type "unicode" at "/a/b"'})
        return

    def test_with_negative_list_index(self):
        """Testing json_get_pointer_info with invalid path containing a negative
        list index
        """
        obj = {b'a': {b'b': [
                       1, 2]}}
        message = b'Negative indexes into lists are not allowed'
        with self.assertRaisesMessage(JSONPointerSyntaxError, message):
            json_get_pointer_info(obj, b'/a/b/-1')

    def test_with_index_with_leading_zero(self):
        """Testing json_get_pointer_info with invalid path containing a list
        index with a leading zero
        """
        obj = {b'a': {b'b': [
                       1, 2]}}
        message = b'List index "01" must not begin with "0"'
        with self.assertRaisesMessage(JSONPointerSyntaxError, message):
            json_get_pointer_info(obj, b'/a/b/01')

    def test_with_non_int_list_index(self):
        """Testing json_get_pointer_info with invalid path containing a
        non-integer list index
        """
        obj = {b'a': {b'b': [
                       1, 2]}}
        message = b'u\'c\' is not a valid list index in "/a/b"'
        with self.assertRaisesMessage(JSONPointerSyntaxError, message):
            json_get_pointer_info(obj, b'/a/b/c')


class JSONResolvePointerTests(TestCase):
    """Unit tests for djblets.util.json_utils.json_resolve_pointer."""

    def test_with_dict(self):
        """Testing json_resolve_pointer with valid dictionary path"""
        obj = {b'': b'hi', 
           b'a': {b'b': {b'c': 123}}}
        self.assertEqual(json_resolve_pointer(obj, b''), obj)
        self.assertEqual(json_resolve_pointer(obj, b'/'), b'hi')
        self.assertEqual(json_resolve_pointer(obj, b'/a'), {b'b': {b'c': 123}})
        self.assertEqual(json_resolve_pointer(obj, b'/a/b'), {b'c': 123})
        self.assertEqual(json_resolve_pointer(obj, b'/a/b/c'), 123)

    def test_with_list_item(self):
        """Testing json_resolve_pointer with valid resulting list item"""
        obj = {b'a': {b'b': {b'c': [
                              1, 2, 3]}}}
        self.assertEqual(json_resolve_pointer(obj, b'/a/b/c/0'), 1)
        self.assertEqual(json_resolve_pointer(obj, b'/a/b/c/1'), 2)
        self.assertEqual(json_resolve_pointer(obj, b'/a/b/c/2'), 3)

    def test_with_list_item_end_of_list(self):
        """Testing json_resolve_pointer with valid resulting list item using
        "-" for end of list
        """
        obj = {b'a': {b'b': {b'c': [
                              1, 2, 3]}}}
        self.assertIsInstance(json_resolve_pointer(obj, b'/a/b/c/-'), JSONPointerEndOfList)

    def test_with_nested_lists_dicts(self):
        """Testing json_resolve_pointer with valid path containing nested
        lists and dictionaries
        """
        obj = {b'a': [
                1,
                {b'b': [
                        2, 3, b'foo']}]}
        self.assertEqual(json_resolve_pointer(obj, b'/a/1/b/2'), b'foo')

    def test_with_escaped(self):
        """Testing json_resolve_pointer with valid escaped paths"""
        obj = {b'/': {b'~': {b'~/~': 123}}}
        self.assertEqual(json_resolve_pointer(obj, b'/~1/~0/~0~1~0'), 123)

    def test_with_bad_key(self):
        """Testing json_resolve_pointer with invalid path containing a bad
        key
        """
        obj = {b'a': {b'b': 123}}
        message = b'Dictionary key "c" not found in "/a"'
        with self.assertRaisesMessage(JSONPointerLookupError, message):
            json_resolve_pointer(obj, b'/a/c')

    def test_with_bad_list_index(self):
        """Testing json_resolve_pointer with invalid path containing a bad
        list index
        """
        obj = {b'a': {b'b': [
                       1, 2]}}
        message = b'3 is outside the list in "/a/b"'
        with self.assertRaisesMessage(JSONPointerLookupError, message):
            json_resolve_pointer(obj, b'/a/b/3')

    def test_with_non_traversable_path(self):
        """Testing json_resolve_pointer with invalid path containing a
        non-traversable item
        """
        obj = {b'a': {b'b': b'test'}}
        message = b'Cannot resolve path within unsupported type "unicode" at "/a/b"'
        with self.assertRaisesMessage(JSONPointerLookupError, message):
            json_resolve_pointer(obj, b'/a/b/c')

    def test_with_index_with_leading_zero(self):
        """Testing json_resolve_pointer with invalid path containing a negative
        list index
        """
        obj = {b'a': {b'b': [
                       1, 2]}}
        message = b'Negative indexes into lists are not allowed'
        with self.assertRaisesMessage(JSONPointerSyntaxError, message):
            json_resolve_pointer(obj, b'/a/b/-1')

    def test_with_negative_list_index(self):
        """Testing json_resolve_pointer with invalid path containing a list
        index with a leading zero
        """
        obj = {b'a': {b'b': [
                       1, 2]}}
        message = b'List index "01" must not begin with "0"'
        with self.assertRaisesMessage(JSONPointerSyntaxError, message):
            json_resolve_pointer(obj, b'/a/b/01')

    def test_with_non_int_list_index(self):
        """Testing json_resolve_pointer with invalid path containing a
        non-integer list index
        """
        obj = {b'a': {b'b': [
                       1, 2]}}
        message = b'u\'c\' is not a valid list index in "/a/b"'
        with self.assertRaisesMessage(JSONPointerSyntaxError, message):
            json_resolve_pointer(obj, b'/a/b/c')