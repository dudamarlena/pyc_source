# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/coils/protocol/dav/workflow/utility.py
# Compiled at: 2012-10-12 07:02:39
import os
from xml.sax import make_parser
from xml.sax.handler import ContentHandler
from coils.core import *
from coils.logic.workflow import BPMLSAXHandler

def filename_for_route_markup(route, version):
    return ('wf/r/{0}.{1}.bpml').format(route.name, version)


def filename_for_process_markup(process):
    return ('wf/p/{0}.bpml').format(process.object_id)


def filename_for_process_code(process, version):
    return ('wf/p/{0}.{1}.cpm').format(process.object_id, version)


def route_versions(route):
    versions = []
    edition = 0
    while edition < route.version:
        edition = edition + 1
        if BLOBManager.Exists(filename_for_route_markup(route, edition)):
            versions.append(str(edition))

    return versions


def process_versions(process):
    versions = []
    edition = 0
    while edition < process.version:
        edition = edition + 1
        if BLOBManager.Exists(filename_for_process_code(process, edition)):
            versions.append(str(edition))

    return versions


def compile_bpml(_file, log=None):
    cpm = None
    try:
        _file.seek(0)
        parser = make_parser()
        handler = BPMLSAXHandler()
        parser.setContentHandler(handler)
        parser.parse(_file)
        cpm = handler.get_processes()
        if log:
            log.debug('Successfully processed BPML document')
        if '__namespace__' in cpm:
            description = {'name': cpm['__namespace__']}
            if log:
                log.debug('Determined namespace of BPML document')
        else:
            if log:
                log.warn('No namespace defined in BPML document')
            description = 'Unnamed route'
    except Exception, e:
        if log:
            log.warn(('Processing of BPML document at {0} failed.').format(_filename))
            log.exception(e)
        raise CoilsException('Processing BPML document failed.')
    else:
        return (
         description, cpm)

    return