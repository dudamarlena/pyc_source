# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.14-intel/egg/bashlex/flags.py
# Compiled at: 2019-03-01 15:42:24
import enum
parser = enum.Enum('parserflags', [
 'CASEPAT',
 'ALEXPNEXT',
 'ALLOWOPNBRC',
 'NEEDCLOSBRC',
 'DBLPAREN',
 'SUBSHELL',
 'CMDSUBST',
 'CASESTMT',
 'CONDCMD',
 'CONDEXPR',
 'ARITHFOR',
 'ALEXPAND',
 'EXTPAT',
 'COMPASSIGN',
 'ASSIGNOK',
 'EOFTOKEN',
 'REGEXP',
 'HEREDOC',
 'REPARSE',
 'REDIRLIST'])
word = enum.Enum('wordflags', [
 'HASDOLLAR',
 'QUOTED',
 'ASSIGNMENT',
 'SPLITSPACE',
 'NOSPLIT',
 'NOGLOB',
 'NOSPLIT2',
 'TILDEEXP',
 'DOLLARAT',
 'DOLLARSTAR',
 'NOCOMSUB',
 'ASSIGNRHS',
 'NOTILDE',
 'ITILDE',
 'NOEXPAND',
 'COMPASSIGN',
 'ASSNBLTIN',
 'ASSIGNARG',
 'HASQUOTEDNULL',
 'DQUOTE',
 'NOPROCSUB',
 'HASCTLESC',
 'ASSIGNASSOC',
 'ASSIGNARRAY',
 'ARRAYIND',
 'ASSNGLOBAL',
 'NOBRACE',
 'ASSIGNINT'])