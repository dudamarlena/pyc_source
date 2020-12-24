# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/coils/protocol/dav/groupware/journalfolder.py
# Compiled at: 2012-10-12 07:02:39
import urllib
from StringIO import StringIO
from coils.core import NoSuchPathException
from coils.core.icalendar import Parser as ICS_Parser
from coils.net import DAVFolder, Parser, BufferedWriter, Multistatus_Response
from noteobject import NoteObject

class JournalFolder(DAVFolder):

    def __init__(self, parent, name, **params):
        DAVFolder.__init__(self, parent, name, **params)

    def get_property_webdav_resourcetype(self):
        return unicode('<D:collection/><C:calendar/>')

    def get_property_caldav_supported_calendar_component_set(self):
        return unicode('<C:comp name="VJOURNAL"/>')

    def supports_PUT(self):
        return True

    def _get_journal_project(self):
        raise NotImplementedException('')
        return

    def _get_journal_folder(self):
        raise NotImplementedException('')
        return

    def _load_contents(self):
        project = self._get_journal_project()
        notes = self.context.run_command('folder::ls', id=folder.object_id)
        if self.request.user_agent.supports_memos:
            for note in notes:
                if note.kind == 'txt':
                    if note.caldav_uid is None:
                        print ('memoId#{0} has no alias').format(note.object_id)
                        self.insert_child(note.object_id, note, alias=('{0}.vjl').format(note.object_id))
                    else:
                        print ('memoId#{0} has alias {1}').format(note.object_id, note.caldav_uid)
                        self.insert_child(note.object_id, note, alias=note.caldav_uid)

        else:
            for note in notes:
                if note.kind == 'txt':
                    self.insert_child(note.title, note)
                elif note.kind == 'ini':
                    self.insert_child(note.title, note)

            return True

    def object_for_key(self, name, auto_load_enabled=True, is_webdav=False):
        if self.load_contents():
            if self.has_child(name):
                return NoteObject(self, name, entity=self.get_child(name), request=self.request, context=self.context)
        self.no_such_path()

    def do_OPTIONS(self):
        """ Return a valid WebDAV OPTIONS response """
        methods = [
         'OPTIONS, GET, HEAD, POST, PUT, DELETE, TRACE, COPY, MOVE',
         'PROPFIND, PROPPATCH, LOCK, UNLOCK, REPORT, ACL']
        self.request.simple_response(200, data=None, mimetype='text/plain', headers={'DAV': '1, 2, access-control, calendar-access', 'Allow': (',').join(methods), 
           'Connection': 'close', 
           'MS-Author-Via': 'DAV'})
        return

    def do_PUT(self, request_name):
        folder = self._get_journal_folder()
        mimetype = self.request.headers.get('CONTENT-TYPE', 'text/plain').split(';')[0].lower()
        if self.load_contents():
            self.log.debug(('Requested label is {0}.').format(request_name))
            payload = self.request.get_request_payload()
            if mimetype == 'text/calendar':
                values = ICS_Parser.Parse(payload, self.context)[0]
                if 'object_id' in values:
                    note = self.context.run_command('note::get', id=values['object_id'])
                elif self.has_child(request_name):
                    note = self.get_child(request_name)
                else:
                    note = None
            else:
                values = None
                if self.has_child(request_name):
                    note = self.get_child(request_name)
                else:
                    note = None
            if note is None:
                print '___CREATE____'
                if values is None:
                    note = self.context.run_command('note::new', values={'title': request_name}, text=payload)
                else:
                    note = self.context.run_command('note::new', values=values, context=self.entity)
                    print ('setting caldav_uid = {0}').format(request_name)
                    note.caldav_uid = request_name
                self.request.simple_response(201, data=None, mimetype=('{0}; charset=utf-8').format(mimetype), headers={'Etag': ('{0}:{1}').format(note.object_id, note.version)})
            else:
                print '___UPDATE____'
                if values is None:
                    note = self.context.run_command('note::set', object=note, context=self.entity, text=payload)
                else:
                    note = self.context.run_command('note::set', object=note, context=self.entity, values=values)
            self.context.commit()
            self.request.simple_response(204, data=None, mimetype=('{0}; charset=utf-8').format(mimetype), headers={'Etag': ('{0}:{1}').format(note.object_id, note.version)})
        return

    def do_REPORT(self):
        folder = self._get_journal_folder()
        payload = self.request.get_request_payload()
        self.log.debug('REPORT REQUEST: %s' % payload)
        parser = Parser.report(payload)
        if parser.report_name == 'calendar-query':
            self._start = parser.parameters.get('start', None)
            self._end = parser.parameters.get('end', None)
            if self.load_contents():
                resources = []
                for note in self.get_children():
                    if note.caldav_uid is None:
                        name = ('{0}.vjl').format(note.object_id)
                    else:
                        name = note.caldav_uid
                    resources.append(NoteObject(self, name, entity=note, request=self.request, context=self.context))

                stream = StringIO()
                (properties, namespaces) = parser.properties
                Multistatus_Response(resources=resources, properties=properties, namespaces=namespaces, stream=stream)
                self.request.simple_response(207, data=stream.getvalue(), mimetype='text/xml; charset="utf-8"', headers={})
        elif parser.report_name == 'calendar-multiget':
            resources = []
            self._start = parser.parameters.get('start', None)
            self._end = parser.parameters.get('end', None)
            for href in parser.references:
                key = href.split('/')[(-1)]
                try:
                    resources.append(self.get_object_for_key(key))
                except NoSuchPathException, e:
                    self.log.debug(('Missing resource {0} in collection').format(key))
                except Exception, e:
                    self.log.exception(e)
                    raise e

            stream = StringIO()
            (properties, namespaces) = parser.properties
            Multistatus_Response(resources=resources, properties=properties, namespaces=namespaces, stream=stream)
            self.request.simple_response(207, data=stream.getvalue(), mimetype='text/xml; charset="utf-8"', headers={})
        else:
            raise CoilsException(('Unsupported report {0} in {1}').format(parser.report_name, self))
        return

    def do_DELETE(self, name):
        folder = self._get_journal_folder()
        if self.load_contents():
            if self.has_child(name):
                self.context.run_command('contact::delete', object=self.get_child(name))
                self.context.commit()
                self.request.simple_response(204, data=None, mimetype=self.entity.get_mimetype(), headers={})
            else:
                self.no_such_path()
        else:
            raise CoilsException('Unable to enumerate collection contents.')
        return