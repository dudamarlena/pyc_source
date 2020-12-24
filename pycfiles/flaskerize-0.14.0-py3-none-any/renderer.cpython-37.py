# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/apryor/projects/flaskerize/flaskerize/renderer.py
# Compiled at: 2019-08-11 08:45:44
# Size of source mod 2**32: 772 bytes
from os import path
import argparse
from typing import Any, List, Optional
from flaskerize.parser import FzArgumentParser

class SchematicRenderer:
    __doc__ = 'Render Flaskerize schematics'

    def __init__(self, schematic_path: str):
        self.schematic_path = schematic_path
        self.arg_parser = self._check_get_arg_parser()

    def _check_get_arg_parser(self) -> Optional[argparse.ArgumentParser]:
        """Load argument parser from schema.json, if provided"""
        import json
        schema_path = f"{self.schematic_path}/schema.json"
        if not path.isfile(schema_path):
            return
        return FzArgumentParser(schema=schema_path)

    def render(self, args: List[Any]) -> None:
        """Renders the schematic"""
        pass