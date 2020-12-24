# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/reg/src/nautilus/nautiluszim/utils.py
# Compiled at: 2020-01-31 09:32:36
# Size of source mod 2**32: 4948 bytes
import os, re, locale, gettext, colorsys, subprocess, PIL, iso639, requests, colorthief
from resizeimage import resizeimage
from .constants import ROOT_DIR
WGET_BINARY = os.getenv('WGET_BINARY', '/usr/bin/wget')

def save_file(url, fpath):
    """ download a binary file from its URL """
    req = requests.get(url)
    req.raise_for_status()
    if not fpath.parent.exists():
        fpath.parent.mkdir(exist_ok=True)
    with open(fpath, 'wb') as (fp):
        fp.write(req.content)


def save_large_file(url, fpath):
    """ download a binary file from its URL, using wget """
    subprocess.run([
     WGET_BINARY,
     '-t',
     '5',
     '--retry-connrefused',
     '--random-wait',
     '-O',
     str(fpath),
     '-c',
     url],
      check=True)


def get_colors(image_path, use_palette=True):
    """ (main, secondary) HTML color codes from an image path """

    def rgb_to_hex(r, g, b):
        """ hexadecimal HTML-friendly color code for RGB tuple """
        return ('#{}{}{}'.format)(*[str(hex(x)[2:]).zfill(2) for x in (r, g, b)]).upper()

    def solarize(r, g, b):
        h, l, s = colorsys.rgb_to_hls(float(r) / 256, float(g) / 256, float(b) / 256)
        r2, g2, b2 = [int(x * 256) for x in colorsys.hls_to_rgb(h, 0.95, s)]
        return (r2, g2, b2)

    ct = colorthief.ColorThief(image_path)
    if use_palette:
        palette = ct.get_palette(color_count=2, quality=1)
        mr, mg, mb = palette[0]
        sr, sg, sb = solarize(*palette[1])
    else:
        mr, mg, mb = ct.get_color(quality=1)
        sr, sg, sb = solarize(mr, mg, mb)
    return (rgb_to_hex(mr, mg, mb), rgb_to_hex(sr, sg, sb))


def resize_image(fpath, width, height=None, to=None, method='width'):
    """ resize an image file (dimensions)

        methods: width, height, cover """
    with open(str(fpath), 'rb') as (fp):
        with PIL.Image.open(fp) as (image):
            if method == 'width':
                resized = resizeimage.resize(method, image, width)
            else:
                if method == 'height':
                    resized = resizeimage.resize(method, image, height=height)
                else:
                    resized = resizeimage.resize(method, image, [width, height])
    kwargs = {'PNG': {'quality': 100}}
    (resized.save)(
     (str(to) if to is not None else fpath), (image.format), **kwargs.get(image.format))


def is_hex_color(text):
    """ whether supplied text is a valid hex-formated color code """
    return re.search('^#(?:[0-9a-fA-F]{3}){1,2}$', text)


def nicer_args_join(args):
    """ slightly better concateated list of subprocess args for display """
    nargs = args[0:1]
    for arg in args[1:]:
        nargs.append(arg if arg.startswith('-') else '"{}"'.format(arg))
    else:
        return ' '.join(nargs)


def get_language_details--- This code section failed: ---

 L. 116         0  LOAD_STR                 'zh-Hans'

 L. 117         2  LOAD_STR                 'zh'

 L. 118         4  LOAD_STR                 'Simplified Chinese'

 L. 119         6  LOAD_STR                 '简化字'

 L. 115         8  LOAD_CONST               ('code', 'iso-639-1', 'english', 'native')
               10  BUILD_CONST_KEY_MAP_4     4 

 L. 122        12  LOAD_STR                 'zh-Hant'

 L. 123        14  LOAD_STR                 'zh'

 L. 124        16  LOAD_STR                 'Traditional Chinese'

 L. 125        18  LOAD_STR                 '正體字'

 L. 121        20  LOAD_CONST               ('code', 'iso-639-1', 'english', 'native')
               22  BUILD_CONST_KEY_MAP_4     4 

 L. 127        24  LOAD_STR                 'iw'
               26  LOAD_STR                 'he'
               28  LOAD_STR                 'Hebrew'
               30  LOAD_STR                 'עברית'
               32  LOAD_CONST               ('code', 'iso-639-1', 'english', 'native')
               34  BUILD_CONST_KEY_MAP_4     4 

 L. 129        36  LOAD_STR                 'es-419'

 L. 130        38  LOAD_STR                 'es-419'

 L. 131        40  LOAD_STR                 'Spanish'

 L. 132        42  LOAD_STR                 'Español'

 L. 128        44  LOAD_CONST               ('code', 'iso-639-1', 'english', 'native')
               46  BUILD_CONST_KEY_MAP_4     4 

 L. 135        48  LOAD_STR                 'mul'

 L. 136        50  LOAD_STR                 'en'

 L. 137        52  LOAD_STR                 'Multiple Languages'

 L. 138        54  LOAD_STR                 'Multiple Languages'

 L. 134        56  LOAD_CONST               ('code', 'iso-639-1', 'english', 'native')
               58  BUILD_CONST_KEY_MAP_4     4 

 L. 114        60  LOAD_CONST               ('zh-Hans', 'zh-Hant', 'iw', 'es-419', 'multi')
               62  BUILD_CONST_KEY_MAP_5     5 
               64  STORE_FAST               'non_iso_langs'

 L. 142        66  SETUP_FINALLY       124  'to 124'

 L. 145        68  LOAD_FAST                'iso_639_3'
               70  LOAD_FAST                'non_iso_langs'
               72  LOAD_METHOD              keys
               74  CALL_METHOD_0         0  ''
               76  COMPARE_OP               in

 L. 144        78  POP_JUMP_IF_FALSE    90  'to 90'
               80  LOAD_FAST                'non_iso_langs'
               82  LOAD_METHOD              get
               84  LOAD_FAST                'iso_639_3'
               86  CALL_METHOD_1         1  ''
               88  JUMP_FORWARD        120  'to 120'
             90_0  COME_FROM            78  '78'

 L. 147        90  LOAD_FAST                'iso_639_3'

 L. 148        92  LOAD_GLOBAL              iso639
               94  LOAD_METHOD              to_iso639_1
               96  LOAD_FAST                'iso_639_3'
               98  CALL_METHOD_1         1  ''

 L. 149       100  LOAD_GLOBAL              iso639
              102  LOAD_METHOD              to_name
              104  LOAD_FAST                'iso_639_3'
              106  CALL_METHOD_1         1  ''

 L. 150       108  LOAD_GLOBAL              iso639
              110  LOAD_METHOD              to_native
              112  LOAD_FAST                'iso_639_3'
              114  CALL_METHOD_1         1  ''

 L. 146       116  LOAD_CONST               ('code', 'iso-639-1', 'english', 'native')
              118  BUILD_CONST_KEY_MAP_4     4 
            120_0  COME_FROM            88  '88'

 L. 143       120  POP_BLOCK        
              122  RETURN_VALUE     
            124_0  COME_FROM_FINALLY    66  '66'

 L. 153       124  DUP_TOP          
              126  LOAD_GLOBAL              iso639
              128  LOAD_ATTR                NonExistentLanguageError
              130  COMPARE_OP               exception-match
              132  POP_JUMP_IF_FALSE   158  'to 158'
              134  POP_TOP          
              136  POP_TOP          
              138  POP_TOP          

 L. 155       140  LOAD_FAST                'iso_639_3'

 L. 156       142  LOAD_FAST                'iso_639_3'

 L. 157       144  LOAD_FAST                'iso_639_3'

 L. 158       146  LOAD_FAST                'iso_639_3'

 L. 154       148  LOAD_CONST               ('code', 'iso_639_3', 'english', 'native')
              150  BUILD_CONST_KEY_MAP_4     4 
              152  ROT_FOUR         
              154  POP_EXCEPT       
              156  RETURN_VALUE     
            158_0  COME_FROM           132  '132'
              158  END_FINALLY      

Parse error at or near `POP_TOP' instruction at offset 136


def setlocale(locale_name):
    computed = locale.setlocale(locale.LC_ALL, (locale_name.split('.')[0], 'UTF-8'))
    gettext.bindtextdomain('messages', str(ROOT_DIR.joinpath('locale')))
    gettext.textdomain('messages')
    return computed