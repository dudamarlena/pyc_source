# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/klog.py
# Compiled at: 2011-12-03 15:03:14
import sys, time
DEFAULT_FORMAT_STR = '%(info_fmt_start)s[%(time)s] %(logger)s > %(channel)s%(info_fmt_end)s %(msg_fmt_start)s%(level)s: %(msg)s%(msg_fmt_end)s'

class Output(object):
    """Formats the log messages and outputs them.
  
  .. note::
    
    This is an abstract class and should not be instantaniated. Instead,
    subclasses should override the :method:`Output.log` method.
  
  Attributes:
    `formatstr` (str):
      The format string for the messages. It uses normal Python string
      formatting syntax with keyword arguments. The available keywords
      are:
      
      %(logger)s:
        The name of the logger.
      %(channel)s:
        The name of the channel.
      %(level)s:
        The name of the level.
      %(msg)s:
        The actual log message.
      %(time)s:
        The current time, as returned by :func:
  """

    def __init__(self, formatstr=DEFAULT_FORMAT_STR):
        """
    Args:
      `formatstr` (str):
        The format string for the messages. Defaults to
        DEFAULT_FORMAT_STR.
    """
        self.formatstr = formatstr

    def log(self, logger, channel, level, msg):
        """Logs a message. On the base class :class:`Output` this is just a
    stub method.
    
    Args:
      `logger` (:class:`Logger`):
        The logger that sent the message.
      `channel` (:class:`Channel`):
        The channel that collected the message.
      `level` (:class:`Level`):
        The level of the message.
      `msg` (str):
        The log message
    """
        pass

    def format_msg(self, logger, channel, level, msg):
        """Formats a message using the `formatstr` attribute.
    
    Args:
      `logger` (:class:`Logger`):
        The logger that sent the message.
      `channel` (:class:`Channel`):
        The channel that collected the message.
      `level` (:class:`Level`):
        The level of the message.
      `msg` (str):
        The log message.
    
    Returns:
      The formatted message.
    """
        d = {'logger': logger.name, 
           'channel': channel.name, 
           'level': level.name, 
           'msg': msg, 
           'time': time.asctime(), 
           'info_fmt_start': level.info_fmt_start, 
           'info_fmt_end': level.info_fmt_end, 
           'msg_fmt_start': level.msg_fmt_start, 
           'msg_fmt_end': level.msg_fmt_end}
        return self.formatstr % d


class StreamOutput(Output):
    """A subclass of :class:`Output` that sends output to a file-like
  object.
  
  Attributes:
    `formatstr` (str):
      The format string for the messages. See the documentation for
      :class:`Output` for information on its format.
    `stream` (file-like object):
      The object to send output to. It must have a `write()` method.
    `use_ansi_escapes` (bool):
      Whether to use ANSI escape codes to show visually formatted
      messages. Only really useful if the output stream is stdout.
  
  """

    def __init__(self, stream=None, formatstr=DEFAULT_FORMAT_STR):
        """
    
    Args:
      `stream` (file-like object):
        The object to send output to. It must have a `write()` method.
      `formatstr` (str):
        The format string for the messages. Defaults to
        DEFAULT_FORMAT_STR.
      `use_ansi_escapes` (bool):
        Whether to use ANSI escape codes to show visually formatted
        messages. Only really useful if the output stream is stdout.
      
    """
        if stream is None:
            stream = sys.stdout
        self.formatstr = formatstr
        self.stream = stream
        return

    def log(self, logger, channel, level, msg):
        """Logs a message.
    
    Args:
      `logger` (:class:`Logger`):
        The logger that sent the message.
      `channel` (:class:`Channel`):
        The channel that collected the message.
      `level` (:class:`Level`):
        The level of the message.
      `msg` (str):
        The log message.
    """
        formatted = self.format_msg(logger, channel, level, msg)
        self.stream.write(formatted + '\n')


class FileOutput(StreamOutput):

    def __init__(self, fname, formatstr=DEFAULT_FORMAT_STR):
        self.formatstr = formatstr
        self.stream = open(fname, 'w')

    def __del__(self):
        self.stream.close()


class Filter(object):

    def __init__(self):
        pass

    def allow(self, logger, channel, level, msg):
        return True


class LevelFilter(object):

    def __init__(self, minlevel=0.0, maxlevel=1.0):
        if isinstance(minlevel, str):
            minlevel = LevelManager.get(minlevel)
        if isinstance(minlevel, Level):
            minlevel = minlevel.priority
        if isinstance(maxlevel, str):
            maxlevel = LevelManager.get(maxlevel)
        if isinstance(maxlevel, Level):
            maxlevel = maxlevel.priority
        self.minlevel = minlevel
        self.maxlevel = maxlevel

    def allow(self, logger, channel, level, msg):
        return level.priority >= self.minlevel and level.priority <= self.maxlevel


class Channel(object):

    def __init__(self, name, outputs=None, filters=None):
        if outputs is None:
            outputs = [
             StreamOutput()]
        if filters is None:
            filters = []
        self.name = name
        self.outputs = outputs
        self.filters = filters
        return

    def add_output(self, output):
        self.outputs.append(output)

    def add_filter(self, filter):
        self.filters.append(filter)

    def log(self, logger, level, msg, channel=None):
        if channel is None:
            channel = self
        for filter in self.filters:
            if not filter.allow(logger, channel, level, msg):
                return

        for output in self.outputs:
            output.log(logger, channel, level, msg)

        return


class RedirectionChannel(Channel):

    def __init__(self, name, dest):
        self.name = name
        if isinstance(dest, str):
            dest = ChannelManager.get(dest)
            if dest is None:
                raise ValueError('Invalid channel')
        self.dest = dest
        return

    def log(self, logger, level, msg):
        self.dest.log(logger, level, msg, self)


class Level(object):

    def __init__(self, name, priority):
        self.name = name.upper()
        self.priority = priority
        self.info_fmt_start = ''
        self.info_fmt_end = ''
        self.msg_fmt_start = ''
        self.msg_fmt_end = ''


def set_ansi_colour(level, clr):
    level.msg_fmt_start = '\x1b[3%dm' % clr
    level.msg_fmt_end = '\x1b[m'
    return level


class ObjectManagerClass(object):

    def __init__(self):
        self.objects = {}

    def add(self, obj):
        self.objects[obj.name.lower()] = obj

    def get(self, name):
        return self.objects.get(name.lower(), None)


ChannelManager = ObjectManagerClass()
ChannelManager.add(Channel('main'))
LevelManager = ObjectManagerClass()
LevelManager.add(set_ansi_colour(Level('DEBUG', 0.1), 4))
LevelManager.add(set_ansi_colour(Level('INFO', 0.3), 6))
LevelManager.add(set_ansi_colour(Level('WARNING', 0.5), 3))
LevelManager.add(set_ansi_colour(Level('ERROR', 0.8), 1))
LevelManager.add(set_ansi_colour(Level('FATAL', 1.0), 5))

class Logger(object):

    def __init__(self, name):
        self.name = name

    def log(self, channel, level, msg):
        if isinstance(channel, str):
            channel = ChannelManager.get(channel)
            if channel is None:
                raise ValueError('Invalid channel')
        if isinstance(level, str):
            level = LevelManager.get(level)
            if level is None:
                raise ValueError('Invalid level')
        channel.log(self, level, msg)
        return