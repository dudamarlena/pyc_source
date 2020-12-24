# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-i386/egg/silme/io/svn.py
# Compiled at: 2010-06-12 17:55:55
import silme.io
from silme.core import Blob
from silme.io.clients import IOClient, RCSClient
import silme.format
from silme.core import L10nPackage
from file import FileClient
import pysvn, os, shutil, codecs, re

def register(Manager):
    Manager.register(SVNClient)


class SVNClient(RCSClient):
    name = 'svn'
    desc = 'SVN Client'
    type = IOClient.__name__
    client = None

    def __init__(self):
        self.user = {'login': None, 'password': None}
        return

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
    def get_entitylist(cls, path, source=False, code='default', parser=None):
        (p, rev) = cls._explode_path(path)
        if not parser:
            parser = silme.format.Manager.get(path=p)
        src = cls.get_source(p, encoding=parser.encoding, fallback=parser.fallback)
        entitylist = parser.get_entitylist(src[0], code=code)
        entitylist.id = os.path.basename(p)
        entitylist.uri = p
        if source:
            entitylist.source = src[0]
        entitylist.encoding = src[1]
        return entitylist

    @classmethod
    def get_l10nobject(cls, path, source=False, code='default', parser=None):
        (p, rev) = cls._explode_path(path)
        if not parser:
            parser = silme.format.Manager.get(path=p)
        src = cls.get_source(p, encoding=parser.encoding, fallback=parser.fallback)
        l10nobject = parser.get_l10nobject(src[0], code=code)
        l10nobject.id = os.path.basename(p)
        l10nobject.uri = p
        if source:
            l10nobject.source = src[0]
        l10nobject.encoding = src[1]
        return l10nobject

    @classmethod
    def get_l10npackage(cls, path, code='default', object_type='l10nobject', source=None, ignore=[
 'CVS', '.svn', '.DS_Store', '.hg']):
        (p, rev) = cls._explode_path(path)
        l10npackage = L10nPackage()
        l10npackage.id = os.path.basename(p)
        l10npackage.uri = p
        if source is None:
            b_source = True
            oe_source = False
        elif source is False:
            b_source = False
            oe_source = False
        else:
            b_source = True
            oe_source = True
        cls.client = pysvn.Client()
        entry_list = cls.client.list(path, recurse=True)
        for i in entry_list:
            elem = os.path.basename(i[0].path)
            if ignore.__class__.__name__ == 'function':
                if ignore(i[0].path):
                    continue
                elif os.path.basename(i[0].path) in ignore:
                    continue
            if i[0].kind == pysvn.node_kind.file:
                dirname = os.path.dirname(i[0].path)
                filename = os.path.basename(i[0].path)
                relpath = re.sub(os.path.dirname(p), '', dirname, 1)
                if relpath.startswith('/'):
                    relpath = os.path.split(relpath)[1]
                try:
                    parser = silme.format.Manager.get(path=elem)
                except Exception:
                    l10npackage.add_object(cls.get_blob(i[0].path, source=b_source), relpath)
                else:
                    if object_type == 'object':
                        l10npackage.add_object(cls.get_blob(i[0].path, source=b_source), relpath)
                    elif object_type == 'entitylist':
                        l10npackage.add_objects(cls.get_entitylist(i[0].path, source=oe_source, code=code, parser=parser), relpath)
                    else:
                        l10npackage.add_objects(cls.get_l10nobject(i[0].path, source=oe_source, code=code, parser=parser), relpath)

        return l10npackage

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
        client = pysvn.Client()
        text = client.cat(path, revision=pysvn.Revision(pysvn.opt_revision_kind.head))
        return text