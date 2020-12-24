# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python3.5/dist-packages/HdlLib/Graphics.py
# Compiled at: 2017-07-10 06:25:14
# Size of source mod 2**32: 2848 bytes
import os, sys, logging
from HdlLib import VHDLParser, Drawing

def DirectoryPath(Path):
    """
        raise error if path is no a directory
        """
    if os.path.isdir(Path):
        return os.path.abspath(Path)
        try:
            os.makedirs(Path)
        except:
            raise TypeError


def FilePath(Path):
    """
        raise error if path is no a directory
        """
    if os.path.isfile(Path):
        return os.path.abspath(os.path.normpath(os.path.expanduser(Path)))
    raise TypeError


def SetupParseOptions(SubParsers):
    """
        Parse argument options and do corresponding actions.
        """
    Parser = SubParsers.add_parser('synoptic', help='Synoptic synoptics of a VHDL entity in a Gtk window.')
    Parser.add_argument('file', action='store', type=FilePath, help='VHDL source file to be parsed as DUT (Design Under Test).')
    Parser.add_argument('-o', '--outputdir', action='store', type=DirectoryPath, help='Output directory (recursively create the folder when it does not exist. Default is current directory.', default=os.getcwd())
    Parser.set_defaults(func=Synoptic_Opt)
    return Parser


def Synoptic_Opt(Options):
    """wrapper for Synoptic function"""
    VHDLFilePath = Options.file
    if not os.path.isfile(VHDLFilePath):
        logging.error("[Synoptic] Given VHDL file '{0}' does not exist or is not a file.".format(VHDLFilePath))
        return False
    if not VHDLFilePath.lower().endswith('.vhd'):
        logging.error('[Synoptic] Given file does not have a VHDL extension.'.format(VHDLFilePath))
        return False
    for Mod in VHDLParser.ParseVHDL(VHDLFilePath):
        return Synoptic(Mod, OutputPath=Options.outputdir)


def Synoptic(Mod, OutputPath):
    """
        Parse VHDL file and generate image of its synoptic in the given directory.
        """
    ImagePNGPath = os.path.join(OutputPath, '{0}.png'.format(Mod.Name))
    Draw = Drawing.CairoDrawing()
    W, H = Draw.IP(Mod, Width=600, Height=400, Ratio=1)
    Draw.ToPNG(ImagePNGPath)
    if os.path.isfile(ImagePNGPath):
        logging.info("Image '{0}' successfully generated.".format(ImagePNGPath))
    else:
        logging.error("Image '{0}' generation failed.".format(ImagePNGPath))
    return ImagePNGPath