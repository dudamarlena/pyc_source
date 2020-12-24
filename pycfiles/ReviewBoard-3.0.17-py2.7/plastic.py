# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/reviewboard/scmtools/plastic.py
# Compiled at: 2020-02-11 04:03:56
from __future__ import unicode_literals
import logging, os, re, subprocess
from tempfile import mkstemp
from django.utils import six
from django.utils.translation import ugettext_lazy as _
from djblets.util.filesystem import is_exe_in_path
from reviewboard.scmtools.core import SCMTool, ChangeSet, HEAD, PRE_CREATION
from reviewboard.scmtools.errors import SCMError, FileNotFoundError, RepositoryNotFoundError
from reviewboard.diffviewer.parser import DiffParser

class PlasticTool(SCMTool):
    scmtool_id = b'plastic'
    name = b'Plastic SCM'
    diffs_use_absolute_paths = True
    supports_pending_changesets = True
    field_help_text = {b'path': _(b'The Plastic repository spec in the form of [repo]@[hostname]:[port].')}
    dependencies = {b'executables': [
                      b'cm']}
    REP_RE = re.compile(b'^(?P<reponame>.*)@(?P<hostname>.*):(?P<port>\\d+)$')
    CS_RE = re.compile(b'^(?P<csid>\\d+) (?P<user>[^\\s]+) (?P<revid>\\d+) (?P<file>.*)$')
    REPOLIST_RE = re.compile(b'^\\s*\\d+\\s*(?P<reponame>[^\\s]+)\\s*.*:.*$')
    UNKNOWN_REV = b'rev:revid:-1'

    def __init__(self, repository):
        super(PlasticTool, self).__init__(repository)
        self.reponame, self.hostname, self.port = self.parse_repository(repository.path)
        self.client = PlasticClient(repository.path, self.reponame, self.hostname, self.port)

    def get_changeset(self, changesetid, allow_empty=False):
        logging.debug(b'Plastic: get_changeset %s' % changesetid)
        changesetdata = self.client.get_changeset(changesetid)
        logging.debug(b'Plastic: changesetdata %s' % changesetdata)
        changeset = ChangeSet()
        changeset.changenum = changesetid
        split = changesetdata.split(b'\n')
        m = self.CS_RE.match(split[0])
        revid = m.group(b'revid')
        changeset.username = m.group(b'user')
        changeset.summary = self.client.get_changeset_comment(changesetid, revid)
        logging.debug(b'Plastic: changeset user %s summary %s' % (
         changeset.username, changeset.summary))
        for line in split:
            if line:
                m = self.CS_RE.match(line)
                if not m:
                    logging.debug(b'Plastic: bad re %s failed to match %s' % (
                     self.CS_RE, line))
                    raise SCMError(b'Error looking up changeset')
                if m.group(b'csid') != six.text_type(changesetid):
                    logging.debug(b'Plastic: csid %s != %s' % (m.group(b'csid'),
                     changesetid))
                    raise SCMError(b'The server returned a changeset ID that was not requested')
                logging.debug(b'Plastic: adding file %s' % m.group(b'file'))
                changeset.files += m.group(b'file')

        return changeset

    def get_file(self, path, revision=HEAD, **kwargs):
        logging.debug(b'Plastic: get_file %s revision %s' % (path, revision))
        if revision == PRE_CREATION:
            return b''
        if revision == self.UNKNOWN_REV:
            return b''
        return self.client.get_file(path, revision)

    def file_exists(self, path, revision=HEAD, **kwargs):
        logging.debug(b'Plastic: file_exists %s revision %s' % (path, revision))
        if revision == PRE_CREATION:
            return True
        if revision == self.UNKNOWN_REV:
            return True
        try:
            return self.client.get_file(path, revision)
        except FileNotFoundError:
            return False

    def parse_diff_revision(self, file_str, revision_str, *args, **kwargs):
        logging.debug(b'Plastic: parse_diff_revision file %s revision %s' % (
         file_str, revision_str))
        if revision_str == b'PRE-CREATION':
            return (file_str, PRE_CREATION)
        return (file_str, revision_str)

    def get_parser(self, data):
        return PlasticDiffParser(data)

    @classmethod
    def parse_repository(cls, path):
        m = cls.REP_RE.match(path)
        if m:
            repopath = m.group(b'reponame')
            hostname = m.group(b'hostname')
            port = m.group(b'port')
            return (
             repopath, hostname, port)
        raise RepositoryNotFoundError()

    @classmethod
    def check_repository(cls, path, username=None, password=None, local_site_name=None):
        m = cls.REP_RE.match(path)
        if not m:
            raise RepositoryNotFoundError()
        server = b'%s:%s' % (m.group(b'hostname'), m.group(b'port'))
        reponame = m.group(b'reponame')
        logging.debug(b'Plastic: Checking repository %s@%s' % (
         reponame, server))
        repositories = PlasticClient.get_repositories(server)
        split = repositories.splitlines()
        for rep in split:
            m = cls.REPOLIST_RE.match(rep)
            if m and m.group(b'reponame') == reponame:
                break
        else:
            raise RepositoryNotFoundError()


class PlasticDiffParser(DiffParser):
    """
    This class is able to parse diffs created with the plastic client
    support in post-review.
    """
    BINARY_RE = re.compile(b'^==== ([^\\s]+) \\(([^\\)]+)\\) ==([ACIMR])==$')

    def __init__(self, data):
        super(PlasticDiffParser, self).__init__(data)

    def parse_diff_header(self, linenum, info):
        m = self.BINARY_RE.match(self.lines[linenum])
        if m:
            info[b'origFile'] = m.group(1)
            info[b'origInfo'] = m.group(2)
            info[b'newFile'] = m.group(1)
            info[b'newInfo'] = b''
            linenum += 1
            if linenum < len(self.lines) and (self.lines[linenum].startswith(b'Binary files ') or self.lines[linenum].startswith(b'Files ')):
                info[b'binary'] = True
                linenum += 1
            return linenum
        return super(PlasticDiffParser, self).parse_diff_header(linenum, info)


class PlasticClient(object):

    def __init__(self, repository, reponame, hostname, port):
        if not is_exe_in_path(b'cm'):
            raise ImportError
        self.reponame = reponame
        self.hostname = hostname
        self.port = port

    def get_file(self, path, revision):
        logging.debug(b'Plastic: get_file %s rev %s' % (path, revision))
        repo = b'rep:%s@repserver:%s:%s' % (self.reponame, self.hostname,
         self.port)
        fd, tmpfile = mkstemp()
        os.close(fd)
        p = subprocess.Popen([
         b'cm', b'cat', revision + b'@' + repo, b'--file=' + tmpfile], stderr=subprocess.PIPE, stdout=subprocess.PIPE, close_fds=os.name != b'nt')
        errmsg = six.text_type(p.stderr.read())
        failure = p.wait()
        if failure:
            if not errmsg:
                errmsg = p.stdout.read()
            raise SCMError(errmsg)
        with open(tmpfile, b'rb') as (readtmp):
            contents = readtmp.read()
        os.unlink(tmpfile)
        return contents

    def get_changeset(self, changesetid):
        logging.debug(b'Plastic: get_changeset %s' % changesetid)
        repo = b'rep:%s@repserver:%s:%s' % (self.reponame, self.hostname,
         self.port)
        p = subprocess.Popen([b'cm', b'find', b'revs', b'where',
         b'changeset=' + six.text_type(changesetid), b'on',
         b'repository', b"'" + repo + b"'",
         b'--format={changeset} {owner} {id} {item}',
         b'--nototal'], stderr=subprocess.PIPE, stdout=subprocess.PIPE, close_fds=os.name != b'nt')
        contents = p.stdout.read()
        errmsg = p.stderr.read()
        failure = p.wait()
        if failure:
            raise SCMError(errmsg)
        return contents

    def get_changeset_comment(self, changesetid, revid):
        logging.debug(b'Plastic: get_changeset_comment %s' % changesetid)
        repo = b'rep:%s@repserver:%s:%s' % (self.reponame, self.hostname,
         self.port)
        p = subprocess.Popen([b'cm', b'find', b'changesets', b'where',
         b'changesetid=' + six.text_type(changesetid),
         b'on', b'repository', b"'" + repo + b"'",
         b'--format={comment}', b'--nototal'], stderr=subprocess.PIPE, stdout=subprocess.PIPE, close_fds=os.name != b'nt')
        contents = p.stdout.read()
        errmsg = p.stderr.read()
        failure = p.wait()
        if failure:
            raise SCMError(errmsg)
        return contents

    @classmethod
    def get_repositories(cls, server):
        logging.debug(b'Plastic: get_repositories %s' % server)
        p = subprocess.Popen([b'cm', b'listrepositories', server], stderr=subprocess.PIPE, stdout=subprocess.PIPE, close_fds=os.name != b'nt')
        repositories = p.stdout.read()
        errmsg = p.stderr.read()
        failure = p.wait()
        if failure:
            if not errmsg and repositories.startswith(b'Error:'):
                error = repositories
            else:
                error = errmsg
            raise SCMError(error)
        return repositories