# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/gerardo/Projects/nlp_model_gen/nlp_model_gen/packages/applicationModule/dataSanitizer/DataSanitizer.py
# Compiled at: 2019-06-14 18:07:58
# Size of source mod 2**32: 640 bytes
from nlp_model_gen.packages.errorHandler.ErrorHandler import ErrorHandler

class DataSanitizer:

    def __init__(self):
        pass

    @staticmethod
    def sanitize_text_for_analysis(text=''):
        """
        Elimina los caracteres no deseados que pueda tener un texto.

        :text: [String] - Texto a preparar.

        :return: [String] - Texto prepatado para el análisis.
        """
        if not isinstance(text, str):
            ErrorHandler.raise_error('E-0094')
        sanitized_text = text.replace('\n', ' ')
        sanitized_text = sanitized_text.replace('\t', ' ')
        return sanitized_text