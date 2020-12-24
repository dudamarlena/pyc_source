# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/alanr/monitor/ctypesgen-davidjamesca/ctypesgen/ctypesgen/__init__.py
# Compiled at: 2019-08-18 21:39:19
# Size of source mod 2**32: 2249 bytes
__doc__ = "\nCtypesgencore is the module that contains the main body of ctypesgen - in fact,\nit contains everything but the command-line interface.\n\nctypesgen's job is divided into three steps:\n\nStep 1: Parse\n\nCtypesgen reads the input header files and parses them. It generates a list of\nfunction, variable, struct, union, enum, constant, typedef, and macro\ndescriptions from the input files. These descriptions are encapsulated as\nctypesgen.descriptions.Description objects.\n\nThe package ctypesgen.parser is responsible for the parsing stage.\n\nStep 2: Process\n\nCtypesgen processes the list of descriptions from the parsing stage. This is\nthe stage where ctypesgen resolves name conflicts and filters descriptions using\nthe regexes specified on the command line. Other processing steps take place\nat this stage, too. When processing is done, ctypesgen finalizes which\ndescriptions will be included in the output file.\n\nThe package ctypesgen.processor is responsible for the processing stage.\n\nStep 3: Print\n\nCtypesgen writes the descriptions to the output file, along with a header.\n\nThe package ctypesgen.printer is responsible for the printing stage.\n\nThere are three modules in ctypesgen that describe the format that the\nparser, processor, and printer modules use to pass information. They are:\n\n* descriptions: Classes to represent the descriptions.\n\n* ctypedecls: Classes to represent C types.\n\n* expressions: Classes to represent an expression in a language-independent\nformat.\n"
__all__ = [
 'parser',
 'processor',
 'printer',
 'descriptions',
 'ctypedescs',
 'expressions',
 'messages',
 'options',
 'version']
from . import parser
from . import processor
from . import printer_python
from . import version
try:
    from . import printer_json
except ImportError:
    pass

__version__ = version.VERSION.partition('-')[(-1)]
VERSION = __version__
from . import descriptions
from . import ctypedescs
from . import expressions
from . import messages
from . import options
printer = printer_python