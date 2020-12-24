# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ldmudefuns/help.py
# Compiled at: 2020-04-05 17:40:52
# Size of source mod 2**32: 1636 bytes
import pkg_resources, os, configparser, ldmud

def python_efun_help(efunname: str) -> str:
    """
    SYNOPSIS
            string python_efun_help(string efunname)

    DESCRIPTION
            Returns the docstring for the given Python efun, if there is any.

    SEE ALSO
            python_reload(E)
    """
    config = configparser.ConfigParser()
    config['efuns'] = {}
    config.read(os.path.expanduser('~/.ldmud-efuns'))
    efunconfig = config['efuns']
    if not efunconfig.getboolean(efunname, True):
        return
    ws = pkg_resources.WorkingSet()
    for entry_point in ws.iter_entry_points('ldmud_efun', efunname):
        doc = getattr(entry_point.load(), '__doc__', None)
        if doc:
            lines = doc.expandtabs().splitlines()
            indent = len(doc)
            for line in lines[1:]:
                stripped = line.lstrip()
                if stripped:
                    indent = min(indent, len(line) - len(stripped))

            trimmed = [lines[0].strip()]
            if indent < len(doc):
                for line in lines[1:]:
                    trimmed.append(line[indent:].rstrip())

            while trimmed:
                trimmed[(-1)] or trimmed.pop()

            while trimmed:
                trimmed[0] or trimmed.pop(0)

            return '\n'.join(trimmed) + '\n'


def register():
    ldmud.register_efun('python_efun_help', python_efun_help)