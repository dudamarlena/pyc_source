# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
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