# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/reviewboard/admin/checks.py
# Compiled at: 2020-02-11 04:03:56
from __future__ import unicode_literals
import getpass, os, sys
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.db import DatabaseError
from django.utils.translation import ugettext as _
from djblets.util.filesystem import is_exe_in_path
from djblets.siteconfig.models import SiteConfiguration
import reviewboard
from reviewboard import get_version_string
from reviewboard.admin.import_utils import has_module
_install_fine = False

def check_updates_required():
    """Check if there are manual updates required.

    Sometimes, especially in developer installs, some things need to be tweaked
    by hand before Review Board can be used on this server.
    """
    global _install_fine
    updates_required = []
    if not _install_fine:
        site_dir = os.path.dirname(settings.HTDOCS_ROOT)
        devel_install = os.path.exists(os.path.join(settings.LOCAL_ROOT, b'manage.py'))
        siteconfig = None
        try:
            siteconfig = SiteConfiguration.objects.get_current()
        except (DatabaseError, SiteConfiguration.DoesNotExist) as e:
            updates_required.append((
             b'admin/manual-updates/database-error.html',
             {b'error': e}))

        cur_version = get_version_string()
        if siteconfig and siteconfig.version != cur_version:
            updates_required.append((
             b'admin/manual-updates/version-mismatch.html',
             {b'current_version': cur_version, 
                b'stored_version': siteconfig.version, 
                b'site_dir': site_dir, 
                b'devel_install': devel_install, 
                b'python_ver': b'%s.%s.%s' % sys.version_info[:3], 
                b'package_path': os.path.dirname(reviewboard.__file__)}))
        if siteconfig and not os.path.exists(settings.STATIC_ROOT):
            new_static_root = os.path.join(settings.HTDOCS_ROOT, b'static')
            if os.path.exists(new_static_root):
                siteconfig.set(b'site_static_root', new_static_root)
                settings.STATIC_ROOT = new_static_root
        if siteconfig and not os.path.exists(settings.MEDIA_ROOT):
            new_media_root = os.path.join(settings.HTDOCS_ROOT, b'media')
            if os.path.exists(new_media_root):
                siteconfig.set(b'site_media_root', new_media_root)
                settings.MEDIA_ROOT = new_media_root
        if siteconfig and b'manual-updates' in siteconfig.settings:
            stored_updates = siteconfig.settings[b'manual-updates']
            if not stored_updates.get(b'static-media', False):
                updates_required.append((
                 b'admin/manual-updates/server-static-config.html',
                 {b'STATIC_ROOT': settings.STATIC_ROOT, 
                    b'SITE_ROOT': settings.SITE_ROOT, 
                    b'SITE_DIR': settings.LOCAL_ROOT}))
        uploaded_dir = os.path.join(settings.MEDIA_ROOT, b'uploaded')
        if not os.path.isdir(uploaded_dir) or not os.path.isdir(os.path.join(uploaded_dir, b'images')):
            updates_required.append((
             b'admin/manual-updates/media-upload-dir.html',
             {b'MEDIA_ROOT': settings.MEDIA_ROOT}))
        try:
            username = getpass.getuser()
        except ImportError:
            username = b'<server username>'

        data_dir = os.environ.get(b'HOME', b'')
        if not data_dir or not os.path.isdir(data_dir) or not os.access(data_dir, os.W_OK):
            try:
                username = getpass.getuser()
            except ImportError:
                username = b'<server username>'

            updates_required.append((
             b'admin/manual-updates/data-dir.html',
             {b'data_dir': data_dir, 
                b'writable': os.access(data_dir, os.W_OK), 
                b'server_user': username, 
                b'expected_data_dir': os.path.join(site_dir, b'data')}))
        ext_roots = [
         settings.MEDIA_ROOT]
        if not settings.DEBUG:
            ext_roots.append(settings.STATIC_ROOT)
        for root in ext_roots:
            ext_dir = os.path.join(root, b'ext')
            if not os.path.isdir(ext_dir) or not os.access(ext_dir, os.W_OK):
                updates_required.append((
                 b'admin/manual-updates/ext-dir.html',
                 {b'ext_dir': ext_dir, 
                    b'writable': os.access(ext_dir, os.W_OK), 
                    b'server_user': username}))

        if not is_exe_in_path(b'patch'):
            if sys.platform == b'win32':
                binaryname = b'patch.exe'
            else:
                binaryname = b'patch'
            updates_required.append((
             b'admin/manual-updates/install-patch.html',
             {b'platform': sys.platform, 
                b'binaryname': binaryname, 
                b'search_path': os.getenv(b'PATH')}))
        _install_fine = not updates_required
    return updates_required


def reset_check_cache():
    """Reset the cached data of all checks.

    This is mainly useful during unit tests.
    """
    global _install_fine
    _install_fine = False


def get_can_enable_ldap():
    """Check whether LDAP authentication can be enabled."""
    if has_module(b'ldap'):
        return (True, None)
    else:
        return (
         False,
         _(b'LDAP authentication requires the python-ldap library, which is not installed.'))
        return


def get_can_enable_dns():
    """Check whether we can query DNS to find the domain controller to use."""
    if has_module(b'DNS'):
        return (True, None)
    else:
        return (
         False,
         _(b'PyDNS, which is required to find the domain controller, is not installed.'))
        return


def get_can_use_amazon_s3():
    """Check whether django-storages (Amazon S3 backend) is installed."""
    try:
        if has_module(b'storages.backends.s3boto', members=[b'S3BotoStorage']):
            return (True, None)
        else:
            return (
             False,
             _(b'Amazon S3 depends on django-storages, which is not installed'))

    except ImproperlyConfigured as e:
        return (
         False, _(b'Amazon S3 backend failed to load: %s') % e)

    return


def get_can_use_openstack_swift():
    """Check whether django-storage-swift is installed."""
    try:
        if has_module(b'swift.storage', members=[b'SwiftStorage']):
            return (True, None)
        else:
            return (
             False,
             _(b'OpenStack Swift depends on django-storage-swift, which is not installed'))

    except ImproperlyConfigured as e:
        return (
         False, _(b'OpenStack Swift backend failed to load: %s') % e)

    return


def get_can_use_couchdb():
    """Check whether django-storages (CouchDB backend) is installed."""
    if has_module(b'storages.backends.couchdb', members=[b'CouchDBStorage']):
        return (True, None)
    else:
        return (
         False,
         _(b'CouchDB depends on django-storages, which is not installed'))
        return