# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/prihodad/Documents/projects/visitor/golm/golm/core/message_parser.py
# Compiled at: 2018-04-15 14:10:04
# Size of source mod 2**32: 2477 bytes
import emoji, re
from django.conf import settings
ENTITY_EXTRACTORS = settings.GOLEM_CONFIG.get('ENTITY_EXTRACTORS', [])

def add_default_extractors():
    if 'WIT_TOKEN' in settings.GOLEM_CONFIG:
        print('Adding wit extractor from wit token')
        from core.parsing import wit_extractor
        ENTITY_EXTRACTORS.append(wit_extractor.WitExtractor())


add_default_extractors()

def parse_text_message(text, num_tries=1):
    if len(ENTITY_EXTRACTORS) <= 0:
        print('No entity extractors configured!')
        return {'type':'message', 
         'entities':{'_message_text': {'value': text}}}
    else:
        entities = {}
        for extractor in ENTITY_EXTRACTORS:
            append = extractor.extract_entities(text)
            for entity, values in append.items():
                entities.setdefault(entity, []).extend(values)

        print('Extracted entities:', entities)
        append = parse_additional_entities(text)
        for entity, value in re.findall(re.compile('/([^/]+)/([^/]+)/'), text):
            if entity not in append:
                append[entity] = []
            append[entity].append({'value': value})

        for entity, values in append.items():
            if entity not in entities:
                entities[entity] = []
            entities[entity] += values

        entities['_message_text'] = [{'value': text}]
        parsed = {'entities':entities, 
         'type':'message'}
        return parsed


def parse_additional_entities(text):
    entities = {}
    chars = {':)':':slightly_smiling_face:', 
     '(y)':':thumbs_up_sign:',  ':(':':disappointed_face:',  ':*':':kissing_face:', 
     ':O':':face_with_open_mouth:',  ':D':':grinning_face:',  '<3':':heavy_black_heart:️', 
     ':P':':face_with_stuck-out_tongue:'}
    demojized = emoji.demojize(text)
    char_emojis = re.compile('(' + '|'.join(chars.keys()).replace('(', '\\(').replace(')', '\\)').replace('*', '\\*') + ')')
    demojized = char_emojis.sub(lambda x: chars[x.group()], demojized)
    if demojized != text:
        match = re.compile(':([a-zA-Z_0-9]+):')
        for emoji_name in re.findall(match, demojized):
            if 'emoji' not in entities:
                entities['emoji'] = []
            entities['emoji'].append({'value': emoji_name})

    return entities