# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/palpageproducer/__main__.py
# Compiled at: 2020-01-28 17:05:58
# Size of source mod 2**32: 11258 bytes
import sys, os, math
from slugify import slugify_url
from appdirs import *
name = 'palpageproducer'
author = 'gargargarrick'
__author__ = 'gargargarrick'
__version__ = '1.2.0'
__copyright__ = 'Copyright 2019-2020 Matthew Ellison'
__license__ = 'GPL'
__maintainer__ = 'gargargarrick'

def getFile():
    """Get the file to process."""
    if len(sys.argv) > 1:
        f = sys.argv[1]
    else:
        f = input('Path to the SASS/LESS/GPL/Oomox file? > ')
    f_abspath = os.path.abspath(f)
    return f_abspath


def openSass(sasspath):
    """Read from a SASS .scss file."""
    with open(sasspath, 'r') as (fin):
        sass_s = fin.read().splitlines()
    return sass_s


def openLess(lesspath):
    """Read from a LESS .less file."""
    with open(lesspath, 'r') as (fin):
        less_s = fin.read().splitlines()
    less_replaced = []
    for line in less_s:
        if line != '':
            line = line.strip()
            if line[0] == '@':
                newl = '${line}'.format(line=(line[1:]))
                less_replaced.append(newl)
        return less_replaced


def openOomox--- This code section failed: ---

 L.  63         0  LOAD_GLOBAL              open
                2  LOAD_FAST                'oomoxpath'
                4  LOAD_STR                 'r'
                6  CALL_FUNCTION_2       2  ''
                8  SETUP_WITH           28  'to 28'
               10  STORE_FAST               'fin'

 L.  64        12  LOAD_FAST                'fin'
               14  LOAD_METHOD              read
               16  CALL_METHOD_0         0  ''
               18  LOAD_METHOD              splitlines
               20  CALL_METHOD_0         0  ''
               22  STORE_FAST               'oomox_s'
               24  POP_BLOCK        
               26  BEGIN_FINALLY    
             28_0  COME_FROM_WITH        8  '8'
               28  WITH_CLEANUP_START
               30  WITH_CLEANUP_FINISH
               32  END_FINALLY      

 L.  65        34  BUILD_LIST_0          0 
               36  STORE_FAST               'oomox_replaced'

 L.  66        38  LOAD_FAST                'oomox_s'
               40  LOAD_CONST               0
               42  BINARY_SUBSCR    
               44  LOAD_CONST               0
               46  LOAD_CONST               9
               48  BUILD_SLICE_2         2 
               50  BINARY_SUBSCR    
               52  LOAD_STR                 'ACCENT_BG'
               54  COMPARE_OP               !=
               56  POP_JUMP_IF_FALSE    78  'to 78'

 L.  67        58  LOAD_GLOBAL              print
               60  LOAD_STR                 'palpageproducer thought {oomoxpath} was an oomox file, but it is not formatted like one. Please try again.'
               62  LOAD_ATTR                format
               64  LOAD_FAST                'oomoxpath'
               66  LOAD_CONST               ('oomoxpath',)
               68  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
               70  CALL_FUNCTION_1       1  ''
               72  POP_TOP          

 L.  68        74  LOAD_CONST               False
               76  RETURN_VALUE     
             78_0  COME_FROM            56  '56'

 L.  71        78  LOAD_STR                 'ARC_WIDGET_BORDER_COLOR'
               80  LOAD_STR                 'ICONS_ARCHDROID'
               82  LOAD_STR                 'ICONS_DARK'
               84  LOAD_STR                 'ICONS_LIGHT'
               86  LOAD_STR                 'ICONS_LIGHT_FOLDER'
               88  LOAD_STR                 'ICONS_MEDIUM'
               90  LOAD_STR                 'ICONS_SYMBOLIC_ACTION'
               92  LOAD_STR                 'ICONS_SYMBOLIC_PANEL'
               94  LOAD_STR                 'MENU_BG'
               96  LOAD_STR                 'MENU_FG'
               98  LOAD_STR                 'SURUPLUS_GRADIENT1'
              100  LOAD_STR                 'SURUPLUS_GRADIENT2'
              102  LOAD_STR                 'TERMINAL_ACCENT_COLOR'
              104  LOAD_STR                 'TERMINAL_BACKGROUND'
              106  LOAD_STR                 'TERMINAL_BASE_TEMPLATE'
              108  LOAD_STR                 'TERMINAL_COLOR0'
              110  LOAD_STR                 'TERMINAL_COLOR1'
              112  LOAD_STR                 'TERMINAL_COLOR2'
              114  LOAD_STR                 'TERMINAL_COLOR3'
              116  LOAD_STR                 'TERMINAL_COLOR4'
              118  LOAD_STR                 'TERMINAL_COLOR5'
              120  LOAD_STR                 'TERMINAL_COLOR6'
              122  LOAD_STR                 'TERMINAL_COLOR7'
              124  LOAD_STR                 'TERMINAL_COLOR8'
              126  LOAD_STR                 'TERMINAL_COLOR9'
              128  LOAD_STR                 'TERMINAL_COLOR10'
              130  LOAD_STR                 'TERMINAL_COLOR11'
              132  LOAD_STR                 'TERMINAL_COLOR12'
              134  LOAD_STR                 'TERMINAL_COLOR13'
              136  LOAD_STR                 'TERMINAL_COLOR14'
              138  LOAD_STR                 'TERMINAL_COLOR15'
              140  LOAD_STR                 'TERMINAL_FOREGROUND'
              142  BUILD_LIST_32        32 
              144  STORE_FAST               'ignored_keys'

 L.  72       146  BUILD_LIST_0          0 
              148  STORE_FAST               'seen_colors'

 L.  73       150  LOAD_FAST                'oomox_s'
              152  GET_ITER         
              154  FOR_ITER            322  'to 322'
              156  STORE_FAST               'line'

 L.  74       158  LOAD_FAST                'line'
              160  LOAD_STR                 ''
              162  COMPARE_OP               ==
              164  POP_JUMP_IF_FALSE   168  'to 168'

 L.  75       166  JUMP_BACK           154  'to 154'
            168_0  COME_FROM           164  '164'

 L.  76       168  LOAD_FAST                'line'
              170  LOAD_METHOD              strip
              172  CALL_METHOD_0         0  ''
              174  STORE_FAST               'line'

 L.  77       176  LOAD_FAST                'line'
              178  LOAD_METHOD              split
              180  LOAD_STR                 '='
              182  CALL_METHOD_1         1  ''
              184  UNPACK_SEQUENCE_2     2 
              186  STORE_FAST               'k'
              188  STORE_FAST               'v'

 L.  79       190  LOAD_GLOBAL              len
              192  LOAD_FAST                'v'
              194  CALL_FUNCTION_1       1  ''
              196  LOAD_CONST               6
              198  COMPARE_OP               !=
              200  POP_JUMP_IF_FALSE   204  'to 204'

 L.  80       202  JUMP_BACK           154  'to 154'
            204_0  COME_FROM           200  '200'

 L.  81       204  SETUP_FINALLY       220  'to 220'

 L.  82       206  LOAD_GLOBAL              int
              208  LOAD_FAST                'v'
              210  LOAD_CONST               16
              212  CALL_FUNCTION_2       2  ''
              214  STORE_FAST               'vtest'
              216  POP_BLOCK        
              218  JUMP_FORWARD        244  'to 244'
            220_0  COME_FROM_FINALLY   204  '204'

 L.  83       220  DUP_TOP          
              222  LOAD_GLOBAL              ValueError
              224  COMPARE_OP               exception-match
              226  POP_JUMP_IF_FALSE   242  'to 242'
              228  POP_TOP          
              230  POP_TOP          
              232  POP_TOP          

 L.  84       234  POP_EXCEPT       
              236  JUMP_BACK           154  'to 154'
              238  POP_EXCEPT       
              240  JUMP_FORWARD        244  'to 244'
            242_0  COME_FROM           226  '226'
              242  END_FINALLY      
            244_0  COME_FROM           240  '240'
            244_1  COME_FROM           218  '218'

 L.  85       244  LOAD_FAST                'k'
              246  LOAD_FAST                'ignored_keys'
              248  COMPARE_OP               in
              250  POP_JUMP_IF_FALSE   254  'to 254'

 L.  86       252  JUMP_BACK           154  'to 154'
            254_0  COME_FROM           250  '250'

 L.  89       254  LOAD_FAST                'v'
              256  LOAD_FAST                'seen_colors'
              258  COMPARE_OP               in
          260_262  POP_JUMP_IF_FALSE   266  'to 266'

 L.  90       264  JUMP_BACK           154  'to 154'
            266_0  COME_FROM           260  '260'

 L.  91       266  LOAD_FAST                'seen_colors'
              268  LOAD_METHOD              append
              270  LOAD_FAST                'v'
              272  CALL_METHOD_1         1  ''
              274  POP_TOP          

 L.  92       276  LOAD_STR                 '$'
              278  LOAD_FAST                'k'
              280  LOAD_METHOD              lower
              282  CALL_METHOD_0         0  ''
              284  BINARY_ADD       
              286  STORE_FAST               'key_id'

 L.  93       288  LOAD_STR                 '#'
              290  LOAD_FAST                'v'
              292  BINARY_ADD       
              294  STORE_FAST               'value_c'

 L.  94       296  LOAD_STR                 '{key_id}: {value_c};'
              298  LOAD_ATTR                format
              300  LOAD_FAST                'key_id'
              302  LOAD_FAST                'value_c'
              304  LOAD_CONST               ('key_id', 'value_c')
              306  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              308  STORE_FAST               'newl'

 L.  95       310  LOAD_FAST                'oomox_replaced'
              312  LOAD_METHOD              append
              314  LOAD_FAST                'newl'
              316  CALL_METHOD_1         1  ''
              318  POP_TOP          
              320  JUMP_BACK           154  'to 154'

 L.  96       322  LOAD_FAST                'oomox_replaced'
              324  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `POP_EXCEPT' instruction at offset 238


def rgbToHex(rgb):
    """Convert RGB colors into hex."""
    r = int(rgb[0])
    g = int(rgb[1])
    b = int(rgb[2])
    h = '#{:02X}{:02X}{:02X}'.format(r, g, b)
    return h


def openGimp(gpl_f):
    """Open a GIMP .gpl palette and process it."""
    with open(gpl_f, 'r') as (fin):
        gpl_raw = fin.read()
    gpl_s = gpl_raw.split('\n')[4:]
    new = []
    for x in gpl_s:
        if x != None and x != '':
            pair = x.strip().split('\t', 1)
            rgb = pair[0]
            name = pair[1]
            rgb = ' '.join(rgb.split())
            rgb = tuple(rgb.split(' '))
            hex = rgbToHex(rgb)
            slugname = slugify_url(name, separator='_')
            finalu = '${name}: {hex}'.format(name=slugname,
              hex=hex)
            new.append(finalu)
        return new


def findDivisor(count):
    """Find divisors below 5 (for determining column count)"""
    foo = reversed(range(1, 6))
    for i in foo:
        if count % i == 0:
            return i


def getColumns(count):
    """Set the number of columns for the output."""
    columns = findDivisor(count)
    if columns == 1:
        columns = 5
        vw = '20'
    else:
        vw = str(int(100 // columns))
    return (
     vw, str(columns))


def wrapInTag(content, tag):
    """Wrap something in an HTML tag"""
    return '<{tag}>{content}</{tag}>'.format(tag=tag,
      content=content)


def getLuminance(hex):
    """Get the luminance of a hex color"""
    hex_nohash = hex.lstrip('#')
    if len(hex_nohash) == 3:
        hex_nohash = ''.join([item * 2 for item in hex_nohash])
    r, g, b = tuple((int(hex_nohash[i:i + 2], 16) for i in (0, 2, 4)))
    rgbs = [r, g, b]
    rgbgs = []
    for component in rgbs:
        if component <= 10:
            adjusted = component / 3294
        else:
            adjusted = (component / 269 + 0.0513) ** 2.4
        rgbgs.append(adjusted)
    else:
        lum = 0.2126 * rgbgs[0] + 0.7152 * rgbgs[1] + 0.0722 * rgbgs[2]
        return lum


def checkContrast(hex):
    """Check the contrast between a hex color and black"""
    foreground = 0.0
    background = getLuminance(hex)
    colors = [foreground, background]
    ratio = (max(colors) + 0.05) / (min(colors) + 0.05)
    return ratio


def main():
    """Read a stylesheet/palette and generate an HTML page."""
    save_path = os.path.join(user_data_dir(name, author), 'output')
    if not os.path.exists(save_path):
        os.makedirs(save_path)
    sass_f = getFile()
    sass_basename = os.path.basename(sass_f)
    sass_splitext = os.path.splitext(sass_basename)
    sass_noext = sass_splitext[0]
    sass_noext_safe = slugify_url(sass_noext, separator='_')
    if sass_splitext[1] == '.scss':
        sass = openSass(sass_f)
    else:
        if sass_splitext[1] == '.gpl':
            sass = openGimp(sass_f)
        else:
            if sass_splitext[1] == '.less':
                sass = openLess(sass_f)
            else:
                if sass_splitext[1] == '':
                    sass = openOomox(sass_f)
                else:
                    if sass == False:
                        return False
                    title = wrapInTag(tag='title', content=sass_basename)
                    h1 = wrapInTag(tag='h1', content=sass_basename)
                    really_colors = []
                    for color in sass:
                        color = color.strip()
                        color = color.strip(';')
                        if color != '' and color[0] == '$':
                            colorid, colorvalue = color.split(': ', 1)
                            if colorvalue[0] == '#':
                                really_colors.append(color)

                if colorvalue[0:3] == 'rgb' and colorvalue[0:4] != 'rgba':
                    norgb = colorvalue.strip('rgb()')
                    justrgb = norgb.split(', ')
                    hex = rgbToHex(justrgb)
                    really_colors.append('{colorid}: {hex}'.format(colorid=colorid,
                      hex=hex))
                    continue
                colors = len(really_colors)
                vw, columns = getColumns(colors)
                css_template = 'body {{box-sizing: border-box}} h1 {{margin: 0em}} main {{display: grid; grid-template-columns: repeat({columns}, 1fr); grid-auto-rows: {vw}vw; grid-gap: 1em}} .colorbox {{padding: 1em; margin: 0.5em; overflow: visible}} p {{margin: 0em}}'.format(columns=columns,
                  vw=vw)
                cssbox_template = '#{colorid} {{background-color: {colorvalue}; color: {borw}}}'
                html_header = ['<!DOCTYPE HTML>', '<html lang="zxx">', '<head>',
                 '<meta charset="utf-8">', title, '<style>', css_template]
                html_body = ['</style>', '</head>', '<body>', h1, '<main>']
                html_close = ['</main>', '</body>', '</html>', '']
                knownids = []
                knowncolors = []
                colorindex = 0
                for color in really_colors:
                    colorid, colorvalue = color.split(': ')
                    colorid = colorid[1:]
                    if colorid not in knownids:
                        knownids.append(colorid)
                        knowncolors.append(colorvalue)
                        contrast = checkContrast(colorvalue)
                        if contrast < 4.5:
                            borw = '#ffffff'
                        else:
                            borw = '#000000'
                        cssbox = cssbox_template.format(colorid=colorid,
                          colorvalue=colorvalue,
                          borw=borw)
                        html = '<div class="colorbox" id="{colorid}"><p>{colorid}: {colorvalue}</p></div>'.format(colorid=colorid,
                          colorvalue=colorvalue)
                        c = {'colorid':colorid,  'colorvalue':colorvalue,  'cssbox':cssbox, 
                         'html':html}
                        html_header.append(cssbox)
                        html_body.append(html)
                    elif colorid in knownids:
                        if colorvalue not in knowncolors:
                            colorid = '{colorid}{colorindex}'.format(colorid=colorid,
                              colorindex=(str(colorindex)))
                            colorindex += 1
                            contrast = checkContrast(colorvalue)
                            if contrast < 4.5:
                                borw = '#ffffff'
                            else:
                                borw = '#000000'
                            cssbox = cssbox_template.format(colorid=colorid,
                              colorvalue=colorvalue,
                              borw=borw)
                            html = '<div class="colorbox" id="{colorid}"><p>{colorid}: {colorvalue}</p></div>'.format(colorid=colorid,
                              colorvalue=colorvalue)
                            c = {'colorid':colorid, 
                             'colorvalue':colorvalue,  'cssbox':cssbox, 
                             'html':html}
                            html_header.append(cssbox)
                            html_body.append(html)
                        all_html_elements = html_header + html_body + html_close
                        html = '\n'.join(all_html_elements)
                        outname = '{noext}_palette.html'.format(noext=sass_noext_safe)
                        outpath = os.path.join(save_path, outname)
                        with open(outpath, 'w') as (fout):
                            fout.write(html)
                        print('Wrote {outpath}.'.format(outpath=outpath))


if __name__ == '__main__':
    main()
# NOTE: have internal decompilation grammar errors.
# Use -t option to show full context.
# not in loop:
#	continue
#                   386  CONTINUE            222  'to 222'