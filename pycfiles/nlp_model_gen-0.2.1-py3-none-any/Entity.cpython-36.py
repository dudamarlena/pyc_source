# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/gerardo/Projects/nlp_model_gen/nlp_model_gen/packages/modelManager/entity/Entity.py
# Compiled at: 2019-06-14 18:07:58
# Size of source mod 2**32: 577 bytes


class Entity:
    _Entity__text = ''
    _Entity__start = 0
    _Entity__end = 0
    _Entity__label = ''

    def __init__(self, text, start, end, label):
        self._Entity__text = text
        self._Entity__start = start
        self._Entity__end = end
        self._Entity__label = label

    def to_dict(self):
        """
        Retorna la entidad como un diccionario.

        :return: [Dict] - Diccionario con los datos de la entidad.
        """
        return {'text':self._Entity__text, 
         'start_pos':self._Entity__start, 
         'end_pos':self._Entity__end, 
         'label':self._Entity__label}