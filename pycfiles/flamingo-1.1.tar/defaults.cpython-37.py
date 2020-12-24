# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/fsc/work/devel/flamingo/flamingo/core/settings/defaults.py
# Compiled at: 2020-03-29 11:07:54
# Size of source mod 2**32: 1565 bytes
import flamingo
CORE_PLUGINS_PRE = [
 'flamingo.core.plugins.layers.PreBuildLayers',
 'flamingo.core.plugins.MetaDataDefaults']
DEFAULT_PLUGINS = [
 'flamingo.plugins.HTML',
 'flamingo.plugins.Yaml',
 'flamingo.plugins.reStructuredText',
 'flamingo.plugins.rstInclude',
 'flamingo.plugins.rstImage',
 'flamingo.plugins.rstFile',
 'flamingo.plugins.rstLink']
PLUGINS = []
CORE_PLUGINS_POST = [
 'flamingo.core.plugins.Media',
 'flamingo.core.plugins.Static',
 'flamingo.core.plugins.layers.PostBuildLayers']
SKIP_HOOKS = []
USE_CHARDET = False
DEDENT_INPUT = False
FOLLOW_LINKS = True
HTML_PARSER_RAW_HTML = False
TEMPLATING_ENGINE = 'flamingo.core.templating.Jinja2'
PRE_RENDER_CONTENT = True
EXTRA_CONTEXT = {}
CORE_THEME_PATHS = [
 flamingo.THEME_ROOT]
THEME_PATHS = []
DEFAULT_TEMPLATE = 'page.html'
DEFAULT_IMAGE_TEMPLATE = 'image.html'
DEFAULT_GALLERY_TEMPLATE = 'gallery.html'
DEFAULT_CODE_BLOCK_TEMPLATE = 'code-block.html'
DEFAULT_PAGINATION = 25
JINJA2_EXTENSIONS = []
JINJA2_TRACEBACKS = True
JINJA2_TRACEBACKS_CONTEXT_LINES = 3
JINJA2_TRACEBACKS_FILTER_PYTHON_CODE = True
JINJA2_TRACEBACKS_PYGMENTS = True
SKIP_FILE_OPERATIONS = False
CONTENT_ROOT = 'content'
CONTENT_PATHS = []
OUTPUT_ROOT = 'output'
MEDIA_ROOT = 'media'
STATIC_ROOT = 'output/static'
PRE_BUILD_LAYERS = []
POST_BUILD_LAYERS = []
LIVE_SERVER_RUNNING = False
LIVE_SERVER_IGNORE_PREFIX = []
LIVE_SERVER_RESETUP_ON_CODE_CHANGE = False