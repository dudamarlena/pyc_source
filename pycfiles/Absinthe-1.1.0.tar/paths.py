# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.6-x86_64/egg/TAMO/paths.py
# Compiled at: 2019-04-23 02:08:32
__doc__ = '\nTAMO.paths: Path information for TAMO Bioninformatics Modules\n\n   NOTE: When adding entries, append a "/" to directory names\n   to facilitate TAMO.paths.variable + "filename" convention\n\n   Instructions for downloading Motif Discovery Programs\n   (AlignACE, MEME, & MDscan) can be found near the end\n   of the file.\n\nCopyright (2005) Whitehead Institute for Biomedical Research\nAll Rights Reserved\nAuthor: David Benjamin Gordon\n\n'
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