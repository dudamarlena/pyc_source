# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/springheel/springheelinit.py
# Compiled at: 2019-12-16 03:05:09
# Size of source mod 2**32: 5778 bytes
import sys, os, shutil
from distutils.dir_util import copy_tree

def initDir(output_path, dir_name):
    """
    Create a subdirectory in the output if it doesn't already exist.

    Parameters
    ----------
    output_path : str
        Path to the output folder.
    dir_name : str
        The name of the directory to create.
    Returns
    -------
    dir_path : str
        Path to the (new) directory.
    """
    dir_path = os.path.join(output_path, dir_name)
    if not os.path.exists(dir_path):
        os.mkdir(dir_path, mode=493)
        os.chmod(dir_path, mode=493)
    return dir_path


def makeOutput():
    """
    Create an output directory if it doesn't already exist.

    Returns
    -------
    c_path : str
        Current (root) path.
    output_path : str
        Path to the output directory.
    pages_path : str
        Path to the pages directory in output.
    assets_path : str
        Path to the assets directory in output.
    arrows_path : str
        Path to the navigation arrow directory in output.
    socialbuttons_path : str
        Path to the social media icon directory in output.
    """
    if not os.path.exists('output'):
        os.mkdir('output', mode=493)
        os.chmod('output', mode=493)
    c_path = os.path.abspath('.')
    output_path = os.path.abspath('output')
    pages_path = initDir(output_path, 'pages')
    assets_path = initDir(output_path, 'assets')
    arrows_path = initDir(output_path, 'arrows')
    socialbuttons_path = initDir(output_path, 'socialbuttons')
    templates_path = initDir(c_path, 'templates')
    input_path = initDir(c_path, 'input')
    return (
     c_path, output_path, pages_path, assets_path, arrows_path, socialbuttons_path)


def getTemplatesPath--- This code section failed: ---

 L.  89         0  SETUP_FINALLY        38  'to 38'

 L.  90         2  LOAD_GLOBAL              sys
                4  LOAD_ATTR                modules
                6  LOAD_STR                 'springheel'
                8  BINARY_SUBSCR    
               10  LOAD_ATTR                __path__
               12  LOAD_CONST               0
               14  BINARY_SUBSCR    
               16  STORE_FAST               'raw_springheel_path'

 L.  91        18  LOAD_GLOBAL              print
               20  LOAD_STR                 'Springheel directory found at {path}...'
               22  LOAD_ATTR                format
               24  LOAD_FAST                'raw_springheel_path'
               26  LOAD_CONST               ('path',)
               28  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
               30  CALL_FUNCTION_1       1  ''
               32  POP_TOP          
               34  POP_BLOCK        
               36  JUMP_FORWARD         68  'to 68'
             38_0  COME_FROM_FINALLY     0  '0'

 L.  92        38  DUP_TOP          
               40  LOAD_GLOBAL              KeyError
               42  COMPARE_OP               exception-match
               44  POP_JUMP_IF_FALSE    66  'to 66'
               46  POP_TOP          
               48  POP_TOP          
               50  POP_TOP          

 L.  93        52  LOAD_GLOBAL              print
               54  LOAD_STR                 'Could not initialize because the Springheel directory was not found, somehow. I have no idea how you are running this at all. File an issue with the full details, but I may take some time to get back to you.'
               56  CALL_FUNCTION_1       1  ''
               58  POP_TOP          

 L.  94        60  POP_EXCEPT       
               62  LOAD_CONST               False
               64  RETURN_VALUE     
             66_0  COME_FROM            44  '44'
               66  END_FINALLY      
             68_0  COME_FROM            36  '36'

 L.  96        68  LOAD_GLOBAL              os
               70  LOAD_ATTR                path
               72  LOAD_METHOD              join
               74  LOAD_FAST                'raw_springheel_path'
               76  LOAD_STR                 'templates'
               78  CALL_METHOD_2         2  ''
               80  STORE_FAST               'templates_path'

 L.  97        82  LOAD_FAST                'raw_springheel_path'
               84  LOAD_FAST                'templates_path'
               86  BUILD_TUPLE_2         2 
               88  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `LOAD_CONST' instruction at offset 62


def copyAssets():
    """
    Copy assets from Springheel's install directory to the current one.

    Returns
    -------
    templates_path : str
        The path to templates in Springheel's install directory.
    """
    raw_springheel_path, templates_path = getTemplatesPath()
    strings_path = os.path.join(templates_path, 'strings.json')
    print('Getting templates from {templates_path}...'.format(templates_path=templates_path))
    if os.path.exists(templates_path) == False:
        print('The Springheel module was found, but template files do not exist. Please make sure {templates_path} exists and try again.'.format(templates_path=templates_path))
        return False
    else:
        current_dir = os.getcwd()
        templates_o = os.path.join(current_dir, 'templates')
        print('Copying templates to {templates_output}...'.format(templates_output=templates_o))
        copy_tree(templates_path, templates_o)
        print('Copying strings file...')
        new_strings_path = os.path.join(current_dir, 'templates', 'strings.json')
        shutil.copy(strings_path, new_strings_path)
        print('Strings file copied from {old} to {new}.'.format(old=strings_path, new=new_strings_path))
        input_path = initDir(current_dir, 'input')
        o_conf = os.path.join(raw_springheel_path, 'conf.ini')
        n_conf = os.path.join(current_dir, 'conf.ini')
        if os.path.exists(n_conf) == False:
            try:
                confpy_path = shutil.copy(o_conf, n_conf)
            except FileNotFoundError:
                print("Couldn't find conf.ini in the Springheel install directory. Did you delete it somehow?")

        else:
            print('conf.ini already exists in output directory; not overwriting.')
    base_arrows_path = os.path.join(raw_springheel_path, 'arrows')
    arrows_path = initDir(current_dir, 'arrows')
    base_themes_path = os.path.join(raw_springheel_path, 'themes')
    themes_path = initDir(current_dir, 'themes')
    base_socialbuttons_path = os.path.join(raw_springheel_path, 'socialbuttons')
    socialbuttons_path = initDir(current_dir, 'socialbuttons')
    copy_tree(base_arrows_path, arrows_path)
    copy_tree(base_themes_path, themes_path)
    copy_tree(base_socialbuttons_path, socialbuttons_path)
    return templates_path