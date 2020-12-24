# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/reviewboard/scmtools/mtn.py
# Compiled at: 2020-02-11 04:03:56
from __future__ import unicode_literals
import os, subprocess
from django.utils import six
from djblets.util.filesystem import is_exe_in_path
from reviewboard.diffviewer.parser import DiffParser
from reviewboard.scmtools.core import SCMTool
from reviewboard.scmtools.errors import FileNotFoundError, SCMError

class MonotoneTool(SCMTool):
    scmtool_id = b'monotone'
    name = b'Monotone'
    diffs_use_absolute_paths = True
    dependencies = {b'executables': [
                      b'mtn']}

    def __init__(self, repository):
        SCMTool.__init__(self, repository)
        self.client = MonotoneClient(repository.path)

    def get_file(self, path, revision=None, **kwargs):
        if not revision:
            return b''
        return self.client.get_file(revision)

    def file_exists(self, path, revision=None, **kwargs):
        if not revision:
            return False
        try:
            self.client.get_file(revision)
        except FileNotFoundError:
            return False

        return True

    def parse_diff_revision(self, file_str, revision_str, *args, **kwargs):
        return (
         file_str, revision_str)

    def get_parser(self, data):
        return MonotoneDiffParser(data)


class MonotoneDiffParser(DiffParser):
    INDEX_SEP = b'=' * 60

    def parse_special_header(self, linenum, info):
        if self.lines[linenum].startswith(b'#'):
            if b'is binary' in self.lines[linenum]:
                info[b'binary'] = True
                linenum += 1
            elif self.lines[(linenum + 1)] == self.INDEX_SEP:
                linenum += 1
        return linenum


class MonotoneClient:

    def __init__(self, path):
        if not is_exe_in_path(b'mtn'):
            raise ImportError
        self.path = path
        if not os.path.isfile(self.path):
            raise SCMError(b'Repository %s does not exist' % path)

    def get_file(self, fileid):
        args = [b'mtn', b'-d', self.path, b'automate', b'get_file', fileid]
        p = subprocess.Popen(args, stderr=subprocess.PIPE, stdout=subprocess.PIPE, close_fds=os.name != b'nt')
        out = p.stdout.read()
        err = six.text_type(p.stderr.read())
        failure = p.wait()
        if not failure:
            return out
        if b'mtn: misuse: no file' in err:
            raise FileNotFoundError(fileid)
        else:
            raise SCMError(err)