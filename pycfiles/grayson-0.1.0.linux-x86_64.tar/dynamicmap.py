# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/scox/dev/grayson/venv/lib/python2.7/site-packages/grayson/compiler/dynamicmap.py
# Compiled at: 2012-07-20 09:24:44
import os, shutil, tarfile, logging, json
from string import Template
from grayson.common.util import GraysonUtil
from grayson.compiler.compiler import Operator
from grayson.compiler.compiler import GraysonCompiler
logger = logging.getLogger(__name__)

class DynamicMapOperator(Operator):
    DYNAMIC_INDEX = 'dynIndex'

    def __init__(self):
        logger.debug('dynamic-map: init()')
        self.version = '1.0'
        self.header = "<?xml version='1.0' encoding='UTF-8'?>\n<!-- generator: grayson -->\n<adag xmlns='http://pegasus.isi.edu/schema/DAX'\n      xmlns:xsi='http://www.w3.org/2001/XMLSchema-instance'\n      xsi:schemaLocation='http://pegasus.isi.edu/schema/DAX http://pegasus.isi.edu/schema/dax-3.2.xsd'\n      version='3.2'\n      name='$namespace'>"
        self.footer = '\n</adag>'
        self.subdax = "\n   <dax id='${namespace}gid${c}' file='${outputname}' >\n      <argument>${instanceArgs} --verbose --verbose --verbose --force --sites ${sites}</argument>\n   </dax>"
        self.subdax = "\n   <dax id='${namespace}gid${c}' file='${outputname}' >\n      <argument>${instanceArgs} --verbose --verbose --verbose --force ${sites}</argument>\n   </dax>"

    def validate(self, context):
        return context

    def execute(self, context={}):
        operatorContext = context['operator']
        method = operatorContext['method']
        inputFile = operatorContext['input']
        variable = operatorContext['variable']
        index = operatorContext['index']
        flow = operatorContext['flow']
        version = operatorContext['version']
        instanceArgs = operatorContext['instanceArgs']
        outputBasename = context['outputName']
        modelPath = context['modelPath']
        outputDir = context['outputDir']
        contextModels = context['contextModels']
        sites = context['sites']
        appHome = context['appHome']
        graysonHome = context['graysonHome']
        tmpOutputDir = os.path.join(outputDir, 'tmp')
        contextModels = contextModels.split(os.pathsep)
        models = [flow]
        for model in contextModels:
            models.append(model)

        main_flow_name = os.path.join(outputDir, '%s.dax' % flow.replace('.graphml', ''))
        namespace = flow.replace('.graphml', '')
        flowContext = {'namespace': outputBasename}
        template = Template(self.header)
        text = [template.substitute(flowContext)]
        replicaText = []
        tar = tarfile.open(inputFile, 'r:gz')
        members = tar.getmembers()
        c = 0
        for archiveMember in members:
            outputname = '%s.%s.dax' % (outputBasename, c)
            definitions = {variable: archiveMember.name, 
               index: '%s' % c, 
               Operator.DYNAMIC_INDEX: '%s' % c, 
               'appHome': appHome}
            logger.debug('dynamic-map: invoking compiler')
            try:
                output = open(os.path.join(outputDir, outputname), 'w')
                try:
                    GraysonCompiler.compile(models=models, output=output, modelPath=modelPath.split(os.pathsep), namespace=namespace, version=None, logLevel='debug', modelProperties=definitions, outputdir=tmpOutputDir, sites=sites, toLogFile=os.path.join(outputDir, 'log.txt'))
                finally:
                    if output:
                        output.close()

            except IOError as e:
                logger.error('Encountered IOError %s compiling subdax %s', e.__str__(), output)
                raise e

            replicaText.append('%s file://%s/%s pool="local"' % (outputname, outputDir, outputname))
            template = Template(self.subdax)
            flowContext['c'] = c
            flowContext['outputname'] = outputname
            flowContext['instanceArgs'] = instanceArgs
            flowContext['sites'] = '--sites %s' % sites if instanceArgs == '' else ''
            text.append(template.substitute(flowContext))
            replicaCatalogName = 'replica-catalog.rc'
            masterRC = os.path.join(outputDir, replicaCatalogName)
            self.updateCatalog(master=masterRC, other=os.path.join(tmpOutputDir, replicaCatalogName))
            c += 1

        text.append(self.footer)
        mainFlowContent = ('').join(text)
        GraysonUtil.writeFile(outputPath=os.path.join(outputDir, main_flow_name), data=mainFlowContent)
        logger.debug('dynamic-map: writing output dax: %s' % mainFlowContent)
        replicaText.append('%s file://%s pool="local"' % (os.path.basename(main_flow_name), main_flow_name))
        GraysonUtil.writeFile(os.path.join(outputDir, 'tmp', replicaCatalogName), ('\n').join(replicaText))
        self.updateCatalog(master=masterRC, other=os.path.join(tmpOutputDir, replicaCatalogName))
        transformationCatalogName = 'transformation-catalog.tc'
        masterTC = os.path.join(outputDir, transformationCatalogName)
        self.updateCatalog(master=masterTC, other=os.path.join(tmpOutputDir, transformationCatalogName))
        return

    def updateCatalog(self, masterCat, other):
        newResources = []
        master = GraysonUtil.readFile(masterCat)
        masterLines = master.split('\n')
        for line in masterLines:
            logger.debug('  __ _ _ _ _ _ _____: %s', line)

        sub = GraysonUtil.readFile(other)
        subLines = sub.split('\n')
        masterMap = {}
        for line in masterLines:
            parts = line.split(' ')
            if len(parts) > 0:
                resource = parts[0]
                if resource:
                    masterMap[resource] = resource
                    logger.debug('     resource : %s', resource)

        for line in subLines:
            parts = line.split(' ')
            if len(parts) > 0:
                resource = parts[0]
                if resource and resource not in masterMap:
                    newResources.append(line)
                    logger.debug('     new resource: %s', resource)

        GraysonUtil.writeFile(masterCat, '%s\n%s' % (master, ('\n').join(newResources)))

    def getFileLines(self, fileName):
        return GraysonUtil.readFile(fileName).split('\n')

    def updateCatalog(self, master, other):
        masterText = GraysonUtil.readFile(master)
        text = GraysonUtil.readFile(other)
        GraysonUtil.writeFile(master, '%s\n%s' % (masterText, text))