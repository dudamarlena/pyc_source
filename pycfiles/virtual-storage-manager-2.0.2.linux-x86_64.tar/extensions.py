# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/vsm/api/extensions.py
# Compiled at: 2016-06-13 14:11:03
import os, webob.dec, webob.exc, vsm.api.openstack
from vsm.api.openstack import wsgi
from vsm.api import xmlutil
from vsm import exception
from vsm import flags
from vsm.openstack.common import exception as common_exception
from vsm.openstack.common import importutils
from vsm.openstack.common import log as logging
import vsm.policy
LOG = logging.getLogger(__name__)
FLAGS = flags.FLAGS

class ExtensionDescriptor(object):
    """Base class that defines the contract for extensions.

    Note that you don't have to derive from this class to have a valid
    extension; it is purely a convenience.

    """
    name = None
    alias = None
    namespace = None
    updated = None

    def __init__(self, ext_mgr):
        """Register extension with the extension manager."""
        ext_mgr.register(self)

    def get_resources(self):
        """List of extensions.ResourceExtension extension objects.

        Resources define new nouns, and are accessible through URLs.

        """
        resources = []
        return resources

    def get_controller_extensions(self):
        """List of extensions.ControllerExtension extension objects.

        Controller extensions are used to extend existing controllers.
        """
        controller_exts = []
        return controller_exts

    @classmethod
    def nsmap(cls):
        """Synthesize a namespace map from extension."""
        nsmap = ext_nsmap.copy()
        nsmap[cls.alias] = cls.namespace
        return nsmap

    @classmethod
    def xmlname(cls, name):
        """Synthesize element and attribute names."""
        return '{%s}%s' % (cls.namespace, name)


def make_ext(elem):
    elem.set('name')
    elem.set('namespace')
    elem.set('alias')
    elem.set('updated')
    desc = xmlutil.SubTemplateElement(elem, 'description')
    desc.text = 'description'
    xmlutil.make_links(elem, 'links')


ext_nsmap = {None: xmlutil.XMLNS_COMMON_V10, 'atom': xmlutil.XMLNS_ATOM}

class ExtensionTemplate(xmlutil.TemplateBuilder):

    def construct(self):
        root = xmlutil.TemplateElement('extension', selector='extension')
        make_ext(root)
        return xmlutil.MasterTemplate(root, 1, nsmap=ext_nsmap)


class ExtensionsTemplate(xmlutil.TemplateBuilder):

    def construct(self):
        root = xmlutil.TemplateElement('extensions')
        elem = xmlutil.SubTemplateElement(root, 'extension', selector='extensions')
        make_ext(elem)
        return xmlutil.MasterTemplate(root, 1, nsmap=ext_nsmap)


class ExtensionsResource(wsgi.Resource):

    def __init__(self, extension_manager):
        self.extension_manager = extension_manager
        super(ExtensionsResource, self).__init__(None)
        return

    def _translate(self, ext):
        ext_data = {}
        ext_data['name'] = ext.name
        ext_data['alias'] = ext.alias
        ext_data['description'] = ext.__doc__
        ext_data['namespace'] = ext.namespace
        ext_data['updated'] = ext.updated
        ext_data['links'] = []
        return ext_data

    @wsgi.serializers(xml=ExtensionsTemplate)
    def index(self, req):
        extensions = []
        for _alias, ext in self.extension_manager.extensions.iteritems():
            extensions.append(self._translate(ext))

        return dict(extensions=extensions)

    @wsgi.serializers(xml=ExtensionTemplate)
    def show(self, req, id):
        try:
            ext = self.extension_manager.extensions[id]
        except KeyError:
            raise webob.exc.HTTPNotFound()

        return dict(extension=self._translate(ext))

    def delete(self, req, id):
        raise webob.exc.HTTPNotFound()

    def create(self, req):
        raise webob.exc.HTTPNotFound()


class ExtensionManager(object):
    """Load extensions from the configured extension path.

    See vsm/tests/api/extensions/foxinsocks/extension.py for an
    example extension implementation.

    """

    def __init__(self):
        LOG.audit(_('Initializing extension manager.'))
        self.cls_list = FLAGS.vsmapi_storage_extension
        self.extensions = {}
        self._load_extensions()

    def is_loaded(self, alias):
        return alias in self.extensions

    def register(self, ext):
        if not self._check_extension(ext):
            return
        alias = ext.alias
        LOG.audit(_('Loaded extension: %s'), alias)
        if alias in self.extensions:
            raise exception.Error('Found duplicate extension: %s' % alias)
        self.extensions[alias] = ext

    def get_resources(self):
        """Returns a list of ResourceExtension objects."""
        resources = []
        resources.append(ResourceExtension('extensions', ExtensionsResource(self)))
        for ext in self.extensions.values():
            try:
                resources.extend(ext.get_resources())
            except AttributeError:
                pass

        return resources

    def get_controller_extensions(self):
        """Returns a list of ControllerExtension objects."""
        controller_exts = []
        for ext in self.extensions.values():
            try:
                get_ext_method = ext.get_controller_extensions
            except AttributeError:
                continue

            controller_exts.extend(get_ext_method())

        return controller_exts

    def _check_extension(self, extension):
        """Checks for required methods in extension objects."""
        try:
            LOG.debug(_('Ext name: %s'), extension.name)
            LOG.debug(_('Ext alias: %s'), extension.alias)
            LOG.debug(_('Ext description: %s'), (' ').join(extension.__doc__.strip().split()))
            LOG.debug(_('Ext namespace: %s'), extension.namespace)
            LOG.debug(_('Ext updated: %s'), extension.updated)
        except AttributeError as ex:
            LOG.exception(_('Exception loading extension: %s'), unicode(ex))
            return False

        return True

    def load_extension(self, ext_factory):
        """Execute an extension factory.

        Loads an extension.  The 'ext_factory' is the name of a
        callable that will be imported and called with one
        argument--the extension manager.  The factory callable is
        expected to call the register() method at least once.
        """
        LOG.debug(_('Loading extension %s'), ext_factory)
        factory = importutils.import_class(ext_factory)
        LOG.debug(_('Calling extension factory %s'), ext_factory)
        factory(self)

    def _load_extensions(self):
        """Load extensions specified on the command line."""
        extensions = list(self.cls_list)
        old_contrib_path = 'vsm.api.openstack.storage.contrib.standard_extensions'
        new_contrib_path = 'vsm.api.contrib.standard_extensions'
        if old_contrib_path in extensions:
            LOG.warn(_('vsmapi_storage_extension is set to deprecated path: %s'), old_contrib_path)
            LOG.warn(_('Please set your flag or vsm.conf settings for vsmapi_storage_extension to: %s'), new_contrib_path)
            extensions = [ e.replace(old_contrib_path, new_contrib_path) for e in extensions
                         ]
        for ext_factory in extensions:
            try:
                self.load_extension(ext_factory)
            except Exception as exc:
                LOG.warn(_('Failed to load extension %(ext_factory)s: %(exc)s') % locals())


class ControllerExtension(object):
    """Extend core controllers of vsm OpenStack API.

    Provide a way to extend existing vsm OpenStack API core
    controllers.
    """

    def __init__(self, extension, collection, controller):
        self.extension = extension
        self.collection = collection
        self.controller = controller


class ResourceExtension(object):
    """Add top level resources to the OpenStack API in vsm."""

    def __init__(self, collection, controller, parent=None, collection_actions=None, member_actions=None, custom_routes_fn=None):
        if not collection_actions:
            collection_actions = {}
        if not member_actions:
            member_actions = {}
        self.collection = collection
        self.controller = controller
        self.parent = parent
        self.collection_actions = collection_actions
        self.member_actions = member_actions
        self.custom_routes_fn = custom_routes_fn


def load_standard_extensions(ext_mgr, logger, path, package, ext_list=None):
    """Registers all standard API extensions."""
    our_dir = path[0]
    for dirpath, dirnames, filenames in os.walk(our_dir):
        relpath = os.path.relpath(dirpath, our_dir)
        if relpath == '.':
            relpkg = ''
        else:
            relpkg = '.%s' % ('.').join(relpath.split(os.sep))
        for fname in filenames:
            root, ext = os.path.splitext(fname)
            if ext != '.py' or root == '__init__':
                continue
            classname = '%s%s' % (root[0].upper(), root[1:])
            classpath = '%s%s.%s.%s' % (
             package, relpkg, root, classname)
            if ext_list is not None and classname not in ext_list:
                logger.debug('Skipping extension: %s' % classpath)
                continue
            try:
                ext_mgr.load_extension(classpath)
            except Exception as exc:
                logger.warn(_('Failed to load extension %(classpath)s: %(exc)s') % locals())

        subdirs = []
        for dname in dirnames:
            if not os.path.exists(os.path.join(dirpath, dname, '__init__.py')):
                continue
            ext_name = '%s%s.%s.extension' % (
             package, relpkg, dname)
            try:
                ext = importutils.import_class(ext_name)
            except common_exception.NotFound:
                subdirs.append(dname)
            else:
                try:
                    ext(ext_mgr)
                except Exception as exc:
                    logger.warn(_('Failed to load extension %(ext_name)s: %(exc)s') % locals())

        dirnames[:] = subdirs

    return


def extension_authorizer(api_name, extension_name):

    def authorize(context, target=None):
        if target is None:
            target = {'project_id': context.project_id, 'user_id': context.user_id}
        action = '%s_extension:%s' % (api_name, extension_name)
        vsm.policy.enforce(context, action, target)
        return

    return authorize


def soft_extension_authorizer(api_name, extension_name):
    hard_authorize = extension_authorizer(api_name, extension_name)

    def authorize(context):
        try:
            hard_authorize(context)
            return True
        except exception.NotAuthorized:
            return False

    return authorize