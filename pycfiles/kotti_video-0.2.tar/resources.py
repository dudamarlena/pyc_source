# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/disko/.virtualenvs/ffl_website/src/kotti_video/kotti_video/resources.py
# Compiled at: 2012-06-20 07:13:51
from kotti import DBSession
from kotti.resources import Document
from kotti.resources import File
from kotti.resources import TypeInfo
from kotti.security import view_permitted
from kotti.util import _
from kotti.util import ViewLink
from kotti.resources import Image
from pprint import pformat
from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy import Integer

class VideoFileTypeInfo(TypeInfo):

    def addable(self, context, request):
        """Return True if
            - the type described in 'self' may be added  *and*
            - no other child of the same type has already be added
           to 'context'."""
        if view_permitted(context, request, self.add_view):
            addable = context.type_info.name in self.addable_to
            child_type_already_added = self in [ c.type_info for c in context.children ]
            return addable and not child_type_already_added
        else:
            return False

    def copy(self, **kwargs):
        d = self.__dict__.copy()
        d.update(kwargs)
        return VideoFileTypeInfo(**d)

    def __repr__(self):
        return pformat(self.__dict__)


generic_video_file_type_info = VideoFileTypeInfo(name='VideoFile', title=_('Video file'), addable_to=[
 'Video'], add_view=None, edit_links=[
 ViewLink('edit', title=_('Edit'))])

class Mp4File(File):
    id = Column(Integer(), ForeignKey('files.id'), primary_key=True)
    type_info = generic_video_file_type_info.copy(name='Mp4File', title=_('Video file (*.mp4)'), add_view='add_mp4file')

    def __init__(self, data=None, filename=None, mimetype=None, size=None, **kwargs):
        super(Mp4File, self).__init__(data=data, filename='video.mp4', mimetype='video/mp4', size=size, **kwargs)


class WebmFile(File):
    id = Column(Integer(), ForeignKey('files.id'), primary_key=True)
    type_info = generic_video_file_type_info.copy(name='WebmFile', title=_('Video file (*.webm)'), add_view='add_webmfile')

    def __init__(self, data=None, filename=None, mimetype=None, size=None, **kwargs):
        super(WebmFile, self).__init__(data=data, filename='video.webm', mimetype='video/webm', size=size, **kwargs)


class OggFile(File):
    id = Column(Integer(), ForeignKey('files.id'), primary_key=True)
    type_info = generic_video_file_type_info.copy(name='OggFile', title=_('Video file (*.ogg)'), add_view='add_oggfile')

    def __init__(self, data=None, filename=None, mimetype=None, size=None, **kwargs):
        super(OggFile, self).__init__(data=data, filename='video.ogv', mimetype='video/ogg', size=size, **kwargs)


class SubtitlesFile(File):
    id = Column(Integer(), ForeignKey('files.id'), primary_key=True)
    type_info = generic_video_file_type_info.copy(name='SubtitlesFile', title=_('Subtitles file (*.srt)'), add_view='add_subtitlesfile')


class ChaptersFile(File):
    id = Column(Integer(), ForeignKey('files.id'), primary_key=True)
    type_info = generic_video_file_type_info.copy(name='ChaptersFile', title=_('Chapters file (*.srt)'), add_view='add_chaptersfile')


class Video(Document):
    id = Column(Integer(), ForeignKey('documents.id'), primary_key=True)
    type_info = Document.type_info.copy(name='Video', title=_('Video'), addable_to=[
     'Document'], add_view='add_video')

    @property
    def mp4_file(self):
        session = DBSession()
        query = session.query(Mp4File).filter(Mp4File.parent_id == self.id)
        if query.count() > 0:
            return query.first()
        else:
            return

    @property
    def webm_file(self):
        session = DBSession()
        query = session.query(WebmFile).filter(WebmFile.parent_id == self.id)
        if query.count() > 0:
            return query.first()
        else:
            return

    @property
    def ogg_file(self):
        session = DBSession()
        query = session.query(OggFile).filter(OggFile.parent_id == self.id)
        if query.count() > 0:
            return query.first()
        else:
            return

    @property
    def subtitles_file(self):
        session = DBSession()
        query = session.query(SubtitlesFile).filter(SubtitlesFile.parent_id == self.id)
        if query.count() > 0:
            return query.first()
        else:
            return

    @property
    def chapters_file(self):
        session = DBSession()
        query = session.query(ChaptersFile).filter(ChaptersFile.parent_id == self.id)
        if query.count() > 0:
            return query.first()
        else:
            return

    @property
    def poster_file(self):
        session = DBSession()
        query = session.query(Image).filter(Image.parent_id == self.id)
        if query.count() > 0:
            return query.first()
        else:
            return