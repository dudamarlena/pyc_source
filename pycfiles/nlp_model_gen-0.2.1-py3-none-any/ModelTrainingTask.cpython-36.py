# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/gerardo/Projects/nlp_model_gen/nlp_model_gen/packages/taskManager/modelTrainingTask/ModelTrainingTask.py
# Compiled at: 2019-06-14 18:07:58
# Size of source mod 2**32: 1712 bytes
from nlp_model_gen.packages.errorHandler.ErrorHandler import ErrorHandler
from nlp_model_gen.constants.constants import TASK_KEYS_MODEL_UPDATE, TASK_KEYS_WORD_PROCESSOR
from nlp_model_gen.packages.adminModule.AdminModuleController import AdminModuleController
from ..task.Task import Task

class ModelTrainingTask(Task):

    def __init__(self, id, model_id):
        super(ModelTrainingTask, self).__init__(id, {TASK_KEYS_MODEL_UPDATE: True, TASK_KEYS_WORD_PROCESSOR: False})
        self._ModelTrainingTask__model_id = model_id

    def get_model_id(self):
        return self._ModelTrainingTask__model_id

    def task_init_hook(self):
        """
        Método que se ejecutará en el template del init de la task de la clase padre.
        """
        try:
            admin = AdminModuleController()
            admin.apply_approved_examples(self._ModelTrainingTask__model_id)
            self.set_results(self.get_task_data())
        except Exception as e:
            error = ErrorHandler.get_error_dict(e)
            self.set_error_data(error)

    def check_model_relation(self, model_id, model_name):
        """
        Determina si una tarea esta relacionada con un determinado modelo utilizando su
        id y su nombre

        :model_id: [String] - Id del modelo

        :model_name: [String] - Nombre del modelo

        :return: [boolean] - True si el modelo esta releacionado, False en caso contrario.
        """
        return self._ModelTrainingTask__model_id == model_id

    def get_task_data(self):
        """
        Retorna los datos de la tarea.

        :return: [Dict] - Diccionario con los datos de la tarea.
        """
        return {'model_id': self.get_model_id()}