# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/gerardo/Projects/nlp_model_gen/nlp_model_gen/packages/trainingModule/TrainExample/TrainExample.py
# Compiled at: 2019-06-14 18:07:58
# Size of source mod 2**32: 2175 bytes
from nlp_model_gen.constants.constants import TRAIN_EXAMPLE_STATUS_APPLIED, TRAIN_EXAMPLE_STATUS_APPROVED, TRAIN_EXAMPLE_STATUS_REJECTED, TRAIN_EXAMPLE_STATUS_SUBMITTED

class TrainExample:

    def __init__(self, example_id, sentence, tags, example_type, status=TRAIN_EXAMPLE_STATUS_SUBMITTED):
        self._TrainExample__example_id = example_id
        self._TrainExample__sentence = sentence
        self._TrainExample__tags = tags
        self._TrainExample__example_type = example_type
        self._TrainExample__status = status

    def get_example_id(self):
        return self._TrainExample__example_id

    def get_sentece(self):
        return self._TrainExample__sentence

    def get_tags(self):
        return self._TrainExample__tags

    def get_example_type(self):
        return self._TrainExample__example_type

    def get_status(self):
        return self._TrainExample__status

    def apply(self):
        """
        Cambia el estado del ejemplo a aplicado.
        """
        self._TrainExample__status = TRAIN_EXAMPLE_STATUS_APPLIED

    def approve(self):
        """
        Cambia el estado del ejemplo a aprobado.
        """
        self._TrainExample__status = TRAIN_EXAMPLE_STATUS_APPROVED

    def reject(self):
        """
        Cambia el estado del ejemplo a rechazado.
        """
        self._TrainExample__status = TRAIN_EXAMPLE_STATUS_REJECTED

    def to_dict(self):
        """
        Obtiene un diccionario a partir de los datos del ejemplo de entrenamiento.

        :return: [Dict] - Diccionario con la información del ejemplo de entrenamiento.
        """
        return {'id':self.get_example_id(), 
         'sentence':self.get_sentece(), 
         'tags':self.get_tags(), 
         'type':self.get_example_type(), 
         'status':self.get_status()}

    def get_annotations(self):
        """
        Devuelve un diccionario con el formato requerido por el NER de spacy para las
        anotaciones.

        :return: [List(Dict)] - Listado de anotaciones para el ejemplo
        """
        entities = list([])
        for entity in self.get_tags():
            data = (
             entity['i_pos'], entity['e_pos'], entity['entity'])
            entities.append(data)

        return (
         self.get_sentece(), {'entities': entities})