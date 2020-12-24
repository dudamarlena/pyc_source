# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/gerardo/Projects/nlp_model_gen/nlp_model_gen/packages/wordProcessor/spanishFuzzyTermsGenerator/FuzzyTermsGenerator.py
# Compiled at: 2019-06-14 18:07:58
# Size of source mod 2**32: 5108 bytes
import itertools
from .helpers.demerauDistanceHelper import damerau_levenshtein_distance
from .helpers.fuzzyHelper import rnd_char_change, rnd_char_del, rnd_confuse_char, rnd_duplicate_char

class FuzzyTermsGenerator:
    __doc__ = '\n    Esta clase sirve como generador de variaciones para un token. A partir de un\n    token permite generar diferentes variaciones en su escritura.\n    '

    def __init__(self, general_config):
        self._FuzzyTermsGenerator__transformations = []
        self._FuzzyTermsGenerator__configs = {'confuse_chars':general_config['char_confusions'], 
         'confuse_chars_max_length':general_config['char_confusions_max_length']}
        self._FuzzyTermsGenerator__setup_transformations(general_config['transformations'])

    def __setup_transformations(self, transformation_keys):
        if 'rnd_confuse_char' in transformation_keys:
            self._FuzzyTermsGenerator__transformations.append(rnd_confuse_char)
        else:
            if 'rnd_char_del' in transformation_keys:
                self._FuzzyTermsGenerator__transformations.append(rnd_char_del)
            if 'rnd_char_change' in transformation_keys:
                self._FuzzyTermsGenerator__transformations.append(rnd_char_change)
            if 'rnd_duplicate_char' in transformation_keys:
                self._FuzzyTermsGenerator__transformations.append(rnd_duplicate_char)

    def set_config(self, general_config):
        self._FuzzyTermsGenerator__configs = {'confuse_chars':general_config['char_confusions'],  'confuse_chars_max_length':general_config['char_confusions_max_length']}
        self._FuzzyTermsGenerator__transformations.clear()
        self._FuzzyTermsGenerator__setup_transformations(general_config['transformations'])

    def get_fuzzy_tokens(self, token, max_distance=0):
        """
        Genera todas las posibles variaciones de la palabra con la que esta
        instanciada la clase (eliminación, trasposición, sustitución y
        duplicación) soportadas. De todas ellas filtra únicamente aquellas
        cuya distancia de demerau_levenshtein sea menor a la distancia máxima
        establecida para la clase y retorna un arreglo con aquellas que cumplan
        dicha condición.

        :token: Termino a deformar

        :max_distance: Distancia de demerau_levenstein maxima permitida

        :return: Arreglo con todas las variaciones que puede generar la clase
        para la palabra con la que fue instanciada, cuya distancia de
        demerau_levenshtein es igual o menor a la establecida.
        """
        transformation_permutations = self._FuzzyTermsGenerator__get_transform_permutations()
        transformation_list = []
        for transformation_sequence in transformation_permutations:
            transformation_list += self._FuzzyTermsGenerator__apply_transformation_sequence(token, transformation_sequence)

        filtered_list = self._FuzzyTermsGenerator__filter_variations_list(token, transformation_list, max_distance)
        return filtered_list

    def __apply_transformation_sequence(self, token, transformation_sequence):
        """
        Aplica una secuencia de transformaciones determinada en el orden recibido.

        :token: Termino a deformar.

        :transformation_sequence: Secuencia ordenada de funciones de tranforamación

        :return: lista de tokens transformados
        """
        variations_list = [
         token]
        for transformation in transformation_sequence:
            self._FuzzyTermsGenerator__apply_transformation(variations_list, transformation)

        return variations_list

    def __filter_variations_list(self, token, transformation_list, max_distance):
        """
        Filtra una lista de variaciones, eliminando aquellas entradas que esten 
        repetidas o que no cumplan con la distancia minima requerida al token.

        :token: Termino original.

        :transformation_list: Lista de transformaciones para el termino original

        :max_distance: Distancia de demerau_levenshtein maxima con el termino 
        original.

        :return: Lista de variaciones filtradas
        """
        filtered_list = list(set(transformation_list))
        filtered_list = filter(lambda transformed_token: damerau_levenshtein_distance(token, transformed_token, True) <= max_distance, filtered_list)
        return list(filtered_list)

    def __apply_transformation(self, token_list, transformation):
        """
        Aplica una transformación determinada a cada uno de los tokens contenidos
        en una lista de tokens

        :token_list: lista de tokens

        :transformation: Función de transformación a aplicar a cada uno de los 
        tokens

        :return: Lista de tokens transformados resultante de aplicar la 
        transformación dada a cada token
        """
        aux_list = []
        for token in token_list:
            aux_list += transformation(token, self._FuzzyTermsGenerator__configs)

        token_list += aux_list

    def __get_transform_permutations(self):
        """
        Obtiene todas las posibles permutaciones para la lista de permutaciones 
        posibles

        :return: lista de arreglos cada uno conteniendo las transformaciones
        en un orden diferente.
        """
        return itertools.permutations(self._FuzzyTermsGenerator__transformations)