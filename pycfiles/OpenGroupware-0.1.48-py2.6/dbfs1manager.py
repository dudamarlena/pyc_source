# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/coils/foundation/dbfs1/dbfs1manager.py
# Compiled at: 2012-10-12 07:02:39


class DBFS1Manager(object):
    """ The DBFS1Manager supports versions documents and document editing; this is compatible
        with the DB Project in Legacy OpenGroupware"""

    def __init__(self, project_id):
        self._project_id = project_id

    def get_path(self, document, version=None):
        path = None
        if version is not None:
            for revision in document.versions:
                if revision.version == version:
                    path = ('documents/{0}/{1}/{2}.{3}').format(self._project_id, revision.object_id / 1000 * 1000, revision.object_id, revision.extension)

        else:
            path = ('documents/{0}/{1}/{2}.{3}').format(self._project_id, document.object_id / 1000 * 1000, document.object_id, document.extension)
        return path

    def create_path(self, document, version):
        folder_path = ('documents/{0}/{1}').format(self._project_id, version.object_id / 1000 * 1000)
        file_name = ('{1}.{2}').format(folder_path, version.object_id, document.extension)
        return (folder_path, file_name)