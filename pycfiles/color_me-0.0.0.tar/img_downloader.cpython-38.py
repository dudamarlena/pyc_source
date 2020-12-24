# uncompyle6 version 3.6.7
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/test/img_downloader.py
# Compiled at: 2020-04-18 14:24:17
# Size of source mod 2**32: 1982 bytes
import requests, os
from tqdm import tqdm
from urllib.parse import urlparse
try:
    from bs4 import BeautifulSoup as bs
except ImportError:
    raise Exception('Please install bs4 package')
else:

    def is_valid(url):
        """
    Checks whether `url` is a valid URL.
    """
        parsed = urlparse(url)
        return bool(parsed.netloc) and bool(parsed.scheme)


    def get_all_images(url):
        """
    Returns all image URLs on a single `url`
    """
        soup = bs(requests.get(url).content, 'html.parser')
        filenames = [x.attrs.get('href') for x in soup.find_all('a') if x.attrs.get('href').__contains__('bmp')]
        urls = [os.path.join(url, filename) for filename in filenames]
        return urls


    def download_file--- This code section failed: ---

 L.  38         0  LOAD_GLOBAL              os
                2  LOAD_ATTR                path
                4  LOAD_METHOD              isdir
                6  LOAD_FAST                'pathname'
                8  CALL_METHOD_1         1  ''
               10  POP_JUMP_IF_TRUE     22  'to 22'

 L.  39        12  LOAD_GLOBAL              os
               14  LOAD_METHOD              makedirs
               16  LOAD_FAST                'pathname'
               18  CALL_METHOD_1         1  ''
               20  POP_TOP          
             22_0  COME_FROM            10  '10'

 L.  41        22  LOAD_GLOBAL              requests
               24  LOAD_ATTR                get
               26  LOAD_FAST                'url'
               28  LOAD_CONST               True
               30  LOAD_CONST               ('stream',)
               32  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
               34  STORE_FAST               'response'

 L.  43        36  LOAD_GLOBAL              int
               38  LOAD_FAST                'response'
               40  LOAD_ATTR                headers
               42  LOAD_METHOD              get
               44  LOAD_STR                 'Content-Length'
               46  LOAD_CONST               0
               48  CALL_METHOD_2         2  ''
               50  CALL_FUNCTION_1       1  ''
               52  STORE_FAST               'file_size'

 L.  45        54  LOAD_GLOBAL              os
               56  LOAD_ATTR                path
               58  LOAD_METHOD              join
               60  LOAD_FAST                'pathname'
               62  LOAD_FAST                'url'
               64  LOAD_METHOD              split
               66  LOAD_STR                 '/'
               68  CALL_METHOD_1         1  ''
               70  LOAD_CONST               -1
               72  BINARY_SUBSCR    
               74  CALL_METHOD_2         2  ''
               76  STORE_FAST               'filename'

 L.  47        78  LOAD_GLOBAL              tqdm
               80  LOAD_FAST                'response'
               82  LOAD_METHOD              iter_content
               84  LOAD_CONST               1024
               86  CALL_METHOD_1         1  ''
               88  LOAD_STR                 'Downloading '
               90  LOAD_FAST                'filename'
               92  FORMAT_VALUE          0  ''
               94  BUILD_STRING_2        2 
               96  LOAD_FAST                'file_size'
               98  LOAD_STR                 'B'
              100  LOAD_CONST               True
              102  LOAD_CONST               1024
              104  LOAD_CONST               ('total', 'unit', 'unit_scale', 'unit_divisor')
              106  CALL_FUNCTION_KW_6     6  '6 total positional and keyword args'
              108  STORE_FAST               'progress'

 L.  48       110  LOAD_GLOBAL              open
              112  LOAD_FAST                'filename'
              114  LOAD_STR                 'wb'
              116  CALL_FUNCTION_2       2  ''
              118  SETUP_WITH          160  'to 160'
              120  STORE_FAST               'f'

 L.  49       122  LOAD_FAST                'progress'
              124  GET_ITER         
              126  FOR_ITER            156  'to 156'
              128  STORE_FAST               'data'

 L.  51       130  LOAD_FAST                'f'
              132  LOAD_METHOD              write
              134  LOAD_FAST                'data'
              136  CALL_METHOD_1         1  ''
              138  POP_TOP          

 L.  53       140  LOAD_FAST                'progress'
              142  LOAD_METHOD              update
              144  LOAD_GLOBAL              len
              146  LOAD_FAST                'data'
              148  CALL_FUNCTION_1       1  ''
              150  CALL_METHOD_1         1  ''
              152  POP_TOP          
              154  JUMP_BACK           126  'to 126'
              156  POP_BLOCK        
              158  BEGIN_FINALLY    
            160_0  COME_FROM_WITH      118  '118'
              160  WITH_CLEANUP_START
              162  WITH_CLEANUP_FINISH
              164  END_FINALLY      

Parse error at or near `BEGIN_FINALLY' instruction at offset 158


    def download_stack(url, path):
        imgs = get_all_images(url)
        for img in imgs:
            download_file(img, path)


    if __name__ == '__main__':
        download_stack('https://www.math.purdue.edu/~lucier/PHOTO_CD/BMP_IMAGES/', os.path.join(os.getcwd(), 'data'))