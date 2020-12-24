# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/dbtexmf/dblatex/grubber/xr-hyper.py
# Compiled at: 2017-04-03 18:58:57
"""
Dependency analysis for the xr package.

The xr package allows one to put references in one document to other
(external) LaTeX documents. It works by reading the external document's .aux
file, so this support package registers these files as dependencies.
"""
import os
from msg import _, msg
from plugins import TexModule
from latex import Latex

class Module(TexModule):

    def __init__(self, doc, dict):
        self.doc = doc
        self.env = doc.env
        self.texmodules = []
        for m in ('pdftex', 'xetex'):
            if doc.modules.has_key(m):
                self.texmodules.append(m)

        doc.parser.add_hook('externaldocument', self.externaldocument)

    def externaldocument(self, dict):
        auxfile = dict['arg'] + '.aux'
        texfile = dict['arg'] + '.tex'
        if not os.path.isfile(texfile):
            msg.log(_('file %s is required by xr package but not found') % texfile, pkg='xr')
            return
        texdep = Latex(self.env)
        texdep.set_source(texfile)
        texdep.batch = self.doc.batch
        texdep.encoding = self.doc.encoding
        texdep.draft_only = True
        for m in self.texmodules:
            texdep.modules.register(m)

        texdep.prepare(exclude_mods=['xr-hyper'])
        self.doc.sources[auxfile] = texdep
        msg.log(_('dependency %s added for external references') % auxfile, pkg='xr')