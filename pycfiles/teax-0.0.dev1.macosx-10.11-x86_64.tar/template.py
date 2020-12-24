# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/site-packages/teax/system/template.py
# Compiled at: 2016-02-02 22:19:15
import os, time, shutil
from teax import conf, tty, TEAX_REAL_PATH, TEAX_WORK_PATH
from teax.messages import T_TEMPLATE_NOT_EXISTS, T_DIRECTORY_EXISTS, T_CREATING_TEMPLATE, T_USING_TEMPLATE
from teax.utils.slugify import slugify

class TemplateObject(object):
    PATH = ''
    BASENAME = ''

    def __init__(self, template):
        self.BASENAME = template.lower()
        self.PATH = TEAX_REAL_PATH + '/templates/' + self.BASENAME
        if not os.path.exists(self.PATH):
            tty.error(T_TEMPLATE_NOT_EXISTS % self.BASENAME)
        tty.info(T_USING_TEMPLATE % self.BASENAME)

    def save(self, path):
        _document_name = slugify(path)
        _local_path = TEAX_WORK_PATH + '/' + _document_name
        if os.path.exists(_local_path):
            timestamp = str(int(time.time()))
            _local_path += '-' + timestamp
            tty.warning(T_DIRECTORY_EXISTS % timestamp)
        shutil.copytree(self.PATH, _local_path)
        tty.info(T_CREATING_TEMPLATE % _document_name)
        _conf_file = TEAX_WORK_PATH + '/' + _document_name + '/' + 'teax.ini'
        conf.save(_conf_file, [
         'general.title',
         'general.authors',
         'general.keywords'])