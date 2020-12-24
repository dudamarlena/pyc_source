# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/prototype/models.py
# Compiled at: 2014-06-19 10:55:29
"""

140325:  Before merge 
        Drop PropertyEquivalence 
        Drop PropertyModel 
        Drop Diagram
        Drop DiagramEntity 

        Do syncDb
"""
from django.db import models
from django.db.models.signals import post_save, post_delete
from protoLib.models import ProtoModel
from protoLib.fields import JSONField, JSONAwareManager
from prototype.protoRules import ONDELETE_TYPES, BASE_TYPES, CRUD_TYPES, DB_ENGINE
from protoLib.utilsBase import slugify
PROTO_PREFIX = 'prototype.ProtoTable.'

class Project(ProtoModel):
    """Corresponds to a corporate conceptual level MCCD"""
    code = models.CharField(blank=False, null=False, max_length=200)
    description = models.TextField(blank=True, null=True)
    dbEngine = models.CharField(blank=True, null=True, max_length=20, choices=DB_ENGINE, default='sqlite3')
    dbName = models.CharField(blank=True, null=True, max_length=200)
    dbUser = models.CharField(blank=True, null=True, max_length=200)
    dbPassword = models.CharField(blank=True, null=True, max_length=200)
    dbHost = models.CharField(blank=True, null=True, max_length=200)
    dbPort = models.CharField(blank=True, null=True, max_length=200)

    def __unicode__(self):
        return slugify(self.code)

    class Meta:
        unique_together = ('code', 'smOwningTeam')

    protoExt = {'actions': [{'name': 'doImportSchema'}, {'name': 'doImportOMS', 'selectionMode': 'single', 'actionParams': []}], 'gridConfig': {'listDisplay': [
                                    '__str__', 'description', 'smOwningTeam']}}


class Model(ProtoModel):
    """
    Los modelos corresponde a una solucion especifica,  
    varios modelos pueden estar enmarcados en un dominio
    
    Los modelos son la unidad para generar una solucion ejecutable, 
    los modelos pueden tener prefijos especificos para todas sus componentes ( entidades ) 
    """
    project = models.ForeignKey('Project', blank=False, null=False)
    code = models.CharField(blank=False, null=False, max_length=200)
    category = models.CharField(max_length=50, blank=True, null=True)
    modelPrefix = models.CharField(blank=True, null=True, max_length=50)
    description = models.TextField(blank=True, null=True)

    class Meta:
        unique_together = ('project', 'code', 'smOwningTeam')

    unicode_sort = ('project', 'code')

    def __unicode__(self):
        return slugify(self.code)

    protoExt = {'actions': [{'name': 'doModelPrototype'}, {'name': 'doExportPrototype'}, {'name': 'doExportProtoJson'}], 'gridConfig': {'listDisplay': [
                                    '__str__', 'description', 'smOwningTeam']}}


class Entity(ProtoModel):
    """ 
    Entity corresponds to the PHYSICAL model;  
    """
    model = models.ForeignKey('Model', blank=False, null=False, related_name='entity_set')
    code = models.CharField(blank=False, null=False, max_length=200)
    dbName = models.CharField(blank=True, null=True, max_length=200)
    description = models.TextField(blank=True, null=True)
    unicode_sort = ('model', 'code')

    def __unicode__(self):
        return slugify(self.model.code + '-' + self.code)

    class Meta:
        unique_together = ('model', 'code', 'smOwningTeam')

    protoExt = {'actions': [
                 {'name': 'doEntityPrototype', 'selectionMode': 'single', 'actionParams': [
                                   {'name': 'viewCode', 'type': 'string', 'required': True, 'tooltip': 'option de menu (msi)'}]}], 
       'detailsConfig': [
                       {'__ptType': 'detailDef', 
                          'menuText': 'Properties', 
                          'conceptDetail': 'prototype.Property', 
                          'detailName': 'entity', 
                          'detailField': 'entity__pk', 
                          'masterField': 'pk'},
                       {'__ptType': 'detailDef', 
                          'menuText': 'Relationships', 
                          'conceptDetail': 'prototype.Relationship', 
                          'detailName': 'entity', 
                          'detailField': 'entity__pk', 
                          'masterField': 'pk'},
                       {'__ptType': 'detailDef', 
                          'menuText': 'Views', 
                          'conceptDetail': 'prototype.Prototype', 
                          'detailName': 'entity', 
                          'detailField': 'entity__pk', 
                          'masterField': 'pk'}], 
       'gridConfig': {'listDisplay': [
                                    '__str__', 'description', 'smOwningTeam']}}


class Property(ProtoModel):
    """ 
    Propiedades por tabla, definicion a nivel de modelo de datos.
    Las relaciones heredan de las propriedades y definien la cardinalidad 
    """
    entity = models.ForeignKey('Entity', related_name='property_set')
    code = models.CharField(blank=False, null=False, max_length=200)
    baseType = models.CharField(blank=True, null=True, max_length=50, choices=BASE_TYPES, default='string')
    prpLength = models.IntegerField(blank=True, null=True)
    prpScale = models.IntegerField(blank=True, null=True)
    vType = models.CharField(blank=True, null=True, max_length=50, choices=BASE_TYPES, default='string')
    prpDefault = models.CharField(blank=True, null=True, max_length=50)
    prpChoices = models.TextField(blank=True, null=True)
    isSensitive = models.BooleanField(default=False)
    description = models.TextField(blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    isPrimary = models.BooleanField(default=False)
    isLookUpResult = models.BooleanField(default=False)
    isNullable = models.BooleanField(default=False)
    isRequired = models.BooleanField(default=False)
    isReadOnly = models.BooleanField(default=False)
    isEssential = models.BooleanField(default=False)
    isForeign = models.BooleanField(editable=False, default=False)
    crudType = models.CharField(blank=True, null=True, max_length=20, choices=CRUD_TYPES)
    dbName = models.CharField(blank=True, null=True, max_length=200)

    def save(self, *args, **kwargs):
        if self.isPrimary:
            self.isRequired = True
            self.isLookUpResult = True
        super(Property, self).save(*args, **kwargs)

    class Meta:
        unique_together = ('entity', 'code', 'smOwningTeam')

    def __unicode__(self):
        return slugify(self.entity.code + '.' + self.code)

    unicode_sort = ('entity', 'code')
    protoExt = {'gridConfig': {'listDisplay': [
                                    '__str__', 'description', 'smOwningTeam']}}


class Relationship(Property):
    """
    * Tipo particula de propiedad q define las relaciones,  la definicion de la cardinlaidad y otras
    """
    refEntity = models.ForeignKey('Entity', related_name='refEntity_set', null=True)
    relatedName = models.CharField(blank=True, null=True, max_length=50)
    baseMin = models.CharField(blank=True, null=True, max_length=50)
    baseMax = models.CharField(blank=True, null=True, max_length=50)
    refMin = models.CharField(blank=True, null=True, max_length=50)
    refMax = models.CharField(blank=True, null=True, max_length=50)
    onRefDelete = models.CharField(blank=True, null=True, max_length=50, choices=ONDELETE_TYPES)
    typeRelation = models.CharField(blank=True, null=True, max_length=50)

    def __unicode__(self):
        return slugify(self.entity.code + '.' + self.code)

    def save(self, *args, **kwargs):
        self.isForeign = True
        super(Relationship, self).save(*args, **kwargs)

    protoExt = {'gridConfig': {'listDisplay': [
                                    '__str__', 'description', 'smOwningTeam']}, 
       'exclude': [
                 'baseType', 'prpLength', 'prpDefault', 'prpChoices']}


class PropertyEquivalence(ProtoModel):
    """ 
    Matriz de equivalencias "semantica"  entre propiedades
    
    Este es un caso particular de relacion donde en usa sola busqueda quisiera 
    obtener donde es source y donde es target, 
    
    se podria agregar un manejador q hicer:   where = sourse UNION where target, 
    o q al momento de guardar generara la relacion inversa y actualizara simpre los dos ( privilegiada )     
    """
    sourceProperty = models.ForeignKey('Property', blank=True, null=True, related_name='sourcePrp')
    targetProperty = models.ForeignKey('Property', blank=True, null=True, related_name='targetPrp')
    description = models.TextField(blank=True, null=True)

    def __unicode__(self):
        return slugify(self.sourceProperty.code + ' - ' + self.targetProperty.code)

    class Meta:
        unique_together = ('sourceProperty', 'targetProperty', 'smOwningTeam')

    def delete(self, *args, **kwargs):
        super(PropertyEquivalence, self).delete(*args, **kwargs)

    protoExt = {'gridConfig': {'listDisplay': [
                                    '__str__', 'description', 'smOwningTeam']}}


class Prototype(ProtoModel):
    """
    Esta tabla manejar la lista de  prototypos almacenados en customDefinicion, 
    Genera la "proto" pci;  con la lista de campos a absorber y los detalles posibles        
    """
    entity = models.ForeignKey(Entity, blank=False, null=False, related_name='prototype_set')
    code = models.CharField(blank=False, null=False, max_length=200, editable=False)
    description = models.TextField(blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    metaDefinition = models.TextField(blank=True, null=True)

    def __unicode__(self):
        return slugify(self.code)

    protoExt = {'gridConfig': {'listDisplay': [
                                    '__str__', 'entity', 'smOwningTeam']}}

    class Meta:
        unique_together = ('code', 'smOwningTeam')


class ProtoTable(ProtoModel):
    """
    Esta es el store de los prototipos   
    """
    entity = models.ForeignKey(Entity, blank=False, null=False)
    info = JSONField(default={})

    def __unicode__(self):
        return self.entity.code + ':' + self.info.__str__()

    def myStr(self, *args, **kwargs):
        val = ''
        for arg in args:
            try:
                val = val + '.' + slugify(self.info.get(arg[6:]))
            except:
                pass

        return val[1:]

    objects = JSONAwareManager(json_fields=['info'])
    protoExt = {'jsonField': 'info'}
    protoExt = {'gridConfig': {'listDisplay': [
                                    '__str__', 'smOwningTeam']}}


class Diagram(ProtoModel):
    project = models.ForeignKey('Project', blank=False, null=False)
    code = models.CharField(blank=False, null=False, max_length=200)
    description = models.TextField(blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    title = models.CharField(blank=True, null=True, max_length=100)
    prefix = models.CharField(blank=True, null=True, max_length=20)
    graphLevel = models.IntegerField(blank=True, null=True, default=0)
    grphMode = models.IntegerField(blank=True, null=True, default=0)
    graphForm = models.IntegerField(blank=True, null=True, default=0)
    showPrpType = models.BooleanField(default=False)
    showBorder = models.BooleanField(default=False)
    showFKey = models.BooleanField(default=False)
    info = JSONField(default={})
    objects = JSONAwareManager(json_fields=['info'])
    unicode_sort = ('project', 'code')

    def as_json(self):
        return dict(id=self.pk, code=self.code, projectID=self.project_id, smUUID=self.smUUID)

    def __unicode__(self):
        return slugify(self.project.code + '-' + self.code)

    class Meta:
        unique_together = ('project', 'code', 'smOwningTeam')

    protoExt = {'actions': [{'name': 'doModelGraph', 'selectionMode': 'multiple'}]}


class DiagramEntity(ProtoModel):
    """ 
    TODO: Entidades del diagrama  ( Relationship )    
    """
    diagram = models.ForeignKey('Diagram', blank=False, null=False)
    entity = models.ForeignKey(Entity, blank=False, null=False)
    info = JSONField(default={})
    objects = JSONAwareManager(json_fields=['info'])
    unicode_sort = ('diagram', 'entity')

    def __unicode__(self):
        return slugify(self.diagram.code + '-' + self.entity.code)

    class Meta:
        unique_together = ('diagram', 'entity', 'smOwningTeam')