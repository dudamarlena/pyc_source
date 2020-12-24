# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-fat/egg/pycommunity/index.py
# Compiled at: 2007-02-23 11:08:20
""" Index render
"""
import os, logging
from shutil import copyfile
from Cheetah.Template import Template
from generator import BaseTask
from generator import registerTask
from utils import rest2Web

class IndexView(object):
    """renders a view using a cheetah template"""

    def __init__(self, templatefile, options):
        (title, content) = rest2Web(options['index'])
        self._template = Template(open(templatefile).read(), searchList=[
         {'options': options, 'title': title, 
            'content': content}])

    def render(self):
        """renders the html"""
        return str(self._template)

    __call__ = render


class IndexTask(BaseTask):
    """creates the index file"""

    def _getName(self):
        """returns the task name"""
        return 'index'

    def _copyStaticFile(self, path, target_folder):
        """copies static file into the target folder"""
        filename = os.path.split(path)[(-1)]
        target_file = os.path.join(target_folder, filename)
        logging.info('copying file to %s' % target_file)
        copyfile(path, target_file)

    def _run(self, configuration):
        """reads the glossary file, and generate
        the html file"""
        static_files = [ configuration.templates[name] for name in ('css', 'js')
                       ]
        media_folder = configuration.media
        targets = configuration.targets.values()
        view = IndexView(configuration.templates['index'], configuration.options)
        result = view()
        for target in targets:
            path = os.path.join(target, 'index.html')
            path = os.path.realpath(path)
            self._writeFile(path, result)
            for file_ in static_files:
                self._copyStaticFile(file_, target)

            logging.info('copying media')
            for file_ in os.listdir(media_folder):
                fullpath = os.path.join(media_folder, file_)
                if not os.path.isfile(fullpath):
                    continue
                target_folder = os.path.join(target, 'media')
                targetpath = os.path.join(target_folder, file_)
                if not os.path.exists(target_folder):
                    os.mkdir(target_folder)
                copyfile(fullpath, targetpath)


registerTask(IndexTask)