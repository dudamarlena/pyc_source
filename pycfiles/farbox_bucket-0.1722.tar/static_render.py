# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/hepochen/Dev/core/farbox_bucket/farbox_bucket/server/static/static_render.py
# Compiled at: 2020-02-14 04:22:51
import os, glob
from flask import g, abort
from farbox_bucket.utils.path import get_relative_path
from farbox_bucket.server.utils.response import send_file_with_304
from farbox_bucket.server.utils.request_path import get_bucket_request_path
static_folder_path = os.path.dirname(os.path.abspath(__file__))

def get_static_resources_map():
    static_resources_map = {}
    raw_filepaths = glob.glob('%s/*' % static_folder_path) + glob.glob('%s/*/*' % static_folder_path) + glob.glob('%s/*/*/*' % static_folder_path) + glob.glob('%s/*/*/*/*' % static_folder_path)
    for filepath in raw_filepaths:
        if os.path.isdir(filepath):
            continue
        ext = os.path.splitext(filepath)[(-1)].lower()
        if ext in ('.py', '.jade', '.coffee', '.scss', '.less', 'jpg', 'gif', 'png'):
            continue
        filename = os.path.split(filepath)[(-1)].lower()
        just_name = os.path.splitext(filename)[0]
        relative_path = get_relative_path(filepath, static_folder_path)
        names = [filename, just_name, relative_path]
        if just_name.startswith('jquery.'):
            names.append(just_name.replace('jquery.', '', 1))
        for name in names:
            static_resources_map[name] = filepath

    return static_resources_map


def send_static_file(path):
    abs_filepath = os.path.join(static_folder_path, path.strip('/'))
    if os.path.isfile(abs_filepath):
        g.is_system_static_file = True
        return send_file_with_304(abs_filepath)


web_static_resources_map = get_static_resources_map()

def send_static_frontend_resource(try_direct_path=False):
    path = get_bucket_request_path()
    if path.startswith('/fb_static/'):
        r_response = send_static_file(path.replace('/fb_static/', ''))
        if r_response:
            return r_response
        abort(404, 'static file under /fb_statice/ can not be found')
    if not try_direct_path and not path.startswith('/__'):
        return
    frontend_name = path.replace('/__', '', 1).strip('/')
    if frontend_name not in web_static_resources_map:
        return
    abs_filepath = web_static_resources_map[frontend_name]
    g.is_system_static_file = True
    return send_file_with_304(abs_filepath)