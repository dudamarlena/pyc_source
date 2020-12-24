# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/tympeg/converter.py
# Compiled at: 2018-03-13 18:11:21
# Size of source mod 2**32: 27570 bytes
from tympeg.util import renameFile
import subprocess, time, warnings
from os import path, mkdir
from .timecode import timecode_to_seconds, seconds_to_timecode, subtract_timecodes
from .util import renameFile

class MediaConverter:
    __doc__ = ' Holds settings that get turned into an arg array for ffmpeg conversion\n    '

    def __init__(self, mediaObject, outputFilePath='', debug=False, verbosity=24):
        """ Generates a ConversionSettings object. Populate fields with createXSettings() Methods.

        :param mediaObject:  MediaObject of file to be created
        :param outputFilePath: string, file path of output file
        :param debug: bool, whether or not to print certain messages helpful with debugging
        :param verbosity: int, level of ffmpeg verbosity. Integers correspond to ffmpeg's -loglevel options
        :return:
        """
        self.mediaObject = mediaObject
        self.debug = debug
        self.verbosity = verbosity
        if self.mediaObject.streams == []:
            self.mediaObject.run()
        else:
            try:
                self.inputFilePath = self.mediaObject.format['filename']
            except KeyError:
                self.inputFilePath = self.mediaObject.filePath
                print('Filename not found in format dictionary for file {}'.format(self.mediaObject.fileName))
                print()

            self.inputFileName = path.basename(self.inputFilePath)
            inDir, inFileName = path.split(self.mediaObject.filePath)
            outDir, outFileName = path.split(outputFilePath)
            if outputFilePath == '':
                outputFilePath = path.join(inDir, renameFile(self.mediaObject.filePath))
            else:
                outFileName = renameFile(path.join(outDir, outFileName))
            outputFilePath = path.join(outDir, outFileName)
        self.outputFilePath = outputFilePath
        self.inputFileName = path.basename(outputFilePath)
        self.videoStreams = []
        self.audioStreams = []
        self.subtitleStreams = []
        self.attachmentStreams = []
        self.otherStreams = []
        self.argsArray = [
         'ffmpeg']

    def convert(self):
        if self.argsArray == ['ffmpeg']:
            self.generateArgsArray()
        outputDirectory, outputFilename = path.split(self.outputFilePath)
        if not path.isdir(outputDirectory):
            mkdir(outputDirectory)
        startTime = time.time()
        subprocess.run(self.argsArray)
        endTime = time.time()
        return endTime - startTime

    def clip(self, startingTime, endingTime):
        self.generateArgsArray(startTime=startingTime, endTime=endingTime)
        print(self.argsArray)
        self.convert()

    def createVideoStream--- This code section failed: ---

 L. 104         0  LOAD_CODE                <code_object buildvpXStream>
                2  LOAD_STR                 'MediaConverter.createVideoStream.<locals>.buildvpXStream'
                4  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
                6  STORE_FAST               'buildvpXStream'

 L. 162         8  LOAD_CODE                <code_object buildx26XStream>
               10  LOAD_STR                 'MediaConverter.createVideoStream.<locals>.buildx26XStream'
               12  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
               14  STORE_FAST               'buildx26XStream'

 L. 218        16  LOAD_CLOSURE             'videoSettingsDict'
               18  BUILD_TUPLE_1         1 
               20  LOAD_CODE                <code_object buildCopyStream>
               22  LOAD_STR                 'MediaConverter.createVideoStream.<locals>.buildCopyStream'
               24  MAKE_FUNCTION_8          'closure'
               26  STORE_FAST               'buildCopyStream'

 L. 227        28  BUILD_MAP_0           0 
               30  STORE_DEREF              'videoSettingsDict'

 L. 231        32  LOAD_FAST                'videoStream'
               34  LOAD_CONST               -1
               36  COMPARE_OP               ==
               38  POP_JUMP_IF_FALSE    52  'to 52'

 L. 232        40  LOAD_FAST                'self'
               42  LOAD_ATTR                mediaObject
               44  LOAD_ATTR                videoStreams
               46  LOAD_CONST               0
               48  BINARY_SUBSCR    
               50  STORE_FAST               'videoStream'
             52_0  COME_FROM            38  '38'

 L. 235        52  LOAD_GLOBAL              isinstance
               54  LOAD_FAST                'videoStream'
               56  LOAD_GLOBAL              int
               58  CALL_FUNCTION_2       2  '2 positional arguments'
               60  POP_JUMP_IF_FALSE   144  'to 144'

 L. 236        62  LOAD_FAST                'self'
               64  LOAD_ATTR                mediaObject
               66  LOAD_ATTR                streams
               68  LOAD_FAST                'videoStream'
               70  BINARY_SUBSCR    
               72  LOAD_STR                 'codec_type'
               74  BINARY_SUBSCR    
               76  LOAD_STR                 'video'
               78  COMPARE_OP               ==
               80  POP_JUMP_IF_FALSE    98  'to 98'

 L. 237        82  LOAD_DEREF               'videoSettingsDict'
               84  LOAD_METHOD              update
               86  LOAD_STR                 'videoStream'
               88  LOAD_FAST                'videoStream'
               90  BUILD_MAP_1           1 
               92  CALL_METHOD_1         1  '1 positional argument'
               94  POP_TOP          
               96  JUMP_ABSOLUTE       178  'to 178'
             98_0  COME_FROM            80  '80'

 L. 239        98  LOAD_GLOBAL              warnings
              100  LOAD_METHOD              warn
              102  LOAD_STR                 'Stream '
              104  LOAD_GLOBAL              str
              106  LOAD_FAST                'videoStream'
              108  CALL_FUNCTION_1       1  '1 positional argument'
              110  BINARY_ADD       
              112  LOAD_STR                 ' is not a video stream. Defaulting to first video streamin MediaObject.'
              114  BINARY_ADD       
              116  CALL_METHOD_1         1  '1 positional argument'
              118  POP_TOP          

 L. 241       120  LOAD_DEREF               'videoSettingsDict'
              122  LOAD_METHOD              update
              124  LOAD_STR                 'videoStream'
              126  LOAD_FAST                'self'
              128  LOAD_ATTR                mediaObject
              130  LOAD_ATTR                videoStreams
              132  LOAD_CONST               0
              134  BINARY_SUBSCR    
              136  BUILD_MAP_1           1 
              138  CALL_METHOD_1         1  '1 positional argument'
              140  POP_TOP          
              142  JUMP_FORWARD        178  'to 178'
            144_0  COME_FROM            60  '60'

 L. 243       144  LOAD_FAST                'videoStream'
              146  LOAD_CONST               None
              148  COMPARE_OP               is
              150  POP_JUMP_IF_FALSE   164  'to 164'

 L. 244       152  LOAD_GLOBAL              warnings
              154  LOAD_METHOD              warn
              156  LOAD_STR                 'No video requested.'
              158  CALL_METHOD_1         1  '1 positional argument'
              160  POP_TOP          
              162  JUMP_FORWARD        178  'to 178'
            164_0  COME_FROM           150  '150'

 L. 247       164  LOAD_GLOBAL              warnings
              166  LOAD_METHOD              warn
              168  LOAD_STR                 "Video stream specified not understood, won't be included."
              170  CALL_METHOD_1         1  '1 positional argument'
              172  POP_TOP          

 L. 248       174  LOAD_CONST               None
              176  RETURN_VALUE     
            178_0  COME_FROM           162  '162'
            178_1  COME_FROM           142  '142'

 L. 250       178  LOAD_STR                 'x264'
              180  LOAD_STR                 'x265'
              182  LOAD_STR                 'vp8'
              184  LOAD_STR                 'vp9'
              186  LOAD_STR                 'copy'
              188  BUILD_LIST_5          5 
              190  STORE_FAST               'supportedEncoders'

 L. 252       192  LOAD_FAST                'videoEncoder'
              194  LOAD_FAST                'supportedEncoders'
              196  COMPARE_OP               in
              198  POP_JUMP_IF_FALSE   216  'to 216'

 L. 253       200  LOAD_DEREF               'videoSettingsDict'
              202  LOAD_METHOD              update
              204  LOAD_STR                 'videoEncoder'
              206  LOAD_FAST                'videoEncoder'
              208  BUILD_MAP_1           1 
              210  CALL_METHOD_1         1  '1 positional argument'
              212  POP_TOP          
              214  JUMP_FORWARD        236  'to 236'
            216_0  COME_FROM           198  '198'

 L. 255       216  LOAD_GLOBAL              ValueError
              218  LOAD_FAST                'videoEncoder'
              220  LOAD_STR                 ' is not supported. Currently supported encoders are: '
              222  BINARY_ADD       
              224  LOAD_GLOBAL              str
              226  LOAD_FAST                'supportedEncoders'
              228  CALL_FUNCTION_1       1  '1 positional argument'
              230  BINARY_ADD       
              232  CALL_FUNCTION_1       1  '1 positional argument'
              234  POP_TOP          
            236_0  COME_FROM           214  '214'

 L. 257       236  LOAD_FAST                'videoEncoder'
              238  LOAD_STR                 'x264'
              240  COMPARE_OP               ==
              242  POP_JUMP_IF_TRUE    254  'to 254'
              244  LOAD_FAST                'videoEncoder'
              246  LOAD_STR                 'x265'
              248  COMPARE_OP               ==
          250_252  POP_JUMP_IF_FALSE   270  'to 270'
            254_0  COME_FROM           242  '242'

 L. 258       254  LOAD_FAST                'buildx26XStream'
              256  LOAD_DEREF               'videoSettingsDict'
              258  LOAD_FAST                'rateControlMethod'
              260  LOAD_FAST                'rateParam'
              262  LOAD_FAST                'speed'
              264  CALL_FUNCTION_4       4  '4 positional arguments'
              266  POP_TOP          
              268  JUMP_FORWARD        348  'to 348'
            270_0  COME_FROM           250  '250'

 L. 259       270  LOAD_FAST                'videoEncoder'
              272  LOAD_STR                 'vp8'
              274  COMPARE_OP               ==
          276_278  POP_JUMP_IF_TRUE    290  'to 290'
              280  LOAD_FAST                'videoEncoder'
              282  LOAD_STR                 'vp9'
              284  COMPARE_OP               ==
          286_288  POP_JUMP_IF_FALSE   304  'to 304'
            290_0  COME_FROM           276  '276'

 L. 260       290  LOAD_FAST                'buildvpXStream'
              292  LOAD_DEREF               'videoSettingsDict'
              294  LOAD_FAST                'rateControlMethod'
              296  LOAD_FAST                'rateParam'
              298  CALL_FUNCTION_3       3  '3 positional arguments'
              300  POP_TOP          
              302  JUMP_FORWARD        348  'to 348'
            304_0  COME_FROM           286  '286'

 L. 261       304  LOAD_FAST                'videoEncoder'
              306  LOAD_STR                 'copy'
              308  COMPARE_OP               ==
          310_312  POP_JUMP_IF_FALSE   324  'to 324'

 L. 262       314  LOAD_FAST                'buildCopyStream'
              316  LOAD_DEREF               'videoSettingsDict'
              318  CALL_FUNCTION_1       1  '1 positional argument'
              320  POP_TOP          
              322  JUMP_FORWARD        348  'to 348'
            324_0  COME_FROM           310  '310'

 L. 264       324  LOAD_GLOBAL              print
              326  LOAD_STR                 'Video encoder parameter not understood in MediaConverter.createVideoStream().'
              328  CALL_FUNCTION_1       1  '1 positional argument'
              330  POP_TOP          

 L. 265       332  LOAD_GLOBAL              print
              334  LOAD_STR                 'Supported encoder parameters are: '
              336  LOAD_GLOBAL              str
              338  LOAD_FAST                'supportedEncoders'
              340  CALL_FUNCTION_1       1  '1 positional argument'
              342  BINARY_ADD       
              344  CALL_FUNCTION_1       1  '1 positional argument'
              346  POP_TOP          
            348_0  COME_FROM           322  '322'
            348_1  COME_FROM           302  '302'
            348_2  COME_FROM           268  '268'

 L. 268       348  LOAD_FAST                'videoEncoder'
              350  LOAD_STR                 'copy'
              352  COMPARE_OP               ==
          354_356  POP_JUMP_IF_FALSE   388  'to 388'

 L. 269       358  LOAD_DEREF               'videoSettingsDict'
              360  LOAD_METHOD              update
              362  LOAD_STR                 'width'
              364  LOAD_CONST               -1
              366  BUILD_MAP_1           1 
              368  CALL_METHOD_1         1  '1 positional argument'
              370  POP_TOP          

 L. 270       372  LOAD_DEREF               'videoSettingsDict'
              374  LOAD_METHOD              update
              376  LOAD_STR                 'height'
              378  LOAD_CONST               -1
              380  BUILD_MAP_1           1 
              382  CALL_METHOD_1         1  '1 positional argument'
              384  POP_TOP          
              386  JUMP_FORWARD        558  'to 558'
            388_0  COME_FROM           354  '354'

 L. 272       388  LOAD_DEREF               'videoSettingsDict'
              390  LOAD_METHOD              update
              392  LOAD_STR                 'width'
              394  LOAD_GLOBAL              int
              396  LOAD_FAST                'width'
              398  CALL_FUNCTION_1       1  '1 positional argument'
              400  BUILD_MAP_1           1 
              402  CALL_METHOD_1         1  '1 positional argument'
              404  POP_TOP          

 L. 273       406  LOAD_DEREF               'videoSettingsDict'
              408  LOAD_METHOD              update
              410  LOAD_STR                 'height'
              412  LOAD_GLOBAL              int
              414  LOAD_FAST                'height'
              416  CALL_FUNCTION_1       1  '1 positional argument'
              418  BUILD_MAP_1           1 
              420  CALL_METHOD_1         1  '1 positional argument'
              422  POP_TOP          

 L. 275       424  LOAD_FAST                'self'
              426  LOAD_ATTR                debug
          428_430  POP_JUMP_IF_FALSE   558  'to 558'

 L. 276       432  LOAD_FAST                'height'
              434  LOAD_CONST               -1
              436  COMPARE_OP               ==
          438_440  POP_JUMP_IF_TRUE    472  'to 472'
              442  LOAD_FAST                'width'
              444  LOAD_CONST               -1
              446  COMPARE_OP               !=
          448_450  POP_JUMP_IF_TRUE    472  'to 472'
              452  LOAD_FAST                'height'
              454  LOAD_CONST               -1
              456  COMPARE_OP               !=
          458_460  POP_JUMP_IF_TRUE    472  'to 472'
              462  LOAD_FAST                'width'
              464  LOAD_CONST               -1
              466  COMPARE_OP               ==
          468_470  POP_JUMP_IF_FALSE   526  'to 526'
            472_0  COME_FROM           458  '458'
            472_1  COME_FROM           448  '448'
            472_2  COME_FROM           438  '438'

 L. 277       472  LOAD_FAST                'height'
              474  LOAD_CONST               -1
              476  COMPARE_OP               ==
          478_480  POP_JUMP_IF_FALSE   504  'to 504'

 L. 278       482  LOAD_GLOBAL              print
              484  LOAD_STR                 'Scaling to width of '
              486  LOAD_GLOBAL              str
              488  LOAD_FAST                'width'
              490  CALL_FUNCTION_1       1  '1 positional argument'
              492  BINARY_ADD       
              494  LOAD_STR                 ' pixels.'
              496  BINARY_ADD       
              498  CALL_FUNCTION_1       1  '1 positional argument'
              500  POP_TOP          
              502  JUMP_FORWARD        524  'to 524'
            504_0  COME_FROM           478  '478'

 L. 280       504  LOAD_GLOBAL              print
              506  LOAD_STR                 'Scaling to height of '
              508  LOAD_GLOBAL              str
              510  LOAD_FAST                'height'
              512  CALL_FUNCTION_1       1  '1 positional argument'
              514  BINARY_ADD       
              516  LOAD_STR                 ' pixels.'
              518  BINARY_ADD       
              520  CALL_FUNCTION_1       1  '1 positional argument'
              522  POP_TOP          
            524_0  COME_FROM           502  '502'
              524  JUMP_FORWARD        558  'to 558'
            526_0  COME_FROM           468  '468'

 L. 282       526  LOAD_GLOBAL              print
              528  LOAD_STR                 'Scaling to width of '
              530  LOAD_GLOBAL              str
              532  LOAD_FAST                'width'
              534  CALL_FUNCTION_1       1  '1 positional argument'
              536  BINARY_ADD       
              538  LOAD_STR                 ' and height of '
              540  BINARY_ADD       
              542  LOAD_GLOBAL              str
              544  LOAD_FAST                'height'
              546  CALL_FUNCTION_1       1  '1 positional argument'
              548  BINARY_ADD       
              550  LOAD_STR                 ' pixels.'
              552  BINARY_ADD       
              554  CALL_FUNCTION_1       1  '1 positional argument'
              556  POP_TOP          
            558_0  COME_FROM           524  '524'
            558_1  COME_FROM           428  '428'
            558_2  COME_FROM           386  '386'

 L. 284       558  LOAD_DEREF               'videoSettingsDict'
              560  LOAD_METHOD              update
              562  LOAD_STR                 'index'
              564  LOAD_GLOBAL              int
              566  LOAD_FAST                'videoStream'
              568  CALL_FUNCTION_1       1  '1 positional argument'
              570  BUILD_MAP_1           1 
              572  CALL_METHOD_1         1  '1 positional argument'
              574  POP_TOP          

 L. 285       576  LOAD_FAST                'self'
              578  LOAD_ATTR                videoStreams
              580  LOAD_METHOD              append
              582  LOAD_DEREF               'videoSettingsDict'
              584  CALL_METHOD_1         1  '1 positional argument'
              586  POP_TOP          

 L. 287       588  LOAD_FAST                'self'
              590  LOAD_ATTR                debug
          592_594  POP_JUMP_IF_FALSE   604  'to 604'

 L. 288       596  LOAD_FAST                'self'
              598  LOAD_METHOD              printVideoSettings
              600  CALL_METHOD_0         0  '0 positional arguments'
              602  POP_TOP          
            604_0  COME_FROM           592  '592'

Parse error at or near `JUMP_FORWARD' instruction at offset 524

    def printVideoSettings(self):
        """ Prints the video settings of the ConversionSettings object.

        :return:
        """
        print('---- VIDEO SETTINGS -----')
        for stream in self.videoStreams:
            print('Stream:  ' + str(stream['videoStream']))
            print('self.width: ' + str(stream['width']))
            print('self.height: ' + str(stream['height']))
            print('self.videoEncoder: ' + str(stream['videoEncoder']))
            if str(stream['videoEncoder']) != 'copy':
                print('self.speed: ' + str(stream['speed']))
                print('self.bitrateMode: ' + str(stream['bitrateMode']))
            print()

    def createAudioStream(self, audioStream=None, audioEncoder='', audioBitrate=128, audioChannels='stereo'):
        """ Populates the ConversionSettings object with information on how to transcode video.

        :param audioStreams: array[int], values correspond to index of MediaObject.streams[]. Specify None for no audio stream.
        :param audioCodec: string, audio codec to be used to encode audio
        :param audioBitrate: desired audio bitrate in kbit/s
        :param audioChannels: string, 'mono' or 'stereo'
        :return:
        """
        audioSettingsDict = {'audioStream':'', 
         'audioEncoder':'aac',  'audioBitrate':128,  'audioChannels':audioChannels}
        if isinstance(audioStream, int):
            if self.mediaObject.streams[audioStream]['codec_type'] == 'audio':
                audioSettingsDict.update({'audioStream': audioStream})
            else:
                warnings.warn('Stream ' + str(audioStream) + ' is not an audio stream. It will not be included in the output file.')
                return
        elif audioStream is None:
            warnings.warn('No audio requested.')
        else:
            warnings.warn("Audio Stream specified not understood, won't be included.")
            return
        supportedAudioEncoders = [
         'aac', 'opus', 'vorbis', 'copy']
        if audioEncoder in supportedAudioEncoders:
            audioSettingsDict.update({'audioEncoder': audioEncoder})
        else:
            if audioEncoder == '':
                audioEncoder = 'aac'
            else:
                warnings.warn(audioEncoder + ' is not supported or recognized. Currently supported encoders are: ' + str(supportedAudioEncoders) + '. Defaulting to aac encoding.')
                audioEncoder = 'aac'
        if isinstance(audioBitrate, int):
            audioSettingsDict.update({'audioBitrate': audioBitrate})
        else:
            if isinstance(audioBitrate, float):
                audioSettingsDict.update({'audioBitrate': int(round(audioBitrate))})
            else:
                warnings.warn('Specified audio bitrate not valid or recognized, defaulting to 128 kbit/s')
                self.audioBitrate = 128
                audioSettingsDict.update({'audioChannels': audioChannels})
        audioSettingsDict.update({'index': int(audioStream)})
        self.audioStreams.append(audioSettingsDict)

    def printAudioSetting(self):
        """ Prints the audio settings of the ConversionSettings object.

        :return:
        """
        streamIndex = 0
        print('---- AUDIO SETTINGS ----')
        for stream in self.audioStreams:
            print('Stream: ' + str(stream['audioStream']))
            print('audioEncoder: ' + str(stream['audioEncoder']))
            print('audioBitrate: ' + str(stream['audioBitrate']))
            print('audioChannels: ' + str(stream['audioChannels']))
            print()

    def createSubtitleStreams(self, subtitleStreams=[]):
        """ Populates the ConversionSettings object with information on how to encode subtitles

        :param subtitleStreams:
        :return:
        """
        for streams in subtitleStreams:
            subtitleSettings = {}
            subtitleSettings.update({'index': int(streams)})
            self.subtitleStreams.append(subtitleSettings)

    def generateArgsArray--- This code section failed: ---

 L. 408         0  LOAD_CODE                <code_object mapStreamsByType>
                2  LOAD_STR                 'MediaConverter.generateArgsArray.<locals>.mapStreamsByType'
                4  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
                6  STORE_FAST               'mapStreamsByType'

 L. 421         8  LOAD_CODE                <code_object addArgsToArray>
               10  LOAD_STR                 'MediaConverter.generateArgsArray.<locals>.addArgsToArray'
               12  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
               14  STORE_FAST               'addArgsToArray'

 L. 434        16  LOAD_CLOSURE             'self'
               18  BUILD_TUPLE_1         1 
               20  LOAD_CODE                <code_object fastSeek>
               22  LOAD_STR                 'MediaConverter.generateArgsArray.<locals>.fastSeek'
               24  MAKE_FUNCTION_8          'closure'
               26  STORE_FAST               'fastSeek'

 L. 455        28  LOAD_CONST               False
               30  STORE_FAST               'streamCopy'

 L. 456        32  LOAD_CONST               False
               34  STORE_FAST               'cut'

 L. 458        36  LOAD_FAST                'addArgsToArray'
               38  LOAD_STR                 '-v '
               40  LOAD_GLOBAL              str
               42  LOAD_DEREF               'self'
               44  LOAD_ATTR                verbosity
               46  CALL_FUNCTION_1       1  '1 positional argument'
               48  BINARY_ADD       
               50  LOAD_DEREF               'self'
               52  LOAD_ATTR                argsArray
               54  CALL_FUNCTION_2       2  '2 positional arguments'
               56  POP_TOP          

 L. 460        58  LOAD_FAST                'startTime'
               60  LOAD_STR                 '0'
               62  COMPARE_OP               !=
               64  POP_JUMP_IF_FALSE   176  'to 176'
               66  LOAD_FAST                'endTime'
               68  LOAD_STR                 '0'
               70  COMPARE_OP               !=
               72  POP_JUMP_IF_FALSE   176  'to 176'

 L. 461        74  LOAD_CONST               True
               76  STORE_FAST               'cut'

 L. 463        78  LOAD_FAST                'fastSeek'
               80  LOAD_FAST                'startTime'
               82  LOAD_FAST                'endTime'
               84  CALL_FUNCTION_2       2  '2 positional arguments'
               86  UNPACK_SEQUENCE_3     3 
               88  STORE_FAST               'fastSeekTime'
               90  STORE_FAST               'startTime'
               92  STORE_FAST               'endTime'

 L. 464        94  LOAD_FAST                'addArgsToArray'
               96  LOAD_STR                 '-ss '
               98  LOAD_FAST                'fastSeekTime'
              100  BINARY_ADD       
              102  LOAD_DEREF               'self'
              104  LOAD_ATTR                argsArray
              106  CALL_FUNCTION_2       2  '2 positional arguments'
              108  POP_TOP          

 L. 465       110  LOAD_FAST                'addArgsToArray'
              112  LOAD_STR                 '-i '
              114  LOAD_DEREF               'self'
              116  LOAD_ATTR                argsArray
              118  CALL_FUNCTION_2       2  '2 positional arguments'
              120  POP_TOP          

 L. 466       122  LOAD_DEREF               'self'
              124  LOAD_ATTR                argsArray
              126  LOAD_METHOD              append
              128  LOAD_GLOBAL              str
              130  LOAD_DEREF               'self'
              132  LOAD_ATTR                mediaObject
              134  LOAD_ATTR                filePath
              136  CALL_FUNCTION_1       1  '1 positional argument'
              138  CALL_METHOD_1         1  '1 positional argument'
              140  POP_TOP          

 L. 469       142  LOAD_FAST                'addArgsToArray'
              144  LOAD_STR                 '-ss '
              146  LOAD_FAST                'startTime'
              148  BINARY_ADD       
              150  LOAD_DEREF               'self'
              152  LOAD_ATTR                argsArray
              154  CALL_FUNCTION_2       2  '2 positional arguments'
              156  POP_TOP          

 L. 470       158  LOAD_FAST                'addArgsToArray'
              160  LOAD_STR                 '-to '
              162  LOAD_FAST                'endTime'
              164  BINARY_ADD       
              166  LOAD_DEREF               'self'
              168  LOAD_ATTR                argsArray
              170  CALL_FUNCTION_2       2  '2 positional arguments'
              172  POP_TOP          
              174  JUMP_FORWARD        208  'to 208'
            176_0  COME_FROM            72  '72'
            176_1  COME_FROM            64  '64'

 L. 473       176  LOAD_FAST                'addArgsToArray'
              178  LOAD_STR                 '-i'
              180  LOAD_DEREF               'self'
              182  LOAD_ATTR                argsArray
              184  CALL_FUNCTION_2       2  '2 positional arguments'
              186  POP_TOP          

 L. 474       188  LOAD_DEREF               'self'
              190  LOAD_ATTR                argsArray
              192  LOAD_METHOD              append
              194  LOAD_GLOBAL              str
              196  LOAD_DEREF               'self'
              198  LOAD_ATTR                mediaObject
              200  LOAD_ATTR                filePath
              202  CALL_FUNCTION_1       1  '1 positional argument'
              204  CALL_METHOD_1         1  '1 positional argument'
              206  POP_TOP          
            208_0  COME_FROM           174  '174'

 L. 477       208  LOAD_STR                 '0:'
              210  STORE_FAST               'fileIndex'

 L. 480       212  SETUP_LOOP          260  'to 260'
              214  LOAD_DEREF               'self'
              216  LOAD_ATTR                videoStreams
              218  LOAD_DEREF               'self'
              220  LOAD_ATTR                audioStreams
              222  LOAD_DEREF               'self'
              224  LOAD_ATTR                subtitleStreams
              226  LOAD_DEREF               'self'
              228  LOAD_ATTR                attachmentStreams
              230  LOAD_DEREF               'self'
              232  LOAD_ATTR                otherStreams
              234  BUILD_LIST_5          5 
              236  GET_ITER         
              238  FOR_ITER            258  'to 258'
              240  STORE_FAST               'streamType'

 L. 481       242  LOAD_FAST                'mapStreamsByType'
              244  LOAD_FAST                'streamType'
              246  LOAD_FAST                'fileIndex'
              248  LOAD_DEREF               'self'
              250  LOAD_ATTR                argsArray
              252  CALL_FUNCTION_3       3  '3 positional arguments'
              254  POP_TOP          
              256  JUMP_BACK           238  'to 238'
              258  POP_BLOCK        
            260_0  COME_FROM_LOOP      212  '212'

 L. 483       260  LOAD_DEREF               'self'
              262  LOAD_ATTR                debug
          264_266  POP_JUMP_IF_FALSE   286  'to 286'

 L. 484       268  LOAD_GLOBAL              print
              270  LOAD_STR                 'Conversion argArray after stream mapping: '
              272  LOAD_GLOBAL              str
              274  LOAD_DEREF               'self'
              276  LOAD_ATTR                argsArray
              278  CALL_FUNCTION_1       1  '1 positional argument'
              280  BINARY_ADD       
              282  CALL_FUNCTION_1       1  '1 positional argument'
              284  POP_TOP          
            286_0  COME_FROM           264  '264'

 L. 487       286  BUILD_LIST_0          0 
              288  STORE_FAST               'vidStrings'

 L. 488       290  LOAD_STR                 'libx264'

 L. 489       292  LOAD_STR                 'libx265'

 L. 490       294  LOAD_STR                 'libvpx'

 L. 491       296  LOAD_STR                 'libvpx-vp9'

 L. 492       298  LOAD_STR                 'copy'
              300  LOAD_CONST               ('x264', 'x265', 'vp8', 'vp9', 'copy')
              302  BUILD_CONST_KEY_MAP_5     5 
              304  STORE_FAST               'ffVideoEncoderNames'

 L. 494   306_308  SETUP_LOOP          752  'to 752'
              310  LOAD_DEREF               'self'
              312  LOAD_ATTR                videoStreams
              314  GET_ITER         
          316_318  FOR_ITER            750  'to 750'
              320  STORE_FAST               'stream'

 L. 495       322  LOAD_CONST               0
              324  STORE_FAST               'streamIndex'

 L. 496       326  LOAD_FAST                'stream'
              328  LOAD_STR                 'videoEncoder'
              330  BINARY_SUBSCR    
              332  LOAD_STR                 'copy'
              334  COMPARE_OP               ==
          336_338  POP_JUMP_IF_FALSE   370  'to 370'

 L. 497       340  LOAD_CONST               True
              342  STORE_FAST               'streamCopy'

 L. 498       344  LOAD_FAST                'addArgsToArray'
              346  LOAD_STR                 '-c:v copy'
              348  LOAD_DEREF               'self'
              350  LOAD_ATTR                argsArray
              352  CALL_FUNCTION_2       2  '2 positional arguments'
              354  POP_TOP          

 L. 499       356  LOAD_FAST                'vidStrings'
              358  LOAD_METHOD              append
              360  LOAD_STR                 '-c:v copy'
              362  CALL_METHOD_1         1  '1 positional argument'
              364  POP_TOP          
          366_368  JUMP_FORWARD        738  'to 738'
            370_0  COME_FROM           336  '336'

 L. 502       370  LOAD_STR                 ' -c:v '
              372  LOAD_FAST                'ffVideoEncoderNames'
              374  LOAD_FAST                'stream'
              376  LOAD_STR                 'videoEncoder'
              378  BINARY_SUBSCR    
              380  BINARY_SUBSCR    
              382  BINARY_ADD       
              384  STORE_FAST               'vidString'

 L. 504       386  LOAD_FAST                'stream'
              388  LOAD_STR                 'bitrateMode'
              390  BINARY_SUBSCR    
              392  LOAD_STR                 'cbr'
              394  COMPARE_OP               ==
          396_398  POP_JUMP_IF_FALSE   506  'to 506'

 L. 505       400  LOAD_FAST                'stream'
              402  LOAD_STR                 'videoEncoder'
              404  BINARY_SUBSCR    
              406  LOAD_STR                 'vp9'
              408  COMPARE_OP               ==
          410_412  POP_JUMP_IF_TRUE    414  'to 414'
            414_0  COME_FROM           410  '410'

 L. 506       414  LOAD_FAST                'vidString'

 L. 507       416  LOAD_STR                 ' -minrate '
              418  LOAD_GLOBAL              str
              420  LOAD_FAST                'stream'
              422  LOAD_STR                 'rateConstant'
              424  BINARY_SUBSCR    
              426  CALL_FUNCTION_1       1  '1 positional argument'
              428  BINARY_ADD       
              430  LOAD_STR                 'k'
              432  BINARY_ADD       
              434  LOAD_STR                 ' -maxrate '
              436  BINARY_ADD       
              438  LOAD_GLOBAL              str
              440  LOAD_FAST                'stream'
              442  LOAD_STR                 'rateConstant'
              444  BINARY_SUBSCR    
              446  CALL_FUNCTION_1       1  '1 positional argument'
              448  BINARY_ADD       
              450  LOAD_STR                 'k'
              452  BINARY_ADD       
              454  LOAD_STR                 ' -b:v '
              456  BINARY_ADD       
              458  LOAD_GLOBAL              str
              460  LOAD_FAST                'stream'
              462  LOAD_STR                 'rateConstant'
              464  BINARY_SUBSCR    
              466  CALL_FUNCTION_1       1  '1 positional argument'
              468  BINARY_ADD       
              470  LOAD_STR                 'k'
              472  BINARY_ADD       
              474  INPLACE_ADD      
              476  STORE_FAST               'vidString'
              478  JUMP_FORWARD        504  'to 504'

 L. 509       480  LOAD_FAST                'vidString'
              482  LOAD_STR                 ' -b:v '
              484  LOAD_GLOBAL              str
              486  LOAD_FAST                'stream'
              488  LOAD_STR                 'rateConstant'
              490  BINARY_SUBSCR    
              492  CALL_FUNCTION_1       1  '1 positional argument'
              494  BINARY_ADD       
              496  LOAD_STR                 'k'
              498  BINARY_ADD       
              500  INPLACE_ADD      
              502  STORE_FAST               'vidString'
            504_0  COME_FROM           478  '478'
              504  JUMP_FORWARD        632  'to 632'
            506_0  COME_FROM           396  '396'

 L. 510       506  LOAD_FAST                'stream'
              508  LOAD_STR                 'bitrateMode'
              510  BINARY_SUBSCR    
              512  LOAD_STR                 'crf'
              514  COMPARE_OP               ==
          516_518  POP_JUMP_IF_FALSE   582  'to 582'

 L. 511       520  LOAD_FAST                'stream'
              522  LOAD_STR                 'videoEncoder'
              524  BINARY_SUBSCR    
              526  LOAD_STR                 'vp9'
              528  COMPARE_OP               ==
          530_532  POP_JUMP_IF_FALSE   560  'to 560'

 L. 512       534  LOAD_FAST                'vidString'
              536  LOAD_STR                 ' -crf '
              538  LOAD_GLOBAL              str
              540  LOAD_FAST                'stream'
              542  LOAD_STR                 'rateConstant'
              544  BINARY_SUBSCR    
              546  CALL_FUNCTION_1       1  '1 positional argument'
              548  BINARY_ADD       
              550  LOAD_STR                 ' -b:v 0 '
              552  BINARY_ADD       
              554  INPLACE_ADD      
              556  STORE_FAST               'vidString'
              558  JUMP_FORWARD        580  'to 580'
            560_0  COME_FROM           530  '530'

 L. 514       560  LOAD_FAST                'vidString'
              562  LOAD_STR                 ' -crf '
              564  LOAD_GLOBAL              str
              566  LOAD_FAST                'stream'
              568  LOAD_STR                 'rateConstant'
              570  BINARY_SUBSCR    
              572  CALL_FUNCTION_1       1  '1 positional argument'
              574  BINARY_ADD       
              576  INPLACE_ADD      
              578  STORE_FAST               'vidString'
            580_0  COME_FROM           558  '558'
              580  JUMP_FORWARD        632  'to 632'
            582_0  COME_FROM           516  '516'

 L. 516       582  LOAD_FAST                'stream'
              584  LOAD_STR                 'bitrateMode'
              586  BINARY_SUBSCR    
              588  LOAD_STR                 'vbr'
              590  COMPARE_OP               ==
          592_594  POP_JUMP_IF_FALSE   622  'to 622'

 L. 517       596  LOAD_FAST                'vidString'
              598  LOAD_STR                 ' -b:v '
              600  LOAD_GLOBAL              str
              602  LOAD_FAST                'stream'
              604  LOAD_STR                 'rateConstant'
              606  BINARY_SUBSCR    
              608  CALL_FUNCTION_1       1  '1 positional argument'
              610  BINARY_ADD       
              612  LOAD_STR                 'k'
              614  BINARY_ADD       
              616  INPLACE_ADD      
              618  STORE_FAST               'vidString'
              620  JUMP_FORWARD        632  'to 632'
            622_0  COME_FROM           592  '592'

 L. 519       622  LOAD_GLOBAL              warnings
              624  LOAD_METHOD              warn
              626  LOAD_STR                 "'bitrateMode' not understood in generateArgsArray. Should be 'cbr', 'vbr', 'crf'."
              628  CALL_METHOD_1         1  '1 positional argument'
              630  POP_TOP          
            632_0  COME_FROM           620  '620'
            632_1  COME_FROM           580  '580'
            632_2  COME_FROM           504  '504'

 L. 521       632  LOAD_FAST                'vidString'
              634  LOAD_STR                 ' -vf scale='
              636  LOAD_GLOBAL              str
              638  LOAD_FAST                'stream'
              640  LOAD_STR                 'width'
              642  BINARY_SUBSCR    
              644  CALL_FUNCTION_1       1  '1 positional argument'
              646  BINARY_ADD       
              648  LOAD_STR                 ':'
              650  BINARY_ADD       
              652  LOAD_GLOBAL              str
              654  LOAD_FAST                'stream'
              656  LOAD_STR                 'height'
              658  BINARY_SUBSCR    
              660  CALL_FUNCTION_1       1  '1 positional argument'
              662  BINARY_ADD       
              664  INPLACE_ADD      
              666  STORE_FAST               'vidString'

 L. 523       668  LOAD_FAST                'stream'
              670  LOAD_STR                 'videoEncoder'
              672  BINARY_SUBSCR    
              674  LOAD_STR                 'x264'
              676  COMPARE_OP               ==
          678_680  POP_JUMP_IF_TRUE    696  'to 696'
              682  LOAD_FAST                'stream'
              684  LOAD_STR                 'videoEncoder'
              686  BINARY_SUBSCR    
              688  LOAD_STR                 'x265'
              690  COMPARE_OP               ==
          692_694  POP_JUMP_IF_FALSE   716  'to 716'
            696_0  COME_FROM           678  '678'

 L. 524       696  LOAD_FAST                'vidString'
              698  LOAD_STR                 ' -preset '
              700  LOAD_GLOBAL              str
              702  LOAD_FAST                'stream'
              704  LOAD_STR                 'speed'
              706  BINARY_SUBSCR    
              708  CALL_FUNCTION_1       1  '1 positional argument'
              710  BINARY_ADD       
              712  INPLACE_ADD      
              714  STORE_FAST               'vidString'
            716_0  COME_FROM           692  '692'

 L. 526       716  LOAD_FAST                'addArgsToArray'
              718  LOAD_FAST                'vidString'
              720  LOAD_DEREF               'self'
              722  LOAD_ATTR                argsArray
              724  CALL_FUNCTION_2       2  '2 positional arguments'
              726  POP_TOP          

 L. 527       728  LOAD_FAST                'vidStrings'
              730  LOAD_METHOD              append
              732  LOAD_FAST                'vidString'
              734  CALL_METHOD_1         1  '1 positional argument'
              736  POP_TOP          
            738_0  COME_FROM           366  '366'

 L. 529       738  LOAD_FAST                'streamIndex'
              740  LOAD_CONST               1
              742  INPLACE_ADD      
              744  STORE_FAST               'streamIndex'
          746_748  JUMP_BACK           316  'to 316'
              750  POP_BLOCK        
            752_0  COME_FROM_LOOP      306  '306'

 L. 532       752  LOAD_DEREF               'self'
              754  LOAD_ATTR                debug
          756_758  POP_JUMP_IF_FALSE   778  'to 778'

 L. 533       760  LOAD_GLOBAL              print
              762  LOAD_STR                 'Conversion argArray after video stream(s): '
              764  LOAD_GLOBAL              str
              766  LOAD_DEREF               'self'
              768  LOAD_ATTR                argsArray
              770  CALL_FUNCTION_1       1  '1 positional argument'
              772  BINARY_ADD       
              774  CALL_FUNCTION_1       1  '1 positional argument'
              776  POP_TOP          
            778_0  COME_FROM           756  '756'

 L. 536       778  BUILD_LIST_0          0 
              780  STORE_FAST               'audioStrings'

 L. 537       782  LOAD_STR                 'aac'

 L. 538       784  LOAD_STR                 'libaac_fdk'

 L. 539       786  LOAD_STR                 'libmp3lame'

 L. 540       788  LOAD_STR                 'flac'

 L. 541       790  LOAD_STR                 'libopus'

 L. 542       792  LOAD_STR                 'libvorbis'

 L. 543       794  LOAD_STR                 'copy'
              796  LOAD_CONST               ('aac', 'fdk', 'lame', 'flac', 'opus', 'vorbis', 'copy')
              798  BUILD_CONST_KEY_MAP_7     7 
              800  STORE_FAST               'ffAudioEncoderNames'

 L. 545       802  LOAD_CONST               0
              804  STORE_FAST               'streamIndex'

 L. 546   806_808  SETUP_LOOP         1224  'to 1224'
              810  LOAD_DEREF               'self'
              812  LOAD_ATTR                audioStreams
              814  GET_ITER         
          816_818  FOR_ITER           1222  'to 1222'
              820  STORE_FAST               'stream'

 L. 547       822  LOAD_FAST                'stream'
              824  LOAD_STR                 'audioEncoder'
              826  BINARY_SUBSCR    
              828  LOAD_STR                 'copy'
              830  COMPARE_OP               ==
          832_834  POP_JUMP_IF_FALSE   882  'to 882'

 L. 548       836  LOAD_CONST               True
              838  STORE_FAST               'streamCopy'

 L. 549       840  LOAD_STR                 ' -c:a:'
              842  LOAD_GLOBAL              str
              844  LOAD_FAST                'streamIndex'
              846  CALL_FUNCTION_1       1  '1 positional argument'
              848  BINARY_ADD       
              850  LOAD_STR                 ' copy'
              852  BINARY_ADD       
              854  STORE_FAST               'fragment'

 L. 550       856  LOAD_FAST                'addArgsToArray'
              858  LOAD_FAST                'fragment'
              860  LOAD_DEREF               'self'
              862  LOAD_ATTR                argsArray
              864  CALL_FUNCTION_2       2  '2 positional arguments'
              866  POP_TOP          

 L. 551       868  LOAD_FAST                'audioStrings'
              870  LOAD_METHOD              append
              872  LOAD_FAST                'fragment'
              874  CALL_METHOD_1         1  '1 positional argument'
              876  POP_TOP          
          878_880  JUMP_FORWARD       1210  'to 1210'
            882_0  COME_FROM           832  '832'

 L. 553       882  LOAD_FAST                'stream'
              884  LOAD_STR                 'audioEncoder'
              886  BINARY_SUBSCR    
              888  LOAD_STR                 'opus'
              890  COMPARE_OP               ==
          892_894  POP_JUMP_IF_FALSE  1130  'to 1130'

 L. 554       896  LOAD_FAST                'stream'
              898  LOAD_STR                 'audioChannels'
              900  BINARY_SUBSCR    
              902  LOAD_STR                 'mono'
              904  COMPARE_OP               ==
          906_908  POP_JUMP_IF_FALSE  1022  'to 1022'

 L. 556       910  LOAD_FAST                'addArgsToArray'
              912  LOAD_STR                 '-c:a:'
              914  LOAD_GLOBAL              str
              916  LOAD_FAST                'streamIndex'
              918  CALL_FUNCTION_1       1  '1 positional argument'
              920  BINARY_ADD       
              922  LOAD_STR                 ' '
              924  BINARY_ADD       
              926  LOAD_GLOBAL              str
              928  LOAD_FAST                'ffAudioEncoderNames'
              930  LOAD_FAST                'stream'
              932  LOAD_STR                 'audioEncoder'
              934  BINARY_SUBSCR    
              936  BINARY_SUBSCR    
              938  CALL_FUNCTION_1       1  '1 positional argument'
              940  BINARY_ADD       

 L. 557       942  LOAD_STR                 ' -af aformat=channel_layouts=mono'
              944  BINARY_ADD       
              946  LOAD_DEREF               'self'
              948  LOAD_ATTR                argsArray
              950  CALL_FUNCTION_2       2  '2 positional arguments'
              952  POP_TOP          

 L. 559       954  LOAD_FAST                'addArgsToArray'
              956  LOAD_STR                 '-b:a:'
              958  LOAD_GLOBAL              str
              960  LOAD_FAST                'streamIndex'
              962  CALL_FUNCTION_1       1  '1 positional argument'
              964  BINARY_ADD       
              966  LOAD_STR                 ' '
              968  BINARY_ADD       
              970  LOAD_GLOBAL              str
              972  LOAD_FAST                'stream'
              974  LOAD_STR                 'audioBitrate'
              976  BINARY_SUBSCR    
              978  CALL_FUNCTION_1       1  '1 positional argument'
              980  BINARY_ADD       
              982  LOAD_STR                 'k '
              984  BINARY_ADD       
              986  LOAD_DEREF               'self'
              988  LOAD_ATTR                argsArray
              990  CALL_FUNCTION_2       2  '2 positional arguments'
              992  POP_TOP          

 L. 560       994  LOAD_FAST                'stream'
              996  LOAD_STR                 'audioBitrate'
              998  BINARY_SUBSCR    
             1000  LOAD_CONST               128
             1002  COMPARE_OP               !=
         1004_1006  POP_JUMP_IF_FALSE  1128  'to 1128'

 L. 561      1008  LOAD_FAST                'addArgsToArray'
             1010  LOAD_STR                 '-vbr constrained'
             1012  LOAD_DEREF               'self'
             1014  LOAD_ATTR                argsArray
             1016  CALL_FUNCTION_2       2  '2 positional arguments'
             1018  POP_TOP          
             1020  JUMP_FORWARD       1128  'to 1128'
           1022_0  COME_FROM           906  '906'

 L. 564      1022  LOAD_FAST                'addArgsToArray'
             1024  LOAD_STR                 '-c:a:'
             1026  LOAD_GLOBAL              str
             1028  LOAD_FAST                'streamIndex'
             1030  CALL_FUNCTION_1       1  '1 positional argument'
             1032  BINARY_ADD       
             1034  LOAD_STR                 ' '
             1036  BINARY_ADD       
             1038  LOAD_GLOBAL              str
             1040  LOAD_FAST                'ffAudioEncoderNames'
             1042  LOAD_FAST                'stream'
             1044  LOAD_STR                 'audioEncoder'
             1046  BINARY_SUBSCR    
             1048  BINARY_SUBSCR    
             1050  CALL_FUNCTION_1       1  '1 positional argument'
             1052  BINARY_ADD       
             1054  LOAD_DEREF               'self'
             1056  LOAD_ATTR                argsArray
             1058  CALL_FUNCTION_2       2  '2 positional arguments'
             1060  POP_TOP          

 L. 566      1062  LOAD_FAST                'addArgsToArray'
             1064  LOAD_STR                 '-b:a:'
             1066  LOAD_GLOBAL              str
             1068  LOAD_FAST                'streamIndex'
             1070  CALL_FUNCTION_1       1  '1 positional argument'
             1072  BINARY_ADD       
             1074  LOAD_STR                 ' '
             1076  BINARY_ADD       
             1078  LOAD_GLOBAL              str
             1080  LOAD_FAST                'stream'
             1082  LOAD_STR                 'audioBitrate'
             1084  BINARY_SUBSCR    
             1086  CALL_FUNCTION_1       1  '1 positional argument'
             1088  BINARY_ADD       
             1090  LOAD_STR                 'k '
             1092  BINARY_ADD       
             1094  LOAD_DEREF               'self'
             1096  LOAD_ATTR                argsArray
             1098  CALL_FUNCTION_2       2  '2 positional arguments'
             1100  POP_TOP          

 L. 567      1102  LOAD_FAST                'stream'
             1104  LOAD_STR                 'audioBitrate'
             1106  BINARY_SUBSCR    
             1108  LOAD_CONST               128
             1110  COMPARE_OP               !=
         1112_1114  POP_JUMP_IF_FALSE  1210  'to 1210'

 L. 568      1116  LOAD_FAST                'addArgsToArray'
             1118  LOAD_STR                 '-vbr constrained'
             1120  LOAD_DEREF               'self'
             1122  LOAD_ATTR                argsArray
             1124  CALL_FUNCTION_2       2  '2 positional arguments'
             1126  POP_TOP          
           1128_0  COME_FROM          1020  '1020'
           1128_1  COME_FROM          1004  '1004'
             1128  JUMP_FORWARD       1210  'to 1210'
           1130_0  COME_FROM           892  '892'

 L. 575      1130  LOAD_FAST                'addArgsToArray'
             1132  LOAD_STR                 '-c:a:'
             1134  LOAD_GLOBAL              str
             1136  LOAD_FAST                'streamIndex'
             1138  CALL_FUNCTION_1       1  '1 positional argument'
             1140  BINARY_ADD       
             1142  LOAD_STR                 ' '
             1144  BINARY_ADD       
             1146  LOAD_GLOBAL              str
             1148  LOAD_FAST                'ffAudioEncoderNames'
             1150  LOAD_FAST                'stream'
             1152  LOAD_STR                 'audioEncoder'
             1154  BINARY_SUBSCR    
             1156  BINARY_SUBSCR    
             1158  CALL_FUNCTION_1       1  '1 positional argument'
             1160  BINARY_ADD       
             1162  LOAD_DEREF               'self'
             1164  LOAD_ATTR                argsArray
             1166  CALL_FUNCTION_2       2  '2 positional arguments'
             1168  POP_TOP          

 L. 576      1170  LOAD_FAST                'addArgsToArray'
             1172  LOAD_STR                 '-b:a:'
             1174  LOAD_GLOBAL              str
             1176  LOAD_FAST                'streamIndex'
             1178  CALL_FUNCTION_1       1  '1 positional argument'
             1180  BINARY_ADD       
             1182  LOAD_STR                 ' '
             1184  BINARY_ADD       
             1186  LOAD_GLOBAL              str
             1188  LOAD_FAST                'stream'
             1190  LOAD_STR                 'audioBitrate'
             1192  BINARY_SUBSCR    
             1194  CALL_FUNCTION_1       1  '1 positional argument'
             1196  BINARY_ADD       
             1198  LOAD_STR                 'k '
             1200  BINARY_ADD       
             1202  LOAD_DEREF               'self'
             1204  LOAD_ATTR                argsArray
             1206  CALL_FUNCTION_2       2  '2 positional arguments'
             1208  POP_TOP          
           1210_0  COME_FROM          1128  '1128'
           1210_1  COME_FROM          1112  '1112'
           1210_2  COME_FROM           878  '878'

 L. 578      1210  LOAD_FAST                'streamIndex'
             1212  LOAD_CONST               1
             1214  INPLACE_ADD      
             1216  STORE_FAST               'streamIndex'
         1218_1220  JUMP_BACK           816  'to 816'
             1222  POP_BLOCK        
           1224_0  COME_FROM_LOOP      806  '806'

 L. 580      1224  LOAD_DEREF               'self'
             1226  LOAD_ATTR                debug
         1228_1230  POP_JUMP_IF_FALSE  1250  'to 1250'

 L. 581      1232  LOAD_GLOBAL              print
             1234  LOAD_STR                 'Conversion argArray after audio stream(s): '
             1236  LOAD_GLOBAL              str
             1238  LOAD_DEREF               'self'
             1240  LOAD_ATTR                argsArray
             1242  CALL_FUNCTION_1       1  '1 positional argument'
             1244  BINARY_ADD       
             1246  CALL_FUNCTION_1       1  '1 positional argument'
             1248  POP_TOP          
           1250_0  COME_FROM          1228  '1228'

 L. 583      1250  SETUP_LOOP         1280  'to 1280'
             1252  LOAD_DEREF               'self'
             1254  LOAD_ATTR                subtitleStreams
             1256  GET_ITER         
             1258  FOR_ITER           1278  'to 1278'
             1260  STORE_FAST               'stream'

 L. 585      1262  LOAD_FAST                'addArgsToArray'
             1264  LOAD_STR                 '-c:s copy'
             1266  LOAD_DEREF               'self'
             1268  LOAD_ATTR                argsArray
             1270  CALL_FUNCTION_2       2  '2 positional arguments'
             1272  POP_TOP          
         1274_1276  JUMP_BACK          1258  'to 1258'
             1278  POP_BLOCK        
           1280_0  COME_FROM_LOOP     1250  '1250'

 L. 587      1280  LOAD_DEREF               'self'
             1282  LOAD_ATTR                debug
         1284_1286  POP_JUMP_IF_FALSE  1306  'to 1306'

 L. 588      1288  LOAD_GLOBAL              print
             1290  LOAD_STR                 'Conversion argArray after subtitle stream(s): '
             1292  LOAD_GLOBAL              str
             1294  LOAD_DEREF               'self'
             1296  LOAD_ATTR                argsArray
             1298  CALL_FUNCTION_1       1  '1 positional argument'
             1300  BINARY_ADD       
             1302  CALL_FUNCTION_1       1  '1 positional argument'
             1304  POP_TOP          
           1306_0  COME_FROM          1284  '1284'

 L. 590      1306  LOAD_FAST                'streamCopy'
         1308_1310  POP_JUMP_IF_FALSE  1330  'to 1330'
             1312  LOAD_FAST                'cut'
         1314_1316  POP_JUMP_IF_FALSE  1330  'to 1330'

 L. 591      1318  LOAD_FAST                'addArgsToArray'
             1320  LOAD_STR                 '-avoid_negative_ts 1'
             1322  LOAD_DEREF               'self'
             1324  LOAD_ATTR                argsArray
             1326  CALL_FUNCTION_2       2  '2 positional arguments'
             1328  POP_TOP          
           1330_0  COME_FROM          1314  '1314'
           1330_1  COME_FROM          1308  '1308'

 L. 592      1330  LOAD_DEREF               'self'
             1332  LOAD_ATTR                argsArray
             1334  LOAD_METHOD              append
             1336  LOAD_DEREF               'self'
             1338  LOAD_ATTR                outputFilePath
             1340  CALL_METHOD_1         1  '1 positional argument'
             1342  POP_TOP          

 L. 594      1344  LOAD_DEREF               'self'
             1346  LOAD_ATTR                debug
         1348_1350  POP_JUMP_IF_FALSE  1370  'to 1370'

 L. 595      1352  LOAD_GLOBAL              print
             1354  LOAD_STR                 'Conversion argArray after output file: '
             1356  LOAD_GLOBAL              str
             1358  LOAD_DEREF               'self'
             1360  LOAD_ATTR                argsArray
             1362  CALL_FUNCTION_1       1  '1 positional argument'
             1364  BINARY_ADD       
             1366  CALL_FUNCTION_1       1  '1 positional argument'
             1368  POP_TOP          
           1370_0  COME_FROM          1348  '1348'

Parse error at or near `JUMP_FORWARD' instruction at offset 504

    def estimateVideoBitrate(self, targetFileSize, startTime=-1, endTime=-1, audioBitrate=-1, otherBitrates=0):
        if startTime == -1:
            if endTime == -1:
                duration = timecode_to_seconds(self.mediaObject.duration)
            else:
                duration = timecode_to_seconds(subtract_timecodes(startTime, endTime))
            if audioBitrate == -1:
                if self.audioStreams != []:
                    audioBitrate = 0
                    for audioStream in self.audioStreams:
                        audioBitrate += audioStream['audioBitrate']

        else:
            audioBitrate = 128
            print('No audioBitrate specified for estimation, defaulting to 128kbit/s')
        estimatedBitrate = targetFileSize / duration - (audioBitrate + otherBitrates)
        return estimatedBitrate

    def createAttachementSettings(self, mediaObject):
        pass

    def createOtherSettings(self, mediaObject):
        pass