# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/gerardo/Projects/nlp_model_gen/nlp_model_gen/packages/applicationModule/ApplicationModuleController.py
# Compiled at: 2019-06-14 18:07:58
# Size of source mod 2**32: 2211 bytes
from nlp_model_gen.utils.classUtills import Singleton
from nlp_model_gen.packages.modelManager.ModelManagerController import ModelManagerController
from nlp_model_gen.packages.trainingModule.ModelTrainingController import ModelTrainingController
from .dataSanitizer.DataSanitizer import DataSanitizer

class ApplicationModuleController(metaclass=Singleton):

    def __init__(self):
        self._ApplicationModuleController__model_manager = ModelManagerController()
        self._ApplicationModuleController__model_trainer = ModelTrainingController()

    def analyse_text(self, model_id, text, only_positives=False):
        """
        Analiza un texto aplicandole el modelo solicitado. El modelo debe existir.

        :model_id: [String] - Id del modelo a utilizar.

        :text: [String] - Texto a analizar.

        :only_positives: [boolean] - Si esta activado, devuelve solo los resultados positivos.

        :return: [List(Dict)] - Resultados del analisis, None si ha ocurrido un error.
        """
        sanitized_text = DataSanitizer.sanitize_text_for_analysis(text)
        return self._ApplicationModuleController__model_manager.analyze_text(model_id, sanitized_text, only_positives)

    def submit_training_example(self, model_id, example):
        """
        Provee de un ejemplo de entrenamiento. El mismo será agregado al sistema si cumple con 
        las validaciones de schema.

        :model_id: [String] - Id del modelo para el cual se provee el ejemplo.

        :example: [Dict] - Ejemplo de enetranamiento, se trata de un diccionario con dos partes:
        una oración y un arreglo que contiene entidades y su posición en la oración.
        """
        self._ApplicationModuleController__model_trainer.add_training_examples(model_id, [example])

    def get_available_tagging_entities(self):
        """
        Devuelve el listado de la entidades disponibles para etiquetar entidades en los ejemplos
        de entrenamiento.

        :return: [List(Dict)] - Lista con todas las entidades posibles.
        """
        available_entities_list = list([])
        available_entities = self._ApplicationModuleController__model_trainer.get_available_entities()
        for entity in available_entities:
            available_entities_list.append(entity.to_dict())

        return available_entities_list