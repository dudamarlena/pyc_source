# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/gerardo/Projects/nlp_model_gen/nlp_model_gen/packages/trainingModule/CustomEntity/CustomEntity.py
# Compiled at: 2019-06-14 18:07:58
# Size of source mod 2**32: 632 bytes


class CustomEntity:

    def __init__(self, name, description):
        self._CustomEntity__name = name
        self._CustomEntity__description = description

    def get_name(self):
        return self._CustomEntity__name

    def get_description(self):
        return self._CustomEntity__description

    def set_description(self, description):
        self._CustomEntity__description = description

    def to_dict(self):
        """
        Obtiene un diccionario a partir de los datos de la entidad.

        :return: [Dict] - Diccionario con los datos de la entidad
        """
        return {'name':self.get_name(), 
         'description':self.get_description()}