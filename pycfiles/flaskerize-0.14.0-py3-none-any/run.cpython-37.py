# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/apryor/projects/flaskerize/flaskerize/schematics/setup/run.py
# Compiled at: 2019-09-08 08:53:32
# Size of source mod 2**32: 322 bytes
from typing import Any, Dict
from flaskerize import SchematicRenderer

def run(renderer: SchematicRenderer, context: Dict[(str, Any)]) -> None:
    template_files = renderer.get_template_files()
    for filename in template_files:
        renderer.render_from_file(filename, context=context)

    renderer.print_summary()