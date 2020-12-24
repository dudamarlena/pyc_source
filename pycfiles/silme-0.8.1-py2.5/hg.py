# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-i386/egg/silme/io/hg.py
# Compiled at: 2010-06-12 17:55:55
import silme.io, silme.format
from silme.io.clients import IOClient, RCSClient
from silme.core.object import L10nPackage, L10nObject, Blob
from mercurial import hg, ui, commands, context
import os

def register(Manager):
    Manager.register(HgClient)


class HgClient(RCSClient):
    name = 'hg'
    desc = 'Mercurial Client'
    type = IOClient.__name__

    @classmethod
    def matches_path(cls, path):
        """
        tests if the ioclient should be used for this type of path
        example: hg:http://localhost/ or hg://localhost
        """
        return path.startswith('hg:')

    @classmethod
    def get_blob(cls, path, source=True):
        (p, rev) = cls._explode_path(path)
        blob = Blob()
        blob.id = os.path.basename(path)
        if source:
            blob.source = cls.get_source_without_encoding(p)
        blob.uri = p
        return blob

    @classmethod
    def _explode_path(cls, path):
        return (path, 0)

    @classmethod
    def _read_with_encoding(cls, path, encoding):
        client = pysvn.Client()
        text = client.cat(path, revision=pysvn.Revision(pysvn.opt_revision_kind.head))
        return text

    @classmethod
    def _read_without_encoding(cls, path):
        repo = hg.repository(ui.ui(), 'http://hg.mozilla.org/webtools/mcs/')
        print repo
        text = commands.cat(ui, repo, 'theme/html/index.html')
        return text