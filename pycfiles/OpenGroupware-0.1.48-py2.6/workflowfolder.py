# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/coils/protocol/dav/workflow/workflowfolder.py
# Compiled at: 2012-10-12 07:02:39
from coils.core import Process
from coils.net import DAVFolder, EmptyFolder, OmphalosCollection
from routesfolder import RoutesFolder
from formatsfolder import FormatsFolder
from mapsfolder import MapsFolder
from tablesfolder import TablesFolder
from loadschedule import LoadScheduleObject
from schedulefolder import ScheduleFolder
from xsdfolder import XSDFolder
from xsltfolder import XSLTFolder
from wsdlfolder import WSDLFolder

class WorkflowFolder(DAVFolder):

    def __init__(self, parent, name, **params):
        DAVFolder.__init__(self, parent, name, **params)

    def _load_contents(self):
        self.insert_child('Routes', None)
        self.insert_child('Formats', None)
        self.insert_child('Schedule', None)
        (self.insert_child('Maps', None),)
        self.insert_child('XSD', None)
        self.insert_child('Tables', None)
        self.insert_child('WSDL', None)
        self.insert_child('XSLT', None)
        return True

    def object_for_key(self, name, auto_load_enabled=True, is_webdav=False):
        if name == 'Routes':
            return RoutesFolder(self, name, parameters=self.parameters, request=self.request, context=self.context)
        else:
            if name == 'LoadSchedule.txt':
                return LoadScheduleObject(self, name, parameters=self.parameters, request=self.request, context=self.context)
            if name == 'Formats':
                return FormatsFolder(self, name, parameters=self.parameters, request=self.request, context=self.context)
            if name == 'Schedule':
                return ScheduleFolder(self, name, parameters=self.parameters, request=self.request, context=self.context)
            if name == 'Maps':
                return MapsFolder(self, name, parameters=self.parameters, request=self.request, context=self.context)
            if name == 'Tables':
                return TablesFolder(self, name, parameters=self.parameters, request=self.request, context=self.context)
            if name == 'XSD':
                return XSDFolder(self, name, parameters=self.parameters, request=self.request, context=self.context)
            if name == 'XSLT':
                return XSLTFolder(self, name, parameters=self.parameters, request=self.request, context=self.context)
            if name == 'WSDL':
                return WSDLFolder(self, name, parameters=self.parameters, request=self.request, context=self.context)
            if name == '.ps':
                import pprint
                pprint.pprint(self.parameters)
                route_group = self.parameters.get('routegroup', None)
                if route_group:
                    route_group = route_group[0]
                if 'all' in self.parameters:
                    if route_group:
                        ps = self.context.run_command('process::list', properties=[Process])
                    else:
                        ps = self.context.run_command('process::list', properties=[Process], route_group=route_group)
                else:
                    ps = self.context.run_command('process::get', route_group=route_group)
                if 'detail' in self.parameters and len(self.parameters['detail']):
                    detail_level = int(self.parameters['detail'][0])
                else:
                    detail_level = 63487
                return OmphalosCollection(self, name, detailLevel=detail_level, rendered=True, data=ps, parameters=self.parameters, context=self.context, request=self.request)
            return self.no_such_path()