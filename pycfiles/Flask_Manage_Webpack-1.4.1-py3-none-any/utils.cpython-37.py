# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/me/PycharmProjects/Flask-Manage-Webpack/flask_manage_webpack/utils.py
# Compiled at: 2019-11-15 03:22:42
# Size of source mod 2**32: 1184 bytes
import errno, os, shutil

def copy(src, destination):
    try:
        shutil.copytree(src, destination)
    except OSError as e:
        try:
            if e.errno == errno.ENOTDIR:
                shutil.copy(src, destination)
            else:
                print(f"assets folder initialized failed. {e}")
        finally:
            e = None
            del e


def init_webpack_config(app_name):
    edit_template = [
     'package.json',
     'postcss.config.js',
     'webpack.config.js']
    current_path = os.path.dirname(os.path.abspath(__file__))
    template_path = os.path.join(current_path, 'template')
    assets_path = os.path.join(template_path, 'assets')
    for template in edit_template:
        if os.path.isfile(template) is False:
            with open(f"{template_path}/{template}", 'rt') as (file_in):
                with open(template, 'wt') as (file_out):
                    for line in file_in:
                        file_out.write(line.replace('app', app_name))

        else:
            print(f"{template} initialized failed. File exists.")

    copy(assets_path, f"{os.getcwd()}/assets")