# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.15-x86_64/egg/samcli/local/lambdafn/zip.py
# Compiled at: 2020-03-21 12:32:11
# Size of source mod 2**32: 3947 bytes
"""
Helper methods to unzip an archive preserving the file permissions. Python's zipfile module does not yet support
this feature natively (https://bugs.python.org/issue15795).
"""
import os, logging, zipfile
from pathlib import Path
import requests
import samcli.lib.utils.progressbar as progressbar
LOG = logging.getLogger(__name__)

def unzip(zip_file_path, output_dir, permission=None):
    """
    Unzip the given file into the given directory while preserving file permissions in the process.

    Parameters
    ----------
    zip_file_path : str
        Path to the zip file

    output_dir : str
        Path to the directory where the it should be unzipped to

    permission : octal int
        Permission to set
    """
    with zipfile.ZipFile(zip_file_path, 'r') as (zip_ref):
        for file_info in zip_ref.infolist():
            name = file_info.filename
            extracted_path = os.path.join(output_dir, name)
            zip_ref.extract(name, output_dir)
            _set_permissions(file_info, extracted_path)
            _override_permissions(extracted_path, permission)

    _override_permissions(output_dir, permission)


def _override_permissions(path, permission):
    """
    Forcefully override the permissions on the path

    Parameters
    ----------
    path str
        Path where the file or directory
    permission octal int
        Permission to set

    """
    if permission:
        os.chmod(path, permission)


def _set_permissions(zip_file_info, extracted_path):
    """
    Sets permissions on the extracted file by reading the ``external_attr`` property of given file info.

    Parameters
    ----------
    zip_file_info : zipfile.ZipInfo
        Object containing information about a file within a zip archive

    extracted_path : str
        Path where the file has been extracted to
    """
    permission = zip_file_info.external_attr >> 16
    if not permission:
        LOG.debug('File %s in zipfile does not have permission information', zip_file_info.filename)
        return
    os.chmod(extracted_path, permission)


def unzip_from_uri(uri, layer_zip_path, unzip_output_dir, progressbar_label):
    """
    Download the LayerVersion Zip to the Layer Pkg Cache

    Parameters
    ----------
    uri str
        Uri to download from
    layer_zip_path str
        Path to where the content from the uri should be downloaded to
    unzip_output_dir str
        Path to unzip the zip to
    progressbar_label str
        Label to use in the Progressbar
    """
    try:
        get_request = requests.get(uri, stream=True, verify=(os.environ.get('AWS_CA_BUNDLE', True)))
        with open(layer_zip_path, 'wb') as (local_layer_file):
            file_length = int(get_request.headers['Content-length'])
            with progressbar(file_length, progressbar_label) as (p_bar):
                for data in get_request.iter_content(chunk_size=None):
                    local_layer_file.write(data)
                    p_bar.update(len(data))

        unzip(layer_zip_path, unzip_output_dir, permission=448)
    finally:
        path_to_layer = Path(layer_zip_path)
        if path_to_layer.exists():
            path_to_layer.unlink()