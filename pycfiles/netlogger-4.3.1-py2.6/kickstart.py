# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-x86_64/egg/netlogger/parsers/modules/kickstart.py
# Compiled at: 2010-04-29 00:14:32
"""
A Pegasus log parser.
"""
__author__ = '$Author: dang $'
__rcsid__ = '$Id: kickstart.py 24753 2010-04-29 04:14:31Z dang $'
import time
from netlogger.parsers.base import BaseParser, getGuid, parseDate
ks = None
try:
    from netlogger.parsers.modules import ks
except ImportError:
    pass

from xml.parsers.expat import ExpatError
try:
    from xml.etree.cElementTree import XML
except:
    try:
        from xml.etree.ElementTree import XML
    except:
        from elementtree.ElementTree import XML

PEGASUS_NS = 'http://pegasus.isi.edu/schema/invocation'
MAIN_JOB_STATUS_XPATH = '{%(pns)s}mainjob/{%(pns)s}status/{%(pns)s}regular' % {'pns': PEGASUS_NS}
_ns = lambda x: '{' + PEGASUS_NS + '}' + x
_xp = lambda comp: ('/').join(map(_ns, comp))

class Parser(BaseParser):
    """Parse the Kickstart job wrapper output.
    See also: http://pegasus.isi.edu/

    Parameters:
        - one_event {yes,no,no*}: If 'yes', generate one event per kickstart invocation 
                                  record, otherwise generate a start/end event pair.
       - use_c {yes,no,no*}: Use the *experimental* C parser instead. This requires that
                             you compiled the parser with "python setup.py swig".

    """

    def __init__(self, f, one_event=False, use_c=False, **kwargs):
        """ Construct and initialize class vars. """
        BaseParser.__init__(self, f, fullname=__name__, **kwargs)
        self._one_event = one_event or use_c
        self._xml_began = False
        if use_c:
            self.input = ''
            self.process = self._c_process
        else:
            self.input = []
            self.events = []
            self.root = None
            self.guid = None
        return

    def process(self, line):
        """Process a line. 

        When a complete invocation document has been read, process it.
        Otherwise return an empty list.
        Skip non-xml prologue.
        """
        if self._xml_began:
            self.input.append(line)
        else:
            p = line.find('<?xml ')
            if p >= 0:
                self.input.append(line[p:])
                self._xml_began = True
            else:
                return ()
        if line.find('</invocation>') == -1:
            return ()
        try:
            self.root = XML(('').join(self.input))
        except ExpatError, experr:
            self.input = []
            raise ValueError('expat error: %s' % experr)

        self.input, self.events = [], []
        return self._process_root()

    def _c_process(self, line):
        self.input += line
        if line.find('</invocation>') == -1:
            return ()
        else:
            event = ks.parseBuffer(self.input)
            self.input = ''
            if event[(-2)] == ' ':
                return [ s + '\n' for s in event.split('\n')[:-1] ]
            return (event,)

    def _process_root(self):
        """ Process the entire invocation doc parsed and rooted at
        self.root."""
        qname = self.root.tag.split('}')
        if len(qname) != 2 or qname[0][1:] != PEGASUS_NS or qname[1] != 'invocation':
            raise ValueError('Invalid pegasus invocation document')
        if self._one_event:
            invoke = {'ts': self.root.get('start')}
        else:
            invoke = {'ts': parseDate(self.root.get('start')), 'guid': getGuid(repr(time.time()), *self.root.attrib.values())}
        attrs = (
         ('hostname', 'host'), ('user', 'user'),
         ('transformation', 'transformation'), ('wf-label', 'workflow.id'))
        self._populate_event(invoke, self.root, attrs)
        usage = self.root.find(_xp(('mainjob', 'usage')))
        self._populate_event(invoke, usage, (('nsignals', 'nsignals'), ))
        duration = float(self.root.get('duration'))
        mainjob_status = int(self.root.find(MAIN_JOB_STATUS_XPATH).get('exitcode'))
        cwd = self.root.find(_ns('cwd'))
        if cwd:
            invoke['cwd'] = cwd.text
        if mainjob_status != 0:
            environment = self.root.find(_ns('environment'))
            envString = '-env-' + ('::').join([ node.get('key') + ':' + node.text for node in environment ])
            resource = self.root.find(_ns('resource'))
            if resource:
                rstring = ('::').join([ n.get('id') + ':' + n.tag + ':' + n.text for n in resource.getchildren() ])
                envString += '-limits-' + rstring
                invoke['text=longvars'] = envString
        argvector = self.root.find(_xp(('mainjob', 'argument-vector')))
        argstr = (' ').join([ k.text for k in argvector.getchildren() ])
        invoke['arguments'] = argstr
        self.events.append(invoke)
        if self._one_event:
            invoke['event'] = 'pegasus.invocation'
            invoke['duration'] = duration
            invoke['status'] = mainjob_status
        else:
            invoke['event'] = 'pegasus.invocation.start'
            invoke_end = {'event': 'pegasus.invocation.end', 
               'ts': invoke['ts'] + duration, 
               'guid': invoke['guid'], 
               'status': mainjob_status}
            self.events.append(invoke_end)
        for statcall in self.root.findall(_ns('statcall')):
            errnum = int(statcall.get('error'))
            if errnum != 0:
                filename = statcall.find(_ns('file')).get('name')
                statinfo = statcall.find(_ns('statinfo'))
                if statinfo is None:
                    statinfo = {'user': 'unknown', 'group': 'unknown'}
                _e = {'event': 'pegasus.invocation.stat.error', 'ts': invoke['ts'], 
                   'file': filename, 
                   'user': statinfo.get('user'), 
                   'group': statinfo.get('group'), 
                   'status': errnum}
                if invoke.has_key('guid'):
                    _e['guid'] = invoke['guid']
                self.events.append(_e)

        return self.events

    def _populate_event(self, event, elem, attrs):
        """ Ultility method for populating the given event with
        attributes from the given element, if those attributes exist
        within that element."""
        if elem is not None:
            for (attr, new_name) in attrs:
                if elem.attrib.has_key(attr):
                    event[new_name] = elem.get(attr)

        return