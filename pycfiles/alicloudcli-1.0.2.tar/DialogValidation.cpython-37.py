# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/max/Workspace/snips/ProjectAliceModules/Tools/JsonValidator/src/dialogValidation.py
# Compiled at: 2019-09-01 17:59:26
# Size of source mod 2**32: 4767 bytes
from pathlib import Path
import json, re
import src.validation as validation
import src.dialogTemplate as dialogTemplate
from snips_nlu_parsers import get_all_builtin_entities
from unidecode import unidecode

class dialogValidation(validation):

    @property
    def JsonSchema(self) -> dict:
        schema = self.dir_path / 'schemas/dialog-schema.json'
        return json.loads(schema.read_text())

    @property
    def JsonFiles(self) -> list:
        return self.modulePath.glob('dialogTemplate/*.json')

    def is_builtin(self, slot: str) -> bool:
        return slot in get_all_builtin_entities()

    def installerJsonFiles(self, modulePath: str) -> list:
        return Path(modulePath).glob('*.install')

    def searchModule(self, moduleName: str) -> Path:
        for module in self.base_path.glob('PublishedModules/*/*'):
            if module.name == moduleName:
                return module

    def getRequiredModules(self, modulePath: str=None) -> set:
        modulePath = Path(modulePath) if modulePath else self.modulePath
        modules = {modulePath}
        for installer in self.installerJsonFiles(modulePath):
            data = self.validateSyntax(installer)
            if data and 'module' in data['conditions']:
                for module in data['conditions']['module']:
                    if module['name'] != self.moduleName:
                        path = self.searchModule(module['name'])
                        pathSet = {path} if path else set()
                        modules = modules.union(pathSet, self.getRequiredModules(path))

        return modules

    def getCoreModules(self) -> list:
        return self.modulePath.glob('PublishedModules/ProjectAlice/*')

    def getAllSlots(self, language: str) -> dict:
        modules = self.getRequiredModules().union(set(self.getCoreModules()))
        all_slots = {}
        for module in modules:
            path = module / 'dialogTemplate' / language
            if path.is_file():
                data = self.validateSyntax(path)
                all_slots.update(dialogTemplate(data).slots)

        return all_slots

    def searchMissingSlotValues(self, values: list, allSlots: dict) -> list:
        found = []
        for value in values:
            uValue = unidecode(value).lower()
            for slot in allSlots['values']:
                allValues = [
                 unidecode(slot['value']).lower()]
                if allSlots['useSynonyms']:
                    if 'synonyms' in slot:
                        allValues.extend([unidecode(x).lower() for x in slot['synonyms']])
                if uValue in allValues or allSlots['automaticallyExtensible']:
                    found.append(value)

        return [x for x in values if x not in found]

    def validateIntentSlots(self) -> None:
        all_slots = {}
        for file in self.JsonFiles:
            all_slots[file] = self.getAllSlots(file.name)

        for file in self.JsonFiles:
            jsonPath = self.validModule['utterances'][file.name]
            data = self.validateSyntax(file)
            for intentName, slots in dialogTemplate(data).utteranceSlots.items():
                for slot, values in slots.items():
                    if self.is_builtin(slot) or slot not in all_slots[file]:
                        self.error = 1
                        if intentName in jsonPath:
                            jsonPath['missingSlots'][intentName].append(slot)
                        else:
                            jsonPath['missingSlots'][intentName] = [
                             slot]
                    else:
                        missingValues = self.searchMissingSlotValues(values, all_slots[file][slot])
                    if missingValues:
                        self.error = 1
                        jsonPath['missingSlotValue'][intentName][slot] = missingValues

    def validateSlots(self) -> None:
        all_slots = {}
        for file in self.JsonFiles:
            data = self.validateSyntax(file)
            all_slots.update(dialogTemplate(data).slots)

        for file in self.JsonFiles:
            data = self.validateSyntax(file)
            missingSlots = self.validModule['slots'][file.name]
            missingSlots = [k for k, v in all_slots.items() if k not in dialogTemplate(data).slots]
            if missingSlots:
                self.error = 1

    def searchDuplicateUtterances(self) -> None:
        for file in self.JsonFiles:
            jsonPath = self.validModule['utterances'][file.name]['duplicates']
            data = self.validateSyntax(file)
            for intentName, shortUtterances in dialogTemplate(data).shortUtterances.items():
                for shortUtterance, utterances in shortUtterances.items():
                    if len(utterances) > 1:
                        jsonPath[intentName][shortUtterance] = utterances

    def validate(self) -> bool:
        self.validateSchema()
        self.validateSlots()
        self.searchDuplicateUtterances()
        self.validateIntentSlots()
        return self.error