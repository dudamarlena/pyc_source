# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/reviewboard/testing/scmtool.py
# Compiled at: 2020-02-11 04:03:57
from __future__ import unicode_literals
from django.utils import six
from django.utils.six.moves import range
from reviewboard.scmtools.core import Branch, Commit, ChangeSet
from reviewboard.scmtools.git import GitTool

class TestTool(GitTool):
    scmtool_id = b'test'
    name = b'Test'
    diffs_use_absolute_paths = False
    supports_post_commit = True

    def get_repository_info(self):
        return {b'key1': b'value1', 
           b'key2': b'value2'}

    def get_branches(self):
        return [
         Branch(id=b'trunk', commit=b'5', default=True),
         Branch(id=b'branch1', commit=b'7', default=False)]

    def get_commits(self, branch=None, start=None):
        return [ Commit(b'user%d' % i, six.text_type(i), b'2013-01-01T%02d:00:00.0000000' % i, b'Commit %d' % i, six.text_type(i - 1)) for i in range(int(start or 10), 0, -1)
               ]

    def get_change(self, commit_id):
        return Commit(author_name=b'user1', id=commit_id, date=b'2013-01-01T00:00:00.0000000', message=b'Commit summary\n\nCommit description.', diff=(b'\n').join([
         b'diff --git a/FILE_FOUND b/FILE_FOUND',
         b'index 712544e4343bf04967eb5ea80257f6c64d6f42c7..f88b7f15c03d141d0bb38c8e49bb6c411ebfe1f1 100644',
         b'--- a/FILE_FOUND',
         b'+++ b/FILE_FOUND',
         b'@ -1,1 +1,1 @@',
         b'-blah blah',
         b'+blah',
         b'-',
         b'1.7.1']))

    def get_file(self, path, revision, **kwargs):
        if path.startswith(b'/data:'):
            return b'%s\n' % path.split(b':', 1)[1].encode(b'utf-8')
        return b'Hello, world!\n'

    def file_exists(self, path, revision, **kwargs):
        if path == b'/FILE_FOUND' or path.startswith(b'/data:'):
            return True
        return super(TestTool, self).file_exists(path, revision, **kwargs)

    @classmethod
    def check_repository(cls, path, *args, **kwargs):
        pass


class TestToolSupportsPendingChangeSets(TestTool):
    scmtool_id = b'test-supports-pending-changesets'
    supports_pending_changesets = True

    def get_changeset(self, changesetid, allow_empty=False):
        changeset = ChangeSet()
        changeset.changenum = changesetid
        changeset.description = b'Hello world!'
        changeset.pending = True
        if not allow_empty:
            changeset.files = [
             b'README.md']
        changeset.summary = b'Added a README markdown to help explain what the repository is used for. Hopefully, this takes off.'
        changeset.testing_done = b'None was performed'
        return changeset