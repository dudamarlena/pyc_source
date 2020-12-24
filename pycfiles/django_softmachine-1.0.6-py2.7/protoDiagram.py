# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/dbDesigner/protoDiagram.py
# Compiled at: 2014-06-19 10:55:26
from django.http import HttpResponse
from protoLib.utilsWeb import JsonError
from prototype.models import Project, Model, Entity, Diagram
from protoLib.utilsBase import JSONEncoder
from dbDesigner.service.diagramJSONAssembler import JSONAssembler
from dbDesigner.service.diagramService import addOrUpdateEntity, addOrUpdateConnector
import json, uuid

def getEntitiesJSONDiagram(request):
    """ return all tables from project
    """
    projectID = request.POST['projectID']
    selectedTables = []
    try:
        entities = Entity.objects.filter(model__project_id=projectID)
        table = {}
        for entity in entities:
            table = {'id': str(uuid.UUID(entity.smUUID)), 'tableName': entity.code}
            selectedTables.append(table)

    except Exception as e:
        print e
        return JsonError('Entity non trouvé')

    jsondict = {'success': True, 
       'message': '', 
       'tables': selectedTables}
    context = json.dumps(jsondict)
    return HttpResponse(context, content_type='application/json')


def getElementsDiagramFromSelectedTables(request):
    """ Creates diagram objects from selected tables in LiveSearchGrid
    """
    selectedTables = []
    connectors = []
    jsondict = {}
    objects = json.loads(request.body)
    UUIDAttributeList = []
    for element in objects:
        elementUUID = uuid.UUID(element['id']).hex
        UUIDAttributeList.append(elementUUID)

    try:
        entities = Entity.objects.filter(smUUID__in=UUIDAttributeList)
        assembler = JSONAssembler()
        assembler.getJSONElements(entities, selectedTables, connectors)
        jsondict = {'success': True, 
           'message': '', 
           'tables': selectedTables, 
           'connectors': connectors}
    except Exception as e:
        print e
        jsondict = {'success': False, 
           'message': 'Error on creating JSON file'}
        context = json.dumps(jsondict)
        return HttpResponse(context, content_type='application/json', status=500)

    context = json.dumps(jsondict)
    return HttpResponse(context, content_type='application/json')


def synchDiagramFromDB(request):
    """ Updates diagram objects from database
    """
    projectID = request.POST['projectID']
    selectedTables = []
    connectors = []
    try:
        entities = Entity.objects.filter(model__project_id=projectID)
        assembler = JSONAssembler()
        assembler.getJSONElements(entities, selectedTables, connectors)
    except Exception as e:
        print e
        return JsonError('Entity non trouvé')

    jsondict = {'success': True, 
       'message': '', 
       'tables': selectedTables, 
       'connectors': connectors}
    context = json.dumps(jsondict)
    return HttpResponse(context, content_type='application/json')


def synchDBFromDiagram(request):
    """ Create and synchronize elements in database
    """
    projectID = request.GET['projectID']
    try:
        project = Project.objects.get(id=projectID)
        user = request.user
        model = Model.objects.filter(project=project)
        if not model:
            model = Model.objects.create(project=project, code='default', smOwningTeam=project.smOwningTeam, smCreatedBy=user, smOwningUser=user)
        else:
            model = model[0]
        owningTeam = model.smOwningTeam
    except Exception as e:
        return JsonError(e)

    objects = json.loads(request.body)
    deletedConnectors = []
    UUIDList = []
    for element in objects:
        elementUUID = uuid.UUID(element['id']).hex
        if element['type'] == 'dbModel.shape.DBTable':
            UUIDList.append(elementUUID)
            addOrUpdateEntity(model, user, owningTeam, deletedConnectors, element, elementUUID)
        elif elementUUID not in deletedConnectors:
            sourceUUID = uuid.UUID(element['source']['node']).hex
            targetUUID = uuid.UUID(element['target']['node']).hex
            try:
                refEntity = Entity.objects.get(smUUID=sourceUUID)
                connEntity = Entity.objects.get(smUUID=targetUUID)
            except Exception as e:
                return JsonError(e)

            addOrUpdateConnector(element, elementUUID, refEntity, connEntity)

    selectedTables = []
    connectors = []
    try:
        entities = Entity.objects.filter(smUUID__in=UUIDList)
        assembler = JSONAssembler()
        assembler.getJSONElements(entities, selectedTables, connectors)
    except Exception as e:
        print e
        return JsonError('Entity non trouvé')

    jsondict = {'success': True, 
       'message': '', 
       'tables': selectedTables, 
       'connectors': connectors}
    context = json.dumps(jsondict)
    return HttpResponse(context, content_type='application/json')


def getDefaultDiagram(request):
    projectID = request.GET['projectID']
    user = request.user
    try:
        project = Project.objects.get(id=projectID)
        diagrams = Diagram.objects.filter(project_id=projectID)
        if not diagrams:
            diagram, created = Diagram.objects.get_or_create(project=project, code='default', smOwningTeam=project.smOwningTeam)
            diagram.smOwningUser = user
            diagram.smCreatedBy = user
            diagram.save()
        else:
            diagram = diagrams[0]
    except Exception as e:
        return JsonError(e)

    jsonDiagram = diagram.info
    if isinstance(jsonDiagram, dict):
        jsonDiagram = json.dumps(jsonDiagram, cls=JSONEncoder)
    jsondict = {'success': True, 
       'message': '', 
       'diagramID': diagram.id, 
       'diagramCode': diagram.code, 
       'diagram': jsonDiagram}
    context = json.dumps(jsondict)
    return HttpResponse(context, content_type='application/json')