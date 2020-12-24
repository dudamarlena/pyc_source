# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/hugo/.virtualenvs/gitinspector/lib/python2.7/site-packages/gitinspector/comment.py
# Compiled at: 2015-08-05 12:31:15
from __future__ import unicode_literals
__comment_begining__ = {b'java': b'/*', b'c': b'/*', b'cc': b'/*', b'cpp': b'/*', b'h': b'/*', b'hh': b'/*', b'hpp': b'/*', b'hs': b'{-', b'html': b'<!--', b'php': b'/*', 
   b'py': b'"""', b'glsl': b'/*', b'rb': b'=begin', b'js': b'/*', b'jspx': b'<!--', b'scala': b'/*', b'sql': b'/*', 
   b'tex': b'\\begin{comment}', b'xhtml': b'<!--', b'xml': b'<!--', b'ml': b'(*', b'mli': b'(*'}
__comment_end__ = {b'java': b'*/', b'c': b'*/', b'cc': b'*/', b'cpp': b'*/', b'h': b'*/', b'hh': b'*/', b'hpp': b'*/', b'hs': b'-}', b'html': b'-->', b'php': b'/*', 
   b'py': b'"""', b'glsl': b'*/', b'rb': b'=end', b'js': b'*/', b'jspx': b'-->', b'scala': b'*/', b'sql': b'*/', 
   b'tex': b'\\end{comment}', b'xhtml': b'-->', b'xml': b'-->', b'ml': b'*)', b'mli': b'*)'}
__comment__ = {b'java': b'//', b'c': b'//', b'cc': b'//', b'cpp': b'//', b'h': b'//', b'hh': b'//', b'hpp': b'//', b'hs': b'--', b'pl': b'#', b'php': b'//', b'py': b'#', 
   b'glsl': b'//', b'rb': b'#', b'js': b'//', b'scala': b'//', b'sql': b'--', b'tex': b'%', b'ada': b'--', b'ads': b'--', b'adb': b'--', 
   b'pot': b'#', b'po': b'#'}
__comment_markers_must_be_at_begining__ = {b'tex': True}

def __has_comment_begining__(extension, string):
    if __comment_markers_must_be_at_begining__.get(extension, None) == True:
        return string.find(__comment_begining__[extension]) == 0
    else:
        if __comment_begining__.get(extension, None) != None and string.find(__comment_end__[extension], 2) == -1:
            return string.find(__comment_begining__[extension]) != -1
        return False


def __has_comment_end__(extension, string):
    if __comment_markers_must_be_at_begining__.get(extension, None) == True:
        return string.find(__comment_end__[extension]) == 0
    else:
        if __comment_end__.get(extension, None) != None:
            return string.find(__comment_end__[extension]) != -1
        return False


def is_comment(extension, string):
    if __comment_begining__.get(extension, None) != None and string.strip().startswith(__comment_begining__[extension]):
        return True
    else:
        if __comment_end__.get(extension, None) != None and string.strip().endswith(__comment_end__[extension]):
            return True
        if __comment__.get(extension, None) != None and string.strip().startswith(__comment__[extension]):
            return True
        return False


def handle_comment_block(is_inside_comment, extension, content):
    comments = 0
    if is_comment(extension, content):
        comments += 1
    if is_inside_comment:
        if __has_comment_end__(extension, content):
            is_inside_comment = False
        else:
            comments += 1
    elif __has_comment_begining__(extension, content) and not __has_comment_end__(extension, content):
        is_inside_comment = True
    return (comments, is_inside_comment)