# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/gerardo/Projects/nlp_model_gen_plugins/nlp_model_gen_plugins/plugins/whatsappPlugin/WhatsappMessage.py
# Compiled at: 2019-07-04 18:48:06
# Size of source mod 2**32: 2476 bytes
from nlp_model_gen_plugins.constants import TASK_STATUS_FINISHED

class WhatsappMessage:

    def __init__(self, filename, origin, timestamp, content, nlp_admin_instance, analysis_task_id):
        self._WhatsappMessage__filename = filename
        self._WhatsappMessage__from = origin
        self._WhatsappMessage__content = content
        self._WhatsappMessage__timestamp = timestamp
        self._WhatsappMessage__nlp_admin_instance = nlp_admin_instance
        self._WhatsappMessage__analysis_task_id = analysis_task_id
        self._WhatsappMessage__analyzed = False
        self._WhatsappMessage__analysis_result = dict({})
        self._WhatsappMessage__token_frequency = dict({})
        self._WhatsappMessage__analysis_error = False
        self._WhatsappMessage__error_description = ''

    def __build_results_dict(self, results):
        return [result.to_dict() for result in results]

    def get_token_frequency(self):
        return self._WhatsappMessage__token_frequency

    def get_error_description(self):
        return self._WhatsappMessage__error_description

    def is_analyzed(self):
        if not self._WhatsappMessage__analyzed:
            self.check_analysis_task()
        return self._WhatsappMessage__analyzed

    def has_error(self):
        return self._WhatsappMessage__analysis_error

    def check_analysis_task(self):
        if not self._WhatsappMessage__nlp_admin_instance or self._WhatsappMessage__analyzed:
            return
        taks_status = self._WhatsappMessage__nlp_admin_instance.get_task_status(self._WhatsappMessage__analysis_task_id)['resource']
        if taks_status['status'] == TASK_STATUS_FINISHED:
            self._WhatsappMessage__analyzed = True
            if taks_status['error']['active']:
                self._WhatsappMessage__analysis_error = True
                self._WhatsappMessage__error_description = taks_status['error']['description_data']
            else:
                self._WhatsappMessage__analysis_result = {'error':False, 
                 'ner_results':self._WhatsappMessage__build_results_dict(taks_status['results']['ner_results']), 
                 'tokenizer_results':self._WhatsappMessage__build_results_dict(taks_status['results']['tokenizer_results']), 
                 'tokenizer_positive':len(taks_status['results']['tokenizer_results']) > 0, 
                 'ner_positive':len(taks_status['results']['ner_results']) > 0}
                self._WhatsappMessage__token_frequency = taks_status['results']['token_frequency']

    def to_dict(self):
        return {'filename':self._WhatsappMessage__filename,  'from':self._WhatsappMessage__from, 
         'timestamp':self._WhatsappMessage__timestamp, 
         'content':self._WhatsappMessage__content, 
         'analysis_task_id':self._WhatsappMessage__analysis_task_id, 
         'analysis_result':self._WhatsappMessage__analysis_result}