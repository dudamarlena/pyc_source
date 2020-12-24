# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/mishmash/web/panels.py
# Compiled at: 2019-12-04 00:39:07
# Size of source mod 2**32: 2024 bytes
import random
from pyramid_layout.panel import panel_config
from ..__about__ import __version__, __years__, __project_name__
from .. import orm

@panel_config(name='navbar', renderer='mishmash.web:templates/panels/navbar.pt')
def navbar(context, request):
    return {}


@panel_config(name='footer')
def footer(context, request):
    return f"""\n<footer class="text-muted">\n  <div class="container">\n    <p class="float-right">\n      <a href="#">Back to top</a>\n    </p>\n    <p><br/></p>\n    <p align=\'right\'>{__project_name__} {__version__} &copy; {__years__}</p>\n  </div>\n</footer>\n"""


@panel_config(name='album_cover')
def album_cover(context, request, album, size=None, link=False):
    front_covers = [img for img in album.images if img.type == orm.Image.FRONT_COVER_TYPE]
    cover_id = random.choice(front_covers).id if front_covers else 'default'
    cover_url = request.route_url('images.covers', id=cover_id)
    width = str(size or '100%')
    height = str(size or '100%')
    panel = "<img class='shadow' width='%s' height='%s' src='%s' title='%s'/>" % (
     width, height, cover_url, '%s - %s' % (album.artist.name, album.title))
    if link:
        panel = "<a href='%s'>%s</a>" % (
         request.route_url('album', id=(album.id)), panel)
    return panel


@panel_config(name='artist_image')
def artist_image(context, request, artist, scale_percent=None, link=False):
    imgs = [img for img in artist.images]
    if not imgs:
        return ''
    width = str(scale_percent or '100%')
    height = str(scale_percent or '100%')
    img_url = request.route_url('images.artist', id=(random.choice(imgs).id))
    panel = f"<img class='shadow' width='{width}' height='{height}' src='{img_url}' title='{artist.name}'/>"
    if link:
        panel = f"<a href='{request.route_url('artist', id=(artist.id))}'>{panel}</a>"
    return panel