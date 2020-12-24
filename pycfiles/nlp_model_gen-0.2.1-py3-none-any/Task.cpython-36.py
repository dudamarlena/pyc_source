# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/gerardo/Projects/nlp_model_gen/nlp_model_gen/packages/taskManager/task/Task.py
# Compiled at: 2019-06-14 18:07:58
# Size of source mod 2**32: 3799 bytes
from abc import ABC, abstractmethod
import datetime
from threading import Thread
from nlp_model_gen.packages.logger.Logger import Logger
from nlp_model_gen.packages.logger.assets.logColors import HIGHLIGHT_COLOR
from nlp_model_gen.utils.classUtills import Observable
from nlp_model_gen.constants.constants import TASK_KEYS_MODEL_UPDATE, TASK_KEYS_WORD_PROCESSOR, TASK_STATUS_CANCELLED, TASK_STATUS_FINISHED, TASK_STATUS_QUEUED, TASK_STATUS_RUNNING

class Task(Thread, Observable, ABC):

    def __init__(self, id, blocking_data=None):
        Thread.__init__(self)
        Observable.__init__(self)
        self._Task__id = id
        self._Task__status = TASK_STATUS_QUEUED
        self._Task__error = {'active':False,  'code':'',  'description':''}
        self._Task__init_time = -1
        self._Task__end_time = -1
        self._Task__results = None
        self._Task__blocking_data = blocking_data if blocking_data is not None else {TASK_KEYS_WORD_PROCESSOR: False, TASK_KEYS_MODEL_UPDATE: False}

    def get_id(self):
        return self._Task__id

    def get_status(self):
        return self._Task__status

    def get_error(self):
        return self._Task__error

    def get_init_time(self):
        return self._Task__init_time

    def get_end_time(self):
        return self._Task__end_time

    def get_results(self):
        return self._Task__results

    def is_blocking(self, task_keys):
        for key in task_keys:
            if self._Task__blocking_data[key]:
                return True

        return False

    def set_error_data(self, error):
        self._Task__error = {'active':True, 
         'description_data':error}

    def set_results(self, results):
        self._Task__results = results

    def run(self):
        """
        Inicia la ejecución del thread
        """
        Logger.log('L-0229', [{'text':self._Task__id,  'color':HIGHLIGHT_COLOR}])
        self._Task__init_time = datetime.datetime.now()
        self._Task__status = TASK_STATUS_RUNNING
        self.task_init_hook()
        self._Task__end_time = datetime.datetime.now()
        self._Task__status = TASK_STATUS_FINISHED
        self.notify(self)
        Logger.log('L-0230')

    def init(self):
        """
        Inicia la tarea.
        """
        if self._Task__status == TASK_STATUS_QUEUED:
            self.start()

    def abort(self):
        """
        Aborta la tarea. Su ejecución no debe haber iniciado para realizar esta operación.
        """
        if self._Task__status == TASK_STATUS_QUEUED:
            self._Task__status = TASK_STATUS_CANCELLED
            return True
        else:
            return False

    def get_task_status_data(self):
        """
        Retorna un resumen de la información de la tarea.

        :return: [Dict] - Diccionario con la inofrmación acerca del estdo de la tarea.
        """
        return {'id':self.get_id(), 
         'status':self.get_status(), 
         'init_time':self.get_init_time(), 
         'end_time':self.get_end_time(), 
         'error':self.get_error(), 
         'results':self.get_results()}

    @abstractmethod
    def check_model_relation(self, model_id, model_name):
        """
        Determina si una tarea esta relacionada con un determinado modelo utilizando su
        id y su nombre

        :model_id: [String] - Id del modelo

        :model_name: [String] - Nombre del modelo

        :return: [boolean] - True si el modelo esta releacionado, False en caso contrario.
        """
        pass

    @abstractmethod
    def task_init_hook(self):
        """
        Método que se ejecutará en el template del init de la task de la clase padre.
        """
        pass

    @abstractmethod
    def get_task_data(self):
        """
        Retorna los datos de la tarea, debe ser sobreescrito por las subclases
        """
        pass