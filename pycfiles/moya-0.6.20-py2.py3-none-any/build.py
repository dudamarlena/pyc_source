# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/will/projects/moya/moya/build.py
# Compiled at: 2017-01-15 13:25:40
from __future__ import unicode_literals
from __future__ import print_function
from .archive import Archive
from .context import Context
from .parser import Parser
from . import tags
from . import errors
from .settings import SettingsContainer
from .filesystems import FSWrapper
from .compat import text_type, string_types, iteritems
from .context.expression import Expression
from .tools import textual_list
from . import pilot
from fs import open_fs
from fs.errors import NoSysPath
from fs.osfs import OSFS
from fs.multifs import MultiFS
import gc, os, sys
from time import time
from collections import namedtuple
from os.path import dirname, abspath
import logging
log = logging.getLogger(b'moya.runtime')
startup_log = logging.getLogger(b'moya.startup')

def read_config(fs, settings_path=b'settings.ini'):
    """Just read the config for a project"""
    if b'://' in fs:
        fs = open_fs(fs)
    else:
        fs = OSFS(fs)
    cfg = SettingsContainer.read(fs, settings_path)
    return cfg


def build(fs, settings_path=b'settings.ini', rebuild=False, archive=None, strict=False, master_settings=None, test_build=False, develop=False):
    """Build a project"""
    if isinstance(fs, string_types):
        if b'://' in fs:
            fs = open_fs(fs)
        else:
            fs = OSFS(fs)
    if isinstance(settings_path, string_types):
        settings_path = [
         settings_path]
    try:
        syspath = fs.getsyspath(b'/')
    except NoSysPath:
        syspath = None

    cwd = os.getcwd()
    if syspath is not None:
        os.chdir(syspath)
    try:
        log.debug((b'reading settings from {}').format(textual_list(settings_path)))
        cfg = SettingsContainer.read(fs, settings_path, master=master_settings)
        if b'customize' in cfg:
            customize_location = cfg.get(b'customize', b'location')
            if customize_location:
                settings_path = cfg.get(b'customize', b'settings', b'settings.ini')
                startup_log.info(b"customizing '%s'", customize_location)
                customize_fs = open_fs(cfg.get(b'customize', b'location'))
                cfg = SettingsContainer.read(customize_fs, settings_path, master=cfg)
                overlay_fs = MultiFS()
                overlay_fs.add_fs(b'project', fs)
                overlay_fs.add_fs(b'custom', customize_fs, write=True)
                fs = overlay_fs
                try:
                    syspath = fs.getsyspath(b'/')
                except NoSysPath:
                    pass
                else:
                    os.chdir(syspath)

        if archive is None:
            archive = Archive(fs, strict=strict, test_build=test_build, develop=develop)
        context = Context()
        archive.cfg = cfg
        root = context.root
        root[b'libs'] = archive.libs
        root[b'apps'] = archive.apps
        root[b'fs'] = FSWrapper(fs)
        root[b'settings'] = SettingsContainer.from_dict(archive.cfg[b'settings'])
        startup_path = archive.cfg.get(b'project', b'startup')
        docs_location = archive.cfg.get(b'project', b'location')
        archive.init_settings()
        root[b'console'] = archive.console
        root[b'debug'] = archive.debug
        root[b'_rebuild'] = rebuild
        parser = Parser(archive, fs.opendir(docs_location), startup_path)
        doc = parser.parse()
        if doc is None:
            raise errors.StartupFailedError((b'unable to parse "{}"').format(startup_path))
        archive.build(doc, fs=fs)
        return (
         fs, archive, context, doc)
    finally:
        os.chdir(cwd)
        gc.collect()

    return


ServerBuildResult = namedtuple(b'ServerBuildResult', [
 b'archive',
 b'context',
 b'server'])

def render_failed_documents(archive, console, no_console=False):
    failed = 0
    for libname, lib in iteritems(archive.libs):
        for failed_doc in lib.failed_documents:
            failed += 1
            if not no_console:
                log.error(b'%s', failed_doc.msg)
                console.document_error(failed_doc.msg, failed_doc.path, failed_doc.code, failed_doc.line, failed_doc.col, diagnosis=failed_doc.diagnosis)

    for failed_doc in archive.failed_documents:
        failed += 1
        if not no_console:
            log.error(b'%s', failed_doc.msg)
            console.document_error(failed_doc.msg, failed_doc.path, failed_doc.code, failed_doc.line, failed_doc.col, diagnosis=failed_doc.diagnosis)

    return failed


def build_lib(location, archive=None, dependancies=None, ignore_errors=False, tests=False):
    """Build a project with a single lib (for testing)"""
    if archive is None:
        archive = Archive()
    if location.startswith(b'py:'):
        py = location.split(b':', 1)[1]
        __import__(py)
        module = sys.modules[py]
        location = dirname(abspath(module.__file__))
    with open_fs(location) as (import_fs):
        lib = archive.load_library(import_fs)
    if tests:
        dependancies = lib._cfg.get_list(b'tests', b'import') or []
    if dependancies:
        for require_lib in dependancies:
            if require_lib.startswith(b'py:'):
                py = require_lib.split(b':', 1)[1]
                __import__(py)
                module = sys.modules[py]
                location = dirname(abspath(module.__file__))
            else:
                location = require_lib
            with open_fs(location) as (import_fs):
                _lib = archive.load_library(import_fs)

    archive.finalize(ignore_errors=ignore_errors)
    return (
     archive, lib)


def get_lib_info(location, archive=None):
    if archive is None:
        archive = Archive()
    if location.startswith(b'py:'):
        py = location.split(b':', 1)[1]
        __import__(py)
        module = sys.modules[py]
        location = dirname(abspath(module.__file__))
    with open_fs(location) as (import_fs):
        cfg = SettingsContainer.read(import_fs, b'lib.ini')
    return cfg


def build_server(fs, settings_path, server_element=b'main', no_console=False, rebuild=False, validate_db=False, breakpoint=False, strict=False, master_settings=None, test_build=False, develop=False):
    """Build a server"""
    start = time()
    archive = Archive()
    console = archive.console
    project_fs = None
    try:
        with Expression._lock:
            project_fs, archive, context, doc = build(fs, settings_path, rebuild=rebuild, strict=strict, master_settings=master_settings, test_build=test_build, develop=develop)
        console = archive.console
    except errors.ParseError as e:
        if not no_console:
            line, col = e.position
            console.document_error(text_type(e), e.path, e.code, line, col)
        return
    except errors.ElementError as element_error:
        if not no_console:
            line = element_error.source_line
            col = 0
            console.document_error(text_type(element_error), element_error.element._location, element_error.element._code, line, col)
        raise errors.StartupFailedError(b'Failed to build project')

    if project_fs is None:
        if isinstance(fs, string_types):
            if b'://' in fs:
                fs = open_fs(fs)
            else:
                fs = OSFS(fs)
    archive.project_fs = project_fs
    try:
        app, server = doc.get_element(server_element)
    except errors.ElementNotFoundError:
        raise errors.StartupFailedError((b"no <server> element called '{}' found in the project (check setting [project]/startup)").format(server_element))

    error_msg = None
    docs_location = archive.cfg.get(b'project', b'location')
    try:
        with pilot.manage_request(None, context):
            server.startup(archive, context, project_fs.opendir(docs_location), breakpoint=breakpoint)
    except errors.StartupFailedError as error:
        error_msg = text_type(error)
    except errors.ElementError as e:
        raise
    except Exception as e:
        failed = render_failed_documents(archive, console, no_console=no_console)
        if failed:
            raise errors.StartupFailedError((b'{} document(s) failed to build').format(failed))
        if hasattr(e, b'__moyaconsole__'):
            e.__moyaconsole__(console)
        error_msg = text_type(e)
        raise errors.StartupFailedError(error_msg or b'Failed to build project')

    failed = render_failed_documents(archive, console, no_console=no_console)
    if failed:
        raise errors.StartupFailedError(error_msg or b'Failed to build project')
    archive.init_media()
    archive.init_data()
    if validate_db:
        from . import db
        if db.validate_all(archive, console) == 0:
            startup_log.debug(b'models validated successfully')
        else:
            msg = b"Models failed to validate, see 'moya db validate' for more information"
            raise errors.StartupFailedError(msg)
    startup_log.info(b'%s built %.1fms', server, (time() - start) * 1000.0)
    return ServerBuildResult(archive=archive, context=context, server=server)


if __name__ == b'__main__':
    build_server(b'./example')