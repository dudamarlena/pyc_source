# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/mahnve/.virtualenvs/blog/lib/python2.7/site-packages/sinor/file_util.py
# Compiled at: 2015-02-14 18:50:51
from sinor.config import config
import os

def read_file(file_name):
    with open(file_name) as (template_file):
        return template_file.read().decode('utf8')


def relative_href_for_file(file_name):
    return file_name.lstrip(os.getcwd()).lstrip(config.build_output_dir())


def absolute_href_for_file(file_name):
    return config.blog_url() + relative_href_for_file(file_name)