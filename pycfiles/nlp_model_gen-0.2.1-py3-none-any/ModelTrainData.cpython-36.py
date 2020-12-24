# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/gerardo/Projects/nlp_model_gen/nlp_model_gen/packages/trainingModule/ModelTrainData/ModelTrainData.py
# Compiled at: 2019-06-14 18:07:58
# Size of source mod 2**32: 2918 bytes
from nlp_model_gen.constants.constants import TRAIN_EXAMPLE_STATUS_APPROVED, TRAIN_EXAMPLE_STATUS_SUBMITTED
from ..TrainExample.TrainExample import TrainExample

class ModelTrainData:

    def __init__(self, model, training_examples_data):
        self._ModelTrainData__model = model
        self._ModelTrainData__training_examples = list([])
        for example_data in training_examples_data:
            example = TrainExample(example_data['id'], example_data['sentence'], example_data['tags'], example_data['type'], example_data['status'])
            self._ModelTrainData__training_examples.append(example)

    def get_model_id(self):
        """
        Devuelve el id del modelo al que corresponde el set de datos de entrenamiento.

        :return: [String] - Id del modelo.
        """
        return self._ModelTrainData__model.get_model_id()

    def add_training_example(self, example):
        """
        Agrega un ejemplo de entrenamiento al set de ejemplos de entrenamiento para el
        modelo.

        :example: [Dict] - Diccionario con los datos del ejemplo.
        """
        new_example = TrainExample(example['example_id'], example['sentence'], example['tags'], example['type'], example['status'])
        self._ModelTrainData__training_examples.append(new_example)

    def check_model(self, model_id):
        """
        Valida si un id de modelo corresponde con el modelo del set del administrador.

        :model_id: [String] - Id del modelo buscado

        :return: [boolean] - True si el modelo al que hace referencia el objeto corresponde
        con el id solicitado
        """
        return self._ModelTrainData__model.get_model_id() == model_id

    def get_example_by_id(self, example_id):
        """
        Valida si el modelo contiene un ejemplo cuyo id coincida con el solicitado.

        :example_id: [Int] - Id del ejemplo.

        :return: [TrainingExample] - Ejemplo de entrenamiento encontrado, None si no se 
        encontró.
        """
        try:
            training_example = next(example for example in self._ModelTrainData__training_examples if example.get_example_id() == example_id)
            return training_example
        except:
            return

    def get_approved_examples(self):
        """
        Devuelve un listado con los ejemplos de entrenamiento aprobados para el modelo.

        :return: [List(TrainExample)] - Listado de los ejemplos de entrenamiento aprobados.
        """
        return list(filter(lambda example: example.get_status() == TRAIN_EXAMPLE_STATUS_APPROVED, self._ModelTrainData__training_examples))

    def get_pending_examples(self):
        """
        Devuelve un listado de los ejemplos pendientes de decisión para el modelo.

        :return: [List(TrainExample)] - Listado de los ejemplos de entrenamiento pendientes
        de definir su aprobación.
        """
        return list(filter(lambda example: example.get_status() == TRAIN_EXAMPLE_STATUS_SUBMITTED, self._ModelTrainData__training_examples))