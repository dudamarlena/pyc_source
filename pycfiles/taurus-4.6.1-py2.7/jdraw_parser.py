# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/taurus/qt/qtgui/graphic/jdraw/jdraw_parser.py
# Compiled at: 2019-08-19 15:09:29
"""This module parses jdraw files"""
from __future__ import absolute_import
import os, re
from ply import lex
from ply import yacc
from taurus.core.util.log import Logger
__all__ = [
 'new_parser', 'parse']
tokens = ('NUMBER', 'SYMBOL', 'LBRACKET', 'RBRACKET', 'TWOP', 'COMMA', 'JDFILE', 'GLOBAL',
          'JDLINE', 'JDRECTANGLE', 'JDROUNDRECTANGLE', 'JDGROUP', 'JDELLIPSE', 'JDBAR',
          'JDSWINGOBJECT', 'JDLABEL', 'JDPOLYLINE', 'JDIMAGE', 'JDAXIS', 'JDSLIDER',
          'JDSPLINE', 'TEXT', 'true', 'false')
t_LBRACKET = '\\{'
t_RBRACKET = '\\}'
t_TWOP = '\\:'
t_COMMA = '\\,'
t_TEXT = '\\"[^"]*\\"'
reserved = {'JDFile': 'JDFILE', 
   'Global': 'GLOBAL', 
   'JDLine': 'JDLINE', 
   'JDRectangle': 'JDRECTANGLE', 
   'JDRoundRectangle': 'JDROUNDRECTANGLE', 
   'JDGroup': 'JDGROUP', 
   'JDEllipse': 'JDELLIPSE', 
   'JDBar': 'JDBAR', 
   'JDSwingObject': 'JDSWINGOBJECT', 
   'JDLabel': 'JDLABEL', 
   'JDPolyline': 'JDPOLYLINE', 
   'JDImage': 'JDIMAGE', 
   'JDAxis': 'JDAXIS', 
   'JDSlider': 'JDSLIDER', 
   'JDSpline': 'JDSPLINE', 
   'true': 'true', 
   'false': 'false'}

def t_SYMBOL(t):
    """[a-zA-Z_][a-zA-Z_0-9]*"""
    t.type = reserved.get(t.value, 'SYMBOL')
    return t


def t_NUMBER(t):
    r"""[-+]?[0-9]*\.?[0-9]+([eE][-+]?[0-9]+)?"""
    try:
        t.value = float(t.value)
    except:
        t.lexer.log.info('[%d]: Number %s is not valid!' % (t.lineno, t.value))
        t.value = 0

    return t


t_ignore = ' \t'

def t_newline(t):
    r"""\n+"""
    t.lexer.lineno += t.value.count('\n')


def t_error(t):
    t.lexer.log.info("[%d]: Illegal character '%s'" % (
     t.lexer.lineno, t.value[0]))
    t.lexer.skip(1)


def p_error(p):
    p.lexer.log.error('[%d]: Syntax error in input [%s]' % (
     p.lexer.lineno, str(p)))


def p_jdfile(p):
    """ jdfile :  JDFILE SYMBOL LBRACKET global element_list RBRACKET """
    factory = p.parser.factory
    p[0] = factory.getSceneObj(p[5])
    if p[0] is None:
        p.parser.log.info('[%d]: Unable to create Scene' % p.lexer.lineno)
    return


def p_jdfile_empty(p):
    """ jdfile : JDFILE LBRACKET global RBRACKET """
    factory = p.parser.factory
    p[0] = factory.getSceneObj([])
    if p[0] is None:
        p.parser.log.info('[%d]: Unable to create Scene' % p.lexer.lineno)
    return


def p_global(p):
    """ global : GLOBAL LBRACKET RBRACKET
               | GLOBAL LBRACKET parameter_list RBRACKET"""
    if len(p) == 4:
        p[0] = {}
    else:
        p[0] = p[3]


def p_element_list(p):
    """element_list : element_list element """
    if p[2] is not None:
        p[0] = p[1] + [p[2]]
    else:
        p[0] = p[1]
    return


def p_element(p):
    """element_list : element """
    p[0] = [
     p[1]]


def p_single_element(p):
    """element : obj LBRACKET RBRACKET
               | obj LBRACKET parameter_list RBRACKET"""
    if len(p) == 4:
        p[3] = {}
    org = name = p[3].get('name')
    keywords = [
     'JDGroup'] + [ n.replace('JD', '') for n in reserved ]
    if not name or name in keywords or re.match('[0-9]+$', name):
        p[3]['name'] = name = ''
        for model in reversed(p.parser.modelStack):
            if model and model not in keywords and not re.match('[0-9]+$', model):
                p[3]['name'] = name = model
                break

    extension = p[3].get('extensions')
    if p.parser.modelStack2:
        if extension is None:
            p[3]['extensions'] = p.parser.modelStack2[0]
        elif len(p.parser.modelStack2) == 2:
            extension.update(p.parser.modelStack2[0])
            p[3]['extensions'] = extension
    factory = p.parser.factory
    ret = factory.getObj(p[1], p[3])
    if ret is None:
        p.parser.log.info("[%d]: Unable to create obj '%s'" % (
         p.lexer.lineno, p[1]))
    p.parser.modelStack.pop()
    if extension:
        p.parser.modelStack2.pop()
    p[0] = ret
    return


def p_obj(p):
    """obj : JDLINE
           | JDRECTANGLE
           | JDROUNDRECTANGLE
           | JDGROUP
           | JDELLIPSE
           | JDBAR
           | JDSWINGOBJECT
           | JDLABEL
           | JDPOLYLINE
           | JDIMAGE
           | JDAXIS
           | JDSLIDER
           | JDSPLINE"""
    p[0] = p[1]


def p_parameter_list(p):
    """parameter_list : parameter_list parameter"""
    p[0] = p[1]
    p[0].update(p[2])


def p_parameter(p):
    """parameter_list : parameter"""
    p[0] = p[1]


def p_single_parameter(p):
    """parameter : SYMBOL TWOP param_value"""
    if p[1] == 'name':
        p.parser.modelStack.append(p[3])
    if p[1] == 'extensions':
        p.parser.modelStack2.append(p[3])
    p[0] = {p[1]: p[3]}


def p_complex_parameter(p):
    """parameter : SYMBOL TWOP LBRACKET RBRACKET
                 | SYMBOL TWOP LBRACKET parameter_list RBRACKET
                 | SYMBOL TWOP LBRACKET element_list RBRACKET"""
    if len(p) == 5:
        p[4] = []
    p[0] = {p[1]: p[4]}
    if p[1] == 'extensions':
        p.parser.modelStack2.append(p[4])


def p_param_value_number_list(p):
    """param_value : value_list """
    if len(p[1]) == 1:
        p[0] = p[1][0]
    else:
        p[0] = p[1]


def p_value_list(p):
    """ value_list : value_list COMMA value """
    p[0] = p[1] + [p[3]]


def p_value_list_value(p):
    """ value_list : value """
    p[0] = [
     p[1]]


def p_value_number(p):
    """value : NUMBER"""
    p[0] = p[1]


def p_value_text(p):
    """value : TEXT"""
    p[0] = p[1].strip('"')


def p_value_bool(p):
    """value : true
             | false"""
    p[0] = p[1] == 'true'


def new_parser(optimize=None, debug=0, outputdir=None):
    log = Logger('JDraw Parser')
    if optimize is None:
        from taurus import tauruscustomsettings
        optimize = getattr(tauruscustomsettings, 'PLY_OPTIMIZE', 1)
    if outputdir is None:
        outputdir = os.path.join(os.path.expanduser('~'), '.taurus')
        if not os.path.exists(outputdir):
            os.makedirs(outputdir)
    debuglog = None
    if debug:
        debuglog = log
    common_kwargs = dict(optimize=optimize, outputdir=outputdir, debug=debug, debuglog=debuglog, errorlog=log)
    if int(lex.__version__.split('.')[0]) < 3:
        common_kwargs.pop('debuglog')
        common_kwargs.pop('errorlog')
    jdraw_lextab = 'jdraw_lextab'
    jdraw_yacctab = 'jdraw_yacctab'
    l = lex.lex(lextab=jdraw_lextab, **common_kwargs)
    try:
        p = yacc.yacc(tabmodule=jdraw_yacctab, debugfile=None, write_tables=1, **common_kwargs)
    except Exception as e:
        msg = 'Error creating jdraw parser.\n' + 'HINT: Try removing jdraw_lextab.* and jdraw_yacctab.* from %s' % outputdir
        raise RuntimeError(msg)

    return (l, p)


def parse(filename=None, factory=None):
    if filename is None or factory is None:
        return
    _, p = new_parser()
    p.factory = factory
    p.modelStack = []
    p.modelStack2 = []
    res = None
    try:
        filename = os.path.realpath(filename)
        f = open(filename)
        res = yacc.parse(f.read())
    except:
        log = Logger('JDraw Parser')
        log.warning('Failed to parse %s' % filename)
        log.debug('Details:', exc_info=1)

    return res


if __name__ == '__main__':
    new_parser()