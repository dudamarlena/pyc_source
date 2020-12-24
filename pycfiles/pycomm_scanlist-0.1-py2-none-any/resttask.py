# uncompyle6 version 3.6.7
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.3-fat/egg/pycommunity/resttask.py
# Compiled at: 2007-02-26 12:42:49
__doc__ = ' reSTructuredText base task\n'
import os, logging
from Cheetah.Template import Template
from utils import rest2Web
from utils import extractHeadTitle
from utils import linkChecker
from generator import BaseTask

class TaskView(object):
    """generates a base view"""

    def __init__(self, templatefile, restfile, glossaryfile, tutorial_folders, recipe_folders):
        (title, content) = rest2Web(restfile)
        content = linkChecker(content, glossaryfile, tutorial_folders, recipe_folders)
        self.title = title
        self._template = Template(open(templatefile).read(), searchList=[
         {'content': content, 'title': title}])

    def render(self):
        """renders the html"""
        return (
         self.title, str(self._template))

    __call__ = render


class TaskListView(TaskView):
    """generates a base view for lists"""

    def __init__(self, templatefile, filelist, title):
        self.title = title
        self._template = Template(open(templatefile).read(), searchList=[
         {'files': filelist, 'title': title}])


class RestTask(BaseTask):
    """creates the html content"""
    _templatefile = None

    def _getRestFiles(self, folder):
        """lists all rest file, given a folder"""
        files = []
        for file_ in os.listdir(folder):
            if file_.endswith('.txt'):
                files.append(file_)

        return [ os.path.realpath(os.path.join(folder, file_)) for file_ in files ]

    def _getFolders(self, configuration):
        """returns the folders"""
        raise NotImplementedError

    def _getTemplateFile(self, configuration):
        """returns the template"""
        raise NotImplementedError

    def _getTemplateListFile(self, configuration):
        """returns the template list"""
        raise NotImplementedError

    def _run(self, configuration):
        """generates recipes"""
        targets = configuration.targets.values()
        folders = self._getFolders(configuration)
        for folder in folders:
            restfiles = self._getRestFiles(folder)
            for target in targets:
                subfolder = os.path.join(target, '%ss' % self._getName())
                if not os.path.exists(subfolder):
                    os.mkdir(subfolder)
                titles = []
                for restfile in restfiles:
                    view = TaskView(self._getTemplateFile(configuration), restfile, configuration.glossary, configuration.tutorials, configuration.recipes)
                    (title, result) = view()
                    titles.append(title)
                    file_name = os.path.split(restfile)[(-1)].split('.')[0]
                    path = os.path.join(subfolder, '%s.html' % file_name)
                    path = os.path.realpath(path)
                    logging.info('writing %s' % path)
                    html_file = open(path, 'w')
                    try:
                        html_file.write(result)
                    finally:
                        html_file.close()

                def getFileInfos(folder, file_):
                    path = os.path.join(folder, file_)
                    title = extractHeadTitle(path)
                    url = '%ss/%s' % (self._getName(), file_)
                    return (
                     title, url)

                restfiles = [ getFileInfos(subfolder, file_) for file_ in os.listdir(subfolder) if file_.endswith('.html')
                            ]
                rootfile = os.path.join(target, '%ss.html' % self._getName())
                view = TaskListView(self._getTemplateListFile(configuration), restfiles, self._getName())
                (title, result) = view()
                rootfile = os.path.realpath(rootfile)
                logging.info('writing %s' % rootfile)
                html_file = open(rootfile, 'w')
                try:
                    html_file.write(result)
                finally:
                    html_file.close()