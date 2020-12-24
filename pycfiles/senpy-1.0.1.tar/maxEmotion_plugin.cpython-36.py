# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/src/app/senpy/plugins/postprocessing/emotion/maxEmotion_plugin.py
# Compiled at: 2019-07-04 11:26:49
# Size of source mod 2**32: 7733 bytes
from senpy import PostProcessing, easy_test

class MaxEmotion(PostProcessing):
    __doc__ = 'Plugin to extract the emotion with highest value from an EmotionSet'
    author = '@dsuarezsouto'
    version = '0.1'

    def process_entry(self, entry, activity):
        if len(entry.emotions) < 1:
            yield entry
            return
        else:
            set_emotions = entry.emotions[0]['onyx:hasEmotion']
            if len(set_emotions) < 2:
                yield entry
                return
            max_emotion = set_emotions[0]
            for tmp_emotion in set_emotions:
                if tmp_emotion['onyx:hasEmotionIntensity'] > max_emotion['onyx:hasEmotionIntensity']:
                    max_emotion = tmp_emotion

            if max_emotion['onyx:hasEmotionIntensity'] == 0:
                max_emotion['onyx:hasEmotionCategory'] = 'neutral'
                max_emotion['onyx:hasEmotionIntensity'] = 1.0
        entry.emotions[0]['onyx:hasEmotion'] = [
         max_emotion]
        entry.emotions[0]['prov:wasGeneratedBy'] = activity.id
        yield entry

    def check(self, request, plugins):
        return 'maxemotion' in request.parameters and self not in plugins

    test_cases = [
     {'name':'If there are several emotions within an emotion set, reduce it to one.', 
      'entry':{'@type':'entry', 
       'onyx:hasEmotionSet':[
        {'@id':'Emotions0', 
         '@type':'emotionSet', 
         'onyx:hasEmotion':[
          {'@id':'_:Emotion_1538121033.74', 
           '@type':'emotion', 
           'onyx:hasEmotionCategory':'anger', 
           'onyx:hasEmotionIntensity':0},
          {'@id':'_:Emotion_1538121033.74', 
           '@type':'emotion', 
           'onyx:hasEmotionCategory':'joy', 
           'onyx:hasEmotionIntensity':0.3333333333333333},
          {'@id':'_:Emotion_1538121033.74', 
           '@type':'emotion', 
           'onyx:hasEmotionCategory':'negative-fear', 
           'onyx:hasEmotionIntensity':0},
          {'@id':'_:Emotion_1538121033.74', 
           '@type':'emotion', 
           'onyx:hasEmotionCategory':'sadness', 
           'onyx:hasEmotionIntensity':0},
          {'@id':'_:Emotion_1538121033.74', 
           '@type':'emotion', 
           'onyx:hasEmotionCategory':'disgust', 
           'onyx:hasEmotionIntensity':0}]}], 
       'nif:isString':'Test'}, 
      'expected':{'@type':'entry', 
       'onyx:hasEmotionSet':[
        {'@id':'Emotions0', 
         '@type':'emotionSet', 
         'onyx:hasEmotion':[
          {'@id':'_:Emotion_1538121033.74', 
           '@type':'emotion', 
           'onyx:hasEmotionCategory':'joy', 
           'onyx:hasEmotionIntensity':0.3333333333333333}]}], 
       'nif:isString':'Test'}},
     {'name':'If the maximum emotion has an intensity of 0, return a neutral emotion.', 
      'entry':{'@type':'entry', 
       'onyx:hasEmotionSet':[
        {'@id':'Emotions0', 
         '@type':'emotionSet', 
         'onyx:hasEmotion':[
          {'@id':'_:Emotion_1538121033.74', 
           '@type':'emotion', 
           'onyx:hasEmotionCategory':'anger', 
           'onyx:hasEmotionIntensity':0},
          {'@id':'_:Emotion_1538121033.74', 
           '@type':'emotion', 
           'onyx:hasEmotionCategory':'joy', 
           'onyx:hasEmotionIntensity':0},
          {'@id':'_:Emotion_1538121033.74', 
           '@type':'emotion', 
           'onyx:hasEmotionCategory':'negative-fear', 
           'onyx:hasEmotionIntensity':0},
          {'@id':'_:Emotion_1538121033.74', 
           '@type':'emotion', 
           'onyx:hasEmotionCategory':'sadness', 
           'onyx:hasEmotionIntensity':0},
          {'@id':'_:Emotion_1538121033.74', 
           '@type':'emotion', 
           'onyx:hasEmotionCategory':'disgust', 
           'onyx:hasEmotionIntensity':0}]}], 
       'nif:isString':'Test'}, 
      'expected':{'@type':'entry', 
       'onyx:hasEmotionSet':[
        {'@id':'Emotions0', 
         '@type':'emotionSet', 
         'onyx:hasEmotion':[
          {'@id':'_:Emotion_1538121033.74', 
           '@type':'emotion', 
           'onyx:hasEmotionCategory':'neutral', 
           'onyx:hasEmotionIntensity':1}]}], 
       'nif:isString':'Test'}}]


if __name__ == '__main__':
    easy_test()