# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/webmpris/views.py
# Compiled at: 2013-11-15 16:40:08
import pympris, json
from django.http import HttpResponse
from django.views.generic import View

def check_player_id(player_id):
    """return True if player_id exists otherwise False"""
    return player_id in pympris.available_players()


def response_json(obj, status):
    """dump obj into json and return HttpResponse with status=status"""
    return HttpResponse(json.dumps(obj), content_type='application/json', status=status)


def get_players(request):
    """view returs list of players ids"""
    items = list(pympris.available_players())
    return response_json(items, status=200)


class Base(View):
    """class implements common functionality
    and used as a base class for other classes
    """
    methods = tuple()
    props = tuple()
    CLS_MPRIS = None

    def instance_by_id(self, player_id):
        """return instance of CLS_MPRIS by player_id"""
        return self.CLS_MPRIS(player_id, private=True)

    def properties(self, player_id):
        """return all properties as a dictionary"""
        obj = self.instance_by_id(player_id)
        d = {}
        for name in self.props:
            try:
                d[name] = getattr(obj, name)
            except pympris.PyMPRISException:
                pass

        return d

    def _method(self, player_id, method_name, *args, **kwd):
        """execute method `method_name`(*args, **kwd) and return result"""
        fn_method = getattr(self.instance_by_id(player_id), method_name)
        return fn_method(*args, **kwd)

    def get(self, request, player_id):
        if not check_player_id(player_id):
            return HttpResponse(json.dumps({'errmsg': 'unknown player id'}), content_type='application/json', status=404)
        return response_json(self.properties(player_id), status=200)

    def post(self, request, player_id, method_name):
        if method_name not in self.methods:
            return response_json({'status': 'fail', 'errmsg': 'unknown method'}, status=404)
        else:
            body = request.body or '{}'
            args = json.loads(body).get('args', [])
            attrs = {'status': 'fail', 'result': None}
            try:
                attrs['result'] = self._method(player_id, method_name, *args)
                attrs['status'] = 'success'
            except pympris.PyMPRISException as err:
                attrs['error'] = str(err)

            return response_json(attrs, status=200)

    def put(self, request, player_id):
        if not check_player_id(player_id):
            return HttpResponse(json.dumps({'errmsg': 'unknown player id'}), content_type='application/json', status=404)
        p = json.loads(request.body)
        obj = self.instance_by_id(player_id)
        errors = []
        for p_name in p:
            try:
                if hasattr(obj, p_name):
                    setattr(obj, p_name, p[p_name])
                else:
                    errors.append({p_name: 'Unknown property'})
            except pympris.PyMPRISException as err:
                message = 'Exception during changing property: ' + str(err)
                errors.append({p_name: message})

        return response_json({'errmsg': errors}, status=200)


class Root(Base):
    """API for org.mpris.MediaPlayer2 interface"""
    CLS_MPRIS = pympris.Root
    methods = ('Raise', 'Quit')
    props = ('CanQuit', 'Fullscreen', 'CanSetFullscreen', 'CanRaise', 'HasTrackList',
             'Identity', 'DesktopEntry', 'SupportedUriSchemes', 'SupportedMimeTypes')


class Player(Base):
    """API for org.mpris.MediaPlayer2.Player interface"""
    CLS_MPRIS = pympris.Player
    methods = ('Next', 'Previous', 'Pause', 'PlayPause', 'Stop', 'Play', 'Seek', 'SetPosition',
               'OpenUri')
    props = ('PlaybackStatus', 'LoopStatus', 'Rate', 'Shuffle', 'Metadata', 'Volume',
             'Position', 'MinimumRate', 'MaximumRate', 'CanGoNext', 'CanGoPrevious',
             'CanPlay', 'CanPause', 'CanSeek', 'CanControl')


class TrackList(Base):
    """API for org.mpris.MediaPlayer2.TrackList interface"""
    CLS_MPRIS = pympris.TrackList
    methods = ('GetTracksMetadata', 'AddTrack', 'RemoveTrack', 'GoTo')
    props = ('Tracks', 'CanEditTracks')


class Playlists(Base):
    """API for org.mpris.MediaPlayer2.Playlists interface"""
    CLS_MPRIS = pympris.PlayLists
    methods = ('ActivatePlaylist', 'GetPlaylists')
    props = ('PlaylistCount', 'Orderings', 'ActivePlaylist')