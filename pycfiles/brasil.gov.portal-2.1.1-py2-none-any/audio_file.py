# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/hvelarde/forcontent/idg/src/brasil.gov.portal/src/brasil/gov/portal/content/audio_file.py
# Compiled at: 2018-10-18 17:35:13
from brasil.gov.portal import _
from plone.dexterity.content import Item
from plone.indexer.decorator import indexer
from plone.namedfile.field import NamedBlobFile
from plone.rfc822.interfaces import IPrimaryFieldInfo
from plone.supermodel import model
from zope.interface import implementer
from zope.interface import Invalid
OGGTYPES = [
 'audio/ogg',
 'audio/x-ogg']
MPEGTYPES = [
 'audio/mp3',
 'audio/mpeg',
 'audio/x-mp3',
 'audio/x-mpeg']

def validate_mimetype(value, audiotypes):
    if value.contentType not in audiotypes:
        raise Invalid(_('File format not supported'))
    return True


def validate_mpeg(value):
    return validate_mimetype(value, MPEGTYPES)


def validate_ogg(value):
    return validate_mimetype(value, OGGTYPES)


class IMPEGAudioFile(model.Schema):
    """ Representa um Arquivo de Audio MPEG"""
    model.primary('file')
    file = NamedBlobFile(title=_('File'), description=_('Please upload a audio file.'), required=True, constraint=validate_mpeg)


class IOGGAudioFile(model.Schema):
    """ Representa um Arquivo de Audio OGG"""
    model.primary('file')
    file = NamedBlobFile(title=_('File'), description=_('Please upload a audio file.'), required=True, constraint=validate_ogg)


class AudioFile(Item):

    @property
    def content_type(self):
        """ Retorna o mimetype do conteudo """
        file = self.file
        if file:
            return file.contentType


@implementer(IMPEGAudioFile)
class MPEGAudioFile(AudioFile):
    """MPEG audio file."""
    pass


@implementer(IOGGAudioFile)
class OGGAudioFile(AudioFile):
    """OGG audio file."""
    pass


@indexer(IMPEGAudioFile)
@indexer(IOGGAudioFile)
def getObjSize_file(obj):
    primary_field_info = IPrimaryFieldInfo(obj)
    return obj.getObjSize(None, primary_field_info.value.size)