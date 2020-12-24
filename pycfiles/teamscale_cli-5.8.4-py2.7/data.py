# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/teamscale_precommit_client/data.py
# Compiled at: 2020-04-21 02:31:18
from __future__ import absolute_import
from __future__ import unicode_literals
from teamscale_client.utils import auto_str

@auto_str
class PreCommitUploadData(object):
    """Represents precommit upload data for Teamscale."""

    def __init__(self, uniformPathToContentMap, deletedUniformPaths):
        """
        Constructor.
        Args:
            uniformPathToContentMap (dict[unicode, unicode]): A map from uniform paths to the content of changed files
            deletedUniformPaths (List[str]): List of names of deleted files
        """
        self.uniformPathToContentMap = uniformPathToContentMap
        self.deletedUniformPaths = deletedUniformPaths