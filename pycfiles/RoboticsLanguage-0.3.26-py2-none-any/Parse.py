# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/glopes/Projects/RoboticsLanguage/RoboticsLanguage/Inputs/Shell/Parse.py
# Compiled at: 2019-09-09 15:48:17
from RoboticsLanguage.Tools import Parsing

def shellLanguageEscape(text):
    return text.replace('\\', '\\\\').replace('"', '\\"').replace('\n', '\\n\\\n')


def parse(text, parameters):
    code = Parsing.xmlNamespace('shell')('script', text=shellLanguageEscape(text))
    return (
     code, parameters)