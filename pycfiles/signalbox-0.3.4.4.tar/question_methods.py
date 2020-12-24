# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ben/dev/signalbox/twiliobox/question_methods.py
# Compiled at: 2014-08-27 19:26:12
import re
from django.conf import settings
from django.http import HttpResponse
from twiliobox.settings import *
from signalbox.custom_contracts import *

@contract
def reply_to_twilio(response):
    """
    Takes a twiliobox response and returns an HttpResponse
    :type response: is_twiml_response
    """
    return HttpResponse(str(response), content_type='text/xml')


@contract
def say_or_play_phrase(response, thingtosayorplay):
    """Function which adds a Twilio verb to a twilioresponse:
    either `say` or `play` depending on whether we pass a string of text or a url

    :type response: is_twiml_response
    :type thingtosayorplay: string
    """
    isaurl = re.search('^http://|^https://', thingtosayorplay.strip())
    if isaurl:
        response.play(thingtosayorplay)
    else:
        response.say(thingtosayorplay, language=settings.TTS_LANGUAGE, voice=settings.TTS_VOICE)
    return response


def say_or_play_question(response, question, reply=None):
    audiourl = question.extra_attrs.get('audio', None)
    if audiourl:
        response.play(audiourl)
    else:
        response.say(question.display_text(reply=reply), language=settings.TTS_LANGUAGE, voice=settings.TTS_VOICE)
    return


def hangup(twimlresponse, question, url, reply=None, *args, **kwargs):
    say_or_play_question(twimlresponse, question, reply)
    twimlresponse.hangup()
    return twimlresponse


def instruction(twimlresponse, question, url, reply=None, *args, **kwargs):
    if question.required:
        say_or_play_question(twimlresponse, question, reply)
    else:
        with twimlresponse.gather(numDigits=1, action=url, method='POST', timeout=0) as (g):
            say_or_play_question(g, question, reply)
    twimlresponse.redirect(url=url, method='POST')
    return twimlresponse


def multiple(twimlresponse, question, url, reply=None, *args, **kwargs):
    """Use Gather to capture a single digit input"""
    for i in range(QUESTION_REPEATS):
        with twimlresponse.gather(numDigits=1, action=url, method='POST', timeout=DEFAULT_TIMEOUT) as (g):
            say_or_play_question(g, question, reply)

    twimlresponse.redirect(url=url, method='POST')
    return twimlresponse


def listen(twimlresponse, question, url, reply=None, *args, **kwargs):
    """Use the Record verb on twilio to save a voice recording."""
    say_or_play_question(twimlresponse, question, reply)
    twimlresponse.record(action=url, method='POST')
    twimlresponse.redirect(url=url, method='POST')
    return twimlresponse