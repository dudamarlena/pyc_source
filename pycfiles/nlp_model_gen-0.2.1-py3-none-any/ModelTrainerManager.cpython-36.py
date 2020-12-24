# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/gerardo/Projects/nlp_model_gen/nlp_model_gen/packages/trainingModule/ModelTrainerManager/ModelTrainerManager.py
# Compiled at: 2019-06-14 18:07:58
# Size of source mod 2**32: 1184 bytes
from nlp_model_gen.packages.logger.Logger import Logger
from nlp_model_gen.packages.errorHandler.ErrorHandler import ErrorHandler

class ModelTrainerManager:

    def __init__(self):
        pass

    def __build_annotations(self, examples):
        """
        Crea el listado de ejemplos a partir de los ejemplos de entrenamiento.

        :examples: [List(TrainExample)] - Lista de ejemplos de entrenamiento.

        :return: [List] - Listado con la anotaciones.
        """
        Logger.log('L-0338')
        annotations = list([])
        for training_example in examples:
            annotations.append(training_example.get_annotations())

        Logger.log('L-0339')
        return annotations

    def train_model(self, model, examples):
        """
        Aplica un set de ejemplos de entrenamiento a un modelo.

        :model: [Model] - Id del modelo sobre el cual aplicar el set de ejemplos.

        :examples: [List] - Lista de ejemplos de entrenamiento
        """
        if not model:
            ErrorHandler.raise_error('E-0090')
        annotations = self._ModelTrainerManager__build_annotations(examples)
        model.train_model(annotations)