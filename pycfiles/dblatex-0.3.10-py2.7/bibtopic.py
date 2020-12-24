# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/dbtexmf/dblatex/grubber/bibtopic.py
# Compiled at: 2017-04-03 18:58:57
from plugins import TexModule
from bibtex import BibTex

class BibSect(BibTex):

    def __init__(self, doc, bibaux, bibfiles, bibstyle):
        self.bibfiles = bibfiles.split(',')
        self.bibstyle = bibstyle
        self.bibaux = bibaux
        BibTex.__init__(self, doc, {}, bibaux)
        for bib in self.bibfiles:
            self.add_db(bib)

        if self.bibstyle:
            self.set_style(self.bibstyle)


class BibNull(BibSect):
    """
    Null biblio section having no bibfile
    """

    def __init__(self, doc, bibaux):
        pass

    def pre_compile(self):
        return 0

    def post_compile(self):
        return 0


class Bibtopic(TexModule):

    def __init__(self, doc, dict):
        self.doc = doc
        self.btsects = []
        doc.parser.add_hook('begin{btSect}', self.add_sect)
        if dict['name'] == 'begin{btSect}':
            self.add_sect(dict)

    def add_sect(self, dict):
        bibaux = '%s%d' % (self.doc.src_base, len(self.btsects) + 1)
        if dict['arg']:
            btsect = BibSect(self.doc, bibaux, dict['arg'], dict['opt'])
        else:
            btsect = BibNull(self.doc, bibaux)
        self.btsects.append(btsect)

    def pre_compile(self):
        rc = 0
        for bib in self.btsects:
            rc += bib.pre_compile()

        return rc

    def post_compile(self):
        rc = 0
        for bib in self.btsects:
            rc += bib.post_compile()

        return rc


class Module(Bibtopic):
    """
    Module to load to handle bibtopic
    """
    pass