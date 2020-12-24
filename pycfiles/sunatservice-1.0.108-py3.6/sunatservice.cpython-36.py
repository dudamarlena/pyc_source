# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/sunatservice/sunatservice.py
# Compiled at: 2020-01-26 23:11:59
# Size of source mod 2**32: 27183 bytes
from .documents import Documents
from .sunatapi import SunatApi
from .ruc import Ruc
import json, sys

class Service:
    xmlPath = False
    fileName = False
    sunatAPI = False
    documentType = False
    keys = [
     '081OHTGAVHJZ4GOZJGJV', '081OHTGAVHJZ4GOZJ888', '081OHTGAVHJZ4GOZJ999']

    def consultRUC(self, ruc):
        rucService = Ruc()
        rucService.setXMLPath(self.xmlPath)
        response = rucService.consultRUC(ruc)
        return response

    def consultRUC_Pydevs(self, tipo_documento, ruc):
        rucService = Ruc()
        rucService.setXMLPath(self.xmlPath)
        if int(tipo_documento) == 6:
            response = rucService.consultRUC_Pydevs(tipo_documento, ruc)
        else:
            response = rucService.consultDNI_essalud(ruc)
        return response

    def processDocumentCancel(self, data):
        has_licence = self.validateLicence(data)
        if has_licence == True:
            has_licence = True
        else:
            return has_licence
        try:
            docs = Documents()
            docs.documentName = self.fileName
            docs.setXMLPath(self.xmlPath)
            docs.fillDocument('eDocCancel', data)
            if str(data['sunat_sol']['certificado']['pass']) == '':
                crt_pass = None
            else:
                crt_pass = str(data['sunat_sol']['certificado']['pass'])
            docs.signDocument(self.xmlPath + '/XMLcertificates/' + str(data['sunat_sol']['certificado']['key']), self.xmlPath + '/XMLcertificates/' + str(data['sunat_sol']['certificado']['crt']), crt_pass)
            wasVerified = docs.verifyDocument(self.xmlPath + '/XMLcertificates/' + str(data['sunat_sol']['certificado']['key']))
            response = {}
            if wasVerified:
                wasZipped = docs.zipDocument(self.xmlPath + '/XMLdocuments/3_signed/', self.xmlPath + '/XMLdocuments/4_compressed/', self.fileName)
                if wasZipped == True:
                    zipFileEncoded = docs.Base64EncodeDocument()
                    if data['accion'] == 'fill_submit':
                        dataSB = {}
                        dataSB['sendBillFile'] = self.xmlPath + str('/XMLrequests/sendSummary.XML')
                        dataSB['fileName'] = docs.documentName + str('.zip')
                        dataSB['contentFile'] = zipFileEncoded
                        dataSB['sunat_sol'] = data['sunat_sol']
                        docs.fillSenBill(dataSB)
                        self.sunatAPI.setEndPointType('INVOICE')
                        response = self.sunatAPI.doResquest()
                        if 'statusCode' in response:
                            if response['statusCode'] == str('OK'):
                                response['ticket'] = str(response['ticket_number'])
                                response['body'] = str('<br></br>') + str('La Comunicación de baja <b>') + str(data['document_id']) + str('</b> ha sido aceptada.') + str('<br></br>') + str('   - ticket #') + str(response['ticket'])
                                response['status'] = self.getStatus(data, response['ticket'])
                            else:
                                response['body'] = str('<br></br>') + str(response['statusMessage'])
                    response['xml_unsigned'] = docs.getXMLUnsignedDocument()
                    response['xml_signed'] = docs.getXMLSignedDocument()
                    return response
                else:
                    return 'ERROR_DOCUMENT_NOT_ZIPPED'
            else:
                return 'ERROR_DOCUMENT_NOT_VERIFIED'
        except Exception as e:
            exc_traceback = sys.exc_info()
            response = {}
            response['status'] = 'FAIL'
            response['code'] = 'SUNAT - Servidor Ocupado'
            response['body'] = 'Servidor no disponible temporalmente, vuelve a intentar.'
            return response

    def getCDR(self, data, document_type):
        dataSB = {}
        docs = Documents()
        docs.documentName = self.fileName
        docs.setXMLPath(self.xmlPath)
        dataSB['getCDRFile'] = self.xmlPath + str('/XMLrequests/getCDR.XML')
        dataSB['rucComprobante'] = data['sunat_sol']['ruc']
        dataSB['tipoComprobante'] = document_type
        dataSB['serieComprobante'] = data['serie']
        dataSB['numeroComprobante'] = data['numero']
        dataSB['sunat_sol'] = data['sunat_sol']
        docs.fillGetCDR(dataSB)
        response = self.sunatAPI.getCDR()
        return response

    def getStatus(self, data, ticket_number):
        dataSB = {}
        docs = Documents()
        docs.documentName = self.fileName
        docs.setXMLPath(self.xmlPath)
        dataSB['getStatusFile'] = self.xmlPath + str('/XMLrequests/getStatus.XML')
        dataSB['ticket'] = ticket_number
        dataSB['sunat_sol'] = data['sunat_sol']
        docs.fillGetStatus(dataSB)
        response = self.sunatAPI.getStatus()
        return response

    def processInvoiceFromSignedXML(self, data):
        dataSB = {}
        docs = Documents()
        docs.documentName = self.fileName
        docs.setXMLPath(self.xmlPath)
        zipFileEncoded = docs.Base64EncodeDocument()
        response = {}
        if zipFileEncoded != None:
            dataSB['sendBillFile'] = self.xmlPath + str('/XMLrequests/sendBill.XML')
            dataSB['fileName'] = self.fileName + str('.zip')
            dataSB['contentFile'] = zipFileEncoded
            dataSB['sunat_sol'] = data['sunat_sol']
            docs.fillSenBill(dataSB)
            self.sunatAPI.setEndPointType('INVOICE')
            response = self.sunatAPI.doResquest()
            response['cdr'] = self.getCDR(data, self.documentType)
            if 'statusCode' in response['cdr']:
                if response['status'] == str('OK'):
                    response['body']['description'] = str('\nCDR: ') + str('\n   Código: ') + str(response['cdr']['statusCode']) + str('\n   Mensaje: ') + str(response['cdr']['statusMessage']) + str('\n\n') + str(response['body']['description'])
                else:
                    response['body'] = str('\nCDR: ') + str('\n   Código: ') + str(response['cdr']['statusCode']) + str('\n   Mensaje: ') + str(response['cdr']['statusMessage']) + str('\n\n') + str(response['body'])
            response['xml_unsigned'] = docs.getXMLUnsignedDocument()
            response['xml_signed'] = docs.getXMLSignedDocument()
        else:
            response['status'] = 'FAIL'
            response['code'] = 'Sistema de Archivos'
            response['body'] = 'El documento XML no se encuentra en el servidor local'
        return response

    def processInvoice(self, data):
        has_licence = self.validateLicence(data)
        if has_licence == True:
            has_licence = True
        else:
            return has_licence
        try:
            docs = Documents()
            docs.documentName = self.fileName
            docs.setXMLPath(self.xmlPath)
            docs.fillDocument('invoice', data)
            if str(data['sunat_sol']['certificado']['pass']) == '':
                crt_pass = None
            else:
                crt_pass = str(data['sunat_sol']['certificado']['pass'])
            docs.signDocument(self.xmlPath + '/XMLcertificates/' + str(data['sunat_sol']['certificado']['key']), self.xmlPath + '/XMLcertificates/' + str(data['sunat_sol']['certificado']['crt']), crt_pass)
            wasVerified = docs.verifyDocument(self.xmlPath + '/XMLcertificates/' + str(data['sunat_sol']['certificado']['key']))
            response = {}
            if wasVerified:
                wasZipped = docs.zipDocument(self.xmlPath + '/XMLdocuments/3_signed/', self.xmlPath + '/XMLdocuments/4_compressed/', self.fileName)
                if wasZipped == True:
                    zipFileEncoded = docs.Base64EncodeDocument()
                    if data['accion'] == 'fill_submit':
                        dataSB = {}
                        dataSB['sendBillFile'] = self.xmlPath + str('/XMLrequests/sendBill.XML')
                        dataSB['fileName'] = docs.documentName + str('.zip')
                        dataSB['contentFile'] = zipFileEncoded
                        dataSB['sunat_sol'] = data['sunat_sol']
                        docs.fillSenBill(dataSB)
                        self.sunatAPI.setEndPointType('INVOICE')
                        response = self.sunatAPI.doResquest()
                        response['cdr'] = self.getCDR(data, str('01'))
                        if 'statusCode' in response['cdr']:
                            if response['status'] == str('OK'):
                                response['body']['description'] = str('\nCDR: ') + str('\n   Código: ') + str(response['cdr']['statusCode']) + str('\n   Mensaje: ') + str(response['cdr']['statusMessage']) + str('\n\n') + str(response['body']['description'])
                            else:
                                response['body'] = str('\nCDR: ') + str('\n   Código: ') + str(response['cdr']['statusCode']) + str('\n   Mensaje: ') + str(response['cdr']['statusMessage']) + str('\n\n') + str(response['body'])
                    response['xml_unsigned'] = docs.getXMLUnsignedDocument()
                    response['xml_signed'] = docs.getXMLSignedDocument()
                    return response
                else:
                    return 'ERROR_DOCUMENT_NOT_ZIPPED'
            else:
                return 'ERROR_DOCUMENT_NOT_VERIFIED'
        except Exception as e:
            exc_traceback = sys.exc_info()
            response = {}
            response['status'] = 'FAIL'
            response['code'] = 'INTERNO'
            response['body'] = getattr(e, 'message', repr(e)) + ' ON LINE ' + format(sys.exc_info()[(-1)].tb_lineno)
            return response

    def processTicket(self, data):
        has_licence = self.validateLicence(data)
        if has_licence == True:
            has_licence = True
        else:
            return has_licence
        try:
            docs = Documents()
            docs.documentName = self.fileName
            docs.setXMLPath(self.xmlPath)
            docs.fillDocument('ticket', data)
            docs.signDocument(self.xmlPath + '/XMLcertificates/' + str(data['sunat_sol']['certificado']['key']), self.xmlPath + '/XMLcertificates/' + str(data['sunat_sol']['certificado']['crt']), data['sunat_sol']['certificado']['pass'])
            wasVerified = docs.verifyDocument(self.xmlPath + '/XMLcertificates/' + str(data['sunat_sol']['certificado']['key']))
            response = {}
            if wasVerified:
                wasZipped = docs.zipDocument(self.xmlPath + '/XMLdocuments/3_signed/', self.xmlPath + '/XMLdocuments/4_compressed/', self.fileName)
                if wasZipped == True:
                    zipFileEncoded = docs.Base64EncodeDocument()
                    if data['accion'] == 'fill_submit':
                        dataSB = {}
                        dataSB['sendBillFile'] = self.xmlPath + str('/XMLrequests/sendBill.XML')
                        dataSB['fileName'] = docs.documentName + str('.zip')
                        dataSB['contentFile'] = zipFileEncoded
                        dataSB['sunat_sol'] = data['sunat_sol']
                        docs.fillSenBill(dataSB)
                        self.sunatAPI.setEndPointType('INVOICE')
                        response = self.sunatAPI.doResquest()
                        response['cdr'] = self.getCDR(data, str('03'))
                        if 'statusCode' in response['cdr']:
                            if response['status'] == str('OK'):
                                response['body']['description'] = str('\nCDR: ') + str('\n   Código: ') + str(response['cdr']['statusCode']) + str('\n   Mensaje: ') + str(response['cdr']['statusMessage']) + str('\n\n') + str(response['body']['description'])
                            else:
                                response['body'] = str('\nCDR: ') + str('\n   Código: ') + str(response['cdr']['statusCode']) + str('\n   Mensaje: ') + str(response['cdr']['statusMessage']) + str('\n\n') + str(response['body'])
                    response['xml_unsigned'] = docs.getXMLUnsignedDocument()
                    response['xml_signed'] = docs.getXMLSignedDocument()
                    return response
                else:
                    return 'ERROR_DOCUMENT_NOT_ZIPPED'
            else:
                return 'ERROR_DOCUMENT_NOT_VERIFIED'
        except Exception as e:
            exc_traceback = sys.exc_info()
            response = {}
            response['status'] = 'FAIL'
            response['code'] = 'INTERNO'
            response['body'] = getattr(e, 'message', repr(e)) + ' ON LINE ' + format(sys.exc_info()[(-1)].tb_lineno)
            return response

    def processCreditNote(self, data):
        has_licence = self.validateLicence(data)
        if has_licence == True:
            has_licence = True
        else:
            return has_licence
        try:
            docs = Documents()
            docs.documentName = self.fileName
            docs.setXMLPath(self.xmlPath)
            docs.fillDocument('creditNote', data)
            if str(data['sunat_sol']['certificado']['pass']) == '':
                crt_pass = None
            else:
                crt_pass = str(data['sunat_sol']['certificado']['pass'])
            docs.signDocument(self.xmlPath + '/XMLcertificates/' + str(data['sunat_sol']['certificado']['key']), self.xmlPath + '/XMLcertificates/' + str(data['sunat_sol']['certificado']['crt']), crt_pass)
            wasVerified = docs.verifyDocument(self.xmlPath + '/XMLcertificates/' + str(data['sunat_sol']['certificado']['key']))
            response = {}
            if wasVerified:
                wasZipped = docs.zipDocument(self.xmlPath + '/XMLdocuments/3_signed/', self.xmlPath + '/XMLdocuments/4_compressed/', self.fileName)
                if wasZipped == True:
                    zipFileEncoded = docs.Base64EncodeDocument()
                    if data['accion'] == 'fill_submit':
                        dataSB = {}
                        dataSB['sendBillFile'] = self.xmlPath + str('/XMLrequests/sendBill.XML')
                        dataSB['fileName'] = docs.documentName + str('.zip')
                        dataSB['contentFile'] = zipFileEncoded
                        dataSB['sunat_sol'] = data['sunat_sol']
                        docs.fillSenBill(dataSB)
                        self.sunatAPI.setEndPointType('INVOICE')
                        response = self.sunatAPI.doResquest()
                        response['cdr'] = self.getCDR(data, str('07'))
                        if 'statusCode' in response['cdr']:
                            if response['status'] == str('OK'):
                                response['body']['description'] = str('\nCDR: ') + str('\n   Código: ') + str(response['cdr']['statusCode']) + str('\n   Mensaje: ') + str(response['cdr']['statusMessage']) + str('\n\n') + str(response['body']['description'])
                            else:
                                response['body'] = str('\nCDR: ') + str('\n   Código: ') + str(response['cdr']['statusCode']) + str('\n   Mensaje: ') + str(response['cdr']['statusMessage']) + str('\n\n') + str(response['body'])
                    response['xml_unsigned'] = docs.getXMLUnsignedDocument()
                    response['xml_signed'] = docs.getXMLSignedDocument()
                    return response
                else:
                    return 'ERROR_DOCUMENT_NOT_ZIPPED'
            else:
                return 'ERROR_DOCUMENT_NOT_VERIFIED'
        except Exception as e:
            exc_traceback = sys.exc_info()
            response = {}
            response['status'] = 'FAIL'
            response['code'] = 'INTERNO'
            response['body'] = getattr(e, 'message', repr(e)) + ' ON LINE ' + format(sys.exc_info()[(-1)].tb_lineno)
            return response

    def processDebitNote(self, data):
        has_licence = self.validateLicence(data)
        if has_licence == True:
            has_licence = True
        else:
            return has_licence
        try:
            docs = Documents()
            docs.documentName = self.fileName
            docs.setXMLPath(self.xmlPath)
            docs.fillDocument('debitNote', data)
            docs.signDocument(self.xmlPath + '/XMLcertificates/' + str(data['sunat_sol']['certificado']['key']), self.xmlPath + '/XMLcertificates/' + str(data['sunat_sol']['certificado']['crt']), data['sunat_sol']['certificado']['pass'])
            wasVerified = docs.verifyDocument(self.xmlPath + '/XMLcertificates/' + str(data['sunat_sol']['certificado']['key']))
            response = {}
            if wasVerified:
                wasZipped = docs.zipDocument(self.xmlPath + '/XMLdocuments/3_signed/', self.xmlPath + '/XMLdocuments/4_compressed/', self.fileName)
                if wasZipped == True:
                    zipFileEncoded = docs.Base64EncodeDocument()
                    if data['accion'] == 'fill_submit':
                        dataSB = {}
                        dataSB['sendBillFile'] = self.xmlPath + str('/XMLrequests/sendBill.XML')
                        dataSB['fileName'] = docs.documentName + str('.zip')
                        dataSB['contentFile'] = zipFileEncoded
                        dataSB['sunat_sol'] = data['sunat_sol']
                        docs.fillSenBill(dataSB)
                        self.sunatAPI.setEndPointType('INVOICE')
                        response = self.sunatAPI.doResquest()
                        response['cdr'] = self.getCDR(data, str('08'))
                        if 'statusCode' in response['cdr']:
                            if response['status'] == str('OK'):
                                response['body']['description'] = str('\nCDR: ') + str('\n   Código: ') + str(response['cdr']['statusCode']) + str('\n   Mensaje: ') + str(response['cdr']['statusMessage']) + str('\n\n') + str(response['body']['description'])
                            else:
                                response['body'] = str('\nCDR: ') + str('\n   Código: ') + str(response['cdr']['statusCode']) + str('\n   Mensaje: ') + str(response['cdr']['statusMessage']) + str('\n\n') + str(response['body'])
                    response['xml_unsigned'] = docs.getXMLUnsignedDocument()
                    response['xml_signed'] = docs.getXMLSignedDocument()
                    return response
                else:
                    return 'ERROR_DOCUMENT_NOT_ZIPPED'
            else:
                return 'ERROR_DOCUMENT_NOT_VERIFIED'
        except Exception as e:
            exc_traceback = sys.exc_info()
            response = {}
            response['status'] = 'FAIL'
            response['code'] = 'INTERNO'
            response['body'] = getattr(e, 'message', repr(e)) + ' ON LINE ' + format(sys.exc_info()[(-1)].tb_lineno)
            return response

    def processDeliveryGuide(self, data):
        has_licence = self.validateLicence(data)
        if has_licence == True:
            has_licence = True
        else:
            return has_licence
        try:
            docs = Documents()
            docs.documentName = self.fileName
            docs.setXMLPath(self.xmlPath)
            docs.fillDocument('deliveryGuide', data)
            if str(data['sunat_sol']['certificado']['pass']) == '':
                crt_pass = None
            else:
                crt_pass = str(data['sunat_sol']['certificado']['pass'])
            docs.signDocument(self.xmlPath + '/XMLcertificates/' + str(data['sunat_sol']['certificado']['key']), self.xmlPath + '/XMLcertificates/' + str(data['sunat_sol']['certificado']['crt']), crt_pass)
            wasVerified = docs.verifyDocument(self.xmlPath + '/XMLcertificates/' + str(data['sunat_sol']['certificado']['key']))
            response = {}
            if wasVerified:
                wasZipped = docs.zipDocument(self.xmlPath + '/XMLdocuments/3_signed/', self.xmlPath + '/XMLdocuments/4_compressed/', self.fileName)
                if wasZipped == True:
                    zipFileEncoded = docs.Base64EncodeDocument()
                    if data['accion'] == 'fill_submit':
                        dataSB = {}
                        dataSB['sendBillFile'] = self.xmlPath + str('/XMLrequests/sendBill.XML')
                        dataSB['fileName'] = docs.documentName + str('.zip')
                        dataSB['contentFile'] = zipFileEncoded
                        dataSB['sunat_sol'] = data['sunat_sol']
                        docs.fillSenBill(dataSB)
                        self.sunatAPI.setEndPointType('GUIDE')
                        response = self.sunatAPI.doResquest()
                        response['cdr'] = self.getCDR(data, str('09'))
                        if 'statusCode' in response['cdr']:
                            if response['status'] == str('OK'):
                                response['body']['description'] = str('\nCDR: ') + str('\n   Código: ') + str(response['cdr']['statusCode']) + str('\n   Mensaje: ') + str(response['cdr']['statusMessage']) + str('\n\n') + str(response['body']['description'])
                            else:
                                response['body'] = str('\nCDR: ') + str('\n   Código: ') + str(response['cdr']['statusCode']) + str('\n   Mensaje: ') + str(response['cdr']['statusMessage']) + str('\n\n') + str(response['body'])
                    response['xml_unsigned'] = docs.getXMLUnsignedDocument()
                    response['xml_signed'] = docs.getXMLSignedDocument()
                    return response
                else:
                    return 'ERROR_DOCUMENT_NOT_ZIPPED'
            else:
                return 'ERROR_DOCUMENT_NOT_VERIFIED'
        except Exception as e:
            exc_traceback = sys.exc_info()
            response = {}
            response['status'] = 'FAIL'
            response['code'] = 'INTERNO'
            response['body'] = getattr(e, 'message', repr(e)) + ' ON LINE ' + format(sys.exc_info()[(-1)].tb_lineno)
            return response

    def processDeliveryGuideFromSignedXML(self, data):
        dataSB = {}
        try:
            docs = Documents()
            docs.documentName = self.fileName
            docs.setXMLPath(self.xmlPath)
            zipFileEncoded = docs.Base64EncodeDocument()
            response = {}
            if zipFileEncoded != None:
                dataSB['sendBillFile'] = self.xmlPath + str('/XMLrequests/sendBill.XML')
                dataSB['fileName'] = self.fileName + str('.zip')
                dataSB['contentFile'] = zipFileEncoded
                dataSB['sunat_sol'] = data['sunat_sol']
                docs.fillSenBill(dataSB)
                self.sunatAPI.setEndPointType('GUIDE')
                response = self.sunatAPI.doResquest()
                response['cdr'] = self.getCDR(data, str('09'))
                if 'statusCode' in response['cdr']:
                    if response['status'] == str('OK'):
                        response['body']['description'] = str('\nCDR: ') + str('\n   Código: ') + str(response['cdr']['statusCode']) + str('\n   Mensaje: ') + str(response['cdr']['statusMessage']) + str('\n\n') + str(response['body']['description'])
                    else:
                        response['body'] = str('\nCDR: ') + str('\n   Código: ') + str(response['cdr']['statusCode']) + str('\n   Mensaje: ') + str(response['cdr']['statusMessage']) + str('\n\n') + str(response['body'])
                response['xml_unsigned'] = docs.getXMLUnsignedDocument()
                response['xml_signed'] = docs.getXMLSignedDocument()
            else:
                response['status'] = 'FAIL'
                response['code'] = 'Sistema de Archivos'
                response['body'] = 'El documento XML no se encuentra en el servidor local'
            return response
        except Exception as e:
            exc_traceback = sys.exc_info()
            response = {}
            response['status'] = 'FAIL'
            response['code'] = 'INTERNO'
            response['body'] = getattr(e, 'message', repr(e)) + ' ON LINE ' + format(sys.exc_info()[(-1)].tb_lineno)
            return response

    def initSunatAPI(self, mode, call):
        self.fileName = self.fileName
        self.sunatAPI = SunatApi(mode, call, self.xmlPath, self.fileName)
        return self.sunatAPI

    def setXMLPath(self, xmlPath):
        self.xmlPath = xmlPath

    def validateLicence(self, data):
        response = {}
        has_licence = False
        for key in self.keys:
            if str(key).strip('\n') == data['licencia']:
                has_licence = True

        if has_licence == True:
            return True
        else:
            response['status'] = 'FAIL'
            response['code'] = 'LCC'
            response['body'] = 'La licencia del servicio es invalida'
            return response