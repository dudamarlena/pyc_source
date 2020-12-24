# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ben/dev/signalbox/signalbox/custom_contracts.py
# Compiled at: 2014-08-27 19:26:12
from contracts import contract, new_contract
from django.db.models.loading import get_model
import signalbox, ask, django
from twilio import twiml
is_twiml_response = lambda s: isinstance(s, twiml.Response)
new_contract('is_twiml_response', is_twiml_response)
model_instance = lambda s: isinstance(s, django.db.models.model)
new_contract('model_instance', model_instance)
is_answer = lambda s: isinstance(s, signalbox.models.Answer)
new_contract('is_answer', is_answer)
is_observation = lambda s: isinstance(s, signalbox.models.Observation)
new_contract('is_observation', is_observation)
is_reply = lambda s: isinstance(s, signalbox.models.Reply)
new_contract('is_reply', is_reply)
is_question = lambda s: isinstance(s, ask.models.Question)
new_contract('is_question', is_question)