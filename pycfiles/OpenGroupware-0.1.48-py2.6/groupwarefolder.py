# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/coils/protocol/dav/groupware/groupwarefolder.py
# Compiled at: 2012-10-12 07:02:39
import hashlib, urlparse, urllib
from coils.core import *
from coils.core.vcard import Parser as VCard_Parser
from coils.core.icalendar import Parser as VEvent_Parser
from coils.net import DAVObject, DAVFolder, OmphalosCollection, OmphalosObject, StaticObject
from teamobject import TeamObject
from taskobject import TaskObject
from eventobject import EventObject
from contactobject import ContactObject
ENTITY_REPRESENTATION_DICT = {'Appointment': EventObject, 'Contact': ContactObject, 
   'Task': TaskObject, 
   'Team': TeamObject}

class GroupwareFolder(object):

    def get_ctag_for_entity(self, entity):
        """ Return a ctag appropriate for this object.
            Actual WebDAV objects should override this method """
        db = self.context.db_session()
        query = db.query(CTag).filter(CTag.entity == entity)
        ctags = query.all()
        if len(ctags) == 0:
            return
        else:
            query = None
            return ctags[0].ctag

    def get_ctag_for_collection(self):
        if self.load_contents():
            m = hashlib.md5()
            for entry in self.get_children():
                m.update(('{0}:{1}').format(entry.object_id, entry.version))

            return m.hexdigest()
        else:
            return

    def get_ctag_representation(self, ctag):
        return StaticObject(self, '.ctag', context=self.context, request=self.request, payload=ctag, mimetype='text/plain')

    @property
    def is_favorites_folder(self):
        if self.parent.__class__.__name__ == 'FavoritesFolder':
            return True
        return False

    @property
    def is_project_folder(self):
        if hasattr(self, 'entity'):
            if self.entity.__entityName__ == 'Project':
                return True
        return False

    @property
    def is_child_folder(self):
        if self.parent.__class__ == self.__class__:
            return True
        return False

    @property
    def is_collection_folder(self):
        if self.is_favorites_folder or self.is_project_folder or self.is_child_folder:
            return True
        return False

    def inspect_name(self, name, default_format='ics'):
        extension = name.split('.')[-1:][0]
        if extension == name:
            extension = None
        if extension:
            format = extension.lower()
            if format in ('ics', 'vjl', 'json', 'xml', 'yaml'):
                uid = name[:-len(format)]
            else:
                format = default_format
                uid = name
        if uid.isdigit():
            numeric = True
        else:
            numeric = False
        if uid.isdigit():
            object_id = int(uid)
        else:
            object_id = None
        return (
         format, extension, uid, numeric)

    def name_has_format_key(self, name):
        if name[-4:] == '.vcf' or name[-5:] == '.json' or name[-4:] == '.xml' or name[-4:] == '.ics' or name[-5:] == '.yaml':
            return True
        return False

    def get_format_key_from_name(self, name):
        if name[-4:] == '.vcf':
            return 'vcf'
        if name[-4:] in ('.ics', '.vjl'):
            return 'ics'
        if name[-5:] == '.json':
            return 'json'
        if name[-4:] == '.xml':
            return 'xml'
        if name[-5:] == '.yaml':
            return 'yaml'
        raise NotImplementedException(('Unimplemented representation "{0}" encountered.').format(name))

    def get_dav_form_of_name(self, name, extension='vcf'):
        return ('{0}.{1}').format(self.get_object_id_from_name(name), extension)

    def get_object_id_from_name(self, name):
        parts = name.split('.')
        if len(parts) == 2:
            if parts[0].isdigit():
                return int(parts[0])
        return

    def name_is_coils_key(self, name):
        parts = name.split('.')
        if len(parts) == 2:
            if self.get_object_id_from_name(name) is not None and self.name_has_format_key(name):
                return True
        return False

    def get_contact_for_key(self, key):
        return self.get_contact_for_key_and_content(key, None)

    def get_contact_for_key_and_content(self, key, payload):
        contact = None
        object_id = None
        payload_values = None
        payload_format = None
        if self.name_is_coils_key(key):
            object_id = self.get_object_id_from_name(key)
            payload_format = self.get_format_key_from_name(key)
        else:
            payload_format = 'vcf'
        if payload is not None:
            if len(payload) > 15:
                if payload_format == 'vcf':
                    payload_values = VCard_Parser.Parse(payload, self.context, entity_name='Contact')
                    if isinstance(payload_values, list):
                        payload_values = payload_values[0]
                elif payload_format == 'json':
                    raise NotImplementedException()
                elif payload_format == 'xml':
                    raise NotImplementedException()
                elif payload_format == 'yaml':
                    raise NotImplementedException()
                else:
                    raise CoilsException(('Format {0} not support for Contact entities').format(payload_format))
                if object_id is None and payload_values is not None and 'object_id' in payload_values:
                    object_id = payload_values.get('object_id')
        if object_id is not None:
            contact = self.context.run_command('contact::get', id=object_id)
        else:
            contact = self.context.run_command('contact::get', uid=key)
        return (
         object_id, payload_format, contact, payload_values)

    def get_appointment_for_key(self, key):
        return self.get_appointment_for_key_and_content(key, None)

    def get_appointment_for_key_and_content(self, key, payload):
        appointment = None
        object_id = None
        payload_values = None
        payload_format = None
        if self.name_is_coils_key(key):
            object_id = self.get_object_id_from_name(key)
            payload_format = self.get_format_key_from_name(key)
            appointment = self.context.run_command('appointment::get', id=object_id)
        else:
            payload_format = 'ics'
            appointment = self.context.run_command('appointment::get', uid=key)
            if appointment is not None:
                object_id = appointment.object_id
        if payload is not None:
            if len(payload) > 15:
                if payload_format == 'ics':
                    payload_values = VEvent_Parser.Parse(payload, self.context)
                    if len(payload_values) > 0:
                        object_id = payload_values[0].get('object_id', None)
                        if object_id is not None:
                            payload_values = payload_values[0]
                            appointment = self.context.run_command('appointment::get', id=object_id)
                elif payload_format == 'json':
                    raise NotImplementedException()
                elif payload_format == 'xml':
                    raise NotImplementedException()
                elif payload_format == 'yaml':
                    raise NotImplementedException()
                else:
                    raise CoilsException(('Format {0} not support for Contact entities').format(payload_format))
        return (
         object_id, payload_format, appointment, payload_values)

    def get_process_for_key(self, key):
        process = None
        object_id = None
        if self.name_is_coils_key(key):
            object_id = self.get_object_id_from_name(key)
            payload_format = self.get_format_key_from_name(key)
            process = self.context.run_command('process::get', id=object_id)
        return (
         object_id, 'ics', process, None)

    def get_task_for_key(self, key):
        return self.get_task_for_key_and_content(key, None)

    def get_task_for_key_and_content(self, key, payload):
        task = None
        object_id = None
        payload_values = None
        payload_format = None
        if self.name_is_coils_key(key):
            object_id = self.get_object_id_from_name(key)
            payload_format = self.get_format_key_from_name(key)
            task = self.context.run_command('task::get', id=object_id)
        else:
            payload_format = 'ics'
            task = self.context.run_command('task::get', uid=key)
            if task is not None:
                object_id = task.object_id
        if payload is not None:
            if len(payload) > 15:
                if payload_format == 'ics':
                    payload_values = VEvent_Parser.Parse(payload, self.context)
                    if len(payload_values) > 0:
                        object_id = payload_values[0].get('object_id', None)
                        if object_id is not None:
                            payload_values = payload_values[0]
                            task = self.context.run_command('task::get', id=object_id)
                elif payload_format == 'json':
                    raise NotImplementedException()
                elif payload_format == 'xml':
                    raise NotImplementedException()
                elif payload_format == 'yaml':
                    raise NotImplementedException()
                else:
                    raise CoilsException(('Format {0} not support for Task entities').format(payload_format))
        return (
         object_id, payload_format, task, payload_values)

    def get_note_for_key_and_content(self, key, payload):
        note = None
        object_id = None
        payload_values = None
        payload_format = None
        if self.name_is_coils_key(key):
            object_id = self.get_object_id_from_name(key)
            payload_format = self.get_format_key_from_name(key)
            note = self.context.run_command('note::get', id=object_id)
        else:
            payload_format = 'ics'
            note = self.context.run_command('note::get', uid=key)
            if note is not None:
                object_id = note.object_id
        if payload is not None:
            if len(payload) > 15:
                if payload_format == 'ics':
                    payload_values = VEvent_Parser.Parse(payload, self.context)
                    if len(payload_values) > 0:
                        object_id = payload_values[0].get('object_id', None)
                        if object_id is not None:
                            payload_values = payload_values[0]
                            note = self.context.run_command('note::get', id=object_id)
                elif payload_format == 'json':
                    raise NotImplementedException()
                elif payload_format == 'xml':
                    raise NotImplementedException()
                elif payload_format == 'yaml':
                    raise NotImplementedException()
                else:
                    raise CoilsException(('Format {0} not support for Note entities').format(payload_format))
        return (
         object_id, payload_format, note, payload_values)

    def get_entity_representation(self, name, entity, representation=None, is_webdav=False, location=None):
        if not is_webdav:
            if representation is None:
                representation = self.get_format_key_from_name(name)
        if is_webdav or representation in ('ics', 'vcf'):
            reprclass = ENTITY_REPRESENTATION_DICT.get(entity.__entityName__, DAVObject)
            return reprclass(self, name, location=location, entity=entity, context=self.context, request=self.request)
        else:
            if representation in ('json', 'yaml', 'xml'):
                return OmphalosObject(self, name, entity=entity, context=self.context, request=self.request)
            raise CoilsException('Unknown representation requested')
            return

    def get_collection_representation(self, name, collection, rendered=False):
        return OmphalosCollection(self, name, rendered=rendered, data=collection, context=self.context, request=self.request)

    def move_helper(self, name):
        """ MOVE /dav/Projects/Application%20-%20BIE/Documents/87031000 HTTP/1.1
            Content-Length: 0
            Destination: http://172.16.54.1:8080/dav/Projects/Application%20-%20BIE/Documents/%5B%5DSheet1
            Overwrite: T
            translate: f
            User-Agent: Microsoft-WebDAV-MiniRedir/6.0.6001
            Host: 172.16.54.1:8080
            Connection: Keep-Alive
            Authorization: Basic YWRhbTpmcmVkMTIz

            RESPONSE
               201 (Created) - Created a new resource
               204 (No Content) - Moved to an existing resource
               403 (Forbidden) - The source and destination URIs are the same.
               409 - Conflict
               412 - Precondition failed
               423 - Locked
               502 - Bad Gateway
            """
        source = self.object_for_key(name)
        overwrite = self.request.headers.get('Overwrite', 'F').upper()
        if overwrite == 'T':
            overwrite = True
        else:
            overwrite = False
        destination = self.request.headers.get('Destination')
        destination = urlparse.urlparse(destination).path
        destination = urllib.unquote(destination)
        if not destination.startswith('/dav/'):
            raise CoilsException('MOVE cannot be performed across multiple DAV roots')
        destination = destination.split('/', 64)[2:]
        target_name = destination[-1:][0]
        target_path = destination[:-1]
        destination = None
        target = self.root
        try:
            for component in target_path:
                target = target.object_for_key(component)

        except:
            pass

        self.log.debug(('Request to move "{0}" to "{1}" as "{2}".').format(source, target, target_name))
        return (
         source, target, target_name, overwrite)