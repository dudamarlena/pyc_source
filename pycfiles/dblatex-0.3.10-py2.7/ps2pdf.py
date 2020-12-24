# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/dbtexmf/dblatex/grubber/ps2pdf.py
# Compiled at: 2017-04-03 18:58:57
"""
PostScript to PDF conversion using GhostScript.
"""
import sys, os
from msg import _, msg
from maker import DependShell
from plugins import TexModule

class Module(TexModule):

    def __init__(self, doc, dict):
        env = doc.env
        ps = env.dep_last().prods[0]
        root, ext = os.path.splitext(ps)
        if ext != '.ps':
            msg.error(_("I can't use ps2pdf when not producing a PS"))
            sys.exit(2)
        pdf = root + '.pdf'
        cmd = ['ps2pdf']
        for opt in doc.paper.split():
            cmd.append('-sPAPERSIZE=' + opt)

        cmd.extend([ps, pdf])
        dep = DependShell(env, cmd, prods=[pdf], sources={ps: env.dep_last()})
        env.dep_append(dep)