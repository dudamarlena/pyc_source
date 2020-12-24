# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/qoaladep/gcp/storage/storage.py
# Compiled at: 2020-03-10 06:22:57
# Size of source mod 2**32: 1444 bytes
from google.cloud import storage

def download_from_storage(bucket_name, source_blob_name, destination_file_name):
    """[Function to download object from google cloud storage to local]
    
    Arguments:
        bucket_name {[string]} -- [Name of bucket in google cloud storage]
        source_blob_name {[string]} -- [Path to object in google cloud storage]
        destination_file_name {[string]} -- [Name and Path object in local]
    
    Returns:
        object  -- [Downloaded object from storage]
    """
    storage_client = storage.Client()
    bucket = storage_client.get_bucket(bucket_name)
    blob = bucket.blob(source_blob_name)
    blob.download_to_filename(destination_file_name)


def upload_to_storage(bucket_name, file_bytes, destination_blob_name, content_type):
    """[Function to upload object from local to google cloud storage]
    
    Arguments:
        bucket_name {[string]} -- [Name of bucket in google cloud storage]
        file_bytes {[bytes]} -- [Bytes of object that want to upload to google cloud storage]
        destination_blob_name {[string]} -- [Name and Path object in google cloud storage]
        content_type {[string]} -- [Type of data to save object in google cloud storage]
    """
    storage_client = storage.Client()
    bucket = storage_client.get_bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)
    blob.upload_from_string(file_bytes, content_type=content_type)