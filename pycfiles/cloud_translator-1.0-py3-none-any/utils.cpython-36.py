# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build\bdist.win-amd64\egg\cloud_training\utils.py
# Compiled at: 2017-10-29 21:52:06
# Size of source mod 2**32: 2402 bytes
import logging, os, zipfile, errno

def data_dir(path: str=''):
    """Returns an absolute path to "data" directory.

    Args:
        path: A path which should be added to the "data" path.

    """
    res_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data')
    if path:
        res_path = os.path.join(res_path, path)
    return res_path


def zip_dir(path: str):
    """Zips non-zip files recursively one by one.

    Note:
        "Unzip" script is located in the "unzip.py" file to be transferred to a remote machine.

    Args:
        path: The directory in which the files should be zipped.

    """
    zip_files_list = []
    for root, dirs, filenames in os.walk(path):
        for filename in filenames:
            _, ext = os.path.splitext(filename)
            if ext == '.zip':
                pass
            else:
                file_path = os.path.join(root, filename)
                zip_file_path = file_path + '.zip'
                if os.path.exists(zip_file_path):
                    pass
                else:
                    zip_files_list.append((file_path, filename, zip_file_path))

    if not zip_files_list:
        logging.debug('No files to zip')
        return
    logging.debug('Zipping files...')
    for file_path, filename, zip_file_path in zip_files_list:
        logging.debug('File: ' + file_path)
        zip_file = zipfile.ZipFile(zip_file_path, 'w', zipfile.ZIP_DEFLATED)
        zip_file.write(file_path, filename)
        zip_file.close()

    logging.debug('Done')


def get_last_checkpoint_name(checkpoint_path):
    """Returns the last TensorFlow checkpoint name from a "checkpoints" directory.
    It's used to avoid a syncing of all saved checkpoints from S3.
    """
    if not os.path.exists(checkpoint_path):
        return False
    else:
        with open(checkpoint_path, 'r') as (f):
            last_model_str = f.readline()
        return os.path.basename(last_model_str[24:-2])


def check_path(path):
    """Creates a directory if it doesn't exist."""
    if not os.path.exists(path):
        try:
            os.makedirs(path)
        except OSError as exception:
            if exception.errno != errno.EEXIST:
                raise