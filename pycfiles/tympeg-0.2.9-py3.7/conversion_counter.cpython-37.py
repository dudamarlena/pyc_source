# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/tympeg/scripts/conversion_counter.py
# Compiled at: 2018-03-13 17:58:16
# Size of source mod 2**32: 4483 bytes
from .. import MediaObject, get_dir_size_recursive
import time, os, math
from os import path

def save_log(directory, printable_list, invalid_files, terse=False):
    file_path = path.join(directory, 'ConversionLog' + str(time.strftime('%Y%m%d')) + '.txt')
    with open(file_path, 'w', encoding='utf8') as (log_file):
        log_file.write('Generated on: {}\n'.format(time.strftime('%b %d %Y, %I:%M %p')))
        total_size = 0
        for n in printable_list:
            total_size += math.floor(n[0] * 100 / 100)

        log_file.write('Total size of h264 files: {} MB\n\n\n'.format(total_size))
        for i in range(len(printable_list) - 1, -1, -1):
            log_file.write('{}\n'.format(printable_list[i][2]))
            log_file.write('Size of h264 files: {} MB\n'.format(math.floor(printable_list[i][0] * 100) / 100))
            log_file.write('Number of h264 files: {}\n'.format(printable_list[i][1]))
            if terse is False or printable_list[i][4] > 0:
                log_file.write('Size of invalid files: {} MB\n'.format(math.floor(printable_list[i][3] * 100) / 100))
                log_file.write('Number of invalid files: {}\n'.format(printable_list[i][4]))
            if not terse is False:
                if printable_list[i][5] > 0:
                    log_file.write('Size of other files & folders: {} MB\n'.format(math.floor(printable_list[i][5] * 100) / 100))
                log_file.write('\n\n')

        log_file.write('Invalid/malformed files:\n')
        for i in range(0, len(invalid_files) - 1):
            log_file.write('\t{}\n'.format(invalid_files[i]))


def analyze(directory, target_codec, print_progress=True):
    print('Analyzing {}'.format(directory))
    directory_list = []
    info_tuples = []
    file_extensions_to_analyze = ['.mp4', '.mkv', '.avi', '.m4v', '.wmv',
     '.MP4', '.MKV', '.AVI', '.M4V', '.wmv']
    invalid_files = []
    for fileNames in os.listdir(directory):
        if os.path.isdir(path.join(directory, fileNames)):
            directory_list.append(fileNames)

    directory_list = sorted(directory_list)
    for dirs in directory_list:
        num_of_files = 0
        size_of_files = 0
        num_of_invalid_files = 0
        size_of_invalid_files = 0
        size_of_other_files = 0
        if print_progress:
            print()
            print(dirs)
        for fileNames in os.listdir(path.join(directory, dirs)):
            file_path = os.path.join(directory, dirs, fileNames)
            if os.path.isdir(file_path):
                size_of_other_files += get_dir_size_recursive(file_path)
            elif any((extensions in fileNames for extensions in file_extensions_to_analyze)):
                media_info = MediaObject(file_path)
                media_info.run()
                if media_info.fileIsValid:
                    codec = media_info.videoCodec
                    if codec != target_codec:
                        num_of_files += 1
                        size_of_files += os.path.getsize(file_path)
                else:
                    invalid_files.append(file_path)
                    num_of_invalid_files += 1
                    size_of_invalid_files += os.path.getsize(file_path)
            else:
                size_of_other_files += os.path.getsize(file_path)

        size_of_files /= 1000000
        size_of_invalid_files /= 1000000
        size_of_other_files /= 1000000
        if num_of_files > 0:
            info_tuples.append((
             size_of_files, num_of_files, dirs, size_of_invalid_files, num_of_invalid_files, size_of_other_files))

    printable_list = sorted(info_tuples)
    return (printable_list, invalid_files)


def run_conversion_counter(directory, target_codec):
    printable, invalids = analyze(directory, target_codec)
    print('\n\nSaving log to {}'.format(directory))
    save_log(directory, printable, invalids)