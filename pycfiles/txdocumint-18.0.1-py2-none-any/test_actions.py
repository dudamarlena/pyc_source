# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/jonathan/Coding/txdocumint/txdocumint/test/test_actions.py
# Compiled at: 2018-07-02 07:11:41
from testtools import TestCase
from testtools.matchers import Equals
from txdocumint import actions

class RenderHTMLTests(TestCase):
    """
    Tests for `txdocumint.actions.render_html`.
    """

    def test_no_base_uri(self):
        """
        Construct a ``render-html`` action without a base URI.
        """
        action, _ = actions.render_html('http://example.com/input1')
        self.assertThat(action, Equals({'action': 'render-html', 'parameters': {'input': 'http://example.com/input1'}}))

    def test_base_uri(self):
        """
        Construct a ``render-html`` action with a base URI.
        """
        action, _ = actions.render_html('http://example.com/input1', 'http://example.com/')
        self.assertThat(action, Equals({'action': 'render-html', 'parameters': {'input': 'http://example.com/input1', 
                          'base-uri': 'http://example.com/'}}))

    def test_parser(self):
        """
        Parse the output of the ``render-html`` action.
        """
        _, parser = actions.render_html('http://example.com/input1')
        result = {'links': {'result': ['http://example.com/output1']}}
        self.assertThat(parser(result), Equals('http://example.com/output1'))


class RenderLegacyHTMLTests(TestCase):
    """
    Tests for `txdocumint.actions.render_legacy_html`.
    """

    def test_no_base_uri(self):
        """
        Construct a ``render-legacy-html`` action without a base URI.
        """
        action, _ = actions.render_legacy_html('http://example.com/input1')
        self.assertThat(action, Equals({'action': 'render-legacy-html', 'parameters': {'input': 'http://example.com/input1'}}))

    def test_base_uri(self):
        """
        Construct a ``render-legacy-html`` action with a base URI.
        """
        action, _ = actions.render_legacy_html('http://example.com/input1', 'http://example.com/')
        self.assertThat(action, Equals({'action': 'render-legacy-html', 'parameters': {'input': 'http://example.com/input1', 
                          'base-uri': 'http://example.com/'}}))

    def test_parser(self):
        """
        Parse the output of the ``render-legacy-html`` action.
        """
        _, parser = actions.render_legacy_html('http://example.com/input1')
        result = {'links': {'result': ['http://example.com/output1']}}
        self.assertThat(parser(result), Equals('http://example.com/output1'))


class ConcatenateTests(TestCase):
    """
    Tests for `txdocumint.actions.concatenate`.
    """

    def test_action(self):
        """
        Construct a ``concatenate`` action..
        """
        action, _ = actions.concatenate(['http://example.com/input1',
         'http://example.com/input2'])
        self.assertThat(action, Equals({'action': 'concatenate', 'parameters': {'inputs': [
                                   'http://example.com/input1',
                                   'http://example.com/input2']}}))

    def test_parser(self):
        """
        Parse the output of the ``concatenate`` action.
        """
        _, parser = actions.concatenate(['http://example.com/input1',
         'http://example.com/input2'])
        result = {'links': {'result': ['http://example.com/output1']}}
        self.assertThat(parser(result), Equals('http://example.com/output1'))


class ThumbnailsTests(TestCase):
    """
    Tests for `txdocumint.actions.thumbnails`.
    """

    def test_action(self):
        """
        Construct a ``thumbnails`` action..
        """
        action, _ = actions.thumbnails('http://example.com/input1', 100)
        self.assertThat(action, Equals({'action': 'thumbnails', 'parameters': {'input': 'http://example.com/input1', 
                          'dpi': 100}}))

    def test_parser(self):
        """
        Parse the output of the ``thumbnails`` action.
        """
        _, parser = actions.thumbnails('http://example.com/input1', 100)
        result = {'links': {'results': ['http://example.com/output1',
                               'http://example.com/output2']}}
        self.assertThat(parser(result), Equals(['http://example.com/output1',
         'http://example.com/output2']))


class SplitTests(TestCase):
    """
    Tests for `txdocumint.actions.split`.
    """

    def test_action(self):
        """
        Construct a ``split`` action..
        """
        action, _ = actions.split('http://example.com/input1', [
         [
          1, 2], [2, 3]])
        self.assertThat(action, Equals({'action': 'split', 'parameters': {'input': 'http://example.com/input1', 
                          'page-groups': [
                                        [
                                         1, 2], [2, 3]]}}))

    def test_parser(self):
        """
        Parse the output of the ``split`` action.
        """
        _, parser = actions.split('http://example.com/input1', [
         [
          1, 2], [2, 3]])
        result = {'links': {'results': ['http://example.com/output1',
                               'http://example.com/output2']}}
        self.assertThat(parser(result), Equals(['http://example.com/output1',
         'http://example.com/output2']))


class MetadataTests(TestCase):
    """
    Tests for `txdocumint.actions.metadata`.
    """

    def test_action(self):
        """
        Construct a ``metadata`` action..
        """
        action, _ = actions.metadata('http://example.com/input1')
        self.assertThat(action, Equals({'action': 'metadata', 'parameters': {'input': 'http://example.com/input1'}}))

    def test_parser(self):
        """
        Parse the output of the ``metadata`` action.
        """
        _, parser = actions.metadata('http://example.com/input1')
        result = {'body': {'page-count': 3, 'title': 'Hello World'}}
        self.assertThat(parser(result), Equals({'page-count': 3, 'title': 'Hello World'}))


class SignTests(TestCase):
    """
    Tests for `txdocumint.actions.sign`.
    """

    def test_action(self):
        """
        Construct a ``sign`` action..
        """
        action, _ = actions.sign(['http://example.com/input1',
         'http://example.com/input2'], 'c', 'l', 'r')
        self.assertThat(action, Equals({'action': 'sign', 'parameters': {'inputs': [
                                   'http://example.com/input1',
                                   'http://example.com/input2'], 
                          'certificate-alias': 'c', 
                          'location': 'l', 
                          'reason': 'r'}}))

    def test_parser(self):
        """
        Parse the output of the ``sign`` action.
        """
        _, parser = actions.sign(['http://example.com/input1',
         'http://example.com/input2'], 'c', 'l', 'r')
        result = {'links': {'results': ['http://example.com/output1',
                               'http://example.com/output2']}}
        self.assertThat(parser(result), Equals(['http://example.com/output1',
         'http://example.com/output2']))


class CrushTests(TestCase):
    """
    Tests for `txdocumint.actions.crush`.
    """

    def test_action(self):
        """
        Construct a ``crush`` action..
        """
        action, _ = actions.crush('http://example.com/input1', 'text')
        self.assertThat(action, Equals({'action': 'crush', 'parameters': {'input': 'http://example.com/input1', 
                          'compression-profile': 'text'}}))

    def test_parser(self):
        """
        Parse the output of the ``crush`` action.
        """
        _, parser = actions.crush('http://example.com/input1', 'text')
        result = {'links': {'result': ['http://example.com/output1']}}
        self.assertThat(parser(result), Equals('http://example.com/output1'))


class StampTests(TestCase):
    """
    Tests for `txdocumint.actions.stamp`.
    """

    def test_action(self):
        """
        Construct a ``stamp`` action..
        """
        action, _ = actions.stamp('http://example.com/watermark', [
         'http://example.com/input1',
         'http://example.com/input2'])
        self.assertThat(action, Equals({'action': 'stamp', 'parameters': {'watermark': 'http://example.com/watermark', 
                          'inputs': [
                                   'http://example.com/input1',
                                   'http://example.com/input2']}}))

    def test_parser(self):
        """
        Parse the output of the ``stamp`` action.
        """
        _, parser = actions.stamp('http://example.com/watermark', [
         'http://example.com/input1',
         'http://example.com/input2'])
        result = {'links': {'results': ['http://example.com/output1',
                               'http://example.com/output2']}}
        self.assertThat(parser(result), Equals(['http://example.com/output1',
         'http://example.com/output2']))