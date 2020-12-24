# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/scox/dev/grayson/venv/lib/python2.7/site-packages/wms/workflowManagementSystem.py
# Compiled at: 2012-03-02 14:59:52
""" system """
from string import Template
from copy import copy
import getopt, json, logging, logging.handlers, os, re, shlex, shutil, string, socket, subprocess, sys, time, traceback, glob
from sys import settrace

class WorkflowManagementSystem(object):

    def setOutputDir(self, outputDir):
        pass

    def getOutputDir(self):
        pass

    def getSiteCatalog(self):
        pass

    def getTransformationCatalog(self):
        pass

    def getReplicaCatalog(self):
        pass

    def getExecuteArguments(self, sites, workflow=None, other=[]):
        pass

    def writeMetaDataCataogs(self, outputDir):
        pass

    def enableSymlinkTransfers(self, enabled=False):
        pass

    def enableShellExecution(self, enabled=True):
        pass

    def createWorkflowModel(self, namespace):
        pass

    def executeWorkflow(self, sites, workflowName, compilerPlugin=None):
        pass


class WorkflowModel(object):

    def setWorkflowRoot(self, workflowRoot):
        pass

    def setProperties(self, nodeId, properties):
        pass

    def getProperties(self, nodeId):
        pass

    def addNode(self, id, node):
        pass

    def getNode(self, id):
        pass

    def createFile(self, fileName):
        pass

    def addFile(self, fileName, isStaticInput=False, fileURL=None, site=None):
        pass

    def getFile(self, fileName, prefix=''):
        pass

    def addExecutable(self, jobId, name, path, version='1.0', exe_os='linux', exe_arch='x86', site='local', installed='true'):
        pass

    def getExecutable(self, name):
        pass

    def addSubWorkflow(self, name, transformation=None):
        pass

    def addJob(self, id, transformation):
        pass

    def addProfiles(self, asbtractJob, profiles):
        pass

    def addInputFiles(self, abstractJob, files):
        pass

    def addOutputFiles(self, abstractJob, files):
        pass

    def addArguments(self, abstractJob, arguments):
        pass

    def addDependency(self, parent, child):
        pass

    def writeExecutable(self, stream):
        pass

    def getADAG(self):
        pass


if __name__ == '__main__':
    test_grayson_compiler()