# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\rbtools\commands\tests\test_post.py
# Compiled at: 2017-04-19 05:14:04
"""Test for RBTools post command."""
from __future__ import unicode_literals
from rbtools.commands import CommandError
from rbtools.commands.post import Post
from rbtools.utils.testbase import RBTestBase

class PostCommandTests(RBTestBase):
    """Tests for rbt post command."""

    def _create_post_command(self, fields):
        """Create an argument parser with the given extra fields.

        Args:
            fields (list of unicode):
                A list of key-value pairs for the field argument.

                Each pair should be of the form key=value.

        Returns:
            argparse.ArgumentParser:
            Argument parser for commandline arguments
        """
        post = Post()
        argv = [b'rbt', b'post']
        parser = post.create_arg_parser(argv)
        post.options = parser.parse_args(argv[2:])
        post.options.fields = fields
        return post

    def test_post_one_extra_fields(self):
        """Testing one extra field argument with rbt post --field foo=bar"""
        post = self._create_post_command([b'foo=bar'])
        post.post_process_options()
        self.assertEqual(post.options.extra_fields, {b'extra_data.foo': b'bar'})

    def test_post_multiple_extra_fields(self):
        """Testing multiple extra field arguments with rbt post --field
        foo=bar --field desc=new
        """
        post = self._create_post_command([b'foo=bar', b'desc=new'])
        post.post_process_options()
        self.assertEqual(post.options.extra_fields, {b'extra_data.foo': b'bar', 
           b'extra_data.desc': b'new'})

    def test_native_fields_through_extra_fields(self):
        """Testing built-in fields through extra_fields with rbt post --field
        description=testing --field summary='native testing' --field
        testing-done='No tests'
        """
        post = self._create_post_command([
         b'description=testing',
         b'summary=native testing',
         b'testing-done=No tests'])
        post.post_process_options()
        self.assertEqual(post.options.description, b'testing')
        self.assertEqual(post.options.summary, b'native testing')
        self.assertEqual(post.options.testing_done, b'No tests')

    def test_wrong_argument_entry(self):
        """Testing built-in fields through extra_fields with rbt post --field
        description and rbt post --field testing_done='No tests'
        """
        post = self._create_post_command([b'testing_done=No tests'])
        self.assertEqual(post.options.testing_done, None)
        post = self._create_post_command([b'description'])
        self.assertRaises(CommandError, post.post_process_options)
        return

    def test_multiple_delimiter(self):
        """Testing multiple delimiters with rbt post --field
        myField=this=string=has=equals=signs
        """
        post = self._create_post_command([
         b'myField=this=string=has=equals=signs'])
        post.post_process_options()
        self.assertEqual(post.options.extra_fields, {b'extra_data.myField': b'this=string=has=equals=signs'})

    def test_arg_field_set_again_by_custom_fields(self):
        """Testing argument duplication with rbt post --field
        myField=test --description test
        """
        post = self._create_post_command([b'description=test'])
        post.options.description = b'test'
        self.assertRaises(CommandError, post.post_process_options)