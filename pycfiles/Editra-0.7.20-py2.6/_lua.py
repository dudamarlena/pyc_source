# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/Editra/src/syntax/_lua.py
# Compiled at: 2011-08-30 21:43:46
"""
FILE: lua.py
AUTHOR: Cody Precord
@summary: Lexer configuration module for Lua
@todo: This setup for Lua5, maybe add Lua4 support

"""
__author__ = 'Cody Precord <cprecord@editra.org>'
__svnid__ = '$Id: _lua.py 68798 2011-08-20 17:17:05Z CJP $'
__revision__ = '$Revision: 68798 $'
import wx.stc as stc, syndata
LUA_KEYWORDS = (0, 'and break do else elseif end false for function if in local nil not or repeat return then true until while')
LUA_FUNCT = (1, '_VERSION assert collectgarbage dofile error gcinfo loadfile loadstring print rawget rawset require tonumber tostring type unpack _G getfenv getmetatable ipairs loadlib next pairs pcall rawequal setfenv setmetatable xpcall \\string table math coroutine io os debug \\load module select')
LUA_STR = (2, 'string.byte string.char string.dump string.find string.len string.lower string.rep string.sub string.upper string.format string.gfind string.gsub table.concat table.foreach table.foreachi table.getn table.sort table.insert table.remove table.setn math.abs math.acos math.asin math.atan math.atan2 math.ceil math.cos math.deg math.exp math.floor math.frexp math.ldexp math.log math.log10 math.max math.min math.mod math.pi math.pow math.rad math.random math.randomseed math.sin math.sqrt math.tan string.gmatch string.match string.reverse table.maxn math.cosh math.fmod math.modf math.sinh math.tanh math.huge')
LUA_CO = (3, 'coroutine.create coroutine.resume coroutine.status coroutine.wrap coroutine.yield io.close io.flush io.input io.lines io.open io.output io.read io.tmpfile io.type io.write io.stdin io.stdout io.stderr os.clock os.date os.difftime os.execute os.exit os.getenv os.remove os.rename os.setlocale os.time os.tmpname coroutine.running package.cpath package.loaded package.loadlib package.path package.preload package.seeall io.popen')
LUA_U1 = (4, '')
LUA_U2 = (5, '')
LUA_U3 = (6, '')
LUA_U4 = (7, '')
SYNTAX_ITEMS = [
 (
  stc.STC_LUA_CHARACTER, 'char_style'),
 (
  stc.STC_LUA_COMMENT, 'comment_style'),
 (
  stc.STC_LUA_COMMENTDOC, 'dockey_style'),
 (
  stc.STC_LUA_COMMENTLINE, 'comment_style'),
 (
  stc.STC_LUA_DEFAULT, 'default_style'),
 (
  stc.STC_LUA_IDENTIFIER, 'default_style'),
 (
  stc.STC_LUA_LITERALSTRING, 'string_style'),
 (
  stc.STC_LUA_NUMBER, 'number_style'),
 (
  stc.STC_LUA_OPERATOR, 'operator_style'),
 (
  stc.STC_LUA_PREPROCESSOR, 'pre_style'),
 (
  stc.STC_LUA_STRING, 'string_style'),
 (
  stc.STC_LUA_STRINGEOL, 'stringeol_style'),
 (
  stc.STC_LUA_WORD, 'keyword_style'),
 (
  stc.STC_LUA_WORD2, 'keyword3_style'),
 (
  stc.STC_LUA_WORD3, 'funct_style'),
 (
  stc.STC_LUA_WORD4, 'funct_style'),
 (
  stc.STC_LUA_WORD5, 'default_style'),
 (
  stc.STC_LUA_WORD6, 'default_style'),
 (
  stc.STC_LUA_WORD7, 'default_style'),
 (
  stc.STC_LUA_WORD8, 'default_style')]
FOLD = ('fold', '1')
FOLD_COMP = ('fold.compact', '1')

class SyntaxData(syndata.SyntaxDataBase):
    """SyntaxData object for Lua"""

    def __init__(self, langid):
        super(SyntaxData, self).__init__(langid)
        self.SetLexer(stc.STC_LEX_LUA)

    def GetKeywords(self):
        """Returns Specified Keywords List """
        return [
         LUA_KEYWORDS, LUA_FUNCT, LUA_STR, LUA_CO]

    def GetSyntaxSpec(self):
        """Syntax Specifications """
        return SYNTAX_ITEMS

    def GetProperties(self):
        """Returns a list of Extra Properties to set"""
        return [
         FOLD, FOLD_COMP]

    def GetCommentPattern(self):
        """Returns a list of characters used to comment a block of code """
        return [
         '--']