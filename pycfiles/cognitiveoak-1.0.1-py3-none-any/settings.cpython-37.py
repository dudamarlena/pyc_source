# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: C:/Users/HDi/Google Drive/ProgramCodes/Released/PyPI/cognitivegeo\cognitivegeo\src\core\settings.py
# Compiled at: 2019-12-05 17:01:42
# Size of source mod 2**32: 7510 bytes
import numpy as np, os, sys
__all__ = [
 'settings']
GUI = {}
GUI['Toolbar'] = {}
GUI['Toolbar']['Left'] = True
GUI['Toolbar']['Right'] = True
GUI['Toolbar']['Top'] = True
GUI['Toolbar']['Bottom'] = True
General = {}
General['RootPath'] = os.path.dirname(__file__)[:-15]
Visual = {}
Visual['Font'] = {}
Visual['Font']['Name'] = 'Times New Roman'
Visual['Font']['Color'] = 'Green'
Visual['Font']['Style'] = 'Normal'
Visual['Font']['Weight'] = 'Normal'
Visual['Font']['Size'] = 16
Visual['Line'] = {}
Visual['Line']['Color'] = 'Red'
Visual['Line']['Width'] = 3
Visual['Line']['Style'] = 'Solid'
Visual['Line']['MarkerStyle'] = 'None'
Visual['Line']['MarkerSize'] = 5
Visual['Image'] = {}
Visual['Image']['Colormap'] = 'Red-White-Blue'
Visual['Image']['Interpolation'] = 'Quadric'
Viewer = {}
Viewer['Viewer3D'] = {}
Viewer['Viewer3D']['GoHome'] = 'U'
Viewer['Viewer3D']['ViewFrom'] = {}
Viewer['Viewer3D']['ViewFrom']['Inline'] = 'I'
Viewer['Viewer3D']['ViewFrom']['Crossline'] = 'X'
Viewer['Viewer3D']['ViewFrom']['Z'] = 'Z'
Viewer['Player'] = {}
Viewer['Player']['First'] = 'A'
Viewer['Player']['Previous'] = 'S'
Viewer['Player']['Next'] = 'D'
Viewer['Player']['Last'] = 'F'
Viewer['Player']['Backward'] = 'Q'
Viewer['Player']['Forward'] = 'W'
Viewer['Player']['Pause'] = 'P'
Viewer['Player']['Interval'] = 1

def checkGUI--- This code section failed: ---

 L.  87         0  LOAD_GLOBAL              len
                2  LOAD_FAST                'gui'
                4  LOAD_METHOD              keys
                6  CALL_METHOD_0         0  ''
                8  CALL_FUNCTION_1       1  ''
               10  LOAD_CONST               1
               12  COMPARE_OP               <
               14  POP_JUMP_IF_FALSE    20  'to 20'

 L.  88        16  LOAD_CONST               False
               18  RETURN_VALUE     
             20_0  COME_FROM            14  '14'

 L.  89        20  LOAD_STR                 'Toolbar'
               22  LOAD_FAST                'gui'
               24  LOAD_METHOD              keys
               26  CALL_METHOD_0         0  ''
               28  COMPARE_OP               not-in
               30  POP_JUMP_IF_FALSE    36  'to 36'

 L.  90        32  LOAD_CONST               False
               34  RETURN_VALUE     
             36_0  COME_FROM            30  '30'

 L.  91        36  LOAD_GLOBAL              len
               38  LOAD_FAST                'gui'
               40  LOAD_STR                 'Toolbar'
               42  BINARY_SUBSCR    
               44  LOAD_METHOD              keys
               46  CALL_METHOD_0         0  ''
               48  CALL_FUNCTION_1       1  ''
               50  LOAD_CONST               1
               52  COMPARE_OP               <
               54  POP_JUMP_IF_FALSE    60  'to 60'

 L.  92        56  LOAD_CONST               False
               58  RETURN_VALUE     
             60_0  COME_FROM            54  '54'

 L.  93        60  LOAD_STR                 'Left'
               62  LOAD_FAST                'gui'
               64  LOAD_STR                 'Toolbar'
               66  BINARY_SUBSCR    
               68  LOAD_METHOD              keys
               70  CALL_METHOD_0         0  ''
               72  COMPARE_OP               not-in
               74  POP_JUMP_IF_TRUE    124  'to 124'

 L.  94        76  LOAD_STR                 'Right'
               78  LOAD_FAST                'gui'
               80  LOAD_STR                 'Toolbar'
               82  BINARY_SUBSCR    
               84  LOAD_METHOD              keys
               86  CALL_METHOD_0         0  ''
               88  COMPARE_OP               not-in
               90  POP_JUMP_IF_TRUE    124  'to 124'

 L.  95        92  LOAD_STR                 'Top'
               94  LOAD_FAST                'gui'
               96  LOAD_STR                 'Toolbar'
               98  BINARY_SUBSCR    
              100  LOAD_METHOD              keys
              102  CALL_METHOD_0         0  ''
              104  COMPARE_OP               not-in
              106  POP_JUMP_IF_TRUE    124  'to 124'

 L.  96       108  LOAD_STR                 'Bottom'
              110  LOAD_FAST                'gui'
              112  LOAD_STR                 'Toolbar'
              114  BINARY_SUBSCR    
              116  LOAD_METHOD              keys
              118  CALL_METHOD_0         0  ''
              120  COMPARE_OP               not-in
              122  POP_JUMP_IF_FALSE   128  'to 128'
            124_0  COME_FROM           106  '106'
            124_1  COME_FROM            90  '90'
            124_2  COME_FROM            74  '74'

 L.  97       124  LOAD_CONST               False
              126  RETURN_VALUE     
            128_0  COME_FROM           122  '122'

 L.  99       128  LOAD_CONST               True
              130  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `RETURN_VALUE' instruction at offset 130


def checkGeneral(general):
    """
    Check if the general setting good to use

    Args:
        general:    general setting dictionary

    Return:
        True or false
    """
    if len(general.keys) < 1:
        return False
    if 'RootPath' not in general.keys:
        return False
    if len(general['RootPath']) < 1:
        return False
    return True


def checkVisual--- This code section failed: ---

 L. 134         0  LOAD_GLOBAL              len
                2  LOAD_FAST                'visual'
                4  LOAD_METHOD              keys
                6  CALL_METHOD_0         0  ''
                8  CALL_FUNCTION_1       1  ''
               10  LOAD_CONST               1
               12  COMPARE_OP               <
               14  POP_JUMP_IF_FALSE    20  'to 20'

 L. 135        16  LOAD_CONST               False
               18  RETURN_VALUE     
             20_0  COME_FROM            14  '14'

 L. 137        20  LOAD_STR                 'Font'
               22  LOAD_FAST                'visual'
               24  LOAD_METHOD              keys
               26  CALL_METHOD_0         0  ''
               28  COMPARE_OP               not-in
               30  POP_JUMP_IF_FALSE    36  'to 36'

 L. 138        32  LOAD_CONST               False
               34  RETURN_VALUE     
             36_0  COME_FROM            30  '30'

 L. 139        36  LOAD_GLOBAL              len
               38  LOAD_FAST                'visual'
               40  LOAD_STR                 'Font'
               42  BINARY_SUBSCR    
               44  LOAD_METHOD              keys
               46  CALL_METHOD_0         0  ''
               48  CALL_FUNCTION_1       1  ''
               50  LOAD_CONST               1
               52  COMPARE_OP               <
               54  POP_JUMP_IF_FALSE    60  'to 60'

 L. 140        56  LOAD_CONST               False
               58  RETURN_VALUE     
             60_0  COME_FROM            54  '54'

 L. 141        60  LOAD_STR                 'Name'
               62  LOAD_FAST                'visual'
               64  LOAD_STR                 'Font'
               66  BINARY_SUBSCR    
               68  LOAD_METHOD              keys
               70  CALL_METHOD_0         0  ''
               72  COMPARE_OP               not-in
               74  POP_JUMP_IF_TRUE    140  'to 140'

 L. 142        76  LOAD_STR                 'Color'
               78  LOAD_FAST                'visual'
               80  LOAD_STR                 'Font'
               82  BINARY_SUBSCR    
               84  LOAD_METHOD              keys
               86  CALL_METHOD_0         0  ''
               88  COMPARE_OP               not-in
               90  POP_JUMP_IF_TRUE    140  'to 140'

 L. 143        92  LOAD_STR                 'Style'
               94  LOAD_FAST                'visual'
               96  LOAD_STR                 'Font'
               98  BINARY_SUBSCR    
              100  LOAD_METHOD              keys
              102  CALL_METHOD_0         0  ''
              104  COMPARE_OP               not-in
              106  POP_JUMP_IF_TRUE    140  'to 140'

 L. 144       108  LOAD_STR                 'Weight'
              110  LOAD_FAST                'visual'
              112  LOAD_STR                 'Font'
              114  BINARY_SUBSCR    
              116  LOAD_METHOD              keys
              118  CALL_METHOD_0         0  ''
              120  COMPARE_OP               not-in
              122  POP_JUMP_IF_TRUE    140  'to 140'

 L. 145       124  LOAD_STR                 'Size'
              126  LOAD_FAST                'visual'
              128  LOAD_STR                 'Font'
              130  BINARY_SUBSCR    
              132  LOAD_METHOD              keys
              134  CALL_METHOD_0         0  ''
              136  COMPARE_OP               not-in
              138  POP_JUMP_IF_FALSE   144  'to 144'
            140_0  COME_FROM           122  '122'
            140_1  COME_FROM           106  '106'
            140_2  COME_FROM            90  '90'
            140_3  COME_FROM            74  '74'

 L. 146       140  LOAD_CONST               False
              142  RETURN_VALUE     
            144_0  COME_FROM           138  '138'

 L. 148       144  LOAD_STR                 'Line'
              146  LOAD_FAST                'visual'
              148  LOAD_METHOD              keys
              150  CALL_METHOD_0         0  ''
              152  COMPARE_OP               not-in
              154  POP_JUMP_IF_FALSE   160  'to 160'

 L. 149       156  LOAD_CONST               False
              158  RETURN_VALUE     
            160_0  COME_FROM           154  '154'

 L. 150       160  LOAD_GLOBAL              len
              162  LOAD_FAST                'visual'
              164  LOAD_STR                 'Line'
              166  BINARY_SUBSCR    
              168  LOAD_METHOD              keys
              170  CALL_METHOD_0         0  ''
              172  CALL_FUNCTION_1       1  ''
              174  LOAD_CONST               1
              176  COMPARE_OP               <
              178  POP_JUMP_IF_FALSE   184  'to 184'

 L. 151       180  LOAD_CONST               False
              182  RETURN_VALUE     
            184_0  COME_FROM           178  '178'

 L. 152       184  LOAD_STR                 'Color'
              186  LOAD_FAST                'visual'
              188  LOAD_STR                 'Line'
              190  BINARY_SUBSCR    
              192  LOAD_METHOD              keys
              194  CALL_METHOD_0         0  ''
              196  COMPARE_OP               not-in
          198_200  POP_JUMP_IF_TRUE    274  'to 274'

 L. 153       202  LOAD_STR                 'Width'
              204  LOAD_FAST                'visual'
              206  LOAD_STR                 'Line'
              208  BINARY_SUBSCR    
              210  LOAD_METHOD              keys
              212  CALL_METHOD_0         0  ''
              214  COMPARE_OP               not-in
          216_218  POP_JUMP_IF_TRUE    274  'to 274'

 L. 154       220  LOAD_STR                 'Style'
              222  LOAD_FAST                'visual'
              224  LOAD_STR                 'Line'
              226  BINARY_SUBSCR    
              228  LOAD_METHOD              keys
              230  CALL_METHOD_0         0  ''
              232  COMPARE_OP               not-in
          234_236  POP_JUMP_IF_TRUE    274  'to 274'

 L. 155       238  LOAD_STR                 'MarkerStyle'
              240  LOAD_FAST                'visual'
              242  LOAD_STR                 'Line'
              244  BINARY_SUBSCR    
              246  LOAD_METHOD              keys
              248  CALL_METHOD_0         0  ''
              250  COMPARE_OP               not-in
          252_254  POP_JUMP_IF_TRUE    274  'to 274'

 L. 156       256  LOAD_STR                 'MarkerSize'
              258  LOAD_FAST                'visual'
              260  LOAD_STR                 'Line'
              262  BINARY_SUBSCR    
              264  LOAD_METHOD              keys
              266  CALL_METHOD_0         0  ''
              268  COMPARE_OP               not-in
          270_272  POP_JUMP_IF_FALSE   278  'to 278'
            274_0  COME_FROM           252  '252'
            274_1  COME_FROM           234  '234'
            274_2  COME_FROM           216  '216'
            274_3  COME_FROM           198  '198'

 L. 157       274  LOAD_CONST               False
              276  RETURN_VALUE     
            278_0  COME_FROM           270  '270'

 L. 159       278  LOAD_STR                 'Image'
              280  LOAD_FAST                'visual'
              282  LOAD_METHOD              keys
              284  CALL_METHOD_0         0  ''
              286  COMPARE_OP               not-in
          288_290  POP_JUMP_IF_FALSE   296  'to 296'

 L. 160       292  LOAD_CONST               False
              294  RETURN_VALUE     
            296_0  COME_FROM           288  '288'

 L. 161       296  LOAD_GLOBAL              len
              298  LOAD_FAST                'visual'
              300  LOAD_STR                 'Image'
              302  BINARY_SUBSCR    
              304  LOAD_METHOD              keys
              306  CALL_METHOD_0         0  ''
              308  CALL_FUNCTION_1       1  ''
              310  LOAD_CONST               1
              312  COMPARE_OP               <
          314_316  POP_JUMP_IF_FALSE   322  'to 322'

 L. 162       318  LOAD_CONST               False
              320  RETURN_VALUE     
            322_0  COME_FROM           314  '314'

 L. 163       322  LOAD_STR                 'Colormap'
              324  LOAD_FAST                'visual'
              326  LOAD_STR                 'Image'
              328  BINARY_SUBSCR    
              330  LOAD_METHOD              keys
              332  CALL_METHOD_0         0  ''
              334  COMPARE_OP               not-in
          336_338  POP_JUMP_IF_FALSE   344  'to 344'

 L. 164       340  LOAD_CONST               False
              342  RETURN_VALUE     
            344_0  COME_FROM           336  '336'

 L. 165       344  LOAD_STR                 'Interpolation'
              346  LOAD_FAST                'visual'
              348  LOAD_STR                 'Image'
              350  BINARY_SUBSCR    
              352  LOAD_METHOD              keys
              354  CALL_METHOD_0         0  ''
              356  COMPARE_OP               not-in
          358_360  POP_JUMP_IF_FALSE   366  'to 366'

 L. 166       362  LOAD_CONST               False
              364  RETURN_VALUE     
            366_0  COME_FROM           358  '358'

 L. 168       366  LOAD_CONST               True
              368  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `RETURN_VALUE' instruction at offset 368


def checkViewer(viewer):
    """
    Check if the Viewer setting good to use

    Args:
        viewer: Viewer setting dictionary

    Return:
        True or false
    """
    if len(viewer.keys) < 1:
        return False
    if 'Viewer3D' not in viewer.keys:
        return False
    if len(viewer['Viewer3D'].keys) < 1:
        return False
    if 'GoHome' not in viewer['Viewer3D'].keys:
        return False
    if 'ViewFrom' not in viewer['Viewer3D'].keys:
        return False
    if len(viewer['Viewer3D']['ViewFrom'].keys) < 1:
        return False
    if 'Inline' not in viewer['Viewer3D']['ViewFrom'].keys:
        return False
    if 'Crossline' not in viewer['Viewer3D']['ViewFrom'].keys:
        return False
    if 'Z' not in viewer['Viewer3D']['ViewFrom'].keys:
        return False
    if 'Player' not in viewer.keys:
        return False
    if len(viewer['Player'].keys) < 1:
        return False
    if 'First' not in viewer['Player'].keys:
        return False
    if 'Previous' not in viewer['Player'].keys:
        return False
    if 'Next' not in viewer['Player'].keys:
        return False
    if 'Last' not in viewer['Player'].keys:
        return False
    if 'Backward' not in viewer['Player'].keys:
        return False
    if 'Forward' not in viewer['Player'].keys:
        return False
    if 'Pause' not in viewer['Player'].keys:
        return False
    if 'Interval' not in viewer['Player'].keys:
        return False
    return True


def checkSettings--- This code section failed: ---

 L. 237         0  LOAD_GLOBAL              checkGUI
                2  LOAD_FAST                'gui'
                4  CALL_FUNCTION_1       1  ''
                6  LOAD_CONST               False
                8  COMPARE_OP               is
               10  POP_JUMP_IF_TRUE     48  'to 48'

 L. 238        12  LOAD_GLOBAL              checkGeneral
               14  LOAD_FAST                'general'
               16  CALL_FUNCTION_1       1  ''
               18  LOAD_CONST               False
               20  COMPARE_OP               is
               22  POP_JUMP_IF_TRUE     48  'to 48'

 L. 239        24  LOAD_GLOBAL              checkVisual
               26  LOAD_FAST                'visual'
               28  CALL_FUNCTION_1       1  ''
               30  LOAD_CONST               False
               32  COMPARE_OP               is
               34  POP_JUMP_IF_TRUE     48  'to 48'

 L. 240        36  LOAD_GLOBAL              checkViewer
               38  LOAD_FAST                'viewer'
               40  CALL_FUNCTION_1       1  ''
               42  LOAD_CONST               False
               44  COMPARE_OP               is
               46  POP_JUMP_IF_FALSE    52  'to 52'
             48_0  COME_FROM            34  '34'
             48_1  COME_FROM            22  '22'
             48_2  COME_FROM            10  '10'

 L. 241        48  LOAD_CONST               False
               50  RETURN_VALUE     
             52_0  COME_FROM            46  '46'

 L. 243        52  LOAD_CONST               True
               54  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `RETURN_VALUE' instruction at offset 54


class settings:
    GUI = GUI
    General = General
    Visual = Visual
    Viewer = Viewer
    checkGUI = checkGUI
    checkGeneral = checkGeneral
    checkVisual = checkVisual
    checkViewer = checkViewer
    Settings = {}
    Settings['General'] = General
    Settings['Gui'] = GUI
    Settings['Visual'] = Visual
    Settings['Viewer'] = Viewer
    checkSettings = checkSettings