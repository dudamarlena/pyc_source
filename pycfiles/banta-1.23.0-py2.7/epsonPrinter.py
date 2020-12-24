# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\banta\packages\optional\printer\epsonPrinter.py
# Compiled at: 2012-09-21 13:48:54
import string, types, logging, unicodedata
from .fiscalGeneric import PrinterInterface, PrinterException
from . import epsonFiscalDriver

class FiscalPrinterError(Exception):
    pass


class FileDriver:

    def __init__(self, filename):
        self.filename = filename
        self.file = open(filename, 'w')

    def sendCommand(self, command, parameters):
        self.file.write('Command: %d, Parameters: %s\n' % (command, parameters))
        return ['BLA', 'BLA', 'BLA', 'BLA', 'BLA', 'BLA', 'BLA', 'BLA']

    def close(self):
        self.file.close()


def formatText(text):
    asciiText = unicodedata.normalize('NFKD', unicode(text)).encode('ASCII', 'ignore')
    return asciiText


class DummyDriver:

    def __init__(self):
        self.number = int(raw_input('Ingrese el número de la última factura: '))

    def close(self):
        pass

    def sendCommand(self, commandNumber, parameters, skipStatusErrors):
        return [
         '00', '00', '', '', str(self.number), '', str(self.number)] + [str(self.number)] * 11


class EpsonPrinter(PrinterInterface):
    DEBUG = True
    CMD_OPEN_FISCAL_RECEIPT = 64
    CMD_OPEN_BILL_TICKET = 96
    CMD_PRINT_TEXT_IN_FISCAL = 65
    CMD_PRINT_LINE_ITEM = (66, 98)
    CMD_PRINT_SUBTOTAL = (67, 99)
    CMD_ADD_PAYMENT = (68, 100)
    CMD_CLOSE_FISCAL_RECEIPT = (69, 101)
    CMD_DAILY_CLOSE = 57
    CMD_STATUS_REQUEST = 42
    CMD_OPEN_DRAWER = 123
    CMD_SET_HEADER_TRAILER = 93
    CMD_OPEN_NON_FISCAL_RECEIPT = 72
    CMD_PRINT_NON_FISCAL_TEXT = 73
    CMD_CLOSE_NON_FISCAL_RECEIPT = 74
    CURRENT_DOC_TICKET = 1
    CURRENT_DOC_BILL_TICKET = 2
    CURRENT_DOC_CREDIT_TICKET = 4
    CURRENT_DOC_NON_FISCAL = 3
    MODEL_TICKET = 0
    MODEL_LX300P = 1
    MODEL_TM220AF = 2
    models = [
     'tickeadoras', 'epsonlx300+', 'tm-220-af']
    MODEL_NAMES = ('Ticketeadoras', 'LX 300+', 'TM 220 AF')
    AVAILABLE_MODELS = ('tickeadoras', 'epsonlx300+', 'tm-220-af')

    def __init__(self, deviceFile=None, speed=9600, host=None, port=None, dummy=False, model=None):
        try:
            if dummy:
                self.driver = DummyDriver()
            elif host:
                self.driver = epsonFiscalDriver.EpsonFiscalDriverProxy(host, port)
            else:
                deviceFile = deviceFile or 0
                self.driver = epsonFiscalDriver.EpsonFiscalDriver(deviceFile, speed)
        except Exception as e:
            raise FiscalPrinterError('Imposible establecer comunicación.', e)

        if not model:
            self.model = 'tickeadoras'
        else:
            self.model = self.AVAILABLE_MODELS[model]
        self._currentDocument = None
        self._currentDocumentType = None
        return

    def _sendCommand(self, commandNumber, parameters, skipStatusErrors=False):
        print '_sendCommand', commandNumber, parameters
        try:
            logging.getLogger().info('sendCommand: SEND|0x%x|%s|%s' % (commandNumber,
             skipStatusErrors and 'T' or 'F',
             str(parameters)))
            return self.driver.sendCommand(commandNumber, parameters, skipStatusErrors)
        except epsonFiscalDriver.PrinterException as e:
            logging.getLogger().error('epsonFiscalDriver.PrinterException: %s' % str(e))
            raise PrinterException('Error de la impresora fiscal: ' + str(e))

    def openNonFiscalReceipt(self):
        status = self._sendCommand(self.CMD_OPEN_NON_FISCAL_RECEIPT, [])
        self._currentDocument = self.CURRENT_DOC_NON_FISCAL
        self._currentDocumentType = None
        return status

    def printNonFiscalText(self, text):
        return self._sendCommand(self.CMD_PRINT_NON_FISCAL_TEXT, [formatText(text[:40])])

    ivaTypeMap = {PrinterInterface.IVA_TYPE_RESPONSABLE_INSCRIPTO: 'I', 
       PrinterInterface.IVA_TYPE_RESPONSABLE_NO_INSCRIPTO: 'R', 
       PrinterInterface.IVA_TYPE_EXENTO: 'E', 
       PrinterInterface.IVA_TYPE_NO_RESPONSABLE: 'N', 
       PrinterInterface.IVA_TYPE_CONSUMIDOR_FINAL: 'F', 
       PrinterInterface.IVA_TYPE_RESPONSABLE_NO_INSCRIPTO_BIENES_DE_USO: 'R', 
       PrinterInterface.IVA_TYPE_RESPONSABLE_MONOTRIBUTO: 'M', 
       PrinterInterface.IVA_TYPE_MONOTRIBUTISTA_SOCIAL: 'M', 
       PrinterInterface.IVA_TYPE_PEQUENIO_CONTRIBUYENTE_EVENTUAL: 'F', 
       PrinterInterface.IVA_TYPE_PEQUENIO_CONTRIBUYENTE_EVENTUAL_SOCIAL: 'F', 
       PrinterInterface.IVA_TYPE_NO_CATEGORIZADO: 'F'}
    ADDRESS_SIZE = 30

    def _setHeaderTrailer(self, line, text):
        self._sendCommand(self.CMD_SET_HEADER_TRAILER, (str(line), text))

    def setHeader(self, header=None):
        """Establecer encabezados"""
        if not header:
            header = []
        line = 3
        for text in (header + [chr(127)] * 3)[:3]:
            self._setHeaderTrailer(line, text)
            line += 1

    def setTrailer(self, trailer=None):
        """Establecer pie"""
        if not trailer:
            trailer = []
        line = 11
        for text in (trailer + [chr(127)] * 9)[:9]:
            self._setHeaderTrailer(line, text)
            line += 1

    def openBillCreditTicket(self, type, name, address, doc, docType, ivaType, reference='NC'):
        return self._openBillCreditTicket(type, name, address, doc, docType, ivaType, isCreditNote=True)

    def openBillTicket(self, type, name, address, doc, docType, ivaType):
        return self._openBillCreditTicket(type, name, address, doc, docType, ivaType, isCreditNote=False)

    def _openBillCreditTicket(self, type, name, address, doc, docType, ivaType, isCreditNote, reference=None):
        if not doc or filter(lambda x: x not in string.digits + '-.', doc or '') or docType not in self.docTypeNames:
            doc, docType = ('', '')
        else:
            doc = doc.replace('-', '').replace('.', '')
            docType = self.docTypeNames[docType]
        self._type = type
        if self.model == 'epsonlx300+':
            parameters = [
             isCreditNote and 'N' or 'F',
             'C',
             type,
             '1',
             'P',
             '17',
             'I',
             self.ivaTypeMap.get(ivaType, 'F'),
             formatText(name[:40]),
             formatText(name[40:80]),
             formatText(docType) or isCreditNote and '-' or '',
             doc or isCreditNote and '-' or '',
             'N',
             formatText(address[:self.ADDRESS_SIZE] or '-'),
             formatText(address[self.ADDRESS_SIZE:self.ADDRESS_SIZE * 2]),
             formatText(address[self.ADDRESS_SIZE * 2:self.ADDRESS_SIZE * 3]),
             (isCreditNote or self.ivaTypeMap.get(ivaType, 'F') != 'F') and '-' or '',
             '',
             'C']
        else:
            parameters = [
             isCreditNote and 'M' or 'T',
             'C',
             type,
             '1',
             'P',
             '17',
             'E',
             self.ivaTypeMap.get(ivaType, 'F'),
             formatText(name[:40]),
             formatText(name[40:80]),
             formatText(docType) or isCreditNote and '-' or '',
             doc or isCreditNote and '-' or '',
             'N',
             formatText(address[:self.ADDRESS_SIZE] or '-'),
             formatText(address[self.ADDRESS_SIZE:self.ADDRESS_SIZE * 2]),
             formatText(address[self.ADDRESS_SIZE * 2:self.ADDRESS_SIZE * 3]),
             (isCreditNote or self.ivaTypeMap.get(ivaType, 'F') != 'F') and '-' or '',
             '',
             'C']
        if isCreditNote:
            self._currentDocument = self.CURRENT_DOC_CREDIT_TICKET
        else:
            self._currentDocument = self.CURRENT_DOC_BILL_TICKET
        self._currentDocumentType = type
        return self._sendCommand(self.CMD_OPEN_BILL_TICKET, parameters)

    def _getCommandIndex(self):
        if self._currentDocument == self.CURRENT_DOC_TICKET:
            return 0
        if self._currentDocument in (self.CURRENT_DOC_BILL_TICKET, self.CURRENT_DOC_CREDIT_TICKET):
            return 1
        if self._currentDocument == self.CURRENT_DOC_NON_FISCAL:
            return 2
        raise 'Invalid currentDocument'

    def openTicket(self):
        if self.model == 'epsonlx300+':
            return self.openBillTicket('B', 'CONSUMIDOR FINAL', '', None, None, self.IVA_TYPE_CONSUMIDOR_FINAL)
        else:
            self._sendCommand(self.CMD_OPEN_FISCAL_RECEIPT, ['C'])
            self._currentDocument = self.CURRENT_DOC_TICKET
            return

    def openDrawer(self):
        self._sendCommand(self.CMD_OPEN_DRAWER, [])

    def closeDocument(self):
        if self._currentDocument == self.CURRENT_DOC_TICKET:
            reply = self._sendCommand(self.CMD_CLOSE_FISCAL_RECEIPT[self._getCommandIndex()], ['T'])
            return reply[2]
        if self._currentDocument == self.CURRENT_DOC_BILL_TICKET:
            reply = self._sendCommand(self.CMD_CLOSE_FISCAL_RECEIPT[self._getCommandIndex()], [
             self.model == 'epsonlx300+' and 'F' or 'T', self._type, 'FINAL'])
            del self._type
            return reply[2]
        if self._currentDocument == self.CURRENT_DOC_CREDIT_TICKET:
            reply = self._sendCommand(self.CMD_CLOSE_FISCAL_RECEIPT[self._getCommandIndex()], [
             self.model == 'epsonlx300+' and 'N' or 'M', self._type, 'FINAL'])
            del self._type
            return reply[2]
        if self._currentDocument in (self.CURRENT_DOC_NON_FISCAL,):
            return self._sendCommand(self.CMD_CLOSE_NON_FISCAL_RECEIPT, ['T'])
        raise NotImplementedError

    def cancelDocument(self):
        if self._currentDocument in (self.CURRENT_DOC_TICKET, self.CURRENT_DOC_BILL_TICKET,
         self.CURRENT_DOC_CREDIT_TICKET):
            status = self._sendCommand(self.CMD_ADD_PAYMENT[self._getCommandIndex()], ['Cancelar', '0', 'C'])
            return status
        if self._currentDocument in (self.CURRENT_DOC_NON_FISCAL,):
            self.printNonFiscalText('CANCELADO')
            return self.closeDocument()
        raise NotImplementedError

    def addItem(self, description, quantity, price, iva, discount=0.0, discountDescription=None, negative=False):
        if type(description) in types.StringTypes:
            description = [
             description]
        if negative:
            sign = 'R'
        else:
            sign = 'M'
        quantityStr = str(int(quantity * 1000))
        bultosStr = str(int(quantity))
        if self._currentDocumentType != 'A':
            priceUnitStr = str(int(round(price * 100, 0)))
        elif self.model == 'tm-220-af':
            priceUnitStr = '%0.4f' % (price / ((100.0 + iva) / 100.0))
        else:
            priceUnitStr = str(int(round(price / ((100 + iva) / 100) * 100, 0)))
        ivaStr = str(int(iva * 100))
        extraparams = self._currentDocument in (self.CURRENT_DOC_BILL_TICKET,
         self.CURRENT_DOC_CREDIT_TICKET) and ['', '', ''] or []
        if self._getCommandIndex() == 0:
            for d in description[:-1]:
                self._sendCommand(self.CMD_PRINT_TEXT_IN_FISCAL, [
                 formatText(d)[:20]])

        reply = self._sendCommand(self.CMD_PRINT_LINE_ITEM[self._getCommandIndex()], [
         formatText(description[(-1)][:20]),
         quantityStr, priceUnitStr, ivaStr, sign, bultosStr, '0'] + extraparams)
        if discount:
            discountStr = str(int(discount * 100))
            self._sendCommand(self.CMD_PRINT_LINE_ITEM[self._getCommandIndex()], [
             formatText(discountDescription[:20]), '1000',
             discountStr, ivaStr, 'R', '0', '0'] + extraparams)
        return reply

    def addPayment(self, description, payment):
        paymentStr = str(int(payment * 100))
        status = self._sendCommand(self.CMD_ADD_PAYMENT[self._getCommandIndex()], [
         formatText(description)[:20], paymentStr, 'T'])
        return status

    def addAdditional(self, description, amount, iva, negative=False):
        u"""Agrega un adicional a la FC.
                                                @param description      Descripción
                                                @param amount                    Importe (sin iva en FC A, sino con IVA)
                                                @param iva                                      Porcentaje de Iva
                                                @param negative True->Descuento, False->Recargo"""
        if negative:
            sign = 'R'
        else:
            sign = 'M'
        quantityStr = '1000'
        bultosStr = '0'
        priceUnit = amount
        if self._currentDocumentType != 'A':
            priceUnitStr = str(int(round(priceUnit * 100, 0)))
        else:
            priceUnitStr = str(int(round(priceUnit / ((100 + iva) / 100) * 100, 0)))
        ivaStr = str(int(iva * 100))
        extraparams = self._currentDocument in (self.CURRENT_DOC_BILL_TICKET,
         self.CURRENT_DOC_CREDIT_TICKET) and ['', '', ''] or []
        reply = self._sendCommand(self.CMD_PRINT_LINE_ITEM[self._getCommandIndex()], [
         formatText(description[:20]),
         quantityStr, priceUnitStr, ivaStr, sign, bultosStr, '0'] + extraparams)
        return reply

    def dailyClose(self, type):
        reply = self._sendCommand(self.CMD_DAILY_CLOSE, [type, 'P'])
        return reply[2:]

    def getLastNumber(self, letter):
        reply = self._sendCommand(self.CMD_STATUS_REQUEST, ['A'], True)
        if len(reply) < 3:
            reply = self._sendCommand(self.CMD_STATUS_REQUEST, ['A'], False)
        if letter == 'A':
            return int(reply[6])
        else:
            return int(reply[4])

    def getLastCreditNoteNumber(self, letter):
        reply = self._sendCommand(self.CMD_STATUS_REQUEST, ['A'], True)
        if len(reply) < 3:
            reply = self._sendCommand(self.CMD_STATUS_REQUEST, ['A'], False)
        if letter == 'A':
            return int(reply[10])
        else:
            return int(reply[11])

    def cancelAnyDocument(self):
        try:
            self._sendCommand(self.CMD_ADD_PAYMENT[0], ['Cancelar', '0', 'C'])
            return True
        except:
            pass

        try:
            self._sendCommand(self.CMD_ADD_PAYMENT[1], ['Cancelar', '0', 'C'])
            return True
        except:
            pass

        try:
            self._sendCommand(self.CMD_CLOSE_NON_FISCAL_RECEIPT, ['T'])
            return True
        except:
            pass

        return False

    def getWarnings(self):
        ret = []
        reply = self._sendCommand(self.CMD_STATUS_REQUEST, ['N'], True)
        printerStatus = reply[0]
        x = int(printerStatus, 16)
        if 16 & x == 16:
            ret.append(['Poco papel para la cinta de auditoría'])
        if 32 & x == 32:
            ret.append(['Poco papel para comprobantes o tickets'])
        return ret

    def __del__(self):
        try:
            self.close()
        except:
            pass

    def close(self):
        self.driver.close()
        self.driver = None
        return