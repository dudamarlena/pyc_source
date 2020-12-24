# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/audman/audws.py
# Compiled at: 2015-09-22 23:03:07
import socket, sys, os, time, getopt, re, traceback, threading, signal
from pkg_resources import resource_filename
from wsgiref.simple_server import WSGIServer, WSGIRequestHandler
from wsgiref import simple_server
from cgi import parse_qs, escape
from mako.template import Template
import aud_dbus

def guess_listening_addr():
    """Guess what address is used when listening with host= ''"""
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(('8.8.8.8', 0))
    except Exception as err:
        print traceback.format_exc()
        s = None

    if s is not None:
        ip = s.getsockname()[0]
    else:
        addrs = [ ip for ip in socket.gethostbyname_ex(socket.gethostname())[2] if not ip.startswith('127.')
                ][:1]
        if len(addrs) > 0:
            ip = addrs[0]
        else:
            ip = socket.gethostname()
    return ip


def codec_shortname(longname):
    if longname.startswith('MPEG-1 layer 3'):
        return 'MP3'
    else:
        if longname.startswith('Free Lossless Audio Codec'):
            return 'FLAC'
        if longname.startswith('Microsoft WAV'):
            return 'WAV'
        if longname.startswith('MPEG-2'):
            return 'MP2'
        return ('').join(re.findall('[A-Z]{3,5}', longname))


def chn_form_shortname(nch):
    if nch > 2 or nch < 1:
        return '%d.1' % nch
    return [
     'mono', 'stereo'][(nch - 1)]


class LogErrorHandler(simple_server.WSGIRequestHandler):

    def log_request(self, *args):
        pass


class AudmanagerServer(WSGIServer):
    kill_thread = None
    default_pl_mode = 'play'
    playlists_locked = False
    DEFAULT_VOL_DELTA = 8
    DEFAULT_TRACKLIST_LEN = 6

    def __init__(self, address, app, handler_class=WSGIRequestHandler):
        WSGIServer.__init__(self, address, handler_class)
        self.set_app(app)
        self.allow_reuse_address = True
        AudmanagerServer.kill_thread = threading.Thread(target=self.shutdown)

    @staticmethod
    def clean_exit(unused_signo=None, unused_frame=None):
        if not AudmanagerServer.kill_thread.isAlive():
            AudmanagerServer.kill_thread.start()
        AudmanagerServer.kill_thread.join()
        print ' Caught interrupt, exiting'
        sys.exit(0)

    tr_list = Template(output_encoding='utf-8', text='<!DOCTYPE html>\n<html>\n  <head>\n      <meta charset="utf-8">\n      <meta http-equiv="refresh" content="10"> \n      <meta name="viewport" \n          content="width=device-width, initial-scale=1.0, user-scalable=yes">\n      <title>${current_title if current_title else \'AudPage\'}</title>\n      <style>\n        body {background-color:#dcdad5;}\n        table.track-list {border: 1px solid black; width:100%;}\n        b.f8 {display:inline-block; width:5em; float: left;}\n        .nowrap {\n            white-space: nowrap;\n        }\n        td.current-track-name {background-color:#acbac6;}\n        span.rightfloat {float: right;}\n        button.pl_enq0 {width: 100%; text-align: left;background-color:hsl(208, 19%, 70%)}\n        button.pl_enq1 {width: 100%; text-align: left;background-color:hsl(208, 19%, 75%)}\n        button.pl_enq2 {width: 100%; text-align: left;background-color:hsl(208, 19%, 80%)}\n        button.pl_enq3 {width: 100%; text-align: left;background-color:hsl(208, 19%, 85%)}\n        button.pl_enq4 {width: 100%; text-align: left;background-color:hsl(208, 19%, 90%)}\n        button.pl_enq5 {width: 100%; text-align: left;background-color:hsl(208, 19%, 95%)}\n        meter {width: 14em;}\n        button.pl_ctl {height: 4em;}\n        button.pl_ctl_grey {height: 4em;opacity: 0.5;}\n        button.up {\n            border-top: solid 2px #eaeaea;\n            border-left: solid 2px #eaeaea;\n            border-bottom: solid 2px #777;\n            border-right: solid 2px #777;\n        }\n        button.down {\n            background: #bbb;\n            border-top: solid 2px #777;\n            border-left: solid 2px #777;;\n            border-bottom:solid 2px #eaeaea;\n            border-right: solid 2px #eaeaea;\n        }\n        button.plplay {width: 100%; text-align: left;}\n        select.pl_select {font-size: 110%; font-weight: normal;}       \n        /* slider; larger thumb */\n        input[type=range]{\n            -webkit-appearance: none;\n        }\n        input[type=range]::-webkit-slider-thumb {\n          -webkit-appearance: none;\n          border: 1px solid #000000;\n          height: 1.6em;\n          width: 2em;\n          border-radius: 3px;\n          background: #dcdad5;\n          cursor: pointer;\n          box-shadow: 1px 1px 1px #000000, 0px 0px 1px #0d0d0d; /* Add cool effects to your sliders! */\n        }\n\n        input[type=range]::-webkit-slider-runnable-track {\n            width: 6em;\n            height: 1.6em;\n            background: #dcdad5;\n            background-color: grey;\n            border: none;\n            border-radius: 3px;\n        }\n\n        input[type=range]:focus {\n            outline: none;\n        }\n\n        /* All the same stuff for Firefox */\n        input[type=range]::-moz-range-thumb {\n          box-shadow: 1px 1px 1px #000000, 0px 0px 1px #0d0d0d;\n          border: 1px solid #000000;\n          height: 1.6em;\n          width: 2em;\n          background: #dcdad5;\n          border-radius: 3px;\n          cursor: pointer;\n        }\n      </style>\n      <script>\n        function zfill(num, len) {\n          return (Array(len).join("0")+num).slice(-len);}\n        function min_sec_pos(secs) {return zfill(Math.floor(secs/60),2) + ":" \n           + zfill(secs%60,2) + "/" + zfill(Math.floor(${track_length} / 60),2) \n           +  ":" + zfill(${track_length} % 60,2);}\n      </script>\n  </head>\n<body>\n<h3>Audacious Control Page on ${hostname}</h3>\n<form name="aud_control" method="post" action="">\n<div class="control_panel">\n<button class="pl_ctl" name="control" type="submit" value="playpause"\n     title="Toggle Pause/Playback">\n  <img src="${state_play_pause}" id="Prev"/>\n</button>\n<button class="pl_ctl" name="control" type="submit" value="pl_prev"\n    title="Prev">\n  <img src="ic_skip_previous_black_48dp.png" id="Prev"/>\n</button>\n<button class="pl_ctl" name="control" type="submit" value="pl_next"\n     title="Next">\n  <img src="ic_skip_next_black_48dp.png" id="Next"/>\n</button>\n<button name="control" type="submit" \n  id="pl_toggle_repeat" value="pl_repeat" \n     % if is_repeat:\n       class="down" title="Stop Repeat">\n     % else:\n       class="up" title="Start Repeat">\n     % endif\n  <img src="ic_repeat_black_48dp.png" id="repeat"/>\n</button>\n<button name="control" type="submit" \n  id="pl_toggle_shuffle" value="pl_shuffle" \n     % if is_shuffle:\n       class="down" title="Stop Shuffle Advance">\n     % else:\n       class="up" title="Start Shuffle Advance">\n     % endif\n  <img src="ic_shuffle_black_48dp.png" id="shuffle"/>\n</button>\n<span name="vol" class="nowrap">\n<button name="control" type="submit" value="volume_down"\n     % if volume == 0:\n       class="pl_ctl_grey"\n       disabled="disabled"\n     % else:\n       class="pl_ctl"\n     % endif\n     title="Decrease volume">\n <img class="icon" src="ic_volume_down_black_48dp.png"/>\n</button>\n<button name="control" type="submit" value="volume_up"\n     % if volume == 100:\n       class="pl_ctl_grey"\n       disabled="disabled"\n     % else:\n       class="pl_ctl"\n     % endif\n     title="Increase volume">\n  <img class="icon" src="ic_volume_up_black_48dp.png"/>\n</button>\n</span>\n</div>\n</form>\n<div>\n<b>Current Track: </b>${current_title}\n<br>\n<form name="seek-bar" method="post" action="">\n<table>\n<tr><td>\n<b class="f8">${state}: </b>\n</td><td>\n<input type="range" class="seek-bar" name="seek_control" min="0"\n  max="${track_length}" onchange="this.form.submit();" id="seek-bar" \n  value="${track_pos}" oninput="document.getElementById(\'seek_pos\').innerHTML=min_sec_pos(this.value)" title="Adjust playback position"/> \n</td> <td>\n<span id="seek_pos">${current_track_pos}</span> ${audio_info}\n</td></tr>\n</table>\n</form>\n</div>\n<form name="control_track" id="playlist" method="post" action=""></form>\n<table class="track-list">\n<tr>\n% if not playlists_lock:\n<td><form name="control_pl" method="post" action="">\n<span name="pl_jump_control" class="nowrap">\n<label for="pl_select"><b>Playlist:</b></label>\n<select class="pl_select" id="pl_select" name="pl_control" type="submit"\n  onchange="this.form.submit();" title="Select playlist">\n  % for ind, pl_name in play_lists:\n     <option value="${ind}"\n     % if ind == active_pl_ind:\n       selected="selected"\n     % endif\n     >${pl_name}</option>\n  % endfor\n</select>\n</spen>\n</form>\n</td>\n% endif\n<td>\n<form name="manage_tracklist" method="get" action="">\n<span name="pl_jump_control" class="nowrap">\n<label for="pl_jump_mode"><b>Click to:</b></label>\n<select name="pl_jump_mode" class="pl_select" type="submit" \n  onchange="this.form.submit();">\n  <option value="play"\n     % if pl_mode == "play":\n       selected="selected"\n     % endif\n  >play</option>\n  <option value="enque"\n     % if pl_mode == "enque":\n       selected="selected"\n     % endif\n  >enque</option>\n</select>\n</span>\n<input type="hidden" name="size" value="${tl_size}" />\n<button class="tr-ctrl" name="size_up" id="size_more" type="submit"\n  onclick="this.form.size.value = this.value"\n         value="${tl_size * 2}" \n         title="Display a longer tracklist">\n  <img class="sm-icon" src="ic_unfold_more_black_24dp.png"/>\n</button>\n<button class="tr-ctrl" name="size_down" id="size_less" type="submit"\n  onclick="this.form.size.value = this.value"\n         value="${tl_size / 2}" \n         title="Display a shorter tracklist">\n  <img class="sm-icon" src="ic_unfold_less_black_24dp.png"/>\n</button>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;\n<span name="scroll" class="nowrap">\n<input type="hidden" name="offset" value="${tl_offset}" />\n<button class="tr-ctrl" name="offset_up" id="scroll_up" type="submit"\n  onclick="this.form.offset.value = this.value"\n         value="${tl_offset - 1}" \n         title="Scroll tracklist Up">\n  <img class="sm-icon" src="ic_arrow_drop_up_black_24dp.png"/>\n</button>\n<button class="tr-ctrl" name="offset_reset" id="scroll_down" type="submit"\n  onclick="this.form.offset.value = 0"\n         value="0" \n         title="Reset tracklist Scrolling">\n  <img class="sm-icon" src="ic_vertical_align_center_black_24dp.png"/>\n</button>\n<button class="tr-ctrl" name="offset_down" id="scroll_down" type="submit"\n  onclick="this.form.offset.value = this.value"\n         value="${tl_offset + 1}" \n         title="Scroll tracklist down">\n  <img class="sm-icon" src="ic_arrow_drop_down_black_24dp.png"/>\n</button>\n</span>\n</form>\n</tr>\n  % for ind, pl_ind, track, que_pos, len in tracks:\n  <tr>\n    <td colspan="2"\n     ## distinguish current track\n     % if ind == track_ind and pl_ind == active_pl_ind:\n        class="current-track-name">\n          ${track}&nbsp;<span class="rightfloat">\n          ${len if len != \'00:00\' else \'\'}</span>\n     % else:\n        class="track-name">\n     ## color code position in the enque list\n     <%\n          pl_class = "plplay"\n          if que_pos >= 0:\n              pl_class = "pl_enq%d" % que_pos\n     %>\n        <button class="${pl_class}" name="jump_control" type="submit"\n          value="${ind}" form="playlist"\n          title="${pl_mode.capitalize()} this track">\n            ${track}&nbsp;<span class="rightfloat">\n            ${len if len != \'00:00\' else \'\'}</span>\n        </button>\n     % endif\n    </td>\n  </tr>\n  % endfor\n</table>\n</body>\n</html>\n')


def application(environ, start_response):
    """Web server page of controls for the audacious-media-player.org player."""
    path = environ['PATH_INFO']
    method = environ['REQUEST_METHOD']
    query = environ['QUERY_STRING']
    form_data = parse_qs(query)
    pl_mode = form_data.get('pl_jump_mode', [
     AudmanagerServer.default_pl_mode])[0]
    redir_url = path + '?' + query if len(query) else path
    try:
        aud_handle = aud_dbus.AudBus()
    except Exception as err:
        if type(err) == aud_dbus.DBusException:
            name = err.get_dbus_name()
            if name.startswith('org.freedesktop.DBus.Error.NoReply'):
                print 'Audman: Fatal Exception %s at %s ' % (
                 err, time.asctime())
                print traceback.format_exc()
                start_response('302 Found', [('Location', redir_url)])
                if not AudmanagerServer.kill_thread.isAlive():
                    AudmanagerServer.kill_thread.start()
                return ['']
        status = '504 Gateway Timeout'
        response_headers = [('Content-Type', 'text/html;charset=utf8')]
        start_response(status, response_headers)
        return [
         'Server Error: Could not find audacious process' + ' on the dbus:\n %s' % err]

    if method == 'POST':
        try:
            request_body_size = int(environ['CONTENT_LENGTH'])
            request_body = environ['wsgi.input'].read(request_body_size)
        except (TypeError, ValueError):
            print traceback.format_exc()
            request_body = '0'

        try:
            response_body = str(request_body)
        except:
            response_body = 'error'

        d = parse_qs(request_body)
        if not (d.has_key('control') or d.has_key('seek_control') or d.has_key('jump_control') or d.has_key('pl_control')):
            start_response('500 INTERNAL SERVER ERROR', [
             ('Content-Type', 'text/plain')])
            return [
             'Internal error: no control element in POST']
        action = None
        if d.has_key('seek_control'):
            action = 'seek_control'
            aud_handle.seek(int(d[action][0]) * 1000)
        else:
            if d.has_key('jump_control'):
                action = 'jump_control'
                ind = int(d[action][0])
                if pl_mode == 'play':
                    aud_handle.jump(ind)
                else:
                    aud_handle.playqueuetoggle(ind)
            elif d.has_key('pl_control'):
                action = 'pl_control'
                pl_ind = int(d[action][0])
                aud_handle.setactiveplaylist(pl_ind)
                aud_handle.playactiveplaylist()
            else:
                action = d['control'][0]
                if 'playpause' == action:
                    aud_handle.playpause()
                elif 'stop' == action:
                    aud_handle.stop()
                elif 'pl_next' == action:
                    aud_handle.advance()
                elif 'pl_prev' == action:
                    aud_handle.reverse()
                elif 'pl_shuffle' == action:
                    aud_handle.toggleshuffle()
                elif 'pl_repeat' == action:
                    aud_handle.togglerepeat()
                elif 'volume_down' == action:
                    aud_handle.lower_volume(AudmanagerServer.DEFAULT_VOL_DELTA)
                elif 'volume_up' == action:
                    aud_handle.raise_volume(AudmanagerServer.DEFAULT_VOL_DELTA)
            if action is None:
                start_response('500 INTERNAL SERVER ERROR', [
                 ('Content-Type', 'text/plain')])
                return [
                 'Internal error: no action element in POST']
        start_response('302 Found', [('Location', redir_url)])
        return []
    else:
        if path.endswith('.png') or path.endswith('.ico'):
            start_response('200 OK', [('Content-type', 'image/png'),
             ('cache-control', 'max-age=3600')])
            return file(resource_filename(__name__, path[1:]))
        tl_size = int(form_data.get('size', [
         AudmanagerServer.DEFAULT_TRACKLIST_LEN])[0])
        tl_offset = int(form_data.get('offset', [0])[0])
        active_pl_ind = -1
        active_pl_name = None
        playlists_lock = AudmanagerServer.playlists_locked
        if playlists_lock:
            active_pl_ind = -1
            active_pl_name = None
        else:
            try:
                active_pl_ind = aud_handle.getactiveplaylist()
                active_pl_name = aud_handle.getactiveplaylistname()
            except Exception as err:
                name = err.get_dbus_name()
                if name.startswith('org.freedesktop.DBus.Error.UnknownMethod'):
                    playlists_lock = True
                else:
                    raise

        track_ind = aud_handle.position()
        length = 0
        current_title = codec = ''
        if track_ind > 0:
            length = aud_handle.songlength(track_ind)
            current_title = aud_handle.songtitle(track_ind)
            codec = codec_shortname(aud_handle.songtuple(track_ind, 'codec'))
        pl_max_ind = aud_handle.pl_length()
        if tl_size < 1:
            tl_size = 1
        new_offset = track_ind + tl_offset * tl_size * 2
        if new_offset < 0:
            tl_offset += 1
        elif new_offset > pl_max_ind:
            tl_offset -= 1
        new_offset = track_ind + tl_offset * tl_size * 2
        play_list = aud_handle.pl_titles(new_offset, tl_size, tl_size, playlists_lock)
        seconds = aud_handle.time()
        volume = aud_handle.volume()
        state = aud_handle.player_status()
        rate, freq, nch = aud_handle.info()
        audio_info = '%s %s, %s' % (
         codec, chn_form_shortname(nch),
         '%02d kHz, %d kbps' % (freq / 1000, rate / 1000))
        is_repeat = aud_handle.is_repeat_mode()
        is_shuffle = aud_handle.is_shuffle_mode()
        if aud_handle.is_paused() or aud_handle.is_stopped():
            play_pause_icon = 'ic_play_arrow_black_48dp.png'
        else:
            play_pause_icon = 'ic_pause_black_48dp.png'
        play_lists = [] if playlists_lock else aud_handle.playlist_names()
        player_state = {'hostname': socket.gethostname(), 
           'current_title': current_title, 
           'active_pl_name': active_pl_name, 'track_ind': track_ind, 
           'active_pl_ind': active_pl_ind, 'track_length': length, 
           'track_pos': seconds, 
           'current_track_pos': '%02d:%02d/%02d:%02d' % (
                               seconds / 60, seconds % 60,
                               length / 60, length % 60), 
           'state': state, 
           'volume': int(volume), 'is_shuffle': is_shuffle, 
           'is_repeat': is_repeat, 'play_lists': play_lists, 
           'audio_info': audio_info, 
           'state_play_pause': play_pause_icon, 'tracks': play_list, 
           'playlists_lock': playlists_lock, 'tl_size': tl_size, 
           'tl_offset': tl_offset, 'pl_mode': pl_mode}
        response_body = AudmanagerServer.tr_list.render(**player_state)
        status = '200 OK'
        response_headers = [('Content-Type', 'text/html;charset=utf8'),
         (
          'Content-Length', str(len(response_body)))]
        start_response(status, response_headers)
        return [response_body]


def usage(args):
    print ('usage: %s [-p <port>] [--port=<port>] [-e] [--enque] ' + '[-l] [--playlists_locked]') % args[0]


def main(args):
    signal.signal(signal.SIGTERM, AudmanagerServer.clean_exit)
    signal.signal(signal.SIGHUP, AudmanagerServer.clean_exit)
    try:
        runaudws(sys.argv)
    except KeyboardInterrupt:
        AudmanagerServer.clean_exit()


def runaudws(args):
    hostname = ''
    port = 8051
    pl_mode = 'play'
    playlists_locked = False
    try:
        opts, args = getopt.getopt(args[1:], 'ep:l', ['enque', 'port=',
         'playlists_locked'])
    except getopt.GetoptError as err:
        print str(err)
        usage(args)
        sys.exit(2)

    for o, a in opts:
        if o in '-p--port':
            port = int(a)
        elif o in ('-e', '--enque'):
            pl_mode = 'enque'
        elif o in ('-l', '--playlists_locked'):
            playlists_locked = True

    maybe_ip = guess_listening_addr()
    server = AudmanagerServer((maybe_ip, port), application, handler_class=LogErrorHandler)
    AudmanagerServer.default_pl_mode = pl_mode
    AudmanagerServer.playlists_locked = playlists_locked
    print 'Audman: Audacious Audio Player Control listening on http://%s:%d' % (
     maybe_ip, port)
    t = threading.Thread(target=server.serve_forever)
    t.start()
    while True:
        t.join(0.3)
        if not t.isAlive():
            break

    AudmanagerServer.kill_thread.join()
    del server
    print 'restarting'
    os.execl(sys.executable, sys.executable, *sys.argv)


if __name__ == '__main__':
    main(sys.argv)