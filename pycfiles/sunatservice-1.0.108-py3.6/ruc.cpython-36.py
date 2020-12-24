# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/sunatservice/ruc.py
# Compiled at: 2020-01-27 19:26:57
# Size of source mod 2**32: 10142 bytes
import requests
from bs4 import BeautifulSoup
from PIL import Image
import pytesseract, os, re, json, sys

class Ruc:
    endPoint = 'http://e-consultaruc.sunat.gob.pe/cl-ti-itmrconsruc/'
    endPoint_essalud = 'https://ww1.essalud.gob.pe/sisep/postulante/postulante/postulante_obtenerDatosPostulante.htm?strDni='
    URL_CONSULT = 'http://e-consultaruc.sunat.gob.pe/cl-ti-itmrconsruc/jcrS03Alias'
    URL_RANDOM = 'http://e-consultaruc.sunat.gob.pe/cl-ti-itmrconsruc/captcha?accion=random'
    maxTries = 3
    maxTried = 1
    xmlPath = ''

    def consultDNI_essalud(self, numero_doc):
        url = self.endPoint_essalud + str(numero_doc)
        res = {'error':True,  'message':None,  'data':{}}
        try:
            response = requests.get(url)
        except requests.exceptions.ConnectionError as e:
            res['message'] = 'Error en la conexion'
            return res

        try:
            response = response.json()
            person = response['DatosPerson'][0]
            if str(person['Nombres']) != '':
                res['error'] = False
                res['data']['nombres'] = person['Nombres']
                res['data']['ape_paterno'] = person['ApellidoPaterno']
                res['data']['ape_materno'] = person['ApellidoMaterno']
                res['data']['fecha_nacimiento'] = person['FechaNacimiento']
                res['data']['sexo'] = person['Sexo']
            else:
                try:
                    res['message'] = str('No encontrado.')
                except Exception as e:
                    res['error'] = True

            res['url'] = url
            return res
        except Exception as e:
            exc_traceback = sys.exc_info()
            res['error'] = True
            return res

        return res

    def consultRUC_Pydevs(self, tipo_doc, numero_doc, format='json'):
        url = 'http://py-devs.com/api'
        type_doc = '/ruc'
        if int(tipo_doc) == 1:
            type_doc = '/dni'
        else:
            url = str(url) + str(type_doc) + str('/') + str(numero_doc) + str('/?format=json')
            res = {'error':True,  'message':None,  'data':{}}
            try:
                response = requests.get(url)
            except requests.exceptions.ConnectionError as e:
                res['message'] = 'Error en la conexion'
                return res

            if response.status_code == 200:
                res['error'] = False
                res['data'] = response.json()
                res['data']['actividad_economica'] = str('')
            else:
                try:
                    res['message'] = response.json()['detail']
                except Exception as e:
                    res['error'] = True

        res['url'] = url
        return res

    def consultRUC(self, ruc):
        res = {'error':False, 
         'message':None,  'data':{}}
        try:
            raiz = str('http://e-consultaruc.sunat.gob.pe/cl-ti-itmrconsruc/')
            sesion = requests.session()
            sesion.get(raiz + 'jcrS00Alias')
            pantalla_principal = sesion.get(raiz + 'frameCriterioBusqueda.jsp')
            soup = BeautifulSoup(pantalla_principal.content, 'html.parser')
            ruta_captcha = raiz + soup.find('img').attrs['src']
            imagen = sesion.get(ruta_captcha)
            with os.fdopen(os.open(self.xmlPath + '/imagen.jpg', os.O_WRONLY | os.O_CREAT, 777), 'wb') as (captcha):
                captcha.write(imagen.content)
            captcha = pytesseract.image_to_string(Image.open(self.xmlPath + '/imagen.jpg'))
            formdata = {'accion':'consPorRuc', 
             'razSoc':'', 
             'nroRuc':ruc, 
             'nrodoc':'', 
             'contexto':'ti - it', 
             'search1':ruc, 
             'codigo':captcha, 
             'tQuery':'on', 
             'tipdoc':'1', 
             'search2':'', 
             'coddpto':'', 
             'codprov':'', 
             'coddist':'', 
             'search3':''}
            resultado = sesion.post((raiz + 'jcrS00Alias'), data=formdata, verify=False)
            resultado = BeautifulSoup(resultado.content, 'html.parser')
            response = {}
            resultado = [td.text.strip() for td in resultado.find('table', attrs={'cellpadding': 2}).find_all('td')]
            itmp = 0
            for posicion, celda in enumerate(resultado):
                if posicion == 1:
                    fullName = celda.strip()
                    fullNameParts = fullName.split('-')
                    companyName = str(fullNameParts[1]).strip()
                    response['name'] = companyName
                else:
                    if posicion == 3:
                        tipoContribuyente = celda.strip()
                        response['tipo_contribuyente'] = tipoContribuyente
                    else:
                        if posicion == 5:
                            nombreComercial = celda.strip()
                            response['nombre_comercial'] = nombreComercial
                        else:
                            if posicion == 18:
                                sistemaEmisionComprobante = celda.strip()
                                response['sistema_emision_comprobante'] = sistemaEmisionComprobante
                            else:
                                if posicion == 22:
                                    sistemaEmisionComprobante = celda.strip()
                                    response['sistema_contabilidad'] = sistemaEmisionComprobante
                                if posicion == 11:
                                    estado_contribuyente = celda.strip()
                                    response['estado_contribuyente'] = estado_contribuyente
                            if posicion == 14:
                                condicion_contribuyente = celda.strip()
                                response['condicion_contribuyente'] = condicion_contribuyente
                        if posicion == 16:
                            fullAddress = celda.strip()
                            fullAddressParts = fullAddress.split('-')
                            adreess = []
                            for record in fullAddressParts:
                                adreess.append(record.strip())

                            district = adreess[(len(adreess) - 1)]
                            province = adreess[(len(adreess) - 2)]
                            response['address'] = str(' ').join(adreess)
                            response['province'] = province
                            response['district'] = district
                            adreessParts = adreess[0].split(' ')
                            response['department'] = adreessParts[(len(adreessParts) - 1)]
                    if posicion == 24:
                        activities = list()
                        actividadEconomica = celda.strip()
                        response['actividad_economica'] = actividadEconomica
                itmp = itmp + 1

        except Exception as e:
            res['error'] = True
            return res

        if len(response['name']) > 0:
            res['error'] = False
            res['data']['ruc'] = ruc
            res['data']['tipo_contribuyente'] = response['tipo_contribuyente']
            res['data']['nombre_comercial'] = response['nombre_comercial']
            res['data']['nombre'] = response['name']
            res['data']['domicilio_fiscal'] = response['address']
            res['data']['departamento'] = self.getDepartment(response['department'])
            res['data']['provincia'] = response['province']
            res['data']['distrito'] = response['district']
            res['data']['sistema_emision_comprobante'] = response['sistema_emision_comprobante']
            res['data']['sistema_contabilidad'] = response['sistema_contabilidad']
            res['data']['estado_contribuyente'] = response['estado_contribuyente']
            res['data']['condicion_contribuyente'] = response['condicion_contribuyente']
            res['data']['actividad_economica'] = response['actividad_economica']
        return res

    def setXMLPath(self, xmlPath):
        self.xmlPath = xmlPath

    def getDepartment(self, department):
        if str(department) == str('DIOS'):
            department = str('MADRE DE DIOS')
        else:
            if str(department) == str('MARTIN'):
                department = str('SAN MARTIN')
            if str(department) == str('LIBERTAD'):
                department = str('LA LIBERTAD')
            if str(department) == str('111)  LIMA'):
                department = str('LIMA')
        return department