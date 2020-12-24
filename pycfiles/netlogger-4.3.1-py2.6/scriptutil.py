# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-x86_64/egg/netlogger/amqp/scriptutil.py
# Compiled at: 2010-09-14 08:19:10
"""
Utility functions, etc. for scripts that deal with AMQP
"""
import optparse
from netlogger.nllog import OptionParser
from netlogger.amqp import connection
from netlogger import util

class AMQPOptionParser(OptionParser):
    """Subclass of OptionParser that adds AMQP options
    for nl_load and nl_parse.
    """
    OPT = {'user': 'user name', 
       'pw': 'password', 
       'vhost': 'virtual host', 
       'insist': 'no redirect', 
       'exchange': 'exchange name', 
       'exchange_type': 'direct, fanout, or topic', 
       'route': 'routing key, @event to use event', 
       'queue': 'queue name'}
    BOOL_OPT = {'durable': 'save messages to disk', 
       'auto_delete': 'delete queues/exchanges when done'}
    OPT.update(BOOL_OPT)
    OPT_HELP = (', ').join([ '%s (%s)' % (k, OPT[k]) for k in sorted(OPT.keys())
                           ])

    def _add_options(self):
        """Override/extend base class method.
        """
        group = optparse.OptionGroup(self, 'AMQP-specific options')
        group.add_option('-a', '--amqp-host', dest='amqp_host', metavar='HOST', default=None, help='Connect to AMQP server at HOST ' + '(default=%s)' % connection._D['host'])
        group.add_option('-A', '--amqp_option', action='append', default=[], dest='amqp_option', metavar='name=val|:file', help="AMQP options; repeatable. Known options: %s. May also be of the form ':<filename>', e.g. ':/tmp/passwd', which reads the options from a file with one name=value pair per line. " % self.OPT_HELP)
        self.add_option_group(group)
        OptionParser._add_options(self)
        return

    def get_amqp_options(self, options):
        """Process the AMQP option values.

        Will cause a parser error() if an option is missing or
        not recognized.

        Parameters:

          - options (OptionParser.Options): All program options.

        Returns: (dict) name/value pairs for AMQP options.
        """
        vals = {}
        for o in options.amqp_option:
            if o[0] == ':':
                filename = o[1:]
                if not filename:
                    self.error('empty AMQP option filename')
                try:
                    fileobj = open(filename, 'r')
                except IOError, err:
                    self.error('opening AMQP option-file: %s' % err)

                for line in fileobj:
                    o = line.strip()
                    if o == '' or o.startswith('#'):
                        continue
                    try:
                        (k, v) = self.process_kvp(o)
                    except ValueError, err:
                        self.error('Bad AMQP option: %s' % err)

                    vals[k] = v

            else:
                try:
                    (k, v) = self.process_kvp(o)
                except ValueError, err:
                    self.error('Bad AMQP option: %s' % err)

                vals[k] = v

        return vals

    def process_kvp(self, opt):
        return util.process_kvp(opt, all=self.OPT, _bool=self.BOOL_OPT)