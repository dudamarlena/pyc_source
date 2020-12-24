# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-fat/egg/tgmochikit/base.py
# Compiled at: 2008-10-26 13:30:23
import pkg_resources, os, glob, logging
logger = logging.getLogger(('.').join(__name__.split('.')[:-1]))
VERSION = '1.3.1'
INITIALIZED = False
PACKED = False
XHTML = False
SUBMODULES = []
PATHS = []
DRAGANDDROP = False

def init(register_static_directory, config={}, version=None, packed=None, xhtml=None, draganddrop=None):
    """Initializes the MochiKit resources.

    The parameter register_static_directory is somewhat hackish: because this
    init is called during initialization of turbogears.widgets itself,
    register_static_directory isn't importable. So we need to pass it as
    argument.

    """
    global DRAGANDDROP
    global INITIALIZED
    global PACKED
    global PATHS
    global VERSION
    global XHTML
    if not INITIALIZED:
        if version is not None:
            VERSION = version
        if packed is not None:
            PACKED = packed
        if xhtml is not None:
            XHTML = xhtml
        if draganddrop is not None:
            DRAGANDDROP = draganddrop
        INITIALIZED = True
        PACKED = config.get('tg_mochikit.packed', PACKED)
        VERSION = config.get('tg_mochikit.version', VERSION)
        XHTML = config.get('tg_mochikit.xhtml', XHTML)
        DRAGANDDROP = config.get('tg_mochikit.draganddrop', DRAGANDDROP)
        is_131 = '1.3.1' in VERSION
        js_base_dir = pkg_resources.resource_filename('tgmochikit', 'static/javascript/')
        if os.path.exists(os.path.join(js_base_dir, VERSION)):
            js_dir = os.path.join(js_base_dir, VERSION)
        else:
            candidates = glob.glob(os.path.join(js_base_dir, '%s*' % VERSION))
            candidates.sort()
            js_dir = candidates[(-1)]
        logger.info('MochiKit version chosen: %s', os.path.basename(js_dir))
        path = os.path.join(js_dir, 'unpacked', '*.js')
        for name in glob.glob(path):
            module = os.path.basename(name)
            if '__' not in name and 'MochiKit' not in module:
                SUBMODULES.append(module)

        register_static_directory('tgmochikit', js_dir)
        if PACKED:
            PATHS = [
             'packed/MochiKit/MochiKit.js']
        else:
            res = [
             'unpacked/MochiKit.js']
            if XHTML:
                for submodule in SUBMODULES:
                    res.append('unpacked/%s' % submodule)

            PATHS = res
        if DRAGANDDROP and not is_131:
            PATHS.append('unpacked/DragAndDrop.js')
    return


def get_paths():
    return PATHS


def get_shipped_versions():
    js_base_dir = pkg_resources.resource_filename('tgmochikit', 'static/javascript/')
    return [ os.path.basename(p) for p in glob.glob(os.path.join(js_base_dir, '*')) ]