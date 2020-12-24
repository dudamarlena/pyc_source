# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.10-x86_64/egg/boto/glacier/writer.py
# Compiled at: 2015-11-24 05:02:18
# Size of source mod 2**32: 9668 bytes
import hashlib
from boto.glacier.utils import chunk_hashes, tree_hash, bytes_to_hex
from boto.glacier.utils import compute_hashes_from_fileobj
_ONE_MEGABYTE = 1048576

class _Partitioner(object):
    __doc__ = 'Convert variable-size writes into part-sized writes\n\n    Call write(data) with variable sized data as needed to write all data. Call\n    flush() after all data is written.\n\n    This instance will call send_fn(part_data) as needed in part_size pieces,\n    except for the final part which may be shorter than part_size. Make sure to\n    call flush() to ensure that a short final part results in a final send_fn\n    call.\n\n    '

    def __init__(self, part_size, send_fn):
        self.part_size = part_size
        self.send_fn = send_fn
        self._buffer = []
        self._buffer_size = 0

    def write(self, data):
        if data == b'':
            return
        self._buffer.append(data)
        self._buffer_size += len(data)
        while self._buffer_size > self.part_size:
            self._send_part()

    def _send_part(self):
        data = (b'').join(self._buffer)
        if len(data) > self.part_size:
            self._buffer = [
             data[self.part_size:]]
            self._buffer_size = len(self._buffer[0])
        else:
            self._buffer = []
            self._buffer_size = 0
        part = data[:self.part_size]
        self.send_fn(part)

    def flush(self):
        if self._buffer_size > 0:
            self._send_part()


class _Uploader(object):
    __doc__ = 'Upload to a Glacier upload_id.\n\n    Call upload_part for each part (in any order) and then close to complete\n    the upload.\n\n    '

    def __init__(self, vault, upload_id, part_size, chunk_size=_ONE_MEGABYTE):
        self.vault = vault
        self.upload_id = upload_id
        self.part_size = part_size
        self.chunk_size = chunk_size
        self.archive_id = None
        self._uploaded_size = 0
        self._tree_hashes = []
        self.closed = False

    def _insert_tree_hash(self, index, raw_tree_hash):
        list_length = len(self._tree_hashes)
        if index >= list_length:
            self._tree_hashes.extend([None] * (list_length - index + 1))
        self._tree_hashes[index] = raw_tree_hash

    def upload_part(self, part_index, part_data):
        """Upload a part to Glacier.

        :param part_index: part number where 0 is the first part
        :param part_data: data to upload corresponding to this part

        """
        if self.closed:
            raise ValueError('I/O operation on closed file')
        part_tree_hash = tree_hash(chunk_hashes(part_data, self.chunk_size))
        self._insert_tree_hash(part_index, part_tree_hash)
        hex_tree_hash = bytes_to_hex(part_tree_hash)
        linear_hash = hashlib.sha256(part_data).hexdigest()
        start = self.part_size * part_index
        content_range = (start,
         start + len(part_data) - 1)
        response = self.vault.layer1.upload_part(self.vault.name, self.upload_id, linear_hash, hex_tree_hash, content_range, part_data)
        response.read()
        self._uploaded_size += len(part_data)

    def skip_part(self, part_index, part_tree_hash, part_length):
        """Skip uploading of a part.

        The final close call needs to calculate the tree hash and total size
        of all uploaded data, so this is the mechanism for resume
        functionality to provide it without actually uploading the data again.

        :param part_index: part number where 0 is the first part
        :param part_tree_hash: binary tree_hash of part being skipped
        :param part_length: length of part being skipped

        """
        if self.closed:
            raise ValueError('I/O operation on closed file')
        self._insert_tree_hash(part_index, part_tree_hash)
        self._uploaded_size += part_length

    def close(self):
        if self.closed:
            return
        if None in self._tree_hashes:
            raise RuntimeError('Some parts were not uploaded.')
        hex_tree_hash = bytes_to_hex(tree_hash(self._tree_hashes))
        response = self.vault.layer1.complete_multipart_upload(self.vault.name, self.upload_id, hex_tree_hash, self._uploaded_size)
        self.archive_id = response['ArchiveId']
        self.closed = True


def generate_parts_from_fobj(fobj, part_size):
    data = fobj.read(part_size)
    while data:
        yield data.encode('utf-8')
        data = fobj.read(part_size)


def resume_file_upload(vault, upload_id, part_size, fobj, part_hash_map, chunk_size=_ONE_MEGABYTE):
    """Resume upload of a file already part-uploaded to Glacier.

    The resumption of an upload where the part-uploaded section is empty is a
    valid degenerate case that this function can handle. In this case,
    part_hash_map should be an empty dict.

    :param vault: boto.glacier.vault.Vault object.
    :param upload_id: existing Glacier upload id of upload being resumed.
    :param part_size: part size of existing upload.
    :param fobj: file object containing local data to resume. This must read
        from the start of the entire upload, not just from the point being
        resumed. Use fobj.seek(0) to achieve this if necessary.
    :param part_hash_map: {part_index: part_tree_hash, ...} of data already
        uploaded. Each supplied part_tree_hash will be verified and the part
        re-uploaded if there is a mismatch.
    :param chunk_size: chunk size of tree hash calculation. This must be
        1 MiB for Amazon.

    """
    uploader = _Uploader(vault, upload_id, part_size, chunk_size)
    for part_index, part_data in enumerate(generate_parts_from_fobj(fobj, part_size)):
        part_tree_hash = tree_hash(chunk_hashes(part_data, chunk_size))
        if part_index not in part_hash_map or part_hash_map[part_index] != part_tree_hash:
            uploader.upload_part(part_index, part_data)
        else:
            uploader.skip_part(part_index, part_tree_hash, len(part_data))

    uploader.close()
    return uploader.archive_id


class Writer(object):
    __doc__ = '\n    Presents a file-like object for writing to a Amazon Glacier\n    Archive. The data is written using the multi-part upload API.\n    '

    def __init__(self, vault, upload_id, part_size, chunk_size=_ONE_MEGABYTE):
        self.uploader = _Uploader(vault, upload_id, part_size, chunk_size)
        self.partitioner = _Partitioner(part_size, self._upload_part)
        self.closed = False
        self.next_part_index = 0

    def write(self, data):
        if self.closed:
            raise ValueError('I/O operation on closed file')
        self.partitioner.write(data)

    def _upload_part(self, part_data):
        self.uploader.upload_part(self.next_part_index, part_data)
        self.next_part_index += 1

    def close(self):
        if self.closed:
            return
        self.partitioner.flush()
        self.uploader.close()
        self.closed = True

    def get_archive_id(self):
        self.close()
        return self.uploader.archive_id

    @property
    def current_tree_hash(self):
        """
        Returns the current tree hash for the data that's been written
        **so far**.

        Only once the writing is complete is the final tree hash returned.
        """
        return tree_hash(self.uploader._tree_hashes)

    @property
    def current_uploaded_size(self):
        """
        Returns the current uploaded size for the data that's been written
        **so far**.

        Only once the writing is complete is the final uploaded size returned.
        """
        return self.uploader._uploaded_size

    @property
    def upload_id(self):
        return self.uploader.upload_id

    @property
    def vault(self):
        return self.uploader.vault