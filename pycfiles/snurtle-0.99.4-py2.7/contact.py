# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/snurtle/bundles/contact.py
# Compiled at: 2012-08-06 20:13:05
from snurtle.cmd2 import options, make_option
from clibundle import CLIBundle
LIST_CONTACT_TEMPLATE = "<%\n  flags = ''\n  if report['isaccount']: flags += 'a'\n  if report['isprivate']: flags += 'p'\n  flags = '{:^6}'.format( flags )\n  \n  if report['fileas']:\n    name = report['fileas']\n  elif report['displayname']:\n    name = report['displayname']\n  else: name = '{0}, {1}'.format(report['lastname'], report['firstname'])\n  name = '{:<35}'.format(name)\n  \n  objectid = '{:<12}'.format(report['objectid'])\n  \n%>${objectid} ${name} ${flags}"
CONTACT_TEMPLATE = '    OGo#${report[\'objectid\']} login: "${report[\'login\']}"  version: ${report[\'version\']} sensitivity: ${report[\'sensitivity\']}\n    isPrivate: ${report[\'isprivate\']} isAccount: ${report[\'isaccount\']} ownerId: ${report[\'ownerobjectid\']}\n    =================================================================\n    firstName:      "${report[\'firstname\']}" \n    lastName:       "${report[\'lastname\']}" \n    displayName:    "${report[\'displayname\']}"\n    birthName:      "${report[\'birthname\']}"\n    birthPlace:     "${report[\'birthplace\']}"\n    citizenship:    "${report[\'citizenship\']}"\n    familyStatus:   "${report[\'familystatus\']}"\n    fileAs:         "${report[\'fileas\']}"\n    gender:         "${report[\'gender\']}" \n    salutation:     "${report[\'salutation\']}"\n    assistantsName: "${report[\'assistantname\']}"\n    managersName:   "${report[\'managersname\']}"\n    keywords:       "${report[\'keywords\']}"\n    asoc.Categories:"${report[\'associatedcategories\']}"\n    asoc.Companies: "${report[\'associatedcompany\']}"\n    asoc.Contacts:  "${report[\'associatedcontacts\']}"\n    birthDate:      "${report[\'birthdate\']}" \n    deathDate:      "${report[\'deathdate\']}"\n    degree:         "${report[\'degree\']}"\n    department:     "${report[\'department\']}"\n    occupation:     "${report[\'occupation\']}"\n    office:         "${report[\'office\']}"\n    url:            <${report[\'url\']}>\n    %for cv in report[\'_companyvalues\']:\n    ${\'{0}:\'.format(cv[\'attribute\']).ljust(16)} "${str(cv[\'value\']).strip()}" [type: "${cv[\'type\']}" uid: "${cv[\'uid\']}"]\n    %endfor\n    %for address in report[\'_addresses\']:\n    --address [objectId#${address[\'objectid\']} type:${address[\'type\']}]--\n    name1:      ${address[\'name1\']}\n    name2:      ${address[\'name2\']}\n    name3:      ${address[\'name3\']}\n    street:     ${address[\'street\']}\n    locality:   ${address[\'city\']}\n    district:   ${address[\'district\']}\n    province:   ${address[\'state\']}\n    country:    ${address[\'country\']}\n    postalCode: ${address[\'zip\']}\n    %endfor\n    %for phone in report[\'_phones\']:\n    --telephone [objectId#${phone[\'objectid\']} type:${phone[\'type\']}]--\n    number:     ${phone[\'number\']}\n    info:       ${phone[\'info\']}\n    %endfor\n    --enterprises--\n    %if len(report[\'_enterprises\']) == 0:\n      Contact is assigned to no enterprises.\n    %else:\n      %for assignment in report[\'_enterprises\']:\n      ${assignment[\'targetobjectid\']}\n      %endfor\n    %endif\n    --projects--\n    %if len(report[\'_projects\']) == 0:\n      Contact is assigned to no projects.\n    %else:\n      %for assignment in report[\'_projects\']:\n      ${assignment[\'targetobjectid\']}\n      %endfor\n    %endif    \n\n  '

class ContactCLIBundle(CLIBundle):

    @options([make_option('--favorite', action='store_true', help='List favorite contacts.')])
    def do_list_contacts(self, arg, opts=None):
        if opts.favorite:
            callid = self.server.get_favorites(entity_name='Contact', detail_level=0, callback=self.callback, feedback=self.pfeedback)
            response = self.get_response(callid)
        if response:
            self.set_result(response, template=LIST_CONTACT_TEMPLATE)

    @options([make_option('--objectid', type='int', help='objectId [Contact] to display.')])
    def do_get_contact(self, arg, opts=None):
        response = self._get_entity(opts.objectid, expected_type='Contact', detail_level=65535)
        if response:
            self.set_result(response, template=CONTACT_TEMPLATE)

    @options([])
    def do_list_accounts(self, arg, opts=None):
        callid = self.server.search_for_objects(entity='Contact', criteria=[{'key': 'isAccount', 'value': 1}], detail=0, callback=self.callback)
        response = self.get_response(callid)
        if response:
            self.set_result(response.payload, template=LIST_CONTACT_TEMPLATE)

    @options([make_option('--firstname', dest='firstname', type='string', help='First name of the contact.'),
     make_option('--lastname', dest='lastname', type='string', help=''),
     make_option('--displayname', dest='displayname', type='string', default='x', help=''),
     make_option('--fileas', dest='fileas', type='string', default='x', help='Attribute name'),
     make_option('--middlename', dest='middlename', type='string', default='x', help='ObjectProperty value'),
     make_option('--private', dest='private', action='store_true', help='ObjectProperty value')])
    def do_create_contact(self, arg, opts=None):
        """Set, or create, the specified object property."""
        e = {'entityName': 'Contact', 'objectId': 0, 
           'firstName': opts.firstname, 
           'lastName': opts.lastname, 
           'displayName': opts.displayname, 
           'fileAs': opts.fileas, 
           'middleName': opts.middlename}
        if opts.private:
            e['isPrivate'] = 1
        callid = self.server.put_object(e, callback=self.callback)
        response = self.get_response(callid)
        if response:
            self.set_result(response, template=CONTACT_TEMPLATE)
        else:
            self.set_result('No response', error=True)