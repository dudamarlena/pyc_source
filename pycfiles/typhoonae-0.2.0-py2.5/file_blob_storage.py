# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-i386/egg/typhoonae/blobstore/file_blob_storage.py
# Compiled at: 2010-12-12 04:36:57
"""TyphoonAE's implementation of Blobstore stub storage."""
import errno, google.appengine.api.blobstore, google.appengine.api.blobstore.blobstore_stub, google.appengine.api.datastore, google.appengine.api.datastore_types, os, typhoonae.blobstore.handlers
__all__ = [
 'FileBlobStorage']

class FileBlobStorage(google.appengine.api.blobstore.blobstore_stub.BlobStorage):
    """Handles blob files stored on disk."""

    def __init__(self, storage_directory, app_id):
        """Constructor.

        Args:
            storage_directory: Directory within which to store blobs.
            app_id: App id to store blobs on behalf of.
        """
        self._storage_directory = storage_directory
        self._app_id = app_id

    def _FileForBlob(self, blob_key):
        """Calculate full filename to store blob contents in.

        This method does not check to see if the file actually exists.

        Args:
            blob_key: Blob key of blob to calculate file for.

        Returns:
            Complete path for file used for storing blob.
        """
        try:
            blob_info = google.appengine.api.datastore.Get(blob_key)
        except google.appengine.api.datastore_errors.EntityNotFoundError:
            return ''

        blob_path = typhoonae.blobstore.handlers.DecodeBlobKey(blob_key)
        f = os.path.join(self._storage_directory, self._app_id, blob_path[(-1)], blob_path)
        return f

    def OpenBlob(self, blob_key):
        """Open blob file for streaming.

        Args:
            blob_key: Blob-key of existing blob to open for reading.

        Returns:
            Open file stream for reading blob from disk.
        """
        if isinstance(blob_key, basestring):
            blob_key = google.appengine.api.datastore_types.Key.from_path('__BlobInfo__', blob_key)
        return open(self._FileForBlob(blob_key), 'rb')

    def DeleteBlob(self, blob_key):
        """Delete blob data from disk.

        Deleting an unknown blob will not raise an error.

        Args:
            blob_key: Blob-key of existing blob to delete.
        """
        try:
            os.remove(self._FileForBlob(blob_key))
        except OSError, e:
            if e.errno != errno.ENOENT:
                raise e