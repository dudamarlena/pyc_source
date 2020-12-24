# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: D:\ProgramData\lib\site-packages\arelle\PluginManager.py
# Compiled at: 2018-02-26 09:10:06
# Size of source mod 2**32: 25418 bytes
"""
Created on March 1, 2012

@author: Mark V Systems Limited
(c) Copyright 2011 Mark V Systems Limited, All rights reserved.

based on pull request 4

"""
import os, sys, types, time, ast, imp, io, json, gettext, traceback
from arelle.Locale import getLanguageCodes
from arelle.FileSource import openFileStream
from arelle.UrlUtil import isAbsolute
try:
    from collections import OrderedDict
except ImportError:
    OrderedDict = dict

PLUGIN_TRACE_FILE = None
pluginJsonFile = None
pluginConfig = None
pluginConfigChanged = False
modulePluginInfos = {}
pluginMethodsForClasses = {}
_cntlr = None
_pluginBase = None
EMPTYLIST = []

def init(cntlr, loadPluginConfig=True):
    global _cntlr
    global _pluginBase
    global modulePluginInfos
    global pluginConfig
    global pluginConfigChanged
    global pluginJsonFile
    global pluginMethodsForClasses
    pluginConfigChanged = False
    _cntlr = cntlr
    _pluginBase = cntlr.pluginDir + os.sep
    if loadPluginConfig:
        try:
            pluginJsonFile = cntlr.userAppDir + os.sep + 'plugins.json'
            with io.open(pluginJsonFile, 'rt', encoding='utf-8') as (f):
                pluginConfig = json.load(f)
            freshenModuleInfos()
        except Exception:
            pass

    if pluginConfig is None:
        pluginConfig = {'modules':{},  'classes':{}}
        pluginConfigChanged = False
    modulePluginInfos = {}
    pluginMethodsForClasses = {}


def reset():
    modulePluginInfos.clear()
    pluginMethodsForClasses.clear()


def orderedPluginConfig():
    return OrderedDict((
     (
      'modules',
      OrderedDict((moduleName,
       OrderedDict(sorted((moduleInfo.items()), key=(lambda k: {'name':'01', 
        'status':'02', 
        'version':'03', 
        'fileDate':'04', 
        'version':'05',  'description':'05', 
        'moduleURL':'06', 
        'localeURL':'07', 
        'localeDomain':'08', 
        'license':'09', 
        'author':'10', 
        'copyright':'11', 
        'classMethods':'12'}.get(k[0], k[0]))))) for moduleName, moduleInfo in sorted(pluginConfig['modules'].items()))),
     (
      'classes', OrderedDict(sorted(pluginConfig['classes'].items())))))


def save(cntlr):
    global pluginConfigChanged
    if pluginConfigChanged:
        if cntlr.hasFileSystem:
            pluginJsonFile = cntlr.userAppDir + os.sep + 'plugins.json'
            with io.open(pluginJsonFile, 'wt', encoding='utf-8') as (f):
                jsonStr = _STR_UNICODE(json.dumps((orderedPluginConfig()), ensure_ascii=False, indent=2))
                f.write(jsonStr)
            pluginConfigChanged = False


def close():
    global webCache
    modulePluginInfos.clear()
    pluginMethodsForClasses.clear()
    webCache = None


def modulesWithNewerFileDates():
    names = set()
    for moduleInfo in pluginConfig['modules'].values():
        freshenedFilename = _cntlr.webCache.getfilename((moduleInfo['moduleURL']), checkModifiedTime=True, normalize=True, base=_pluginBase)
        try:
            if moduleInfo['fileDate'] < time.strftime('%Y-%m-%dT%H:%M:%S UTC', time.gmtime(os.path.getmtime(freshenedFilename))):
                names.add(moduleInfo['name'])
        except Exception as err:
            _msg = _('Exception at plug-in method modulesWithNewerFileDates: {error}').format(error=err)
            if PLUGIN_TRACE_FILE:
                with open(PLUGIN_TRACE_FILE, 'at', encoding='utf-8') as (fh):
                    fh.write(_msg + '\n')
            else:
                print(_msg, file=(sys.stderr))

    return names


def freshenModuleInfos():
    for moduleName in pluginConfig['modules'].keys():
        moduleInfo = pluginConfig['modules'][moduleName]
        freshenedFilename = _cntlr.webCache.getfilename((moduleInfo['moduleURL']), checkModifiedTime=True, normalize=True, base=_pluginBase)
        try:
            if moduleInfo['fileDate'] != time.strftime('%Y-%m-%dT%H:%M:%S UTC', time.gmtime(os.path.getmtime(freshenedFilename))):
                freshenedModuleInfo = moduleModuleInfo((moduleInfo['moduleURL']), reload=True)
                if freshenedModuleInfo is not None:
                    pluginConfig['modules'][moduleName] = freshenedModuleInfo
        except Exception as err:
            _msg = _('Exception at plug-in method freshenModules: {error}').format(error=err)
            if PLUGIN_TRACE_FILE:
                with open(PLUGIN_TRACE_FILE, 'at', encoding='utf-8') as (fh):
                    fh.write(_msg + '\n')
            else:
                print(_msg, file=(sys.stderr))


def moduleModuleInfo(moduleURL, reload=False, parentImportsSubtree=False):
    moduleFilename = _cntlr.webCache.getfilename(moduleURL, reload=reload, normalize=True, base=_pluginBase)
    if moduleFilename:
        f = None
        try:
            if os.path.isdir(moduleFilename):
                if os.path.isfile(os.path.join(moduleFilename, '__init__.py')):
                    moduleFilename = os.path.join(moduleFilename, '__init__.py')
                else:
                    return
            else:
                if not moduleFilename.endswith('.py'):
                    if not os.path.exists(moduleFilename):
                        if os.path.exists(moduleFilename + '.py'):
                            moduleFilename += '.py'
                moduleDir, moduleName = os.path.split(moduleFilename)
                if PLUGIN_TRACE_FILE:
                    with open(PLUGIN_TRACE_FILE, 'at', encoding='utf-8') as (fh):
                        fh.write('Scanning module for plug-in info: {}\n'.format(moduleFilename))
                f = openFileStream(_cntlr, moduleFilename)
                tree = ast.parse((f.read()), filename=moduleFilename)
                constantStrings = {}
                functionDefNames = set()
                moduleImports = []
                for item in tree.body:
                    if isinstance(item, ast.Assign):
                        attr = item.targets[0].id
                        if attr == '__pluginInfo__':
                            f.close()
                            moduleInfo = {'name': None}
                            classMethods = []
                            importURLs = []
                            for i, key in enumerate(item.value.keys):
                                _key = key.s
                                _value = item.value.values[i]
                                _valueType = _value.__class__.__name__
                                if _key == 'import':
                                    if _valueType == 'Str':
                                        importURLs.append(_value.s)
                                    else:
                                        if _valueType in ('List', 'Tuple'):
                                            for elt in _value.elts:
                                                importURLs.append(elt.s)

                                        else:
                                            if _valueType == 'Str':
                                                moduleInfo[_key] = _value.s
                                            else:
                                                if _valueType == 'Name':
                                                    if _value.id in constantStrings:
                                                        moduleInfo[_key] = constantStrings[_value.id]
                                                    else:
                                                        if _value.id in functionDefNames:
                                                            classMethods.append(_key)
                                                elif _key == 'imports':
                                                    pass
                                        if _valueType in ('List', 'Tuple'):
                                            importURLs = [elt.s for elt in _value.elts]

                            moduleInfo['classMethods'] = classMethods
                            moduleInfo['moduleURL'] = moduleURL
                            moduleInfo['status'] = 'enabled'
                            moduleInfo['fileDate'] = time.strftime('%Y-%m-%dT%H:%M:%S UTC', time.gmtime(os.path.getmtime(moduleFilename)))
                            mergedImportURLs = []
                            _moduleImportsSubtree = False
                            for _url in importURLs:
                                if _url.startswith('module_import'):
                                    for moduleImport in moduleImports:
                                        mergedImportURLs.append(moduleImport + '.py')

                                    if _url == 'module_import_subtree':
                                        _moduleImportsSubtree = True
                                else:
                                    if _url == 'module_subtree':
                                        for _dir in os.listdir(moduleDir):
                                            _subtreeModule = os.path.join(moduleDir, _dir)
                                            if os.path.isdir(_subtreeModule) and _dir != '__pycache__':
                                                mergedImportURLs.append(_subtreeModule)

                                    else:
                                        mergedImportURLs.append(_url)

                            if parentImportsSubtree:
                                if not _moduleImportsSubtree:
                                    _moduleImportsSubtree = True
                                    for moduleImport in moduleImports:
                                        mergedImportURLs.append(moduleImport + '.py')

                            imports = []
                            for _url in mergedImportURLs:
                                if isAbsolute(_url) or os.path.isabs(_url):
                                    _importURL = _url
                                else:
                                    _importURL = os.path.join(os.path.dirname(moduleURL), os.path.normpath(_url))
                                if not os.path.exists(_importURL):
                                    _importURL = _url
                                _importModuleInfo = moduleModuleInfo(_importURL, reload, _moduleImportsSubtree)
                                if _importModuleInfo:
                                    _importModuleInfo['isImported'] = True
                                    imports.append(_importModuleInfo)

                            moduleInfo['imports'] = imports
                            return moduleInfo
                        if isinstance(item.value, ast.Str):
                            for assignmentName in item.targets:
                                constantStrings[assignmentName.id] = item.value.s

                    else:
                        if isinstance(item, ast.ImportFrom):
                            if item.level == 1:
                                if item.module is None:
                                    for importee in item.names:
                                        if importee.name == '*':
                                            for _file in os.listdir(moduleDir):
                                                if _file != moduleFile and os.path.isfile(_file) and _file.endswith('.py'):
                                                    moduleImports.append(_file)

                                        elif os.path.isfile(os.path.join(moduleDir, importee.name + '.py')):
                                            if importee.name not in moduleImports:
                                                moduleImports.append(importee.name)

                                else:
                                    modulePkgs = item.module.split('.')
                                    modulePath = (os.path.join)(*modulePkgs)
                                    if os.path.isfile(os.path.join(moduleDir, modulePath) + '.py'):
                                        if modulePath not in moduleImports:
                                            moduleImports.append(modulePath)
                                    for importee in item.names:
                                        _importeePfxName = os.path.join(modulePath, importee.name)
                                        if os.path.isfile(os.path.join(moduleDir, _importeePfxName) + '.py') and _importeePfxName not in moduleImports:
                                            moduleImports.append(_importeePfxName)

                            else:
                                if isinstance(item, ast.FunctionDef):
                                    functionDefNames.add(item.name)

                if PLUGIN_TRACE_FILE:
                    with open(PLUGIN_TRACE_FILE, 'at', encoding='utf-8') as (fh):
                        fh.write('Successful module plug-in info: ' + moduleFilename + '\n')
        except Exception as err:
            _msg = _('Exception obtaining plug-in module info: {error}\n{traceback}').format(error=err,
              traceback=(traceback.format_tb(sys.exc_info()[2])))
            if PLUGIN_TRACE_FILE:
                with open(PLUGIN_TRACE_FILE, 'at', encoding='utf-8') as (fh):
                    fh.write(_msg + '\n')
            else:
                print(_msg, file=(sys.stderr))

        if f:
            f.close()


def moduleInfo(pluginInfo):
    moduleInfo = {}
    for name, value in pluginInfo.items():
        if isinstance(value, '_STR_UNICODE'):
            moduleInfo[name] = value
        else:
            if isinstance(value, types.FunctionType):
                moduleInfo.getdefault('classes', []).append(name)


def loadModule(moduleInfo, packagePrefix=''):
    global pluginConfigChanged
    name = moduleInfo['name']
    moduleURL = moduleInfo['moduleURL']
    moduleFilename = _cntlr.webCache.getfilename(moduleURL, normalize=True, base=_pluginBase)
    if moduleFilename:
        try:
            if os.path.basename(moduleFilename) == '__init__.py':
                if os.path.isfile(moduleFilename):
                    moduleFilename = os.path.dirname(moduleFilename)
            elif os.path.isdir(moduleFilename) and os.path.isfile(os.path.join(moduleFilename, '__init__.py')):
                moduleDir = os.path.dirname(moduleFilename)
                moduleName = os.path.basename(moduleFilename)
                packageImportPrefix = moduleName + '.'
            else:
                moduleName = os.path.basename(moduleFilename).partition('.')[0]
                moduleDir = os.path.dirname(moduleFilename)
                packageImportPrefix = packagePrefix
            file, path, description = imp.find_module(moduleName, [moduleDir])
            if file or path:
                try:
                    try:
                        module = imp.load_module(packagePrefix + moduleName, file, path, description)
                        pluginInfo = module.__pluginInfo__.copy()
                        elementSubstitutionClasses = None
                        if name == pluginInfo.get('name'):
                            pluginInfo['moduleURL'] = moduleURL
                            modulePluginInfos[name] = pluginInfo
                            if 'localeURL' in pluginInfo:
                                localeDir = os.path.dirname(module.__file__) + os.sep + pluginInfo['localeURL']
                                try:
                                    _gettext = gettext.translation(pluginInfo['localeDomain'], localeDir, getLanguageCodes())
                                except IOError:
                                    _gettext = lambda x: x

                            else:
                                _gettext = lambda x: x
                            for key, value in pluginInfo.items():
                                if key == 'name':
                                    if name:
                                        pluginConfig['modules'][name] = moduleInfo
                                    elif isinstance(value, types.FunctionType):
                                        classModuleNames = pluginConfig['classes'].setdefault(key, [])
                                        if name:
                                            if name not in classModuleNames:
                                                classModuleNames.append(name)
                                    if key == 'ModelObjectFactory.ElementSubstitutionClasses':
                                        elementSubstitutionClasses = value

                            module._ = _gettext
                            pluginConfigChanged = True
                        if elementSubstitutionClasses:
                            try:
                                from arelle.ModelObjectFactory import elementSubstitutionModelClass
                                elementSubstitutionModelClass.update(elementSubstitutionClasses)
                            except Exception as err:
                                _msg = _('Exception loading plug-in {name}: processing ModelObjectFactory.ElementSubstitutionClasses').format(name=name,
                                  error=err)
                                if PLUGIN_TRACE_FILE:
                                    with open(PLUGIN_TRACE_FILE, 'at', encoding='utf-8') as (fh):
                                        fh.write(_msg + '\n')
                                else:
                                    print(_msg, file=(sys.stderr))

                        for importModuleInfo in moduleInfo.get('imports', EMPTYLIST):
                            loadModule(importModuleInfo, packageImportPrefix)

                    except (ImportError, AttributeError, SystemError) as err:
                        _msg = _('Exception loading plug-in {name}: {error}\n{traceback}').format(name=name,
                          error=err,
                          traceback=(traceback.format_tb(sys.exc_info()[2])))
                        if PLUGIN_TRACE_FILE:
                            with open(PLUGIN_TRACE_FILE, 'at', encoding='utf-8') as (fh):
                                fh.write(_msg + '\n')
                        else:
                            print(_msg, file=(sys.stderr))

                finally:
                    if file:
                        file.close()

        except (EnvironmentError, ImportError, NameError, SyntaxError) as err:
            _msg = _('Exception finding plug-in {name}: {error}').format(name=name, error=err)
            if PLUGIN_TRACE_FILE:
                with open(PLUGIN_TRACE_FILE, 'at', encoding='utf-8') as (fh):
                    fh.write(_msg + '\n')
            else:
                print(_msg, file=(sys.stderr))


def pluginClassMethods(className):
    if pluginConfig:
        try:
            pluginMethodsForClass = pluginMethodsForClasses[className]
        except KeyError:
            pluginMethodsForClass = []
            modulesNamesLoaded = set()
            if className in pluginConfig['classes']:
                for moduleName in pluginConfig['classes'].get(className):
                    if moduleName:
                        if moduleName in pluginConfig['modules']:
                            if moduleName not in modulesNamesLoaded:
                                modulesNamesLoaded.add(moduleName)
                                moduleInfo = pluginConfig['modules'][moduleName]
                                if moduleInfo['status'] == 'enabled':
                                    if moduleName not in modulePluginInfos:
                                        loadModule(moduleInfo)
                        if moduleName in modulePluginInfos:
                            pluginInfo = modulePluginInfos[moduleName]
                            if className in pluginInfo:
                                pluginMethodsForClass.append(pluginInfo[className])

            pluginMethodsForClasses[className] = pluginMethodsForClass

        for method in pluginMethodsForClass:
            yield method


def addPluginModule(url):
    global pluginConfigChanged
    moduleInfo = moduleModuleInfo(url)
    if moduleInfo:
        if moduleInfo.get('name'):
            name = moduleInfo['name']
            removePluginModule(name)

            def _addPluginModule(moduleInfo):
                _name = moduleInfo.get('name')
                if _name:
                    for classMethod in moduleInfo['classMethods']:
                        classMethods = pluginConfig['classes'].setdefault(classMethod, [])
                        _name = moduleInfo['name']
                        if _name and _name not in classMethods:
                            classMethods.append(_name)

                    for importModuleInfo in moduleInfo.get('imports', EMPTYLIST):
                        _addPluginModule(importModuleInfo)

                    pluginConfig['modules'][_name] = moduleInfo

            _addPluginModule(moduleInfo)
            pluginConfigChanged = True
            return moduleInfo


def reloadPluginModule(name):
    if name in pluginConfig['modules']:
        url = pluginConfig['modules'][name].get('moduleURL')
        if url:
            moduleInfo = moduleModuleInfo(url, reload=True)
            if moduleInfo:
                addPluginModule(url)
                return True
    return False


def removePluginModule(name):
    global pluginConfigChanged
    moduleInfo = pluginConfig['modules'].get(name)
    if moduleInfo and name:

        def _removePluginModule(moduleInfo):
            _name = moduleInfo.get('name')
            if _name:
                for classMethod in moduleInfo['classMethods']:
                    classMethods = pluginConfig['classes'].get(classMethod)
                    if classMethods and _name and _name in classMethods:
                        classMethods.remove(_name)
                        if not classMethods:
                            del pluginConfig['classes'][classMethod]

                for importModuleInfo in moduleInfo.get('imports', EMPTYLIST):
                    _removePluginModule(importModuleInfo)

                del pluginConfig['modules'][_name]

        _removePluginModule(moduleInfo)
        pluginConfigChanged = True
        return True
    else:
        return False