# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/max/Workspace/snips/ProjectAliceModules/Tools/JsonValidator/src/dialogTemplate.py
# Compiled at: 2019-09-01 16:55:19
# Size of source mod 2**32: 2165 bytes
import re

class dialogTemplate:

    def __init__(self, dialogTemplate: dict):
        self.dialogTemplate = dialogTemplate

    @property
    def slots(self) -> dict:
        slots = {}
        if self.dialogTemplate:
            for slot in self.dialogTemplate['slotTypes']:
                slots[slot['name']] = slot

        return slots

    @property
    def intents(self) -> dict:
        intents = {}
        if self.dialogTemplate:
            for intent in self.dialogTemplate['intents']:
                intents[intent['name']] = intent

        return intents

    @property
    def shortUtterances(self) -> dict:

        def upper_repl(match):
            return match.group(1).upper()

        utterancesDict = {}
        for intentName, intents in self.intents.items():
            utterancesDict[intentName] = {}
            for utterance in intents['utterances']:
                short_utterance = utterance.lower()
                short_utterance = re.sub('{.*?:=>(.*?)}', upper_repl, short_utterance)
                short_utterance = re.sub('[^a-zA-Z1-9 ]', '', short_utterance)
                short_utterance = ' '.join(short_utterance.split())
                if short_utterance in utterancesDict[intentName]:
                    utterancesDict[intentName][short_utterance].append(utterance)
                else:
                    utterancesDict[intentName][short_utterance] = [
                     utterance]

        return utterancesDict

    @property
    def utteranceSlots(self) -> dict:
        utteranceSlotDict = {}
        for intentName, intents in self.intents.items():
            utteranceSlotDict[intentName] = {}
            for utterance in intents['utterances']:
                slotNames = re.findall('{(.*?):=>(.*?)}', utterance)
                for slot in intents['slots']:
                    for value, slotName in slotNames:
                        if slot['name'] == slotName:
                            if slot['type'] in utteranceSlotDict[intentName]:
                                if value not in utteranceSlotDict[intentName][slot['type']]:
                                    utteranceSlotDict[intentName][slot['type']].append(value)
                            else:
                                utteranceSlotDict[intentName][slot['type']] = [
                                 value]

        return utteranceSlotDict