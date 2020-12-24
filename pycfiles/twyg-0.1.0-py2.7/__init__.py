# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-x86_64/egg/twyg/__init__.py
# Compiled at: 2014-03-15 08:22:53
__version__ = '0.1dev'
import os, sys
from twyg.common import calculate_margins, loadjson
from twyg.config import NODE_CONFIG, CONNECTION_CONFIG, LAYOUT_CONFIG, COLOR_CONFIG, STYLE, DEFAULT_LEVEL, Level, SectionLevel, ConfigError, get_stylename, createlevel, loadconfig, config_path
from twyg.layout import layout_by_name
from twyg.tree import Tree
import twyg.colorizer, twyg.config, twyg.connection, twyg.node
try:
    nodebox = _fullname(_ctx) == 'nodebox.graphics.Context'
except NameError:
    nodebox = False

import twyg.common
if nodebox:
    import inspect, os
    twyg.common.TWYG_HOME = os.path.dirname(os.path.abspath(os.path.join(inspect.getfile(inspect.currentframe()), '..')))
elif 'TWYG_HOME' in os.environ:
    twyg.common.TWYG_HOME = os.environ['TWYG_HOME']
else:
    twyg.common.TWYG_HOME = os.path.join(os.path.expanduser('~'), '.twyg')
_initialized = False

def _fullname(o):
    """ Get the fully qualified class name of an object. """
    module = o.__class__.__module__
    if module is None or module == str.__class__.__module__:
        return o.__class__.__name__
    else:
        return module + '.' + o.__class__.__name__


def _init():
    """
    Autodetect the available drawing backend and initialize the system
    with the correct backend (PyCairo or NodeBox1).
    """
    global _ctx
    global _initialized
    if _initialized:
        return
    if nodebox:
        pass
    else:
        from twyg.cairowrapper import context as _ctx
    twyg.common.init(nodebox=nodebox, ctx=_ctx)
    twyg.config._ctx = _ctx
    twyg.colorizer._ctx = _ctx
    twyg.common._ctx = _ctx
    twyg.connection._ctx = _ctx
    twyg.node._ctx = _ctx
    _initialized = True


def _has_levels(section):
    """ Check if a given configuration section has levels or not. """
    num_dicts = [ x for x in section.values() if type(x) == dict ]
    return len(num_dicts) == len(section)


def _get_style(section, config):
    """
    Get the style name associated with a given configuration
    section.
    """
    style = get_stylename(section, config)
    del config[STYLE]
    return style


def _create_drawers(config, section, factory_func, constr_args=()):
    """
    Create a list of SectionLevel objects for a given configuration
    section from a full configuration.
    """
    c = config[section]
    level_dict = c if _has_levels(c) else {DEFAULT_LEVEL: c}
    drawers = []
    for levelname, conf in level_dict.iteritems():
        style = _get_style(section + '.' + levelname, conf)
        level = createlevel(levelname, conf)
        drawer_class = factory_func(style)
        drawer = drawer_class(conf, *constr_args)
        drawers.append(SectionLevel(level, drawer))

    return drawers


def get_scale_factor(dpi, scale):
    return dpi / 72.0 * scale


def generate_output(data_fname, config_fname, out_fname, outformat, colorscheme=None, scale=1.0, margins=['10%', '5%']):
    """
    TODO
    """
    tree = _buildtree(data_fname, config_fname, colorscheme)
    _ctx.initsurface(1, 1, outformat, None, scale)
    width, height = tree.calclayout()
    padtop, padleft, padbottom, padright = calculate_margins(width, height, margins)
    width += padleft + padright
    height += padtop + padbottom
    tree.shiftnodes(padleft, padtop)
    _ctx.initsurface(width, height, outformat, out_fname, scale)
    _ctx.background(tree.background_color())
    tree.draw()
    _ctx.writesurface()
    return


def generate_output_nodebox(data_fname, config_fname, colorscheme=None, margins=[
 '10%', '5%']):
    tree = _buildtree(data_fname, config_fname, colorscheme)
    width, height = tree.calclayout()
    padtop, padleft, padbottom, padright = calculate_margins(width, height, margins)
    width += padleft + padright
    height += padtop + padbottom
    tree.shiftnodes(padleft, padtop)
    _ctx.size(width, height)
    _ctx.background(tree.background_color())
    tree.draw()


def _buildtree(data_fname, config_fname, colorscheme):
    data = loadjson(data_fname)
    config = loadconfig(config_path(config_fname))
    return twyg.buildtree(data, config, colorscheme)


def buildtree(data, config, colorscheme_path=None):
    """
    # TODO
    Build a `Tree` object from a nested tree data structure according to
    the rules specified in the configuration and apply a colorscheme.

    This method does not perform the actual tree layouting and drawing;
    it stops after creating a ``Tree`` object initialized with the
    correct drawer objects.

    `data`
         Hierarchical tree structure (dicts, lists, TODO)

    `config'
        Tree visualisation configuration.

    `colorscheme_path`
        Colorscheme to use.
    """
    _init()
    section = LAYOUT_CONFIG
    c = config[section]
    if _has_levels(c):
        raise Exception('Layout section cannot have levels')
    style = _get_style(section, c)
    layout_cls = layout_by_name(style)
    layout = layout_cls(c)
    nodedrawers = _create_drawers(config, NODE_CONFIG, factory_func=twyg.node.nodedrawer_by_name)
    conndrawers = _create_drawers(config, CONNECTION_CONFIG, factory_func=twyg.connection.conndrawer_by_name)
    colorizers = _create_drawers(config, COLOR_CONFIG, factory_func=twyg.colorizer.colorizer_by_name, constr_args=(
     colorscheme_path,))
    return Tree(layout, nodedrawers, conndrawers, colorizers, data)