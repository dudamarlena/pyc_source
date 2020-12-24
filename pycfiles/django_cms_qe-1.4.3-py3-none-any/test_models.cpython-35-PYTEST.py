# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/tomas/git/euroix/django-cms-qe/cms_qe_video/tests/test_models.py
# Compiled at: 2019-02-04 04:18:45
# Size of source mod 2**32: 4364 bytes
import builtins as @py_builtins, _pytest.assertion.rewrite as @pytest_ar, pytest
from cms_qe_video.models import VIMEO, YOUTUBE
from django.core.exceptions import ValidationError
from pytest_data import use_data
non_default_data = {'controls': False, 
 'width': 500, 
 'height': 500, 
 'autoplay': True, 
 'loop': True, 
 'muted': True}

def test__get_attributes_str_to_html_with_default_attributes(cms_qe_video_source_file_video_player_model):
    attr_str = cms_qe_video_source_file_video_player_model._get_attributes_str_to_html(('width',
                                                                                        'height',
                                                                                        'controls',
                                                                                        'autoplay',
                                                                                        'loop',
                                                                                        'muted'))
    @py_assert1 = []
    @py_assert2 = 'width=500'
    @py_assert4 = @py_assert2 not in attr_str
    @py_assert0 = @py_assert4
    if @py_assert4:
        @py_assert9 = 'height=500'
        @py_assert11 = @py_assert9 not in attr_str
        @py_assert0 = @py_assert11
    if not @py_assert0:
        @py_format6 = @pytest_ar._call_reprcompare(('not in', ), (@py_assert4,), ('%(py3)s not in %(py5)s', ), (@py_assert2, attr_str)) % {'py3': @pytest_ar._saferepr(@py_assert2), 'py5': @pytest_ar._saferepr(attr_str) if 'attr_str' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(attr_str) else 'attr_str'}
        @py_format8 = '%(py7)s' % {'py7': @py_format6}
        @py_assert1.append(@py_format8)
        if @py_assert4:
            @py_format13 = @pytest_ar._call_reprcompare(('not in', ), (@py_assert11,), ('%(py10)s not in %(py12)s', ), (@py_assert9, attr_str)) % {'py10': @pytest_ar._saferepr(@py_assert9), 'py12': @pytest_ar._saferepr(attr_str) if 'attr_str' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(attr_str) else 'attr_str'}
            @py_format15 = '%(py14)s' % {'py14': @py_format13}
            @py_assert1.append(@py_format15)
        @py_format16 = @pytest_ar._format_boolop(@py_assert1, 0) % {}
        @py_format18 = 'assert %(py17)s' % {'py17': @py_format16}
        raise AssertionError(@pytest_ar._format_explanation(@py_format18))
    @py_assert0 = @py_assert1 = @py_assert2 = @py_assert4 = @py_assert9 = @py_assert11 = None
    @py_assert0 = 'controls'
    @py_assert2 = @py_assert0 in attr_str
    if not @py_assert2:
        @py_format4 = @pytest_ar._call_reprcompare(('in', ), (@py_assert2,), ('%(py1)s in %(py3)s', ), (@py_assert0, attr_str)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py3': @pytest_ar._saferepr(attr_str) if 'attr_str' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(attr_str) else 'attr_str'}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert0 = @py_assert2 = None
    @py_assert0 = 'autoplay'
    @py_assert2 = @py_assert0 not in attr_str
    if not @py_assert2:
        @py_format4 = @pytest_ar._call_reprcompare(('not in', ), (@py_assert2,), ('%(py1)s not in %(py3)s', ), (@py_assert0, attr_str)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py3': @pytest_ar._saferepr(attr_str) if 'attr_str' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(attr_str) else 'attr_str'}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert0 = @py_assert2 = None
    @py_assert0 = 'loop'
    @py_assert2 = @py_assert0 not in attr_str
    if not @py_assert2:
        @py_format4 = @pytest_ar._call_reprcompare(('not in', ), (@py_assert2,), ('%(py1)s not in %(py3)s', ), (@py_assert0, attr_str)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py3': @pytest_ar._saferepr(attr_str) if 'attr_str' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(attr_str) else 'attr_str'}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert0 = @py_assert2 = None
    @py_assert0 = 'muted'
    @py_assert2 = @py_assert0 not in attr_str
    if not @py_assert2:
        @py_format4 = @pytest_ar._call_reprcompare(('not in', ), (@py_assert2,), ('%(py1)s not in %(py3)s', ), (@py_assert0, attr_str)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py3': @pytest_ar._saferepr(attr_str) if 'attr_str' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(attr_str) else 'attr_str'}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert0 = @py_assert2 = None


@use_data(cms_qe_video_source_file_video_player_model_data=non_default_data)
def test__get_attributes_str_to_html_with_non_default_attributes(cms_qe_video_source_file_video_player_model):
    attr_str = cms_qe_video_source_file_video_player_model._get_attributes_str_to_html(('width',
                                                                                        'height',
                                                                                        'controls',
                                                                                        'autoplay',
                                                                                        'loop',
                                                                                        'muted'))
    @py_assert1 = []
    @py_assert2 = 'width=500'
    @py_assert4 = @py_assert2 in attr_str
    @py_assert0 = @py_assert4
    if @py_assert4:
        @py_assert9 = 'height=500'
        @py_assert11 = @py_assert9 in attr_str
        @py_assert0 = @py_assert11
    if not @py_assert0:
        @py_format6 = @pytest_ar._call_reprcompare(('in', ), (@py_assert4,), ('%(py3)s in %(py5)s', ), (@py_assert2, attr_str)) % {'py3': @pytest_ar._saferepr(@py_assert2), 'py5': @pytest_ar._saferepr(attr_str) if 'attr_str' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(attr_str) else 'attr_str'}
        @py_format8 = '%(py7)s' % {'py7': @py_format6}
        @py_assert1.append(@py_format8)
        if @py_assert4:
            @py_format13 = @pytest_ar._call_reprcompare(('in', ), (@py_assert11,), ('%(py10)s in %(py12)s', ), (@py_assert9, attr_str)) % {'py10': @pytest_ar._saferepr(@py_assert9), 'py12': @pytest_ar._saferepr(attr_str) if 'attr_str' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(attr_str) else 'attr_str'}
            @py_format15 = '%(py14)s' % {'py14': @py_format13}
            @py_assert1.append(@py_format15)
        @py_format16 = @pytest_ar._format_boolop(@py_assert1, 0) % {}
        @py_format18 = 'assert %(py17)s' % {'py17': @py_format16}
        raise AssertionError(@pytest_ar._format_explanation(@py_format18))
    @py_assert0 = @py_assert1 = @py_assert2 = @py_assert4 = @py_assert9 = @py_assert11 = None
    @py_assert0 = 'controls'
    @py_assert2 = @py_assert0 not in attr_str
    if not @py_assert2:
        @py_format4 = @pytest_ar._call_reprcompare(('not in', ), (@py_assert2,), ('%(py1)s not in %(py3)s', ), (@py_assert0, attr_str)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py3': @pytest_ar._saferepr(attr_str) if 'attr_str' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(attr_str) else 'attr_str'}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert0 = @py_assert2 = None
    @py_assert0 = 'autoplay'
    @py_assert2 = @py_assert0 in attr_str
    if not @py_assert2:
        @py_format4 = @pytest_ar._call_reprcompare(('in', ), (@py_assert2,), ('%(py1)s in %(py3)s', ), (@py_assert0, attr_str)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py3': @pytest_ar._saferepr(attr_str) if 'attr_str' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(attr_str) else 'attr_str'}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert0 = @py_assert2 = None
    @py_assert0 = 'loop'
    @py_assert2 = @py_assert0 in attr_str
    if not @py_assert2:
        @py_format4 = @pytest_ar._call_reprcompare(('in', ), (@py_assert2,), ('%(py1)s in %(py3)s', ), (@py_assert0, attr_str)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py3': @pytest_ar._saferepr(attr_str) if 'attr_str' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(attr_str) else 'attr_str'}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert0 = @py_assert2 = None
    @py_assert0 = 'muted'
    @py_assert2 = @py_assert0 in attr_str
    if not @py_assert2:
        @py_format4 = @pytest_ar._call_reprcompare(('in', ), (@py_assert2,), ('%(py1)s in %(py3)s', ), (@py_assert0, attr_str)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py3': @pytest_ar._saferepr(attr_str) if 'attr_str' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(attr_str) else 'attr_str'}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert0 = @py_assert2 = None


def test__get_attributes_str_to_url_with_default_attributes(cms_qe_video_source_file_video_player_model):
    attr_str = cms_qe_video_source_file_video_player_model._get_attributes_str_to_url(('width',
                                                                                       'height',
                                                                                       'controls',
                                                                                       'autoplay',
                                                                                       'loop',
                                                                                       'muted'))
    @py_assert1 = []
    @py_assert2 = 'width'
    @py_assert4 = @py_assert2 not in attr_str
    @py_assert0 = @py_assert4
    if @py_assert4:
        @py_assert9 = 'height'
        @py_assert11 = @py_assert9 not in attr_str
        @py_assert0 = @py_assert11
    if not @py_assert0:
        @py_format6 = @pytest_ar._call_reprcompare(('not in', ), (@py_assert4,), ('%(py3)s not in %(py5)s', ), (@py_assert2, attr_str)) % {'py3': @pytest_ar._saferepr(@py_assert2), 'py5': @pytest_ar._saferepr(attr_str) if 'attr_str' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(attr_str) else 'attr_str'}
        @py_format8 = '%(py7)s' % {'py7': @py_format6}
        @py_assert1.append(@py_format8)
        if @py_assert4:
            @py_format13 = @pytest_ar._call_reprcompare(('not in', ), (@py_assert11,), ('%(py10)s not in %(py12)s', ), (@py_assert9, attr_str)) % {'py10': @pytest_ar._saferepr(@py_assert9), 'py12': @pytest_ar._saferepr(attr_str) if 'attr_str' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(attr_str) else 'attr_str'}
            @py_format15 = '%(py14)s' % {'py14': @py_format13}
            @py_assert1.append(@py_format15)
        @py_format16 = @pytest_ar._format_boolop(@py_assert1, 0) % {}
        @py_format18 = 'assert %(py17)s' % {'py17': @py_format16}
        raise AssertionError(@pytest_ar._format_explanation(@py_format18))
    @py_assert0 = @py_assert1 = @py_assert2 = @py_assert4 = @py_assert9 = @py_assert11 = None
    @py_assert0 = 'controls=1'
    @py_assert2 = @py_assert0 in attr_str
    if not @py_assert2:
        @py_format4 = @pytest_ar._call_reprcompare(('in', ), (@py_assert2,), ('%(py1)s in %(py3)s', ), (@py_assert0, attr_str)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py3': @pytest_ar._saferepr(attr_str) if 'attr_str' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(attr_str) else 'attr_str'}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert0 = @py_assert2 = None
    @py_assert0 = 'autoplay'
    @py_assert2 = @py_assert0 not in attr_str
    if not @py_assert2:
        @py_format4 = @pytest_ar._call_reprcompare(('not in', ), (@py_assert2,), ('%(py1)s not in %(py3)s', ), (@py_assert0, attr_str)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py3': @pytest_ar._saferepr(attr_str) if 'attr_str' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(attr_str) else 'attr_str'}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert0 = @py_assert2 = None
    @py_assert0 = 'loop'
    @py_assert2 = @py_assert0 not in attr_str
    if not @py_assert2:
        @py_format4 = @pytest_ar._call_reprcompare(('not in', ), (@py_assert2,), ('%(py1)s not in %(py3)s', ), (@py_assert0, attr_str)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py3': @pytest_ar._saferepr(attr_str) if 'attr_str' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(attr_str) else 'attr_str'}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert0 = @py_assert2 = None
    @py_assert0 = 'muted'
    @py_assert2 = @py_assert0 not in attr_str
    if not @py_assert2:
        @py_format4 = @pytest_ar._call_reprcompare(('not in', ), (@py_assert2,), ('%(py1)s not in %(py3)s', ), (@py_assert0, attr_str)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py3': @pytest_ar._saferepr(attr_str) if 'attr_str' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(attr_str) else 'attr_str'}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert0 = @py_assert2 = None


@use_data(cms_qe_video_source_file_video_player_model_data=non_default_data)
def test__get_attributes_str_to_url_with_non_default_attributes(cms_qe_video_source_file_video_player_model):
    attr_str = cms_qe_video_source_file_video_player_model._get_attributes_str_to_url(('width',
                                                                                       'height',
                                                                                       'controls',
                                                                                       'autoplay',
                                                                                       'loop',
                                                                                       'muted'))
    @py_assert1 = []
    @py_assert2 = 'width=500'
    @py_assert4 = @py_assert2 in attr_str
    @py_assert0 = @py_assert4
    if @py_assert4:
        @py_assert9 = 'height=500'
        @py_assert11 = @py_assert9 in attr_str
        @py_assert0 = @py_assert11
    if not @py_assert0:
        @py_format6 = @pytest_ar._call_reprcompare(('in', ), (@py_assert4,), ('%(py3)s in %(py5)s', ), (@py_assert2, attr_str)) % {'py3': @pytest_ar._saferepr(@py_assert2), 'py5': @pytest_ar._saferepr(attr_str) if 'attr_str' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(attr_str) else 'attr_str'}
        @py_format8 = '%(py7)s' % {'py7': @py_format6}
        @py_assert1.append(@py_format8)
        if @py_assert4:
            @py_format13 = @pytest_ar._call_reprcompare(('in', ), (@py_assert11,), ('%(py10)s in %(py12)s', ), (@py_assert9, attr_str)) % {'py10': @pytest_ar._saferepr(@py_assert9), 'py12': @pytest_ar._saferepr(attr_str) if 'attr_str' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(attr_str) else 'attr_str'}
            @py_format15 = '%(py14)s' % {'py14': @py_format13}
            @py_assert1.append(@py_format15)
        @py_format16 = @pytest_ar._format_boolop(@py_assert1, 0) % {}
        @py_format18 = 'assert %(py17)s' % {'py17': @py_format16}
        raise AssertionError(@pytest_ar._format_explanation(@py_format18))
    @py_assert0 = @py_assert1 = @py_assert2 = @py_assert4 = @py_assert9 = @py_assert11 = None
    @py_assert0 = 'controls'
    @py_assert2 = @py_assert0 not in attr_str
    if not @py_assert2:
        @py_format4 = @pytest_ar._call_reprcompare(('not in', ), (@py_assert2,), ('%(py1)s not in %(py3)s', ), (@py_assert0, attr_str)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py3': @pytest_ar._saferepr(attr_str) if 'attr_str' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(attr_str) else 'attr_str'}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert0 = @py_assert2 = None
    @py_assert0 = 'autoplay=1'
    @py_assert2 = @py_assert0 in attr_str
    if not @py_assert2:
        @py_format4 = @pytest_ar._call_reprcompare(('in', ), (@py_assert2,), ('%(py1)s in %(py3)s', ), (@py_assert0, attr_str)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py3': @pytest_ar._saferepr(attr_str) if 'attr_str' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(attr_str) else 'attr_str'}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert0 = @py_assert2 = None
    @py_assert0 = 'loop=1'
    @py_assert2 = @py_assert0 in attr_str
    if not @py_assert2:
        @py_format4 = @pytest_ar._call_reprcompare(('in', ), (@py_assert2,), ('%(py1)s in %(py3)s', ), (@py_assert0, attr_str)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py3': @pytest_ar._saferepr(attr_str) if 'attr_str' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(attr_str) else 'attr_str'}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert0 = @py_assert2 = None
    @py_assert0 = 'muted=1'
    @py_assert2 = @py_assert0 in attr_str
    if not @py_assert2:
        @py_format4 = @pytest_ar._call_reprcompare(('in', ), (@py_assert2,), ('%(py1)s in %(py3)s', ), (@py_assert0, attr_str)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py3': @pytest_ar._saferepr(attr_str) if 'attr_str' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(attr_str) else 'attr_str'}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert0 = @py_assert2 = None
    @py_assert1 = attr_str.count
    @py_assert3 = '&'
    @py_assert5 = @py_assert1(@py_assert3)
    @py_assert8 = 4
    @py_assert7 = @py_assert5 == @py_assert8
    if not @py_assert7:
        @py_format10 = @pytest_ar._call_reprcompare(('==', ), (@py_assert7,), ('%(py6)s\n{%(py6)s = %(py2)s\n{%(py2)s = %(py0)s.count\n}(%(py4)s)\n} == %(py9)s', ), (@py_assert5, @py_assert8)) % {'py6': @pytest_ar._saferepr(@py_assert5), 'py2': @pytest_ar._saferepr(@py_assert1), 'py4': @pytest_ar._saferepr(@py_assert3), 'py9': @pytest_ar._saferepr(@py_assert8), 'py0': @pytest_ar._saferepr(attr_str) if 'attr_str' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(attr_str) else 'attr_str'}
        @py_format12 = 'assert %(py11)s' % {'py11': @py_format10}
        raise AssertionError(@pytest_ar._format_explanation(@py_format12))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert8 = None


@use_data(cms_qe_video_hosting_video_player_model_data={'video_hosting_service': YOUTUBE, 
 'video_url': 'isnotyoutube.com/somevideo'})
def test_clean_youtube_bad_url(cms_qe_video_hosting_video_player_model):
    with pytest.raises(ValidationError) as (validation_exception):
        cms_qe_video_hosting_video_player_model.clean()
    validation_exception.match('.*YouTube.*')


@use_data(cms_qe_video_hosting_video_player_model_data={'video_hosting_service': VIMEO, 
 'video_url': 'notvimeo.com/somevideo'})
def test_clean_vimeo_bad_url(cms_qe_video_hosting_video_player_model):
    with pytest.raises(ValidationError) as (validation_exception):
        cms_qe_video_hosting_video_player_model.clean()
    validation_exception.match('.*Vimeo.*')


@use_data(cms_qe_video_hosting_video_player_model_data={'video_url': 'youtube.com/somevideo', 
 'video_hosting_service': YOUTUBE})
def test_clean_youtube_good_urls(cms_qe_video_hosting_video_player_model):
    cms_qe_video_hosting_video_player_model.clean()


@use_data(cms_qe_video_hosting_video_player_model_data={'video_url': 'vimeo.com/somevideo', 
 'video_hosting_service': VIMEO})
def test_clean_vimeo_good_urls(cms_qe_video_hosting_video_player_model):
    cms_qe_video_hosting_video_player_model.clean()


@use_data(cms_qe_video_hosting_video_player_model_data={'video_url': 'vimeo.com/somevideo', 
 'video_hosting_service': VIMEO, 
 'controls': False})
def test_clean_vimeo_disabled_controls(cms_qe_video_hosting_video_player_model):
    with pytest.raises(ValidationError) as (validation_exception):
        cms_qe_video_hosting_video_player_model.clean()
    validation_exception.match('.*Vimeo.*controls.*')