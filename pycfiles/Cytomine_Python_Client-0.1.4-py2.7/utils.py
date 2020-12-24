# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/cytomine/utils.py
# Compiled at: 2017-09-05 05:52:58
__author__ = 'Stévens Benjamin <b.stevens@ulg.ac.be>'
__contributors__ = ['Marée Raphaël <raphael.maree@ulg.ac.be>', 'Rollus Loïc <lrollus@ulg.ac.be']
__copyright__ = 'Copyright 2010-2015 University of Liège, Belgium, http://www.cytomine.be/'
import threading, Queue, copy, progressbar

def parameters_values_to_argv(parameters, parameters_values):
    argv = []
    for key in parameters_values:
        name, value = parameters_values[key]
        if name in parameters.keys():
            if type(value) is bool or value == 'True':
                if bool(value):
                    argv.append('--%s' % name)
            elif not value == 'False':
                argv.append('--%s' % name)
                argv.append('%s' % value)

    return argv


class ImageFetcher(threading.Thread):

    def __init__(self, queue, cytomine, override, pbar=None, verbose=True):
        threading.Thread.__init__(self)
        self.cytomine = copy.deepcopy(cytomine)
        self.verbose = verbose
        self.override = override
        self.queue = queue
        self.pbar = pbar

    def run(self):
        while True:
            url, filename, annotation = self.queue.get()
            download_successful = self.cytomine.fetch_url_into_file(url, filename, self.override)
            if not download_successful:
                import warnings
                warnings.warn('Crop Error for annotation %d' % annotation.id)
                if os.path.exists(filename):
                    os.remove(filename)
            self.queue.task_done()