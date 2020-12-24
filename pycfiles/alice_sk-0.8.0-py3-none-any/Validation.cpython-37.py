# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/max/Workspace/snips/ProjectAliceModules/Tools/JsonValidator/src/validation.py
# Compiled at: 2019-09-01 18:03:37
# Size of source mod 2**32: 1668 bytes
from pathlib import Path
from jsonschema import Draft7Validator, exceptions
import json
from collections import defaultdict
from abc import ABC, abstractmethod

class validation(ABC):

    def __init__(self, modulePath: Path):
        self.modulePath = modulePath
        self.validModule = self.infinidict()
        self.dir_path = Path(__file__).resolve().parent
        self.base_path = self.dir_path.parent.parent.parent
        self.error = 0

    def infinidict(self):
        return defaultdict(self.infinidict)

    @property
    def validModules(self) -> dict:
        return self.validModule

    @property
    @abstractmethod
    def JsonSchema(self) -> dict:
        pass

    @property
    @abstractmethod
    def JsonFiles(self) -> list:
        pass

    @property
    def moduleName(self) -> str:
        return self.modulePath.name

    @property
    def moduleAuthor(self) -> str:
        return self.modulePath.parent.name

    def validateSyntax(self, file: Path) -> dict:
        data = dict()
        try:
            data = json.loads(file.read_text())
        except ValueError as e:
            try:
                self.validModule['syntax'][file.name] = str(e)
                self.error = 1
            finally:
                e = None
                del e

        return data

    def validateSchema(self) -> None:
        schema = self.JsonSchema
        for file in self.JsonFiles:
            self.validModule['schema'][file.name] = list()
            jsonPath = self.validModule['schema'][file.name]
            data = self.validateSyntax(file)
            try:
                Draft7Validator(schema).validate(data)
            except exceptions.ValidationError:
                self.error = 1
                for error in sorted((Draft7Validator(schema).iter_errors(data)), key=str):
                    jsonPath.append(error.message)

    @abstractmethod
    def validate(self) -> bool:
        pass