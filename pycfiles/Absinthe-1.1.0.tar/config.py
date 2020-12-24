# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.6-x86_64/egg/abseqPy/config.py
# Compiled at: 2019-06-27 02:13:06
__doc__ = '\n    Short description: Quality Control Analysis of Immunoglobulin Repertoire NGS (Paired-End MiSeq)    \n    Author: Monther Alhamdoosh    \n    Python Version: 2.7\n    Changes log: check git commits. \n'
import os, sys, re, platform

def _findWebLogo():
    r"""
    on unix systems, return the binary name 'weblogo'
    on windows systems, return the path to 'weblogo' script with "python" prefixed in front, EG
    "python c:\pythonN\Scripts\weblogo" (where N is 2 or 3, depending on the version of weblogo installed)

    if weblogo wasn't installed in PYTHONPATH, return 'None' (string) regardless of the OS

    :return: "weblogo" or "python c:\pythonN\Scripts\weblogo" depending on the operating system.
    Returns 'None" (string) if weblogo can't be located, regardless of the OS.
    """
    try:
        import weblogolib
        if platform.system() != 'Windows':
            return 'weblogo'
        path = weblogolib.__file__
        return ('python {}').format(re.sub('lib.*', 'Scripts\\weblogo', path))
    except:
        return 'None'


def _find_fastQC():
    """
    fastqc shebang does not work in windows, manually execute perl script using perl interpreter

    :return: "fastqc" or "perl <path>/<to>/<fastqc>" if OS is windows
    """
    if platform.system() == 'Windows':
        return 'perl ' + os.path.join(os.path.expandvars('$FASTQCROOT'), 'fastqc')
    else:
        return 'fastqc'


ABSEQROOT = os.path.abspath(os.path.dirname(__file__))
VERSION = '0.99.4'
EXTERNAL_DEP_DIR = '3rd_party'
CLUSTALOMEGA = 'clustalo'
FASTQC = _find_fastQC()
LEEHOM = 'leeHomMulti'
FLASH = 'flash'
PEAR = 'pear'
IGBLASTN = 'igblastn'
IGBLASTP = 'igblastp'
DEFAULT_TOP_CLONE_VALUE = 'inf'
DEFAULT_MERGER = 'leehom' if platform.system() != 'Windows' else 'flash'
DEFAULT_TASK = 'abundance'
WEBLOGO = _findWebLogo()
FR4_CONSENSUS = {'VH': 'WGQGTXVTVSS', 
   'VK': 'FGXGTKLEIK', 
   'VL': 'FGXGTKLTVL'}
FR4_CONSENSUS_DNA = {'VH': 'TGGGGCCAGGGCACCNNNGTGACCGTGAGCAGC', 
   'VK': 'TTTGGCCAGGGGACCAAGCTGGAGATCAAA', 
   'VL': 'TTCGGCGGAGGGACCAAGCTGACCGTCCTA'}
AUX_FOLDER = 'auxiliary'
HDF_FOLDER = 'hdf'
GB = 1073741824.0
if sys.platform == 'darwin' or platform.system() == 'Windows':
    from psutil import virtual_memory
    mem = virtual_memory()
    MEM_GB = mem.total / GB
else:
    tmp = os.sysconf('SC_PAGE_SIZE') * os.sysconf('SC_PHYS_PAGES')
    MEM_GB = tmp / GB