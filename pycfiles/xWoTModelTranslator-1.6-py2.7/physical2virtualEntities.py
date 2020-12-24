# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.10-intel/egg/xwot1/physical2virtualEntities.py
# Compiled at: 2015-10-27 03:42:27
import sys, logging, logging.config, os, xml.dom.minidom, argparse, codecs
from colorama import Fore, Back, Style
from os.path import dirname, join, expanduser
if float(sys.version[:3]) < 3.0:
    import ConfigParser
else:
    import configparser as ConfigParser

class Physical2VirtualEntities:
    """
        Created on 23 sep. 2013
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
        self.__m2wConfig.read([
         join(CONFIG_DIR, 'Physical2Virtual.cfg'), expanduser('~/.Physical2Virtual.cfg'), 'Physical2Virtual.cfg'])
        self.__baseURI = self.__m2wConfig.get('Config', 'baseURI')
        self.__basePackage = self.__m2wConfig.get('Config', 'basePackage')
        self.__schemaFile = self.__m2wConfig.get('Config', 'schemaFile')
        self.__model = None
        self.__input = None
        self.__output = None
        return

    def __setupxWoT(self):
        self.__log.debug('Enter __setupxWoT')
        self.__xwot = xml.dom.minidom.Document()
        rootElement = self.__xwot.createElementNS('http://diuf.unifr.ch/softeng', 'xwot:Entity')
        rootElement.setAttribute('xmlns:xmi', 'http://www.omg.org/XMI')
        rootElement.setAttribute('xmlns:xsi', 'http://www.w3.org/2001/XMLSchema-instance')
        rootElement.setAttribute('xmlns:xwot', 'http://diuf.unifr.ch/softeng')
        rootElement.setAttribute('xmi:version', '2.0')
        self.__xwot.appendChild(rootElement)

    def __createVirtualEntities(self):
        self.__log.debug('Enter __createVirtualEntities')
        root = self.__xwot.documentElement
        ve = self.__xwot.createElement('VirtualEntity')
        physicalEntity = self.__model.getElementsByTagName('PhysicalEntity')[0]
        newPhysEnt = physicalEntity.cloneNode(False)
        root.appendChild(newPhysEnt)
        elType = physicalEntity.getAttribute('xsi:type')
        name = physicalEntity.getAttribute('name')
        ve.setAttribute('name', name + 'Resource')
        uri = raw_input('Specify URI for ' + Fore.RED + elType + ' ' + Fore.GREEN + name + Fore.RESET + ': ')
        ve.setAttribute('uri', uri)
        if elType == 'xwot:Device':
            ve.setAttribute('xsi:type', 'xwot:Resource')
            self.__log.debug(physicalEntity.attributes)
            if physicalEntity.hasAttribute('composed'):
                ve.setAttribute('composed', physicalEntity.getAttribute('composed'))
            root.appendChild(ve)
            physicalEntities = list(self.__filterChildrenByTagName(self.__model.getElementsByTagName('PhysicalEntity')[0], 'Component'))
            physicalEntities = self.__searchForContextResources(physicalEntities, newPhysEnt, ve)
            for entity in physicalEntities:
                self.__log.debug('Working on Node: ' + entity.getAttribute('name'))
                self.__addResources(newPhysEnt, entity, ve)

        elif elType == 'xwot:Sensor':
            ve.setAttribute('xsi:type', 'xwot:SensorResource')
            root.appendChild(ve)
            answer = raw_input('Has this Sensor a publisher? ' + Fore.RED + '[y/n] ' + Fore.RESET + '?')
            if answer in ('y', 'Y', 'Yes', 'yes', 'YES'):
                self.__createPublisherResource(ve)
        elif elType == 'xwot:Actuator':
            ve.setAttribute('xsi:type', 'xwot:ActuatorResource')
            root.appendChild(ve)

    def __addResources(self, targetPhysicalEntity, sourceNode, targetNode):
        self.__log.debug('Enter __addResources')
        vent = self.__xwot.createElement('Resource')
        ename = sourceNode.getAttribute('name')
        etype = sourceNode.getAttribute('xsi:type')
        vent.setAttribute('name', ename + 'Resource')
        uri = raw_input('Specify URI for ' + Fore.RED + etype + ' ' + Fore.GREEN + ename + Fore.RESET + ': ')
        vent.setAttribute('uri', uri)
        newTargetPhysicalEntity = sourceNode.cloneNode(False)
        targetPhysicalEntity.appendChild(newTargetPhysicalEntity)
        if etype == 'xwot:Device':
            vent.setAttribute('xsi:type', 'xwot:Resource')
            if sourceNode.hasAttribute('composed'):
                vent.setAttribute('composed', sourceNode.getAttribute('composed'))
            targetNode.appendChild(vent)
            subPhysicalEntities = list(self.__filterChildrenByTagName(sourceNode, 'Component'))
            subPhysicalEntities = self.__searchForContextResources(subPhysicalEntities, newTargetPhysicalEntity, vent)
            for subEntity in subPhysicalEntities:
                self.__log.debug('Working on Node: ' + subEntity.getAttribute('name'))
                self.__addResources(newTargetPhysicalEntity, subEntity, vent)

        elif etype == 'xwot:Sensor':
            vent.setAttribute('xsi:type', 'xwot:SensorResource')
            targetNode.appendChild(vent)
            answer = raw_input('Has this Sensor a publisher? ' + Fore.RED + '[y/n] ' + Fore.RESET + '?')
            if answer in ('y', 'Y', 'Yes', 'yes', 'YES'):
                self.__createPublisherResource(vent)
        elif etype == 'xwot:Actuator':
            vent.setAttribute('xsi:type', 'xwot:ActuatorResource')
            targetNode.appendChild(vent)

    @staticmethod
    def __filterChildrenByTagName(node, tagName):
        for child in node.childNodes:
            if child.nodeType == child.ELEMENT_NODE and child.tagName == tagName:
                yield child

    def __searchForContextResources(self, inputNodeList, targetPhysicalEntity, parentDestinationNode):
        self.__log.debug('Enter __searchForContextResources')
        doAskAgain = True if len(inputNodeList) > 1 else False
        while doAskAgain and len(inputNodeList) > 1:
            print 'I have found the following Nodes:'
            self.__printChildren(inputNodeList)
            answer = raw_input('Is there a ContextResource? ' + Fore.RED + '[y/n]' + Fore.RESET + '?')
            if answer not in ('y', 'Y', 'Yes', 'yes', 'YES'):
                doAskAgain = False
                continue
            if len(inputNodeList) > 2:
                numbers = raw_input('Input comma separated numbers of ContextResource: ')
                firstElement = inputNodeList[int(numbers.rsplit(',')[0])]
                secondElement = inputNodeList[int(numbers.rsplit(',')[1])]
            else:
                firstElement = inputNodeList[0]
                secondElement = inputNodeList[1]
            inputNodeList.remove(firstElement)
            inputNodeList.remove(secondElement)
            print 'Combining Node ' + firstElement.getAttribute('name') + ' and Node ' + secondElement.getAttribute('name') + ' into ContextResource'
            newTargetPhysicalEntity = firstElement.cloneNode(False)
            targetPhysicalEntity.appendChild(newTargetPhysicalEntity)
            newTargetPhysicalEntity = secondElement.cloneNode(False)
            targetPhysicalEntity.appendChild(newTargetPhysicalEntity)
            self.__createContextResource(firstElement, secondElement, parentDestinationNode)

        return inputNodeList

    def __createContextResource(self, firstElement, secondElement, parentDestinationNode):
        self.__log.debug('Enter __createContextResource')
        vent = self.__xwot.createElement('Resource')
        ename = firstElement.getAttribute('name') + secondElement.getAttribute('name')
        vent.setAttribute('name', ename + 'ContextResource')
        uri = raw_input('Specify URI for ContextResource ' + Fore.GREEN + ename + Fore.RESET + ': ')
        vent.setAttribute('uri', uri)
        vent.setAttribute('xsi:type', 'xwot:ContextResource')
        parentDestinationNode.appendChild(vent)
        answer = raw_input('Has this ContextResource a publisher? ' + Fore.RED + '[y/n] ' + Fore.RESET + '?')
        if answer in ('y', 'Y', 'Yes', 'yes', 'YES'):
            self.__createPublisherResource(vent)

    def __createPublisherResource(self, parentDestinationNode):
        self.__log.debug('Enter __createPublisherResource')
        ename = parentDestinationNode.getAttribute('name')
        publisher = self.__xwot.createElement('Resource')
        publisher.setAttribute('xsi:type', 'xwot:PublisherResource')
        publisher.setAttribute('name', ename + 'PublisherResource')
        publisher.setAttribute('uri', 'pub')
        parentDestinationNode.appendChild(publisher)

    @staticmethod
    def __printChildren(nodes):
        i = 0
        for node in nodes:
            print str(i) + ': ' + node.toxml()
            i += 1

    def simplify(self):
        self.__log.debug('Enter simplify')
        virtualEntity = self.__xwot.getElementsByTagName('VirtualEntity')[0]
        resources = self.__filterChildrenByTagName(virtualEntity, 'Resource')
        for resource in resources:
            self.__doSimplify(resource)

    def __doSimplify(self, resource):
        self.__log.debug('Enter __doSimplify')
        self.__log.debug('Working on Node: ' + resource.getAttribute('name'))
        self.__log.debug('Has ' + str(len(resource.childNodes)) + ' children')
        if len(resource.childNodes) == 1 and resource.childNodes[0].getAttribute('uri') != 'pub':
            child = resource.childNodes[0].cloneNode(True)
            parent = resource.parentNode
            self.__log.debug('Will replace node ' + resource.getAttribute('name') + ' with node ' + child.getAttribute('name'))
            parent.replaceChild(child, resource)
            self.__doSimplify(child)
        else:
            resources = self.__filterChildrenByTagName(resource, 'Resource')
            for r in resources:
                self.__doSimplify(r)

    def main(self):
        """The main function"""
        self.__log.debug('current working directory is: ' + os.getcwd())
        self.__log.debug('input File is: ' + self.__input)
        self.__log.debug('output File is: ' + self.__output)
        self.__setupxWoT()
        self.__model = xml.dom.minidom.parse(self.__input)
        self.__createVirtualEntities()
        self.simplify()
        f = codecs.open(self.__output, 'w', 'utf-8')
        self.__xwot.writexml(f, indent='', addindent='\t', newl='\n', encoding='UTF-8')

    def getArguments(self, argv):
        parser = argparse.ArgumentParser()
        parser.add_argument('-i', '--input', help='input xwot1 file containing the Model to be translated', required=True)
        parser.add_argument('-o', '--output', help='output xwot1 file containing the Model enhanced with the virtual entities', required=True)
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
    prog = Physical2VirtualEntities()
    prog.getArguments(sys.argv[1:])