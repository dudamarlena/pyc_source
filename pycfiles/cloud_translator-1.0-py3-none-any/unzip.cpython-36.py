# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build\bdist.win-amd64\egg\cloud_training\data\unzip.py
# Compiled at: 2017-10-24 15:25:44
# Size of source mod 2**32: 1169 bytes
__doc__ = "\n   This script is being uploaded to the remote server before the training process\n   It shouldn't depend on the files from this project\n"
import argparse, os, zipfile
parser = argparse.ArgumentParser()
parser.add_argument('path', type=str, help='Path to directory with zipped files')
args = parser.parse_args()
unzip_files_list = []
for root, dirs, filenames in os.walk(args.path):
    for zip_filename in filenames:
        _, ext = os.path.splitext(zip_filename)
        if ext != '.zip':
            pass
        else:
            zip_file_path = os.path.join(root, zip_filename)
            file_path = zip_file_path[:-4]
            if os.path.exists(file_path):
                pass
            else:
                unzip_files_list.append((zip_file_path, root))

if not unzip_files_list:
    print('No files to unzip')
    exit()
print('Unzipping files...')
for zip_file_path, extract_dir in unzip_files_list:
    print('File: ' + zip_file_path)
    zip_ref = zipfile.ZipFile(zip_file_path, 'r')
    zip_ref.extractall(extract_dir)
    zip_ref.close()

print('Done')