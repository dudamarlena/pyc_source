# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/byt3bl33d3r/.virtualenvs/CME_old/lib/python2.7/site-packages/cme/enum/wmiquery.py
# Compiled at: 2016-12-29 01:49:52
import logging, traceback
from impacket.dcerpc.v5.dtypes import NULL
from impacket.dcerpc.v5.dcom import wmi
from impacket.dcerpc.v5.dcomrt import DCOMConnection

class WMIQUERY:

    def __init__(self, connection):
        self.__logger = connection.logger
        self.__addr = connection.host
        self.__username = connection.username
        self.__password = connection.password
        self.__hash = connection.hash
        self.__domain = connection.domain
        self.__namespace = connection.args.wmi_namespace
        self.__query = connection.args.wmi
        self.__iWbemServices = None
        self.__doKerberos = False
        self.__aesKey = None
        self.__oxidResolver = True
        self.__lmhash = ''
        self.__nthash = ''
        if self.__hash is not None:
            self.__lmhash, self.__nthash = self.__hash.split(':')
        if self.__password is None:
            self.__password = ''
        self.__dcom = DCOMConnection(self.__addr, self.__username, self.__password, self.__domain, self.__lmhash, self.__nthash, self.__aesKey, self.__oxidResolver, self.__doKerberos)
        try:
            iInterface = self.__dcom.CoCreateInstanceEx(wmi.CLSID_WbemLevel1Login, wmi.IID_IWbemLevel1Login)
            iWbemLevel1Login = wmi.IWbemLevel1Login(iInterface)
            self.__iWbemServices = iWbemLevel1Login.NTLMLogin(self.__namespace, NULL, NULL)
            iWbemLevel1Login.RemRelease()
        except Exception as e:
            self.__logger.error(e)

        return

    def query(self):
        query = self.__query.strip('\n')
        if query[-1:] == ';':
            query = query[:-1]
        if self.__iWbemServices:
            iEnumWbemClassObject = self.__iWbemServices.ExecQuery(query.strip('\n'))
            self.__logger.success('Executed specified WMI query')
            self.printReply(iEnumWbemClassObject)
            iEnumWbemClassObject.RemRelease()
            self.__iWbemServices.RemRelease()
            self.__dcom.disconnect()

    def describe(self, sClass):
        sClass = sClass.strip('\n')
        if sClass[-1:] == ';':
            sClass = sClass[:-1]
        try:
            iObject, _ = self.iWbemServices.GetObject(sClass)
            iObject.printInformation()
            iObject.RemRelease()
        except Exception as e:
            traceback.print_exc()

    def printReply(self, iEnum):
        printHeader = True
        while True:
            try:
                pEnum = iEnum.Next(4294967295, 1)[0]
                record = pEnum.getProperties()
                line = []
                for rec in record:
                    line.append(('{}: {}').format(rec, record[rec]['value']))

                self.__logger.highlight((' | ').join(line))
            except Exception as e:
                if str(e).find('S_FALSE') < 0:
                    raise
                else:
                    break

        iEnum.RemRelease()