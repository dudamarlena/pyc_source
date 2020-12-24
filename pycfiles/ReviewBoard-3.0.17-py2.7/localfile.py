# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/reviewboard/scmtools/localfile.py
# Compiled at: 2020-02-11 04:03:56
from __future__ import unicode_literals
from django.utils import six
from reviewboard.scmtools.core import FileNotFoundError, SCMTool, HEAD

class LocalFileTool(SCMTool):
    scmtool_id = b'local-file'
    name = b'Local File'

    def __init__(self, repository):
        self.repopath = repository.path
        if self.repopath[(-1)] == b'/':
            self.repopath = self.repopath[:-1]
        SCMTool.__init__(self, repository)

    def get_file(self, path, revision=HEAD, **kwargs):
        if not path or revision != HEAD:
            raise FileNotFoundError(path, revision)
        try:
            with open(self.repopath + b'/' + path, b'rb') as (f):
                return f.read()
        except IOError as e:
            raise FileNotFoundError(path, revision, detail=six.text_type(e))

    def parse_diff_revision(self, file_str, revision_str, *args, **kwargs):
        return (file_str, HEAD)