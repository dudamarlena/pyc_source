# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-build-ed191__6/Pygments/pygments/lexers/teraterm.py
# Compiled at: 2020-01-10 16:25:35
# Size of source mod 2**32: 6310 bytes
"""
    pygments.lexers.teraterm
    ~~~~~~~~~~~~~~~~~~~~~~~~

    Lexer for Tera Term macro files.

    :copyright: Copyright 2006-2019 by the Pygments team, see AUTHORS.
    :license: BSD, see LICENSE for details.
"""
import re
from pygments.lexer import RegexLexer, include, bygroups
from pygments.token import Text, Comment, Operator, Name, String, Number, Keyword
__all__ = [
 'TeraTermLexer']

class TeraTermLexer(RegexLexer):
    __doc__ = '\n    For `Tera Term <https://ttssh2.osdn.jp/>`_ macro source code.\n\n    .. versionadded:: 2.4\n    '
    name = 'Tera Term macro'
    aliases = ['ttl', 'teraterm', 'teratermmacro']
    filenames = ['*.ttl']
    mimetypes = ['text/x-teratermmacro']
    tokens = {'root':[
      include('comments'),
      include('labels'),
      include('commands'),
      include('builtin-variables'),
      include('user-variables'),
      include('operators'),
      include('numeric-literals'),
      include('string-literals'),
      include('all-whitespace'),
      (
       '[^\\s]', Text)], 
     'comments':[
      (
       ';[^\\r\\n]*', Comment.Single),
      (
       '/\\*', Comment.Multiline, 'in-comment')], 
     'in-comment':[
      (
       '\\*/', Comment.Multiline, '#pop'),
      (
       '[^*/]+', Comment.Multiline),
      (
       '[*/]', Comment.Multiline)], 
     'labels':[
      (
       '(?i)^(\\s*)(:[0-9a-z_]+)', bygroups(Text, Name.Label))], 
     'commands':[
      (
       '(?i)\\b(basename|beep|bplusrecv|bplussend|break|bringupbox|callmenu|changedir|checksum16|checksum16file|checksum32|checksum32file|checksum8|checksum8file|clearscreen|clipb2var|closesbox|closett|code2str|connect|continue|crc16|crc16file|crc32|crc32file|cygconnect|delpassword|dirname|dirnamebox|disconnect|dispstr|do|else|elseif|enablekeyb|end|endif|enduntil|endwhile|exec|execcmnd|exit|expandenv|fileclose|fileconcat|filecopy|filecreate|filedelete|filelock|filemarkptr|filenamebox|fileopen|fileread|filereadln|filerename|filesearch|fileseek|fileseekback|filestat|filestrseek|filestrseek2|filetruncate|fileunlock|filewrite|filewriteln|findclose|findfirst|findnext|flushrecv|foldercreate|folderdelete|foldersearch|for|getdate|getdir|getenv|getfileattr|gethostname|getipv4addr|getipv6addr|getmodemstatus|getpassword|getspecialfolder|gettime|gettitle|getttdir|getver|if|ifdefined|include|inputbox|int2str|intdim|ispassword|kmtfinish|kmtget|kmtrecv|kmtsend|listbox|loadkeymap|logautoclosemode|logclose|loginfo|logopen|logpause|logrotate|logstart|logwrite|loop|makepath|messagebox|mpause|next|passwordbox|pause|quickvanrecv|quickvansend|random|recvln|regexoption|restoresetup|return|rotateleft|rotateright|scprecv|scpsend|send|sendbreak|sendbroadcast|sendfile|sendkcode|sendln|sendlnbroadcast|sendlnmulticast|sendmulticast|setbaud|setdate|setdebug|setdir|setdlgpos|setdtr|setecho|setenv|setexitcode|setfileattr|setflowctrl|setmulticastname|setpassword|setrts|setsync|settime|settitle|show|showtt|sprintf|sprintf2|statusbox|str2code|str2int|strcompare|strconcat|strcopy|strdim|strinsert|strjoin|strlen|strmatch|strremove|strreplace|strscan|strspecial|strsplit|strtrim|testlink|then|tolower|toupper|unlink|until|uptime|var2clipb|wait|wait4all|waitevent|waitln|waitn|waitrecv|waitregex|while|xmodemrecv|xmodemsend|yesnobox|ymodemrecv|ymodemsend|zmodemrecv|zmodemsend)\\b',
       Keyword),
      (
       '(?i)(call|goto)([ \\t]+)([0-9a-z_]+)',
       bygroups(Keyword, Text, Name.Label))], 
     'builtin-variables':[
      (
       '(?i)(groupmatchstr1|groupmatchstr2|groupmatchstr3|groupmatchstr4|groupmatchstr5|groupmatchstr6|groupmatchstr7|groupmatchstr8|groupmatchstr9|param1|param2|param3|param4|param5|param6|param7|param8|param9|paramcnt|params|inputstr|matchstr|mtimeout|result|timeout)\\b',
       Name.Builtin)], 
     'user-variables':[
      (
       '(?i)[A-Z_][A-Z0-9_]*', Name.Variable)], 
     'numeric-literals':[
      (
       '(-?)([0-9]+)', bygroups(Operator, Number.Integer)),
      (
       '(?i)\\$[0-9a-f]+', Number.Hex)], 
     'string-literals':[
      (
       '(?i)#(?:[0-9]+|\\$[0-9a-f]+)', String.Char),
      (
       "'", String.Single, 'in-single-string'),
      (
       '"', String.Double, 'in-double-string')], 
     'in-general-string':[
      (
       '[\\\\][\\\\nt]', String.Escape),
      (
       '.', String)], 
     'in-single-string':[
      (
       "'", String.Single, '#pop'),
      include('in-general-string')], 
     'in-double-string':[
      (
       '"', String.Double, '#pop'),
      include('in-general-string')], 
     'operators':[
      (
       'and|not|or|xor', Operator.Word),
      (
       '[!%&*+<=>^~\\|\\/-]+', Operator),
      (
       '[()]', String.Symbol)], 
     'all-whitespace':[
      (
       '[\\s]+', Text)]}

    def analyse_text(text):
        result = 0.0
        if re.search(TeraTermLexer.tokens['commands'][0][0], text):
            result += 0.01
        return result