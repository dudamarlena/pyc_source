# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/gerardo/Projects/nlp_model_gen/nlp_model_gen/packages/taskManager/textAnalysisTask/TextAnalysisTask.py
# Compiled at: 2019-07-04 20:05:13
# Size of source mod 2**32: 2364 bytes
from nlp_model_gen.packages.errorHandler.ErrorHandler import ErrorHandler
from nlp_model_gen.constants.constants import TASK_KEYS_MODEL_UPDATE, TASK_KEYS_WORD_PROCESSOR
from nlp_model_gen.packages.applicationModule.ApplicationModuleController import ApplicationModuleController
from nlp_model_gen.packages.modelManager.ModelManagerController import ModelManagerController
from ..task.Task import Task

class TextAnalysisTask(Task):

    def __init__(self, id, model_id, text, only_positives):
        super(TextAnalysisTask, self).__init__(id, {TASK_KEYS_MODEL_UPDATE: True, TASK_KEYS_WORD_PROCESSOR: False})
        self._TextAnalysisTask__model_id = model_id
        self._TextAnalysisTask__text = text
        self._TextAnalysisTask__only_positives = only_positives

    def get_model_id(self):
        return self._TextAnalysisTask__model_id

    def get_text(self):
        return self._TextAnalysisTask__text

    def is_only_positives(self):
        return self._TextAnalysisTask__only_positives

    def check_model_relation(self, model_id, model_name):
        """
        Determina si una tarea esta relacionada con un determinado modelo utilizando su
        id y su nombre

        :model_id: [String] - Id del modelo

        :model_name: [String] - Nombre del modelo

        :return: [boolean] - True si el modelo esta releacionado, False en caso contrario.
        """
        model_manager = ModelManagerController()
        model = model_manager.get_model(self._TextAnalysisTask__model_id)
        if not model:
            return False
        else:
            return model_id == self._TextAnalysisTask__model_id and not model.is_loaded()

    def task_init_hook(self):
        """
        Método hook para completar el template de inicializadion en el padre.
        """
        try:
            application_module = ApplicationModuleController()
            results = application_module.analyse_text(self._TextAnalysisTask__model_id, self._TextAnalysisTask__text, self._TextAnalysisTask__only_positives)
            self.set_results(results)
        except Exception as e:
            error = ErrorHandler.get_error_dict(e)
            self.set_error_data(error)

    def get_task_data(self):
        """
        Retorna los datos de la tarea.

        :return: [Dict] - Diccionario con los datos de la tarea.
        """
        return {'model_id':self.get_model_id(), 
         'text':self.get_text(), 
         'only_positives':self.is_only_positives()}