# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/coils/protocol/dav/groupware/contactsfolder.py
# Compiled at: 2012-10-12 07:02:39
import sys, coils.core, time
from StringIO import StringIO
from coils.core import *
from coils.core.vcard import Parser as VCard_Parser
from coils.foundation import CTag, Contact
from coils.net import DAVFolder, DAVObject, OmphalosCollection, OmphalosObject
from groupwarefolder import GroupwareFolder

class ContactsFolder(DAVFolder, GroupwareFolder):

    def __init__(self, parent, name, **params):
        DAVFolder.__init__(self, parent, name, **params)

    def __repr__(self):
        return ('<ContactsFolder name="{0}" projectMode="{1}" favoriteMode="{2}"/>').format(self.name, self.is_project_folder, self.is_favorites_folder)

    def supports_GET(self):
        return False

    def supports_POST(self):
        return False

    def supports_PUT(self):
        return True

    def supports_DELETE(self):
        return True

    def supports_PROPFIND(self):
        return True

    def supports_PROPATCH(self):
        return False

    def supports_MKCOL(self):
        return False

    def get_property_unknown_getctag(self):
        return self.get_property_caldav_getctag()

    def get_property_webdav_getctag(self):
        return self.get_property_caldav_getctag()

    def get_property_caldav_getctag(self):
        return self.get_ctag()

    def get_ctag(self):
        if self.is_collection_folder:
            return self.get_ctag_for_collection()
        else:
            return self.get_ctag_for_entity('Person')

    def _load_contents(self):
        if self.is_project_folder:
            content = self.context.run_command('project::get-contacts', object=self.entity)
        elif self.is_favorites_folder:
            content = self.context.run_command('contact::get-favorite')
        else:
            content = self.context.run_command('contact::list', properties=[Contact])
        if len(content) > 0:
            for contact in content:
                if contact.carddav_uid is None:
                    self.insert_child(contact.object_id, contact, alias=('{0}.vcf').format(contact.object_id))
                else:
                    self.insert_child(contact.object_id, contact, alias=contact.carddav_uid)

        else:
            self.empty_content()
        return True

    def object_for_key(self, name, auto_load_enabled=True, is_webdav=False):
        if name == '.ctag':
            return self.get_ctag_representation(self.get_ctag())
        else:
            if name in ('.json', '.ls') and self.load_contents():
                return self.get_collection_representation(name, self.get_children())
            if name == '.birthdays.json':
                results = self.context.run_command('contact::get-upcoming-birthdays')
                return self.get_collection_representation(name, results, rendered=True)
            if self.is_collection_folder:
                if auto_load_enabled:
                    self.load_contents()
                if self.is_loaded:
                    contact = self.get_child(name)
                    if contact is not None:
                        location = ('/dav/Contacts/{0}').format(name)
            else:
                location = None
                if self.is_loaded:
                    contact = self.get_child(name)
                else:
                    (object_id, payload_format, contact, values) = self.get_contact_for_key(name)
            if contact is not None:
                return self.get_entity_representation(name, contact, location=location, is_webdav=is_webdav)
            self.no_such_path()
            return

    def apply_permissions(self, contact):
        pass

    def do_PUT(self, name):
        payload = self.request.get_request_payload()
        (object_id, payload_format, contact, payload_values) = self.get_contact_for_key_and_content(name, payload)
        if_etag = self.request.headers.get('If-Match', None)
        if if_etag is None:
            self.log.warn('Client issued a put operation with no If-Match!')
        else:
            self.log.warn(('If-Match test not implemented at {0}').format(self.url))
        if payload_values:
            if object_id is None:
                contact = self.context.run_command('contact::new', values=payload_values)
                contact.carddav_uid = name
                self.apply_permissions(contact)
                if self.is_favorites_folder:
                    self.context.run_command('contact::add-favorite', id=contact.object_id)
                elif self.is_project_folder:
                    self.context.run_command('project::assign-contact', project=project, contact_id=object_id)
                    raise NotImplementedException('Creating contacts via a project folder is not implemented.')
                self.context.commit()
                self.request.simple_response(201, data=None, mimetype='text/x-vcard; charset=utf-8', headers={'Etag': ('{0}:{1}').format(contact.object_id, contact.version), 'Location': ('/dav/Contacts/{0}.ics').format(contact.object_id)})
            else:
                try:
                    contact = self.context.run_command('contact::set', object=contact, values=payload_values)
                    if self.is_favorites_folder:
                        self.context.run_command('contact::add-favorite', id=contact.object_id)
                    elif self.is_project_folder:
                        self.context.run_command('project::assign-contact', project=project, contact_id=object_id)
                except Exception, e:
                    self.log.error(('Error updating objectId#{0} via WebDAV').format(object_id))
                    self.log.exception(e)
                    raise e
                else:
                    self.context.commit()
                    self.request.simple_response(204, data=None, mimetype='text/x-vcard; charset=utf-8', headers={'Etag': ('{0}:{1}').format(contact.object_id, contact.version), 'Location': ('/dav/Contacts/{0}.ics').format(contact.object_id)})
        return

    def do_DELETE(self, name):
        if self.is_favorites_folder and self.load_contents():
            contact = self.get_child(name)
        else:
            (object_id, payload_format, contact, values) = self.get_contact_for_key(name)
        if contact is None:
            self.no_such_path()
        try:
            if self.is_favorites_folder:
                self.log.debug(('Removing favorite status from contactId#{0} for userId#{1}').format(contact.object_id, self.context.account_id))
                self.context.run_command('contact::remove-favorite', id=contact.object_id)
            elif self.is_project_folder:
                self.context.run_command('project::unassign-contact', project=project, contact_id=object_id)
            else:
                if contact.is_account:
                    self.simple_response(423, message='Account objects cannot be deleted.')
                    return
                self.context.run_command('contact::delete', object=contact)
            self.context.commit()
        except:
            self.request.simple_response(500, message='Deletion failed')
        else:
            self.request.simple_response(204)

        return

    def do_OPTIONS(self):
        """ Return a valid WebDAV OPTIONS response """
        methods = ['OPTIONS, GET, HEAD, POST, PUT, DELETE, TRACE, COPY, MOVE',
         'PROPFIND, PROPPATCH, LOCK, UNLOCK, REPORT, ACL']
        self.request.simple_response(200, data=None, mimetype='text/plain', headers={'DAV': '1, 2, access-control, addressbook', 'Allow': (',').join(methods), 
           'Connection': 'close', 
           'MS-Author-Via': 'DAV'})
        return