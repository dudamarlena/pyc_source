# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/higlass/viewer.py
# Compiled at: 2020-01-26 00:21:31
# Size of source mod 2**32: 7165 bytes
import json, logging, ipywidgets as widgets
from traitlets import Bool, Dict, Float, Int, List, Unicode, Union
import slugid
from ._version import __version__
import os, threading, time

def save_b64_image_to_png(filename, b64str):
    """Save a base64 encoded image to a file."""
    import base64
    imgdata = base64.b64decode(b64str.split(',')[1])
    with open(filename, 'wb') as (f):
        f.write(imgdata)


@widgets.register
class HiGlassDisplay(widgets.DOMWidget):
    _view_name = Unicode('HiGlassDisplayView').tag(sync=True)
    _model_name = Unicode('HiGlassDisplayModel').tag(sync=True)
    _view_module = Unicode('higlass-jupyter').tag(sync=True)
    _model_module = Unicode('higlass-jupyter').tag(sync=True)
    _view_module_version = Unicode(__version__).tag(sync=True)
    _model_module_version = Unicode(__version__).tag(sync=True)
    _model_data = List([]).tag(sync=True)
    viewconf = Dict({}).tag(sync=True)
    height = Int().tag(sync=True)
    dom_element_id = Unicode(read_only=True).tag(sync=True)
    location = List((Union([Float(), List()])), read_only=True).tag(sync=True)
    cursor_location = List([], read_only=True).tag(sync=True)
    selection = List([], read_only=True).tag(sync=True)
    auth_token = Unicode().tag(sync=True)
    bounded = Bool(None, allow_none=True).tag(sync=True)
    default_track_options = Dict({}).tag(sync=True)
    dark_mode = Bool(False).tag(sync=True)
    renderer = Unicode().tag(sync=True)
    select_mode = Bool(False).tag(sync=True)
    selection_on_alt = Bool(False).tag(sync=True)
    options = Dict({}).tag(sync=True)

    def __init__(self, **kwargs):
        self.on_msg(self._handle_js_events)
        self.callbacks = {}
        (super(HiGlassDisplay, self).__init__)(**kwargs)

    def get_base64_img(self, callback):
        uuid = slugid.nice()
        self.callbacks[uuid] = callback
        self.send(json.dumps({'request':'save_as_png',  'params':{'uuid': uuid}}))

    def _handle_js_events(self, widget, content, buffers=None):
        try:
            if self.callbacks[content['params']['uuid']]:
                self.callbacks[content['params']['uuid']](content['imgData'])
                del self.callbacks[content['params']['uuid']]
        except Exception as e:
            try:
                self.log.error(e)
                self.log.exception('Unhandled exception while handling msg')
            finally:
                e = None
                del e


def display(views, location_syncs=[], value_scale_syncs=[], zoom_syncs=[], host='localhost', server_port=None, dark_mode=False, log_level=logging.ERROR, fuse=True, auth_token=None):
    """
    Instantiate a HiGlass display with the given views.

    Args:
        views: A list of views to display. If the items in the list are
            lists themselves, then automatically create views out of them.
        location_syncs: A list of lists, each containing a list of views which
            will scroll together.
        zoom_syncs: A list of lists, each containing a list of views that
            will zoom together.
        host: The host on which the internal higlass server will be running on.
        server_port: The port on which the internal higlass server will be running on.
        dark_mode: Whether to use dark mode or not.
        log_level: Level of logging to perform.
        fuse: Whether to mount the fuse filesystem. Set to false if not loading any
            data over http or https.

    Returns:
        (display: HiGlassDisplay, server: higlass.server.Server, higlass.client.viewconf) tuple
        Display is an object used to create
        a HiGlass viewer within a Jupyter notebook. The server object encapsulates
        a Flask instance of a higlass server and the viewconf is a Python object
        containing the viewconf describing the higlass dashboard.
    """
    from .server import Server
    from .client import CombinedTrack, DividedTrack, View, ViewConf, ViewportProjection
    tilesets = []
    new_views = []
    for view in views:
        if isinstance(view, (tuple, list)):
            new_views.append(View(view))
        else:
            new_views.append(view)

    views = new_views
    for view in views:
        for track in view.tracks:
            if hasattr(track, 'tracks'):
                for track1 in track.tracks:
                    if isinstance(track1, ViewportProjection) or track1.tileset:
                        tilesets += [track1.tileset]

            if track.tileset:
                tilesets += [track.tileset]

    server = Server(tilesets,
      host=host, port=server_port, fuse=fuse, log_level=log_level)
    server.start()
    cloned_views = [View.from_dict(view.to_dict()) for view in views]
    for view in cloned_views:
        for track in view.tracks:
            if isinstance(track, CombinedTrack):
                for track1 in track.tracks:
                    if 'fromViewUid' in track1.conf:
                        continue
                    if not 'server' not in track1.conf:
                        if track1.conf['server'] is None:
                            pass
                        track1.conf['server'] = server.api_address

            else:
                if 'fromViewUid' in track.conf:
                    continue
                if 'data' in track.conf:
                    continue
                if not 'server' not in track.conf:
                    if track.conf['server'] is None:
                        pass
                track.conf['server'] = server.api_address

    viewconf = ViewConf(cloned_views,
      location_syncs=location_syncs,
      value_scale_syncs=value_scale_syncs,
      zoom_syncs=zoom_syncs)
    extra_args = {}
    if auth_token:
        extra_args['auth_token'] = auth_token
    return (
     HiGlassDisplay(viewconf=viewconf.to_dict(), 
      hg_options={'theme': 'dark' if dark_mode else 'light'}, **extra_args),
     server,
     viewconf)