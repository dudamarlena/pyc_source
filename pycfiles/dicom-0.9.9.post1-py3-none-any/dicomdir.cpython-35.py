# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: c:\git\pydicom-clean\source\build\lib\dicom\dicomdir.py
# Compiled at: 2017-01-26 21:09:37
# Size of source mod 2**32: 4057 bytes
"""Module for DicomDir class"""
from dicom.errors import InvalidDicomError
from dicom.dataset import FileDataset

class DicomDir(FileDataset):
    __doc__ = 'Hold a DICOMDIR dataset read from file.\n\n    Derived from FileDataset, but additional methods are available,\n    specific to the Directory structure\n    '

    def __init__(self, filename_or_obj, dataset, preamble=None, file_meta=None, is_implicit_VR=True, is_little_endian=True):
        """Initialize a DICOMDIR dataset read from a DICOM file
        Carries forward all the initialization from FileDataset class

        :param filename: full path and filename to the file. Use None if is a BytesIO.
        :param dataset: some form of dictionary, usually a Dataset from read_dataset()
        :param preamble: the 128-byte DICOM preamble
        :param file_meta: the file meta info dataset, as returned by _read_file_meta,
                or an empty dataset if no file meta information is in the file
        :param is_implicit_VR: True if implicit VR transfer syntax used; False if explicit VR. Default is True.
        :param is_little_endian: True if little-endian transfer syntax used; False if big-endian. Default is True.
        """
        if file_meta:
            class_uid = file_meta.MediaStorageSOPClassUID
            if not class_uid == 'Media Storage Directory Storage':
                print(class_uid, type(class_uid))
                msg = 'SOP Class is not Media Storage Directory (DICOMDIR)'
                raise InvalidDicomError(msg)
            FileDataset.__init__(self, filename_or_obj, dataset, preamble, file_meta, is_implicit_VR=True, is_little_endian=True)
            self.parse_records()

    def parse_records(self):
        """Build the hierarchy of given directory records, and structure
        into Patient, Studies, Series, Images hierarchy.

        This is intended for initial read of file only,
        it will not reorganize correctly if records are changed.

        :return: None
        """

        def get_siblings(record, map_offset_to_record):
            """Return a list of all siblings of the given directory record,
            including itself.
            """
            sibling_list = [
             record]
            current_record = record
            while current_record.OffsetOfTheNextDirectoryRecord:
                offset_of_next = current_record.OffsetoftheNextDirectoryRecord
                sibling = map_offset_to_record[offset_of_next]
                sibling_list.append(sibling)
                current_record = sibling

            return sibling_list

        records = self.DirectoryRecordSequence
        map_offset_to_record = {}
        for record in records:
            offset = record.seq_item_tell
            map_offset_to_record[offset] = record

        for record in records:
            child_offset = record.OffsetOfReferencedLowerLevelDirectoryEntity
            if child_offset:
                child = map_offset_to_record[child_offset]
                record.children = get_siblings(child, map_offset_to_record)
            else:
                record.children = []

        self.patient_records = get_siblings(records[0], map_offset_to_record)