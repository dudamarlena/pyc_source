# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/snurtle/bundles/enterprise.py
# Compiled at: 2012-08-03 08:35:35
from snurtle.cmd2 import options, make_option
from clibundle import CLIBundle
ENTERPRISE_TEMPLATE = '\n  objectId#${report[\'objectid\']} version: ${report[\'version\']} sensitivity: ${report[\'sensitivity\']}\n    isPrivate: ${report[\'isprivate\']} isCustomer: ${report[\'iscustomer\']} ownerId: ${report[\'ownerobjectid\']}\n    =================================================================\n    name:           "${report[\'name\']}" \n    bank:           "${report[\'bank\']}" \n    email:          "${report[\'bankcode\']}"\n    url:            "${report[\'url\']}"\n    fileAs:         "${report[\'fileas\']}"\n    keywords:       "${report[\'keywords\']}"\n    asoc.Categories:"${report[\'associatedcategories\']}"\n    asoc.Companies: "${report[\'associatedcompany\']}"\n    asoc.Contacts:  "${report[\'associatedcontacts\']}"\n    %for cv in report[\'_companyvalues\']:\n    ${\'{0}:\'.format(cv[\'attribute\']).ljust(16)} "${str(cv[\'value\']).strip()}" [type: "${cv[\'type\']}" uid: "${cv[\'uid\']}"]\n    %endfor\n    %for address in report[\'_addresses\']:\n    --address [objectId#${address[\'objectid\']} type:${address[\'type\']}]--\n    name1:      ${address[\'name1\']}\n    name2:      ${address[\'name2\']}\n    name3:      ${address[\'name3\']}\n    street:     ${address[\'street\']}\n    locality:   ${address[\'city\']}\n    district:   ${address[\'district\']}\n    province:   ${address[\'state\']}\n    country:    ${address[\'country\']}\n    postalCode: ${address[\'zip\']}\n    %endfor\n    %for phone in report[\'_phones\']:\n    --telephone [objectId#${phone[\'objectid\']} type:${phone[\'type\']}]--\n    number:     ${phone[\'number\']}\n    info:       ${phone[\'info\']}\n    %endfor\n    --contacts--\n    %if len(report[\'_contacts\']) == 0:\n      No contacts are assigned to the enterprise.\n    %else:\n      %for assignment in report[\'_contacts\']:\n      ${assignment[\'targetobjectid\']}\n      %endfor\n    %endif\n    --projects--\n    %if len(report[\'_projects\']) == 0:\n      Contact is assigned to no projects.\n    %else:\n      %for assignment in report[\'_projects\']:\n      ${assignment[\'targetobjectid\']}\n      %endfor\n    %endif   \n  '

class EnterpriseCLIBundle(CLIBundle):

    @options([make_option('--favorite', action='store_true', help='List favorite enterprises.')])
    def do_list_enterprises(self, arg, opts=None):
        if opts.favorite:
            callid = self.server.get_favorites(entity_name='Enterprise', detail_level=0, callback=self.callback, feedback=self.pfeedback)
        response = self.get_response(callid)
        if response:
            self.set_result(response)

    @options([make_option('--objectid', type='int', help='objectId [Enterprise] to display.')])
    def do_get_enterprise(self, arg, opts=None):
        response = self._get_entity(opts.objectid, expected_type='Enterprise', detail_level=65535)
        if response:
            self.set_result(response, template=ENTERPRISE_TEMPLATE)