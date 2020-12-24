# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/prototype/actions/importOMS.py
# Compiled at: 2014-05-29 10:16:48
from xml.etree.ElementTree import ElementTree
import logging
from prototype.models import Model, Entity, Property, Relationship
from protoLib.utilsConvert import toBoolean
from protoLib.protoActionEdit import setSecurityInfo

class importOMS:

    def __init__(self, userProfile):
        self.__filename = ''
        self.project = None
        self.__tree = None
        self.__logger = logging.getLogger('Convert XML Database')
        self.__logger.setLevel(logging.DEBUG)
        formatter = logging.Formatter('[%(levelname)s] %(message)s')
        handler = logging.StreamHandler()
        handler.setFormatter(formatter)
        self.__logger.addHandler(handler)
        self.OK = 0
        self.ERROR_OPEN_FILE = 1
        self.ERR0R_PARSE_XML = 2
        self.OPERATIONAL_ERROR = 3
        self.ADDING_ERROR = 4
        self.ERROR = 5
        self.userProfile = userProfile
        return

    def loadFile(self, filename):
        self.__tree = ElementTree()
        self.__logger.info('Chargement du fichier...')
        try:
            self.__tree.parse(filename)
            self.__filename = filename
        except IOError:
            self.__logger.critical('Impossible d ouvrir le fichier...')
            return self.ERROR_OPEN_FILE
        except:
            self.__logger.critical('Erreur de traitement fichier...')
            return self.ERROR

        self.__logger.info('Chargement du fichier effectue...')
        return self.OK

    def __write(self):
        self.__logger.info('Ecriture dans la base de donnee...')
        fdsModel = ('code', 'category', 'modelPrefix')
        fdsEntity = ('code', )
        fdsProperty = ('code', )
        booProperty = ('isPrimary', 'isNullable', 'isRequired', 'isSensitive', 'isEssential')
        fdsRelationship = ('code', 'baseMin', 'baseMax', 'refMin', 'refMax')
        data = {}
        if self.__tree != None:
            xProjects = self.__tree.getiterator('domain')
            xModels = xProjects[0].getiterator('model')
            for xModel in xModels:
                dModel = Model()
                dModel.project = self.project
                modelUdps = []
                for child in xModel:
                    if child.tag in fdsModel:
                        setattr(dModel, child.tag, child.text)
                    elif child.tag == 'udps':
                        for xUdp in child:
                            modelUdps.append((xUdp.tag, xUdp.get('text')))

                try:
                    setSecurityInfo(dModel, data, self.userProfile, True)
                    dModel.save()
                except:
                    self.__logger.info('Error dModel.save')
                    return

                self.__logger.info('Model...' + dModel.code)
                xEntitys = xModel.getiterator('concept')
                for xEntity in xEntitys:
                    dEntity = Entity()
                    dEntity.model = dModel
                    for child in xEntity:
                        if child.tag in fdsEntity:
                            if child.text is not None:
                                setattr(dEntity, child.tag, child.text)
                        elif child.tag == 'physicalName':
                            setattr(dEntity, 'dbName', child.text)

                    try:
                        setSecurityInfo(dEntity, data, self.userProfile, True)
                        dEntity.save()
                    except:
                        self.__logger.info('Error dEntity.save')
                        return

                    self.__logger.info('Entity...' + dEntity.code)
                    xProperties = xEntity.getiterator('property')
                    for xProperty in xProperties:
                        dProperty = Property()
                        dProperty.entity = dEntity
                        for child in xProperty:
                            if child.tag in fdsProperty:
                                if child.text is not None:
                                    setattr(dProperty, child.tag, child.text)
                            elif child.tag in booProperty:
                                bValue = toBoolean(child.text)
                                setattr(dProperty, child.tag, bValue)

                        try:
                            setSecurityInfo(dProperty, data, self.userProfile, True)
                            dProperty.save()
                        except:
                            self.__logger.info('Error prpDom.save')
                            return

                    xForeigns = xEntity.getiterator('foreign')
                    for xForeign in xForeigns:
                        dForeign = Relationship()
                        dForeign.entity = dEntity
                        dForeign.refEntity = dEntity
                        for child in xForeign:
                            if child.tag in fdsRelationship:
                                setattr(dForeign, child.tag, child.text)
                            elif child.tag == 'baseConcept':
                                setattr(dForeign, 'dbName', child.text)
                            elif child.tag == 'alias':
                                setattr(dForeign, 'relatedName', child.text)
                            elif child.tag in booProperty:
                                bValue = toBoolean(child.text)
                                setattr(dForeign, child.tag, bValue)

                        try:
                            setSecurityInfo(dForeign, data, self.userProfile, True)
                            dForeign.save()
                        except Exception as e:
                            self.__logger.info('Error dForeign.save' + str(e))
                            return

        self.__logger.info('Ecriture dans la base de donnee effectuee...')
        return {'state': self.OK, 'message': 'Ecriture effectuee'}

    def doFkMatch(self):
        for dForeign in Relationship.objects.filter(entity__model__project=self.project):
            try:
                dReference = Entity.objects.get(model__project=dForeign.entity.model.project, code=dForeign.dbName)
            except:
                continue

            dForeign.refEntity = dReference
            if len(dForeign.code) < 6:
                dForeign.code = dForeign.entity.code + '-' + dReference.code
            try:
                dForeign.save()
            except Exception as e:
                self.__logger.info('Error dForeign.save' + str(e))
                continue

        self.__logger.info('Fk mathc effectuee...')

    def doImport(self, dProject):
        self.project = dProject
        dictWrite = self.__write()
        if dictWrite['state'] != self.OK:
            return dictWrite
        return {'state': self.OK, 'message': 'Ecriture effectuee base donnee'}