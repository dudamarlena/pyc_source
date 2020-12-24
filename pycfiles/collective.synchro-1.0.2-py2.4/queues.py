# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/collective/synchro/queues.py
# Compiled at: 2008-12-16 18:21:21
import os, random
from time import time
from zope.interface import implements
from interfaces.queues import IQueue
from interfaces import ISynchroData
from cPickle import load
from cPickle import dump
from cPickle import PickleError
from scripts.utils import create_queue_structure
from scripts.utils import LEVEL_ONE
from scripts.utils import LEVEL_TWO
from scripts.utils import good_name
from scripts.utils import islock
import config

class Queue(object):
    __module__ = __name__
    implements(IQueue)

    def __init__(self, path):
        """ constructor of a queue """
        self.path = path
        create_queue_structure(self)

    def put(self, data):
        """ export data in a queue
            @param : data an ISynchroData
            @return : filename in system or None if not succedd
        """
        if ISynchroData.providedBy(data):
            randint = random.randint(0, 1000000)
            uid = data.getUid()
            t = time()
            file_name_lock = 'data_%s_%f_%d.zs.lock' % (uid, t, randint)
            file_name = 'data_%s_%f_%d.zs' % (uid, t, randint)
            file_path_lock = os.path.join(self.export_to_process_path, file_name_lock)
            file_path = os.path.join(self.export_to_process_path, file_name)
            try:
                fd = open(file_path_lock, 'wb')
                try:
                    dump(data, fd)
                except PickleError, e:
                    fd.close()
                    os.unlink(file_path_lock)
                    config.logger.exception("can't pickle data")
                    return

                fd.close()
            except IOError, e:
                config.logger.exception("can't pickle data")
                return
            else:
                fd.close()
                os.rename(file_path_lock, file_path)
                config.logger.info('put %s to be imported' % file_path)
                return file_path

    def listQueue(self, type='EXPORT', queue='TO_PROCESS'):
        """ list element in queue """
        files = os.listdir(getattr(self, '%s_%s_path' % (type.lower(), queue.lower())))
        files.sort(lambda x, y: cmp(float(good_name(x).groups()[1]), float(good_name(y).groups()[1])))
        return files

    def importFile(self, context, file_name):
        """ import data in context
            @param : context : the context of the import
                     file : file wich contains data
        """
        to_process_file_name = os.path.join(self.import_to_process_path, file_name)
        processing_file_name = os.path.join(self.import_processing_path, file_name)
        done_file_name = os.path.join(self.import_done_path, file_name)
        error_file_name = os.path.join(self.import_error_path, file_name)
        os.rename(to_process_file_name, processing_file_name)
        fd = None
        try:
            fd = open(processing_file_name, 'r')
            data = load(fd)
        except PickleError, e:
            fd.close()
            config.logger.exception("can't unpickle data %s" % file_name)
            os.rename(processing_file_name, error_file_name)
            return
        except Exception, e:
            config.logger.exception('error in reading file %s' % file_name)
            os.rename(processing_file_name, error_file_name)
            return

        if fd is not None:
            fd.close()
        try:
            data(context)
        except Exception, e:
            config.logger.exception('error in import file %s' % file_name)
            os.rename(processing_file_name, error_file_name)
            return

        config.logger.info('import %s is ok' % file_name)
        os.rename(processing_file_name, done_file_name)
        return