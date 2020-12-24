# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: sync/version_manager.py
# Compiled at: 2018-04-27 05:54:44
import os, json, rest, re, datetime, hashlib
from helper.exception import print_stack
import wx, wx.lib.newevent
from conans.util.files import md5sum

class VersionManagerException(Exception):

    def __init__(self, error):
        super(VersionManagerException, self).__init__(error)


class VersionManagerEnabler(object):

    def __init__(self, manager):
        self.manager = manager
        self.manager_stack = {}
        if self.manager_stack.has_key(self.manager) == False:
            self.manager_stack[self.manager] = []

    def __enter__(self):
        self.manager_stack[self.manager].append(False)
        self.manager.file_manager.Enabled(False)

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.manager_stack[self.manager].pop()
        if len(self.manager_stack[self.manager]) == 0:
            self.manager.file_manager.Enabled(True)


class VersionManager(object):

    def __init__(self, file_manager):
        super(VersionManager, self).__init__()
        self.on_change_hook = None
        self.root_path = file_manager.root_path()
        self.file_manager = file_manager
        self.config = os.path.join(self.root_path, file_manager.version_file())
        file_manager.on_change_hook = self.on_file_changed
        self.local_files = {}
        self.LoadState()
        return

    def deserialize_file(self, json):
        file = rest.model.VersionedFile()
        if json.has_key('id'):
            file.id = int(json['id'])
        if json.has_key('source_path'):
            file.source_path = json['source_path']
        if json.has_key('storage_path'):
            file.storage_path = json['storage_path']
        if json.has_key('md5'):
            file.md5 = json['md5']
        if json.has_key('metadata'):
            file.metadata = unicode(json['metadata'])
        if json.has_key('version'):
            file.version = int(json['version'])
        if json.has_key('category'):
            file.category = unicode(json['category'])
        if json.has_key('updated'):
            updated = re.sub(' ', 'T', json['updated'])
            file.updated = updated
        file.state = ''
        if json.has_key('state'):
            file.state = json['state']
        return file

    def serialize_file(self, file):
        res = {}
        if file.id:
            res['id'] = unicode(file.id)
        if file.source_path:
            res['source_path'] = unicode(file.source_path)
        if file.storage_path:
            res['storage_path'] = unicode(file.storage_path)
        if file.metadata:
            res['metadata'] = unicode(file.metadata)
        if file.md5:
            res['md5'] = unicode(file.md5)
        if file.version:
            res['version'] = unicode(file.version)
        if file.updated:
            res['updated'] = unicode(file.updated)
        if file.category:
            res['category'] = unicode(file.category)
        if file.state:
            res['state'] = file.state
        return res

    def SaveState(self):
        with VersionManagerEnabler(self) as (f):
            print '===> SaveState----'
            content = []
            for file in self.local_files:
                print '+', file, self.local_files[file]
                content.append(self.serialize_file(self.local_files[file]))

            with open(self.config, 'wb') as (outfile):
                json.dump(content, outfile, sort_keys=True, indent=2, separators=(',',
                                                                                  ': '))
                outfile.close()
            print '------------------'

    def on_file_changed(self, path):
        self.file_manager.Load()
        for filepath in self.file_manager.files:
            file = self.file_manager.files[filepath]
            if filepath.startswith(filepath) and self.local_files.has_key(filepath):
                localfile = self.local_files[filepath]
                if file.md5 != localfile.md5 or file.metadata != localfile.metadata:
                    localfile.state = 'outgo_change'
                    localfile.updated = rest.api.get_date()
                    localfile.md5 = file.md5
                    localfile.content = file.content
                    localfile.metadata = file.metadata

        if self.on_change_hook:
            self.on_change_hook(path)

    def GetFile(self, path):
        with VersionManagerEnabler(self) as (f):
            if os.path.exists(self.config) == False:
                return
            else:
                return self.local_files[path]

        return

    def LoadState(self):
        """
        Synchronize local files with state
        """
        with VersionManagerEnabler(self) as (f):
            state_files = {}
            if os.path.exists(self.config) == False:
                self.SaveState()
            content = json.load(open(self.config))
            for data in content:
                file = self.deserialize_file(data)
                state_files[file.source_path] = file

            self.file_manager.Load()
            for filepath in self.file_manager.files:
                file_disk = self.file_manager.files[filepath]
                if self.local_files.has_key(filepath) == False:
                    file_disk.state = ''
                    self.local_files[filepath] = file_disk

            for filepath in state_files:
                state_file = state_files[filepath]
                if self.local_files.has_key(filepath):
                    file_disk = self.local_files[filepath]
                    file_disk.id = state_file.id
                    file_disk.version = state_file.version
                    metadata_changed = False
                    if file_disk.metadata:
                        if not state_file.metadata:
                            state_file.metadata = '{}'
                        src_metadata = json.loads(file_disk.metadata)
                        dst_metadata = json.loads(state_file.metadata)
                        for meta in src_metadata:
                            dst_metadata[meta] = src_metadata[meta]

                        new_metadata = json.dumps(dst_metadata)
                        if new_metadata != state_file.metadata:
                            state_file.metadata = new_metadata
                            metadata_changed = True
                    if (file_disk.md5 != state_file.md5 or metadata_changed) and (state_file.state == '' or state_file.state is None):
                        file_disk.state = 'outgo_change'
                        file_disk.updated = rest.api.get_date()
                    else:
                        file_disk.state = state_file.state
                        file_disk.updated = state_file.updated
                    file_disk.category = self.file_manager.category()
                    print '$$$$', filepath, state_file.metadata
                    file_disk.metadata = state_file.metadata

            pop_list = []
            for filepath in self.local_files:
                file_disk = self.local_files[filepath]
                if self.file_manager.Exists(filepath) == False and file_disk.state != 'outgo_del':
                    pop_list.append(filepath)

            for filepath in pop_list:
                self.local_files.pop(filepath)

            for filepath in state_files:
                file_version = state_files[filepath]
                file_disk = None
                if self.local_files.has_key(filepath) == False and file_version.state == 'outgo_del':
                    self.local_files[filepath] = file_version

        return

    def Synchronize_(self):
        with VersionManagerEnabler(self) as (f):
            self.LoadState()
            return self.local_files

    def Synchronize(self):
        """
        Return synchronization state from server
        """
        with VersionManagerEnabler(self) as (f):
            self.LoadState()
            files = []
            for file in self.local_files:
                files.append(self.local_files[file])

            if len(files) == 0:
                files.append(rest.model.VersionedFile())
            sync_files = {}
            for file in rest.api.synchronize_versioned_files(files, category=self.file_manager.category()):
                sync_files[file.source_path] = file
                if file.state != 'income_add' and file.state != 'income_change' and file.state != 'income_del' and file.state != 'conflict_add' and file.state != 'conflict_change' and file.state != 'conflict_del':
                    self.local_files[file.source_path] = file

            self.SaveState()
            return sync_files

    def EditMetadata(self, path, metadata):
        with VersionManagerEnabler(self) as (f):
            metadata = self.file_manager.EditMetadata(path, metadata)
            if self.local_files.has_key(path):
                self.local_files[path].updated = datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%SZ')
                self.local_files[path].metadata = metadata
                self.local_files[path].status = 'outgo_change'
                self.SaveState()
            else:
                raise VersionManagerException('Updating metadata failed for file %s' % path)

    def CreateFile(self, path, content):
        with VersionManagerEnabler(self) as (f):
            file = self.file_manager.CreateFile(path, content)
            file.state = 'outgo_add'
            self.local_files[path] = file
            self.SaveState()
            return file

    def EditFile(self, path, content, create=False):
        with VersionManagerEnabler(self) as (f):
            if self.local_files.has_key(path) == False and create == False:
                raise VersionManagerException('File %s does not exists' % path)
            file = self.local_files[path]
            file, changed = self.file_manager.EditFile(file, content, create)
            if changed:
                file.status = 'outgo_change'
            self.SaveState()
            return file

    def MoveFile(self, source_path, dest_path):
        with VersionManagerEnabler(self) as (f):
            if self.local_files.has_key(source_path) == False:
                raise VersionManagerException('File %s does not exists' % source_path)
            file = self.local_files[source_path]
            file = self.file_manager.MoveFile(file, dest_path)
            self.local_files.pop(source_path)
            self.local_files[dest_path] = file
            if file.version is None:
                file.state = 'outgo_add'
            else:
                file.state = 'outgo_change'
            self.SaveState()
            return file
        return

    def delete_file(self, file):
        with VersionManagerEnabler(self) as (f):
            if self.local_files.has_key(file.source_path) == False:
                raise VersionManagerException('File %s does not exists' % file.source_path)
            file = self.file_manager.DeleteFile(file)
            if file.id is None:
                self.local_files.pop(file.source_path)
            else:
                file.state = 'outgo_del'
                self.local_files[file.source_path] = file
            return file
        return

    def DeleteFile(self, file):
        with VersionManagerEnabler(self) as (f):
            if file.state == 'outgo_del':
                return
            else:
                file = self.delete_file(file)
                self.SaveState()
                return file

    def CreateFolder(self, path):
        with VersionManagerEnabler(self) as (f):
            self.file_manager.CreateFolder(path)

    def MoveFolder(self, source_path, dest_path):
        with VersionManagerEnabler(self) as (f):
            to_move = []
            for filename in self.local_files:
                file = self.local_files[filename]
                if file.source_path.startswith(source_path):
                    to_move.append(file)

            self.file_manager.MoveFolder(source_path, dest_path)
            for file in to_move:
                self.local_files.pop(file.source_path)
                file.source_path = file.source_path.replace(source_path, dest_path, 1)
                file.updated = rest.api.get_date()
                self.local_files[file.source_path] = file
                if file.version is None:
                    file.state = 'outgo_add'
                else:
                    file.state = 'outgo_change'

            self.SaveState()
        return

    def DeleteFolder(self, path):
        with VersionManagerEnabler(self) as (f):
            to_delete = []
            for filename in self.local_files:
                file = self.local_files[filename]
                if file.source_path.startswith(path):
                    to_delete.append(file)

            for file in to_delete:
                if file.state.endswith('_del') == False:
                    self.delete_file(file)

            self.file_manager.DeleteFolder(path)
            self.SaveState()

    def Commit(self, files, force=False):
        with VersionManagerEnabler(self) as (f):
            for file in files:
                if force or file.state == 'outgo_add' or file.state == 'outgo_change':
                    if self.file_manager.Exists(file.source_path):
                        self.file_manager.LoadContent(file)

            commits = []
            try:
                commits = rest.api.commit_versioned_files(files, force=force)
            except Exception as e:
                for file in json.loads(e.body):
                    if file['state'] == 'conflict_add' or file['state'] == 'conflict_change' or file['state'] == 'conflict_del':
                        raise VersionManagerException('Commit failed due to unresolved conflict')

                raise VersionManagerException('Commit failed: %s' % format(e))

            for file in commits:
                if file.storage_path:
                    self.local_files[file.source_path] = file
                elif self.local_files.has_key(file.source_path):
                    self.local_files.pop(file.source_path)

            self.SaveState()
            return commits

    def Update(self, files, force=False):
        with VersionManagerEnabler(self) as (f):
            updates = []
            try:
                updates = rest.api.update_versioned_files(files, force=force)
            except Exception as e:
                for file in json.loads(e.body):
                    if file['state'] == 'conflict_add' or file['state'] == 'conflict_change' or file['state'] == 'conflict_del':
                        raise VersionManagerException('Update failed due to unresolved conflict')

                raise VersionManagerException('Update failed: %s' % format(e))

            for file in updates:
                if file.state == 'income_add':
                    newfile = self.file_manager.CreateFile(file.source_path, file.content, overwrite=force)
                    newfile.metadata = file.metadata
                    newfile.id = file.id
                    newfile.version = file.version
                    newfile.state = ''
                    self.local_files[file.source_path] = newfile
                    file = newfile
                    self.file_manager.EditMetadata(file.source_path, file.metadata)
                elif file.state == 'income_change':
                    file, changed = self.file_manager.EditFile(file, file.content, create=True)
                    self.file_manager.EditMetadata(file.source_path, file.metadata)
                    local_file = None
                    for local_file_name in self.local_files:
                        print '****', self.local_files[local_file_name], '###', file
                        if self.local_files[local_file_name].id == file.id:
                            local_file = self.local_files[local_file_name]
                            break

                    if local_file and local_file.source_path != file.source_path:
                        self.file_manager.DeleteFile(local_file, True)
                    self.local_files[file.source_path] = file
                elif file.state == 'income_del':
                    self.DeleteFile(file)
                file.state = ''

            self.SaveState()
            return updates
        return

    def _debug(self, files):
        for file_path in files:
            file = files[file_path]
            if file.id:
                print "-- %s: %d '%s'" % (file_path, file.id, file.state)
            else:
                print "-- %s: None '%s'" % (file_path, file.state)