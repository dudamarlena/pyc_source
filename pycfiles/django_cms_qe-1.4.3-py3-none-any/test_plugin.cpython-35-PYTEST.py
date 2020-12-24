# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/tomas/git/euroix/django-cms-qe/cms_qe_video/tests/test_plugin.py
# Compiled at: 2019-02-04 04:18:45
# Size of source mod 2**32: 1045 bytes
import builtins as @py_builtins, _pytest.assertion.rewrite as @pytest_ar, re
from pytest_data import use_data
from cms_qe_test import render_plugin
from ..cms_plugins import HostingVideoPlayerPlugin, SourceFileVideoPlayerPlugin

@use_data(cms_qe_video_source_file_video_player_model_data={'source_file': None})
def test_render_source_file_video_plugin_without_source_file(cms_qe_video_source_file_video_player_model):
    html = render_plugin(SourceFileVideoPlayerPlugin, cms_qe_video_source_file_video_player_model)
    @py_assert1 = re.search
    @py_assert3 = '<p>Video file is missing</p>'
    @py_assert6 = @py_assert1(@py_assert3, html)
    if not @py_assert6:
        @py_format8 = ('' + 'assert %(py7)s\n{%(py7)s = %(py2)s\n{%(py2)s = %(py0)s.search\n}(%(py4)s, %(py5)s)\n}') % {'py2': @pytest_ar._saferepr(@py_assert1), 'py4': @pytest_ar._saferepr(@py_assert3), 'py7': @pytest_ar._saferepr(@py_assert6), 'py5': @pytest_ar._saferepr(html) if 'html' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(html) else 'html', 'py0': @pytest_ar._saferepr(re) if 're' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(re) else 're'}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert6 = None


def test_render_source_file_video_plugin(cms_qe_video_source_file_video_player_model):
    html = render_plugin(SourceFileVideoPlayerPlugin, cms_qe_video_source_file_video_player_model)
    @py_assert1 = re.search
    @py_assert3 = '<iframe(\\s|.)*</iframe>'
    @py_assert6 = @py_assert1(@py_assert3, html)
    @py_assert8 = not @py_assert6
    if not @py_assert8:
        @py_format9 = ('' + 'assert not %(py7)s\n{%(py7)s = %(py2)s\n{%(py2)s = %(py0)s.search\n}(%(py4)s, %(py5)s)\n}') % {'py2': @pytest_ar._saferepr(@py_assert1), 'py4': @pytest_ar._saferepr(@py_assert3), 'py7': @pytest_ar._saferepr(@py_assert6), 'py5': @pytest_ar._saferepr(html) if 'html' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(html) else 'html', 'py0': @pytest_ar._saferepr(re) if 're' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(re) else 're'}
        raise AssertionError(@pytest_ar._format_explanation(@py_format9))
    @py_assert1 = @py_assert3 = @py_assert6 = @py_assert8 = None


def test_render_hosting_video_plugin(cms_qe_video_hosting_video_player_model):
    html = render_plugin(HostingVideoPlayerPlugin, cms_qe_video_hosting_video_player_model)
    @py_assert1 = re.search
    @py_assert3 = '<video(\\s|.)*</video>'
    @py_assert6 = @py_assert1(@py_assert3, html)
    @py_assert8 = not @py_assert6
    if not @py_assert8:
        @py_format9 = ('' + 'assert not %(py7)s\n{%(py7)s = %(py2)s\n{%(py2)s = %(py0)s.search\n}(%(py4)s, %(py5)s)\n}') % {'py2': @pytest_ar._saferepr(@py_assert1), 'py4': @pytest_ar._saferepr(@py_assert3), 'py7': @pytest_ar._saferepr(@py_assert6), 'py5': @pytest_ar._saferepr(html) if 'html' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(html) else 'html', 'py0': @pytest_ar._saferepr(re) if 're' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(re) else 're'}
        raise AssertionError(@pytest_ar._format_explanation(@py_format9))
    @py_assert1 = @py_assert3 = @py_assert6 = @py_assert8 = None
    @py_assert1 = re.search
    @py_assert3 = '<iframe(\\s|.)*</iframe>'
    @py_assert6 = @py_assert1(@py_assert3, html)
    if not @py_assert6:
        @py_format8 = ('' + 'assert %(py7)s\n{%(py7)s = %(py2)s\n{%(py2)s = %(py0)s.search\n}(%(py4)s, %(py5)s)\n}') % {'py2': @pytest_ar._saferepr(@py_assert1), 'py4': @pytest_ar._saferepr(@py_assert3), 'py7': @pytest_ar._saferepr(@py_assert6), 'py5': @pytest_ar._saferepr(html) if 'html' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(html) else 'html', 'py0': @pytest_ar._saferepr(re) if 're' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(re) else 're'}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert6 = None