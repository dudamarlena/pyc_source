# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/asynctwitch/dataclasses.py
# Compiled at: 2017-08-12 07:12:15
# Size of source mod 2**32: 14767 bytes
import asyncio, uuid, datetime, inspect, os
try:
    import isodate
    iso_installed = True
except ImportError:
    print('To use music, please install isodate. (pip install isodate)')
    iso_installed = False

try:
    import aiohttp
    aio_installed = True
except ImportError:
    print('To use stats from the API, make sure to install aiohttp. (pip install aiohttp)')
    aio_installed = False

def _parse_badges(s):
    if not s:
        return []
    else:
        if ',' in s:
            badges = s.split(',')
            return [Badge(*badge.split('/')) for badge in badges]
        return [Badge(*s.split('/'))]


def _parse_emotes(s):
    emotelist = []
    if not s:
        return []
    else:
        if '/' in s:
            emotes = s.split('/')
            for emote in emotes:
                res = emote.split(':')
                emote_id = res[0]
                locations = res[1]
                if ',' in locations:
                    for loc in locations.split(','):
                        emotelist.append(Emote(emote_id, loc))

                else:
                    emotelist.append(Emote(emote_id, locations))

        else:
            res = s.split(':')
            emote_id = res[0]
            locations = res[1]
            if ',' in locations:
                for loc in locations.split(','):
                    emotelist.append(Emote(emote_id, loc))

            else:
                emotelist.append(Emote(emote_id, locations))
        return emotelist


class Object:
    __doc__ = '\n    An object that may be created as substitute for functions.\n    '

    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)


class Emote:
    __doc__ = '\n    A class to hold emote data\n\n    Attributes\n    ----------\n    id : int\n        The ID of the emote.\n    location : str\n        The location of the emote in the message.\n    url : str\n        The url of the emote.\n    '

    def __init__(self, id, loc):
        self.id = int(id)
        self.location = loc
        self.url = 'https://static-cdn.jtvnw.net/emoticons/v1/{}/3.0'.format(id)

    def __str__(self):
        if not aio_installed:
            raise Exception('Please install aiohttp to use this feature')
        else:
            for k, v in emotes.items():
                if v['image_id'] == self.id:
                    return k

            return ''


class Badge:
    __doc__ = '\n    A class to hold badge data.\n\n    Attributes\n    ----------\n    name : str\n        Name of the badge.\n    value : str\n        Variant of the badge.\n    '

    def __init__(self, name, value):
        self.name = name
        self.value = value

    def __str__(self):
        return '{0.name}/{0.value}'.format(self)

    @classmethod
    def from_str(cls, s):
        """ e.g. Moderator/1 """
        n, v = s.split('/')
        return cls(n, v)


class Color:
    __doc__ = "\n    Available colors for non-turbo users when using Bot.color\n\n    Conversions are not working perfectly:\n\n    .. code-block:: python\n\n        >>> str( Color.blue() ) #0000FF\n        '#0000ff'\n\n        #0000FF to and from yiq\n        >>> str( Color.from_yiq( *Color.blue().to_yiq() ) )\n        '#0000fe'\n\n        #0000FF to and from hsv\n        >>> str( Color.from_hsv( *Color.blue().to_hsv() ) )\n        '#00ffff'\n        "

    def __init__(self, value):
        if not value:
            value = 0
        else:
            if isinstance(value, str):
                value = int(value.strip('#'), 16)
        self.value = value

    def _get_rgb(self, byte):
        return self.value >> 8 * byte & 255

    def _get_yiq(self, rm, gm, bm, mode):
        if mode == 'y':
            v1 = v2 = 1
        else:
            if mode == 'i':
                v1 = v2 = -1
            else:
                if mode == 'q':
                    v1 = -1
                    v2 = 1
        return round(rm * (self.r / 255) + v1 * (gm * (self.g / 255)) + v2 * (bm * (self.b / 255)), 3)

    def __eq__(self, clr):
        return isinstance(clr, Color) and self.value == clr.value

    def __ne__(self, clr):
        return not self.__eq__(clr)

    def __str__(self):
        return '#{:0>6x}'.format(self.value)

    def __add__(self, clr):
        return Color.from_rgb(min(self.r + clr.r, 255), min(self.g + clr.g, 255), min(self.b + clr.b, 255))

    def __sub__(self, clr):
        return Color.from_rgb(max(self.r - clr.r, 0), max(self.g - clr.g, 0), max(self.b - clr.b, 0))

    def blend(self, clr):
        return Color.from_rgb((self.r + clr.r) / 2, (self.g + clr.g) / 2, (self.b + clr.b) / 2)

    @property
    def r(self):
        return self._get_rgb(2)

    @property
    def g(self):
        return self._get_rgb(1)

    @property
    def b(self):
        return self._get_rgb(0)

    @r.setter
    def r(self, value):
        self = Color.from_rgb(value, self.g, self.b)

    @g.setter
    def g(self, value):
        self = Color.from_rgb(self.r, value, self.b)

    @b.setter
    def b(self, value):
        self = Color.from_rgb(self.r, self.g, value)

    @property
    def y(self):
        return self._get_yiq(0.299, 0.587, 0.114, 'y')

    @property
    def i(self):
        return self._get_yiq(0.596, 0.275, 0.321, 'i')

    @property
    def q(self):
        return self._get_yiq(0.212, 0.528, 0.311, 'q')

    @y.setter
    def y(self, value):
        self = Color.from_yiq(value, self.i, self.q)

    @i.setter
    def i(self, value):
        self = Color.from_yiq(self.y, value, self.q)

    @q.setter
    def q(self, value):
        self = Color.from_yiq(self.y, self.i, value)

    def to_rgb(self):
        """ Returns an (r, g, b) tuple of the color """
        return (
         self.r, self.g, self.b)

    def to_yiq(self):
        """ Returns a (y, i, q) tuple of the color """
        return (
         self.y, self.i, self.q)

    def to_hsv(self):
        """ Returns a (h, s, v) tuple of the color """
        r = self.r / 255
        g = self.b / 255
        b = self.b / 255
        _min = min(r, g, b)
        _max = max(r, g, b)
        v = _max
        delta = _max - _min
        if _max == 0:
            return (0, 0, v)
        else:
            s = delta / _max
            if delta == 0:
                delta = 1
            if r == _max:
                h = 60 * ((g - b) / delta % 6)
            else:
                if g == _max:
                    h = 60 * ((b - r) / delta + 2)
                else:
                    h = 60 * ((r - g) / delta + 4)
            return (
             round(h, 3), round(s, 3), round(v, 3))

    @classmethod
    def blue(cls):
        return cls(255)

    @classmethod
    def red(cls):
        return cls(16711680)

    @classmethod
    def chocolate(cls):
        return cls(13789470)

    @classmethod
    def green(cls):
        return cls(32768)

    @classmethod
    def hot_pink(cls):
        return cls(16738740)

    @classmethod
    def dodger_blue(cls):
        return cls(2003199)

    @classmethod
    def coral(cls):
        return cls(16744272)

    @classmethod
    def cadet_blue(cls):
        return cls(6266528)

    @classmethod
    def firebrick(cls):
        return cls(11674146)

    @classmethod
    def blue_violet(cls):
        return cls(9055202)

    @classmethod
    def golden_rod(cls):
        return cls(14329120)

    @classmethod
    def orange_red(cls):
        return cls(16729344)

    @classmethod
    def sea_green(cls):
        return cls(3050327)

    @classmethod
    def spring_green(cls):
        return cls(65407)

    @classmethod
    def yellow_green(cls):
        return cls(10145074)

    @classmethod
    def from_rgb(cls, r, g, b):
        """ (0,0,0) to (255,255,255) """
        value = (int(r) << 16) + (int(g) << 8) + int(b)
        return cls(value)

    @classmethod
    def from_yiq(cls, y, i, q):
        r = y + 0.956 * i + 0.621 * q
        g = y - 0.272 * i - 0.647 * q
        b = y - 1.108 * i + 1.705 * q
        r = 1 if r > 1 else max(0, r)
        g = 1 if g > 1 else max(0, g)
        b = 1 if b > 1 else max(0, b)
        return cls.from_rgb(round(r * 255, 3), round(g * 255, 3), round(b * 255, 3))

    @classmethod
    def from_hsv(cls, h, s, v):
        c = v * s
        h /= 60
        x = c * (1 - abs(h % 2 - 1))
        m = v - c
        if h < 1:
            res = (
             c, x, 0)
        else:
            if h < 2:
                res = (
                 x, c, 0)
            else:
                if h < 3:
                    res = (
                     0, c, x)
                else:
                    if h < 4:
                        res = (
                         0, x, c)
                    else:
                        if h < 5:
                            res = (
                             x, 0, c)
                        else:
                            if h < 6:
                                res = (
                                 c, 0, x)
                            else:
                                raise Exception('Unable to convert from HSV to RGB')
        r, g, b = res
        return cls.from_rgb(round((r + m) * 255, 3), round((g + m) * 255, 3), round((b + m) * 255, 3))


class Song:
    __doc__ = '\n    Contains information about a song\n\n    Attributes\n    ----------\n    title : str\n        The title of the song\n    '

    def __init__(self):
        self.title = ''
        self.is_playing = False

    def setattrs(self, obj):
        self.title = obj['title']
        try:
            if isinstance(obj['duration'], str):
                self.duration = isodate.parse_duration(obj['duration']).total_seconds()
            else:
                self.duration = obj['duration']
            self.uploader = obj['uploader']
            self.description = obj['description']
            self.categories = obj['categories']
            self.views = obj['view_count']
            self.thumbnail = obj['thumbnail']
            self.id = obj['id']
            self.is_live = obj['is_live']
            self.likes = obj['like_count']
            self.dislikes = obj['dislike_count']
        except Exception:
            pass

    def __str__(self):
        return self.title

    @asyncio.coroutine
    def _play(self, file, cleanup=True):
        if self.is_playing:
            raise Exception('Already playing!')
        self.is_playing = True
        yield from asyncio.create_subprocess_exec('ffplay',
          '-nodisp', '-autoexit', '-v', '-8', file, stdout=(asyncio.subprocess.DEVNULL),
          stderr=(asyncio.subprocess.DEVNULL))
        yield from asyncio.sleep(self.duration + 2)
        self.is_playing = False
        if cleanup:
            os.remove(file)
        if False:
            yield None


class User:
    __doc__ = ' Custom user class '

    def __init__(self, a, channel, tags=None):
        self.name = a
        self.channel = channel
        if tags:
            self.badges = _parse_badges(tags['badges'])
            self.color = Color(tags['color'])
            self.mod = tags['mod']
            self.subscriber = tags['subscriber']
            self.type = tags['user-type']
            try:
                self.turbo = tags['turbo']
                self.id = tags['user-id']
            except:
                pass


class Message:
    __doc__ = ' Custom message object to combine message, author and timestamp '

    def __init__(self, m, a, channel, tags):
        if tags:
            self.raw_timestamp = tags['tmi-sent-ts']
            self.timestamp = datetime.datetime.fromtimestamp(int(tags['tmi-sent-ts']) / 1000)
            self.emotes = _parse_emotes(tags['emotes'])
            self.id = uuid.UUID(tags['id'])
            self.room_id = tags['room-id']
        self.content = m
        self.author = User(a, channel, tags)
        self.channel = channel

    def __str__(self):
        return self.content


class Command:
    __doc__ = ' A command class to provide methods we can use with it '

    def __init__(self, bot, comm, desc='', alias=[], admin=False, unprefixed=False, listed=True):
        self.comm = comm
        self.desc = desc
        self.alias = alias
        self.admin = admin
        self.listed = listed
        self.unprefixed = unprefixed
        self.subcommands = {}
        self.bot = bot
        bot.commands[comm] = self
        for a in self.alias:
            bot.commands[a] = self

    def subcommand(self, *args, **kwargs):
        """ Create subcommands """
        return SubCommand(self, *args, **kwargs)

    def __call__(self, func):
        """ Make it able to be a decorator """
        self.func = func
        return self

    @asyncio.coroutine
    def run(self, message):
        """ Does type checking for command arguments """
        args = message.content[len(self.bot.prefix):].split(' ')[1:]
        args_name = inspect.getfullargspec(self.func)[0][1:]
        if len(args) > len(args_name):
            args[len(args_name) - 1] = ' '.join(args[len(args_name) - 1:])
            args = args[:len(args_name)]
        else:
            ann = self.func.__annotations__
            for x in range(0, len(args_name)):
                try:
                    v = args[x]
                    k = args_name[x]
                    if not type(v) == ann[k]:
                        try:
                            v = ann[k](v)
                        except Exception:
                            raise TypeError('Invalid type: got {}, {} expected'.format(ann[k].__name__, v.__name__))

                    args[x] = v
                except IndexError:
                    break

            if len(list(self.subcommands.keys())) > 0:
                try:
                    subcomm = args.pop(0).split(' ')[0]
                except Exception:
                    yield from (self.func)(message, *args)
                    return
                else:
                    if subcomm in self.subcommands.keys():
                        c = message.content.split(' ')
                        c.pop(1)
                        message.content = ' '.join(c)
                        yield from self.subcommands[subcomm].run(message)
                    else:
                        yield from (self.func)(message, *args)
            else:
                try:
                    yield from (self.func)(message, *args)
                except TypeError as e:
                    if len(args) < len(args_name):
                        raise Exception('Not enough arguments for {}, required arguments: {}'.format(self.comm, ', '.join(args_name)))
                    else:
                        raise e

        if False:
            yield None


class SubCommand(Command):
    __doc__ = ' Subcommand class '

    def __init__(self, parent, comm, desc, *alias):
        self.comm = comm
        self.parent = parent
        self.subcommands = {}
        parent.subcommands[comm] = self
        for a in alias:
            parent.subcommands[a] = self