# uncompyle6 version 3.7.4
# Python bytecode 3.3 (3230)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/lib64/python3.3/site-packages/batman/pafy.py
# Compiled at: 2014-02-04 12:42:52
# Size of source mod 2**32: 19330 bytes
"""
Python API for YouTube.

https://github.com/np1/pafy

Copyright (C)  2013-2014 nagev

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""
__version__ = '0.3.31'
__author__ = 'nagev'
__license__ = 'GPLv3'
import re, os, sys, time, json, logging
from xml.etree import ElementTree as etree
decode_if_py3 = lambda x: x.decode('utf8')
if sys.version_info[:2] >= (3, 0):
    from urllib.request import build_opener
    from urllib.error import HTTPError, URLError
    from urllib.parse import parse_qs, unquote_plus
else:
    decode_if_py3 = lambda x: x
    from urllib2 import build_opener, HTTPError, URLError
    from urllib import unquote_plus
    from urlparse import parse_qs
if os.path.exists(os.path.join(os.path.expanduser('~'), '.pafydebug')):
    logging.basicConfig(level=logging.DEBUG)

def _extract_function_from_js(name, js):
    """ Find a function definition called `name` and extract components.

    Return a dict representation of the function.

    """
    name = name.replace('$', '\\$')
    m = re.search('function %s\\(((?:\\w+,?)+)\\)\\{([^}]+)\\}' % name, js)
    logging.debug(m.group(0))
    return {'name': name,  'parameters': m.group(1).split(','),  'body': m.group(2)}


def _getval(val, argsdict):
    """ resolve variable values, preserve int literals. Return dict."""
    m = re.match('(\\d+)', val)
    if m:
        return int(m.group(1))
    if val in argsdict:
        return argsdict[val]
    raise RuntimeError('Error val %s from dict %s' % (val, argsdict))


def _get_func_from_call(caller_function, name, arguments, js):
    """
    Search js string for function call to `name`.

    Returns dict representation of the funtion
    Places argument values specified in `arguments` list parameter into
    the returned function representations `args` dict

    """
    newfunction = _extract_function_from_js(name, js)
    newfunction['args'] = {}
    for n, arg in enumerate(arguments):
        value = _getval(arg, caller_function['args'])
        param = newfunction['parameters'][n]
        newfunction['args'][param] = value

    return newfunction


def _solve(f, js):
    """Solve basic javascript function. Return dict function representation."""
    patterns = {'split_or_join': '(\\w+)=\\1\\.(?:split|join)\\(""\\)$', 
     'func_call': '(\\w+)=([$\\w]+)\\(((?:\\w+,?)+)\\)$', 
     'x1': 'var\\s(\\w+)=(\\w+)\\[(\\w+)\\]$', 
     'x2': '(\\w+)\\[(\\w+)\\]=(\\w+)\\[(\\w+)\\%(\\w+)\\.length\\]$', 
     'x3': '(\\w+)\\[(\\w+)\\]=(\\w+)$', 
     'return': 'return (\\w+)(\\.join\\(""\\))?$', 
     'reverse': '(\\w+)=(\\w+)\\.reverse\\(\\)$', 
     'slice': '(\\w+)=(\\w+)\\.slice\\((\\w+)\\)$'}
    parts = f['body'].split(';')
    for part in parts:
        logging.debug('Working on part: ' + part)
        name = ''
        for n, p in patterns.items():
            m, name = re.match(p, part), n
            if m:
                break

        if name == 'split_or_join':
            pass
        elif name == 'func_call':
            lhs, funcname, args = m.group(1, 2, 3)
            newfunc = _get_func_from_call(f, funcname, args.split(','), js)
            f['args'][lhs] = _solve(newfunc, js)
        elif name == 'x1':
            b, c = [_getval(x, f['args']) for x in m.group(2, 3)]
            f['args'][m.group(1)] = b[c]
        elif name == 'x2':
            vals = m.group(*range(1, 6))
            a, b, c, d, e = [_getval(x, f['args']) for x in vals]
            f['args'][m.group(1)] = a[:b] + c[(d % len(e))] + a[b + 1:]
        elif name == 'x3':
            a, b, c = [_getval(x, f['args']) for x in m.group(1, 2, 3)]
            f['args'][m.group(1)] = a[:b] + c + a[b + 1:]
        else:
            if name == 'return':
                return f['args'][m.group(1)]
            if name == 'reverse':
                f['args'][m.group(1)] = _getval(m.group(2), f['args'])[::-1]
            elif name == 'slice':
                a, b, c = [_getval(x, f['args']) for x in m.group(1, 2, 3)]
                f['args'][m.group(1)] = b[c:]
            else:
                raise RuntimeError('no match for %s' % part)

    raise RuntimeError('Processed js funtion parts without finding return')


def _decodesig(sig, js):
    """Get sig func name from a function call. Return function dict, js."""
    m = re.search('\\w\\.sig\\|\\|(\\w+)\\(\\w+\\.\\w+\\)', js)
    funcname = m.group(1)
    function = _extract_function_from_js(funcname, js)
    if not len(function['parameters']) == 1:
        raise RuntimeError('Main sig js function has more than one arg: %s' % function['parameters'])
    function['args'] = {function['parameters'][0]: sig}
    new.callback('Decrypting signature')
    solved = _solve(function, js)
    new.callback('Decrypted signature')
    return solved


def new(url, callback=None):
    """ Return a new pafy instance given a url or video id. """
    return Pafy(url, callback=callback)


class Stream(object):
    __doc__ = ' YouTube video stream class. '
    itags = {'5': ('320x240', 'flv', 'normal'), 
     '17': ('176x144', '3gp', 'normal'), 
     '18': ('640x360', 'mp4', 'normal'), 
     '22': ('1280x720', 'mp4', 'normal'), 
     '34': ('640x360', 'flv', 'normal'), 
     '35': ('854x480', 'flv', 'normal'), 
     '36': ('320x240', '3gp', 'normal'), 
     '37': ('1920x1080', 'mp4', 'normal'), 
     '38': ('4096x3072', 'superHD', 'normal'), 
     '43': ('640x360', 'webm', 'normal'), 
     '44': ('854x480', 'webm', 'normal'), 
     '45': ('1280x720', 'webm', 'normal'), 
     '46': ('1920x1080', 'webm', 'normal'), 
     '82': ('640x360-3D', 'mp4', 'normal'), 
     '84': ('1280x720-3D', 'mp4', 'normal'), 
     '100': ('640x360-3D', 'webm', 'normal'), 
     '102': ('1280x720-3D', 'webm', 'normal'), 
     '133': ('426x240', 'm4v', 'video'), 
     '134': ('640x360', 'm4v', 'video'), 
     '135': ('854x480', 'm4v', 'video'), 
     '136': ('1280x720', 'm4v', 'video'), 
     '137': ('1920x1080', 'm4v', 'video'), 
     '138': ('4096x3072', 'm4v', 'video'), 
     '139': ('48k', 'm4a', 'audio'), 
     '140': ('128k', 'm4a', 'audio'), 
     '141': ('256k', 'm4a', 'audio'), 
     '160': ('256x144', 'm4v', 'video'), 
     '171': ('128k', 'ogg', 'audio'), 
     '172': ('192k', 'ogg', 'audio'), 
     '242': ('360x240', 'webm', 'normal'), 
     '243': ('480x360', 'webm', 'normal'), 
     '244': ('640x480', 'webm', 'normal'), 
     '245': ('640x480', 'webm', 'normal'), 
     '246': ('640x480', 'webm', 'normal'), 
     '247': ('720x480', 'webm', 'normal'), 
     '248': ('unknown', 'unknown', 'unknown'), 
     '264': ('1920x1080', 'm4v', 'video')}

    def __init__(self, sm, opener, title='ytvid', js=None):
        self.url = sm['url'][0]
        if sm.get('s'):
            sm['sig'] = [
             _decodesig(sm['s'][0], js)]
            logging.debug('Calculated decrypted sig: ' + sm['sig'][0])
        if 'signature=' not in self.url:
            self.url += '&signature=' + sm['sig'][0]
        if 'ratebypass=' not in self.url:
            self.url = self.url + '&ratebypass=yes'
        self.itag = sm['itag'][0]
        self.threed = 'stereo3d' in sm and sm['stereo3d'][0] == '1'
        self.resolution = self.itags[self.itag][0]
        self.dimensions = tuple(self.resolution.split('-')[0].split('x'))
        safeint = lambda x: int(x) if x.isdigit() else x
        self.dimensions = tuple(map(safeint, self.dimensions))
        self.vidformat = sm['type'][0].split(';')[0]
        self.quality = self.resolution
        self.extension = self.itags[self.itag][1]
        self.title = title
        self.filename = self.title + '.' + self.extension
        self.fsize = None
        self._opener = opener
        self.bitrate = self.rawbitrate = None
        self.mediatype = self.itags[self.itag][2]
        if self.mediatype == 'audio':
            self.bitrate = self.resolution
            self.rawbitrate = int(sm['bitrate'][0])
            self.dimensions = (0, 0)
            self.resolution = '0x0'
            self.quality = self.bitrate
        return

    def __repr__(self):
        out = '%s:%s@%s' % (self.mediatype, self.extension, self.quality)
        return out

    def get_filesize(self):
        """ Return filesize of the stream in bytes.  Set member variable. """
        if not self.fsize:
            try:
                opener = self._opener
                cl = 'content-length'
                self.fsize = int(opener.open(self.url).headers[cl])
            except (HTTPError, URLError):
                self.fsize = 0

        return self.fsize

    def download(self, filepath='', quiet=False, callback=None):
        """ Download.  Use quiet=True to supress output. Return filename. """
        status_string = '  {:,} Bytes [{:.2%}] received. Rate: [{:4.0f} kbps].  ETA: [{:.0f} secs]'
        response = self._opener.open(self.url)
        total = int(response.info()['Content-Length'].strip())
        chunksize, bytesdone, t0 = 16384, 0, time.time()
        fname = filepath or self.filename
        try:
            outfh = open(fname, 'wb')
        except IOError:
            ok = re.compile('[^\\\\/?*$\\\'"%&:<>|]')
            fname = ''.join((x if ok.match(x) else '_') for x in self.filename)
            outfh = open(fname, 'wb')

        while 1:
            chunk = response.read(chunksize)
            outfh.write(chunk)
            elapsed = time.time() - t0
            bytesdone += len(chunk)
            rate = bytesdone / 1024 / elapsed
            eta = (total - bytesdone) / (rate * 1024)
            progress_stats = (bytesdone, bytesdone * 1.0 / total, rate, eta)
            if not chunk:
                outfh.close()
                break
            if not quiet:
                status = status_string.format(*progress_stats)
                sys.stdout.write('\r' + status + '    ' + '\r')
                sys.stdout.flush()
            if callback:
                callback(total, *progress_stats)
                continue

        return fname


class Pafy(object):
    __doc__ = ' Class to represent a YouTube video. '

    def __len__(self):
        return self.length

    def __repr__(self):
        keys = 'Title Author ID Duration Rating Views Thumbnail Keywords'
        keys = keys.split(' ')
        self.keywords = self.keywords or ''
        keywords = ', '.join(self.keywords)
        length = time.strftime('%H:%M:%S', time.gmtime(self.length))
        info = dict(Title=self.title, Author=self.author, Views=self.viewcount, Rating=self.rating, Duration=length, ID=self.videoid, Thumbnail=self.thumb, Keywords=keywords)
        return '\n'.join(['%s: %s' % (k, info.get(k, '')) for k in keys])

    def get_js(self, opener):
        """ Get location of html5player javascript file and fetch.

        Return javascript as string and args.

        """
        logging.debug('call to get js')
        if not self.js or not self.xargs:
            watchurl = 'https://www.youtube.com/watch?v=' + self.videoid
            watchinfo = opener.open(watchurl).read().decode('UTF-8')
            m = re.search(';ytplayer.config = ({.*?});', watchinfo)
            try:
                myjson = json.loads(m.group(1))
            except:
                raise RuntimeError('Problem handling this video')

            args = myjson['args']
            html5player = myjson['assets']['js']
            if html5player.startswith('//'):
                html5player = 'https:' + html5player
            logging.debug('opening js url')
            js = opener.open(html5player).read().decode('UTF-8')
            self.js, self.xargs = js, args
        return (self.js, self.xargs)

    def getstreammap(self, allinfo, key, opener):
        """ get stream map. Return stream map and javascript."""
        js = self.js
        streamMap = allinfo[key][0].split(',')
        smap = [parse_qs(sm) for sm in streamMap]
        if smap[0].get('s'):
            logging.debug('encrypted sig')
            new.callback('Getting javascript data..')
            js, args = self.get_js(opener)
            new.callback('Got javascript')
            streamMap = args[key].split(',')
            smap = [parse_qs(sm) for sm in streamMap]
        return (
         smap, js)

    def get_video_gdata(self):
        """ Fetch video data using GData API if not previously fetched.

        Return xml string

        """
        if not self.gdata:
            url = 'https://gdata.youtube.com/feeds/api/videos/%s?v=2'
            url = url % self.videoid
            self.gdata = self._opener.open(url).read()
        return self.gdata

    @property
    def description(self):
        """ Extract description, fetch gdata if necessary. Return string."""
        if not self._description:
            t0 = '{http://search.yahoo.com/mrss/}'
            gdata = self.get_video_gdata()
            tree = etree.fromstring(gdata)
            d = tree.findall('%s%s/%s%s' % (t0, 'group', t0, 'description'))
            self._description = d[0].text
        return self._description

    @property
    def category(self):
        """Extract category label from gdata. Return string."""
        if not self._category:
            t0 = '{http://search.yahoo.com/mrss/}'
            gdata = self.get_video_gdata()
            tree = etree.fromstring(gdata)
            d = tree.findall('%s%s/%s%s' % (t0, 'group', t0, 'category'))
            self._category = d[0].text
        return self._category

    def __init__(self, video_url, callback=None):
        infoUrl = 'https://www.youtube.com/get_video_info?video_id='
        ok = ('a-zA-Z0-9_-', 'a-zA-Z0-9_-', 'a-zA-Z0-9_-')
        regx = re.compile('(?:^|[^%s]+)([%s]{11})(?:[^%s]+|$)' % ok)
        m = regx.search(video_url)
        if not m:
            err = 'Need 11 character video id or the URL of the video. Got %s'
            raise RuntimeError(err % video_url)
        vidid = m.group(1)
        infoUrl += vidid + '&asv=3&el=detailpage&hl=en_US'
        opener = build_opener()
        ua = 'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64;Trident/5.0)'
        opener.addheaders = [
         (
          'User-Agent', ua)]
        self.keywords = ''
        allinfo = parse_qs(decode_if_py3(opener.open(infoUrl).read()))
        if allinfo['status'][0] == 'fail':
            reason = allinfo['reason'][0] or 'Bad video argument'
            raise RuntimeError('Youtube says: %s' % reason)
        if callback:
            new.callback = callback
        else:
            new.callback = lambda x: None
        f = lambda x: allinfo.get(x, ['unknown'])[0]
        self.gdata = None
        self.xargs = None
        self.js = None
        self.title = f('title').replace('/', '-')
        self.author = f('author')
        self.videoid = f('video_id')
        self.rating = float(f('avg_rating'))
        self.length = int(f('length_seconds'))
        self.viewcount = int(f('view_count'))
        self.thumb = unquote_plus(f('thumbnail_url'))
        self.duration = time.strftime('%H:%M:%S', time.gmtime(self.length))
        self.formats = f('fmt_list').split(',')
        self.formats = [x.split('/') for x in self.formats]
        self._description = None
        self._category = None
        self.keywords = self.bigthumb = self.bigthumbhd = None
        if 'keywords' in allinfo:
            self.keywords = f('keywords').split(',')
        if allinfo.get('iurlsd'):
            self.bigthumb = f('iurlsd')
        if allinfo.get('iurlmaxres'):
            self.bigthumbhd = f('iurlmaxres')
        self._opener = opener
        try:
            smap, js = self.getstreammap(allinfo, 'url_encoded_fmt_stream_map', opener)
        except KeyError:
            raise IOError("Can't get video stream info")

        self.streams = [Stream(sm, opener, self.title, js) for sm in smap]
        self.videostreams = self.audiostreams = []
        if 'adaptive_fmts' in allinfo:
            smap_adpt, js = self.getstreammap(allinfo, 'adaptive_fmts', opener)
            self.streams_ad = [Stream(sm, opener, self.title, js) for sm in smap_adpt]
            self.audiostreams = [x for x in self.streams_ad if x.bitrate]
            self.videostreams = [x for x in self.streams_ad if not x.bitrate]
            m4astreams = [x for x in self.audiostreams if x.extension == 'm4a']
            oggstreams = [x for x in self.audiostreams if x.extension == 'ogg']
            self.m4astreams, self.oggstreams = m4astreams, oggstreams
        self.allstreams = self.streams + self.videostreams + self.audiostreams
        return

    def getbest(self, preftype='any', ftypestrict=True):
        """
        Return the best resolution available.

        set ftypestrict to False to use a non preferred format if that
        has a higher resolution

        """

        def _sortkey(x, key3d=0, keyres=0, keyftype=0):
            """ sort function for max() """
            key3d = '3D' not in x.resolution
            keyres = int(x.resolution.split('x')[0])
            keyftype = preftype == x.extension
            if ftypestrict:
                return (key3d, keyftype, keyres)
            else:
                return (
                 key3d, keyres, keyftype)

        r = max(self.streams, key=_sortkey)
        if ftypestrict and preftype != 'any' and r.extension != preftype:
            return
        else:
            return r
            return

    def getbestaudio(self, preftype='any', ftypestrict=True):
        """ Return the highest bitrate audio Stream object."""

        def _sortkey(x, keybitrate=0, keyftype=0):
            """ Sort function for sort by bitrates. """
            keybitrate = int(x.rawbitrate)
            keyftype = preftype == x.extension
            if ftypestrict:
                return (keyftype, keybitrate)
            else:
                return (
                 keybitrate, keyftype)

        r = max(self.audiostreams, key=_sortkey)
        if ftypestrict and preftype != 'any' and r.extension != preftype:
            return
        else:
            return r
            return