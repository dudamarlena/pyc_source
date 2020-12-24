# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/cloud_utils/file_utils/diagram_builders.py
# Compiled at: 2018-01-31 14:44:08
import blockdiag, nwdiag, seqdiag, actdiag

def _BuildDiagram(diag_class, source_json, filename):
    parser = diag_class.parser
    builder = diag_class.builder
    drawer = diag_class.drawer
    tree = parser.parse_string(source_json)
    diagram = builder.ScreenNodeBuilder.build(tree)
    draw = drawer.DiagramDraw('PNG', diagram, filename=filename)
    draw.draw()
    draw.save()
    return draw


def BuildNetworkDiagram(source_json, filename):
    return _BuildDiagram(diag_class=nwdiag, source_json=source_json, filename=filename)


def BuildBlockDiagram(source_json, filename):
    return _BuildDiagram(diag_class=blockdiag, source_json=source_json, filename=filename)


def BuildSequenceDiagram(source_json, filename):
    return _BuildDiagram(diag_class=seqdiag, source_json=source_json, filename=filename)


def BuildActivityDiagram(source_json, filename):
    return _BuildDiagram(diag_class=actdiag, source_json=source_json, filename=filename)