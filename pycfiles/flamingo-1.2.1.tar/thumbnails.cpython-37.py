# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/fsc/work/devel/flamingo/flamingo/plugins/thumbnails.py
# Compiled at: 2020-04-28 06:15:31
# Size of source mod 2**32: 8933 bytes
from collections import OrderedDict
import hashlib, logging, re, os
try:
    from docutils.parsers.rst import directives
    RST = True
except ImportError:
    RST = False

from PIL import Image as PillowImage
from flamingo.core.data_model import Content
logger = logging.getLogger('flamingo.plugins.Thumbnails')
DEFAULT_THUMBNAIL_CACHE = 'thumbs'
DIMENSION_RE = re.compile('^([0-9]{1,})(px)?$')

def parse_bool(value):
    value = value.lower()
    values = {'false':False, 
     'true':True, 
     '0':False, 
     '1':True}
    if value not in values:
        return False
    return values[value]


def parse_dimensions(dimension):
    if isinstance(dimension, int):
        return dimension
    try:
        return int(DIMENSION_RE.search(dimension).groups()[0])
    except Exception:
        return 0


def hash_image(path, options):
    options = OrderedDict(options)
    stream = b''
    for k, v in options.items():
        stream += '{}={},'.format(k, v).encode()

    stream += open(path, 'rb').read()
    return hashlib.md5(stream).hexdigest()


def scale_image(original_size, width=None, height=None):
    if width:
        if height:
            return (
             int(width), int(height))
    original_width, original_height = original_size
    if width:
        width_percentage = width / original_width * 100
        height = original_height * (width_percentage / 100)
        return (
         width, int(height))
    if height:
        height_percentage = height / original_height * 100
        width = original_width * (height_percentage / 100)
        return (
         int(width), height)
    return original_size


class Thumbnails:
    THEME_PATHS = [
     os.path.join(os.path.dirname(__file__), 'theme')]

    def settings_setup(self, context):
        THUMBNAIL_CACHE = getattr(context.settings, 'THUMBNAIL_CACHE', DEFAULT_THUMBNAIL_CACHE)
        context.settings.LIVE_SERVER_IGNORE_PREFIX.append(os.path.join(context.settings.CONTENT_ROOT, THUMBNAIL_CACHE))
        if RST:
            logger.debug("setting up 'thumbnail' option for rst images")
            if not hasattr(context.settings, 'RST_IMAGE_EXTRA_OPTION_SPEC'):
                context.settings.RST_IMAGE_EXTRA_OPTION_SPEC = {}
            context.settings.RST_IMAGE_EXTRA_OPTION_SPEC['thumbnail'] = directives.unchanged
        else:
            logger.debug('docutils seems to be not installed. setup skipped')

    def media_added(self, context, content, media_content):
        logger.debug('processing %s:%s', content['path'] or content, media_content['path'] or media_content)
        if media_content['is_thumbnail'] or media_content['original']:
            logger.debug('setup of thumbnail for %s:%s skipped: image is already a thumbnail', content['path'], media_content['path'])
            return
        if media_content['type'] != 'media/image':
            logger.debug("setup of thumbnail for %s:%s skipped: type is not 'media/image'", content['path'], media_content['path'])
            return
        if 'thumbnail' in media_content:
            if not parse_bool(media_content['thumbnail']):
                logger.debug('setup of thumbnail for %s:%s skipped: disabled by option', content['path'], media_content['path'])
                return
        if not media_content['width']:
            if not media_content['height']:
                logger.debug('setup of thumbnail for %s:%s skipped: no dimensions set', content['path'], media_content['path'])
                return
        width = parse_dimensions(media_content['width'])
        height = parse_dimensions(media_content['height'])
        path = os.path.join(context.settings.CONTENT_ROOT, media_content['path'])
        try:
            image = PillowImage.open(path)
        except FileNotFoundError:
            logger.error('%s not found. Used in %s', path, media_content['content']['path'])
            return
        else:
            width, height = scale_image((image.size), width=width, height=height)
            media_content['width'] = width
            media_content['height'] = height
            image_hash = hash_image(os.path.join(context.settings.CONTENT_ROOT, media_content['path']), {'width':media_content['width'], 
             'height':media_content['height']})
            logger.debug('setup thumbnail for %s:%s (%s)', content['path'], media_content['path'], image_hash)
            image_name, image_extension = os.path.splitext(media_content['output'])
            thumbnail_path = os.path.join(getattr(context.settings, 'THUMBNAIL_CACHE', DEFAULT_THUMBNAIL_CACHE), '{}{}'.format(image_hash, image_extension))
            thumbnail_output = '{}.thumb{}'.format(image_name, image_extension)
            thumbnail_url = '/' + thumbnail_output
            original_content = Content(url=(media_content['url']),
              path=(media_content['path']),
              output=(media_content['output']),
              thumbnail=False)
            content['media'].add(original_content)
            media_content['path'] = thumbnail_path
            media_content['output'] = thumbnail_output
            media_content['url'] = thumbnail_url
            media_content['is_thumbnail'] = True
            media_content['original'] = original_content
            original_content['thumbnail'] = media_content
            if context.settings.LIVE_SERVER_RUNNING:
                return
            self.gen_thumbnail(context, media_content, image=image)

    def gen_thumbnail(self, context, media_content, image=None):
        if not image:
            path = os.path.join(context.settings.CONTENT_ROOT, media_content['original']['path'])
            try:
                image = PillowImage.open(path)
            except FileNotFoundError:
                logger.error('%s not found. Used in %s', path, media_content['original']['content']['path'])
                return

            output = os.path.join(context.settings.CONTENT_ROOT, media_content['path'])
            if os.path.exists(output):
                return
        elif not media_content['width']:
            logger.error("%s: invalid width '%s'", media_content['original']['path'], media_content['width'])
        else:
            media_content['height'] or logger.error("%s: invalid height '%s'", media_content['original']['path'], media_content['height'])
            return media_content['width'] or None
        context.mkdir_p(output, force=True)
        image.thumbnail((media_content['width'], media_content['height']))
        image.save(output)

    def render_media_content(self, context, media_content):
        if not media_content['is_thumbnail']:
            return
        self.gen_thumbnail(context, media_content)

    def post_build(self, context):
        THUMBNAIL_CACHE = os.path.join(context.settings.CONTENT_ROOT, context.settings.get('THUMBNAIL_CACHE', DEFAULT_THUMBNAIL_CACHE))
        THUMBNAIL_REMOVE_ORPHANED = context.settings.get('THUMBNAIL_REMOVE_ORPHANED', True)
        if not THUMBNAIL_REMOVE_ORPHANED:
            return
        else:
            return os.path.exists(THUMBNAIL_CACHE) or None
        thumbnails = []
        for content in context.contents:
            if not content['media']:
                continue
            for media_content in content['media']:
                if media_content['is_thumbnail']:
                    path = os.path.join(context.settings.CONTENT_ROOT, media_content['path'])
                    thumbnails.append(path)

        for path in os.listdir(THUMBNAIL_CACHE):
            path = os.path.join(THUMBNAIL_CACHE, path)
            if path not in thumbnails:
                logger.info('removing orphaned %s', path)
                context.rm_rf(path, force=True)