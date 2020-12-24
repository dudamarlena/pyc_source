# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/tympeg/mediaobject.py
# Compiled at: 2018-10-07 17:16:25
# Size of source mod 2**32: 18229 bytes
from .timecode import timecode_to_seconds
from os import path, listdir
import subprocess, warnings, json
from argparse import Namespace

class MediaObject:
    __doc__ = ' An object that holds information relevant to manipulating and transcoding a file with ffmpeg. Uses ffprobe to\n     find information and stores it as nested dictionaries in MediaObject.streams[] and MediaObject.format{}.\n     Contains methods to help find keys and/or values in streams and streams with keys and/or values.\n\n    '

    def __init__(self, filePath):
        """ Initializes attributes that the MediaObject will contain.

        :param filePath: string, filepath of file to create object over.
        :return:
        """
        self.filePath = filePath
        self.directory, self.fileName = path.split(self.filePath)
        self.ffprobeOut = ''
        self.fileIsValid = True
        self.streams = []
        self.videoStreams = []
        self.audioStreams = []
        self.subtitleStreams = []
        self.attachmentStreams = []
        self.unrecognizedStreams = []
        self.resolutions = []
        self.width = 0
        self.height = 0
        self.file_size = path.getsize(self.filePath)
        self.format = {}
        self.framerates_dec = []
        self.framerates_frac = []
        self.framerate_dec = []
        self.framerate_frac = []
        self.duration = -1.0
        self.codecs = []
        self.streamTypes = []
        self.videoCodec = ''
        self.bitrates = []
        self.video_bitrate = 0
        self.audio_bitrate = 0
        self.bitrate = 0
        self.size = 0
        self.languages = {}

    def run(self, verbose=True):
        """ Calls ffprobe and extracts media information from it's output. Then calls methods to parse the information
         into self.streams[] and self.format{}. Stores ffprobe output as self.ffprobeOut.

        :return:
        """
        if not path.isfile(self.filePath):
            warnings.warn('File specified at ' + str(self.filePath) + " does not exist or can't be found!")
            return
        argsArray = ['ffprobe', '-v', 'quiet', '-print_format', 'json', '-show_format', '-show_streams', '-i', self.filePath]
        try:
            if verbose:
                print('Creating MediaObject of: ' + str(self.filePath))
            self.ffprobeOut = subprocess.check_output(argsArray).decode('utf-8')
        except subprocess.CalledProcessError as cpe:
            try:
                warnings.warn('\nCalledProcessError with ' + self.filePath + ' in MediaObject.run().\n\tFile is likely malformed or invalid.')
                print('CalledProcessError: ' + str(cpe))
                print()
                self.fileIsValid = False
            finally:
                cpe = None
                del cpe

        if self.fileIsValid:
            self.parseStreams()
            self.parseMetaInfo()

    def parseMetaInfo(self):
        """ Parses ffprobe json output and builds the self.format{} dictionary. Also sets some useful attributes like
        filesize, bitrate, codecs, etc...

        :return:
        """

        def try_to_get_float(key, default=-1.0):
            try:
                value = float(self.format[key])
            except KeyError:
                value = default

            return value

        def try_to_get_int(key, default=-1):
            try:
                value = int(self.format[key])
            except KeyError:
                value = default

            return value

        ffProbeInfo = json.loads((self.ffprobeOut), object_hook=(lambda d: Namespace(**d)))
        self.namespaceToDict(ffProbeInfo.format, '', -1, self.format)
        self.bitrate = try_to_get_int('bit_rate')
        self.duration = try_to_get_float('duration')
        self.size = try_to_get_int('size')
        for stream in self.streams:
            try:
                self.codecs.append(stream['codec_name'])
            except KeyError:
                print('codec_name not found in stream ' + str(stream['index']))
                print('     codecs[' + str(stream['index']) + "] set to 'unknown'.")
                self.streamTypes.append('unknown')

            try:
                self.streamTypes.append(stream['codec_type'])
            except KeyError:
                print('codec_type not found in stream ' + str(stream['index']))
                print('     streamTypes[' + str(stream['index']) + "] set to 'unknown'.")
                self.streamTypes.append('unknown')

            try:
                bps = self.getValueFromKey('bit_rate', stream)
                if bps is not None:
                    self.bitrates.append(int(bps))
                else:
                    try:
                        bps = self.getValueFromKey('BPS', stream)
                        if bps is not None:
                            self.bitrates.append(int(bps))
                    finally:
                        if bps is None:
                            self.bitrates.append(0)

            except KeyError:
                print('Bitrate not found in stream ' + str(stream['index']))

        vidcodecs = self.videoCodecs()
        if len(vidcodecs) > 1:
            self.videoCodec = [
             0]
        else:
            try:
                self.videoCodec = vidcodecs[0]
            except IndexError as ie:
                try:
                    print(ie)
                    print('Could not find videoCodec info')
                finally:
                    ie = None
                    del ie

    def parseStreams(self):
        """ Turns the ffprobe json stream output into nested dictionaries stored as a list at self.streams[{}]. Sorts
         streams into seperate lists based on type (audio, video, etc...). Lists of types integers that correspond to
         the index of self.streams[].

        :return:
        """
        ffProbeInfo = json.loads((self.ffprobeOut), object_hook=(lambda d: Namespace(**d)))
        try:
            self.duration = float(json.loads(self.ffprobeOut)['format']['duration'])
        except KeyError:
            try:
                print('Extracting duration from video stream...')
                print('\t' + self.filePath)
                self.duration = timecode_to_seconds(json.loads(self.ffprobeOut)['streams'][0]['tags']['DURATION'])
                print('Extracted duration is {}\n'.format(self.duration))
            except KeyError:
                print("\tDuration couldn't be found in file meta-info or video stream! Defaulting to a duration of -1.0!")

        i = 0
        for stream in ffProbeInfo.streams:
            streamDict = {}
            self.streams.append(streamDict)
            self.namespaceToDict(stream, '', -1, self.streams[i])
            i += 1

        for stream in self.streams:
            if stream['codec_type'] == 'video':
                self.videoStreams.append(stream['index'])
                try:
                    self.video_bitrate += int(self.getValueFromKey('bit_rate', stream))
                except TypeError as te:
                    try:
                        pass
                    finally:
                        te = None
                        del te

                framerate = self.getValueFromKey('r_frame_rate', stream)
                num, denom = framerate.split('/')
                self.framerates_dec.append(float(num) / float(denom))
                self.framerates_frac.append(framerate)
                coded_height = int(self.getValueFromKey('coded_height', stream))
                coded_width = int(self.getValueFromKey('coded_width', stream))
                height = int(self.getValueFromKey('height', stream))
                width = int(self.getValueFromKey('width', stream))
                y_dim = max(coded_height, height)
                if y_dim == coded_height:
                    x_dim = coded_width
                else:
                    x_dim = width
                self.resolutions.append((x_dim, y_dim))
            elif stream['codec_type'] == 'audio':
                self.audioStreams.append(stream['index'])
                try:
                    self.audio_bitrate += int(self.getValueFromKey('bit_rate', stream))
                except TypeError as te:
                    try:
                        pass
                    finally:
                        te = None
                        del te

            elif stream['codec_type'] == 'subtitle':
                self.subtitleStreams.append(stream['index'])
            elif stream['codec_type'] == 'attachment':
                self.attachmentStreams.append(stream['index'])
            else:
                self.unrecognizedStreams.append(stream['index'])

        if self.video_bitrate == 0 and self.audio_bitrate == 0:
            self.audio_bitrate = 128000
            self.video_bitrate = (8 * self.file_size - self.audio_bitrate * self.duration) / self.duration
        else:
            if self.video_bitrate == 0:
                self.video_bitrate = (8 * self.file_size - self.audio_bitrate * self.duration) / self.duration
            else:
                if self.audio_bitrate == 0:
                    self.audio_bitrate = (8 * self.file_size - self.video_bitrate * self.duration) / self.duration
                if len(self.videoStreams) != 0:
                    widths = []
                    for ndx in range(len(self.resolutions)):
                        widths.append(self.resolutions[ndx][0])

                    self.width = max(widths)
                    primary_vid_stream = widths.index(self.width)
                    self.height = self.resolutions[primary_vid_stream][1]
                    self.framerate_dec = self.framerates_dec[primary_vid_stream]
                    self.framerate_frac = self.framerates_frac[primary_vid_stream]
                return self.streams

    def streamInfo(self, streamIndex):
        return self.streams[streamIndex]

    def streamCodec(self, streamIndex):
        """ Gets the codec of the stream specified by the streamIndex parameter

        :param streamIndex: int, corresponds to the self.streams[] array.
        :return: string, name of codec used to encode stream
        """
        codec = self.streams[streamIndex]['codec_name']
        return codec

    def videoCodecs(self):
        """ Gets the codecs of all video streams.

        :return: array[str], an array of the names of codecs used to encode video streams.
        """
        streamArray = []
        i = 0
        for i in range(0, len(self.streamTypes)):
            if self.streamTypes[i] == 'video':
                streamArray.append(self.codecs[i])

        return streamArray

    def getStreamsWithValue(self, value, streamList=''):
        """ Finds streams with values in them and returns their self.streams[] indices in an array.

        :param value: string or number, the value that you want to find in the stream dictionaries.
        :return: array[int], an array of integers whose values correspond to the self.streams[] array that the value
        was found in.
        """

        def isValueInStream(nestedDict, value, prepath=()):
            for keys, values in nestedDict.items():
                path = prepath + (keys,)
                if values == value:
                    return True
                    if hasattr(values, 'items'):
                        p = isValueInStream(values, value, path)
                        if p is not None:
                            return p

        streams = []
        if streamList == '':
            streams = self.streams
        else:
            for stream in streamList:
                streams.append(self.streams[int(stream)])

        streamArray = []
        for stream in streams:
            if isValueInStream(stream, value):
                streamArray.append(stream['index'])

        return streamArray

    def getStreamsWithKeys(self, key, streamList=''):
        """ Finds streams with the specified key in them and returns their self.streams[] indices in an array.

        :param key: string, the value that you want to find in the stream dictionaries.
        :return: array[int], an array of integers whose values correspond to the self.streams[] array that the key
        was found in.
        """

        def isKeyInStream(nestedDict, key, prepath=()):
            for keys, values in nestedDict.items():
                path = prepath + (keys,)
                if keys == key:
                    return True
                    if hasattr(values, 'items'):
                        p = isKeyInStream(values, key, path)
                        if p is not None:
                            return p

        streamArray = []
        streams = []
        if streamList == '':
            streams = self.streams
        else:
            for stream in streamList:
                streams.append(self.streams[int(stream)])

        for stream in streams:
            if isKeyInStream(stream, key):
                streamArray.append(stream['index'])

        return streamArray

    def getValueFromKey(self, key, stream):
        """ Gets the value associated with a key from a stream or format dictionary.

        :param streamDict: dict, dictionary of stream from self.streams[]
        :param key: key of the value to be found
        :return: string, value associated with key. If key was not found value is None
        """
        streamDict = {}
        if isinstance(stream, int):
            streamDict = self.streams[stream]
        else:
            if isinstance(stream, dict):
                streamDict = stream
            else:
                print('getValueFromKey(): stream parameter not understood. Should be a stream dictionary or a list index of a stream.')
        if key in streamDict:
            return streamDict[key]
        for k, v in streamDict.items():
            if isinstance(v, dict):
                item = self.getValueFromKey(key, v)
                if item is not None:
                    return item

    def namespaceToDict(self, data, key, level, streamDict):
        """ Transforms namespace extracted from ffprobe json into a nested dictionary strucutre for polling later.

        :param data: Namespace or dictionary
        :param key: string, can be empty (should be for top levels)
        :param level: int, keeps track of level of nested dictionary during traversal
        :param streamDict: the dictionary that is being created as namespaces are converted
        :return:
        """
        level += 1
        if level > 0:
            data = vars(data)
            streamDict.update({key: data})
            for key, value in data.items():
                if isinstance(value, Namespace):
                    self.namespaceToDict(value, key, level, streamDict)

        else:
            data = vars(data)
            streamDict.update(data)
            for key, value in data.items():
                if isinstance(value, Namespace):
                    self.namespaceToDict(value, key, level, streamDict)


def makeMediaObjectsInDirectory(directory, selector=None):

    def conditionDirectoryString(directoryString):
        if type(directoryString) is not str:
            print("That's not a string that points to a directory, is type " + str(type(directoryString)))
            return
        if directoryString.endswith('/'):
            return directoryString
        return directoryString + '/'

    directory = conditionDirectoryString(directory)
    mediaObjectArray = []
    fileExtensions = ['.mp4', '.mkv', '.avi', '.m4v', '.wmv', '.webm', '.flv', '.mov', '.mpg', '.mpeg', '.ogg', '.ogv',
     '.ts', '.vob', '.VOB', '.mov', '.MOV', '.rmvb']
    for fileNames in listdir(directory):
        if any((extensions in fileNames for extensions in fileExtensions)):
            mediaInfo = MediaObject(directory + fileNames)
            mediaInfo.run()
            mediaObjectArray.append(mediaInfo)

    return mediaObjectArray