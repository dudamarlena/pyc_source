# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/coils/logic/workflow/actions/mail/unsubscribe.py
# Compiled at: 2012-10-12 07:02:39
from coils.core.logic import ActionCommand
from coils.core import *

class UnsubscribeAction(ActionCommand):
    __domain__ = 'action'
    __operation__ = 'mail-unsubscribe'
    __aliases__ = ['unsubscribeMailAction', 'unsubscribeMail']

    def __init__(self):
        ActionCommand.__init__(self)

    @property
    def assignments(self):
        return self.state[self.uuid].get('idList')

    def load_defaults(self):
        sd = ServerDefaultsManager()
        self.suppression_attribute = sd.default_as_dict('SMTPServer').get('SuppressEMailAttribute', None)
        if self.suppression_attribute is None:
            self.log_message('No email suppression attribute configured', category='info')
        else:
            self.log_message(('Email suppression attribute is "{0}"').format(self.suppression_attribute), category='info')
        return

    def read_assignment_ids(self):
        assignments = []
        for entry in self._rfile.xreadlines():
            components = [ x.strip() for x in entry.split('@') ]
            if len(components) == 2:
                if components[1] == self._ctx.cluster_id:
                    if components[0].isdigit():
                        assignments.append(int(components[0]))

        return assignments

    def do_action(self):
        self.load_defaults()
        if self.suppression_attribute is None:
            self.log_message('No e-mail supression attribute configured.', category='warn')
            return
        else:
            assignments = self.read_assignment_ids()
            self.log_message(('Processing {0} unsubscribe requests.').format(len(assignments)), category='info')
            assignments = self._ctx.run_command('collection::get-assignment', ids=assignments)
            counter = 0
            for (k, v) in assignments.iteritems():
                counter += 1
                if isinstance(v[1], Contact):
                    contact = v[1]
                    text = contact.get_company_value_text(self.suppression_attribute)
                    if text is None or text.strip().lower() not in ('no', 'false'):
                        self._ctx.run_command('contact::set', object=contact, values={'_COMPANYVALUES': [
                                            {'attribute': self.suppression_attribute, 'value': 'no'}]})
                        self.log_message(('ContactId#{0} <{1}> bulk-email disabled by request').format(contact.object_id, contact.get_display_name()), category='info')
                    else:
                        self.log_message(('ContactId#{0} <{1}> bulk-email already disabled.').format(contact.object_id, contact.get_display_name()), category='info')
                else:
                    self.log_message(('objectId#{0} is not a Contact entity [{1}]').format(k, v[1]), category='info')

            if counter == 0:
                self.log_message('No assignments from input could be resolved', category='info')
            else:
                self.log_message(('{0} assignments from input processed.').format(counter), category='info')
            return

    def parse_action_parameters(self):
        pass

    def do_epilogue(self):
        pass