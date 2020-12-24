# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/reviewboard/scmtools/clearcase.py
# Compiled at: 2020-02-11 04:03:56
from __future__ import unicode_literals
import logging, os, platform, re, subprocess, sys
from reviewboard.diffviewer.parser import DiffParser
from reviewboard.scmtools.core import SCMTool, HEAD, PRE_CREATION
from reviewboard.scmtools.errors import SCMError, FileNotFoundError
if sys.platform.startswith(b'win') or sys.platform.startswith(b'cygwin'):
    import ntpath as cpath
else:
    import posixpath as cpath
_popen_shell = sys.version_info[:2] == (2, 7) and platform.system() == b'Windows' and platform.release() == b'7'

class ClearCaseTool(SCMTool):
    scmtool_id = b'clearcase'
    name = b'ClearCase'
    field_help_text = {b'path': b'The absolute path to the VOB.'}
    dependencies = {b'executables': [
                      b'cleartool']}
    UNEXTENDED = re.compile(b'^(.+?)/|/?(.+?)/main/?.*?/([0-9]+|CHECKEDOUT)')
    VIEW_SNAPSHOT, VIEW_DYNAMIC, VIEW_UNKNOWN = range(3)

    def __init__(self, repository):
        self.repopath = repository.path
        SCMTool.__init__(self, repository)
        self.viewtype = self._get_view_type(self.repopath)
        if self.viewtype == self.VIEW_SNAPSHOT:
            self.client = ClearCaseSnapshotViewClient(self.repopath)
        elif self.viewtype == self.VIEW_DYNAMIC:
            self.client = ClearCaseDynamicViewClient(self.repopath)
        else:
            raise SCMError(b'Unsupported view type.')

    def unextend_path(self, extended_path):
        """Remove ClearCase revision and branch informations from path.

        ClearCase paths contain additional informations about branch
        and file version preceded by @@. This function remove this
        parts from ClearCase path to make it more readable
        For example this function convert extended path::

            /vobs/comm@@/main/122/network@@/main/55/sntp
            @@/main/4/src@@/main/1/sntp.c@@/main/8

        to the the to regular path::

            /vobs/comm/network/sntp/src/sntp.c
        """
        if b'@@' not in extended_path:
            return (HEAD, extended_path)
        unextended_chunks = [ b or a for a, b, foo in self.UNEXTENDED.findall(extended_path.replace(b'@@', b''))
                            ]
        if sys.platform.startswith(b'win'):
            if unextended_chunks[0].endswith(b':'):
                unextended_chunks[0] = b'%s\\' % unextended_chunks[0]
            elif unextended_chunks[0] == b'/' or unextended_chunks[0] == os.sep:
                unextended_chunks[0] = b'\\\\'
        unextended_path = cpath.realpath(cpath.join(*unextended_chunks))
        revision = extended_path.rsplit(b'@@', 1)[1]
        if revision.endswith(b'CHECKEDOUT'):
            revision = HEAD
        return (revision, unextended_path)

    @classmethod
    def relpath(cls, path, start):
        """Wrapper for os.path.relpath for Python 2.4.

        Python 2.4 doesn't have the os.path.relpath function, so this
        approximates it well enough for our needs.

        ntpath.relpath() overflows and throws TypeError for paths containing
        atleast 520 characters (not that hard to encounter in UCM
        repository).
        """
        try:
            return cpath.relpath(path, start)
        except (AttributeError, TypeError):
            if start[(-1)] != os.sep:
                start += os.sep
            return path[len(start):]

    def normalize_path_for_display(self, filename):
        """Return display friendly path without revision informations.

        In path construct for only display purpuse we don't need
        information about branch, version or even repository path
        so we return unextended path relative to repopath (view)
        """
        return self.relpath(self.unextend_path(filename)[1], self.repopath)

    def get_repository_info(self):
        vobstag = self._get_vobs_tag(self.repopath)
        return {b'repopath': self.repopath, 
           b'uuid': self._get_vobs_uuid(vobstag)}

    def _get_view_type(self, repopath):
        cmdline = [
         b'cleartool', b'lsview', b'-full', b'-properties', b'-cview']
        p = subprocess.Popen(cmdline, stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd=repopath, shell=_popen_shell)
        res, error = p.communicate()
        failure = p.poll()
        if failure:
            raise SCMError(error)
        for line in res.splitlines(True):
            splitted = line.split(b' ')
            if splitted[0] == b'Properties:':
                if b'snapshot' in splitted:
                    return self.VIEW_SNAPSHOT
                if b'dynamic' in splitted:
                    return self.VIEW_DYNAMIC

        return self.VIEW_UNKNOWN

    def _get_vobs_tag(self, repopath):
        cmdline = [
         b'cleartool', b'describe', b'-short', b'vob:.']
        p = subprocess.Popen(cmdline, stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd=self.repopath, shell=_popen_shell)
        res, error = p.communicate()
        failure = p.poll()
        if failure:
            raise SCMError(error)
        return res.rstrip()

    def _get_vobs_uuid(self, vobstag):
        cmdline = [
         b'cleartool', b'lsvob', b'-long', vobstag]
        p = subprocess.Popen(cmdline, stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd=self.repopath, shell=_popen_shell)
        res, error = p.communicate()
        failure = p.poll()
        if failure:
            raise SCMError(error)
        for line in res.splitlines(True):
            if line.startswith(b'Vob family uuid:'):
                return line.split(b' ')[(-1)].rstrip()

        raise SCMError(b"Can't find familly uuid for vob: %s" % vobstag)

    def _get_object_kind(self, extended_path):
        cmdline = [
         b'cleartool', b'desc', b'-fmt', b'%m', extended_path]
        p = subprocess.Popen(cmdline, stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd=self.repopath, shell=_popen_shell)
        res, error = p.communicate()
        failure = p.poll()
        if failure:
            raise SCMError(error)
        return res.strip()

    def get_file(self, extended_path, revision=HEAD, **kwargs):
        """Return content of file or list content of directory"""
        if not extended_path:
            raise FileNotFoundError(extended_path, revision)
        if revision == PRE_CREATION:
            return b''
        if self.viewtype == self.VIEW_SNAPSHOT:
            file_path = extended_path.rsplit(b'@@', 1)[0] + b'@@'
            okind = self._get_object_kind(file_path)
            if okind == b'directory element':
                raise SCMError(b'Directory elements are unsupported.')
            elif okind == b'file element':
                output = self.client.cat_file(extended_path, revision)
            else:
                raise FileNotFoundError(extended_path, revision)
        elif cpath.isdir(extended_path):
            output = self.client.list_dir(extended_path, revision)
        elif cpath.exists(extended_path):
            output = self.client.cat_file(extended_path, revision)
        else:
            raise FileNotFoundError(extended_path, revision)
        return output

    def parse_diff_revision(self, extended_path, revision_str, *args, **kwargs):
        """Guess revision based on extended_path.

        Revision is part of file path, called extended-path,
        revision_str contains only modification's timestamp.
        """
        if extended_path.endswith(os.path.join(os.sep, b'main', b'0')):
            revision = PRE_CREATION
        elif extended_path.endswith(b'CHECKEDOUT') or b'@@' not in extended_path:
            revision = HEAD
        else:
            revision = extended_path.rsplit(b'@@', 1)[1]
        return (extended_path, revision)

    def get_parser(self, data):
        return ClearCaseDiffParser(data, self.repopath, self._get_vobs_tag(self.repopath))


class ClearCaseDiffParser(DiffParser):
    """
    Special parsing for diffs created with the post-review for ClearCase.
    """
    SPECIAL_REGEX = re.compile(b'^==== (\\S+) (\\S+) ====$')

    def __init__(self, data, repopath, vobstag):
        self.repopath = repopath
        self.vobstag = vobstag
        super(ClearCaseDiffParser, self).__init__(data)

    def parse_diff_header(self, linenum, info):
        """Obtain correct clearcase file paths.

        Paths for the same file may differ from paths in developer view
        because it depends from configspec and this is custom so we
        translate oids, attached by post-review, to filenames to get paths
        working well inside clearcase view on reviewboard side.
        """
        linenum = super(ClearCaseDiffParser, self).parse_diff_header(linenum, info)
        m = self.SPECIAL_REGEX.match(self.lines[linenum])
        if m:
            currentFilename = info.get(b'origFile', b'')
            try:
                info[b'origFile'] = self._oid2filename(m.group(1))
            except:
                logging.debug(b'oid (%s) not found, get filename from client', m.group(1))
                info[b'origFile'] = self.client_relpath(currentFilename)

            currentFilename = info.get(b'newFile', b'')
            try:
                info[b'newFile'] = self._oid2filename(m.group(2))
            except:
                logging.debug(b'oid (%s) not found, get filename from client', m.group(2))
                info[b'newFile'] = self.client_relpath(currentFilename)

            linenum += 1
            if linenum < len(self.lines) and (self.lines[linenum].startswith(b'Binary files ') or self.lines[linenum].startswith(b'Files ')):
                info[b'origInfo'] = b''
                info[b'newInfo'] = b''
                info[b'binary'] = True
                linenum += 1
        return linenum

    def _oid2filename(self, oid):
        cmdline = [
         b'cleartool', b'describe', b'-fmt', b'%En@@%Vn', b'oid:%s' % oid]
        p = subprocess.Popen(cmdline, stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd=self.repopath, shell=_popen_shell)
        res, error = p.communicate()
        failure = p.poll()
        if failure:
            raise SCMError(error)
        drive = os.path.splitdrive(self.repopath)[0]
        if drive:
            res = os.path.join(drive, res)
        return ClearCaseTool.relpath(res, self.repopath)

    def client_relpath(self, filename):
        """Normalize any path sent from client view and return relative path
        against vobtag
        """
        try:
            path, revision = filename.split(b'@@', 1)
        except ValueError:
            path = filename
            revision = None

        relpath = b''
        logging.debug(b'vobstag: %s, path: %s', self.vobstag, path)
        while True:
            if path == b'/':
                logging.debug(b'vobstag not found in path, use client filename')
                return filename
            if path.endswith(self.vobstag):
                break
            path, basename = os.path.split(path)
            if len(relpath) == 0:
                relpath = basename
            else:
                relpath = os.path.join(basename, relpath)

        logging.debug(b'relpath: %s', relpath)
        if revision:
            relpath = relpath + b'@@' + revision
        return relpath


class ClearCaseDynamicViewClient(object):

    def __init__(self, path):
        self.path = path

    def cat_file(self, filename, revision):
        with open(filename, b'rb') as (f):
            return f.read()

    def list_dir(self, path, revision):
        return (b'').join([ b'%s\n' % s for s in sorted(os.listdir(path))
                          ])


class ClearCaseSnapshotViewClient(object):

    def __init__(self, path):
        self.path = path

    def cat_file(self, extended_path, revision):
        import tempfile
        temp = tempfile.NamedTemporaryFile()
        temp.close()
        cmdline = [
         b'cleartool', b'get', b'-to', temp.name, extended_path]
        p = subprocess.Popen(cmdline, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=_popen_shell)
        res, error = p.communicate()
        failure = p.poll()
        if failure:
            raise FileNotFoundError(extended_path, revision)
        try:
            with open(temp.name, b'rb') as (f):
                return f.read()
        except:
            raise FileNotFoundError(extended_path, revision)