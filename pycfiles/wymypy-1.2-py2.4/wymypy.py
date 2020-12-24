# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/wymypy/wymypy.py
# Compiled at: 2007-02-03 10:41:07
import os, time, sys, cgi, socket
from urllib import urlencode
from libs.mpdsafe import MpdSafe
from libs.config import Config
from libs import wsgiserver
from libs.utilities import get_post_form, explodePath
import base64
u64enc = base64.urlsafe_b64encode
u64dec = base64.urlsafe_b64decode
MPD = None
CFG = None
__version__ = '1.2'
try:
    os.chdir(os.path.dirname(__file__))
except:
    pass

from plugins import wPlugin

def register_ajax(path, method):
    return '\n    function ajax_%(method)s()\n    { sajax_do_call("%(path)s%(method)s",ajax_%(method)s.arguments);}\n    ' % locals()


class WyMyPy:
    __module__ = __name__

    def __init__(self, path='/'):
        self.__path = path

    def __call__(self, environ, start_response):
        path = environ['PATH_INFO']
        (f, mpath) = explodePath(path)
        if self.__path != '/':
            ppath = self.__path.strip('/')
            if ppath == f:
                (f, mpath) = explodePath(mpath)
            else:
                start_response('404 not found', [('content-type', 'text/html')])
                return ['404 not found']
        if f == '':
            if mpath == '/dewplayer.swf':
                start_response('200 OK', [('content-type', 'application/x-shockwave-flash')])
                return open('libs/dewplayer.swf', 'rb')
            else:
                start_response('200 OK', [('content-type', 'text/html')])
                return mainpage(self.__path)
        elif f == '__ajax':
            start_response('200 OK', [('content-type', 'text/html')])
            args = [ i.value for i in get_post_form(environ).list ]
            return makeajax(mpath, args)
        elif f == 'listen':
            name = u64dec(mpath[1:])
            start_response('200 OK', [('content-type', 'Content-Type: application/octet-stream'), ('Content-Disposition', 'attachment; filename="%s";' % name)])
            file = os.path.join('/media/data/mp3', name)
            return open(file, 'rb')
        else:
            start_response('200 OK', [('content-type', 'application/x-shockwave-flash')])
            i = wPlugin.getInstance(f)
            if i:
                start_response('200 OK', [('content-type', 'text/html')])
                return i.get(mpath)
            else:
                start_response('404 not found', [('content-type', 'text/html')])
                return ('404 not found', )


def mainpage(path):
    yield '<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN">\n                <html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en-US" />\n                <html>\n                  <head>\n                    <meta http-equiv="content-type" content="text/html; charset=utf-8" />\n                    <meta http-equiv="content-language" content="en-US" />\n                    <meta name="language" content="en-US" />\n                    <meta name="description" content="Official website of the web-band manella">\n                    <title>wymypy</title>\n          '
    yield "<style type='text/css'>"
    yield '\n          body {background:#222;}\n          * {font-size:13px;font-family: arial, helvetica, sans-serif;color:white }\n          input,select {background:#111;border:1px solid #666}\n          a {text-decoration:none;color:#AAF}\n          li {display:block;list-style-type: none;background:black;padding-top:1px;color:white}\n          li.p{background:#111}\n          li.s{background:#AA3;color:black}\n          li.s a {color:black}\n          li:hover {background:#555;color:black}\n          li:hover a {background:#555;color:#BBF}\n          button{background:#666;color:white;cursor:pointer;border:1px solid #666}\n          button:hover {background:#333}\n          span {background:#800;color:white;padding-left:2px;padding-right:2px;margin-left:1px;margin-right:2px}\n          form {display:inline;}\n          div#zonePlayer {\n            padding:2px;\n            position:absolute;\n            left:50%;\n            top:24px;\n            right:0px;\n            overflow:auto;\n            height:70px;\n            }\n          div#zoneListen {border:2px solid blue;visibility:hidden}\n\n          div#zonePlayList{\n            overflow:auto;\n            border:2px solid #222;\n            position:absolute;\n            top:100px;\n            bottom:25px;\n            left:50%;\n            right:0px;\n            background:#000;\n            padding:2px\n          }\n          div#zoneView{\n            overflow:auto;\n            border:1px solid black;\n            position:absolute;\n            top:24px;\n            bottom:0px;\n            left:0px;\n            right:50%;\n            background:#000;\n            }\n\n          div#zoneOpt{\n            position:absolute;\n            bottom:0px;\n            left:50%;\n            right:0px;\n            padding:2px;\n\n          }\n\n          div#zonePlugins{\n            position:absolute;\n            left:0;\n            right:0px;\n            top:0px;\n          }\n\n          /* seekbar */\n          a#sb{width:200px;height:16px;background:#888;display:block;text-align:left;border:1px solid red;cursor:pointer}\n          div#sbc{height:100%;background:#008}\n\n          '
    for i in wPlugin.instances:
        yield i.css

    yield '</style>'
    yield "<script type='text/javascript'>"
    am = AjaxMethods()
    for i in dir(am):
        if str(i).lower().startswith('ajax_'):
            yield register_ajax(path + '__ajax/', i[5:])

    for plugin in wPlugin.instances:
        for i in dir(plugin):
            if str(i).lower().startswith('ajax_'):
                yield register_ajax(path + '__ajax/' + plugin.path + '/', i[5:])

    yield '\n        function $(id) {\n            return document.getElementById(id);\n        }\n\n        // remote scripting library\n        // (c) copyright 2005 modernmethod, inc\n        //http://www.modernmethod.com/sajax/\n\n       function set_cursor(t) {\n             //var cursor =\n             //document.layers ? document.cursor :\n             //document.all ? document.all.cursor :\n             //document.getElementById ? document.getElementById(\'cursor\') : null;\n             document.body.style.cursor = t;\n         }\n\n        var sajax_debug_mode = false;\n\n        function sajax_debug(text) {\n            if (sajax_debug_mode)\n                alert("RSD: " + text)\n        }\n\n        function sajax_init_object() {\n            sajax_debug("sajax_init_object() called..")\n\n            var A;\n            try {\n                A=new ActiveXObject("Msxml2.XMLHTTP");\n            } catch (e) {\n                try {\n                    A=new ActiveXObject("Microsoft.XMLHTTP");\n                } catch (oc) {\n                    A=null;\n                }\n            }\n            if(!A && typeof XMLHttpRequest != "undefined")\n                A = new XMLHttpRequest();\n            if (!A)\n                sajax_debug("Could not create connection object.");\n            return A;\n        }\n        function sajax_do_call( url, args) {\n            set_cursor(\'wait\');\n            var i, x, n, data="";\n            url = url + "?rsrnd=" + new Date().getTime();\n            for (i = 0; i < args.length; i++) {\n                if(data!="") data+="&";\n                data = data + "p"+i+"=" + encodeURIComponent(args[i]);\n            }\n            x = sajax_init_object();\n            x.open("POST", url, true);\n            x.setRequestHeader("Method", "POST " + url + " HTTP/1.1");\n            x.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");\n            x.onreadystatechange = function() {\n                if (x.readyState != 4)\n                    return;\n                sajax_debug("received " + x.responseText);\n\n                set_cursor(\'default\');\n                var status;\n                var data;\n                status = x.responseText.charAt(0);\n                data = x.responseText.substring(2);\n                if (status == "-")\n                    alert("Error: " + data);\n                else {\n                    //if (data) {\n                      var obj=eval("("+data+")"); // data i a json dict\n                      for(var id in obj)\n                          document.getElementById(id).innerHTML = obj[id];\n                    //}\n                }\n            }\n            x.send(data);\n            sajax_debug(" url = " + url);\n            sajax_debug(" waiting..");\n            delete x;\n        }\n\n\n        function refresh(isForced)\n        {\n            ajax_player(isForced);\n\n            var v=$("timer").value;\n            if(v!="")\n                _timer=window.setTimeout(\'refresh()\',parseInt(v));\n        }\n\n\n        function seekclick(e)\n        {\n            var x;\n            if(e.offsetX)\n                x=e.offsetX\n            else\n            {\n                var Element = e.target ;\n                var CalculatedTotalOffsetLeft = CalculatedTotalOffsetTop = 0 ;\n                while (Element.offsetParent)\n                {\n                    CalculatedTotalOffsetLeft += Element.offsetLeft ;\n                    CalculatedTotalOffsetTop += Element.offsetTop ;\n                    Element = Element.offsetParent ;\n                }\n\n                OffsetXForNS6 = e.pageX - CalculatedTotalOffsetLeft ;\n                OffsetYForNS6 = e.pageY - CalculatedTotalOffsetTop ;\n                x=OffsetXForNS6;\n            }\n\n            ajax_ope("seek",Math.round(x/2));\n        }\n\n        function do_operation(cmd,idx)\n        {\n          ajax_ope(cmd,idx);\n        }\n\n        function changeDisplay(elt)\n        {\n          ajax_ope("changeDisplay",(elt.checked?"1":"0"));\n        }\n\n\n        function init()\n        {\n          // ajax_liste("");\n          refresh(1);\n        }\n        '
    for i in wPlugin.instances:
        yield i.js

    yield '</script>'
    yield '\n              </head>\n              <body onload="init();">\n          '
    yield '<div id="zonePlugins">'
    for i in wPlugin.instances:
        yield i.show()

    yield '</div>'
    yield '<div id="zoneOpt">'
    yield "<b style='float:right'><a href='http://manatlan.infogami.com/wymypy'>wymypy</a> %s</b>" % __version__
    yield '\n    <select id=\'timer\' onchange="refresh();">\n        <option value=\'1000\'>refresh 1s</option>\n        <option value=\'2000\'>refresh 2s</option>\n        <option value=\'5000\' selected>refresh 5s</option>\n        <option value=\'10000\'>refresh 10s</option>\n        <option value=\'\'>refresh none</option>\n    </select>\n\n    <input type="checkbox" id=\'dispTags\' onchange=\'changeDisplay(this);\' />\n    '
    yield '</div>'
    yield '<div id="zoneListen"></div>'
    yield '<div id="zonePlayer"></div>'
    yield '<div id="zoneView">\n    <h1>Welcome</h1>\n    Welcome to wymypy ! From here you can pilot your Music Player Daemon!\n    <br><br>\n    <p>At the top, you have the "plugin bar" with provide the main operations in your library. Plugins will always be displayed in this zone.</p>\n    <p>At the right, you can control your player, and your playlist.</p>\n    <p>At the bottom right, you find the wymypy options now.</p>\n    <p>Other configurations take place in your <b>~/.wymypy</b> config file (in the future they will be editable thru a plugin)</p>\n    </div>'
    yield '<div id="zonePlayList"></div>'
    yield '  </body>\n            </html>\n            ' % locals()


def flux2dict(iter):
    l = {}
    key = None
    for i in iter:
        if i[:2] == '[[' and i[-2:] == ']]':
            key = i[2:-2]
            l[key] = ''
        elif key == None:
            raise 'key error'
        else:
            l[key] += i

    return l


def jsonize(dict):
    return '{' + (',').join([ ' "%s" : "%s" ' % (i, dict[i].replace('"', '\\"').replace('\n', '\\n')) for i in dict ]) + '}'


def makeajax(method, args):
    pmethod = method
    largs = []
    for i in args:
        if i == 'undefined':
            largs.append(None)
        else:
            largs.append(i)

    args = largs
    if method.count('/') == 2:
        t = method.split('/')
        inst = wPlugin.getInstance(t[1])
        method = t[2]
        isPlugin = True
    else:
        inst = AjaxMethods()
        method = method[1:]
        isPlugin = False
    method = 'ajax_' + method
    if hasattr(inst, method):
        fct = getattr(inst, method)
        iter = fct(*args, **{})
        if isPlugin:
            if "'generator'" in str(type(iter)):

                def _iterInZoneView(iter):
                    yield '[[zoneView]]'
                    for i in iter:
                        yield i

                iter = _iterInZoneView(iter)
            elif iter == 'player':
                inst = AjaxMethods()
                iter = inst.ajax_player()
            else:
                yield '+ {"":""}'
                return
        dic = flux2dict(iter)
        yield '+ '
        yield jsonize(dic)
    else:
        yield (
         '- methode non existante : ', pmethod)
    return


def getUrlsForMpdSong(s):
    if s.path.lower().startswith('http://'):
        if '-' in s.title:
            l = s.title.split('-')
            artist = l[0].strip()
            title = l[1].strip()
            album = ''
        else:
            return {}
    else:
        artist = s.artist.strip()
        title = s.title.strip()
        album = s.album.strip()
    url = {}
    if artist:
        url['amg'] = '<a href="http://www.allmusic.com/cg/amg.dll?opt1=1&P=amg&sql=%s">amg</a> ' % (artist,)
        url['lastfm'] = '<a href="http://www.last.fm/music/%s">lfm</a> ' % artist.replace(' ', '+')
        if title:
            url['lyrc'] = '<a href="http://lyrc.com.ar/en/tema1en.php?%s">lyrics</a> ' % urlencode({'artist': artist, 'songname': title})
    return url


class AjaxMethods:
    __module__ = __name__

    def ajax_player(self, isForced=0):
        global CFG
        global MPD
        yield '[[zonePlayer]]'
        stat = MPD.status()
        if not stat:
            MPD.stop()
            yield "Error : Can't play that!"

            class stat:
                __module__ = __name__
                state = 0

        elif stat.state in (2, 3):
            s = MPD.getCurrentSong()
            if s.path.lower().startswith('http://'):
                yield '[Stream] '
                yield s.title and s.title or 'playing ...'
            else:
                yield MPD.display(s, CFG.server.tagformat)
            yield '<br />'
            d = getUrlsForMpdSong(s)
            urls = (' ').join([ d[i] for i in sorted(d.keys()) ])
            ds = lambda t: '%02d:%02d' % (t / 60, t % 60)
            (s, t, p) = MPD.getSongPosition()
            yield "\n                  <table>\n                    <tr>\n                      <td>\n                        <a id='sb' onclick='seekclick(event);'>\n                            <div id='sbc' style='width:%dpx'></div>\n                        </a>\n                      </td>\n                      <td>\n                        %d %% - %s/%s - %s\n                      </td>\n                    </tr>\n                  </table>" % (int(p * 2), int(p), ds(s), ds(t), urls)
        yield '\n        <button onclick=\'do_operation("prev");\'><<</button>\n        '
        if stat.state != 2:
            yield ' <button onclick=\'do_operation("play");\'>></button>'
        else:
            yield ' <button onclick=\'do_operation("pause");\'>||</button>'
        if stat.state != 1:
            yield ' <button onclick=\'do_operation("stop");\'>[]</button>'
        yield '\n        <button onclick=\'do_operation("next");\'>>></button>\n        '
        if stat.state != 0:
            yield '\n            <button onclick=\'do_operation("voldown");\'>-</button>\n            <button onclick=\'do_operation("volup");\'>+</button>\n            '
            yield str(stat.volume)
            yield '%'
        if isForced or MPD.needRedrawPlaylist():
            (idx, tot) = MPD.getPlaylistPosition()
            yield '[[zonePlayList]]'
            yield '\n            <h2>Playlist (%d)\n            <button onclick=\'do_operation("clear");\'>clear</button>\n            <button onclick=\'do_operation("shuffle");\'>shuffle</button>\n            </h2>\n            ' % tot
            l = MPD.playlist()
            for s in l:
                i = l.index(s)
                if i + 1 == idx:
                    classe = " class='s'"
                else:
                    classe = i % 2 == 0 and " class='p'" or ''
                if s.path.lower().startswith('http://'):
                    title = s.path
                else:
                    title = MPD.display(s, CFG.server.tagformat)
                yield '<li%s>' % classe
                yield '%03d' % (i + 1)
                yield '<a href=\'#\' onclick="do_operation(\'delete\',\'' + str(i) + '\');"><span>X</span></a>'
                yield '<a href=\'#\' onclick="do_operation(\'play\',\'' + str(i) + '\');">' + title + '</a>'
                yield '</li>'

    def ajax_ope(self, op, idx=None):
        if op == 'play':
            if idx:
                MPD.play(int(idx))
            else:
                MPD.play()
        elif op == 'delete':
            MPD.delete([int(idx)])
        elif op == 'next':
            MPD.next()
        elif op == 'prev':
            MPD.prev()
        elif op == 'play':
            MPD.play()
        elif op == 'pause':
            MPD.pause()
        elif op == 'stop':
            MPD.stop()
        elif op == 'clear':
            MPD.clear()
        elif op == 'shuffle':
            MPD.shuffleIt()
        elif op == 'seek':
            MPD.seek(percent=int(idx))
        elif op == 'volup':
            MPD.volumeUp()
        elif op == 'voldown':
            MPD.volumeDown()
        elif op == 'changeDisplay':
            MPD.changeDisplay(int(idx))
        else:
            raise 'ERROR:' + op + ',' + str(idx)
        return self.ajax_player()

    def ajax_listen(self, file_enc):
        file = u64dec(file_enc)
        yield '[[zoneListen]]'
        url = 'listen/%s' % file_enc
        yield '<a href="%s">%s</a> ' % (url, file)
        yield '\n        <object type="application/x-shockwave-flash"\n        data="dewplayer.swf?son=%(url)s&amp;autoplay=1&amp;bgcolor=FFFFFF"\n        height="20"\n        width="160">\n        <param name="movie" value="dewplayer.swf?son=%(url)s&amp;autoplay=1&amp;bgcolor=FFFFFF">\n        </object>\n        ' % locals()


def main(path):
    global CFG
    global MPD
    CFG = Config()
    MPD = MpdSafe(CFG.mpd.host, int(CFG.mpd.port))
    err = MPD.connect()
    if err:
        print "wymypy can't connect to your MPD : ", err
        sys.exit(-1)
    else:
        wPlugin.initInstances(MPD, 'plugins')
        app = WyMyPy(path)
        run = lambda : wsgiserver.WSGIServer(('', int(CFG.server.port)), {'': app}).serve_forever()
        print 'wymypy is listening on http://localhost:%s%s' % (CFG.server.port, path)
        print '(hit CTRL+C to quit)'
        try:
            run()
        except KeyboardInterrupt:
            pass
        except socket.error:
            print 'The port %s is already in use, perhaps wymypy is already running ?!' % CFG.server.port
            sys.exit(-1)

        sys.exit(0)


USAGE = 'USAGE : %s [option]\nWebserver frontend for MusicPlayerDaemon. Version ' + __version__ + '\nCopyright 2007 by Marc Lentz under the GPL2 licence.\nOptions:\n    -h        : this help\n    -p <path> : protect the web access with a path'

def run():
    if len(sys.argv) > 1:
        if sys.argv[1] == '-h':
            print USAGE % os.path.basename(sys.argv[0])
            sys.exit(0)
        elif sys.argv[1] == '-p':
            if len(sys.argv) != 3:
                print USAGE % os.path.basename(sys.argv[0])
                sys.exit(-1)
            else:
                main('/' + sys.argv[2] + '/')
        else:
            print USAGE % os.path.basename(sys.argv[0])
            sys.exit(-1)
    else:
        main('/')


if __name__ == '__main__':
    run()