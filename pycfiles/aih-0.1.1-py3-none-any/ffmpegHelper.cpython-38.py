# uncompyle6 version 3.6.7
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build\bdist.win32\egg\aigpy\ffmpegHelper.py
# Compiled at: 2020-02-14 02:12:37
# Size of source mod 2**32: 11937 bytes
__doc__ = '\n@File    :   ffmpegHelper.py\n@Time    :   2018/12/17\n@Author  :   Yaron Huang \n@Version :   1.0\n@Contact :   yaronhuang@qq.com\n@Desc    :   \n'
import os, re, sys, shutil, subprocess
import aigpy.fileHelper as fileHelper
import aigpy.systemHelper as systemHelper
import aigpy.netHelper as netHelper
import aigpy.pathHelper as pathHelper
import aigpy.threadHelper as threadHelper
from aigpy.progressHelper import ProgressTool

class FFmpegTool(object):

    def __init__(self, threadNum=50, mergerTimeout=None):
        """
        #Func    :   初始化             
        #Param   :   threadNum     [in] 线程数          
        #Param   :   mergerTimeout [in] 超时 秒     
        #Return  :   True/False             
        """
        self.thread = threadHelper.ThreadTool(threadNum)
        self.waitCount = 0
        self.completeCount = 0
        self.progress = None
        self.mergerTimeout = mergerTimeout
        self.enable = self._checkTool()

    def __thradfunc_dl(self, url, filepath, retrycount):
        check = False
        try:
            while retrycount > 0:
                retrycount = retrycount - 1
                check = netHelper.downloadFile(url, filepath, 30)
                if check:
                    break

        except:
            pass
        else:
            self.completeCount = self.completeCount + 1
            if self.progress is not None:
                self.progress.step()

    def __parseM3u8(self, url):
        content = netHelper.downloadString(url, None)
        pattern = re.compile('(?<=http).+?(?=\\\\n)')
        plist = pattern.findall(str(content))
        urllist = []
        for item in plist:
            urllist.append('http' + item)

        return urllist

    def __process--- This code section failed: ---

 L.  66         0  LOAD_CONST               None
                2  STORE_FAST               'stdoutFile'

 L.  67         4  LOAD_CONST               None
                6  STORE_FAST               'fp'
              8_0  COME_FROM           260  '260'

 L.  68         8  LOAD_FAST                'retrycount'
               10  LOAD_CONST               0
               12  COMPARE_OP               >=
            14_16  POP_JUMP_IF_FALSE   274  'to 274'

 L.  69        18  LOAD_FAST                'retrycount'
               20  LOAD_CONST               1
               22  INPLACE_SUBTRACT 
               24  STORE_FAST               'retrycount'

 L.  70        26  SETUP_FINALLY       224  'to 224'

 L.  71        28  LOAD_FAST                'showshell'
               30  POP_JUMP_IF_FALSE    96  'to 96'

 L.  72        32  LOAD_GLOBAL              sys
               34  LOAD_ATTR                version_info
               36  LOAD_CONST               0
               38  BINARY_SUBSCR    
               40  LOAD_CONST               2
               42  COMPARE_OP               >
               44  POP_JUMP_IF_FALSE    66  'to 66'

 L.  73        46  LOAD_GLOBAL              subprocess
               48  LOAD_ATTR                call
               50  LOAD_FAST                'cmd'
               52  LOAD_FAST                'self'
               54  LOAD_ATTR                mergerTimeout
               56  LOAD_CONST               True
               58  LOAD_CONST               ('timeout', 'shell')
               60  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
               62  STORE_FAST               'res'
               64  JUMP_ABSOLUTE       206  'to 206'
             66_0  COME_FROM            44  '44'

 L.  75        66  LOAD_FAST                'cmd'
               68  LOAD_METHOD              encode
               70  LOAD_GLOBAL              sys
               72  LOAD_METHOD              getfilesystemencoding
               74  CALL_METHOD_0         0  ''
               76  CALL_METHOD_1         1  ''
               78  STORE_FAST               'cmd'

 L.  76        80  LOAD_GLOBAL              subprocess
               82  LOAD_ATTR                call
               84  LOAD_FAST                'cmd'
               86  LOAD_CONST               True
               88  LOAD_CONST               ('shell',)
               90  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
               92  STORE_FAST               'res'
               94  JUMP_FORWARD        206  'to 206'
             96_0  COME_FROM            30  '30'

 L.  78        96  LOAD_GLOBAL              pathHelper
               98  LOAD_METHOD              getFileExtension
              100  LOAD_FAST                'filename'
              102  CALL_METHOD_1         1  ''
              104  STORE_FAST               'exten'

 L.  79       106  LOAD_FAST                'filename'
              108  LOAD_METHOD              replace
              110  LOAD_FAST                'exten'
              112  LOAD_STR                 '-stdout.txt'
              114  CALL_METHOD_2         2  ''
              116  STORE_FAST               'stdoutFile'

 L.  80       118  LOAD_GLOBAL              open
              120  LOAD_FAST                'stdoutFile'
              122  LOAD_STR                 'w'
              124  CALL_FUNCTION_2       2  ''
              126  STORE_FAST               'fp'

 L.  81       128  LOAD_GLOBAL              sys
              130  LOAD_ATTR                version_info
              132  LOAD_CONST               0
              134  BINARY_SUBSCR    
              136  LOAD_CONST               2
              138  COMPARE_OP               >
              140  POP_JUMP_IF_FALSE   166  'to 166'

 L.  82       142  LOAD_GLOBAL              subprocess
              144  LOAD_ATTR                call
              146  LOAD_FAST                'cmd'
              148  LOAD_FAST                'self'
              150  LOAD_ATTR                mergerTimeout
              152  LOAD_CONST               True
              154  LOAD_FAST                'fp'
              156  LOAD_FAST                'fp'
              158  LOAD_CONST               ('timeout', 'shell', 'stdout', 'stderr')
              160  CALL_FUNCTION_KW_5     5  '5 total positional and keyword args'
              162  STORE_FAST               'res'
              164  JUMP_FORWARD        184  'to 184'
            166_0  COME_FROM           140  '140'

 L.  84       166  LOAD_GLOBAL              subprocess
              168  LOAD_ATTR                call
              170  LOAD_FAST                'cmd'
              172  LOAD_CONST               True
              174  LOAD_FAST                'fp'
              176  LOAD_FAST                'fp'
              178  LOAD_CONST               ('shell', 'stdout', 'stderr')
              180  CALL_FUNCTION_KW_4     4  '4 total positional and keyword args'
              182  STORE_FAST               'res'
            184_0  COME_FROM           164  '164'

 L.  85       184  LOAD_FAST                'fp'
              186  LOAD_METHOD              close
              188  CALL_METHOD_0         0  ''
              190  POP_TOP          

 L.  86       192  LOAD_CONST               None
              194  STORE_FAST               'fp'

 L.  87       196  LOAD_GLOBAL              pathHelper
              198  LOAD_METHOD              remove
              200  LOAD_FAST                'stdoutFile'
              202  CALL_METHOD_1         1  ''
              204  POP_TOP          
            206_0  COME_FROM            94  '94'

 L.  88       206  LOAD_FAST                'res'
              208  LOAD_CONST               0
              210  COMPARE_OP               ==
              212  POP_JUMP_IF_FALSE   220  'to 220'

 L.  89       214  POP_BLOCK        
              216  LOAD_CONST               True
              218  RETURN_VALUE     
            220_0  COME_FROM           212  '212'
              220  POP_BLOCK        
              222  JUMP_FORWARD        236  'to 236'
            224_0  COME_FROM_FINALLY    26  '26'

 L.  90       224  POP_TOP          
              226  POP_TOP          
              228  POP_TOP          

 L.  91       230  POP_EXCEPT       
              232  JUMP_FORWARD        236  'to 236'
              234  END_FINALLY      
            236_0  COME_FROM           232  '232'
            236_1  COME_FROM           222  '222'

 L.  92       236  LOAD_FAST                'fp'
              238  POP_JUMP_IF_FALSE   248  'to 248'

 L.  93       240  LOAD_FAST                'fp'
              242  LOAD_METHOD              close
              244  CALL_METHOD_0         0  ''
              246  POP_TOP          
            248_0  COME_FROM           238  '238'

 L.  94       248  LOAD_GLOBAL              pathHelper
              250  LOAD_METHOD              remove
              252  LOAD_FAST                'stdoutFile'
              254  CALL_METHOD_1         1  ''
              256  POP_TOP          

 L.  95       258  LOAD_FAST                'removeFile'
              260  POP_JUMP_IF_FALSE     8  'to 8'

 L.  96       262  LOAD_GLOBAL              pathHelper
              264  LOAD_METHOD              remove
              266  LOAD_FAST                'filename'
              268  CALL_METHOD_1         1  ''
              270  POP_TOP          
              272  JUMP_BACK             8  'to 8'
            274_0  COME_FROM            14  '14'

 L.  97       274  LOAD_CONST               False
              276  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `LOAD_CONST' instruction at offset 216

    def mergerByM3u8_Multithreading2--- This code section failed: ---

 L. 100         0  SETUP_FINALLY       118  'to 118'

 L. 102         2  LOAD_FAST                'self'
                4  LOAD_METHOD              _FFmpegTool__parseM3u8
                6  LOAD_FAST                'url'
                8  CALL_METHOD_1         1  ''
               10  STORE_FAST               'urllist'

 L. 103        12  LOAD_GLOBAL              len
               14  LOAD_FAST                'urllist'
               16  CALL_FUNCTION_1       1  ''
               18  LOAD_CONST               0
               20  COMPARE_OP               <=
               22  POP_JUMP_IF_FALSE    30  'to 30'

 L. 104        24  POP_BLOCK        
               26  LOAD_CONST               False
               28  RETURN_VALUE     
             30_0  COME_FROM            22  '22'

 L. 106        30  LOAD_GLOBAL              pathHelper
               32  LOAD_METHOD              getFileExtension
               34  LOAD_FAST                'filepath'
               36  CALL_METHOD_1         1  ''
               38  STORE_FAST               'ext'

 L. 107        40  LOAD_FAST                'filepath'
               42  LOAD_METHOD              replace
               44  LOAD_FAST                'ext'
               46  LOAD_STR                 '.ts'
               48  CALL_METHOD_2         2  ''
               50  STORE_FAST               'tspath'

 L. 108        52  LOAD_GLOBAL              pathHelper
               54  LOAD_METHOD              remove
               56  LOAD_FAST                'tspath'
               58  CALL_METHOD_1         1  ''
               60  POP_TOP          

 L. 109        62  LOAD_GLOBAL              netHelper
               64  LOAD_METHOD              downloadFileByUrls
               66  LOAD_FAST                'urllist'
               68  LOAD_FAST                'tspath'
               70  LOAD_CONST               30
               72  LOAD_CONST               True
               74  CALL_METHOD_4         4  ''
               76  POP_JUMP_IF_TRUE     84  'to 84'

 L. 110        78  POP_BLOCK        
               80  LOAD_CONST               False
               82  RETURN_VALUE     
             84_0  COME_FROM            76  '76'

 L. 111        84  LOAD_FAST                'self'
               86  LOAD_METHOD              covertFile
               88  LOAD_FAST                'tspath'
               90  LOAD_FAST                'filepath'
               92  CALL_METHOD_2         2  ''
               94  POP_JUMP_IF_FALSE   112  'to 112'

 L. 112        96  LOAD_GLOBAL              pathHelper
               98  LOAD_METHOD              remove
              100  LOAD_FAST                'tspath'
              102  CALL_METHOD_1         1  ''
              104  POP_TOP          

 L. 113       106  POP_BLOCK        
              108  LOAD_CONST               True
              110  RETURN_VALUE     
            112_0  COME_FROM            94  '94'

 L. 114       112  POP_BLOCK        
              114  LOAD_CONST               False
              116  RETURN_VALUE     
            118_0  COME_FROM_FINALLY     0  '0'

 L. 115       118  POP_TOP          
              120  POP_TOP          
              122  POP_TOP          

 L. 116       124  POP_EXCEPT       
              126  LOAD_CONST               False
              128  RETURN_VALUE     
              130  END_FINALLY      

Parse error at or near `LOAD_CONST' instruction at offset 26

    def mergerByM3u8_Multithreading--- This code section failed: ---

 L. 127       0_2  SETUP_FINALLY       266  'to 266'

 L. 129         4  LOAD_FAST                'self'
                6  LOAD_METHOD              _FFmpegTool__parseM3u8
                8  LOAD_FAST                'url'
               10  CALL_METHOD_1         1  ''
               12  STORE_FAST               'urllist'

 L. 130        14  LOAD_GLOBAL              len
               16  LOAD_FAST                'urllist'
               18  CALL_FUNCTION_1       1  ''
               20  LOAD_CONST               0
               22  COMPARE_OP               <=
               24  POP_JUMP_IF_FALSE    32  'to 32'

 L. 131        26  POP_BLOCK        
               28  LOAD_CONST               False
               30  RETURN_VALUE     
             32_0  COME_FROM            24  '24'

 L. 134        32  LOAD_GLOBAL              pathHelper
               34  LOAD_METHOD              getDirName
               36  LOAD_FAST                'filepath'
               38  CALL_METHOD_1         1  ''
               40  STORE_FAST               'path'

 L. 135        42  LOAD_GLOBAL              pathHelper
               44  LOAD_METHOD              getDiffTmpPathName
               46  LOAD_FAST                'path'
               48  CALL_METHOD_1         1  ''
               50  STORE_FAST               'tmpPath'

 L. 136        52  LOAD_GLOBAL              pathHelper
               54  LOAD_METHOD              mkdirs
               56  LOAD_FAST                'tmpPath'
               58  CALL_METHOD_1         1  ''
               60  LOAD_CONST               False
               62  COMPARE_OP               is
               64  POP_JUMP_IF_FALSE    72  'to 72'

 L. 137        66  POP_BLOCK        
               68  LOAD_CONST               False
               70  RETURN_VALUE     
             72_0  COME_FROM            64  '64'

 L. 140        72  LOAD_CONST               None
               74  LOAD_FAST                'self'
               76  STORE_ATTR               progress

 L. 141        78  LOAD_FAST                'showprogress'
               80  POP_JUMP_IF_FALSE    96  'to 96'

 L. 142        82  LOAD_GLOBAL              ProgressTool
               84  LOAD_GLOBAL              len
               86  LOAD_FAST                'urllist'
               88  CALL_FUNCTION_1       1  ''
               90  CALL_FUNCTION_1       1  ''
               92  LOAD_FAST                'self'
               94  STORE_ATTR               progress
             96_0  COME_FROM            80  '80'

 L. 145        96  BUILD_LIST_0          0 
               98  STORE_FAST               'allpath'

 L. 146       100  LOAD_GLOBAL              len
              102  LOAD_FAST                'urllist'
              104  CALL_FUNCTION_1       1  ''
              106  LOAD_FAST                'self'
              108  STORE_ATTR               waitCount

 L. 147       110  LOAD_CONST               0
              112  LOAD_FAST                'self'
              114  STORE_ATTR               completeCount

 L. 148       116  LOAD_GLOBAL              enumerate
              118  LOAD_FAST                'urllist'
              120  CALL_FUNCTION_1       1  ''
              122  GET_ITER         
              124  FOR_ITER            226  'to 226'
              126  UNPACK_SEQUENCE_2     2 
              128  STORE_FAST               'i'
              130  STORE_FAST               'item'

 L. 149       132  LOAD_FAST                'i'
              134  LOAD_CONST               100001
              136  BINARY_ADD       
              138  STORE_FAST               'index'

 L. 150       140  LOAD_FAST                'tmpPath'
              142  LOAD_STR                 '/'
              144  BINARY_ADD       
              146  LOAD_GLOBAL              str
              148  LOAD_FAST                'index'
              150  CALL_FUNCTION_1       1  ''
              152  BINARY_ADD       
              154  LOAD_STR                 '.ts'
              156  BINARY_ADD       
              158  STORE_FAST               'path'

 L. 151       160  LOAD_GLOBAL              os
              162  LOAD_ATTR                path
              164  LOAD_METHOD              abspath
              166  LOAD_FAST                'path'
              168  CALL_METHOD_1         1  ''
              170  STORE_FAST               'path'

 L. 152       172  LOAD_FAST                'allpath'
              174  LOAD_METHOD              append
              176  LOAD_FAST                'path'
              178  CALL_METHOD_1         1  ''
              180  POP_TOP          

 L. 153       182  LOAD_GLOBAL              os
              184  LOAD_ATTR                path
              186  LOAD_METHOD              exists
              188  LOAD_FAST                'path'
              190  CALL_METHOD_1         1  ''
              192  POP_JUMP_IF_FALSE   204  'to 204'

 L. 154       194  LOAD_GLOBAL              os
              196  LOAD_METHOD              remove
              198  LOAD_FAST                'path'
              200  CALL_METHOD_1         1  ''
              202  POP_TOP          
            204_0  COME_FROM           192  '192'

 L. 155       204  LOAD_FAST                'self'
              206  LOAD_ATTR                thread
              208  LOAD_METHOD              start
              210  LOAD_FAST                'self'
              212  LOAD_ATTR                _FFmpegTool__thradfunc_dl
              214  LOAD_FAST                'item'
              216  LOAD_FAST                'path'
              218  LOAD_CONST               3
              220  CALL_METHOD_4         4  ''
              222  POP_TOP          
              224  JUMP_BACK           124  'to 124'

 L. 156       226  LOAD_FAST                'self'
              228  LOAD_ATTR                thread
              230  LOAD_METHOD              waitAll
              232  CALL_METHOD_0         0  ''
              234  POP_TOP          

 L. 157       236  LOAD_FAST                'self'
              238  LOAD_METHOD              mergerByTs
              240  LOAD_FAST                'tmpPath'
              242  LOAD_FAST                'filepath'
              244  LOAD_FAST                'showshell'
              246  CALL_METHOD_3         3  ''
              248  STORE_FAST               'ret'

 L. 159       250  LOAD_GLOBAL              shutil
              252  LOAD_METHOD              rmtree
              254  LOAD_FAST                'tmpPath'
              256  CALL_METHOD_1         1  ''
              258  POP_TOP          

 L. 160       260  LOAD_FAST                'ret'
              262  POP_BLOCK        
              264  RETURN_VALUE     
            266_0  COME_FROM_FINALLY     0  '0'

 L. 161       266  POP_TOP          
              268  POP_TOP          
              270  POP_TOP          

 L. 162       272  POP_EXCEPT       
              274  LOAD_CONST               False
              276  RETURN_VALUE     
              278  END_FINALLY      

Parse error at or near `LOAD_CONST' instruction at offset 28

    def mergerByM3u8(self, url, filepath, showshell=False):
        """
        #Func    :   合并文件(使用M3u8的url)        
        #Param   :   url         [in] 链接       
        #Param   :   filepath    [in] 目标文件名            
        #Param   :   showshell   [in] 是否显示cmd信息              
        #Return  :   True/False 
        """
        res = -1
        try:
            filepath = os.path.abspath(filepath)
            cmd = 'ffmpeg -safe 0 -i ' + url + ' -c copy -bsf:a aac_adtstoasc "' + filepath + '"'
            res = self._FFmpegTool__processcmd3showshellfilepath
        except:
            pass
        else:
            return res

    def mergerByTs(self, srcDir, filepath, showshell=False):
        srcDir = os.path.abspath(srcDir)
        filepath = os.path.abspath(filepath)
        if os.path.exists(srcDir) is False:
            return False
        else:
            exten = pathHelper.getFileExtension(filepath)
            tmppath = filepath.replace(exten, '.ts')
            if systemHelper.isWindows():
                srcDir += '\\*.ts'
                cmd = 'copy /b "' + srcDir + '" "' + tmppath + '"'
            else:
                srcDir += '/*.ts'
            cmd = 'cat ' + srcDir + ' > "' + tmppath + '"'
        ret = self._FFmpegTool__processcmd3showshelltmppath
        if ret is True:
            cmd = 'ffmpeg -i "' + tmppath + '" -c copy "' + filepath + '"'
            ret = self._FFmpegTool__processcmd3showshellfilepath
        pathHelper.remove(tmppath)
        return ret

    def mergerByTsfiles(self, srcfilepaths, filepath, showshell=False):
        """
        #Func    :   合并ts文件             
        #Return  :   True/False         
        """
        filepath = os.path.abspath(filepath)
        exten = pathHelper.getFileExtension(filepath)
        tmppath = filepath.replace(exten, '.ts')
        tmppath2 = filepath.replace(exten, '2.ts')
        array = [srcfilepaths[i:i + 25] for i in range(0, len(srcfilepaths), 25)]
        pathHelper.remove(tmppath)
        pathHelper.remove(tmppath2)
        for item in array:
            for index, file in enumerate(item):
                item[index] = '"' + file + '"'

            form = ' + '.join(item)
            if os.access(tmppath, 0):
                form = '"' + tmppath + '" + ' + form
            cmd = 'copy /b ' + form + ' "' + tmppath2 + '"'
            ret = self._FFmpegTool__processcmd3showshelltmppath2
            if ret is False:
                break
            pathHelper.remove(tmppath)
            os.rename(tmppath2, tmppath)

        if ret is True:
            cmd = 'ffmpeg -i "' + tmppath + '" -c copy "' + filepath + '"'
            ret = self._FFmpegTool__processcmd3showshellfilepath
        pathHelper.remove(tmppath)
        pathHelper.remove(tmppath2)
        return ret

    def _checkTool(self):
        check = False
        try:
            cmd = 'ffmpeg -V'
            stdoutFile = 'ffmpegcheck-stdout.txt'
            fp = openstdoutFile'w'
            if sys.version_info[0] > 2:
                res = subprocess.call(cmd, timeout=(self.mergerTimeout), shell=True, stdout=fp, stderr=fp)
            else:
                res = subprocess.call(cmd, shell=True, stdout=fp, stderr=fp)
            fp.close()
            txt = fileHelper.getFileContent(stdoutFile)
            if 'version' in txt:
                if 'Copyright' in txt:
                    check = True
        except:
            pass
        else:
            pathHelper.remove(stdoutFile)
            return check

    def covertFile--- This code section failed: ---

 L. 257         0  SETUP_FINALLY        70  'to 70'

 L. 258         2  LOAD_GLOBAL              os
                4  LOAD_ATTR                path
                6  LOAD_METHOD              abspath
                8  LOAD_FAST                'srcfile'
               10  CALL_METHOD_1         1  ''
               12  STORE_FAST               'filepath'

 L. 259        14  LOAD_GLOBAL              os
               16  LOAD_ATTR                path
               18  LOAD_METHOD              abspath
               20  LOAD_FAST                'descfile'
               22  CALL_METHOD_1         1  ''
               24  STORE_FAST               'filepath2'

 L. 260        26  LOAD_STR                 'ffmpeg -i "'
               28  LOAD_FAST                'filepath'
               30  BINARY_ADD       
               32  LOAD_STR                 '" -c copy "'
               34  BINARY_ADD       
               36  LOAD_FAST                'filepath2'
               38  BINARY_ADD       
               40  LOAD_STR                 '"'
               42  BINARY_ADD       
               44  STORE_FAST               'cmd'

 L. 261        46  LOAD_FAST                'self'
               48  LOAD_METHOD              _FFmpegTool__process
               50  LOAD_FAST                'cmd'
               52  LOAD_CONST               3
               54  LOAD_FAST                'showshell'
               56  LOAD_FAST                'filepath'
               58  LOAD_CONST               False
               60  CALL_METHOD_5         5  ''
               62  STORE_FAST               'ret'

 L. 262        64  LOAD_FAST                'ret'
               66  POP_BLOCK        
               68  RETURN_VALUE     
             70_0  COME_FROM_FINALLY     0  '0'

 L. 263        70  POP_TOP          
               72  POP_TOP          
               74  POP_TOP          

 L. 264        76  POP_EXCEPT       
               78  LOAD_CONST               False
               80  RETURN_VALUE     
               82  END_FINALLY      

Parse error at or near `POP_BLOCK' instruction at offset 66

    def mergerByFiles--- This code section failed: ---

 L. 274         0  LOAD_GLOBAL              os
                2  LOAD_ATTR                path
                4  LOAD_METHOD              abspath
                6  LOAD_FAST                'filepath'
                8  CALL_METHOD_1         1  ''
               10  STORE_FAST               'filepath'

 L. 275        12  LOAD_CONST               -1
               14  STORE_FAST               'res'

 L. 276        16  LOAD_FAST                'filepath'
               18  LOAD_STR                 'TMP.txt'
               20  BINARY_ADD       
               22  STORE_FAST               'tmpfile'

 L. 277        24  LOAD_DEREF               'srcfilepaths'
               26  STORE_FAST               'paths'

 L. 278        28  LOAD_CONST               None
               30  STORE_FAST               'group'

 L. 279        32  LOAD_CONST               50
               34  STORE_DEREF              'groupnum'

 L. 280     36_38  SETUP_FINALLY       308  'to 308'

 L. 282        40  LOAD_GLOBAL              len
               42  LOAD_DEREF               'srcfilepaths'
               44  CALL_FUNCTION_1       1  ''
               46  LOAD_DEREF               'groupnum'
               48  COMPARE_OP               >
               50  POP_JUMP_IF_FALSE   206  'to 206'

 L. 283        52  LOAD_GLOBAL              pathHelper
               54  LOAD_METHOD              getDirName
               56  LOAD_FAST                'filepath'
               58  CALL_METHOD_1         1  ''
               60  STORE_FAST               'dirName'

 L. 284        62  LOAD_GLOBAL              pathHelper
               64  LOAD_METHOD              getDiffTmpPathName
               66  LOAD_FAST                'dirName'
               68  CALL_METHOD_1         1  ''
               70  STORE_FAST               'group'

 L. 285        72  LOAD_GLOBAL              pathHelper
               74  LOAD_METHOD              mkdirs
               76  LOAD_FAST                'group'
               78  CALL_METHOD_1         1  ''
               80  LOAD_CONST               False
               82  COMPARE_OP               is
               84  POP_JUMP_IF_FALSE    92  'to 92'

 L. 286        86  POP_BLOCK        
               88  LOAD_CONST               False
               90  RETURN_VALUE     
             92_0  COME_FROM            84  '84'

 L. 288        92  BUILD_LIST_0          0 
               94  STORE_FAST               'newPaths'

 L. 289        96  LOAD_CLOSURE             'groupnum'
               98  LOAD_CLOSURE             'srcfilepaths'
              100  BUILD_TUPLE_2         2 
              102  LOAD_LISTCOMP            '<code_object <listcomp>>'
              104  LOAD_STR                 'FFmpegTool.mergerByFiles.<locals>.<listcomp>'
              106  MAKE_FUNCTION_8          'closure'
              108  LOAD_GLOBAL              range
              110  LOAD_CONST               0
              112  LOAD_GLOBAL              len
              114  LOAD_DEREF               'srcfilepaths'
              116  CALL_FUNCTION_1       1  ''
              118  LOAD_DEREF               'groupnum'
              120  CALL_FUNCTION_3       3  ''
              122  GET_ITER         
              124  CALL_FUNCTION_1       1  ''
              126  STORE_FAST               'array'

 L. 290       128  LOAD_GLOBAL              enumerate
              130  LOAD_FAST                'array'
              132  CALL_FUNCTION_1       1  ''
              134  GET_ITER         
            136_0  COME_FROM           190  '190'
              136  FOR_ITER            202  'to 202'
              138  UNPACK_SEQUENCE_2     2 
              140  STORE_FAST               'index'
              142  STORE_FAST               'item'

 L. 291       144  LOAD_FAST                'group'
              146  LOAD_STR                 '/'
              148  BINARY_ADD       
              150  LOAD_GLOBAL              str
              152  LOAD_FAST                'index'
              154  CALL_FUNCTION_1       1  ''
              156  BINARY_ADD       
              158  LOAD_STR                 '.mp4'
              160  BINARY_ADD       
              162  STORE_FAST               'file'

 L. 292       164  LOAD_FAST                'newPaths'
              166  LOAD_METHOD              append
              168  LOAD_FAST                'file'
              170  CALL_METHOD_1         1  ''
              172  POP_TOP          

 L. 293       174  LOAD_FAST                'self'
              176  LOAD_METHOD              mergerByFiles
              178  LOAD_FAST                'item'
              180  LOAD_FAST                'file'
              182  LOAD_FAST                'showshell'
              184  CALL_METHOD_3         3  ''
              186  LOAD_CONST               False
              188  COMPARE_OP               is
              190  POP_JUMP_IF_FALSE   136  'to 136'

 L. 294       192  POP_TOP          
              194  POP_BLOCK        
              196  LOAD_CONST               False
              198  RETURN_VALUE     
              200  JUMP_BACK           136  'to 136'

 L. 295       202  LOAD_FAST                'newPaths'
              204  STORE_FAST               'paths'
            206_0  COME_FROM            50  '50'

 L. 298       206  LOAD_GLOBAL              open
              208  LOAD_FAST                'tmpfile'
              210  LOAD_STR                 'w'
              212  CALL_FUNCTION_2       2  ''
              214  SETUP_WITH          262  'to 262'
              216  STORE_FAST               'fd'

 L. 299       218  LOAD_FAST                'paths'
              220  GET_ITER         
              222  FOR_ITER            258  'to 258'
              224  STORE_FAST               'item'

 L. 300       226  LOAD_GLOBAL              os
              228  LOAD_ATTR                path
              230  LOAD_METHOD              abspath
              232  LOAD_FAST                'item'
              234  CALL_METHOD_1         1  ''
              236  STORE_FAST               'item'

 L. 301       238  LOAD_FAST                'fd'
              240  LOAD_METHOD              write
              242  LOAD_STR                 "file '"
              244  LOAD_FAST                'item'
              246  BINARY_ADD       
              248  LOAD_STR                 "'\n"
              250  BINARY_ADD       
              252  CALL_METHOD_1         1  ''
              254  POP_TOP          
              256  JUMP_BACK           222  'to 222'
              258  POP_BLOCK        
              260  BEGIN_FINALLY    
            262_0  COME_FROM_WITH      214  '214'
              262  WITH_CLEANUP_START
              264  WITH_CLEANUP_FINISH
              266  END_FINALLY      

 L. 305       268  LOAD_STR                 'ffmpeg -f concat -safe 0 -i "'
              270  LOAD_FAST                'tmpfile'
              272  BINARY_ADD       
              274  LOAD_STR                 '" -c copy "'
              276  BINARY_ADD       
              278  LOAD_FAST                'filepath'
              280  BINARY_ADD       
              282  LOAD_STR                 '"'
              284  BINARY_ADD       
              286  STORE_FAST               'cmd'

 L. 306       288  LOAD_FAST                'self'
              290  LOAD_METHOD              _FFmpegTool__process
              292  LOAD_FAST                'cmd'
              294  LOAD_CONST               3
              296  LOAD_FAST                'showshell'
              298  LOAD_FAST                'filepath'
              300  CALL_METHOD_4         4  ''
              302  STORE_FAST               'res'
              304  POP_BLOCK        
              306  JUMP_FORWARD        320  'to 320'
            308_0  COME_FROM_FINALLY    36  '36'

 L. 307       308  POP_TOP          
              310  POP_TOP          
              312  POP_TOP          

 L. 308       314  POP_EXCEPT       
              316  JUMP_FORWARD        320  'to 320'
              318  END_FINALLY      
            320_0  COME_FROM           316  '316'
            320_1  COME_FROM           306  '306'

 L. 310       320  LOAD_GLOBAL              os
              322  LOAD_METHOD              access
              324  LOAD_FAST                'tmpfile'
              326  LOAD_CONST               0
              328  CALL_METHOD_2         2  ''
          330_332  POP_JUMP_IF_FALSE   344  'to 344'

 L. 311       334  LOAD_GLOBAL              os
              336  LOAD_METHOD              remove
              338  LOAD_FAST                'tmpfile'
              340  CALL_METHOD_1         1  ''
              342  POP_TOP          
            344_0  COME_FROM           330  '330'

 L. 312       344  LOAD_FAST                'group'
              346  LOAD_CONST               None
              348  COMPARE_OP               is-not
          350_352  POP_JUMP_IF_FALSE   364  'to 364'

 L. 313       354  LOAD_GLOBAL              shutil
              356  LOAD_METHOD              rmtree
              358  LOAD_FAST                'group'
              360  CALL_METHOD_1         1  ''
              362  POP_TOP          
            364_0  COME_FROM           350  '350'

 L. 314       364  LOAD_FAST                'res'
              366  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `LOAD_CONST' instruction at offset 88

    def test(self):
        self._FFmpegTool__process'dir'3False'e:\\7\\Video\\1.ts'


# NOTE: have internal decompilation grammar errors.
# Use -t option to show full context.
# not in loop:
#	break
#      L.  48        40  BREAK_LOOP           44  'to 44'