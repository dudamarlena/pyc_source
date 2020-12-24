# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-x86_64/egg/TAMO/paths.py
# Compiled at: 2019-04-23 02:08:32
"""
TAMO.paths: Path information for TAMO Bioninformatics Modules

   NOTE: When adding entries, append a "/" to directory names
   to facilitate TAMO.paths.variable + "filename" convention

   Instructions for downloading Motif Discovery Programs
   (AlignACE, MEME, & MDscan) can be found near the end
   of the file.

Copyright (2005) Whitehead Institute for Biomedical Research
All Rights Reserved
Author: David Benjamin Gordon

"""
import os, sys, TAMO.localpaths
TAMOroot = TAMO.localpaths.TAMOroot
TAMOdata = TAMO.localpaths.TAMOdata
THEMEroot = TAMOroot
FSAdir = TAMOdata + 'fsafiles/'
BGdir = TAMOdata + 'fsafiles/'
Whiteheaddir = TAMOdata + 'Whitehead/'
Yeast6kArraydir = Whiteheaddir + 'Yeast6kArray/'
Human13kArraydir = Whiteheaddir + 'Human13kArray/'
SGDdir = TAMOdata + 'SGD/'
HumanSeqdir = TAMOdata + 'HumanSeq/'
Novartisdir = TAMOdata + 'Novartis/'
Holstegedir = TAMOdata + 'Holstege/'
AlignACEdir = TAMOdata + 'MDprogs/alignace2004/'
MEMEdir = TAMOdata + 'MDprogs/meme.3.0.13/'
MDscandir = TAMOdata + 'MDprogs/MDscan/'
weblogodir = TAMOdata + 'weblogo/'

def CHECK(filelist, arg, note=''):
    """
    Check whether the files can be found in the expected locations.  If not,
    suggest how they might be retrieved.
    """
    if type(filelist) != type([]):
        filelist = [filelist]
    for file in filelist:
        if note:
            exceptiontxt = '\n   CANNOT FIND FILE %s\n   EXAMINE TAMO/paths.py ' % file
            exceptiontxt += 'FOR INFORMATION REGARDING %s' % note
            exceptiontxt += '   (If file does exist, check permissions on file and directory)'
        else:
            exceptiontxt = '   CANNOT FIND FILE %s\nINVOKE:\n\t    GetDataFiles.py --%s' % (file, arg)
            exceptiontxt += '\n   (If file does exist, check permissions on file and directory)'
        if not os.path.exists(file):
            raise Exception, exceptiontxt