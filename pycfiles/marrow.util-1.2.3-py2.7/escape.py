# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.8-intel/egg/marrow/util/escape.py
# Compiled at: 2012-07-26 02:07:58
import re
__all__ = [
 'escape_slashes', 'escape_percents', 'unescape']
escapes = re.compile('(\\\\[^\\\\]\\([^\\)]+\\)|\\\\[^\\\\]|\\\\\\\\|%[^%][\\w]?|%%|\\$\\([^\\)]+\\)|\\$\\$)')
escape_slashes = dict(t='\t', n='\n', r='\r', k='\x1b[K', rk='\r\x1b[K')
escape_slashes['s(normal)'] = '\x1b[0m'
escape_slashes['s(bold)'] = '\x1b[1m'
escape_slashes['s(intense)'] = '\x1b[1m'
escape_slashes['s(dim)'] = '\x1b[2m'
escape_slashes['s(italic)'] = '\x1b[3m'
escape_slashes['s(underline)'] = '\x1b[4m'
escape_slashes['s(inverse)'] = '\x1b[7m'
escape_slashes['s(hidden)'] = '\x1b[8m'
escape_slashes['s(strike)'] = '\x1b[9m'
escape_slashes['c(black)'] = '\x1b[30m'
escape_slashes['c(red)'] = '\x1b[31m'
escape_slashes['c(green)'] = '\x1b[32m'
escape_slashes['c(yellow)'] = '\x1b[33m'
escape_slashes['c(blue)'] = '\x1b[34m'
escape_slashes['c(magenta)'] = '\x1b[35m'
escape_slashes['c(cyan)'] = '\x1b[36m'
escape_slashes['c(white)'] = '\x1b[37m'
escape_slashes['c(default)'] = '\x1b[39m'
escape_slashes['b(black)'] = '\x1b[40m'
escape_slashes['b(red)'] = '\x1b[41m'
escape_slashes['b(green)'] = '\x1b[42m'
escape_slashes['b(yellow)'] = '\x1b[43m'
escape_slashes['b(blue)'] = '\x1b[44m'
escape_slashes['b(magenta)'] = '\x1b[45m'
escape_slashes['b(cyan)'] = '\x1b[46m'
escape_slashes['b(white)'] = '\x1b[47m'
escape_slashes['b(default)'] = '\x1b[49m'
escape_percents = dict(t='\t', r='\n', b=' ')

def unescape(caller, text, obj=None):
    gender = getattr(caller, 'gender', caller.get('gender', 'it'))[0] if caller else 'i'
    local_slashes = dict()
    local_percents = dict(s=dict(m='he', f='she', i='it', o='it', n='ze', s='e', g='they')[gender], o=dict(m='him', f='her', i='it', o='it', n='hir', s='em', g='them')[gender], v=dict(m='him', f='her', i='it', o='it', n='hir', s='em', g='them')[gender], p=dict(m='his', f='her', i='its', o='its', n='hir', s='eir', g='their')[gender], a=dict(m='his', f='hers', i='its', o='its', n='hirs', s='eirs', g='theirs')[gender], f=dict(m='himself', f='herself', i='itself', o='itself', n='hirself', s='emself', g='themselves')[gender], S=dict(m='He', f='She', i='It', o='It', n='Ze', s='E', g='They')[gender], O=dict(m='Him', f='Her', i='It', o='It', n='Hir', s='Em', g='Them')[gender], V=dict(m='Him', f='Her', i='It', o='It', n='Hir', s='Em', g='Them')[gender], P=dict(m='His', f='Her', i='Its', o='Its', n='Hir', s='Eir', g='Their')[gender], A=dict(m='His', f='Hers', i='Its', o='Its', n='hirs', s='Eirs', g='Theirs')[gender], F=dict(m='Himself', f='Herself', i='Itself', o='Itself', n='Hirself', s='Emself', g='Themselves')[gender], N=getattr(caller, 'name', caller.get('name', 'Anonymous')) if caller else 'Anonymous')
    local_percents['#'] = '#%s' % (getattr(caller, 'id', caller.get('id', '%#')),) if caller else '%#'
    local_percents['@'] = local_percents['#']

    def process(match):
        match = match.group(0)
        if match == '\\\\':
            return '\\'
        else:
            if match == '%%':
                return '%'
            if match == '$$':
                return '$'
            if match.startswith('\\') and match[1:] in escape_slashes:
                return escape_slashes[match[1:]]
            if match.startswith('%') and match[1:] in escape_slashes:
                return escape_slashes[match[1:]]
            if match.startswith('\\') and match[1:] in local_slashes:
                return local_slashes[match[1:]]
            if match.startswith('%') and match[1:] in local_percents:
                return local_percents[match[1:]]
            if match.startswith('$(') and match.endswith(')') and obj:
                match = match[2:-1].split('.')
                ref = obj
                for i in match:
                    ref = getattr(ref, i, ref.get(i, None))

                return unescape(caller, str(ref), obj)
            return match

    return escapes.sub(process, text)