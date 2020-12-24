# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: ./src/utils/racovimge.py
# Compiled at: 2020-01-01 14:22:44
# Size of source mod 2**32: 3237 bytes
"""
Original source: https://github.com/anqxyr/racovimge
"""
import base64, html, logging, os, random as rand, textwrap
from pathlib import Path
from jinja2 import Environment, FileSystemLoader
logger = logging.getLogger('RACOVIMGE')
ROOT = Path(__file__).parent.parent / 'assets'
templates = [i.stem for i in (ROOT / 'templates').glob('*.svg')]
fonts = ROOT / 'fonts'
fonts = [str(i) for i in fonts.glob('*.*') if i.suffix in ('.ttf', '.otf')]
with (ROOT / 'colors.txt').open() as (file):
    color_schemes = [i.split() for i in file.read().split('\n')]

def to_rgb(color):
    color = color.lstrip('#')
    r, g, b = map(lambda x: int(x, 16), [color[:2], color[2:4], color[4:]])
    return 'rgb({},{},{})'.format(r, g, b)


def wrap(text, width):
    if not isinstance(text, str):
        return text
    else:
        return textwrap.wrap(text,
          break_long_words=False, break_on_hyphens=False, width=width)


template_dir = os.path.abspath(str(ROOT / 'templates'))
env = Environment(loader=FileSystemLoader(searchpath=template_dir))
env.filters['wrap'] = wrap
env.filters['rgb'] = to_rgb

def random_cover(title, author):
    font_size_title = 96
    font_size_author = 48
    font = rand.choice(fonts)
    template = rand.choice(templates)
    colors = rand.choice(color_schemes)
    color1, color2, color3, color4, color5 = colors
    title = html.escape(title)
    author = html.escape(author)
    author = author.split(', ') if isinstance(author, str) else author
    authors = [author] if isinstance(author, str) else author
    authors = authors[:3] if authors else []
    font_mimetypes = dict(otf='font/opentype',
      ttf='application/x-font-ttf')
    font = Path(font)
    with font.open('rb') as (file):
        font_data = file.read()
        font_data = base64.b64encode(font_data).decode('utf-8')
    font_name = font.stem
    font_type = font_mimetypes[font.suffix.lstrip('.')]
    kargs = dict(title=title,
      authors=authors,
      font=font_name,
      font_type=font_type,
      font_data=font_data,
      color1=color1,
      color2=color2,
      color3=color3,
      color4=color4,
      color5=color5,
      font_size=font_size_title,
      font_size_author=font_size_author)
    logger.debug('Cover image: template = %s, font = %s [%s]', template, font_name, font_type)
    return (env.get_template(template + '.svg').render)(**kargs)