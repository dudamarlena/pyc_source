# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/travis/build/WellDone/pymomo/pymomo/config/site_scons/cfileparser.py
# Compiled at: 2015-03-19 14:45:48
from pycparser import parse_file, c_ast
import utilities

class FunctionDefinitionRecorder(c_ast.NodeVisitor):

    def __init__(self):
        self.defined_functions = []
        self.def_locations = []

    def visit_FuncDef(self, node):
        self.defined_functions.append(node.decl.name)
        self.def_locations.append(node.decl.coord)


class ParsedCFile:
    """
        An object allowing one to explore the AST of a C file.  The file is 
        parsed using pycparser and various convenience routines are given to
        speed access to certain parts of the file.  
        """

    def __init__(self, filepath, arch):
        self.filepath = filepath
        self.arch = arch
        self._parse_file()

    def _parse_file(self):
        """
                Preprocess and parse C file into an AST
                """
        args = utilities.build_includes(self.arch.includes())
        args.append('-mcpu=%s' % self.arch.property('chip'))
        args.append('-E')
        args.append('-D__attribute__(x)=')
        args.append('-D__extension__=')
        self.ast = parse_file(self.filepath, use_cpp=True, cpp_path='xc16-gcc', cpp_args=args)

    def defined_functions(self, criterion=lambda x: True):
        visitor = FunctionDefinitionRecorder()
        visitor.visit(self.ast)
        return filter(criterion, visitor.defined_functions)