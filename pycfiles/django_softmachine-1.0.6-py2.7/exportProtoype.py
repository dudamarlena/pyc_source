# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/prototype/actions/exportProto/exportProtoype.py
# Compiled at: 2014-06-19 10:55:29
from prototype.actions.pttActionTools import TypeEquivalence
from protoLib.utilsBase import slugify, repStr, getClassName
from cStringIO import StringIO

def exportPrototypeModel(request, pModel):
    strModel = StringIO()
    modelCode = slugify(pModel.code, '_')
    strModel.write('# -*- coding: utf-8 -*-\n\n')
    strModel.write('# This is an auto-generated model module by CeRTAE SoftMachine v13.12dgt\n')
    strModel.write(('# for model : "{0}"\n').format(modelCode))
    strModel.write("# You'll have to do the following manually to clean this up:\n")
    strModel.write('#     * Add specific procedures  (WFlow)\n\n')
    strModel.write('from django.db import models\n')
    strModel.write('from protoLib.models import ProtoModel\n')
    strModel.write('from protoLib.utilsBase import slugify\n')
    for pEntity in pModel.entity_set.all():
        strModel.write('\n')
        strModel.write(('class {0}(ProtoModel):\n').format(getClassName(pEntity.code)))
        arrKeys = []
        for pProperty in pEntity.property_set.all():
            pCode = slugify(pProperty.code, '_')
            if pProperty.isForeign:
                pType = getClassName(pProperty.relationship.refEntity.code)
                strAux = "{0} = models.ForeignKey('{1}', blank= {2}, null= {2}, related_name='{5}_{0}')\n"
            else:
                pType = TypeEquivalence.get(pProperty.baseType, 'CharField')
                intLength = pProperty.prpLength
                intScale = pProperty.prpScale
                if pType == 'CharField':
                    strAux = '{0} = models.{1}(blank= {2}, null= {2}, max_length= {3})\n'
                    if intLength == 0:
                        intLength = 200
                elif pType == 'DecimalField':
                    strAux = '{0} = models.{1}(blank= {2}, null= {2}, max_digits={3}, decimal_places= {4})\n'
                    if intLength == 0 or intLength > 24:
                        intLength = 48
                    if intScale < 0 or intScale > intLength:
                        intScale = 2
                elif pType == 'BooleanField':
                    strAux = '{0} = models.{1}()\n'
                else:
                    strAux = '{0} = models.{1}(blank = {2}, null = {2})\n'
            if pProperty.isRequired:
                strNull = 'False'
            else:
                strNull = 'True'
            if pProperty.isPrimary:
                arrKeys.append(pCode)
            strModel.write(repStr(' ', 4) + strAux.format(pCode, pType, strNull, str(intLength), str(intScale), slugify(pEntity.code, '_')))

        strModel.write('\n')
        strModel.write(repStr(' ', 4) + 'def __unicode__(self):\n')
        if arrKeys.__len__() > 0:
            strOptions = ''
            for pProperty in pEntity.property_set.all():
                if not pProperty.isPrimary:
                    continue
                if strOptions.__len__() > 0:
                    strOptions += " +  '.' + "
                if pProperty.isForeign or pProperty.baseType not in ('string', 'text'):
                    strAux = ('str( self.{0})').format(slugify(pProperty.code, '_'))
                else:
                    strAux = ('self.{0}').format(slugify(pProperty.code, '_'))
                strOptions += strAux

            strModel.write(repStr(' ', 8) + ('return slugify({0})\n').format(strOptions))
            strModel.write('\n')
            strModel.write(repStr(' ', 4) + 'class Meta:\n')
            strOptions = ''
            for pCode in arrKeys:
                strOptions += ("'{0}',").format(pCode)

            strModel.write(repStr(' ', 8) + ('unique_together = ({0})\n').format(strOptions))
        else:
            strModel.write(repStr(' ', 8) + "return 'NoKey'")

    strAux = strModel.getvalue()
    strModel.close()
    return strAux