# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.14-x86_64/egg/libreary/adapters/BaseAdapter.py
# Compiled at: 2020-03-19 14:48:15
# Size of source mod 2**32: 3031 bytes


class BaseAdapter:
    __doc__ = '\n    Class definition for the base adapter for libre-ary resource adapters.\n\n    Use this mostly as a reference for what other adapters need to implement.\n\n    An adapter allows LIBREary to save copies of digital objects\n        to different places across cyberspace. Working with many\n        adapters in concert, one should be able do save sufficient\n        copies to places they want them.\n    '

    def __init__(config: dict):
        """
        This should handle configuration (auth, etc.) and set up the
        metadata db connection
        """
        pass

    def store(resource_id: str) -> str:
        """
        Store a copy of a resource in this adapter.

        Store assumes that the file is in the `dropbox_dir`.
        AdapterManager will always verify that this is the case.

        :param r_id - the resource to store's UUID
        """
        pass

    def _store_canonical(current_path: str, r_id: str) -> str:
        """
            Store a canonical copy of a resource in this adapter.

            If we're using an adapter as a canonical adapter, we need
            to be able to store from a current path, taking in a generated UUID,
            rather than looking info up from the database.

            :param current_path - current path to object
            :param r_id - UUID of resource you're storing
            :param checksum - checksum of resource
            :param filename - filename of resource you're storing

        """
        pass

    def _delete_canonical(self, r_id: str) -> None:
        """
        Delete a canonical copy of a resource from this adapter.
        Delete the corresponding entry in the `copies` table.

        :param r_id - the resource to retrieve's UUID
        """
        pass

    def retrieve(resource_id: str) -> str:
        """
        Retrieve a copy of a resource from this adapter.

        Retrieve assumes that the file can be stored to the `output_dir`.
        AdapterManager will always verify that this is the case.

        Returns the path to the resource.

        May overwrite files in the `output_dir`

        :param r_id - the resource to retrieve's UUID
        """
        pass

    def update(resource_id: str, updated: str) -> None:
        """
        Update a resource with a new object. Preserves UUID and all other metadata (levels, etc.)

        :param r_id - the UUID of the object you'd like to update
        :param updated_path - path to the contents of the updated object.

        """
        pass

    def delete(resource_id: str) -> None:
        """
        Delete a copy of a resource from this adapter.
        Delete the corresponding entry in the `copies` table.

        :param r_id - the resource to retrieve's UUID
        """
        pass

    def get_actual_checksum(self, r_id: str) -> str:
        """
        Return an exact checksum of a resource, not relying on the metadata db

        If possible, this should be done with no file I/O
        """
        pass