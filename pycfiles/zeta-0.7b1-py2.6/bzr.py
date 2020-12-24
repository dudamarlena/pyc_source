# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/zeta/lib/vcs/bzr.py
# Compiled at: 2010-07-11 03:19:00
"""Bazaar binding for Zeta version control system"""
import re, os
from os.path import commonprefix, join
import time, datetime as dt, difflib as dl
from pytz import timezone
from bzrlib import branch, bzrdir, errors, inventory, osutils, revision, transport
from bzrlib.log import Logger
import bzrlib.api as bzrapi
from bzrlib.revision import CURRENT_REVISION, NULL_REVISION
mime_type = {'directory': 'text/directory', 
   'file': 'text/file'}
changetypes = {}

class Client(object):
    """Bazaar Client definition"""
    xdelist = [
     '.bzr']

    def __init__(self, rooturl):
        self.rooturl = rooturl
        self.apiver = bzrapi.get_current_api_version(None)
        self.trans = transport.get_transport(rooturl)
        self.branch = bzrdir.BzrDir.open_from_transport(self.trans).open_branch()
        self.branch.lock_read()
        self.revmaps = self.branch.get_revision_id_to_revno_map()
        self.currevno = self.branch.revno()
        return

    def __del__(self):
        self.branch.unlock()

    def info(self, url=None, revno=None):
        revno = revno or self.currevno
        try:
            (revno, revid) = self._normalizerev(revno)
            r = revid and self._revision(revid)
            author = self._author(r.committer)
            utcdt = self._datetime(r.timestamp, r.timezone)
            relpath = url and self._relpath(url)
            node = relpath and self._node(relpath, revid)
        except:
            revno = 0
            author = '-'
            utcdt = None
            node = None

        idict = {'l_revision': self._revno(revid), 'l_author': author, 
           'l_date': utcdt}
        ndict = {}
        if node:
            ndict = {'mime_type': mime_type[node.kind], 'size': node.text_size, 'repos_path': relpath}
        idict.update(ndict)
        return idict

    def list(self, url, revno=None, recurse=False):
        revno = revno or self.currevno
        try:
            (revno, revid) = self._normalizerev(revno)
            relpath = url and self._relpath(url) or '.'
            node = relpath and self._node(relpath, revid)
        except:
            revno = None
            node = None

        ldir = []
        try:
            if node and node.kind == 'directory':
                entries = self.trans.list_dir(relpath)
                for child in self._filterde(entries):
                    crpath = relpath + '/' + child
                    cnode = self._node(crpath, revid)
                    if not cnode:
                        continue
                    r = self._revision(cnode.revision)
                    author = self._author(r.committer)
                    utcdt = self._datetime(r.timestamp, r.timezone)
                    ldir.append([
                     self._revno(cnode.revision),
                     mime_type[cnode.kind],
                     join(self.rooturl, relpath, child),
                     author,
                     cnode.text_size,
                     utcdt.strftime('%m/%d/%Y'),
                     crpath])

        except:
            ldir = []

        return ldir

    def cat(self, url, revno=None, annotate=False):
        revno = revno or self.currevno
        try:
            (revno, revid) = self._normalizerev(revno)
            relpath = url and self._relpath(url)
            node = relpath and self._node(relpath, revid)
        except:
            revid = 0
            node = None

        annotations = []
        try:
            if node and revid:
                tree = self._tree(revid)
                annotations = tree.annotate_iter(node.file_id)
        except:
            annotations = []

        lineno = 1
        lines = []
        try:
            for (revid, line) in annotations:
                r = self._revision(revid)
                author = self._author(r.committer)
                utcdt = self._datetime(r.timestamp, r.timezone)
                lineno += 1
                lines.append([lineno,
                 line.strip('\r\n'),
                 self._revno(revid),
                 author,
                 utcdt])

        except:
            lines = []

        return lines

    def diff(self, url, revno1, revno2, url2=None):
        revno2 = revno2 or self.currevno
        revno1 = revno1 or 1
        try:
            (revno1, revid1) = self._normalizerev(revno1)
            (revno2, revid2) = self._normalizerev(revno2)
            relpath1 = url and self._relpath(url)
            relpath2 = url2 and self._relpath(url2) or relpath1
            tree1 = self._tree(revid1)
            tree2 = self._tree(revid2)
            node1 = self._node(relpath1, revid1, tree=tree1)
            node2 = self._node(relpath2, revid2, tree=tree1)
            a = tree1.get_file_lines(node1.file_id)
            b = tree2.get_file_lines(node2.file_id)
            title1 = '%s (revision %s)' % (relpath1, revno1)
            title2 = '%s (revision %s)' % (relpath2, revno2)
            diffgen = dl.unified_diff(a, b, fromfile=title1, tofile=title2)
            diff = ('').join([ l for l in diffgen ])
        except:
            diff = ''

        return diff

    def logs(self, url=None, revstart=None, revend=None):
        revstart = revstart or 1
        revend = revend or self.currevno
        try:
            if url and url != self.rooturl:
                relpath = self._relpath(url)
                fileid = self._fileid(relpath, self._getrevid(revend))
                rqst = {'_match_using_deltas': None, 'delta_type': None, 
                   'diff_type': None, 
                   'direction': 'reverse', 
                   'end_revision': None, 
                   'generate_tags': True, 
                   'levels': 1, 
                   'limit': None, 
                   'message_search': None, 
                   'specific_fileids': [
                                      fileid], 
                   'start_revision': None}
                logg = Logger(None, rqst)
                genrtr = logg._generator_factory(self.branch, rqst)
                revs = [ [lr.revno, lr.rev.revision_id, lr.rev] for lr in genrtr.iter_log_revisions()
                       ]
            else:
                revs = []
            for revno in range(revstart, revend + 1):
                revid = self._getrevid(revno)
                revs.append([revno, revid, self._revision(revid)])

        except:
            revs = []

        logs = []
        try:
            for (revno, revid, r) in revs:
                logs.append([
                 r.message,
                 int(revno),
                 self._author(r.committer),
                 self._datetime(r.timestamp, r.timezone)])

        except:
            raise

        return logs

    def changedfiles(self, url, revstart, revend):
        revstart = int(revstart or 1)
        revend = int(revend or self.currevno)
        changes = []
        try:
            if url == self.rooturl:
                tree1 = self._tree(self._getrevid(revstart))
                tree2 = self._tree(self._getrevid(revend))
                delta = tree2.changes_from(tree1)
            else:
                relpath = self._relpath(url)
                tree1 = self._tree(self._getrevid(revstart))
                tree2 = self._tree(self._getrevid(revend))
                delta = tree2.changes_from(tree1, specific_files=[relpath])
        except:
            delta = None

        if delta:
            for a in delta.added:
                changes.append({'repos_path': a[0], 
                   'changetype': 'added', 
                   'mime_type': mime_type[a[2]]})

            for a in delta.removed:
                changes.append({'repos_path': a[0], 
                   'changetype': 'deleted', 
                   'mime_type': mime_type[a[2]]})

            for a in delta.modified:
                changes.append({'repos_path': a[0], 
                   'changetype': 'modified', 
                   'mime_type': mime_type[a[2]]})

        return changes

    def _normalizerev(self, revno):
        try:
            revno = revno or self._currevno()
            revid = self._getrevid(revno)
        except:
            revno = self._currevno()
            revid = self._getrevid(revno)

        return (
         revno, revid)

    def _merged2revid(self, map, allrevids, revid):
        res = [ k[0] for (k, fromlist) in map.iteritems() if (revid,) in fromlist ]
        fil = filter(lambda id: id in allrevids, res)
        if fil and fil[0]:
            merged2revid = fil[0]
        else:
            merged2revid = self._merged2revid(map, allrevids, res[0])
        return merged2revid

    def _getrevid(self, revno):
        return self.branch.get_rev_id(revno)

    def _currevno(self):
        return self.branch.revno()

    def _revision(self, revid):
        r = self.branch.repository.get_revision(revid)
        return r

    def _revno(self, revid):
        try:
            revno = self.branch.revision_id_to_revno(revid)
        except:
            try:
                map = self.branch.repository.inventories.get_parent_map(self.branch.repository.inventories.keys())
                merged2revid = self._merged2revid(map, self.branch.revision_history(), revid)
                revno = self.branch.revision_id_to_revno(merged2revid)
            except:
                revno = None

        return revno

    def _author(self, text):
        reauth = re.match('^.*(<.*>).*', text).groups()
        author = reauth and reauth[0][1:-1] or text
        return author

    def _datetime(self, timestamp, delta=0):
        timestamp = timestamp + delta
        tz = timezone('UTC')
        utcdt = tz.localize(dt.datetime(*time.localtime(timestamp)[:6]))
        return utcdt

    def _relpath(self, url):
        relpath = url and self.trans.relpath(url) or ''
        return relpath

    def _tree(self, revid):
        return self.branch.repository.revision_tree(revid)

    def _fileid(self, relpath, revid, tree=None):
        tree = tree or self._tree(revid)
        fid = tree.inventory.path2id(relpath)
        entry = fid and tree.inventory[fid].file_id
        return entry

    def _node(self, relpath, revid, tree=None):
        tree = tree or self._tree(revid)
        fid = tree.inventory.path2id(relpath)
        entry = fid and tree.inventory[fid]
        return entry

    def _filterde(self, entries):
        return filter(lambda f: f not in self.xdelist, entries)


def init(vcs):
    return Client(vcs.rooturl)


def info(self, url=None, revno=None):
    return self.client.info(url=url, revno=revno)


def list(self, url_dir, revno=None, recurse=False):
    return self.client.list(url=url_dir, revno=revno, recurse=recurse)


def cat(self, url, revno=None, annotate=False):
    return self.client.cat(url=url, revno=revno, annotate=annotate)


def diff(self, url, revno1, revno2, url2=None):
    return self.client.diff(url=url, revno1=revno1, revno2=revno2, url2=url2)


def logs(self, url, revstart=None, revend=None):
    return self.client.logs(url=url, revstart=revstart, revend=revend)


def changedfiles(self, url=None, revstart=None, revend=None):
    return self.client.changedfiles(url=url, revstart=revstart, revend=revend)