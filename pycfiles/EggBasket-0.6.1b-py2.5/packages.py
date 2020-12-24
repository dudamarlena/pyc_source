# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/eggbasket/controllers/packages.py
# Compiled at: 2008-07-13 16:55:56
import logging, os, tempfile
from os.path import dirname, exists, isdir, join
from operator import attrgetter
import cherrypy as cp, turbogears as tg
from cherrypy.lib.cptools import serve_file
from eggbasket import model
from eggbasket.validators import ValidPackage, PackageFileSchema
from eggbasket.util import is_package_dir, is_package_file, munge_pkg_info, txt2html
from eggbasket.permissions import has_permission
log = logging.getLogger('eggbasket.controllers')

class MaxUploadSizeExceeded(Exception):
    pass


class PackageController(tg.controllers.Controller):
    """Controller for handling package info display, download and upload."""

    @tg.expose(template='eggbasket.templates.package_list')
    @tg.identity.require(has_permission('viewpkgs', 'You have no permission to view the list of packages.'))
    def index(self, *args, **kw):
        """Return list of packages in the repository."""
        pkg_root = tg.config.get('eggbasket.package_root', os.getcwd())
        log.debug('Listing package root directory: %s', pkg_root)
        packages = [ model.Package(join(pkg_root, name)) for name in os.listdir(pkg_root) if is_package_dir(join(pkg_root, name))
                   ]
        packages.sort(key=attrgetter('name'))
        return dict(packages=packages)

    @tg.expose('eggbasket.templates.package_files')
    @tg.validate(validators=dict(package=ValidPackage))
    @tg.identity.require(has_permission('viewfiles', 'You have no permission to view package distibution file lists.'))
    def files(self, package, tg_errors=None):
        """List available releases and distribution files for given package."""
        if tg_errors:
            raise cp.NotFound()
        pkg_root = tg.config.get('eggbasket.package_root', os.getcwd())
        pkg_dir = join(pkg_root, package)
        log.debug('Reading package directory %s.', pkg_dir)
        package = model.Package(pkg_dir)
        return dict(package=package)

    default = files

    @tg.expose('eggbasket.templates.package_info')
    @tg.validate(validators=PackageFileSchema)
    @tg.identity.require(has_permission('viewinfo', 'You have no permission to view package meta data.'))
    def info(self, package, filename, tg_errors=None):
        """Show meta data from PKG-INFO for given package distribution file."""
        if tg_errors:
            if tg_errors.get('package'):
                tg.redirect('/')
                flash(unicode(tg_errors['package']))
            if tg_errors.get('filename'):
                flash(unicode(tg_errors['filename']))
                tg.redirect('/package/%s' % package)
        pkg_root = tg.config.get('eggbasket.package_root', os.getcwd())
        pkg_dir = join(pkg_root, package)
        package = model.Package(pkg_dir)
        pkg_info = package.package_info(join(pkg_dir, filename))
        pkg_desc = txt2html(pkg_info.pop('description', ''), tg.config.get('eggbasket.pkg_desc_format', 'plain') == 'rest')
        pkg_info = munge_pkg_info(pkg_info)
        return dict(package=package, description=pkg_desc, pkg_info=pkg_info, filename=filename)

    @tg.expose()
    @tg.validate(validators=PackageFileSchema)
    @tg.identity.require(has_permission('download', 'You have no permission to download package distribution files.'))
    def download(self, package, filename, tg_errors=None):
        """Serve given package distribution file as binary download."""
        if tg_errors:
            if tg_errors.get('package'):
                tg.redirect('/')
                flash(unicode(tg_errors['package']))
            if tg_errors.get('filename'):
                flash(unicode(tg_errors['filename']))
                tg.redirect('/package/%s' % package)
        pkg_root = tg.config.get('eggbasket.package_root', os.getcwd())
        pkg_file = join(pkg_root, package, filename)
        return serve_file(pkg_file, 'application/octet-stream', 'attachment', filename)

    @tg.expose()
    def upload(self, name, content, *args, **kw):
        """Handle submissions from the distutils 'upload' command."""
        if not has_permission('upload'):
            raise cp.HTTPError(401, 'Unauthorized - No upload permission')
        if not is_package_file(content.filename):
            raise cp.HTTPError(400, 'Bad request - Package file type not recognized')
        pkg_root = tg.config.get('eggbasket.package_root', os.getcwd())
        pkg_dir = join(pkg_root, name)
        pkg_file = os.path.join(pkg_dir, content.filename)
        if exists(pkg_file) and not has_permission('overwrite'):
            raise cp.HTTPError(409, 'Conflict - File exists')
        if not isdir(pkg_dir):
            try:
                os.makedirs(pkg_dir)
            except (IOError, OSError), exc:
                log.error("Could not create package directory '%s': %s", pkg_dir, exc)
                raise cp.HTTPError(500, 'Internal Server Error - Could not create package directory')

        (fd, tmpfile) = tempfile.mkstemp('.tmp', 'eggbasket_', pkg_dir)
        try:
            fo = os.fdopen(fd, 'wb')
            try:
                size = 0
                chunk_size = 8192
                max_size = tg.config.get('eggbasket.max_upload_size', 104857600)
                while True:
                    chunk = content.file.read(chunk_size)
                    if not chunk:
                        break
                    size += len(chunk)
                    if size > max_size:
                        raise MaxUploadSizeExceeded()
                    fo.write(chunk)

            finally:
                fo.close()
                os.rename(tmpfile, pkg_file)

        except (IOError, OSError), exc:
            log.error("Could not write package file '%s': %s", pkg_file, exc)
            raise cp.HTTPError(500, 'Internal Server Error - Could not write package file')
        except MaxUploadSizeExceeded, exc:
            try:
                os.unlink(tmpfile)
            except:
                pass
            else:
                log.error("Upload attempt failed for '%s': %s", pkg_file, exc)
                raise cp.HTTPError(400, 'Bad Request Maximum upload size (%i bytes) exceeded' % max_size)

        log.info('Uploaded %s' % pkg_file)
        return ''

    @tg.expose()
    @tg.validate(validators=PackageFileSchema)
    @tg.identity.require(has_permission('delete', 'You have no permission to delete package distribution files.'))
    def delete(self, package, filename, tg_errors=None):
        """Delete a package file from the repository."""
        if tg_errors:
            if tg_errors.get('package'):
                tg.redirect('/')
                flash(unicode(tg_errors['package']))
            if tg_errors.get('filename'):
                flash(unicode(tg_errors['filename']))
                tg.redirect('/package/%s' % package)
        pkg_root = tg.config.get('eggbasket.package_root', os.getcwd())
        pkg_file = join(pkg_root, package, filename)
        try:
            os.unlink(pkg_file)
            tg.flash("Package file '%s' deleted." % filename)
        except OSError, exc:
            tg.flash("Could not delete package file '%s': %s" % (
             filename, exc))

        if is_package_dir(join(pkg_root, package)):
            tg.redirect('/package/%s' % package)
        else:
            tg.redirect('/')