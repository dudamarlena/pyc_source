# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.10-intel/egg/xwot1/model2WADL.py
# Compiled at: 2015-10-27 03:38:54
import logging, logging.config, sys, xml.dom.minidom, argparse, codecs
from os.path import dirname, join, expanduser
if float(sys.version[:3]) < 3.0:
    import ConfigParser
else:
    import configparser as ConfigParser

class Model2WADL():
    """
        Created on 18 apr. 2013
        @author: ruppena
    """

    def __init__(self):
        """Do some initialization stuff"""
        INSTALL_DIR = dirname(__file__)
        CONFIG_DIR = '/etc/Model2WADL/'
        logging.basicConfig(level=logging.ERROR)
        logging.config.fileConfig([join(CONFIG_DIR, 'logging.conf'), expanduser('~/.logging.conf'), 'logging.conf'])
        self.__log = logging.getLogger('thesis')
        self.__log.debug('Reading general configuration from Model2WADL.cfg')
        self.__m2wConfig = ConfigParser.SafeConfigParser()
        self.__m2wConfig.read([join(CONFIG_DIR, 'Model2WADL.cfg'), expanduser('~/.Model2WADL.cfg'), 'Model2WADL.cfg'])
        self.__baseURI = self.__m2wConfig.get('Config', 'baseURI')
        self.__basePackage = self.__m2wConfig.get('Config', 'basePackage')
        self.__schemaFile = self.__m2wConfig.get('Config', 'schemaFile')
        self.__wadl = None
        self.__model = None
        self.__input = None
        self.__output = None
        return

    def createXSD(self):
        xsd = xml.dom.minidom.Document()
        rootElement = xsd.createElementNS('http://softeng.unifr.ch/REST/generator/', 'xs:schema')
        rootElement.setAttribute('xmlns:xs', 'http://www.w3.org/2001/XMLSchema')
        rootElement.setAttribute('elementFormDefault', 'qualified')
        rootElement.setAttribute('xmlns:jaxb', 'http://java.sun.com/xml/ns/jaxb')
        rootElement.setAttribute('jaxb:version', '2.0')
        rootElement.setAttribute('targetNamespace', 'http://softeng.unifr.ch/REST/generator/')
        xsd.appendChild(rootElement)
        annotationElement = xsd.createElement('xs:annotation')
        rootElement.appendChild(annotationElement)
        appinfoElement = xsd.createElement('xs:appinfo')
        annotationElement.appendChild(appinfoElement)
        globalBindingsElement = xsd.createElement('jaxb:globalBindings')
        appinfoElement.appendChild(globalBindingsElement)
        javaTypeElement = xsd.createElement('jaxb:javaType')
        javaTypeElement.setAttribute('name', 'java.net.URI')
        javaTypeElement.setAttribute('xmlType', 'xs:anyURI')
        javaTypeElement.setAttribute('parseMethod', 'create')
        javaTypeElement.setAttribute('printMethod', 'toASCIIString')
        globalBindingsElement.appendChild(javaTypeElement)
        javaTypeElement = xsd.createElement('jaxb:javaType')
        javaTypeElement.setAttribute('name', 'java.util.Calendar')
        javaTypeElement.setAttribute('xmlType', 'xs:dateTime')
        javaTypeElement.setAttribute('parseMethod', 'javax.xml.bind.DatatypeConverter.parseDateTime')
        javaTypeElement.setAttribute('printMethod', 'javax.xml.bind.DatatypeConverter.printDateTime')
        globalBindingsElement.appendChild(javaTypeElement)
        f = codecs.open(self.__schemaFile, 'w', 'utf-8')
        xsd.writexml(f, indent='', addindent='\t', newl='\n', encoding='UTF-8')

    def createWADL(self):
        self.__wadl = xml.dom.minidom.Document()
        rootElement = self.__wadl.createElementNS('http://wadl.dev.java.net/2009/02', 'application')
        rootElement.setAttribute('xmlns', 'http://wadl.dev.java.net/2009/02')
        rootElement.setAttribute('xmlns:xsi', 'http://www.w3.org/2001/XMLSchema-instance')
        rootElement.setAttribute('xsi:schemaLocation', 'http://wadl.dev.java.net/2009/02 http://www.w3.org/Submission/wadl/wadl.xsd')
        rootElement.setAttribute('xmlns:ns', 'http://softeng.unifr.ch/REST/generator/')
        self.__wadl.appendChild(rootElement)
        grammar = self.__wadl.createElement('grammars')
        rootElement.appendChild(grammar)
        include = self.__wadl.createElement('include')
        include.setAttribute('href', self.__schemaFile)
        grammar.appendChild(include)
        resources = self.__wadl.createElement('resources')
        resources.setAttribute('base', self.__baseURI)
        rootElement.appendChild(resources)
        ve = self.__model.getElementsByTagName('VirtualEntity')[0]
        resourcePath = '/' + ve.getAttribute('uri')
        resourceEl = self.__wadl.createElement('resource')
        resourceEl.setAttribute('path', resourcePath)
        resourceEl.setAttribute('id', self.__basePackage + ve.getAttribute('name'))
        resources.appendChild(resourceEl)
        self.addMethods(ve, resourceEl)
        self.addResources(ve, resources, resourcePath)
        self.__log.debug(self.__wadl.toprettyxml())
        f = codecs.open(self.__output, 'w', 'utf-8')
        self.__wadl.writexml(f, indent='', addindent='\t', newl='\n', encoding='UTF-8')

    def addResources(self, source, target, path):
        for resource in self.getResourceNodes(source):
            resourceEl = self.__wadl.createElement('resource')
            resourcePath = path + '/' + resource.getAttribute('uri')
            resourceEl.setAttribute('path', resourcePath)
            resourceEl.setAttribute('id', self.__basePackage + resource.getAttribute('name'))
            self.addMethods(resource, resourceEl)
            target.appendChild(resourceEl)
            self.addResources(resource, target, resourcePath)

    def addMethods(self, node, destinationElement):
        ve_type = node.getAttribute('xsi:type')
        if ve_type == 'xwot:ContextResource':
            self.createGETMethod(node, destinationElement)
            self.createPUTMethod(node, destinationElement)
        elif ve_type == 'xwot:SensorResource':
            self.createGETMethod(node, destinationElement)
        elif ve_type == 'xwot:ActuatorResource':
            self.createPUTMethod(node, destinationElement)
        elif ve_type == 'xwot:ServiceResource':
            self.createGETMethod(node, destinationElement)
            self.createPUTMethod(node, destinationElement)
            self.createPOSTMethod(node, destinationElement)
            self.createDELETEMethod(node, destinationElement)
        else:
            self.createGETMethod(node, destinationElement)
            self.createPOSTMethod(node, destinationElement)

    def addMethods2(self, SourceResource, TargetResource):
        """Adds the methods"""
        methods = SourceResource.getElementsByTagName('Method')
        if len(methods) == 0:
            self.createGETMethod(SourceResource, TargetResource)
            self.createPOSTMethod(SourceResource, TargetResource)
            self.createPUTMethod(SourceResource, TargetResource)
            self.createDELETEMethod(SourceResource, TargetResource)
        for method in methods:
            methodEl = self.__wadl.createElement('method')
            methodEl.setAttribute('id', method.getAttribute('name'))
            methodEl.setAttribute('name', method.getAttribute('method'))
            TargetResource.appendChild(methodEl)

    def createGETMethod(self, parentResource, targetResource):
        methodEl = self.__wadl.createElement('method')
        methodEl.setAttribute('id', 'get' + parentResource.getAttribute('name') + 'XML')
        methodEl.setAttribute('name', 'GET')
        targetResource.appendChild(methodEl)
        responseEL = self.__wadl.createElement('response')
        methodEl.appendChild(responseEL)
        represenationEl = self.__wadl.createElement('representation')
        represenationEl.setAttribute('mediaType', 'application/xml')
        responseEL.appendChild(represenationEl)
        represenationEl = self.__wadl.createElement('representation')
        represenationEl.setAttribute('mediaType', 'application/json')
        responseEL.appendChild(represenationEl)
        represenationEl = self.__wadl.createElement('representation')
        represenationEl.setAttribute('mediaType', 'text/xml')
        responseEL.appendChild(represenationEl)
        methodEl = self.__wadl.createElement('method')
        methodEl.setAttribute('id', 'get' + parentResource.getAttribute('name') + 'HTML')
        methodEl.setAttribute('name', 'GET')
        targetResource.appendChild(methodEl)
        responseEL = self.__wadl.createElement('response')
        methodEl.appendChild(responseEL)
        represenationEl = self.__wadl.createElement('representation')
        represenationEl.setAttribute('mediaType', 'text/html')
        responseEL.appendChild(represenationEl)

    def createPOSTMethod(self, parentResource, targetResource):
        methodEl = self.__wadl.createElement('method')
        methodEl.setAttribute('id', 'post' + parentResource.getAttribute('name') + 'XML')
        methodEl.setAttribute('name', 'POST')
        targetResource.appendChild(methodEl)
        responseEL = self.__wadl.createElement('response')
        methodEl.appendChild(responseEL)
        represenationEl = self.__wadl.createElement('representation')
        represenationEl.setAttribute('mediaType', 'application/xml')
        responseEL.appendChild(represenationEl)
        represenationEl = self.__wadl.createElement('representation')
        represenationEl.setAttribute('mediaType', 'application/json')
        responseEL.appendChild(represenationEl)
        represenationEl = self.__wadl.createElement('representation')
        represenationEl.setAttribute('mediaType', 'text/xml')
        responseEL.appendChild(represenationEl)

    def createPUTMethod(self, parentResource, targetResource):
        methodEl = self.__wadl.createElement('method')
        methodEl.setAttribute('id', 'put' + parentResource.getAttribute('name') + 'XML')
        methodEl.setAttribute('name', 'PUT')
        targetResource.appendChild(methodEl)
        responseEL = self.__wadl.createElement('response')
        methodEl.appendChild(responseEL)
        represenationEl = self.__wadl.createElement('representation')
        represenationEl.setAttribute('mediaType', 'application/xml')
        responseEL.appendChild(represenationEl)
        represenationEl = self.__wadl.createElement('representation')
        represenationEl.setAttribute('mediaType', 'application/json')
        responseEL.appendChild(represenationEl)
        represenationEl = self.__wadl.createElement('representation')
        represenationEl.setAttribute('mediaType', 'text/xml')
        responseEL.appendChild(represenationEl)

    def createDELETEMethod(self, parentResource, targetResource):
        methodEl = self.__wadl.createElement('method')
        methodEl.setAttribute('id', 'post' + parentResource.getAttribute('name') + 'XML')
        methodEl.setAttribute('name', 'DELETE')
        targetResource.appendChild(methodEl)
        responseEL = self.__wadl.createElement('response')
        methodEl.appendChild(responseEL)
        represenationEl = self.__wadl.createElement('representation')
        represenationEl.setAttribute('mediaType', 'application/xml')
        responseEL.appendChild(represenationEl)
        represenationEl = self.__wadl.createElement('representation')
        represenationEl.setAttribute('mediaType', 'application/json')
        responseEL.appendChild(represenationEl)
        represenationEl = self.__wadl.createElement('representation')
        represenationEl.setAttribute('mediaType', 'text/xml')
        responseEL.appendChild(represenationEl)

    @staticmethod
    def getResourceNodes(parent):
        resources = []
        for child in parent.childNodes:
            if child.localName == 'Resource':
                resources.append(child)

        return resources

    def main(self):
        """The main function"""
        self.__log.debug('input File is: ' + self.__input)
        self.__log.debug('output File is: ' + self.__output)
        self.__model = xml.dom.minidom.parse(self.__input)
        self.createWADL()
        self.createXSD()

    def getArguments(self, argv):
        parser = argparse.ArgumentParser()
        parser.add_argument('-i', '--input', help='input XMI file containing the Model to be translated', required=True)
        parser.add_argument('-o', '--output', help='destination WADL file', required=True)
        args = parser.parse_args(argv)
        self.__input = args.input
        self.__output = args.output
        try:
            self.__log.info('Start processing')
            self.main()
            self.__log.info('Successfully created the necessary service(s)')
        except Exception as err:
            self.__log.error('Something went really wrong')
            self.__log.debug(err)


if __name__ == '__main__':
    prog = Model2WADL()
    prog.getArguments(sys.argv[1:])