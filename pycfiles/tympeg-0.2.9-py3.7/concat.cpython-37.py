# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/tympeg/concat.py
# Compiled at: 2017-06-08 14:08:58
# Size of source mod 2**32: 3526 bytes
import subprocess
from os import path, getcwd, remove, rename, rmdir
from .mediaobject import MediaObject, makeMediaObjectsInDirectory
from .util import list_files

def ffConcat(mediaObjectArray, outputFilepath):
    """

    :param mediaObjectArray: Array of mediaObjects in order of concatenation
    :param outputFilepath: String, output file path
    :return: subprocess completion data
    """
    for items in mediaObjectArray:
        if type(items) is not MediaObject:
            print('ffConcat needs an array of mediaObject. Item in index ' + str(mediaObjectArray.index(items)) + " in the passed array is type '" + str(type(items)) + "'!")
            print()
            print('Aborting pymeg.ffConcat()')
            print()
            return

    listFileName = path.join(str(getcwd()), 'tempFfConcat.txt')
    with open(listFileName, 'w') as (file):
        for items in mediaObjectArray:
            print(str(items.filePath))
            file.write("file '" + str(items.filePath) + "'" + '\n')

    ffmpegConcatArr = [
     'ffmpeg', '-f', 'concat', '-safe', '0', '-i', listFileName, '-c', 'copy', outputFilepath]
    try:
        try:
            processData = subprocess.run(ffmpegConcatArr, check=True)
        except subprocess.CalledProcessError as cpe:
            try:
                print('Error: CalledProcess in ttympeg.ffConcat()')
                print('CalledProcessError: ' + str(cpe))
                processData = None
            finally:
                cpe = None
                del cpe

    finally:
        remove(listFileName)

    return processData


def concat_files_in_directory(input_dir_path, alphabetical=True, delete_source=False, output_dir_path=''):
    """
    Attempts to concat ALL files in a directory, be careful! Places file in parent folder with first file's name
    then deletes source files if specified.
    :param input_dir_path: string, path to directory of files to be concatenated
    :param alphabetical: boolean, whether or not to alphabetize the files during concatenation
    :param delete_source: boolean, deletes source files when completed
    :param output_dir_path: string, optionally specify output directory
    :return: string, path of output file
    """
    media_object_array = makeMediaObjectsInDirectory(input_dir_path)
    if alphabetical:
        media_object_array = sorted(media_object_array, key=(lambda media: media.fileName))
    elif output_dir_path != '':
        output_dir = output_dir_path
    else:
        output_dir, tail = path.split(input_dir_path)
    output_path = path.join(output_dir, media_object_array[0].fileName)
    files = list_files(input_dir_path)
    num_files = len(files)
    if num_files == 1:
        rename(files[0], path.join(output_path))
    else:
        if num_files == 0:
            return
        ffConcat(media_object_array, output_path)
        if delete_source:
            if path.isfile(output_path):
                for file in files:
                    remove(file)

                rmdir(input_dir_path)
    return output_path