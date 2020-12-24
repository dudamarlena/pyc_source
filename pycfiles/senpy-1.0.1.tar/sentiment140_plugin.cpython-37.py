# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/j/git/lab.gsi/senpy/senpy/senpy/plugins/sentiment/sentiment140_plugin.py
# Compiled at: 2019-07-04 11:27:08
# Size of source mod 2**32: 2674 bytes
import requests, json
from senpy.plugins import SentimentBox
ENDPOINT = 'http://www.sentiment140.com/api/bulkClassifyJson'

class Sentiment140(SentimentBox):
    __doc__ = 'Connects to the sentiment140 free API: http://sentiment140.com'
    author = '@balkian'
    version = '0.2'
    url = 'https://github.com/gsi-upm/senpy-plugins-community'
    extra_params = {'language': {'@id':'lang_sentiment140', 
                  'description':'language of the text', 
                  'aliases':[
                   'language', 'l'], 
                  'required':True, 
                  'default':'auto', 
                  'options':[
                   'es', 'en', 'auto']}}
    classes = [
     'marl:Positive', 'marl:Neutral', 'marl:Negative']
    binary = True

    def predict_many(self, features, activity):
        lang = activity.params['language']
        data = []
        for feature in features:
            data.append({'text': feature[0]})

        res = requests.post(ENDPOINT, json.dumps({'language':lang, 
         'data':data}))
        for res in res.json()['data']:
            polarity = int(res['polarity'])
            neutral_value = 2
            if polarity > neutral_value:
                yield [
                 1, 0, 0]
                continue
            else:
                if polarity < neutral_value:
                    yield [
                     0, 0, 1]
                    continue
            yield [
             0, 1, 0]

    test_cases = [
     {'entry':{'nif:isString': 'I love Titanic'}, 
      'params':{},  'expected':{'nif:isString':'I love Titanic', 
       'marl:hasOpinion':[
        {'marl:hasPolarity': 'marl:Positive'}]}, 
      'responses':[
       {'url':ENDPOINT, 
        'method':'POST', 
        'json':{'data': [{'polarity': 4}]}}]}]