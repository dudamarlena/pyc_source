# uncompyle6 version 3.7.4
# Python bytecode 2.3 (62011)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/pyclearsilver/wordwrap.py
# Compiled at: 2004-05-24 13:56:39
"""
WordWrapping
"""
import os, sys, string, time, getopt, re

def WordWrap(text, cols=70, detect_paragraphs=0, is_header=0):
    text = string.replace(text, '\r\n', '\n')

    def nlrepl(matchobj):
        if matchobj.group(1) != ' ' and matchobj.group(2) != ' ':
            repl_with = ' '
        else:
            repl_with = ''
        return matchobj.group(1) + repl_with + matchobj.group(2)

    if detect_paragraphs:
        text = re.sub('([^\n])\n([^\n])', nlrepl, text)
    body = []
    i = 0
    j = 0
    ltext = len(text)
    while i < ltext:
        if i + cols < ltext:
            r = string.find(text, '\n', i, i + cols)
            j = r
            if r == -1:
                j = string.rfind(text, ' ', i, i + cols)
                if j == -1:
                    r = string.find(text, '\n', i + cols)
                    if r == -1:
                        r = ltext
                    j = string.find(text, ' ', i + cols)
                    if j == -1:
                        j = ltext
                    j = min(j, r)
        else:
            j = ltext
        body.append(string.strip(text[i:j]))
        i = j + 1

    if is_header:
        body = string.join(body, '\n ')
    else:
        body = string.join(body, '\n')
    return body