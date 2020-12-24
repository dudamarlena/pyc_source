# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-intel/egg/cpip/TokenCss.py
# Compiled at: 2017-10-03 13:07:16
"""CSS Support for ITU+TU files in HTML."""
__author__ = 'Paul Ross'
__date__ = '2011-07-10'
__rights__ = 'Copyright (c) 2008-2017 Paul Ross'
import os
from cpip import ExceptionCpip
from cpip.core import ItuToTokens
import string

class ExceptionTokenCss(ExceptionCpip):
    pass


TT_ENUM_MAP = {}
ENUM_TT_MAP = {}
for __i, __tt in enumerate(ItuToTokens.ITU_TOKEN_TYPES):
    __enum = string.ascii_lowercase[__i]
    TT_ENUM_MAP[__tt] = __enum
    ENUM_TT_MAP[__enum] = __tt

ITU_CSS_LIST = [
 '/* Conditionally compiled == %s. */\nspan.%s {\nbackground-color: GreenYellow;\n}' % (True, True),
 '/* Conditionally compiled == %s. */\nspan.%s {\nbackground-color: Salmon;\n}' % (False, False),
 '/* Conditionally compiled == %s. */\nspan.%s {\nbackground-color: yellowgreen;\n}' % ('Maybe',
                                                                                       'Maybe'),
 '/* %s */\nspan.%s {\ncolor:         Chartreuse;\nfont-style:    italic;\n}' % ('header-name', TT_ENUM_MAP['header-name']),
 '/* %s */\nspan.%s {\ncolor:         BlueViolet;\nfont-style:    normal;\n}' % ('identifier', TT_ENUM_MAP['identifier']),
 '/* %s */\nspan.%s {\ncolor:         HotPink;\nfont-style:    normal;\n}' % ('pp-number', TT_ENUM_MAP['pp-number']),
 '/* %s */\nspan.%s {\ncolor:         orange;\nfont-style:    italic;\n}' % ('character-literal', TT_ENUM_MAP['character-literal']),
 '/* %s */\nspan.%s {\ncolor:         LimeGreen;\nfont-style:    italic;\n}' % ('string-literal', TT_ENUM_MAP['string-literal']),
 '/* %s */\nspan.%s {\ncolor:         black;\nfont-weight:   bold;\nfont-style:    normal;\n}' % ('preprocessing-op-or-punc', TT_ENUM_MAP['preprocessing-op-or-punc']),
 '/* %s */\nspan.%s {\ncolor:         silver;\nfont-style:    normal;\n}' % ('non-whitespace', TT_ENUM_MAP['non-whitespace']),
 '/* %s */\nspan.%s {\ncolor:         black;\nfont-style:    normal;\n}' % ('whitespace', TT_ENUM_MAP['whitespace']),
 '/* %s */\nspan.%s {\ncolor:         black;\nfont-style:    normal;\n}' % ('concat', TT_ENUM_MAP['concat']),
 '/* %s */\nspan.%s {\ncolor:         red;\nfont-style:    normal;\n}' % ('trigraph', TT_ENUM_MAP['trigraph']),
 '/* %s */\nspan.%s {\ncolor:         sienna;\nfont-style:    normal;\n}' % ('C comment', TT_ENUM_MAP['C comment']),
 '/* %s */\nspan.%s {\ncolor:         peru;\nfont-style:    normal;\n}' % ('C++ comment', TT_ENUM_MAP['C++ comment']),
 '/* %s */\nspan.%s {\ncolor:         red;\nfont-style:    normal;\n}' % ('keyword', TT_ENUM_MAP['keyword']),
 '/* %s */\nspan.%s {\ncolor:         blue;\nfont-style:    normal;\n}' % ('preprocessing-directive', TT_ENUM_MAP['preprocessing-directive']),
 '/* %s */\nspan.%s {\ncolor:         red;\nfont-style:    italic;\n}' % ('Unknown', TT_ENUM_MAP['Unknown']),
 'body {\nfont-size:      12px;\nfont-family:    arial,helvetica,sans-serif;\nmargin:         6px;\npadding:        6px;\n}',
 'h1 {\ncolor:            darkgoldenrod;\nfont-family:      sans-serif;\nfont-size:        14pt;\nfont-weight:      bold;\n}',
 'h2 {\ncolor:          IndianRed;\nfont-family:    sans-serif;\nfont-size:      14pt;\nfont-weight:    normal;\n}',
 'h3 {\ncolor:          Black;\nfont-family:    sans-serif;\nfont-size:      12pt;\nfont-weight:    bold;\n}',
 'h4 {\ncolor:          FireBrick;\nfont-family:    sans-serif;\nfont-size:      10pt;\nfont-weight:    bold;\n}',
 'span.line {\ncolor:           slategrey;\n/*font-style:    italic; */\n}',
 'span.file {\n color:         black;\n font-style:    italic;\n}',
 'table.filetable {\n    border:         2px solid black;\n    font-family:    monospace;\n    color:          black;\n}',
 'th.filetable, td.filetable {\n    /* border: 1px solid black; */\n    border: 1px;\n    border-top-style:solid;\n    border-right-style:dotted;\n    border-bottom-style:none;\n    border-left-style:none;\n    vertical-align:top;\n    padding: 2px 6px 2px 6px; \n}',
 'table.monospace {\nborder:            2px solid black;\nborder-collapse:   collapse;\nfont-family:       monospace;\ncolor:             black;\n}',
 'th.monospace, td.monospace {\nborder:            1px solid black;\nvertical-align:    top;\npadding:           2px 6px 2px 6px; \n}',
 'span.macro_s_f_r_f_name{\n    color:          DarkSlateGray;\n    font-family:    monospace;\n    font-weight:    normal;\n    font-style:     italic;\n}',
 'span.macro_s_t_r_f_name {\n    color:          DarkSlateGray;\n    font-family:    monospace;\n    font-weight:    normal;\n    font-style:     normal;\n}',
 'span.macro_s_f_r_t_name {\n    color:          Red; /* OrangeRed; */\n    font-family:    monospace;\n    font-weight:    bold;\n    font-style:     italic;\n}',
 'span.macro_s_t_r_t_name{\n    color:          Red; /* OrangeRed; */\n    font-family:    monospace;\n    font-weight:    bold;\n    font-style:     normal;\n}',
 'span.macro_s_f_r_f_repl{\n    color:          SlateGray;\n    font-family:    monospace;\n    font-weight:    normal;\n    font-style:     italic;\n}',
 'span.macro_s_t_r_f_repl {\n    color:          SlateGray;\n    font-family:    monospace;\n    font-weight:    normal;\n    font-style:     normal;\n}',
 'span.macro_s_f_r_t_repl {\n    color:          RosyBrown; /* Orange; */\n    font-family:    monospace;\n    font-weight:    bold;\n    font-style:     italic;\n}',
 'span.macro_s_t_r_t_repl{\n    color:          RosyBrown; /* Orange; */\n    font-family:    monospace;\n    font-weight:    bold;\n    font-style:     normal;\n}',
 'span.file_decl {\n    color:          black;\n    font-family:    monospace;\n    /* font-weight:    bold;\n    font-style:     italic; */\n}',
 'span.CcgNodeTrue {\n    color:          LimeGreen;\n    font-family:    monospace;\n    /* font-weight:    bold; */\n    /* font-style:     italic; */\n}',
 'span.CcgNodeFalse {\n    color:          red;\n    font-family:    monospace;\n    /* font-weight:    bold; */\n    /* font-style:     italic; */\n}']
TT_CSS_FILE = 'cpip.css'
TT_CSS_STRING = ('\n').join(ITU_CSS_LIST)

def writeCssToDir(theDir):
    """Writes the CSS file into to the directory."""
    try:
        if not os.path.exists(theDir):
            os.makedirs(theDir)
        open(os.path.join(theDir, TT_CSS_FILE), 'w').write(TT_CSS_STRING)
    except IOError as err:
        raise ExceptionTokenCss('writeCssToDir(): %s' % str(err))


def writeCssForFile(theFile):
    """Writes the CSS file into to the directory that the file is in."""
    return writeCssToDir(os.path.dirname(theFile))


def retClass(theTt):
    try:
        return TT_ENUM_MAP[theTt]
    except KeyError:
        raise ExceptionTokenCss('Unknown token type %s' % theTt)