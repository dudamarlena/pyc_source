# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/scox/dev/grayson/venv/lib/python2.7/site-packages/grayson/wms/pegasus/pegasusWMS.py
# Compiled at: 2012-07-18 14:51:47
from string import Template
from copy import copy
import getopt, json, logging, logging.handlers, os, re, shlex, shutil, string, socket, subprocess, sys, time, traceback, glob
from sys import settrace
from Pegasus.DAX3 import ADAG
from Pegasus.DAX3 import DAX
from Pegasus.DAX3 import Dependency
from Pegasus.DAX3 import DuplicateError
from Pegasus.DAX3 import Executable
from Pegasus.DAX3 import File
from Pegasus.DAX3 import Job
from Pegasus.DAX3 import Link
from Pegasus.DAX3 import PFN
from Pegasus.DAX3 import Profile
from Pegasus.DAX3 import Transformation
from grayson.compiler.abstractsyntax import ASTProfile
from grayson.executor import Executor
from grayson.log import LogManager
from grayson.common.util import GraysonUtil
from grayson.wms.workflowManagementSystem import WorkflowManagementSystem
from grayson.wms.workflowManagementSystem import WorkflowModel
logger = logging.getLogger(__name__)

class PegasusWMS(WorkflowManagementSystem):

    def __init__(self, outputDir):
        self.outputDir = outputDir
        if not self.outputDir:
            raise ValueError('outputDir required')
        self.pegasusProperties = PegasusProperties()
        self.siteCatalog = SiteCatalogXML(self)
        self.transformationCatalog = PegasusTC()
        self.replicaCatalog = PegasusFileRC()
        self.dataConfiguration = None
        return

    def getOutputDir(self):
        logger.debug('getoutputdir: %s %s', self.outputDir, self)
        return self.outputDir

    def getSiteCatalog(self):
        return self.siteCatalog

    def getTransformationCatalog(self):
        return self.transformationCatalog

    def getReplicaCatalog(self):
        return self.replicaCatalog

    def createWorkflowModel(self, namespace):
        return PegasusWorkflowModel(namespace, self)

    def enableShellExecution(self, enabled=True):
        return self.pegasusProperties.enableShellExecution(enabled)

    def isShellExecutionEnabled(self):
        return self.pegasusProperties.isShellExecutionEnabled()
        if self.isShellExecutionEnabled():
            installed = 'false'

    def setDataConfiguration(self, dataConfiguration):
        self.dataConfiguration = dataConfiguration

    def getDataConfiguration(self):
        return self.dataConfiguration

    def enableSymlinkTransfers(self, enabled=True):
        self.pegasusProperties.enableSymlinkTransfers(enabled)

    def getExecuteArguments(self, sites, workflow=None, other=[]):
        result = None
        pegasusHome = GraysonUtil.getPegasusHome()
        args = ['--conf=${outputDir}/${pegasusProperties}',
         '--sites ${sites}',
         '--force',
         '--verbose',
         '--verbose',
         '--verbose',
         '--nocleanup',
         '--output local']
        if self.dataConfiguration:
            args.append('-Dpegasus.data.configuration=%s' % self.dataConfiguration)
            args.append('--staging-site=local')
        for arg in other:
            args.append(arg)

        template = Template((' ').join(args))
        context = {'outputDir': self.getOutputDir(), 
           'pegasusProperties': PegasusProperties.PEGASUS_PROPERTIES, 
           'sites': sites}
        if workflow:
            context['outputDax'] = os.path.join(self.getOutputDir(), workflow)
        result = template.substitute(context)
        logger.debug('generated workflow execute arguments: %s', result)
        return result

    def executeWorkflow(self, sites, workflowName, compilerPlugin=None):
        additionalArgs = [' --dir ${outputDir}/work --dax ${outputDax} --submit']
        arguments = self.getExecuteArguments(sites=sites, workflow=workflowName, other=additionalArgs)
        executeCommand = 'pegasus-plan %s' % arguments
        logger.debug('getExecuteArguments: %s', executeCommand)
        executor = Executor({})
        logger.info('--(pegasus-plan): %s', executeCommand)
        lines = []

        def submitProcessor(line):
            line = line.replace('\n', '')
            lines.append(line)
            logger.info('--(pegasus-plan): %s', line)

        wrappedOutputProcessor = submitProcessor
        if compilerPlugin:

            def wrappedOutputProcessor(line):
                submitProcessor(line)
                compilerPlugin.notifyShellEvent(line, workflowName)

        try:
            executor.execute(executeCommand, pipe=True, processor=wrappedOutputProcessor)
        except Exception as e:
            traceback.print_exc(e)
            logger.error(('\n').join(lines))
            raise e

    def writeMetaDataCatalogs(self):
        GraysonUtil.writeFile(outputPath=os.path.join(self.outputDir, PegasusProperties.SITE_CATALOG), data=self.getSiteCatalog().generateXML())
        GraysonUtil.writeFile(outputPath=os.path.join(self.outputDir, PegasusProperties.REPLICA_CATALOG), data=self.getReplicaCatalog().generateRC())
        GraysonUtil.writeFile(outputPath=os.path.join(self.outputDir, PegasusProperties.TRANSFORMATION_CATALOG), data=self.getTransformationCatalog().generateTC())
        GraysonUtil.writeFile(outputPath=os.path.join(os.path.join(self.outputDir, PegasusProperties.PEGASUS_PROPERTIES)), data=self.pegasusProperties.generateProperties(configDir=self.outputDir))


class PegasusProperties:
    PEGASUS_PROPERTIES = 'pegasus.properties'
    REPLICA_CATALOG = 'replica-catalog.rc'
    SITE_CATALOG = 'sites.xml'
    TRANSFORMATION_CATALOG = 'transformation-catalog.tc'
    CODE_GENERATOR_EQUALS_SHELL = 'pegasus.code.generator = Shell'

    def __init__(self):
        self.symlinkTransfers = False
        self.text = '\npegasus.catalog.site=XML3\npegasus.catalog.site.file=${configDir}/${siteCatalog}\n\npegasus.catalog.replica=File\npegasus.catalog.replica.file=${configDir}/${replicaCatalog}\n\npegasus.catalog.transformation=Text\npegasus.catalog.transformation.file=${configDir}/${transformationCatalog}\n\npegasus.dir.useTimestamp=true\npegasus.dir.storage.deep=false\npegasus.transfer.links=${symlinkTransfers}\n\n${pegasusCodeGenerator}\n'
        self.pegasusCodeGenerator = ''

    def enableSymlinkTransfers(self, enabled=True):
        self.symlinkTransfers = enabled

    def enableShellExecution(self, enabled=True):
        self.pegasusCodeGenerator = self.CODE_GENERATOR_EQUALS_SHELL

    def isShellExecutionEnabled(self):
        return self.pegasusCodeGenerator == self.CODE_GENERATOR_EQUALS_SHELL

    def generateProperties(self, siteFile='sites.xml', configDir='.'):
        template = Template(self.text)
        context = {'configDir': configDir, 
           'siteCatalog': self.SITE_CATALOG, 
           'replicaCatalog': self.REPLICA_CATALOG, 
           'transformationCatalog': self.TRANSFORMATION_CATALOG, 
           'symlinkTransfers': str(self.symlinkTransfers).lower(), 
           'pegasusCodeGenerator': self.pegasusCodeGenerator}
        return template.substitute(context)


class PegasusTC:

    def __init__(self):
        self.text = '\ntr ${namespace}::${jobName}:${version} {\n   site ${cluster} {\n      pfn "${location}"\n      arch "${architecture}"\n      os "${OS}"\n      type "${transfer}"\n   }\n}\n\n'
        self.entries = {}

    def addEntry(self, jobName, location, transfer='INSTALLED', architecture='x86_64', OS='linux', cluster='local', namespace='app', version='1.0'):
        if not architecture:
            architecture = ''
        if not version:
            version = '1.0'
        if not cluster:
            cluster = 'local'
        if location.startswith(os.sep):
            location = 'file://%s' % location
        if not transfer:
            transfer = 'STAGEABLE'
        logger.debug('wms:pegasus:transformationcatalog:add-entry : job=%s, location=%s, transfer=%s, arch=%s, os=%s, cluster=%s, namespace=%s', jobName, location, transfer, architecture, OS, cluster, namespace)
        template = Template(self.text)
        context = {'jobName': jobName, 
           'location': location, 
           'transfer': transfer, 
           'architecture': architecture, 
           'OS': OS, 
           'cluster': cluster, 
           'namespace': namespace, 
           'version': version}
        entryText = template.substitute(context)
        key = self.getKey(namespace, jobName, version)
        self.entries[key] = entryText

    def getKey(self, namespace, app, version):
        return '%s::%s:%s' % (namespace, app, version)

    def generateTC(self):
        text = []
        keys = sorted(self.entries.iterkeys())
        for key in keys:
            text.append(self.entries[key])

        return ('').join(text)


class PegasusFileRC(object):

    def __init__(self):
        self.text = '${fileName} ${fileURL} pool="${poolName}"'
        self.entries = {}

    def addEntry(self, fileName, fileURL, pool):
        if fileURL is not None:
            logger.debug('wms:pegasus:replica-catalog:add-entry: file(%s)=>(%s,%s)', fileName, fileURL, pool)
            template = Template(self.text)
            context = {'fileName': fileName, 
               'fileURL': fileURL, 
               'poolName': pool}
            entryText = template.substitute(context)
            self.entries[fileName] = entryText
        return

    def dump(self):
        keys = sorted(self.entries.keys())
        for k in keys:
            logger.debug('zzz: RC: %s', k)

    def removeEntry(self, fileName):
        if fileName in self.entries:
            logger.debug('zzz: DELETING filename: %s', fileName)
            del self.entries[fileName]

    def generateRC(self):
        logger.debug('wms:pegasus:replica-catalog:generateRC')
        values = []
        for key in self.entries:
            values.append(self.entries[key])

        values.sort()
        return ('\n').join(values)


class SiteCatalogXML(object):
    LOCAL = 'local'
    HOSTNAME = 'hostName'

    def __init__(self, wms):
        self.wms = wms
        self.sites = {}
        self.stagingTemplate = {'architecture': 'x86_64', 
           'os': 'LINUX', 
           'protocol': 'file', 
           'name': 'staging'}
        self.siteProperties = {'siteName': 'local', 
           'hostName': 'localhost', 
           'architecture': 'x86_64', 
           'os': 'LINUX', 
           'gridType': 'gt2', 
           'scheduler': 'fork', 
           'schedulerType': 'Fork', 
           'jobType': 'compute', 
           'scratchFileServerProtocol': 'file', 
           'scratchFileServerURL': 'file://', 
           'scratchFileServerMountPoint': '', 
           'scratchInternalMountPoint': '', 
           'scratchInternalMountPointFreeSize': '100G', 
           'scratchInternalTotalSize': '30G', 
           'storageFileServerProtocol': 'file', 
           'storageFileServerMountPoint': '', 
           'storageMountPoint': '', 
           'storageFreeSize': '100G', 
           'storageTotalSize': '30G', 
           'storageInternalMountPoint': '', 
           'storageFreeSize': '100G', 
           'storageTotalSize': '30G', 
           'pegasusLocation': '/opt/pegasus', 
           'globusLocation': '/opt/globus'}
        self.configureLocal()
        self.xmlHeader = '<?xml version="1.0" encoding="UTF-8"?>\n<sitecatalog\n        xmlns="http://pegasus.isi.edu/schema/sitecatalog"\n        xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"\n        xsi:schemaLocation="http://pegasus.isi.edu/schema/sitecatalog http://pegasus.isi.edu/schema/sc-3.0.xsd"\n        version="3.0">\n        '
        self.xmlSite = '    \n   <site  handle="${siteName}" arch="${architecture}" os="${os}">\n      <grid  type="${gridType}" contact="${hostName}/jobmanager-fork" scheduler="Fork" jobtype="auxillary"/>\n      <grid  type="${gridType}" contact="${hostName}/jobmanager-${scheduler}" scheduler="${schedulerType}" jobtype="${jobType}"/>\n      <head-fs>\n         <scratch>\n            <shared>\n               <file-server protocol="${scratchFileServerProtocol}" url="${scratchFileServerURL}" mount-point="${scratchFileServerMountPoint}"/>\n               <internal-mount-point mount-point="${scratchInternalMountPoint}"/>\n            </shared>\n         </scratch>\n         <storage>\n            <shared>\n               <file-server protocol="${storageFileServerProtocol}" url="${storageFileServerURL}" mount-point="${storageFileServerMountPoint}"/>\n               <internal-mount-point mount-point="${storageInternalMountPoint}"/>\n            </shared>\n         </storage>\n       </head-fs>\n       <replica-catalog  type="LRC" url="rlsn://dummyValue.url.edu" />\n       <profile namespace="dagman" key="retry">0</profile>\n       ${X509_user_proxy_profile}\n       <profile namespace="env"    key="PEGASUS_HOME" >${pegasusLocation}</profile>\n       <profile namespace="env"    key="GLOBUS_LOCATION" >${globusLocation}</profile>\n   </site>'
        self.xmlStaging = '\n    <site handle="${name}" arch="${architecture}" os="${os}">\n        <head-fs>\n            <scratch>\n                <shared>\n                    <file-server protocol="${protocol}" url="${protocol}://${hostname}" mount-point="${directory}/staging"/>\n                    <internal-mount-point mount-point="${directory}/staging"/>\n                </shared>\n            </scratch>\n        </head-fs>\n        <replica-catalog  type="LRC" url="rlsn://dummyValue.url.edu" />\n    </site>'
        self.xmlSitePool = '\n    <site handle="${clusterId}" arch="${architecture}" os="${os}">\n        <head-fs>\n            <scratch />\n            <storage />\n        </head-fs>\n        <replica-catalog  type="LRC" url="rlsn://dummyValue.url.edu" />\n        ${profileText}\n    </site>'
        self.xmlFooter = '\n</sitecatalog>\n        '

    def configureLocal(self):
        pegasusLocation = GraysonUtil.getPegasusHome()
        globusLocation = os.getenv('GLOBUS_LOCATION')
        if not globusLocation:
            raise ValueError('GLOBUS_LOCATION must be defined')
        self.addEntry('local', {'architecture': 'x86_64', 
           'scratchFileServerProtocol': 'file', 
           'scratchFileServerMountPoint': '%s/work/outputs' % self.wms.getOutputDir(), 
           'scratchInternalMountPoint': '%s/work/outputs' % self.wms.getOutputDir(), 
           'storageFileServerProtocol': 'file', 
           'storageFileServerMountPoint': '%s/work/outputs' % self.wms.getOutputDir(), 
           'storageMountPoint': '%s/work/outputs' % self.wms.getOutputDir(), 
           'storageInternalMountPoint': '%s/work/outputs' % self.wms.getOutputDir(), 
           'pegasusLocation': pegasusLocation, 
           'globusLocation': globusLocation})

    def addEntry(self, siteName, properties, profiles=[]):
        if siteName not in self.sites:
            if 'clusterId' in properties:
                for key in ['os', 'architecture', 'scheduler']:
                    properties[key] = self.siteProperties[key]

                self.sites[siteName] = properties
                logger.debug('wms:pegasus:register-site %s', properties)
            else:
                base = copy(self.siteProperties)
                logger.debug('wms:pegasus:register-site %s', base)
                base.update(properties)
                self.sites[siteName] = base

    def getEntry(self, siteName):
        return self.sites[siteName]

    def getScratchURL(self, fileName, siteKey='local'):
        return self.getURL(fileName, siteKey, urlType='scratch')

    def getURL(self, fileName, siteKey='local', urlType='storage'):
        fileURL = None
        protocolKey = '%sFileServerProtocol' % urlType
        mountPointKey = '%sFileServerMountPoint' % urlType
        if logging.getLogger().isEnabledFor(logging.DEBUG):
            logger.debug('getURL(%s, %s, %s) protocolKey: %s, mountPointKey: %s', fileName, siteKey, urlType, protocolKey, mountPointKey)
        if siteKey in self.sites:
            logger.debug('siteinsites %s', siteKey)
            site = self.getEntry(siteKey)
            if protocolKey in site and mountPointKey in site:
                hostname = site['hostName']
                protocol = site[protocolKey]
                mountPoint = site[mountPointKey]
                if protocol == 'file':
                    path = os.path.abspath('%s/%s' % (mountPoint, fileName))
                    fileURL = 'file://%s' % path
                elif self.HOSTNAME in site:
                    hostname = site[self.HOSTNAME]
                    fileURL = '%s://%s/%s/%s' % (protocol, hostname, mountPoint, fileName)
                logger.debug('getURL (url=%s hostname=%s, protocol=%s, mountPoint=%s\nsite=%s)', fileURL, hostname, protocol, mountPoint, site)
        return fileURL

    def generateXML(self):
        siteText = [
         self.xmlHeader]
        for siteName in self.sites:
            logger.debug('generating site catalog data for site (%s)', siteName)
            site = self.sites[siteName]
            template = None
            logger.debug('site: %s', json.dumps(site, sort_keys=True, indent=3))
            staging = None
            if 'scratchFileServerMountPoint' in site:
                x509userproxyKey = 'x509userproxy'
                x509userproxyProfileKey = 'X509_user_proxy_profile'
                x509userproxyProfile = ''
                if x509userproxyKey in site:
                    x509userproxyProfile = '<profile namespace="condor" key="x509userproxy" >%s</profile>' % site[x509userproxyKey]
                site[x509userproxyProfileKey] = x509userproxyProfile
                for kind in ['scratch', 'storage']:
                    fileServerProtocolKey = '%sFileServerProtocol' % kind
                    fileServerURLKey = '%sFileServerURL' % kind
                    if site[fileServerProtocolKey] is 'file':
                        site[fileServerURLKey] = 'file://'
                    else:
                        site[fileServerURLKey] = '%s://%s' % (site[fileServerProtocolKey], site['hostName'])

                template = Template(self.xmlSite)
            elif 'clusterId' in site:
                profileText = []
                if 'profiles' in site:
                    profiles = site['profiles']
                    for groupKey in profiles:
                        profileGroup = profiles[groupKey]
                        for key in profileGroup:
                            value = profileGroup[key]
                            profileText.append('\n        <profile namespace="%s" key="%s" >%s</profile>' % (groupKey, key, value))

                    site['profileText'] = ('').join(profileText)
                template = Template(self.xmlSitePool)
                if 'staging' in site:
                    staging = site['staging']
            siteText.append(template.substitute(site))
            if staging:
                symmetric_difference = set(staging) ^ set(self.stagingTemplate)
                for k in symmetric_difference:
                    if k not in staging:
                        staging[k] = self.stagingTemplate[k]

                template = Template(self.xmlStaging)
                siteText.append(template.substitute(staging))

        siteText.append(self.xmlFooter)
        return ('\n').join(siteText)


class PegasusWorkflowModel(WorkflowModel):

    def __init__(self, namespace, wms):
        logger.debug('wms:pegasus:create-workflowmodel: %s' % namespace)
        self.wms = wms
        logger.debug('outputdir: %s', wms.getOutputDir())
        self.adag = ADAG(namespace)
        self.namespace = namespace
        self.files = {}
        self.exes = {}
        self.propertyMap = {}
        self.nodes = {}
        self.jobTransformations = {}
        self.variableMap = {'literalToVariable': {}, 'literalToNodeId': {}}

    def addToVariableMap(self, literal, variable, id):
        self.variableMap['literalToVariable'][literal] = variable
        self.variableMap['literalToNodeId'][literal] = id
        logger.debug('variablematch: recorded lit=%s var=%s id=%s', literal, variable, id)

    def setProperties(self, nodeId, properties):
        logger.debug('wms:pegasus:dax:setprops: (%s)->(%s)' % (nodeId, properties))
        self.propertyMap[nodeId] = properties

    def getProperties(self, nodeId):
        return self.propertyMap[nodeId]

    def createFile(self, fileName):
        return File(fileName)

    def addNode(self, id, node):
        logger.debug('wms:pegasus:dax:add-node: (%s)->(%s)' % (node.getId(), properties))
        self.nodes[id] = node

    def getNode(self, id):
        node = None
        if id in self.nodes:
            node = self.nodes[id]
            return node
        else:
            return

    def addFile(self, fileName, fileURL=None, site=None):
        file = self.getFile(fileName)
        if not file:
            file = File(fileName)
            if not fileURL:
                fileURL = 'file://%s/%s' % (self.wms.getOutputDir(), fileName)
            if not site:
                site = 'local'
            if not isinstance(fileURL, basestring) and len(fileURL) > 0:
                fileURL = fileURL[0]
            logger.debug('--add-pfn: (%s)(%s)(%s)', fileName, fileURL, site)
            pfn = PFN(fileURL, site)
            file.addPFN(pfn)
            self.adag.addFile(file)
            self.files[fileName] = file
        return file

    def getFile(self, fileName, prefix=''):
        key = '%s%s' % (prefix, fileName)
        if key in self.files:
            logger.debug('wms:pegasus:dax:get-file: (%s)' % key)
            return self.files[key]
        else:
            return
            return

    def addExecutable(self, jobId, name, path, version='1.0', exe_os='linux', exe_arch='x86_64', site='local', installed='true'):
        e_exe = self.getExecutable(name)
        if not version:
            version = '1.0'
        if not exe_arch:
            exe_arch = 'x86_64'
        if not e_exe:
            e_exe = Executable(namespace=self.namespace, name=name, version=version, os=exe_os, arch=exe_arch, installed=installed)
            if not site:
                site = 'local'
            if not installed:
                installed = False
            if logging.getLogger().isEnabledFor(logging.DEBUG):
                logger.debug('wms:pegasus:dax:add-exe: (name=[%s], path=[%s], version=[%s], os=[%s], arch=[%s], site=[%s], installed=[%s])' % (
                 name,
                 path,
                 version,
                 exe_os,
                 exe_arch,
                 site,
                 installed))
            if '://' not in path:
                path = 'file://%s' % path
            if not path:
                raise ValueError('empty path for executable: %s at site %s' % (name, site))
            e_exe.addPFN(PFN(path, site))
            if not installed:
                e_exe.installed = installed
            self.adag.addExecutable(e_exe)
            self.exes[name] = e_exe
            transformation = Transformation(name, self.namespace, version)
            self.jobTransformations[jobId] = transformation
        return e_exe

    def getExecutable(self, name):
        key = name
        if key in self.exes:
            return self.exes[key]
        else:
            return
            return

    def addSubWorkflow(self, name, transformation=None):
        abstractJob = DAX(name)
        self.adag.addDAX(abstractJob)
        return abstractJob

    def addJob(self, id):
        transformation = self.jobTransformations[id]
        logger.debug('wms:pegasus:add-job: transformation(%s) jobid(%s)', transformation.name, id)
        abstractJob = Job(name=transformation, id=id)
        self.adag.addJob(abstractJob)
        return abstractJob

    def addProfiles(self, abstractJob, profiles):
        if profiles:
            for astProfile in profiles:
                logger.debug('wms:pegasus:add-profile: (namespace=%s,key=%s,value=%s) to job (%s)', astProfile.namespace, astProfile.key, astProfile.value, abstractJob.name)
                profile = Profile(astProfile.namespace, astProfile.key, astProfile.value)
                abstractJob.addProfile(profile)

    def addFiles(self, abstractJob, files, link):
        if files:
            for fileKey in files:
                tuple = files[fileKey]
                fileElement = tuple[0]
                file = fileElement.getDaxNode()
                try:
                    abstractJob.uses(file, link=link)
                    arg = tuple[1]
                    if arg:
                        abstractJob.addArguments(arg, file)
                except DuplicateError:
                    pass

    def addInputFiles(self, abstractJob, files):
        self.addFiles(abstractJob, files, Link.INPUT)

    def addOutputFiles(self, abstractJob, files):
        self.addFiles(abstractJob, files, Link.OUTPUT)

    def addArguments(self, abstractJob, arguments):
        if arguments:
            abstractJob.addArguments(arguments)

    def addDependency(self, parent, child):
        self.adag.addDependency(Dependency(parent, child))

    def writeExecutable(self, stream):
        self.adag.writeXML(stream)
        filename = '%s.%s' % (self.namespace, 'obj')
        filepath = os.path.join(self.wms.getOutputDir(), filename)
        try:
            output = None
            try:
                output = open(filepath, 'w')
                output.write(json.dumps(self.variableMap, indent=3, sort_keys=True))
                output.flush()
            finally:
                if output:
                    output.close()

        except IOError:
            traceback.print_stack()

        return

    def getADAG(self):
        return self.adag