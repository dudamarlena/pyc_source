# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python3.5/dist-packages/HdlLib/__init__.py
# Compiled at: 2017-07-08 08:29:58
# Size of source mod 2**32: 4368 bytes
__all__ = []
import os, sys, logging, argparse
try:
    import lxml
except:
    logging.error('[Dependency check] No module lxml found. Please install it (pip install lxml).')

from HdlLib.Utilities.ErrorHandlers import HdlLibError
from HdlLib import VHDLParser
from HdlLib.Utilities.ErrorHandlers import ParseError
from HdlLib import TBGen
from HdlLib import Graphics

def ParseVHDL(FilePath):
    """
        Generate a new Module instance from a given filepath and return it.
        """
    if FilePath is None or FilePath == '':
        raise HdlLibError("FilePath argument must not be empty (None or empty string). Given : '{0}'.".format(FilePath))
    try:
        ModuleList = VHDLParser.ParseVHDL(FilePath=FilePath)
        for M in ModuleList:
            M.Display()

        return ModuleList
    except ParseError:
        logging.error("The VHDL file couldn't be parsed. Please correct the detected errors and try again.")
        return


def LibGen_Opt(Opt):
    """
        Parse VHDL, add ports functions and generate XML from the module object.
        """
    VHDLFilePath = Opt.file
    if Opt.outputdir is None:
        OutputPath = os.path.dirname(VHDLFilePath)
    else:
        OutputPath = Opt.outputdir
    ModuleList = VHDLParser.ParseVHDL(FilePath=VHDLFilePath)
    if len(ModuleList) > 1:
        logging.warning("Found more than one entity in '{0}'".format(os.path.basename(VHDLFilePath)))
    XMLList = []
    for Mod in ModuleList:
        Mod.SetupPortsFunc()
        XMLList.append(Mod.DumpToFile(OutputPath=OutputPath))

    for XmlPath in XMLList:
        logging.info("Generated library file '{0}'".format(XmlPath))

    return XMLList


def FilePath(Path):
    """
        raise error if path is no a directory
        """
    if os.path.isfile(Path):
        return os.path.abspath(os.path.normpath(os.path.expanduser(Path)))
    raise TypeError


def DirectoryPath(Path):
    """
        raise error if path is no a directory
        """
    if os.path.isdir(Path):
        return os.path.abspath(Path)
    raise TypeError


def LibGen_SetupParseOptions(SubParsers):
    """
        Parse argument options to generate library files.
        """
    ArgParser = SubParsers.add_parser('addlib', help='Add VHDL entity to library by generating an XML file. By default, creates a folder in the VHDL source directory.')
    ArgParser.add_argument('file', action='store', type=FilePath, help='VHDL source file to be parsed as top module.')
    ArgParser.add_argument('-o', '--outputdir', action='store', type=DirectoryPath, help='Output directory (recursively create the folder when it does not exist). Default is current directory.', default=None)
    ArgParser.set_defaults(func=LibGen_Opt)
    return ArgParser


def StandAlone():
    sys.path.append(os.path.normpath(os.path.join(os.path.dirname(__file__), '..')))
    from HdlLib.Utilities import ConsoleInterface
    ConsoleInterface.ConfigLogging(Version='0.1', ModuleName='HdlLib')
    from HdlLib.Utilities import ColoredLogging
    ColoredLogging.SetActive(True)
    from HdlLib import TBGen, VHDLParser
    Parser = argparse.ArgumentParser(description='Manage VHDL sources for simulation, synthesis and more.', epilog='')
    SubParsers = Parser.add_subparsers(help='Library manager sub-commands.', dest='Sub-command')
    SubParsers.required = True
    TBGen.SetupParseOptions(SubParsers)
    VHDLParser.SetupParseOptions(SubParsers)
    Graphics.SetupParseOptions(SubParsers)
    LibGen_SetupParseOptions(SubParsers)
    Opt = Parser.parse_args()
    Opt.func(Opt)