# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/Kamaelia/Visualisation/ER/ERVisualiserServer.py
# Compiled at: 2008-10-19 12:19:52
import Kamaelia.Visualisation.PhysicsGraph
from Kamaelia.Visualisation.PhysicsGraph.TopologyViewer import TopologyViewer as _TopologyViewer
_TopologyViewerServer = Kamaelia.Visualisation.PhysicsGraph.TopologyViewerServer
from PEntity import PEntity
from PRelation import PRelation
from PISA import PISA
from PAttribute import PAttribute
from ERLaws import AxonLaws
from ExtraWindowFurniture import ExtraWindowFurniture
from Kamaelia.Chassis.Pipeline import Pipeline
from Kamaelia.Visualisation.PhysicsGraph.chunks_to_lines import chunks_to_lines
from Kamaelia.Visualisation.PhysicsGraph.lines_to_tokenlists import lines_to_tokenlists

def ERVisualiserServer(**dictArgs):
    """    - particleTypes
    - laws
    - simCyclesPerRedraw
    - extraWindowFurniture
    """
    particleTypes = {'entity': PEntity, 'relation': PRelation.Relation, 
       'isa': PISA.Isa, 
       'attribute': PAttribute.Attribute}
    return _TopologyViewerServer(particleTypes=particleTypes, laws=AxonLaws(), simCyclesPerRedraw=3, extraDrawing=ExtraWindowFurniture(), **dictArgs)


def text_to_token_lists():
    return Pipeline(chunks_to_lines(), lines_to_tokenlists())


def ERVisualiser(**dictArgs):
    """    - particleTypes
    - laws
    - simCyclesPerRedraw
    - extraWindowFurniture
    """
    args = dict(dictArgs)
    particleTypes = {'entity': PEntity, 'relation': PRelation.Relation, 
       'isa': PISA.Isa, 
       'attribute': PAttribute.Attribute}
    args['particleTypes'] = particleTypes
    args.pop('laws', None)
    return _TopologyViewer(laws=AxonLaws(), simCyclesPerRedraw=3, showGrid=False, extraDrawing=ExtraWindowFurniture(), **args)


__kamaelia_prefabs__ = (
 ERVisualiserServer, ERVisualiser)