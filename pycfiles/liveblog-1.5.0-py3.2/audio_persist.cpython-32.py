# uncompyle6 version 3.7.4
# Python bytecode 3.2 (3180)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/superdesk/media_archive/impl/audio_persist.py
# Compiled at: 2013-10-02 09:54:57
"""
Created on Aug 23, 2012

@package: superdesk media archive
@copyright: 2012 Sourcefabric o.p.s.
@license: http://www.gnu.org/licenses/gpl-3.0.txt
@author: Ioan v. Pocol

Implementation for the audio persistence API.
"""
from ally.container import wire, app
from ally.container.ioc import injected
from ally.container.support import setup
from ally.support.sqlalchemy.session import SessionSupport
from ally.support.sqlalchemy.util_service import handle
from ally.support.util_sys import pythonPath
from os import remove
from os.path import splitext, abspath, join, exists
from sqlalchemy.exc import SQLAlchemyError
from subprocess import Popen, PIPE, STDOUT
from superdesk.media_archive.core.impl.meta_service_base import thumbnailFormatFor, metaTypeFor
from superdesk.media_archive.core.spec import IMetaDataHandler, IThumbnailManager
import re
from superdesk.media_archive.meta.meta_data import MetaDataMapped
from superdesk.media_archive.meta.audio_data import AudioDataEntry, META_TYPE_KEY
from superdesk.media_archive.meta.audio_info import AudioInfoMapped

@injected
@setup(IMetaDataHandler, name='audioDataHandler')
class AudioPersistanceAlchemy(SessionSupport, IMetaDataHandler):
    """
    Provides the service that handles the audio persistence @see: IAudioPersistanceService.
    """
    format_file_name = '%(id)s.%(file)s'
    wire.config('format_file_name', doc='\n    The format for the audios file names in the media archive')
    default_format_thumbnail = '%(size)s/audio.jpg'
    wire.config('default_format_thumbnail', doc='\n    The format for the audio thumbnails in the media archive')
    format_thumbnail = '%(size)s/%(id)s.%(name)s.jpg'
    wire.config('format_thumbnail', doc='\n    The format for the audio thumbnails in the media archive')
    ffmpeg_path = join('workspace', 'tools', 'ffmpeg', 'bin', 'ffmpeg.exe')
    wire.config('ffmpeg_path', doc='\n    The path where the ffmpeg is found')
    ffmpeg_tmp_path = join('workspace', 'tools', 'ffmpeg', 'tmp')
    wire.config('ffmpeg_tmp_path', doc='\n    The path where ffmpeg writes temp data')
    audio_supported_files = '3gp, act, AIFF, ALAC, Au, flac, gsm, m4a, m4p, mp3, ogg, ram, raw, vox, wav, wma'
    thumbnailManager = IThumbnailManager
    wire.entity('thumbnailManager')

    def __init__(self):
        assert isinstance(self.format_file_name, str), 'Invalid format file name %s' % self.format_file_name
        assert isinstance(self.default_format_thumbnail, str), 'Invalid format thumbnail %s' % self.default_format_thumbnail
        assert isinstance(self.format_thumbnail, str), 'Invalid format thumbnail %s' % self.format_thumbnail
        assert isinstance(self.audio_supported_files, str), 'Invalid supported files %s' % self.audio_supported_files
        assert isinstance(self.ffmpeg_path, str), 'Invalid ffmpeg path %s' % self.ffmpeg_path
        assert isinstance(self.ffmpeg_tmp_path, str), 'Invalid ffmpeg tmp path %s' % self.ffmpeg_tmp_path
        self.audioSupportedFiles = set(re.split('[\\s]*\\,[\\s]*', self.audio_supported_files))
        self._defaultThumbnailFormatId = self._thumbnailFormatId = self._metaTypeId = None
        return

    def addMetaInfo(self, metaDataMapped, languageId):
        audioInfoMapped = AudioInfoMapped()
        audioInfoMapped.MetaData = metaDataMapped.Id
        audioInfoMapped.Language = languageId
        try:
            self.session().add(audioInfoMapped)
            self.session().flush((audioInfoMapped,))
        except SQLAlchemyError as e:
            handle(e, audioInfoMapped)

        return audioInfoMapped

    def processByInfo(self, metaDataMapped, contentPath, contentType):
        """
        @see: IMetaDataHandler.processByInfo
        """
        if contentType is not None and contentType.startswith(META_TYPE_KEY):
            return self.process(metaDataMapped, contentPath)
        else:
            extension = splitext(metaDataMapped.Name)[1][1:]
            if extension in self.audioSupportedFiles:
                return self.process(metaDataMapped, contentPath)
            return False

    def process(self, metaDataMapped, contentPath):
        """
        @see: IMetaDataHandler.process
        """
        assert isinstance(metaDataMapped, MetaDataMapped), 'Invalid meta data mapped %s' % metaDataMapped
        tmpFile = self.ffmpeg_tmp_path + str(metaDataMapped.Id)
        if exists(tmpFile):
            remove(tmpFile)
        p = Popen((self.ffmpeg_path, '-i', contentPath, '-f', 'ffmetadata', tmpFile), stdin=PIPE, stdout=PIPE, stderr=STDOUT)
        result = p.wait()
        if exists(tmpFile):
            remove(tmpFile)
        if result != 0:
            return False
        else:
            audioDataEntry = AudioDataEntry()
            audioDataEntry.Id = metaDataMapped.Id
            metadata = False
            while 1:
                line = p.stdout.readline()
                if not line:
                    break
                line = str(line, 'utf-8')
                if line.find('misdetection possible!') != -1:
                    return False
                if metadata:
                    property = self.extractProperty(line)
                    if property == None:
                        metadata = False
                    else:
                        if property == 'title':
                            audioDataEntry.Title = self.extractString(line)
                        else:
                            if property == 'artist':
                                audioDataEntry.Artist = self.extractString(line)
                            else:
                                if property == 'track':
                                    audioDataEntry.Track = self.extractNumber(line)
                                else:
                                    if property == 'album':
                                        audioDataEntry.Album = self.extractString(line)
                                    else:
                                        if property == 'genre':
                                            audioDataEntry.Genre = self.extractString(line)
                                        else:
                                            if property == 'TCMP':
                                                audioDataEntry.Tcmp = self.extractNumber(line)
                                            else:
                                                if property == 'album_artist':
                                                    audioDataEntry.AlbumArtist = self.extractString(line)
                                                else:
                                                    if property == 'date':
                                                        audioDataEntry.Year = self.extractNumber(line)
                                                    else:
                                                        if property == 'disc':
                                                            audioDataEntry.Disk = self.extractNumber(line)
                                                        else:
                                                            if property == 'TBPM':
                                                                audioDataEntry.Tbpm = self.extractNumber(line)
                                                            else:
                                                                if property == 'composer':
                                                                    audioDataEntry.Composer = self.extractString(line)
                                                                elif property == 'Duration':
                                                                    metadata = False
                    if metadata:
                        continue
                elif line.find('Metadata') != -1:
                    metadata = True
                    continue
                if line.find('Stream') != -1 and line.find('Audio') != -1:
                    try:
                        values = self.extractAudio(line)
                        audioDataEntry.AudioEncoding = values[0]
                        audioDataEntry.SampleRate = values[1]
                        audioDataEntry.Channels = values[2]
                        audioDataEntry.AudioBitrate = values[3]
                    except:
                        pass

                elif line.find('Duration') != -1 and line.find('start') != -1:
                    try:
                        values = self.extractDuration(line)
                        audioDataEntry.Length = values[0]
                        audioDataEntry.AudioBitrate = values[1]
                    except:
                        pass

                elif line.find('Output #0') != -1:
                    break

            path = self.format_file_name % {'id': metaDataMapped.Id,  'file': metaDataMapped.Name}
            path = ''.join((META_TYPE_KEY, '/', self.generateIdPath(metaDataMapped.Id), '/', path))
            metaDataMapped.content = path
            metaDataMapped.Type = META_TYPE_KEY
            metaDataMapped.typeId = self.metaTypeId()
            metaDataMapped.thumbnailFormatId = self.defaultThumbnailFormatId()
            metaDataMapped.IsAvailable = True
            try:
                self.session().add(audioDataEntry)
                self.session().flush((audioDataEntry,))
            except SQLAlchemyError as e:
                metaDataMapped.IsAvailable = False
                handle(e, AudioDataEntry)

            return True

    @app.populate
    def populateThumbnail(self):
        """
        Populates the thumbnail for audio.
        """
        self.thumbnailManager.putThumbnail(self.defaultThumbnailFormatId(), abspath(join(pythonPath(), 'resources', 'audio.jpg')))

    def metaTypeId(self):
        """
        Provides the meta type id.
        """
        if self._metaTypeId is None:
            self._metaTypeId = metaTypeFor(self.session(), META_TYPE_KEY).Id
        return self._metaTypeId

    def defaultThumbnailFormatId(self):
        """
        Provides the thumbnail format id.
        """
        if not self._defaultThumbnailFormatId:
            self._defaultThumbnailFormatId = thumbnailFormatFor(self.session(), self.default_format_thumbnail).id
        return self._defaultThumbnailFormatId

    def thumbnailFormatId(self):
        """
        Provides the thumbnail format id.
        """
        if not self._thumbnailFormatId:
            self._thumbnailFormatId = thumbnailFormatFor(self.session(), self.format_thumbnail).id
        return self._thumbnailFormatId

    def extractDuration(self, line):
        properties = line.split(',')
        length = properties[0].partition(':')[2]
        length = length.strip().split(':')
        length = int(length[0]) * 60 + int(length[1]) * 60 + int(float(length[2]))
        bitrate = properties[2]
        bitrate = bitrate.partition(':')[2]
        bitrate = bitrate.strip().partition(' ')
        if bitrate[2] == 'kb/s':
            bitrate = int(float(bitrate[0]))
        else:
            bitrate = None
        return (length, bitrate)

    def extractAudio(self, line):
        properties = line.rpartition(':')[2].split(',')
        index = 0
        encoding = properties[index].strip()
        index += 1
        sampleRate = properties[index].strip().partition(' ')
        if sampleRate[2] == 'Hz':
            sampleRate = int(float(sampleRate[0]))
        else:
            sampleRate = None
        index += 1
        channels = properties[index].strip()
        index += 2
        bitrate = properties[4].strip().partition(' ')
        if bitrate[2] == 'kb/s':
            bitrate = int(float(bitrate[0]))
        else:
            bitrate = None
        return (encoding, sampleRate, channels, bitrate)

    def extractProperty(self, line):
        return line.partition(':')[0].strip()

    def extractNumber(self, line):
        return int(float(line.partition(':')[2].strip()))

    def extractString(self, line):
        return line.partition(':')[2].strip()

    def generateIdPath(self, id):
        return '{0:03d}'.format(id // 1000 % 1000)