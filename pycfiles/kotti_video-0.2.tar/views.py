# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/disko/.virtualenvs/ffl_website/src/kotti_video/kotti_video/views.py
# Compiled at: 2012-05-09 04:47:10
import logging
from kotti.util import _
from kotti.views.edit import DocumentSchema, make_generic_add, make_generic_edit
from kotti.views.file import AddFileFormView, EditFileFormView
from kotti_video.resources import Video, Mp4File, WebmFile, OggFile, SubtitlesFile, ChaptersFile
from pyramid.response import Response
from pyramid.url import resource_url
from pyramid.view import view_config
log = logging.getLogger(__name__)

class BaseView(object):

    def __init__(self, context, request):
        self.context = context
        self.request = request


class VideoView(BaseView):

    @view_config(context=Video, name='view', permission='view', renderer='templates/video-view.pt')
    def view(self):
        result = {}
        for t in ('mp4', 'webm', 'ogg', 'subtitles', 'chapters', 'poster'):
            key = '%s_url' % t
            file = getattr(self.context, '%s_file' % t)
            if file is None:
                result[key] = None
            else:
                result[key] = resource_url(file, self.request, '@@attachment-view')

        return result


class AddMp4FileFormView(AddFileFormView):
    item_type = _('Mp4File')
    item_class = Mp4File


class AddWebmFileFormView(AddFileFormView):
    item_type = _('WebmFile')
    item_class = WebmFile


class AddOggFileFormView(AddFileFormView):
    item_type = _('OggFile')
    item_class = OggFile


class AddSubtitlesFileFormView(AddFileFormView):
    item_type = _('SubtitlesFile')
    item_class = SubtitlesFile


class AddChaptersFileFormView(AddFileFormView):
    item_type = _('ChaptersFile')
    item_class = ChaptersFile


def includeme(config):
    config.add_static_view('static-kotti_video', 'kotti_video:static')
    config.scan('kotti_video')
    config.add_view(make_generic_add(DocumentSchema(), Video), name=Video.type_info.add_view, permission='add', renderer='kotti:templates/edit/node.pt')
    config.add_view(make_generic_edit(DocumentSchema()), context=Video, name='edit', permission='edit', renderer='kotti:templates/edit/node.pt')
    for file_type in (Mp4File, WebmFile, OggFile, SubtitlesFile, ChaptersFile):
        config.add_view(EditFileFormView, context=file_type, name='edit', permission='edit', renderer='kotti:templates/edit/node.pt')

    config.add_view(AddMp4FileFormView, name=Mp4File.type_info.add_view, permission='add', renderer='kotti:templates/edit/node.pt')
    config.add_view(AddWebmFileFormView, name=WebmFile.type_info.add_view, permission='add', renderer='kotti:templates/edit/node.pt')
    config.add_view(AddOggFileFormView, name=OggFile.type_info.add_view, permission='add', renderer='kotti:templates/edit/node.pt')
    config.add_view(AddSubtitlesFileFormView, name=SubtitlesFile.type_info.add_view, permission='add', renderer='kotti:templates/edit/node.pt')
    config.add_view(AddChaptersFileFormView, name=ChaptersFile.type_info.add_view, permission='add', renderer='kotti:templates/edit/node.pt')