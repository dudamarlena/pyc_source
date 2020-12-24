# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/gerardo/Projects/nlp_model_gen_plugins/nlp_model_gen_plugins/plugins/whatsappPlugin/WhatsappExtract.py
# Compiled at: 2019-07-04 20:38:00
# Size of source mod 2**32: 4373 bytes
"""
nlp_model_gen plugin for formatting whatsapp extracted data.

Expected format:
    De: From: 5492231111111@s.whatsapp.net Persona1
    Marca de hora: 23/11/2017 22:53:55(UTC-3)
    Aplicación de origen: WhatsApp
    Contenido:
    Hola Ana
    -----------------------------

"""
from nlp_model_gen_plugins.constants import WHATSAPP_DIVIDER, WHATSAPP_FROM, WHATSAPP_INLINE_DIVIDER, WHATSAPP_TIMESTAMP
from nlp_model_gen_plugins.utils.collectionsUtils import tuple_word_list_to_counter
from .WhatsappMessage import WhatsappMessage

class WhatsappExtract:

    def __init__(self, files, nlp_admin_instance=None, model_id=''):
        self._WhatsappExtract__extracts_list = []
        self._WhatsappExtract__nlp_admin_instance = nlp_admin_instance
        self._WhatsappExtract__model_id = model_id
        self._WhatsappExtract__initialize(files)
        self._WhatsappExtract__error = False

    def __get_message_field(self, message_parts, field):
        for part in message_parts:
            if part.startswith(field):
                return part.replace(field, '')

        return ''

    def __analyze_message(self, content):
        if not self._WhatsappExtract__nlp_admin_instance:
            return
        else:
            return self._WhatsappExtract__nlp_admin_instance.analyze_text(self._WhatsappExtract__model_id, content, True)

    def __process_file(self, file):
        messages_data = file.read()
        for message in messages_data.split(WHATSAPP_DIVIDER):
            message_parts = message.split(WHATSAPP_INLINE_DIVIDER)
            part_from = self._WhatsappExtract__get_message_field(message_parts, WHATSAPP_FROM)
            part_timestamp = self._WhatsappExtract__get_message_field(message_parts, WHATSAPP_TIMESTAMP)
            part_content = message_parts[(len(message_parts) - 2)]
            changos = self._WhatsappExtract__analyze_message(part_content)
            print(changos)
            analysis_task = changos['resource']['task_id']
            self._WhatsappExtract__extracts_list.append(WhatsappMessage(file.name, part_from, part_timestamp, part_content, self._WhatsappExtract__nlp_admin_instance, analysis_task))

    def __initialize(self, files):
        for file in files:
            self._WhatsappExtract__process_file(file)

    def get_extracts_list(self):
        if not self.get_status()['is_analyzed']:
            return
        else:
            return [message.to_dict() for message in self._WhatsappExtract__extracts_list]

    def get_ner_positives(self):
        if not self.get_status()['is_analyzed']:
            return
        else:
            return [message.to_dict() for message in self._WhatsappExtract__extracts_list if message.to_dict()['analysis_result']['ner_positive']]

    def get_tokenizer_positives(self):
        if not self.get_status()['is_analyzed']:
            return
        else:
            return [message.to_dict() for message in self._WhatsappExtract__extracts_list if message.to_dict()['analysis_result']['tokenizer_positive']]

    def get_positives_results(self):
        if not self.get_status()['is_analyzed']:
            return
        else:
            return [message.to_dict() for message in self._WhatsappExtract__extracts_list if message.to_dict()['analysis_result']['ner_positive'] or message.to_dict()['analysis_result']['tokenizer_positive']]

    def get_token_frequency(self):
        if not self.get_status()['is_analyzed']:
            return
        else:
            frequency_counter = dict({})
            for message in self._WhatsappExtract__extracts_list:
                token_frequency = message.get_token_frequency()
                for key in token_frequency.keys():
                    token_count = tuple_word_list_to_counter(token_frequency[key])
                    if key in frequency_counter.keys():
                        frequency_counter[key] = frequency_counter[key] + token_count
                    else:
                        frequency_counter[key] = token_count

            count_results = dict({})
            for key in frequency_counter.keys():
                count_results[key] = frequency_counter[key].most_common()

            return count_results

    def get_status(self):
        if not self._WhatsappExtract__nlp_admin_instance:
            return {'is_analyzed':False,  'has_error':True}
        else:
            for extract in self._WhatsappExtract__extracts_list:
                if not extract.is_analyzed():
                    return {'is_analyzed':False, 
                     'has_error':False}
                if extract.has_error():
                    return {'is_analyzed':False, 
                     'has_error':True}

            return {'is_analyzed':True, 
             'has_error':False}