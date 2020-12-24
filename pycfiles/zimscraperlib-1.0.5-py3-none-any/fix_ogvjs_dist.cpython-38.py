# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/reg/src/zimscraperlib/src/zimscraperlib/fix_ogvjs_dist.py
# Compiled at: 2020-04-03 07:42:10
# Size of source mod 2**32: 5765 bytes
""" quick script to inject a function in ogv.js' -wasm.js scripts

    ogv.js dynamicaly loads .wasm scripts.
    it does it in two different manners, not always respecting its .base attribute
    .wasm scripts are binaries so they reside in /I/ inside ZIM files
    while javascript ones are in /-/.
    To easily circumvent this while keeping in working in HTML folder (no zim),
    we inject a `target=zim_fix_wasm_target(target)` in the -wasm.js files.
    We do it on the dist files as those files are not from the JS source of ogv.js
    but built with emscripten. Also, ogv.js toolchain is long to setup.

"""
import sys, inspect, logging, pathlib
logging.basicConfig(format='%(levelname)s:%(message)s', level=(logging.DEBUG))
logger = logging.getLogger(__name__)
generic_function_block = '\nif (typeof zim_fix_wasm_target === \'undefined\') {\n    IS_IN_ZIM = self.location.href.indexOf("/-/") != -1 || self.location.href.indexOf("/I/") != -1 || self.location.href.indexOf("/A/") != -1;\n    ZIM_IMG_NS = (IS_IN_ZIM) ? \'../../{extra_parent_jumps}../I/\' : \'\';\n    hasImageNamespacePrefix = function(target) { return target.indexOf("/I/") != -1; }\n    hasMetaNamespacePrefix = function(target) { return target.indexOf("/-/") != -1; }\n    changeNamespacePrefix = function(target, new_ns) { return target.replace("/-/", new_ns); }\n    zim_fix_wasm_target = function(target) {\n        console.debug("in-file zim_fix_wasm_target:", target);\n        if (!IS_IN_ZIM) {\n            console.debug("..not in zim");\n            return target;\n        }\n        if (hasImageNamespacePrefix(target)) {\n            // we already have a good path, leave it\n        }\n        else if (hasMetaNamespacePrefix(target)) {\n            // we have a prefix, just replace it\n            target = changeNamespacePrefix(target, "I");\n        }\n        else {\n            // we lack the prefix, add it\n            target = ZIM_IMG_NS + "{vendors_path}/ogvjs/" + target;\n        }\n        console.debug("..target:", target);\n        return target;\n    }\n  }\n\n'

def fix_source_dir--- This code section failed: ---

 L.  60         0  LOAD_GLOBAL              logger
                2  LOAD_METHOD              info
                4  LOAD_STR                 'about to add fix to ogv.js files to dynamicaly load wasm files in ZIM'
                6  CALL_METHOD_1         1  ''
                8  POP_TOP          

 L.  61        10  LOAD_GLOBAL              len
               12  LOAD_GLOBAL              pathlib
               14  LOAD_METHOD              Path
               16  LOAD_FAST                'dest_vendors_path'
               18  CALL_METHOD_1         1  ''
               20  LOAD_ATTR                parts
               22  CALL_FUNCTION_1       1  ''
               24  STORE_FAST               'parent_dir_count'

 L.  62        26  LOAD_GLOBAL              generic_function_block
               28  LOAD_METHOD              replace

 L.  63        30  LOAD_STR                 '{extra_parent_jumps}'

 L.  63        32  LOAD_STR                 '../'
               34  LOAD_FAST                'parent_dir_count'
               36  LOAD_CONST               1
               38  BINARY_SUBTRACT  
               40  BINARY_MULTIPLY  

 L.  62        42  CALL_METHOD_2         2  ''
               44  STORE_FAST               'function_block'

 L.  65        46  LOAD_GLOBAL              pathlib
               48  LOAD_METHOD              Path
               50  LOAD_FAST                'source_vendors_path'
               52  CALL_METHOD_1         1  ''
               54  STORE_FAST               'root'

 L.  66        56  LOAD_FAST                'root'
               58  LOAD_METHOD              joinpath
               60  LOAD_STR                 'ogvjs'
               62  CALL_METHOD_1         1  ''
               64  STORE_FAST               'ogvjs_path'

 L.  68        66  LOAD_CONST               ('ogv-decoder-audio-opus-wasm.js', 'ogv-decoder-audio-vorbis-wasm.js', 'ogv-decoder-video-av1-wasm.js', 'ogv-decoder-video-theora-wasm.js', 'ogv-decoder-video-vp8-wasm.js', 'ogv-decoder-video-vp9-wasm.js', 'ogv-demuxer-ogg-wasm.js', 'ogv-demuxer-webm-wasm.js')
               68  GET_ITER         
            70_72  FOR_ITER            378  'to 378'
               74  STORE_FAST               'fname'

 L.  81        76  LOAD_FAST                'ogvjs_path'
               78  LOAD_METHOD              joinpath
               80  LOAD_FAST                'fname'
               82  CALL_METHOD_1         1  ''
               84  STORE_FAST               'fpath'

 L.  83        86  LOAD_GLOBAL              open
               88  LOAD_FAST                'fpath'
               90  LOAD_STR                 'r'
               92  CALL_FUNCTION_2       2  ''
               94  SETUP_WITH          110  'to 110'
               96  STORE_FAST               'fp'

 L.  84        98  LOAD_FAST                'fp'
              100  LOAD_METHOD              read
              102  CALL_METHOD_0         0  ''
              104  STORE_FAST               'content'
              106  POP_BLOCK        
              108  BEGIN_FINALLY    
            110_0  COME_FROM_WITH       94  '94'
              110  WITH_CLEANUP_START
              112  WITH_CLEANUP_FINISH
              114  END_FINALLY      

 L.  85       116  LOAD_STR                 'zim_fix_wasm_target'
              118  LOAD_FAST                'content'
              120  COMPARE_OP               in
              122  POP_JUMP_IF_FALSE   146  'to 146'

 L.  86       124  LOAD_GLOBAL              logger
              126  LOAD_METHOD              info
              128  LOAD_STR                 'File `'
              130  LOAD_FAST                'fpath'
              132  FORMAT_VALUE          0  ''
              134  LOAD_STR                 '` is already fixed!'
              136  BUILD_STRING_3        3 
              138  CALL_METHOD_1         1  ''
              140  POP_TOP          

 L.  87       142  JUMP_BACK            70  'to 70'
              144  JUMP_FORWARD        164  'to 164'
            146_0  COME_FROM           122  '122'

 L.  89       146  LOAD_GLOBAL              logger
              148  LOAD_METHOD              info
              150  LOAD_STR                 'File `'
              152  LOAD_FAST                'fpath'
              154  FORMAT_VALUE          0  ''
              156  LOAD_STR                 '` needs to be fixed.'
              158  BUILD_STRING_3        3 
              160  CALL_METHOD_1         1  ''
              162  POP_TOP          
            164_0  COME_FROM           144  '144'

 L.  92       164  LOAD_FAST                'content'
              166  LOAD_METHOD              index
              168  LOAD_STR                 'var a;a'
              170  CALL_METHOD_1         1  ''
              172  STORE_FAST               'vara_pos'

 L.  93       174  LOAD_FAST                'content'
              176  LOAD_CONST               0
              178  LOAD_FAST                'vara_pos'
              180  BUILD_SLICE_2         2 
              182  BINARY_SUBSCR    
              184  STORE_FAST               'before'

 L.  94       186  LOAD_FAST                'content'
              188  LOAD_FAST                'vara_pos'
              190  LOAD_CONST               None
              192  BUILD_SLICE_2         2 
              194  BINARY_SUBSCR    
              196  STORE_FAST               'after'

 L.  96       198  LOAD_FAST                'before'
              200  LOAD_FAST                'function_block'
              202  LOAD_METHOD              replace
              204  LOAD_STR                 '{vendors_path}'
              206  LOAD_FAST                'dest_vendors_path'
              208  CALL_METHOD_2         2  ''
              210  BINARY_ADD       
              212  LOAD_FAST                'after'
              214  BINARY_ADD       

 L.  95       216  STORE_FAST               'content'

 L. 100       218  LOAD_FAST                'content'
              220  LOAD_METHOD              index
              222  LOAD_STR                 '.locateFile'
              224  CALL_METHOD_1         1  ''
              226  STORE_FAST               'locatefile_pos'

 L. 101       228  LOAD_FAST                'locatefile_pos'
              230  LOAD_FAST                'content'
              232  LOAD_FAST                'locatefile_pos'
              234  LOAD_CONST               None
              236  BUILD_SLICE_2         2 
              238  BINARY_SUBSCR    
              240  LOAD_METHOD              index
              242  LOAD_STR                 '}'
              244  CALL_METHOD_1         1  ''
              246  BINARY_ADD       
              248  STORE_FAST               'bracket_pos'

 L. 102       250  LOAD_FAST                'content'
              252  LOAD_CONST               0
              254  LOAD_FAST                'bracket_pos'
              256  BUILD_SLICE_2         2 
              258  BINARY_SUBSCR    
              260  STORE_FAST               'before'

 L. 103       262  LOAD_FAST                'content'
              264  LOAD_FAST                'bracket_pos'
              266  LOAD_CONST               None
              268  BUILD_SLICE_2         2 
              270  BINARY_SUBSCR    
              272  STORE_FAST               'after'

 L. 104       274  LOAD_FAST                'before'
              276  LOAD_CONST               None
              278  LOAD_CONST               None
              280  LOAD_CONST               -1
              282  BUILD_SLICE_3         3 
              284  BINARY_SUBSCR    
              286  LOAD_METHOD              index
              288  LOAD_STR                 '='
              290  CALL_METHOD_1         1  ''
              292  STORE_FAST               'equal_pos'

 L. 105       294  LOAD_FAST                'before'
              296  LOAD_CONST               None
              298  LOAD_CONST               None
              300  LOAD_CONST               -1
              302  BUILD_SLICE_3         3 
              304  BINARY_SUBSCR    
              306  LOAD_FAST                'equal_pos'
              308  LOAD_CONST               1
              310  BINARY_ADD       
              312  LOAD_FAST                'equal_pos'
              314  LOAD_CONST               2
              316  BINARY_ADD       
              318  BUILD_SLICE_2         2 
              320  BINARY_SUBSCR    
              322  STORE_FAST               'variable'

 L. 106       324  LOAD_STR                 ';{var}=zim_fix_wasm_target({var});'
              326  LOAD_ATTR                format
              328  LOAD_FAST                'variable'
              330  LOAD_CONST               ('var',)
              332  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
              334  STORE_FAST               'our_fix'

 L. 108       336  LOAD_GLOBAL              open
              338  LOAD_FAST                'fpath'
              340  LOAD_STR                 'w'
              342  CALL_FUNCTION_2       2  ''
              344  SETUP_WITH          370  'to 370'
              346  STORE_FAST               'fp'

 L. 109       348  LOAD_FAST                'fp'
              350  LOAD_METHOD              write
              352  LOAD_FAST                'before'
              354  LOAD_FAST                'our_fix'
              356  BINARY_ADD       
              358  LOAD_FAST                'after'
              360  BINARY_ADD       
              362  CALL_METHOD_1         1  ''
              364  POP_TOP          
              366  POP_BLOCK        
              368  BEGIN_FINALLY    
            370_0  COME_FROM_WITH      344  '344'
              370  WITH_CLEANUP_START
              372  WITH_CLEANUP_FINISH
              374  END_FINALLY      
              376  JUMP_BACK            70  'to 70'

 L. 111       378  LOAD_GLOBAL              logger
              380  LOAD_METHOD              info
              382  LOAD_STR                 'fixing videosjs-ogvjs.js'
              384  CALL_METHOD_1         1  ''
              386  POP_TOP          

 L. 112       388  LOAD_FAST                'root'
              390  LOAD_METHOD              joinpath
              392  LOAD_STR                 'videojs-ogvjs.js'
              394  CALL_METHOD_1         1  ''
              396  STORE_FAST               'plugin_path'

 L. 113       398  LOAD_GLOBAL              open
              400  LOAD_FAST                'plugin_path'
              402  LOAD_STR                 'r'
              404  CALL_FUNCTION_2       2  ''
              406  SETUP_WITH          422  'to 422'
              408  STORE_FAST               'fp'

 L. 114       410  LOAD_FAST                'fp'
              412  LOAD_METHOD              read
              414  CALL_METHOD_0         0  ''
              416  STORE_FAST               'content'
              418  POP_BLOCK        
              420  BEGIN_FINALLY    
            422_0  COME_FROM_WITH      406  '406'
              422  WITH_CLEANUP_START
              424  WITH_CLEANUP_FINISH
              426  END_FINALLY      

 L. 116       428  LOAD_FAST                'content'
              430  LOAD_METHOD              replace

 L. 117       432  LOAD_STR                 "_OGVLoader2['default'].base = options.base;"

 L. 118       434  LOAD_STR                 "_OGVLoader2['default'].base = ZIM_META_NS + options.base;"

 L. 116       436  CALL_METHOD_2         2  ''
              438  STORE_FAST               'content'

 L. 120       440  LOAD_FAST                'content'
              442  LOAD_METHOD              replace

 L. 121       444  LOAD_STR                 "return type.indexOf('/ogg') !== -1 ? 'maybe' : '';"

 L. 122       446  LOAD_STR                 "return (type.indexOf('/webm') !== -1 || type.indexOf('/ogg') !== -1) ? 'maybe' : '';"

 L. 120       448  CALL_METHOD_2         2  ''
              450  STORE_FAST               'content'

 L. 125       452  LOAD_GLOBAL              open
              454  LOAD_FAST                'plugin_path'
              456  LOAD_STR                 'w'
              458  CALL_FUNCTION_2       2  ''
              460  SETUP_WITH          478  'to 478'
              462  STORE_FAST               'fp'

 L. 126       464  LOAD_FAST                'fp'
              466  LOAD_METHOD              write
              468  LOAD_FAST                'content'
              470  CALL_METHOD_1         1  ''
              472  POP_TOP          
              474  POP_BLOCK        
              476  BEGIN_FINALLY    
            478_0  COME_FROM_WITH      460  '460'
              478  WITH_CLEANUP_START
              480  WITH_CLEANUP_FINISH
              482  END_FINALLY      

 L. 128       484  LOAD_GLOBAL              logger
              486  LOAD_METHOD              info
              488  LOAD_STR                 'hack video.min.js (TEMP FIX to work aroung Qt bug in reader)'
              490  CALL_METHOD_1         1  ''
              492  POP_TOP          

 L. 129       494  LOAD_FAST                'root'
              496  LOAD_METHOD              joinpath
              498  LOAD_STR                 'videojs'
              500  LOAD_STR                 'video.min.js'
              502  CALL_METHOD_2         2  ''
              504  STORE_FAST               'videojs_path'

 L. 130       506  LOAD_GLOBAL              open
              508  LOAD_FAST                'videojs_path'
              510  LOAD_STR                 'r'
              512  CALL_FUNCTION_2       2  ''
              514  SETUP_WITH          530  'to 530'
              516  STORE_FAST               'fp'

 L. 131       518  LOAD_FAST                'fp'
              520  LOAD_METHOD              read
              522  CALL_METHOD_0         0  ''
              524  STORE_FAST               'content'
              526  POP_BLOCK        
              528  BEGIN_FINALLY    
            530_0  COME_FROM_WITH      514  '514'
              530  WITH_CLEANUP_START
              532  WITH_CLEANUP_FINISH
              534  END_FINALLY      

 L. 133       536  LOAD_FAST                'content'
              538  LOAD_METHOD              replace
              540  LOAD_STR                 ';return 0!==e?(t='
              542  LOAD_STR                 ';return (0!==e || IS_IN_ZIM)?(t='
              544  CALL_METHOD_2         2  ''
              546  STORE_FAST               'content'

 L. 135       548  LOAD_GLOBAL              open
              550  LOAD_FAST                'videojs_path'
              552  LOAD_STR                 'w'
              554  CALL_FUNCTION_2       2  ''
              556  SETUP_WITH          574  'to 574'
              558  STORE_FAST               'fp'

 L. 136       560  LOAD_FAST                'fp'
              562  LOAD_METHOD              write
              564  LOAD_FAST                'content'
              566  CALL_METHOD_1         1  ''
              568  POP_TOP          
              570  POP_BLOCK        
              572  BEGIN_FINALLY    
            574_0  COME_FROM_WITH      556  '556'
              574  WITH_CLEANUP_START
              576  WITH_CLEANUP_FINISH
              578  END_FINALLY      

 L. 138       580  LOAD_GLOBAL              logger
              582  LOAD_METHOD              info
              584  LOAD_STR                 'all done.'
              586  CALL_METHOD_1         1  ''
              588  POP_TOP          

Parse error at or near `JUMP_FORWARD' instruction at offset 144


def run():
    args = sys.argv[1:]
    if not args:
        signature = inspect.signature(fix_source_dir)
        dvp = signature.parameters['dest_vendors_path']
        print(f"Usage: {sys.argv[0]} <source_vendors_path> [<dest_vendors_path>]")
        print('\t<source_vendors_path>\tpath to your folder containing ogvjs/videojs/videojs-ogvjs.')
        print(f"\t<dest_vendors_path>\trelative path to that folder in dest HTML. Defaults to `{dvp.default}`")
        sys.exit(1)
    return sys.exit(fix_source_dir(*args))


if __name__ == '__main__':
    run()