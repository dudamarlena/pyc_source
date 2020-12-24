# uncompyle6 version 3.6.7
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build\bdist.win32\egg\aigpy\tagHelper.py
# Compiled at: 2020-02-14 05:17:03
# Size of source mod 2**32: 6061 bytes
__doc__ = '\n@File    :   tagHelper.py\n@Time    :   2019/07/18\n@Author  :   Yaron Huang \n@Version :   1.0\n@Contact :   yaronhuang@qq.com\n@Desc    :   \n'
import os, sys
from mutagen import File
from mutagen import flac
from mutagen import mp4
from mutagen.id3 import TALB, TCOP, TDRC, TIT2, TPE1, TRCK, APIC, TCON, TCOM, TSRC
from aigpy import pathHelper

def _getHash(pHash, key):
    if key in pHash:
        return pHash[key]
    return ''


def _lower(inputs):
    if isinstance(inputs, str):
        inputs = inputs.decode('utf-8')
    inputs = inputs.lower().encode('utf-8')
    return inputs


def _getExtension(filepath):
    index = filepath.rfind('.')
    ret = filepath[index + 1:len(filepath)]
    v = sys.version_info
    if v[0] > 2:
        return str.lower(ret)
    return _lower(ret)


def _getFileData--- This code section failed: ---

 L.  44         0  SETUP_FINALLY        50  'to 50'

 L.  45         2  LOAD_GLOBAL              open
                4  LOAD_FAST                'filepath'
                6  LOAD_STR                 'rb'
                8  CALL_FUNCTION_2       2  ''
               10  SETUP_WITH           40  'to 40'
               12  STORE_FAST               'f'

 L.  46        14  LOAD_FAST                'f'
               16  LOAD_METHOD              read
               18  CALL_METHOD_0         0  ''
               20  STORE_FAST               'data'

 L.  47        22  LOAD_FAST                'data'
               24  POP_BLOCK        
               26  ROT_TWO          
               28  BEGIN_FINALLY    
               30  WITH_CLEANUP_START
               32  WITH_CLEANUP_FINISH
               34  POP_FINALLY           0  ''
               36  POP_BLOCK        
               38  RETURN_VALUE     
             40_0  COME_FROM_WITH       10  '10'
               40  WITH_CLEANUP_START
               42  WITH_CLEANUP_FINISH
               44  END_FINALLY      
               46  POP_BLOCK        
               48  JUMP_FORWARD         64  'to 64'
             50_0  COME_FROM_FINALLY     0  '0'

 L.  48        50  POP_TOP          
               52  POP_TOP          
               54  POP_TOP          

 L.  49        56  POP_EXCEPT       
               58  LOAD_CONST               None
               60  RETURN_VALUE     
               62  END_FINALLY      
             64_0  COME_FROM            48  '48'

Parse error at or near `POP_BLOCK' instruction at offset 24


def _tryInt--- This code section failed: ---

 L.  53         0  SETUP_FINALLY        16  'to 16'

 L.  54         2  LOAD_GLOBAL              int
                4  LOAD_FAST                'obj'
                6  CALL_FUNCTION_1       1  ''
                8  STORE_FAST               'ret'

 L.  55        10  LOAD_FAST                'ret'
               12  POP_BLOCK        
               14  RETURN_VALUE     
             16_0  COME_FROM_FINALLY     0  '0'

 L.  56        16  POP_TOP          
               18  POP_TOP          
               20  POP_TOP          

 L.  57        22  POP_EXCEPT       
               24  LOAD_CONST               0
               26  RETURN_VALUE     
               28  END_FINALLY      

Parse error at or near `POP_BLOCK' instruction at offset 12


def _getArrayStr(array):
    if array is None:
        return ''
    if len(array) <= 0:
        return array
    ret = None
    for item in array:
        if ret is None:
            ret = item
        else:
            ret += ', ' + item

    return ret


def _noneToEmptyString(obj):
    if obj is None:
        return ''
    return obj


class TagTool(object):

    def __init__(self, filePath):
        if os.path.isfile(filePath) is False:
            return
        self._filepath = filePath
        self._ext = _getExtension(filePath)
        self._handle = File(filePath)
        self.title = ''
        self.album = ''
        self.albumartist = ''
        self.artist = ''
        self.copyright = ''
        self.tracknumber = ''
        self.totaltrack = ''
        self.discnumber = ''
        self.totaldisc = ''
        self.genre = ''
        self.date = ''
        self.composer = ''
        self.isrc = ''

    def save--- This code section failed: ---

 L. 105         0  SETUP_FINALLY        84  'to 84'

 L. 106         2  LOAD_STR                 'mp3'
                4  LOAD_FAST                'self'
                6  LOAD_ATTR                _ext
                8  COMPARE_OP               in
               10  POP_JUMP_IF_FALSE    24  'to 24'

 L. 107        12  LOAD_FAST                'self'
               14  LOAD_METHOD              _saveMp3
               16  LOAD_FAST                'coverPath'
               18  CALL_METHOD_1         1  ''
               20  POP_BLOCK        
               22  RETURN_VALUE     
             24_0  COME_FROM            10  '10'

 L. 108        24  LOAD_STR                 'flac'
               26  LOAD_FAST                'self'
               28  LOAD_ATTR                _ext
               30  COMPARE_OP               in
               32  POP_JUMP_IF_FALSE    46  'to 46'

 L. 109        34  LOAD_FAST                'self'
               36  LOAD_METHOD              _saveFlac
               38  LOAD_FAST                'coverPath'
               40  CALL_METHOD_1         1  ''
               42  POP_BLOCK        
               44  RETURN_VALUE     
             46_0  COME_FROM            32  '32'

 L. 110        46  LOAD_STR                 'mp4'
               48  LOAD_FAST                'self'
               50  LOAD_ATTR                _ext
               52  COMPARE_OP               in
               54  POP_JUMP_IF_TRUE     66  'to 66'
               56  LOAD_STR                 'm4a'
               58  LOAD_FAST                'self'
               60  LOAD_ATTR                _ext
               62  COMPARE_OP               in
               64  POP_JUMP_IF_FALSE    78  'to 78'
             66_0  COME_FROM            54  '54'

 L. 111        66  LOAD_FAST                'self'
               68  LOAD_METHOD              _saveMp4
               70  LOAD_FAST                'coverPath'
               72  CALL_METHOD_1         1  ''
               74  POP_BLOCK        
               76  RETURN_VALUE     
             78_0  COME_FROM            64  '64'

 L. 112        78  POP_BLOCK        
               80  LOAD_CONST               False
               82  RETURN_VALUE     
             84_0  COME_FROM_FINALLY     0  '0'

 L. 113        84  POP_TOP          
               86  POP_TOP          
               88  POP_TOP          

 L. 114        90  POP_EXCEPT       
               92  LOAD_CONST               False
               94  RETURN_VALUE     
               96  END_FINALLY      

Parse error at or near `RETURN_VALUE' instruction at offset 22

    def _saveMp3(self, coverPath):
        self._handle.tags.add(TIT2(encoding=3, text=(self.title)))
        self._handle.tags.add(TALB(encoding=3, text=(self.album)))
        self._handle.tags.add(TPE1(encoding=3, text=(self.artist)))
        self._handle.tags.add(TCOP(encoding=3, text=(self.copyright)))
        self._handle.tags.add(TRCK(encoding=3, text=(str(self.tracknumber))))
        self._handle.tags.add(TCON(encoding=3, text=(self.genre)))
        self._handle.tags.add(TDRC(encoding=3, text=(self.date)))
        self._handle.tags.add(TCOM(encoding=3, text=(self.composer)))
        self._handle.tags.add(TSRC(encoding=3, text=(self.isrc)))
        self._savePic(coverPath)
        self._handle.save()
        return True

    def _saveFlac(self, coverPath):
        if self._handle.tags is None:
            self._handle.add_tags()
        self._handle.tags['title'] = self.title
        self._handle.tags['album'] = self.album
        self._handle.tags['albumartist'] = self.albumartist
        self._handle.tags['artist'] = self.artist
        self._handle.tags['copyright'] = _noneToEmptyString(self.copyright)
        self._handle.tags['tracknumber'] = str(self.tracknumber)
        self._handle.tags['tracktotal'] = str(self.totaltrack)
        self._handle.tags['discnumber'] = str(self.discnumber)
        self._handle.tags['disctotal'] = str(self.totaldisc)
        self._handle.tags['genre'] = _noneToEmptyString(self.genre)
        self._handle.tags['date'] = _noneToEmptyString(self.date)
        self._handle.tags['composer'] = _noneToEmptyString(self.composer)
        self._handle.tags['isrc'] = str(self.isrc)
        self._savePic(coverPath)
        self._handle.save()
        return True

    def _saveMp4(self, coverPath):
        self._handle.tags['©nam'] = self.title
        self._handle.tags['©alb'] = self.album
        self._handle.tags['aART'] = _getArrayStr(self.albumartist)
        self._handle.tags['©ART'] = _getArrayStr(self.artist)
        self._handle.tags['cprt'] = _noneToEmptyString(self.copyright)
        self._handle.tags['trkn'] = [[_tryInt(self.tracknumber), _tryInt(self.totaltrack)]]
        self._handle.tags['disk'] = [[_tryInt(self.discnumber), _tryInt(self.totaldisc)]]
        self._handle.tags['©gen'] = _noneToEmptyString(self.genre)
        self._handle.tags['©day'] = _noneToEmptyString(self.date)
        self._handle.tags['©wrt'] = _getArrayStr(self.composer)
        self._savePic(coverPath)
        self._handle.save()
        return True

    def _savePic(self, coverPath):
        data = _getFileData(coverPath)
        if data is None:
            return
        if 'flac' in self._ext:
            pic = flac.Picture()
            pic.data = data
            if pathHelper.getFileExtension(coverPath) == '.jpg':
                pic.mime = 'image/jpeg'
            self._handle.clear_pictures()
            self._handle.add_picture(pic)
        if 'mp3' in self._ext:
            self._handle.tags.add(APIC(encoding=3, data=data))
        if 'mp4' in self._ext or 'm4a' in self._ext:
            pic = mp4.MP4Cover(data)
            self._handle.tags['covr'] = [pic]