# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/coils/protocol/dav/groupware/processcalendar.py
# Compiled at: 2012-10-12 07:02:39
from StringIO import StringIO
from datetime import datetime, timedelta
from coils.foundation import CTag, ServerDefaultsManager
from coils.core import *
import coils.core.icalendar
from coils.net import DAVFolder, OmphalosCollection, OmphalosObject, Parser, Multistatus_Response
from groupwarefolder import GroupwareFolder
from eventobject import EventObject

class ProcessCalendarFolder(DAVFolder, GroupwareFolder):

    def __init__(self, parent, name, **params):
        DAVFolder.__init__(self, parent, name, **params)
        self._start = None
        self._end = None
        return

    def supports_PUT(self):
        return False

    def supports_DELETE(self):
        return True

    def supports_REPORT(self):
        return True

    def _get_process_range(self, **params):
        events = self.context.run_command('process::get-range', **params)
        return events

    def get_property_webdav_owner(self):
        return ('<D:href>/dav/Contacts/{0}.vcf</D:href>').format(self.context.account_id)

    def get_property_webdav_resourcetype(self):
        return '<D:collection/><C:calendar/><G:vevent-collection/>'

    def get_property_caldav_getctag(self):
        return self.get_ctag()

    def get_ctag(self):
        return self.get_ctag_for_entity('Process')

    def get_property_caldav_calendar_description(self):
        return ''

    def get_property_caldav_supported_calendar_component_set(self):
        return unicode('<C:comp name="VEVENT"/>')

    @property
    def is_collection_folder(self):
        return False

    def _load_contents(self):
        self.log.info(('Loading content in calendar folder for name {0}').format(self.name))
        if self._start is None:
            self._start = datetime.now() - timedelta(days=90)
        if self._end is None:
            self._end = datetime.now() + timedelta(days=30)
        events = self._get_process_range(start=self._start, end=self._end, visible_only=True)
        for event in events:
            self.insert_child(event.object_id, event, alias=('{0}.ics').format(event.object_id))

        return True

    def object_for_key(self, name, auto_load_enabled=True, is_webdav=False):
        if name == '.ctag':
            return self.get_ctag_representation(self.get_ctag_for_entity('Process'))
        else:
            (object_id, payload_format, entity, values) = self.get_process_for_key(name)
            if entity is not None:
                return EventObject(self, name, entity=entity, context=self.context, request=self.request)
            self.log.debug(('No such path for key {0}').format(name))
            self.no_such_path()
            return

    def do_OPTIONS(self):
        """ Return a valid WebDAV OPTIONS response """
        methods = ['OPTIONS, GET, HEAD, DELETE, TRACE',
         'PROPFIND, PROPPATCH, REPORT, ACL']
        self.request.simple_response(200, data=None, mimetype='text/plain', headers={'DAV': '1, 2, access-control, calendar-access', 'Allow': (',').join(methods), 
           'Connection': 'close', 
           'MS-Author-Via': 'DAV'})
        return

    def do_REPORT(self):
        """ Preocess a report request """
        payload = self.request.get_request_payload()
        self.log.debug('REPORT REQUEST: %s' % payload)
        parser = Parser.report(payload, self.context.user_agent_description)
        if parser.report_name == 'calendar-query':
            self._start = parser.parameters.get('start', None)
            self._end = parser.parameters.get('end', None)
            resources = []
            if self.load_contents():
                for child in self.get_children():
                    name = ('{0}.ics').format(child.object_id)
                    resources.append(EventObject(self, name, entity=child, context=self.context, request=self.request))

                stream = StringIO()
                (properties, namespaces) = parser.properties
                Multistatus_Response(resources=resources, properties=properties, namespaces=namespaces, stream=stream)
                self.request.simple_response(207, data=stream.getvalue(), mimetype='text/xml; charset="utf-8"')
        elif parser.report_name == 'calendar-multiget':
            resources = []
            self.log.debug('calendar-multiget')
            for href in parser.references:
                self.log.debug(('href: {0}').format(href))
                key = href.split('/')[(-1)]
                try:
                    entity = self.get_object_for_key(key)
                    self.log.debug(entity)
                    resources.append(entity)
                except NoSuchPathException, e:
                    self.log.debug(('Missing resource {0} in collection').format(key))
                except Exception, e:
                    self.log.exception(e)
                    raise e

            stream = StringIO()
            (properties, namespaces) = parser.properties
            Multistatus_Response(resources=resources, properties=properties, namespaces=namespaces, stream=stream)
            self.request.simple_response(207, data=stream.getvalue(), mimetype='text/xml; charset="utf-8"')
        else:
            raise CoilsException(('Unsupported report {0} in {1}').format(parser.report_name, self))
        return

    def apply_permissions(self, appointment):
        pass