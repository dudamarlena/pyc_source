# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/tomas/git/euroix/django-cms-qe/cms_qe_video/fixtures.py
# Compiled at: 2019-02-04 04:18:45
# Size of source mod 2**32: 701 bytes
from unittest.mock import Mock
import pytest
from filer.models import File
from pytest_data import get_data
from .models import HostingVideoPlayer, SourceFileVideoPlayer

@pytest.fixture
def cms_qe_video_source_file_video_player_model(request):
    file_mock = Mock(spec=File, name='FileMock')
    file_mock._state = Mock()
    return SourceFileVideoPlayer(**get_data(request, 'cms_qe_video_source_file_video_player_model_data', {'source_file': file_mock}))


@pytest.fixture
def cms_qe_video_hosting_video_player_model(request):
    return HostingVideoPlayer(**get_data(request, 'cms_qe_video_hosting_video_player_model_data'))