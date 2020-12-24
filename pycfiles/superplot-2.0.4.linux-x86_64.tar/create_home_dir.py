# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/michael/anaconda2/lib/python2.7/site-packages/superplot/create_home_dir.py
# Compiled at: 2016-09-15 04:31:36
"""
A utility script to create a home directory containing config files and examples at a specified location.
"""
from argparse import ArgumentParser as arg_parser
import os, sys, shutil, warnings
from distutils.util import strtobool

def prompt(query):
    sys.stdout.write('%s [y/n]: ' % query)
    val = raw_input()
    try:
        ret = strtobool(val)
    except ValueError:
        sys.stdout.write('Please answer with a y/n\n')
        return prompt(query)

    return ret


def main():
    parser = arg_parser(description='Superplot home directory setup', conflict_handler='resolve')
    parser.add_argument('--dir', '-d', help='Location of user home directory', type=str, required=True)
    args = vars(parser.parse_args())
    user_dir = os.path.abspath(args['dir'])
    try:
        if not os.path.isdir(user_dir):
            os.mkdir(user_dir)
    except OSError as e:
        warnings.warn(('Could not create home directory: {}').format(e.strerror))
        sys.exit(1)

    script_dir = os.path.dirname(os.path.realpath(__file__))
    home_dir_file = os.path.join(script_dir, 'user_home.txt')
    with open(home_dir_file, 'wb') as (f):
        f.write(user_dir)
    config_path = os.path.join(user_dir, 'config.yml')
    copy_config = True
    if os.path.exists(config_path):
        print 'config.yml already present. Please note that versions of this file distributed with previous versions of superplot may not work with this release. If you wish to compare your customised config.yml with the current defaults, an example is distributed with the source code (superplot/config.yml).'
        copy_config = prompt(('Replace existing file: {}').format(config_path))
    if copy_config:
        copy_from = os.path.join(script_dir, 'config.yml')
        try:
            shutil.copy(copy_from, config_path)
        except shutil.Error as e:
            warnings.warn(('Error copying config file to user directory: {}').format(e.strerror))

    styles_dir = os.path.join(user_dir, 'styles')
    copy_style_sheets = True
    if os.path.isdir(styles_dir):
        copy_style_sheets = prompt(('Replace existing style sheets: {}').format(styles_dir))
        if copy_style_sheets:
            try:
                shutil.rmtree(styles_dir)
            except shutil.Error as e:
                warnings.warn(('Error removing existing style sheets: {}').format(e.strerror))

    if copy_style_sheets:
        try:
            copy_from = os.path.join(script_dir, 'plotlib/styles')
            shutil.copytree(copy_from, styles_dir)
        except shutil.Error as e:
            warnings.warn(('Error copying style sheets to user directory: {}').format(e.strerror))

    example_dir = os.path.join(user_dir, 'example')
    copy_examples = True
    if os.path.isdir(example_dir):
        copy_examples = prompt(('Replace existing example files: {}').format(example_dir))
        if copy_examples:
            try:
                shutil.rmtree(example_dir)
            except shutil.Error as e:
                warnings.warn(('Error removing existing example files: {}').format(e.strerror))

    if copy_examples:
        try:
            copy_from = os.path.join(script_dir, 'example')
            shutil.copytree(copy_from, example_dir)
        except shutil.Error as e:
            warnings.warn(('Error copying example files to user directory: {}').format(e.strerror))


if __name__ == '__main__':
    main()