# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/egnyte/client.py
# Compiled at: 2016-12-07 06:45:59
from __future__ import print_function
import collections, os, os.path, shutil
from egnyte import exc, base, resources, audits, events

class EgnyteClient(base.Session):
    """Main client objects. This should be the only object you have to manually create in standard API use."""

    @property
    def links(self):
        """API for Links management"""
        return resources.Links(self)

    @property
    def user_info(self):
        """
        Information about user associated with this API access token.
        """
        return exc.default.check_json_response(self.GET(self.get_url('pubapi/v1/userinfo')))

    @property
    def users(self):
        """API for User management"""
        return resources.Users(self)

    @property
    def audits(self):
        """API for Audit Reports"""
        return audits.Audits(self)

    @property
    def notes(self):
        """API for Notes management"""
        return resources.Notes(self)

    @property
    def groups(self):
        """API for Group Management"""
        return resources.Groups(self)

    @property
    def search(self):
        """API for Search"""
        return resources.Search(self)

    @property
    def events(self):
        """API for events"""
        return events.Events(self)

    @property
    def settings(self):
        """Domain settings."""
        if not hasattr(self, '_cached_settings'):
            result = {}
            urls = (('users', 'pubapi/v2/users/settings'),
             ('links', 'pubapi/v1/links/settings'),
             ('file_system', 'pubapi/v1/fs/settings'),
             ('audit', 'pubapi/v1/audit/settings'))
            for name, url in urls:
                try:
                    result[name] = exc.default.check_json_response(self.GET(self.get_url(url)))
                except Exception:
                    pass

            self._cached_settings = result
        return self._cached_settings

    def folder(self, path='/Shared', **kwargs):
        """Get a Folder object for the specified path"""
        return resources.Folder(self, path=path.rstrip('/'), **kwargs)

    def file(self, path, **kwargs):
        """Get a File object for the specified path"""
        return resources.File(self, path=path, **kwargs)

    def get(self, path):
        """Check whether a path is a file or a folder and return the right object."""
        return self.folder(path)._get()

    def impersonate(self, username):
        """
        Start impersonating another user.

        * username: either username or full email address of user to impersonate.
        """
        self._session.headers['X-Egnyte-Act-As-Email' if '@' in username else 'X-Egnyte-Act-As'] = username

    def stop_impersonating(self):
        """
        Stop impersonating another user.
        """
        self._session.headers.pop('X-Egnyte-Act-As', None)
        self._session.headers.pop('X-Egnyte-Act-As-Email', None)
        return

    def bulk_upload(self, paths, target, exclude=None, progress_callbacks=None):
        """
        Transfer many files or directories to Cloud File System.

        * paths - list of local file paths
        * target - Path in CFS to upload to
        * progress_callbacks - Callback object (see ProgressCallbacks)
        """
        if not paths:
            return
        else:
            if progress_callbacks is None:
                progress_callbacks = ProgressCallbacks()
            target_folder = self.folder(target)
            progress_callbacks.creating_directory(target_folder)
            target_folder.create(True)
            for is_dir, local_path, cloud_path in base.generate_paths(paths, exclude):
                if is_dir:
                    cloud_dir = target_folder.folder(cloud_path)
                    progress_callbacks.creating_directory(cloud_dir)
                    cloud_dir.create(True)
                else:
                    size = os.path.getsize(local_path)
                    if size:
                        cloud_file = target_folder.file(cloud_path, size=size)
                        with open(local_path, 'rb') as (fp):
                            progress_callbacks.upload_start(local_path, cloud_file, size)
                            cloud_file.upload(fp, size, progress_callbacks.upload_progress)
                        progress_callbacks.upload_finish(cloud_file)

            progress_callbacks.finished()
            return

    def _bulk_download(self, items, root_path, local_dir, overwrite, progress_callbacks):
        root_len = len(root_path.rstrip('/')) + 1
        queue = collections.deque(items)
        while True:
            try:
                obj = queue.popleft()
            except IndexError:
                break

            relpath = obj.path[root_len:].strip('/')
            local_path = os.path.join(local_dir, relpath.replace('/', os.sep))
            dir_path = os.path.dirname(local_path)
            if not os.path.isdir(dir_path):
                if os.path.exists(dir_path):
                    if overwrite:
                        os.unlink(local_path)
                    else:
                        progress_callbacks.skipped(obj, 'Existing file conflicts with cloud folder')
                        continue
                os.makedirs(dir_path)
            if obj.is_folder:
                if obj.files is None:
                    progress_callbacks.getting_info(obj.path)
                    obj.list()
                    progress_callbacks.got_info(obj)
                queue.extend(obj.files)
                queue.extend(obj.folders)
            else:
                if os.path.exists(local_path):
                    if overwrite:
                        if os.path.isdir(local_path) and not os.path.islink(local_path):
                            shutil.rmtree(local_path)
                        else:
                            os.unlink(local_path)
                    else:
                        progress_callbacks.skipped(obj, 'Existing file conflicts with cloud file')
                        continue
                progress_callbacks.download_start(local_path, obj, obj.size)
                obj.download().save_to(local_path, progress_callbacks.download_progress)
                progress_callbacks.download_finish(obj)

        return

    def bulk_download(self, paths, local_dir, overwrite=False, progress_callbacks=None):
        """
        Transfer many files or directories to Cloud File System.

        * paths - list of local file paths
        * target - Path in CFS to upload to
        * progress_callbacks - Callback object (see ProgressCallbacks)
        """
        if progress_callbacks is None:
            progress_callbacks = ProgressCallbacks()
        for path in paths:
            progress_callbacks.getting_info(path)
            obj = self.get(path)
            progress_callbacks.got_info(obj)
            root_path = path[:path.rstrip('/').rfind('/')]
            if obj.is_folder:
                items = obj.files + obj.folders
            else:
                items = (
                 obj,)
            self._bulk_download(items, root_path, local_dir, overwrite, progress_callbacks)

        progress_callbacks.finished()
        return


class ProgressCallbacks(object):
    """
    This object is used for bulk transfers (uploads and downloads)
    Inherit this and add override any of the callabcks you'd like to handle.
    """

    def getting_info(self, cloud_path):
        """Getting information about an object. Called for directories and unknown paths."""
        pass

    def got_info(self, cloud_obj):
        """Got information about an object."""
        pass

    def creating_directory(self, cloud_folder):
        """Creating a directory."""
        pass

    def download_start(self, local_path, cloud_file, size):
        """Starting to download a file."""
        pass

    def download_progress(self, cloud_file, size, downloaded):
        """Some progress in file download."""
        pass

    def download_finish(self, cloud_file):
        """Finished downloading a file."""
        pass

    def upload_start(self, local_path, cloud_file, size):
        """Starting to upload a file."""
        pass

    def upload_progress(self, cloud_file, size, uploaded):
        """Some progress in file upload."""
        pass

    def upload_finish(self, cloud_file):
        """Finished uploading a file."""
        pass

    def finished(self):
        """Called after all operations."""
        pass

    def skipped(self, cloud_obj, reason):
        """Object has been skipped because of 'reason'"""
        pass