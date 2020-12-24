# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/openspeechcorpus_cli/cmu_sphinx/clean_previous_configuration.py
# Compiled at: 2020-01-11 21:48:27
# Size of source mod 2**32: 1202 bytes
import argparse, os
FILES_CREATED = [
 '{}_test.fileids',
 '{}_test.transcription',
 '{}_train.fileids',
 '{}_train.transcription',
 '{}.dic',
 '{}.fileids',
 '{}.filler',
 '{}.phone',
 '{}.transcription',
 '{}.idngram',
 '{}.lm',
 '{}.lm.DMP',
 '{}.phone',
 '{}.vocab']

def clean_sphinx_configuration(etc_folder, project_name):
    for file in FILES_CREATED:
        file_to_delete = os.path.join(etc_folder, file.format(project_name))
        if os.path.exists(file_to_delete):
            print('Deleting {}'.format(file_to_delete))
            os.remove(file_to_delete)
        else:
            print('File {} Does not exists, skipping'.format(file_to_delete))


def execute_from_command_line():
    parser = argparse.ArgumentParser('Deletes all files created by the configure_sphinx command')
    parser.add_argument('project_name',
      help='Name of the sphinxtrain project')
    parser.add_argument('--etc_folder',
      default='etc',
      help='etc folder for Sphinx train')
    args = vars(parser.parse_args())
    clean_sphinx_configuration(args['etc_folder'], args['project_name'])