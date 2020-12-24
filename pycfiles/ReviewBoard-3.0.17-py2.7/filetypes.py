# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/reviewboard/diffviewer/filetypes.py
# Compiled at: 2020-02-11 04:03:56
from __future__ import unicode_literals
import re
HEADER_REGEXES = {b'.cs': [
          re.compile(b'^\\s*((public|private|protected|static)\\s+)+([a-zA-Z_][a-zA-Z0-9_\\.\\[\\]]*\\s+)+?[a-zA-Z_][a-zA-Z0-9_]*\\s*\\('),
          re.compile(b'^\\s*((public|static|private|protected|internal|abstract|partial)\\s+)*(class|struct)\\s+([A-Za-z0-9_])+')], 
   b'.c': [
         re.compile(b'^@(interface|implementation|class|protocol)'),
         re.compile(b'^[A-Za-z0-9$_]')], 
   b'.java': [
            re.compile(b'^\\s*((public|private|protected|static)\\s+)+([a-zA-Z_][a-zA-Z0-9_\\.\\[\\]]*\\s+)+?[a-zA-Z_][a-zA-Z0-9_]*\\s*\\('),
            re.compile(b'^\\s*((public|static|private|protected)\\s+)*(class|struct)\\s+([A-Za-z0-9_])+')], 
   b'.js': [
          re.compile(b'^\\s*function [A-Za-z0-9_]+\\s*\\('),
          re.compile(b'^\\s*(var\\s+)?[A-Za-z0-9_]+\\s*[=:]\\s*function\\s*\\(')], 
   b'.m': [
         re.compile(b'^@(interface|implementation|class|protocol)'),
         re.compile(b'^[-+]\\s+\\([^\\)]+\\)\\s+[A-Za-z0-9_]+[^;]*$'),
         re.compile(b'^[A-Za-z0-9$_]')], 
   b'.php': [
           re.compile(b'^\\s*(public|private|protected)?\\s*(class|function) [A-Za-z0-9_]+')], 
   b'.pl': [
          re.compile(b'^\\s*sub [A-Za-z0-9_]+')], 
   b'.py': [
          re.compile(b'^\\s*(def|class) [A-Za-z0-9_]+\\s*\\(?')], 
   b'.rb': [
          re.compile(b'^\\s*(def|class) [A-Za-z0-9_]+\\s*\\(?')]}
HEADER_REGEX_ALIASES = {b'.cc': b'.c', 
   b'.cpp': b'.c', 
   b'.cxx': b'.c', 
   b'.c++': b'.c', 
   b'.h': b'.c', 
   b'.hh': b'.c', 
   b'.hpp': b'.c', 
   b'.hxx': b'.c', 
   b'.h++': b'.c', 
   b'.C': b'.c', 
   b'.H': b'.c', 
   b'.mm': b'.m', 
   b'.pm': b'.pl', 
   b'SConstruct': b'.py', 
   b'SConscript': b'.py', 
   b'.pyw': b'.py', 
   b'.sc': b'.py', 
   b'Rakefile': b'.rb', 
   b'.rbw': b'.rb', 
   b'.rake': b'.rb', 
   b'.gemspec': b'.rb', 
   b'.rbx': b'.rb'}