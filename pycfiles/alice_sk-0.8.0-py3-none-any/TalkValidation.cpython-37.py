# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/max/Workspace/snips/ProjectAliceModules/Tools/JsonValidator/src/talkValidation.py
# Compiled at: 2019-09-01 18:00:14
# Size of source mod 2**32: 938 bytes
from pathlib import Path
import json
import src.validation as validation

class talkValidation(validation):

    @property
    def JsonSchema(self) -> dict:
        schema = self.dir_path / 'schemas/talk-schema.json'
        return json.loads(schema.read_text())

    @property
    def JsonFiles(self) -> list:
        return self.modulePath.glob('talks/*.json')

    def validateTypes(self) -> bool:
        all_slots = {}
        for file in self.JsonFiles:
            all_slots.update(self.validateSyntax(file))

        for file in self.JsonFiles:
            data = self.validateSyntax(file)
            self.validModule['types'][file.name] = [k for k, v in all_slots.items() if k not in data]
            if self.validModule['types'][file.name]:
                self.error = 1

    def validate(self) -> bool:
        self.validateSchema()
        self.validateTypes()
        return self.error