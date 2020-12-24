# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/gerardo/Projects/nlp_model_gen/nlp_model_gen/packages/modelManager/analyzerException/AnalyzerException.py
# Compiled at: 2019-06-14 18:07:58
# Size of source mod 2**32: 1923 bytes


class AnalyzerException:

    def __init__(self, base_form, token_text, enabled):
        self._AnalyzerException__base_form = base_form
        self._AnalyzerException__token_text = token_text
        self._AnalyzerException__enabled = enabled

    def is_enabled(self):
        return self._AnalyzerException__enabled

    def check_exception(self, token_text, base_form):
        """
        Valida si la excepción corresponde con el texto del token y la forma base,
        si esto es asi y, además, la excepción esta activada devuelve True.

        :token_text: [String] - Texto del token (el detectado).

        :base_form: [String] - Forma base que matchea el token.

        :return: [boolean] - True si la forma matchea y además la excepción esta 
        activada.
        """
        return self.match_exception(token_text, base_form) and self._AnalyzerException__enabled

    def match_exception(self, token_text, base_form):
        """
        Valida que los datos de una excepción sean coincidentes con los datos de
        esta excepción.

        :token_text: [String] - Texto del token (el detectado).

        :base_form: [String] - Forma base que matchea el token.

        :return: [Boolean] - True si la excepción matchea, False en caso contrario.
        """
        return token_text == self._AnalyzerException__token_text and base_form == self._AnalyzerException__base_form

    def enable(self):
        """
        Activa la excepción, la misma no debe encontrarse ya activada
        """
        self._AnalyzerException__enabled = True

    def disable(self):
        """
        Desactiva la excepción, la misma no debe estar desactivada previamente.
        """
        self._AnalyzerException__enabled = False

    def to_dict(self):
        """
        Devuelve un diccionario con los datos de la excepción.

        :return: [Dict] - Diccionario que representa la excepción
        """
        return {'base_form':self._AnalyzerException__base_form, 
         'token_text':self._AnalyzerException__token_text, 
         'enabled':self._AnalyzerException__enabled}