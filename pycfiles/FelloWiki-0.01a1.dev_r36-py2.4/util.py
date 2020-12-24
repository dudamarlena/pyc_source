# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/fellowiki/controllers/wikiparser/util.py
# Compiled at: 2006-11-21 20:30:39
import re

def remove_escaping_backslashes(string):
    r"""translate string with escaping backslashes to un-escaped version
    
    parameters: string: escaped string, may be unicode as well
    returns: unescaped version of the string
    
    This function looks for any occurence of "\." where "." can be any
    single character and replaces it by the character "." itself.
    
    """
    pattern = re.compile('\\\\(.)')
    return pattern.sub('\\1', string)


def remove_backslashes_and_whitespace(string):
    r"""remove escaping backslashes and enclosing whitespace
    
    parameters: string: escaped string, may be unicode as well
    returns: unescaped version of the string
    
    This function looks for any occurence of "\." where "." can be any
    single character and replaces it by the character "." itself.
    
    Additionally it removes all enclosing whitespace (i.e. blank and
    tab) which hadn't been escaped before.
    
    """
    string = string.lstrip(' \t')
    pattern = re.compile('(\\\\)(?=[ \\t]*$)')
    string2 = pattern.sub('\\\\\\\\', string)
    if len(string) == len(string2):
        return remove_escaping_backslashes(string).rstrip(' \t')
    string = remove_escaping_backslashes(string)
    string2 = remove_escaping_backslashes(string2)
    if len(string) == len(string2):
        return string.rstrip(' \t')
    else:
        pattern = re.compile('([ \\t])[ \\t]*$')
        return pattern.sub('\\1', string)