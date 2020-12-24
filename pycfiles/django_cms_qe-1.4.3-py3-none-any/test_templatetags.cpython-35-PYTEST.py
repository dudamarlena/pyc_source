# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/tomas/git/euroix/django-cms-qe/cms_qe_video/tests/test_templatetags.py
# Compiled at: 2019-02-04 04:18:45
# Size of source mod 2**32: 1018 bytes
import builtins as @py_builtins, _pytest.assertion.rewrite as @pytest_ar
from ..templatetags.cms_qe_video import cms_qe_video_url_to_embed
import pytest

@pytest.mark.parametrize('url, expected', [
 ('https://servis.com/somevideo', 'https://servis.com/somevideo'),
 ('http://vimeo.com/somevideo', 'http://player.vimeo.com/video/somevideo'),
 ('https://vimeo.com/somevideo', 'https://player.vimeo.com/video/somevideo'),
 ('https://vimeo.com/somevideo?param', 'https://player.vimeo.com/video/somevideo'),
 ('https://youtu.be/watch?v=ZGuQmszmtaQ', 'https://www.youtube.com/embed/ZGuQmszmtaQ'),
 ('https://www.youtube.com/watch?v=ZGuQmszmtaQ', 'https://www.youtube.com/embed/ZGuQmszmtaQ'),
 ('https://www.youtube.com/watch?v=ZGuQmszmtaQ&index=10&list=PLfTu7SiuiT_izjvg_1JRKXkrWSnvuP4pd',
 'https://www.youtube.com/embed/ZGuQmszmtaQ')])
def test_url_to_embed(url, expected):
    @py_assert4 = cms_qe_video_url_to_embed(url)
    @py_assert1 = expected == @py_assert4
    if not @py_assert1:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py5)s\n{%(py5)s = %(py2)s(%(py3)s)\n}', ), (expected, @py_assert4)) % {'py2': @pytest_ar._saferepr(cms_qe_video_url_to_embed) if 'cms_qe_video_url_to_embed' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(cms_qe_video_url_to_embed) else 'cms_qe_video_url_to_embed', 'py3': @pytest_ar._saferepr(url) if 'url' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(url) else 'url', 'py5': @pytest_ar._saferepr(@py_assert4), 'py0': @pytest_ar._saferepr(expected) if 'expected' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(expected) else 'expected'}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert4 = None