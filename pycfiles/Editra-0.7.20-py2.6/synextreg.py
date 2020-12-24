# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/Editra/src/syntax/synextreg.py
# Compiled at: 2012-03-17 12:57:53
"""
FILE: synextreg.py
LANGUAGE: Python
@summary: This module defines all supported language/filetype identifiers and
          an extension register for mapping file extensions to filetypes.
@see: synglob.py for more details on how this data is used

@note: Don't use this module directly for internal use only

"""
__author__ = 'Cody Precord <cprecord@editra.org>'
__svnid__ = '$Id: synextreg.py 70228 2011-12-31 20:39:16Z CJP $'
__revision__ = '$Revision: 70228 $'
import os

def _NewId():
    global _idCounter
    _idCounter += 1
    return _idCounter


_idCounter = 32100
ID_LANG_TXT = _NewId()
LANG_TXT = 'Plain Text'
ID_LANG_ADA = _NewId()
LANG_ADA = 'Ada'
ID_LANG_ASM = _NewId()
LANG_ASM = 'GNU Assembly'
ID_LANG_DSP56K = _NewId()
LANG_DSP56K = 'DSP56K Assembly'
ID_LANG_68K = _NewId()
LANG_68K = '68k Assembly'
ID_LANG_MASM = _NewId()
LANG_MASM = 'MASM'
ID_LANG_NASM = _NewId()
LANG_NASM = 'Netwide Assembler'
ID_LANG_BOURNE = _NewId()
LANG_BOURNE = 'Bourne Shell Script'
ID_LANG_BASH = _NewId()
LANG_BASH = 'Bash Shell Script'
ID_LANG_CSH = _NewId()
LANG_CSH = 'C-Shell Script'
ID_LANG_KSH = _NewId()
LANG_KSH = 'Korn Shell Script'
ID_LANG_CAML = _NewId()
LANG_CAML = 'Caml'
ID_LANG_APACHE = _NewId()
LANG_APACHE = 'Apache Conf'
ID_LANG_AS = _NewId()
LANG_AS = 'ActionScript'
ID_LANG_C = _NewId()
LANG_C = 'C'
ID_LANG_CILK = _NewId()
LANG_CILK = 'Cilk'
ID_LANG_CPP = _NewId()
LANG_CPP = 'CPP'
ID_LANG_CSHARP = _NewId()
LANG_CSHARP = 'C#'
ID_LANG_D = _NewId()
LANG_D = 'D'
ID_LANG_DOT = _NewId()
LANG_DOT = 'DOT'
ID_LANG_EDJE = _NewId()
LANG_EDJE = 'Edje'
ID_LANG_FERITE = _NewId()
LANG_FERITE = 'Ferite'
ID_LANG_GLSL = _NewId()
LANG_GLSL = 'GLSL'
ID_LANG_HAXE = _NewId()
LANG_HAXE = 'HaXe'
ID_LANG_JAVA = _NewId()
LANG_JAVA = 'Java'
ID_LANG_OBJC = _NewId()
LANG_OBJC = 'Objective C'
ID_LANG_OOC = _NewId()
LANG_OOC = 'OOC'
ID_LANG_PIKE = _NewId()
LANG_PIKE = 'Pike'
ID_LANG_SQUIRREL = _NewId()
LANG_SQUIRREL = 'Squirrel'
ID_LANG_STATA = _NewId()
LANG_STATA = 'Stata'
ID_LANG_VALA = _NewId()
LANG_VALA = 'Vala'
ID_LANG_CSS = _NewId()
LANG_CSS = 'Cascading Style Sheet'
ID_LANG_ESS = _NewId()
LANG_ESS = 'Editra Style Sheet'
ID_LANG_EIFFEL = _NewId()
LANG_EIFFEL = 'Eiffel'
ID_LANG_ERLANG = _NewId()
LANG_ERLANG = 'Erlang'
ID_LANG_FLAGSHIP = _NewId()
LANG_FLAGSHIP = 'FlagShip'
ID_LANG_F77 = _NewId()
LANG_F77 = 'Fortran 77'
ID_LANG_FORTH = _NewId()
LANG_FORTH = 'Forth'
ID_LANG_F95 = _NewId()
LANG_F95 = 'Fortran 95'
ID_LANG_GUI4CLI = _NewId()
LANG_GUI4CLI = 'Gui4Cli'
ID_LANG_HASKELL = _NewId()
LANG_HASKELL = 'Haskell'
ID_LANG_COLDFUSION = _NewId()
LANG_COLDFUSION = 'ColdFusion'
ID_LANG_HTML = _NewId()
LANG_HTML = 'HTML'
ID_LANG_JS = _NewId()
LANG_JS = 'JavaScript'
ID_LANG_PHP = _NewId()
LANG_PHP = 'PHP'
ID_LANG_XML = _NewId()
LANG_XML = 'XML'
ID_LANG_SGML = _NewId()
ID_LANG_INNO = _NewId()
LANG_INNO = 'Inno Setup Script'
ID_LANG_KIX = _NewId()
LANG_KIX = 'Kix'
ID_LANG_LISP = _NewId()
LANG_LISP = 'Lisp'
ID_LANG_SCHEME = _NewId()
LANG_SCHEME = 'Scheme'
ID_LANG_NEWLISP = _NewId()
LANG_NEWLISP = 'newLISP'
ID_LANG_LOUT = _NewId()
LANG_LOUT = 'Lout'
ID_LANG_LUA = _NewId()
LANG_LUA = 'Lua'
ID_LANG_MSSQL = _NewId()
LANG_MSSQL = 'Microsoft SQL'
ID_LANG_NONMEM = _NewId()
LANG_NONMEM = 'NONMEM Control Stream'
ID_LANG_NSIS = _NewId()
LANG_NSIS = 'Nullsoft Installer Script'
ID_LANG_PASCAL = _NewId()
LANG_PASCAL = 'Pascal'
ID_LANG_PERL = _NewId()
LANG_PERL = 'Perl'
ID_LANG_PS = _NewId()
LANG_PS = 'Postscript'
ID_LANG_BOO = _NewId()
LANG_BOO = 'Boo'
ID_LANG_PYTHON = _NewId()
LANG_PYTHON = 'Python'
ID_LANG_COBRA = _NewId()
LANG_COBRA = 'Cobra'
ID_LANG_MATLAB = _NewId()
LANG_MATLAB = 'Matlab'
ID_LANG_RUBY = _NewId()
LANG_RUBY = 'Ruby'
ID_LANG_ST = _NewId()
LANG_ST = 'Smalltalk'
ID_LANG_SQL = _NewId()
LANG_SQL = 'SQL'
ID_LANG_PLSQL = _NewId()
LANG_PLSQL = 'PL/SQL'
ID_LANG_4GL = _NewId()
LANG_4GL = 'Progress 4GL'
ID_LANG_TCL = _NewId()
LANG_TCL = 'Tcl/Tk'
ID_LANG_TEX = _NewId()
LANG_TEX = 'Tex'
ID_LANG_LATEX = _NewId()
LANG_LATEX = 'LaTeX'
ID_LANG_VB = _NewId()
LANG_VB = 'Visual Basic'
ID_LANG_VBSCRIPT = _NewId()
LANG_VBSCRIPT = 'VBScript'
ID_LANG_VERILOG = _NewId()
LANG_VERILOG = 'Verilog'
ID_LANG_SYSVERILOG = _NewId()
LANG_SYSVERILOG = 'System Verilog'
ID_LANG_VHDL = _NewId()
LANG_VHDL = 'VHDL'
ID_LANG_OCTAVE = _NewId()
LANG_OCTAVE = 'Octave'
ID_LANG_BATCH = _NewId()
LANG_BATCH = 'DOS Batch Script'
ID_LANG_DIFF = _NewId()
LANG_DIFF = 'Diff File'
ID_LANG_MAKE = _NewId()
LANG_MAKE = 'Makefile'
ID_LANG_PROPS = _NewId()
LANG_PROPS = 'Properties'
ID_LANG_YAML = _NewId()
LANG_YAML = 'YAML'
ID_LANG_DJANGO = _NewId()
LANG_DJANGO = 'Django'
ID_LANG_ISSL = _NewId()
LANG_ISSL = 'IssueList'
ID_LANG_MAKO = _NewId()
LANG_MAKO = 'Mako'
ID_LANG_R = _NewId()
LANG_R = 'R'
ID_LANG_S = _NewId()
LANG_S = 'S'
ID_LANG_GROOVY = _NewId()
LANG_GROOVY = 'Groovy'
ID_LANG_XTEXT = _NewId()
LANG_XTEXT = 'Xtext'
EXT_MAP = {'4gl': LANG_4GL, 
   '56k': LANG_DSP56K, 
   '68k': LANG_68K, 
   'ada adb ads a': LANG_ADA, 
   'conf htaccess': LANG_APACHE, 
   'as asc mx': LANG_AS, 
   'gasm': LANG_ASM, 
   'bsh sh configure': LANG_BASH, 
   'bat cmd': LANG_BATCH, 
   'boo': LANG_BOO, 
   'c h': LANG_C, 
   'ml mli': LANG_CAML, 
   'cilk cilkh': LANG_CILK, 
   'cobra': LANG_COBRA, 
   'cfm cfc cfml dbm': LANG_COLDFUSION, 
   'cc c++ cpp cxx hh h++ hpp hxx': LANG_CPP, 
   'csh': LANG_CSH, 
   'cs': LANG_CSHARP, 
   'css': LANG_CSS, 
   'd': LANG_D, 
   'patch diff': LANG_DIFF, 
   'django': LANG_DJANGO, 
   'dot': LANG_DOT, 
   'edc': LANG_EDJE, 
   'e': LANG_EIFFEL, 
   'erl': LANG_ERLANG, 
   'ess': LANG_ESS, 
   'f for': LANG_F77, 
   'f90 f95 f2k fpp': LANG_F95, 
   'fe': LANG_FERITE, 
   'fth 4th fs seq': LANG_FORTH, 
   'prg': LANG_FLAGSHIP, 
   'frag vert glsl': LANG_GLSL, 
   'gc gui': LANG_GUI4CLI, 
   'hs': LANG_HASKELL, 
   'hx hxml': LANG_HAXE, 
   'htm html shtm shtml xhtml': LANG_HTML, 
   'isl': LANG_ISSL, 
   'iss': LANG_INNO, 
   'java': LANG_JAVA, 
   'js': LANG_JS, 
   'kix': LANG_KIX, 
   'ksh': LANG_KSH, 
   'aux tex sty': LANG_LATEX, 
   'cl lisp': LANG_LISP, 
   'lsp': LANG_NEWLISP, 
   'lt': LANG_LOUT, 
   'lua': LANG_LUA, 
   'mak makefile mk': LANG_MAKE, 
   'mao mako': LANG_MAKO, 
   'asm masm': LANG_MASM, 
   'matlab': LANG_MATLAB, 
   'mssql': LANG_MSSQL, 
   'nasm': LANG_NASM, 
   'ctl nonmem': LANG_NONMEM, 
   'nsi nsh': LANG_NSIS, 
   'mm m': LANG_OBJC, 
   'oct octave': LANG_OCTAVE, 
   'ooc': LANG_OOC, 
   'dfm dpk dpr inc p pas pp': LANG_PASCAL, 
   'cgi pl pm pod': LANG_PERL, 
   'php php3 phtml phtm': LANG_PHP, 
   'pike': LANG_PIKE, 
   'plsql': LANG_PLSQL, 
   'ini inf reg url cfg cnf': LANG_PROPS, 
   'ai ps': LANG_PS, 
   'py pyw python': LANG_PYTHON, 
   'r': LANG_R, 
   'do ado': LANG_STATA, 
   'rake rb rbw rbx gemspec': LANG_RUBY, 
   's': LANG_S, 
   'scm smd ss': LANG_SCHEME, 
   'sql': LANG_SQL, 
   'nut': LANG_SQUIRREL, 
   'st': LANG_ST, 
   'sv svh': LANG_SYSVERILOG, 
   'itcl tcl tk': LANG_TCL, 
   'txt': LANG_TXT, 
   'vala': LANG_VALA, 
   'bas cls frm vb': LANG_VB, 
   'vbs dsm': LANG_VBSCRIPT, 
   'v': LANG_VERILOG, 
   'vh vhdl vhd': LANG_VHDL, 
   'axl dtd plist rdf svg xml xrc xsd xsl xslt xul': LANG_XML, 
   'yaml yml': LANG_YAML, 
   'groovy': LANG_GROOVY, 
   'xtext': LANG_XTEXT}

class ExtensionRegister(dict):
    """A data storage class for managing mappings of
    file types to file extensions. The register is created as a singleton.

    """
    instance = None
    config = 'synmap'

    def __init__(self):
        """Initializes the register"""
        if not ExtensionRegister.instance:
            self.LoadDefault()

    def __new__(cls, *args, **kargs):
        """Maintain only a single instance of this object
        @return: instance of this class

        """
        if not cls.instance:
            cls.instance = dict.__new__(cls, *args, **kargs)
        return cls.instance

    def __missing__(self, key):
        """Return the default value if an item is not found
        @return: txt extension for plain text

        """
        return 'txt'

    def __setitem__(self, i, y):
        """Ensures that only one filetype is associated with an extension
        at one time. The behavior is that more recent settings override
        and remove associations from older settings.
        @param i: key to set
        @param y: value to set
        @throws: TypeError Only accepts list() objects

        """
        if not isinstance(y, list):
            raise TypeError, 'Extension Register Expects a List'
        for (key, val) in self.iteritems():
            for item in y:
                if item in val:
                    val.pop(val.index(item))

        y.sort()
        dict.__setitem__(self, i, [ x.strip() for x in y ])

    def __str__(self):
        """Converts the Register to a string that is formatted
        for output to a config file.
        @return: the register as a string

        """
        keys = self.keys()
        keys.sort()
        tmp = list()
        for key in keys:
            tmp.append('%s=%s' % (key, (':').join(self.__getitem__(key))))

        return os.linesep.join(tmp)

    def Associate(self, ftype, ext):
        """Associate a given file type with the given file extension(s).
        The ext parameter can be a string of space separated extensions
        to allow for multiple associations at once.
        @param ftype: file type description string
        @param ext: file extension to associate
        
        """
        assoc = self.get(ftype, None)
        exts = ext.strip().split()
        if assoc:
            for x in exts:
                if x not in assoc:
                    assoc.append(x)

        else:
            assoc = list(set(exts))
        assoc.sort()
        super(ExtensionRegister, self).__setitem__(ftype, assoc)
        return

    def Disassociate(self, ftype, ext):
        """Disassociate a file type with a given extension or space
        separated list of extensions.
        @param ftype: filetype description string
        @param ext: extension to disassociate

        """
        to_drop = ext.strip().split()
        assoc = self.get(ftype, None)
        if assoc:
            for item in to_drop:
                if item in assoc:
                    assoc.remove(item)

            super(ExtensionRegister, self).__setitem__(ftype, assoc)
        return

    def FileTypeFromExt(self, ext):
        """Returns the file type that is associated with
        the extension. Matching is done with a case insensitive search.
        If no association is found Plain Text
        will be returned by default.
        @param ext: extension to lookup

        """
        ext = ext.lower()
        for (key, val) in self.iteritems():
            if ext in [ ext2.lower() for ext2 in val ]:
                return key

        return LANG_TXT

    def GetAllExtensions(self):
        """Returns a sorted list of all extensions registered
        @return: list of all registered extensions

        """
        ext = list()
        for extension in self.values():
            ext.extend(extension)

        ext.sort()
        return ext

    def LoadDefault(self):
        """Loads the default settings
        @postcondition: sets dictionary back to default installation state

        """
        self.clear()
        for key in EXT_MAP:
            self.__setitem__(EXT_MAP[key], key.split())

    def LoadFromConfig(self, config):
        """Load the extension register with values from a config file
        @param config: path to config file to load settings from

        """
        path = os.path.join(config, self.config)
        if not os.path.exists(path):
            self.LoadDefault()
        else:
            file_h = file(path, 'rb')
            lines = file_h.readlines()
            file_h.close()
        for line in lines:
            tmp = line.split('=')
            if len(tmp) != 2:
                continue
            ftype = tmp[0].strip()
            exts = tmp[1].split(':')
            self.__setitem__(ftype, exts)

    def Remove(self, ftype):
        """Remove a filetype from the register
        @param ftype: File type description string
        @return: bool removed or not

        """
        if ftype in self:
            del self[ftype]
            return True
        return False

    def SetAssociation(self, ftype, ext):
        """Like Associate but overrides any current settings instead of
        just adding to them.
        @param ftype: File type description string
        @param ext: space separated list of file extensions to set

        """
        self.__setitem__(ftype, list(set(ext.split())))


def GetFileExtensions():
    """Gets a sorted list of all file extensions the editor is configured
    to handle.
    @return: all registered file extensions

    """
    extreg = ExtensionRegister()
    return extreg.GetAllExtensions()


def RegisterNewLangId(langId, langName):
    """Register a new language identifier
    @param langId: "ID_LANG_FOO"
    @param langName: "Foo"
    @return: int

    """
    gdict = globals()
    if langId not in gdict:
        gdict[langId] = _NewId()
        gdict[langId[3:]] = langName
    return gdict[langId]