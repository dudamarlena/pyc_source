# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/coils/logic/contact/get_contact_as_vcard.py
# Compiled at: 2012-10-12 07:02:39
from sqlalchemy import *
from coils.core import *
from coils.core.logic import GetCommand
from coils.foundation import Project, Appointment, Contact, Enterprise
from coils.core.vcard import Render
from utility import read_cached_vcard, cache_vcard

class GetContactAsVCard(GetCommand):
    __domain__ = 'contact'
    __operation__ = 'get-as-vcard'
    mode = None

    def __init__(self):
        GetCommand.__init__(self)

    def parse_parameters(self, **params):
        self.objects = None
        self.object_ids = None
        if 'object' in params:
            self.mode = 1
            self.objects = [params['object']]
        elif 'objects' in params:
            self.mode = 2
            self.objects = params['objects']
        elif 'id' in params:
            self.mode = 1
            self.object_ids = [params['id']]
        elif 'ids' in params:
            self.mode = 2
            self.object_ids = params['ids']
        return

    def run(self):
        if self.objects is None and self.object_ids is not None:
            try:
                data = self._ctx.run_command('contact::get', ids=self.object_ids, access_check=self.access_check)
            except Exception, e:
                self.log.exception('exception retrieving contact')
                self._result = None
                return
            else:
                self.objects = data
        if self.objects is None:
            self._result = None
        else:
            self._result = []
            for contact in self.objects:
                vcf = read_cached_vcard(contact.object_id, contact.version)
                if vcf is None:
                    vcf = Render.render(contact, self._ctx)
                    if vcf is not None:
                        cache_vcard(contact.object_id, contact.version, vcf)
                if vcf is not None:
                    self._result.append(vcf)

            if self.mode == 1:
                if len(self._result) > 0:
                    self._result = self._result[0]
                else:
                    self._result = None
        return