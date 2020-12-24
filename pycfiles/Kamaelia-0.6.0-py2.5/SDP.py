# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/Kamaelia/Protocol/SDP.py
# Compiled at: 2008-10-19 12:19:52
"""==========================================
Session Description Protocol (SDP) Support
==========================================

The SDPParser component parses Session Description Protocol (see `RFC 4566`_) data
sent to it as individual lines of text (not multiline strings) and outputs a
dictionary containing the parsed session description.

.. _`RFC 4566`: http://tools.ietf.org/html/rfc4566

Example Usage
-------------

Fetch SDP data from a URL, parse it, and display the output::

    Pipeline( OneShot("http://www.mysite.com/sessiondescription.sdp"),
              SimpleHTTPClient(),
              chunks_to_lines(),
              SDPParser(),
              ConsoleEchoer(),
            ).run()

If the session description at the URL provided is this::

    v=0
    o=jdoe 2890844526 2890842807 IN IP4 10.47.16.5
    s=SDP Seminar
    i=A Seminar on the session description protocol
    u=http://www.example.com/seminars/sdp.pdf
    e=j.doe@example.com (Jane Doe)
    c=IN IP4 224.2.17.12/127
    t=2873397496 2873404696
    a=recvonly
    m=audio 49170 RTP/AVP 0
    m=video 51372 RTP/AVP 99
    a=rtpmap:99 h263-1998/90000

Then parsing will return this dictionary::

    { 'protocol_version': 0,
      'origin'     : ('jdoe', 2890844526, 2890842807, 'IN', 'IP4', '10.47.16.5'),
      'sessionname': 'SDP Seminar',
      'information': 'A Seminar on the session description protocol',
      'connection' : ('IN', 'IP4', '224.2.17.12', '127', 1),
      'time'       : [(2873397496L, 2873404696L, [])],
      'URI'        : 'http://www.example.com/seminars/sdp.pdf',
      'email'      : 'j.doe@example.com (Jane Doe)',
      'attribute'  : ['recvonly'],
      'media':
          [ { 'media'     : ('audio', 49170, 1, 'RTP/AVP', '0'),
              'connection': ('IN', 'IP4', '224.2.17.12', '127', 1)
            },
            { 'media'     : ('video', 51372, 1, 'RTP/AVP', '99'),
              'connection': ('IN', 'IP4', '224.2.17.12', '127', 1),
              'attribute' : ['rtpmap:99 h263-1998/90000']
            }
          ],
    }

    
Behaviour
---------

Send individual lines as strings to SDPParser's "inbox" inbox. SDPParser cannot
handle multiple lines in the same string.

When SDPParser receives a producerFinished() message on its "control" inbox, or
if it encounter another "v=" line then it knows it has reached the end of the
SDP data and will output the parsed data as a dictionary to its "outbox" outbox.

The SDP format does *not* contain any kind of marker to signify the end of a
session description - so SDPParser only deduces this by being told that the
producer/data source has finished, or if it encounters a "v=" line indicating
the start of another session description.

SDPParser can parse more than one session description, one after the other.

If the SDP data is malformed AssertionError, or other exceptions, may be raised.
SDPParser does not rigorously test for exact compliance - it just complains if
there are glaring problems, such as fields appearing in the wrong sections!

If a producerFinished or shutdownMicroprocess message is received on the
"control" inbox then, once any pending data at the "inbox" inbox has been
processed, this component will terminate. It will send the message on out of
its "signal" outbox.

Only if the message is a producerFinished message will it output the session
description is has been parsing. A shutdownMicroprocess message will not result
in it being output.

Format of parsed output
-----------------------

The result of parsing SDP data is a dictionary mapping descriptive names of
types to values:

 ======  ======================  ======================================================================
 Session Description
 ------------------------------------------------------------------------------------------------------
 Type    Dictionary key          Format of the value
 ======  ======================  ======================================================================
 v       "protocol_version"      version_number
 o       "origin"                ("user", session_id, session_version, "net_type", "addr_type", "addr")
 s       "sessionname"           "session name"
 t & r   "time"                  (starttime, stoptime, [repeat,repeat, ...])
                                    where repeat = (interval,duration,[offset,offset, ...])
 a       "attribute"             "value of attribute"
 b       "bandwidth"             (mode, bitspersecond)
 i       "information"           "value"
 e       "email"                 "email-address"
 u       "URI"                   "uri"
 p       "phone"                 "phone-number"
 c       "connection"            ("net_type", "addr_type", "addr", ttl, groupsize)
 z       "timezone adjustments"  [(adj-time,offset), (adj-time,offset), ...]
 k       "encryption"            ("method","value")
 m       "media"                 [media-description, media-description, ... ]
                                     see next table for media description structure
 ======  ======================  ======================================================================

Note that 't' and 'r' lines are combined in the dictionary into a single
"time" key containing both the start and end times specified in the 't' line
and a list of any repeats specified in any 'r' lines present.

The "media" key contains a list of media descriptions. Like for the overall
session description, each is parsed into a dictionary, that will contain some
or all of the following:

 ======  ======================  ======================================================================
 Media Descriptions
 ------------------------------------------------------------------------------------------------------
 Type    Dictionary key          Format of the value
 ======  ======================  ======================================================================
 m       "media"                 ("media-type", port-number, number-of-ports, "protocol", "format")
 c       "connection"            ("net_type", "addr_type", "addr", ttl, groupsize)
 b       "bandwidth"             (mode, bitspersecond)
 i       "information"           "value"
 k       "encryption"            ("method","value")
 a       "attribute"             "value of attribute"
 ======  ======================  ======================================================================

Some lines are optional in SDP. If they are not included, then the parsed output
will not contain the corresponding key.
 
The formats of values are left unchanged by the parsing. For example, integers
representing times are simply converted to integers, but the units used remain
unchanged (ie. they will not be converted to unix time units).

"""
from Axon.Component import component
from Axon.Ipc import producerFinished, shutdownMicroprocess
import re

class SDPParser(component):
    """    SDPParser() -> new SDPParser component.

    Parses Session Description Protocol data (see RFC 4566) sent to its "inbox"
    inbox as individual strings for each line of the SDP data. Outputs a dict
    containing the parsed data from its "outbox" outbox.
    """
    Inboxes = {'inbox': 'SDP data in strings, each containing a single line', 'control': 'Shutdown signalling'}
    Outboxes = {'outbox': 'Parsed SDP data in a dictionary', 'signal': 'Shutdown signalling'}

    def handleControl(self):
        while self.dataReady('control'):
            msg = self.recv('control')
            if isinstance(msg, producerFinished):
                self.shutdownMsg = msg
                raise 'DONE'
            elif isinstance(msg, shutdownMicroprocess):
                self.shutdownMsg = msg
                raise 'STOP'
            else:
                self.send(msg, 'signal')

    def readline(self):
        while 1:
            if self.dataReady('inbox'):
                line = self.recv('inbox')
                if line != '':
                    yield line
                    return
            self.handleControl()
            self.pause()
            yield

        return

    def main(self):
        self.shutdownMsg = None
        session = {}
        mandatory = 'XXX'
        try:
            for line in self.readline():
                yield 1

            (type, key, value) = _parseline(line)
            while 1:
                session = {}
                mandatory = 'vost'
                multiple_allowed = 'abtr'
                single_allowed = 'vosiuepcbzk'
                most_recent_t = None
                while type != 'm':
                    if type == 'v' and 'v' not in mandatory:
                        break
                    mandatory = mandatory.replace(type, '')
                    if not type in single_allowed:
                        assert type in multiple_allowed
                        single_allowed = single_allowed.replace(type, '')
                        if type in multiple_allowed:
                            assert type == 'r' and most_recent_t is not None
                            most_recent_t[2].append(value)
                        else:
                            session[key] = session.get(key, [])
                            session[key].append(value)
                    else:
                        session[key] = value
                    for line in self.readline():
                        yield 1

                    (type, key, value) = _parseline(line)

                assert mandatory == ''
                mandatory_additional = ''
                if 'c' in single_allowed:
                    mandatory_additional += 'c'
                session['media'] = []
                while type == 'm':
                    mandatory = '' + mandatory_additional
                    multiple_allowed = 'a'
                    single_allowed = 'icbk'
                    media = {key: value}
                    session['media'].append(media)
                    for line in self.readline():
                        yield 1

                    (type, key, value) = _parseline(line)
                    while type != 'm' and type != 'v':
                        mandatory = mandatory.replace(type, '')
                        assert type in single_allowed or type in multiple_allowed
                        single_allowed = single_allowed.replace(type, '')
                        if type in multiple_allowed:
                            media[key] = media.get(key, [])
                            media[key].append(value)
                        else:
                            media[key] = value
                        for line in self.readline():
                            yield 1

                        (type, key, value) = _parseline(line)

                    assert mandatory == ''

                self.sendOutParsedSDP(session)

        except 'DONE':
            if mandatory == '':
                self.sendOutParsedSDP(session)
            yield 1
        except 'STOP':
            pass

        if self.shutdownMsg is None:
            self.shutdownMsg = producerFinished()
        self.send(self.shutdownMsg, 'signal')
        return

    def sendOutParsedSDP(self, session):
        if 'connection' in session:
            for media in session['media']:
                media['connection'] = session['connection']

        self.send(session, 'outbox')


def _parseline(line):
    match = re.match('^(.)=(.*)', line)
    type, value = match.group(1), match.group(2)
    if type == 'v':
        assert value == '0'
        return (type, 'protocol_version', int(value))
    elif type == 'o':
        (user, sid, ver, ntype, atype, addr) = re.match('^ *(\\S+) +(\\d+) +(\\d+) +(IN) +(IP[46]) +(.+)', value).groups()
        return (type, 'origin', (user, int(sid), int(ver), ntype, atype, addr))
    elif type == 's':
        return (
         type, 'sessionname', value)
    elif type == 'i':
        return (
         type, 'information', value)
    elif type == 'u':
        return (
         type, 'URI', value)
    elif type == 'e':
        return (
         type, 'email', value)
    elif type == 'p':
        return (
         type, 'phone', value)
    elif type == 'c':
        if re.match('^ *IN +IP4 +.*$', value):
            match = re.match('^ *IN +IP4 +([^/]+)(?:/(\\d+)(?:/(\\d+))?)? *$', value)
            (ntype, atype) = ('IN', 'IP4')
            (addr, ttl, groupsize) = match.groups()
            if ttl is None:
                ttl = 127
            if groupsize is None:
                groupsize = 1
        elif re.match('^ *IN +IP6 +.*$', value):
            match = re.match('^ *IN +IP6 +([abcdefABCDEF0123456789:.]+)(?:/(\\d+))? *$')
            (ntype, atype) = ('IN', 'IP6')
            (addr, groupsize) = match.groups()
        else:
            assert False
        return (type, 'connection', (ntype, atype, addr, ttl, groupsize))
    elif type == 'b':
        (mode, rate) = re.match('^ *((?:AS)|(?:CT)|(?:X-[^:]+)):(\\d+) *$', value).groups()
        bitspersecond = long(rate) * 1000
        return (type, 'bandwidth', (mode, bitspersecond))
    elif type == 't':
        (start, stop) = [ long(x) for x in re.match('^ *(\\d+) +(\\d+) *$', value).groups() ]
        repeats = []
        return (type, 'time', (start, stop, repeats))
    elif type == 'r':
        terms = re.split('\\s+', value)
        parsedterms = []
        for term in terms:
            (value, unit) = re.match('^\\d+([dhms])?$').groups()
            value = long(value) * {None: 1, 's': 1, 'm': 60, 'h': 3600, 'd': 86400}[unit]
            parsedterms.append(value)

        interval, duration = parsedterms[0], parsedterms[1]
        offsets = parsedterms[2:]
        return (type, 'repeats', (interval, duration, offsets))
    elif type == 'z':
        adjustments = []
        while value.strip() != '':
            (adjtime, offset, offsetunit, value) = re.match('^ *(\\d+) +([+-]?\\d+)([dhms])? *?(.*)$', value).groups()
            adjtime = long(adjtime)
            offset = long(offset) * {None: 1, 's': 1, 'm': 60, 'h': 3600, 'd': 86400}[offsetunit]
            adjustments.append((adjtime, offset))

        return (type, 'timezone adjustments', adjustments)
    elif type == 'k':
        (method, value) = re.match('^(clear|base64|uri|prompt)(?:[:](.*))?$', value).groups()
        return (type, 'encryption', (method, value))
    elif type == 'a':
        return (
         type, 'attribute', value)
    elif type == 'm':
        (media, port, numports, protocol, fmt) = re.match('^(audio|video|text|application|message) +(\\d+)(?:[/](\\d+))? +([^ ]+) +(.+)$', value).groups()
        port = int(port)
        if numports is None:
            numports = 1
        else:
            numports = int(numports)
        return (
         type, 'media', (media, port, numports, protocol, fmt))
    else:
        return (
         type, 'unknown', value)
    return


__kamaelia_components__ = (
 SDPParser,)
if __name__ == '__main__':
    from Kamaelia.Util.DataSource import DataSource
    from Kamaelia.Chassis.Pipeline import Pipeline
    from Kamaelia.Util.Console import ConsoleEchoer
    sdp = ('v=0\no=jdoe 2890844526 2890842807 IN IP4 10.47.16.5\ns=SDP Seminar\ni=A Seminar on the session description protocol\nu=http://www.example.com/seminars/sdp.pdf\ne=j.doe@example.com (Jane Doe)\nc=IN IP4 224.2.17.12/127\nt=2873397496 2873404696\na=recvonly\nm=audio 49170 RTP/AVP 0\nm=video 51372 RTP/AVP 99\na=rtpmap:99 h263-1998/90000\n\nv=0\no=bfcrd 1140190501 1140190501 IN IP4 132.185.224.80\ns=BFC ONE [H.264/AVC]\ni=Multicast trial service from the BBC! Get BFC FLURBLE here!\na=x-qt-text-nam:BFC FLURBLE [H.264/AVC]\na=x-qt-text-aut:BFC Research & Development\na=x-qt-text-cpy:Copyright (c) 2006 British Flurbling Corporation\nu=http://www.bbc.co.uk/multicast/\ne=Multicast Support <multicast-tech@bfc.co.uk>\nt=0 0\nc=IN IP4 233.122.227.151/32\nm=video 5150 RTP/AVP 33\nb=AS:1200000\na=type:broadcast\na=mux:m2t\n\nv=0\n\n\n').splitlines()
    Pipeline(DataSource(sdp), SDPParser(), ConsoleEchoer()).run()