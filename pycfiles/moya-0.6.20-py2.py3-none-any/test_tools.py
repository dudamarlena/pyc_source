# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/will/projects/moya/moya/tests/test_tools.py
# Compiled at: 2015-11-12 15:26:48
from __future__ import unicode_literals
from __future__ import print_function
from moya import tools
from moya.context.missing import Missing
from moya.compat import text_type
from moya.elements.elementbase import ReturnContainer
import pytz, datetime, unittest, io, os.path

class TestTools(unittest.TestCase):

    def test_extract_namespace(self):
        tests = [
         (
          b'{http://moyaproject.com}test1', ('http://moyaproject.com', 'test1')),
         (
          b'test2', ('http://moyaproject.com', 'test2')),
         (
          b'{http://moyaproject.com/db}query', ('http://moyaproject.com/db', 'query'))]
        for test, result in tests:
            self.assertEqual(tools.extract_namespace(test), result)

    def test_asint(self):
        assert tools.asint(b'5') == 5
        assert tools.asint(b'-5') == -5
        assert tools.asint(b'foo', 3) == 3

    def test_match_exception(self):
        tests = [
         (
          b'*', b'anything', True),
         (
          b'foo', b'foo', True),
         (
          b'foo.bar', b'foo.bar', True),
         (
          b'foo.*', b'foo.bar', True),
         (
          b'foo.*', b'foo.bar.baz', True),
         (
          b'bar', b'foo', False),
         (
          b'foo.bar.*', b'foo.baz.egg', False)]
        for m, exc, result in tests:
            print(exc, m, result)
            assert tools.match_exception(exc, m) == result

    def test_md5_hexdigest(self):
        assert tools.md5_hexdigest(b'foo') == b'acbd18db4cc2f85cedef654fccc4a4d8'

    def test_check_missing(self):
        tools.check_missing({b'foo': b'bar'})
        try:
            tools.check_missing({b'foo': Missing(b'bar')})
        except ValueError:
            pass
        else:
            assert False

    def test_timer(self):
        with tools.timer(b'foo'):
            pass
        with tools.timer(b'foo', ms=True):
            pass
        with tools.timer(b'foo', write_file=b'/tmp/__timertest__'):
            pass

    def test_parse_timedelta(self):
        assert tools.parse_timedelta(b'10') == 10
        assert tools.parse_timedelta(b'10s') == 10000
        assert tools.parse_timedelta(b'1m') == 60000
        try:
            tools.parse_timedelta(b'agfdwrg')
        except ValueError:
            assert True
        else:
            assert False

    def test_get_moya_dir(self):
        moya_dir = os.path.join(os.path.dirname(__file__), b'moyadir')
        path = os.path.join(moya_dir, b'foo')
        assert tools.get_moya_dir(path) == moya_dir
        try:
            tools.get_moya_dir()
        except ValueError:
            assert True
        else:
            assert False

        try:
            tools.get_moya_dir(b'/')
        except ValueError:
            assert True
        else:
            assert False

    def test_is_moya_dir(self):
        moya_dir = os.path.join(os.path.dirname(__file__), b'moyadir')
        path = os.path.join(moya_dir, b'foo')
        assert not tools.is_moya_dir(path)
        assert tools.is_moya_dir(moya_dir)
        assert not tools.is_moya_dir(b'/')
        assert not tools.is_moya_dir()

    def test_file_chunker(self):
        text = b'Hello, World'
        f = io.BytesIO(text)
        chunks = list(tools.file_chunker(f, 1))
        assert chunks == [b'H', b'e', b'l', b'l', b'o', b',', b' ', b'W', b'o', b'r', b'l', b'd']
        f = io.BytesIO(text)
        chunks = list(tools.file_chunker(f, 2))
        assert chunks == [b'He', b'll', b'o,', b' W', b'or', b'ld']
        f = io.BytesIO(text)
        chunks = list(tools.file_chunker(f, 256))
        assert chunks == [text]

    def test_make_id(self):
        assert tools.make_id() != tools.make_id()

    def test_datetime_to_epoch(self):
        assert tools.datetime_to_epoch(100) == 100
        epoch_start = datetime.datetime(1970, 1, 1, 0, 0, tzinfo=pytz.UTC)
        self.assertEqual(tools.datetime_to_epoch(epoch_start), 0)

    def test_split_commas(self):
        assert tools.split_commas(b'foo, bar') == [b'foo', b'bar']

    def test_summarize_text(self):
        assert tools.summarize_text(None) == b''
        assert tools.summarize_text(b'hello') == b'hello'
        assert tools.summarize_text(b'hello, world', max_length=5) == b'hello[...]'
        return

    def test_get_return(self):
        assert tools.get_return(None) == {}
        assert tools.get_return(100) == 100
        ret = ReturnContainer(b'foo')
        assert tools.get_return(ret) == b'foo'
        return

    def test_as_dict(self):
        assert tools.as_dict({b'foo': b'bar'}) == {b'foo': b'bar'}

        class D(object):

            def items(self):
                return [
                 ('foo', 'bar')]

            def iteritems(self):
                return iter(self.items())

        d = D()
        assert tools.as_dict(d) == {b'foo': b'bar'}

    def test_quote(self):
        assert tools.quote(b'hello') == b'"hello"'

    def test_squote(self):
        assert tools.squote(b'hello') == b"'hello'"

    def test_textual_list(self):
        assert tools.textual_list([b'foo', b'bar']) == b"'foo' or 'bar'"
        assert tools.textual_list([b'foo', b'bar', b'baz']) == b"'foo', 'bar' or 'baz'"
        assert tools.textual_list([b'foo']) == b"'foo'"
        assert tools.textual_list([], empty=b'nadda') == b'nadda'

    def test_moya_update(self):
        d = {}
        tools.moya_update(d, {b'foo': b'bar'})
        self.assertEqual(d, {b'foo': b'bar'})

    def test_url_join(self):
        assert tools.url_join(b'http://moyaproject.com/', b'/foo/') == b'http://moyaproject.com/foo/'

    def test_remove_padding(self):
        assert tools.remove_padding(b'    ') == b''
        assert tools.remove_padding(b'') == b''
        assert tools.remove_padding(b'  hello  ') == b'  hello  '
        assert tools.remove_padding(b'\n\nhello\n\n') == b'hello'
        assert tools.remove_padding(b'\n\nhello\nworld\n\n') == b'hello\nworld'

    def test_unique(self):
        assert tools.unique([]) == []
        assert tools.unique([b'foo']) == [b'foo']
        assert tools.unique([b'foo', b'bar']) == [b'foo', b'bar']
        assert tools.unique([b'foo', b'bar', b'bar', b'bar', b'baz']) == [b'foo', b'bar', b'baz']
        assert tools.unique(5) == []

    def test_format_element_type(self):
        assert tools.format_element_type(('foo', 'bar')) == b'{foo}bar'
        assert tools.format_element_type(b'foo') == b'foo'

    def test_multi_replace(self):
        replacer = tools.MultiReplace({b'foo': b'bar', b'baz': b'egg'})
        assert replacer(b'foo baz foo ok') == b'bar egg bar ok'

    def test_dummy_lock(self):
        with tools.DummyLock() as (_lock):
            pass

    def test_make_cache_key(self):
        assert tools.make_cache_key([b'foo', b'bar']) == b'foo.bar'
        assert tools.make_cache_key([b'foo', b'bar', [1, 2]]) == b'foo.bar.1-2'
        assert tools.make_cache_key([b'foo', b'bar', [1, 2], {b'foo': b'bar'}]) == b'foo.bar.1-2.foo_bar'

    def test_nearers_word(self):
        assert tools.nearest_word(b'floo', [b'foo', b'bar']) == b'foo'

    def test_show_tb(self):

        @tools.show_tb
        def test():
            raise Exception(b'everything is fine')

        try:
            test()
        except:
            assert True
        else:
            assert False

    def test_normalize_url_path(self):
        assert tools.normalize_url_path(b'') == b'/'
        assert tools.normalize_url_path(b'foo') == b'/foo/'
        assert tools.normalize_url_path(b'foo/bar') == b'/foo/bar/'

    def test_lazystr(self):
        s = tools.lazystr(lambda : b'foo')
        assert text_type(s) == b'foo'
        s = tools.lazystr(lambda : b'foo')
        assert len(s) == 3
        s = tools.lazystr(lambda : b'foo')
        assert s.upper() == b'FOO'