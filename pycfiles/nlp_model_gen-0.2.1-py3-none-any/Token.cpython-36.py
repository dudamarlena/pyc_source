# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/gerardo/Projects/nlp_model_gen/nlp_model_gen/packages/modelManager/token/Token.py
# Compiled at: 2019-06-14 18:07:58
# Size of source mod 2**32: 1893 bytes


class Token:
    _Token__base_form = ('', )
    _Token__is_out_of_vocabulary = False
    _Token__part_of_speech = ''
    _Token__sentence = 0.0
    _Token__sentiment = ''
    _Token__tag = ''
    _Token__token_text = ''
    _Token__positive = False
    _Token__analysis_result = None

    def __init__(self, base_form, is_out_of_vocabulary, part_of_speech, sentence, sentiment, tag, token_text):
        self._Token__base_form = base_form
        self._Token__is_out_of_vocabulary = is_out_of_vocabulary
        self._Token__part_of_speech = part_of_speech
        self._Token__sentence = sentence
        self._Token__sentiment = sentiment
        self._Token__tag = tag
        self._Token__token_text = token_text

    def get_base_form(self):
        return self._Token__base_form

    def get_token_text(self):
        return self._Token__token_text

    def is_positive(self):
        return self._Token__positive

    def to_dict(self):
        """
        Devuelve los atributos del objeto en Diccionario de Python

        :return: [Dict] - Diccionario con los datos del token.
        """
        return {'base_form':self._Token__base_form, 
         'is_out_of_vocabulary':self._Token__is_out_of_vocabulary, 
         'part_of_speech':self._Token__part_of_speech, 
         'sentence':self._Token__sentence, 
         'sentiment':self._Token__sentiment, 
         'tag':self._Token__tag, 
         'token_text':self._Token__token_text, 
         'positve':self._Token__positive, 
         'analysis_result':self._Token__analysis_result}

    def set_theme_detected(self, theme, message):
        """
        Setea al token como un positivo en la busqueda. Asigna el mensaje y el tema 
        encontrado en el mismo.

        :theme: [String] - Tema / categoria detectada.

        :message: [String] - Mensaje de detección.
        """
        self._Token__positive = True
        self._Token__analysis_result = {'category_detected':theme, 
         'alert_message':message}