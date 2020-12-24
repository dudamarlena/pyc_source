# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/WikiTemplates/attachment.py
# Compiled at: 2008-04-21 09:04:49
import os, re, shutil, time, unicodedata
from trac import perm, util
from trac.config import BoolOption, IntOption
from trac.core import *
from trac.env import IEnvironmentSetupParticipant
from trac.mimeview import *
from trac.util import get_reporter_id, create_unique_file
from trac.util.datefmt import format_datetime, pretty_timedelta
from trac.util.html import Markup, html
from trac.util.text import unicode_quote, unicode_unquote, pretty_size
from trac.web import HTTPBadRequest, IRequestHandler
from trac.web.chrome import add_link, add_stylesheet, INavigationContributor
from trac.wiki.api import IWikiSyntaxProvider
from trac.wiki.formatter import wiki_to_html, wiki_to_oneliner

class InvalidAttachment(TracError):
    """Exception raised when attachment validation fails."""
    pass


class IAttachmentChangeListener(Interface):
    """Extension point interface for components that require notification when
    attachments are created or deleted."""

    def attachment_added(attachment):
        """Called when an attachment is added."""
        pass

    def attachment_deleted(attachment):
        """Called when an attachment is deleted."""
        pass


class IAttachmentManipulator(Interface):
    """Extension point interface for components that need to manipulate
    attachments.

    Unlike change listeners, a manipulator can reject changes being committed
    to the database."""

    def prepare_attachment(req, attachment, fields):
        """Not currently called, but should be provided for future
        compatibility."""
        pass

    def validate_attachment(req, attachment):
        """Validate an attachment after upload but before being stored in Trac
        environment.

        Must return a list of `(field, message)` tuples, one for each problem
        detected. `field` can be any of `description`, `username`, `filename`,
        `content`, or `None` to indicate an overall problem with the
        attachment. Therefore, a return value of `[]` means everything is
        OK."""
        pass


class Attachment(object):

    def __init__(self, env, parent_type, parent_id, filename=None, db=None):
        self.env = env
        self.parent_type = parent_type
        self.parent_id = unicode(parent_id)
        if filename:
            self._fetch(filename, db)
        else:
            self.filename = None
            self.description = None
            self.size = None
            self.time = None
            self.author = None
            self.ipnr = None
        return

    def _fetch(self, filename, db=None):
        if not db:
            db = self.env.get_db_cnx()
        cursor = db.cursor()
        cursor.execute('SELECT filename,description,size,time,author,ipnr FROM attachment WHERE type=%s AND id=%s AND filename=%s ORDER BY time', (
         self.parent_type, unicode(self.parent_id), filename))
        row = cursor.fetchone()
        cursor.close()
        if not row:
            self.filename = filename
            raise TracError('Attachment %s does not exist.' % self.title, 'Invalid Attachment')
        self.filename = row[0]
        self.description = row[1]
        self.size = row[2] and int(row[2]) or 0
        self.time = row[3] and int(row[3]) or 0
        self.author = row[4]
        self.ipnr = row[5]

    def _get_path(self):
        path = os.path.join(self.env.path, 'attachments', self.parent_type, unicode_quote(self.parent_id))
        if self.filename:
            path = os.path.join(path, unicode_quote(self.filename))
        return os.path.normpath(path)

    path = property(_get_path)

    def href(self, req, *args, **dict):
        return req.href.attachment(self.parent_type, self.parent_id, self.filename, *args, **dict)

    def parent_href(self, req):
        return req.href(self.parent_type, self.parent_id)

    def _get_title(self):
        return '%s%s: %s' % (self.parent_type == 'ticket' and '#' or '',
         self.parent_id, self.filename)

    title = property(_get_title)

    def delete(self, db=None):
        assert self.filename, 'Cannot delete non-existent attachment'
        if not db:
            db = self.env.get_db_cnx()
            handle_ta = True
        else:
            handle_ta = False
        cursor = db.cursor()
        cursor.execute('DELETE FROM attachment WHERE type=%s AND id=%s AND filename=%s', (
         self.parent_type, self.parent_id,
         self.filename))
        if os.path.isfile(self.path):
            try:
                os.unlink(self.path)
            except OSError:
                self.env.log.error('Failed to delete attachment file %s', self.path, exc_info=True)
                if handle_ta:
                    db.rollback()
                raise TracError, 'Could not delete attachment'

        self.env.log.info('Attachment removed: %s' % self.title)
        if handle_ta:
            db.commit()
        for listener in AttachmentModule(self.env).change_listeners:
            listener.attachment_deleted(self)

    def insert(self, filename, fileobj, size, t=None, db=None):
        if not db:
            db = self.env.get_db_cnx()
            handle_ta = True
        else:
            handle_ta = False
        self.size = size and int(size) or 0
        self.time = int(t or time.time())
        attachments_dir = os.path.join(os.path.normpath(self.env.path), 'attachments')
        commonprefix = os.path.commonprefix([attachments_dir, self.path])
        assert commonprefix == attachments_dir
        if not os.access(self.path, os.F_OK):
            os.makedirs(self.path)
        filename = unicode_quote(filename)
        (path, targetfile) = create_unique_file(os.path.join(self.path, filename))
        try:
            basename = os.path.basename(path).encode('ascii')
            filename = unicode_unquote(basename)
            cursor = db.cursor()
            cursor.execute('INSERT INTO attachment VALUES (%s,%s,%s,%s,%s,%s,%s,%s)', (
             self.parent_type, self.parent_id, filename,
             self.size, self.time, self.description, self.author,
             self.ipnr))
            shutil.copyfileobj(fileobj, targetfile)
            self.filename = filename
            self.env.log.info('New attachment: %s by %s', self.title, self.author)
            if handle_ta:
                db.commit()
            for listener in AttachmentModule(self.env).change_listeners:
                listener.attachment_added(self)

        finally:
            targetfile.close()

    def select(cls, env, parent_type, parent_id, db=None):
        if not db:
            db = env.get_db_cnx()
        cursor = db.cursor()
        cursor.execute('SELECT filename,description,size,time,author,ipnr FROM attachment WHERE type=%s AND id=%s ORDER BY time', (
         parent_type, unicode(parent_id)))
        for (filename, description, size, time, author, ipnr) in cursor:
            attachment = Attachment(env, parent_type, parent_id)
            attachment.filename = filename
            attachment.description = description
            attachment.size = size and int(size) or 0
            attachment.time = time and int(time) or 0
            attachment.author = author
            attachment.ipnr = ipnr
            yield attachment

    def delete_all(cls, env, parent_type, parent_id, db):
        """Delete all attachments of a given resource.

        As this is usually done while deleting the parent resource,
        the `db` argument is ''not'' optional here.
        """
        attachment_dir = None
        for attachment in list(cls.select(env, parent_type, parent_id, db)):
            attachment_dir = os.path.dirname(attachment.path)
            attachment.delete(db)

        if attachment_dir:
            try:
                os.rmdir(attachment_dir)
            except OSError:
                env.log.error("Can't delete attachment directory %s", attachment_dir, exc_info=True)

        return

    select = classmethod(select)
    delete_all = classmethod(delete_all)

    def open(self):
        self.env.log.debug('Trying to open attachment at %s', self.path)
        try:
            fd = open(self.path, 'rb')
        except IOError:
            raise TracError('Attachment %s not found' % self.filename)

        return fd


def attachments_to_hdf(env, req, db, parent_type, parent_id):
    return [ attachment_to_hdf(env, req, db, attachment) for attachment in Attachment.select(env, parent_type, parent_id, db)
           ]


def attachment_to_hdf(env, req, db, attachment):
    if not db:
        db = env.get_db_cnx()
    hdf = {'filename': attachment.filename, 'description': wiki_to_oneliner(attachment.description, env, db), 
       'author': attachment.author, 
       'ipnr': attachment.ipnr, 
       'size': pretty_size(attachment.size), 
       'time': format_datetime(attachment.time), 
       'age': pretty_timedelta(attachment.time), 
       'href': attachment.href(req)}
    return hdf


class AttachmentModule(Component):
    implements(IEnvironmentSetupParticipant, IRequestHandler, INavigationContributor, IWikiSyntaxProvider)
    change_listeners = ExtensionPoint(IAttachmentChangeListener)
    manipulators = ExtensionPoint(IAttachmentManipulator)
    CHUNK_SIZE = 4096
    max_size = IntOption('attachment', 'max_size', 262144, 'Maximum allowed file size for ticket and wiki attachments.')
    render_unsafe_content = BoolOption('attachment', 'render_unsafe_content', 'false', 'Whether non-binary attachments should be rendered in the browser, or\n        only made downloadable.\n\n        Pretty much any text file may be interpreted as HTML by the browser,\n        which allows a malicious user to attach a file containing cross-site\n        scripting attacks.\n\n        For public sites where anonymous users can create attachments, it is\n        recommended to leave this option disabled (which is the default).')

    def environment_created(self):
        """Create the attachments directory."""
        if self.env.path:
            attachments_dir = os.path.join(self.env.path, 'attachments')
            if not os.path.exists(attachments_dir):
                os.mkdir(attachments_dir)

    def environment_needs_upgrade(self, db):
        return False

    def upgrade_environment(self, db):
        pass

    def get_active_navigation_item(self, req):
        return req.args.get('type')

    def get_navigation_items(self, req):
        return []

    def match_request(self, req):
        match = re.match('^/attachment/(ticket|wiki|templates)(?:[/:](.*))?$', req.path_info)
        if match:
            req.args['type'] = match.group(1)
            req.args['path'] = match.group(2).replace(':', '/')
            return True

    def process_request(self, req):
        parent_type = req.args.get('type')
        path = req.args.get('path')
        if not parent_type or not path:
            raise HTTPBadRequest('Bad request')
        if parent_type not in ('ticket', 'wiki', 'templates'):
            raise HTTPBadRequest('Unknown attachment type')
        action = req.args.get('action', 'view')
        if action == 'new':
            attachment = Attachment(self.env, parent_type, path)
        else:
            segments = path.split('/')
            parent_id = ('/').join(segments[:-1])
            last_segment = segments[(-1)]
            if len(segments) == 1:
                self._render_list(req, parent_type, last_segment)
                return ('attachment.cs', None)
            if not last_segment:
                raise HTTPBadRequest('Bad request')
            attachment = Attachment(self.env, parent_type, parent_id, last_segment)
        (parent_link, parent_text) = self._parent_to_hdf(req, attachment.parent_type, attachment.parent_id)
        if req.method == 'POST':
            if action == 'new':
                self._do_save(req, attachment)
            elif action == 'delete':
                self._do_delete(req, attachment)
        elif action == 'delete':
            self._render_confirm(req, attachment)
        elif action == 'new':
            self._render_form(req, attachment)
        else:
            add_link(req, 'up', parent_link, parent_text)
            self._render_view(req, attachment)
        add_stylesheet(req, 'common/css/code.css')
        return ('attachment.cs', None)

    def _parent_to_hdf(self, req, parent_type, parent_id):
        parent_link = req.href(parent_type, parent_id)
        if parent_type == 'ticket':
            parent_text = 'Ticket #' + parent_id
        else:
            parent_text = parent_id
        req.hdf['attachment.parent'] = {'type': parent_type, 'id': parent_id, 'name': parent_text, 
           'href': parent_link}
        return (
         parent_link, parent_text)

    def get_wiki_syntax(self):
        return []

    def get_link_resolvers(self):
        yield (
         'attachment', self._format_link)

    def get_history(self, start, stop, type):
        """Return an iterable of tuples describing changes to attachments on
        a particular object type.

        The tuples are in the form (change, type, id, filename, time,
        description, author). `change` can currently only be `created`."""
        db = self.env.get_db_cnx()
        cursor = db.cursor()
        cursor.execute('SELECT type, id, filename, time, description, author   FROM attachment   WHERE time > %s AND time < %s         AND type = %s', (
         start, stop, type))
        for (type, id, filename, time, description, author) in cursor:
            yield (
             'created', type, id, filename, time, description, author)

    def get_timeline_events(self, req, db, type, format, start, stop, display):
        """Return an iterable of events suitable for ITimelineEventProvider.

        `display` is a callback for formatting the attachment's parent
        """
        for (change, type, id, filename, time, descr, author) in self.get_history(start, stop, type):
            title = html.EM(os.path.basename(filename)) + ' attached to ' + display(id)
            if format == 'rss':
                descr = wiki_to_html(descr or '--', self.env, req, db, absurls=True)
                href = req.abs_href
            else:
                descr = wiki_to_oneliner(descr, self.env, db, shorten=True)
                title += Markup(' by %s', author)
                href = req.href
            yield (
             'attachment', href.attachment(type, id, filename), title,
             time, author, descr)

    def _do_save(self, req, attachment):
        perm_map = {'ticket': 'TICKET_APPEND', 
           'wiki': 'WIKI_MODIFY', 
           'templates': 'TEMPLATES_MODIFY'}
        req.perm.assert_permission(perm_map[attachment.parent_type])
        if req.args.has_key('cancel'):
            req.redirect(attachment.parent_href(req))
        upload = req.args['attachment']
        if not hasattr(upload, 'filename') or not upload.filename:
            raise TracError('No file uploaded')
        if hasattr(upload.file, 'fileno'):
            size = os.fstat(upload.file.fileno())[6]
        else:
            upload.file.seek(0, 2)
            size = upload.file.tell()
            upload.file.seek(0)
        if size == 0:
            raise TracError("Can't upload empty file")
        max_size = self.max_size
        if max_size >= 0 and size > max_size:
            raise TracError('Maximum attachment size: %d bytes' % max_size, 'Upload failed')
        filename = unicodedata.normalize('NFC', unicode(upload.filename, 'utf-8'))
        filename = filename.replace('\\', '/').replace(':', '/')
        filename = os.path.basename(filename)
        if not filename:
            raise TracError('No file uploaded')
        attachment.description = req.args.get('description', '')
        attachment.author = get_reporter_id(req, 'author')
        attachment.ipnr = req.remote_addr
        for manipulator in self.manipulators:
            for (field, message) in manipulator.validate_attachment(req, attachment):
                if field:
                    raise InvalidAttachment('Attachment field %s is invalid: %s' % (
                     field, message))
                else:
                    raise InvalidAttachment('Invalid attachment: %s' % message)

        if req.args.get('replace'):
            try:
                old_attachment = Attachment(self.env, attachment.parent_type, attachment.parent_id, filename)
                if not (old_attachment.author and req.authname and old_attachment.author == req.authname):
                    perm_map = {'ticket': 'TICKET_ADMIN', 'wiki': 'WIKI_DELETE', 
                       'templates': 'TEMPLATES_DELETE'}
                    req.perm.assert_permission(perm_map[old_attachment.parent_type])
                old_attachment.delete()
            except TracError:
                pass
            else:
                attachment.filename = None
        attachment.insert(filename, upload.file, size)
        req.redirect(attachment.href(req))
        return

    def _do_delete(self, req, attachment):
        perm_map = {'ticket': 'TICKET_ADMIN', 
           'wiki': 'WIKI_DELETE', 
           'templates': 'TEMPLATES_DELETE'}
        req.perm.assert_permission(perm_map[attachment.parent_type])
        if req.args.has_key('cancel'):
            req.redirect(attachment.href(req))
        attachment.delete()
        req.redirect(attachment.parent_href(req))

    def _render_confirm(self, req, attachment):
        perm_map = {'ticket': 'TICKET_ADMIN', 
           'wiki': 'WIKI_DELETE', 
           'templates': 'TEMPLATES_DELETE'}
        req.perm.assert_permission(perm_map[attachment.parent_type])
        req.hdf['title'] = '%s (delete)' % attachment.title
        req.hdf['attachment'] = {'filename': attachment.filename, 'mode': 'delete'}

    def _render_form(self, req, attachment):
        perm_map = {'ticket': 'TICKET_APPEND', 
           'wiki': 'WIKI_MODIFY', 
           'templates': 'TEMPLATES_MODIFY'}
        req.perm.assert_permission(perm_map[attachment.parent_type])
        req.hdf['attachment'] = {'mode': 'new', 'author': get_reporter_id(req)}

    def _render_view(self, req, attachment):
        perm_map = {'ticket': 'TICKET_VIEW', 
           'wiki': 'WIKI_VIEW', 
           'templates': 'TEMPLATES_VIEW'}
        req.perm.assert_permission(perm_map[attachment.parent_type])
        req.check_modified(attachment.time)
        req.hdf['title'] = attachment.title
        req.hdf['attachment'] = attachment_to_hdf(self.env, req, None, attachment)
        req.hdf['attachment.description'] = wiki_to_html(attachment.description, self.env, req)
        perm_map = {'ticket': 'TICKET_ADMIN', 
           'wiki': 'WIKI_DELETE', 
           'templates': 'TEMPLATES_DELETE'}
        if req.perm.has_permission(perm_map[attachment.parent_type]):
            req.hdf['attachment.can_delete'] = 1
        fd = attachment.open()
        try:
            mimeview = Mimeview(self.env)
            str_data = fd.read(1000)
            fd.seek(0)
            binary = is_binary(str_data)
            mime_type = mimeview.get_mimetype(attachment.filename, str_data)
            format = req.args.get('format')
            if format in ('raw', 'txt'):
                if not self.render_unsafe_content and not binary:
                    req.send_header('Content-Disposition', 'attachment;filename=' + attachment.filename)
                if not mime_type or self.render_unsafe_content and not binary and format == 'txt':
                    mime_type = 'text/plain'
                if 'charset=' not in mime_type:
                    charset = mimeview.get_charset(str_data, mime_type)
                    mime_type = mime_type + '; charset=' + charset
                req.send_file(attachment.path, mime_type)
            if self.render_unsafe_content and not binary and mime_type and not mime_type.startswith('text/plain'):
                plaintext_href = attachment.href(req, format='txt')
                add_link(req, 'alternate', plaintext_href, 'Plain Text', mime_type)
            raw_href = attachment.href(req, format='raw')
            add_link(req, 'alternate', raw_href, 'Original Format', mime_type)
            self.log.debug('Rendering preview of file %s with mime-type %s' % (
             attachment.filename, mime_type))
            req.hdf['attachment'] = mimeview.preview_to_hdf(req, fd, os.fstat(fd.fileno()).st_size, mime_type, attachment.filename, raw_href, annotations=['lineno'])
        finally:
            fd.close()

        return

    def _render_list(self, req, p_type, p_id):
        self._parent_to_hdf(req, p_type, p_id)
        req.hdf['attachment'] = {'mode': 'list', 
           'list': attachments_to_hdf(self.env, req, None, p_type, p_id), 
           'attach_href': req.href.attachment(p_type, p_id)}
        return

    def _format_link(self, formatter, ns, target, label):
        (link, params, fragment) = formatter.split_link(target)
        ids = link.split(':', 2)
        if len(ids) == 3:
            (parent_type, parent_id, filename) = ids
        else:
            (parent_type, parent_id) = ('wiki', 'WikiStart')
            if formatter.req:
                path_info = formatter.req.path_info.split('/', 2)
                if len(path_info) > 1:
                    parent_type = path_info[1]
                if len(path_info) > 2:
                    parent_id = path_info[2]
            filename = link
        href = formatter.href()
        try:
            attachment = Attachment(self.env, parent_type, parent_id, filename)
            if formatter.req:
                href = attachment.href(formatter.req) + params
            return html.A(label, class_='attachment', href=href, title='Attachment %s' % attachment.title)
        except TracError:
            return html.A(label, class_='missing attachment', rel='nofollow', href=formatter.href())