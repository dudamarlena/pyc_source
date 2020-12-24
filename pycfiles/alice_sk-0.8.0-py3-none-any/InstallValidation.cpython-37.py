# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/max/Workspace/snips/ProjectAliceModules/Tools/JsonValidator/src/installValidation.py
# Compiled at: 2019-09-01 17:53:17
# Size of source mod 2**32: 412 bytes
from pathlib import Path
import json
import src.validation as validation

class installValidation(validation):

    @property
    def JsonSchema(self) -> dict:
        schema = self.dir_path / 'schemas/install-schema.json'
        return json.loads(schema.read_text())

    @property
    def JsonFiles(self) -> list:
        return self.modulePath.glob('*.install')

    def validate(self) -> bool:
        self.validateSchema()
        return self.error