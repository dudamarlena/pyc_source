# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/protoLib/protoActionRep.py
# Compiled at: 2014-06-23 11:39:29
from django.http import HttpResponse
from django.utils.encoding import smart_str, smart_unicode
from models import getDjangoModel, ProtoDefinition
from protoActionList import Q2Dict, getQSet
from protoGrid import getBaseModelName
from utilsBase import getReadableError
from protoQbe import addFilter
from utils.downloadFile import getFullPath
from utilsWeb import JsonError, JsonSuccess
import json

def sheetConfigRep(request):
    """ Reporte basado en la definicion de plantillas ( sheets )
    """
    if not request.user.is_authenticated():
        return JsonError('readOnly User')
    if request.method != 'POST':
        return JsonError('invalid message')
    viewCode = request.POST.get('viewCode', '')
    sheetName = request.POST.get('sheetName', '')
    selectedKeys = request.POST.get('selectedKeys', [])
    selectedKeys = json.loads(selectedKeys)
    protoMeta, Qs = getReportBase(viewCode)
    if type(selectedKeys).__name__ == type([]).__name__ and selectedKeys.__len__() > 0:
        pFilter = {'pk__in': selectedKeys}
        Qs = addFilter(Qs, pFilter)
    pSheet = getSheetConf(protoMeta, sheetName)
    sheetName = pSheet.get('name', 'Auto')
    templateFp = pSheet.get('templateFp', '<span ' + sheetName + '.firstPage></span>')
    templateFp = templateFp + pSheet.get('templateBb', '<span ' + sheetName + '.BeforeBlock></span>')
    templateLp = pSheet.get('templateAb', '<span ' + sheetName + '.AfterBlock></span>')
    templateLp = templateLp + pSheet.get('templateLp', '<span ' + sheetName + '.lastPage></span>')
    templateEr = pSheet.get('templateEr', pSheet.get('template', ''))
    templateFp = getReport(['reportTitle'], templateFp, {'reportTitle': pSheet.get('title', sheetName)})
    MyReport = SheetReportFactory()
    MyReport.getReport(Qs, templateFp, templateEr, templateLp, protoMeta, pSheet.get('sheetDetails', []))
    return HttpResponse(MyReport.myReport)


def getSheetConf(protoMeta, sheetName):
    """ Obtiene un sheetConfig dado su nombre
        recibe  la definicion ( protoMeta ) y el nombre ( str )
        retorna sheetConfig ( obj )
    """
    try:
        pSheets = protoMeta.get('sheetConfig', [])
    except Exception as e:
        return {}

    pSheet = None
    for item in pSheets:
        if pSheet == None:
            pSheet = item
        if item.get('name', '') == sheetName:
            pSheet = item
            break

    if pSheet == None:
        pSheet = {}
    return pSheet


def getReportBase(viewCode):
    viewEntity = getBaseModelName(viewCode)
    try:
        model = getDjangoModel(viewEntity)
    except Exception as e:
        pass

    try:
        protoDef = ProtoDefinition.objects.get(code=viewCode)
        protoMeta = json.loads(protoDef.metaDefinition)
    except Exception as e:
        pass

    Qs = model.objects.select_related()
    return (
     protoMeta, Qs)


class SheetReportFactory(object):
    """ Construye un reporte basado en templates ( sheets )
    """

    def __init__(self):
        self.myReport = ''
        self.rowCount = 0

    def getReport(self, Qs, templateBefore, templateERow, templateAfter, protoMeta, sheetDetails):
        """ Construye el reporte en bloques recursivos ( basado en sheetDetails )
        # recibe :
        # myReport      : Reporte en curso
        # Qs            : QuerySet ya preparado
        # Templates     : Los templates son diferentes dependiendo la definicion del modelo
        # protoMeta     : Se requiere para llamar Q2Dict
        # sheetDetails  : Detalles a iterar
        """
        blockRowCount = 0
        pList = Q2Dict(protoMeta, Qs, False)
        bfProps = getProperties(protoMeta['fields'], templateBefore)
        erProps = getProperties(protoMeta['fields'], templateERow)
        afProps = getProperties(protoMeta['fields'], templateAfter)
        if pList.__len__() > 0:
            row = pList[0]
        else:
            row = {}
        self.myReport += getReport(bfProps, templateBefore, row)
        for row in pList:
            blockRowCount += 1
            self.rowCount += 1
            self.myReport += getReport(erProps, templateERow, row)
            for detail in sheetDetails:
                detailName = detail.get('name')
                detailName = detail.get('detailName', detailName)
                templateBb = detail.get('templateBb', '<span ' + detailName + '.BeforeDet></span>')
                templateAb = detail.get('templateAb', '<span ' + detailName + '.AfterDet></span>')
                templateEr = detail.get('templateEr', '<span ' + detailName + '.EveryRow></span>')
                detailConf = getDetailConf(protoMeta, detailName)
                if detailConf == None:
                    continue
                protoMetaDet, QsDet = getReportBase(detailConf['conceptDetail'])
                masterField = detailConf['masterField']
                idMaster = row[masterField.replace('pk', 'id')]
                pFilter = {detailConf['detailField']: idMaster}
                QsDet = addFilter(QsDet, pFilter)
                self.getReport(QsDet, templateBb, templateEr, templateAb, protoMetaDet, detail['sheetDetails'])

        self.myReport += getReport(afProps, templateAfter, row)
        return


def getProperties(fields, template):
    template = smart_str(template)
    if not template.__contains__('{{'):
        return []
    properties = ['id']
    for field in fields:
        fName = smart_str(field['name'])
        if template.__contains__('{{' + fName + '}}'):
            properties.append(fName)

    return set(properties)


def getDetailConf(protoMeta, detailName):
    try:
        pDetails = protoMeta.get('detailsConfig', [])
    except Exception:
        return

    for item in pDetails:
        itemName = item.get('detailName', '')
        if itemName == '':
            itemName = item.get('menuText ', '')
        if itemName == detailName:
            return item

    return


def getReport(props, template, row):
    sAux = smart_str(template[0:])
    for prop in props:
        rValue = smart_str(row.get(prop, ''))
        sAux = sAux.replace('{{' + smart_str(prop) + '}}', rValue)

    return sAux


def getLineCsv(line):
    sAux = ''
    for e in line:
        sAux = sAux + ',"' + smart_unicode(e) + '"'

    return sAux[1:] + '\n'


def protoCsv(request):
    if not request.user.is_authenticated():
        return JsonError('readOnly User')
    if request.method != 'POST':
        return JsonError('invalid message')
    protoMeta = request.POST.get('protoMeta', '')
    protoMeta = json.loads(protoMeta)
    protoFilter = request.POST.get('protoFilter', '')
    baseFilter = request.POST.get('baseFilter', '')
    sort = request.POST.get('sort', '')
    Qs, orderBy, fakeId, refAllow = getQSet(protoMeta, protoFilter, baseFilter, sort, request.user)
    refAllow = refAllow and False
    if orderBy:
        pRows = Qs.order_by(*orderBy)
    else:
        pRows = Qs.all()
    try:
        pList = Q2Dict(protoMeta, pRows, fakeId)
    except Exception as e:
        message = getReadableError(e)
        pList = [message]

    filename = protoMeta.get('viewCode', '') + '.csv'
    fullpath = getFullPath(request, filename)
    import codecs
    with codecs.open(fullpath, 'w', 'utf-8') as (outfile):
        outfile.write(getLineCsv(pList[0].keys()))
        for row in pList:
            outfile.write(getLineCsv(row.values()))

    return JsonSuccess({'message': filename})