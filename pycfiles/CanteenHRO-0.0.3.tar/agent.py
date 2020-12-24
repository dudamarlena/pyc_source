# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /usr/local/lib/python2.7/site-packages/canteen/logic/http/agent.py
# Compiled at: 2014-09-26 04:50:19
__doc__ = '\n\n  HTTP agent logic\n  ~~~~~~~~~~~~~~~~\n\n  :author: Sam Gammon <sg@samgammon.com>\n  :copyright: (c) Sam Gammon, 2014\n  :license: This software makes use of the MIT Open Source License.\n            A copy of this license is included as ``LICENSE.md`` in\n            the root of the project.\n\n'
from canteen.base import logic
from canteen.util import struct
from canteen.util import decorators

class Vendor(struct.BidirectionalEnum):
    """ Enumerated common vendors that can be found in an HTTP client or browser's
      ``User-Agent`` string. """
    GOOGLE = 0
    MOZILLA = 1
    MICROSOFT = 2
    OPERA = 3
    APPLE = 4
    OPEN = 5
    OTHER = 6


class AgentInfo(object):
    """ Base class structure that removes object slots in favor of an extendable,
      fully-static object structure. Used for indivisual objects that retain or
      specify details about an HTTP client's ``User-Agent`` string. """
    __slots__ = tuple()

    def dump(self):
        """ Dump the local data carried by this ``AgentInfo`` object or subclass
        object.

        :returns: Dictionary (``dict``) of held ``key => value`` pairs. """
        return dict((k, getattr(self, k, None)) for k in self.__slots__)

    def __repr__(self):
        """ Generate a pleasant string representation for this unit of
        ``AgentInfo``.

        :returns: Human-readable string representation of this object. """
        return '%s(%s)' % (
         self.__class__.__name__.replace('Agent', ''),
         (', ').join(('=').join((i, str(getattr(self, i) if hasattr(self, i) else None))) for i in self.__slots__ if not i.startswith('__')))


class AgentVersion(AgentInfo):
    """ Holds parsed version information for a software HTTP client or browser,
      found while scanning the ``User-Agent`` header. """
    __slots__ = ('major', 'minor', 'micro')

    def __init__(self, major, minor=None, micro=None):
        """ Initialize this version info container.

        :param major: Major version.
        :param minor: Minor version (optional, defaults to ``None``).
        :param micro: Micro version (optional, defaults to ``None``). """
        self.major, self.minor, self.micro = major, minor, micro


class AgentOS(AgentInfo):
    """ Holds parsed operating system information for a software HTTP client or
      browser, found while scanning the ``User-Agent`` string. """
    __slots__ = ('name', 'vendor', 'version')

    def __init__(self, name, vendor, version):
        """ Initialize this OS info container.

        :param name: Name of the operating system running on the host described
          by the subject ``User-Agent`` string.

        :param vendor: Software vendor that produced the operating system
          running on the host described by the ``User-Agent`` string.

        :param version: Version information for the operating system running on
          the host described by the ``User-Agent`` string. """
        self.name, self.vendor, self.version = name, vendor, version

    @classmethod
    def scan(cls, request, user_agent, detected):
        """ Scan a target ``user_agent`` string, encapsulated by an HTTP
        ``request``, for information about an HTTP client or browser's active
        operating system.

        :param request: HTTP request that carries with it the ``User-Agent``
          header in question.

        :param user_agent: Specifically, the ``User-Agent`` that the framework
          wishes us to scan.

        :param detected: Container of other information detected so-far in the
          ``User-Agent`` detection process.

        :returns: Spawned ``AgentOS`` info container describing any operating
          system information in the ``User-Agent`` in question."""
        return cls(*{'bsd': (
                 'BSD', Vendor.OPEN, AgentVersion(0)), 
           'linux': (
                   'Linux', Vendor.OPEN, AgentVersion(0)), 
           'macos': (
                   'Mac OS X', Vendor.APPLE, AgentVersion(0)), 
           'windows': (
                     'Windows', Vendor.MICROSOFT, AgentVersion(0)), 
           'ipad': (
                  'iOS', Vendor.APPLE, AgentVersion(0)), 
           'iphone': (
                    'iOS', Vendor.APPLE, AgentVersion(0))}.get(user_agent.platform.lower().strip(), (
         'unknown', Vendor.OTHER, AgentVersion(0))))


class AgentCapabilities(AgentInfo):
    """ Holds parsed or detected information about a software HTTP client or
      browser's extra/interesting capabilities. """
    __slots__ = ('spdy', 'quic', 'webp', 'webm', 'http2')

    def __init__(self, **kwargs):
        """ Initialize this capabilities container.

        :param **kwargs: Accepts keywords for supported flags, to set them as
          active (``True``) or inactive (``False``). Currently, the supported
          capabilities flags are all ``bool`` and consist of:

          - ``spdy`` - is the client browser communicating over SPDY?
          - ``quic`` - is the client browser communicating over QUIC?
          - ``http2`` - is the client browser communicating over HTTP2?
          - ``webp`` - does the client indicate support for WebP?
          - ``webm`` - does the client indicate support for WebM?  """
        for datapoint in self.__slots__:
            setattr(self, datapoint, kwargs[datapoint] if datapoint in kwargs else None)

        return

    @classmethod
    def scan(cls, request, user_agent, detected):
        """ Scan a target ``user_agent`` string, encapsulated by an HTTP
        ``request``, for information about an HTTP client or browser's
        indicated or implied capabilities.

        :param request: HTTP request that contains the original ``User-Agent``
          header to be scanned.

        :param user_agent: Specifically, the ``User-Agent`` that the framework
          wishes us to scan, should it be different from the original.

        :param detected: Container of other information detected so-far in the
          ``User-Agent`` scanning process.

        :returns: Spawned ``AgentCapabilities`` object describing any detected
          capabilities implied or indicated by the subject ``User-Agent``
          string. """
        detected = {}
        accept_string = request.headers['Accept'] if 'Accept' in request.headers else ''
        for datapoint, conditional in (
         (
          'quic', user_agent.browser == 'chrome'),
         (
          'spdy', user_agent.browser in ('chrome', 'firefox', 'opera')),
         (
          'webm', user_agent.browser in ('chrome', 'firefox', 'opera')),
         (
          'webp', user_agent.browser == 'chrome' or 'webp' in accept_string)):
            detected[datapoint] = conditional

        return cls(**detected)


class AgentFingerprint(AgentInfo):
    """ Holds a full picture of detected information about a software HTTP client
      or browser, scanned or inferred from various request headers such as
      ``User-Agent`` and ``Accept``.

      Encapsulates local information about:

      - asset quality preferences indicated by browser
      - general flags for whether a client is *modern* or *ancient*
      - supported languages, character sets, mimetypes and encodings
      - a client's OS (contained in an ``AgentOS`` instance)
      - a client's inferred or indicated capabilities (in an
        ``AgentCapabilities`` instance) """
    __slots__ = ('accept', 'string', 'vendor', 'version', 'quality', 'charsets', 'encodings',
                 'languages', 'mimetypes', 'modern', 'ancient', 'chrome', 'seamonkey',
                 'msie', 'safari', 'firefox', 'opera', 'googlebot', 'aol', 'ask',
                 'yahoo', 'mobile', 'tablet', 'desktop', 'crawler', 'gecko', 'blink',
                 'webkit', 'presto', 'trident', 'spidermonkey', '__os__', '__supports__')

    def __init__(self, **kwargs):
        """ Initialize a new ``AgentFingerprint`` object.

        :param **kwargs: Arbitrary container of parameters to write into the
          new ``AgentFingerprint`` object. Valid options are specified in the
          object's ``__slots__`` attribute. """
        self.__os__, self.__supports__ = (None, None)
        for datapoint in self.__slots__:
            setattr(self, datapoint, kwargs[datapoint] if datapoint in kwargs else None)

        return

    @property
    def os(self):
        """ Property accessor for detected operating system information.

        :returns: ``AgentOS`` instance describing operating system information
          for a given ``AgentFingerprint`` subject. """
        return self.__os__

    @property
    def supports(self):
        """ Property accessor for inferred or indicated client capabilities.

        :returns: ``AgentCapabilities`` instance describing detected/supported
          capabilities and features for a given ``AgentFingerprint``
          subject. """
        return self.__supports__

    capabilities = supports

    @classmethod
    def scan(cls, request, ua):
        """ Scan a target HTTP ``request`` and ``User-Agent`` string for various
        pieces of information, such as an OS, browser/vendor, etc. Also scan
        other request-based headers that can provide hints about supported
        browser features and options.

        :param request: Original HTTP request providing the ``User-Agent`` to
          be scanned.

        :param ua: Specific ``User-Agent`` string requested for parsing by the
          framework.

        :returns: Spawned ``AgentFingerprint`` instance describing any and all
          information available to be parsed from the ``User-Agent`` and
          ``Accept``-series request headers. """
        detected = {'accept': request.headers.get('accept'), 
           'string': request.headers.get('user-agent'), 
           'charsets': request.accept_charsets, 
           'encodings': request.accept_encodings, 
           'languages': request.accept_languages, 
           'mimetypes': request.accept_mimetypes}
        if ua is None:
            return cls(**{})
        else:
            version = detected['version'] = ua.version.split('.')
            version_spec = []
            for grouping in version:
                if len(version_spec) >= 3:
                    break
                try:
                    version_spec.append(int(grouping))
                except ValueError:
                    break

            version = detected['version'] = AgentVersion(*tuple(version_spec)) if version_spec else AgentVersion(0)
            platform = ua.platform.lower().strip()
            for datapoint, condition in (
             (
              'chrome', ua.browser == 'chrome'),
             (
              'firefox', ua.browser == 'firefox'),
             (
              'seamonkey', ua.browser == 'seamonkey'),
             (
              'safari', ua.browser == 'safari'),
             (
              'opera', ua.browser == 'opera'),
             (
              'msie', ua.browser == 'msie'),
             (
              'googlebot', ua.browser == 'google'),
             (
              'yahoo', ua.browser == 'yahoo'),
             (
              'aol', ua.browser == 'aol'),
             (
              'ask', ua.browser == 'ask'),
             (
              'trident', ua.browser == 'msie'),
             (
              'blink', ua.browser in ('chrome', 'opera')),
             (
              'presto', ua.browser == 'opera' and version.major < 15),
             (
              'webkit', ua.browser in ('safari', 'chrome', 'opera')),
             (
              'spidermonkey', ua.browser in ('firefox', 'seamonkey')),
             (
              'gecko',
              'Gecko' in ua.string and 'WebKit' not in ua.string and 'Chrome' not in ua.string),
             (
              'tablet', 'Tabl' in ua.string or 'iPad' in ua.string),
             (
              'crawler', ua.browser in ('google', 'yahoo', 'aol', 'ask')),
             (
              'mobile',
              'Mobi' in ua.string or 'IEMobile' in ua.string or platform in ('ios', 'iphone', 'ipad'))):
                detected[datapoint] = condition

            detected['vendor'] = Vendor.OTHER
            for k, v in {Vendor.GOOGLE: detected.get('chrome') or detected.get('googlebot'), 
               Vendor.MOZILLA: detected.get('firefox') or detected.get('seamonkey'), 
               Vendor.MICROSOFT: detected.get('msie'), 
               Vendor.OPERA: detected.get('opera'), 
               Vendor.APPLE: detected.get('safari'), 
               Vendor.OPEN: detected.get('seamonkey')}.iteritems():
                if v:
                    detected['vendor'] = k

            detected['desktop'] = not any((
             detected.get('mobile'), detected.get('tablet')))
            detected['__os__'] = AgentOS.scan(request, ua, detected)
            detected['__supports__'] = AgentCapabilities.scan(request, ua, detected)
            detected['modern'] = (detected['chrome'] or detected['safari'] or detected['firefox'] or detected['opera']) and detected['__os__'].name in ('Mac OS X',
                                                                                                                                                        'Windows',
                                                                                                                                                        'Linux')
            detected['quality'] = {}
            if 'mimetypes' in detected:
                for mime, quality in detected['mimetypes']:
                    detected['quality'][mime] = quality

            detected['ancient'] = not detected['modern']
            return cls(**detected)


@decorators.bind('http.agent')
class UserAgent(logic.Logic):
    """ Provides structured access to HTTP request headers. Interrogates values
      such as ``User-Agent`` and ``Accept`` to infer or detect things such as a
      client's OS, browser, and feature capabilities. """

    @staticmethod
    def scan(request):
        """ Scan an HTTP ``request`` for information about the other end of the
        connection. Detect as much information as possible from headers such as
        ``User-Agent`` and ``Accept``.

        :param request: HTTP request to be scanned.

        :returns: :py:class:`AgentFingerprint` instance containing any detected
          information found in the ``User-Agent`` or ``Accept``-series request
          headers. """
        return AgentFingerprint.scan(request, request.user_agent)