# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/coils/protocol/dav/groupware/birthdayfolder.py
# Compiled at: 2012-10-12 07:02:39
from coils.core import *
from coils.net import DAVFolder, OmphalosCollection, OmphalosObject, Parser, Multistatus_Response
from groupwarefolder import GroupwareFolder

class BirthdayFolder(DAVFolder, GroupwareFolder):

    def __init__(self, parent, name, **params):
        DAVFolder.__init__(self, parent, name, **params)
        self._start = None
        self._end = None
        return

    def supports_REPORT(self):
        return True

    def get_property_webdav_owner(self):
        return ('<D:href>/dav/Contacts/{0}.vcf</D:href>').format(self.context.account_id)

    def get_property_webdav_resourcetype(self):
        return '<D:collection/><C:calendar/><G:vevent-collection/>'

    def get_property_caldav_getctag(self):
        return 'fred'

    def get_property_caldav_calendar_description(self):
        return unicode('Birthdays')

    def get_property_caldav_supported_calendar_component_set(self):
        return unicode('<C:comp name="VEVENT"/>')

    def _load_contents(self):
        contacts = self.context('contact::get-upcoming-birthdays')
        for contact in contacts:
            n = ('b{0}.ics').format(contact.object_id)
            x = DateObject(self, name, entity=entity, comment='', title=n, context=self.context, request=self.request)
            self.insert_child(n, x)

        return True

    def object_for_key(self, name, auto_load_enabled=True, is_webdav=False):
        if self.load_contents():
            entity = self.get_child(name)
            if entity is not None:
                return entity
        self.no_such_path()
        return

    def do_OPTIONS(self):
        """ Return a valid WebDAV OPTIONS response """
        methods = [
         'OPTIONS', 'GET', 'HEAD', 'PROPFIND', 'PROPPATCH', 'REPORT', 'ACL']
        self.request.simple_response(200, data=None, mimetype='text/plain', headers={'DAV': '1, 2, access-control, calendar-access', 'Allow': (',').join(methods), 
           'Connection': 'close', 
           'MS-Author-Via': 'DAV'})
        return

    def do_REPORT(self):
        """ Preocess a report request """
        payload = self.request.get_request_payload()
        self.log.debug('REPORT REQUEST: %s' % payload)
        parser = Parser.report(payload)
        if parser.report_name == 'calendar-query':
            self._start = parser.parameters.get('start', None)
            self._end = parser.parameters.get('end', None)
            resources = []
            if self.load_contents():
                for child in self.get_children():
                    if child.caldav_uid is None:
                        name = ('{0}.ics').format(child.object_id)
                    else:
                        name = child.caldav_uid
                    resources.append(EventObject(self, name, entity=child, location=('/dav/Calendar/{0}.ics').format(child.object_id), context=self.context, request=self.request))

                stream = StringIO()
                (properties, namespaces) = parser.properties
                Multistatus_Response(resources=resources, properties=properties, namespaces=namespaces, stream=stream)
                self.request.simple_response(207, data=stream.getvalue(), mimetype='text/xml; charset="utf-8"')
        elif parser.report_name == 'calendar-multiget':
            if self.load_contents():
                resources = []
                for href in parser.references:
                    key = href.split('/')[(-1)]
                    try:
                        entity = self.get_object_for_key(key)
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