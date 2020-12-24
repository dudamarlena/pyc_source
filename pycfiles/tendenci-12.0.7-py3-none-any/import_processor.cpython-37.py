# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/jennyq/.pyenv/versions/venv_t12/lib/python3.7/site-packages/tendenci/apps/corporate_memberships/import_processor.py
# Compiled at: 2020-02-26 14:47:57
# Size of source mod 2**32: 22002 bytes
from decimal import Decimal
from datetime import datetime, date
import dateutil.parser as dparser
import pytz
from django.core import exceptions
from django.contrib.auth.models import User
from tendenci.apps.site_settings.utils import get_setting
from tendenci.apps.corporate_memberships.models import CorpMembership, CorpProfile, CorpMembershipRep, CorporateMembershipType
from tendenci.apps.corporate_memberships.utils import update_authorized_domains
from tendenci.apps.memberships.models import MembershipDefault
from tendenci.apps.profiles.models import Profile
from tendenci.apps.entities.models import Entity

class CorpMembershipImportProcessor(object):
    __doc__ = '\n    Check and process (insert/update) a corporate membership.\n    '

    def __init__(self, request_user, mimport, dry_run=True, **kwargs):
        """
        :param mimport: a instance of MembershipImport
        :param dry_run: if True, do everything except updating the database.
        """
        self.key = mimport.key
        self.request_user = request_user
        self.mimport = mimport
        self.dry_run = dry_run
        self.summary_d = self.init_summary()
        self.corp_profile_fields = dict([(field.name, field) for field in CorpProfile._meta.fields if field.get_internal_type() != 'AutoField' if field.name not in ('guid', )])
        self.corp_membership_fields = dict([(field.name, field) for field in CorpMembership._meta.fields if field.get_internal_type() != 'AutoField' if field.name not in ('user',
                                                                                                                                                                           'guid',
                                                                                                                                                                           'corp_profile')])
        self.private_settings = self.set_default_private_settings()
        self.t4_timezone_map = {'AST':'Canada/Atlantic',  'EST':'US/Eastern', 
         'CST':'US/Central', 
         'MST':'US/Mountain', 
         'AKST':'US/Alaska', 
         'PST':'US/Pacific', 
         'GMT':'UTC'}

    def init_summary(self):
        return {'insert':0, 
         'update':0, 
         'update_insert':0, 
         'invalid':0}

    def set_default_private_settings(self):
        memberprotection = get_setting('module', 'memberships', 'memberprotection')
        d = {'allow_anonymous_view':False,  'allow_user_view':False, 
         'allow_member_view':False, 
         'allow_user_edit':False, 
         'allow_member_edit':False}
        if memberprotection == 'public':
            d['allow_anonymous_view'] = True
        if memberprotection == 'all-members':
            d['allow_user_view'] = True
        if memberprotection == 'member-type':
            d['allow_member_view'] = True
        return d

    def validate_fields(self, cmemb_data, key):
        """
        1. Check if we have enough data to process for this row.
        2. Check if this is an archived corporate membership.
        """
        error_msg = []
        if key == 'name':
            if not cmemb_data['company_name']:
                error_msg.append("Missing key 'company_name'.")
        return ' '.join(error_msg)

    def process_corp_membership(self, cmemb_data, **kwargs):
        """
        Check if it's insert or update. If dry_run is False,
        do the import to the corpmembership.

        :param cmemb_data: a dictionary that includes the info
        of a corp_membership
        """
        self.cmemb_data = cmemb_data
        if 'id' not in self.cmemb_data:
            if 'id' in self.corp_membership_fields:
                del self.corp_membership_fields['id']
        self.cmemb_data['name'] = self.cmemb_data['company_name']
        del self.cmemb_data['company_name']
        self.field_names = cmemb_data
        corp_memb_display = {}
        corp_memb_display['error'] = ''
        corp_memb_display['user'] = None
        status_detail = self.cmemb_data.get('status_detail', 'active')
        if status_detail == 'archived':
            status_detail = 'archive'
        if status_detail not in CorpMembership.VALID_STATUS_DETAIL:
            status_detail = 'active'
        self.cmemb_data['status_detail'] = status_detail
        expiration_dt = self.cmemb_data.get('expiration_dt', None)
        if expiration_dt:
            expiration_dt = dparser.parse(expiration_dt)
        error_msg = self.validate_fields(self.cmemb_data, self.key)
        if error_msg:
            corp_memb_display['error'] = error_msg
            corp_memb_display['action'] = 'skip'
            if not self.dry_run:
                self.summary_d['invalid'] += 1
        else:
            corp_profile, = CorpProfile.objects.filter(name=(self.cmemb_data['name']))[:1] or [None]
            if corp_profile:
                corp_membs = CorpMembership.objects.filter(corp_profile=corp_profile,
                  status_detail=status_detail)
                if status_detail == 'archive':
                    if expiration_dt:
                        corp_membs = corp_membs.filter(expiration_dt__year=(expiration_dt.year),
                          expiration_dt__month=(expiration_dt.month),
                          expiration_dt__day=(expiration_dt.day))
                corp_memb, = corp_membs.order_by('-id')[:1] or [None]
            else:
                corp_memb = None
            if corp_profile:
                if corp_memb:
                    corp_memb_display['action'] = 'update'
                    corp_memb_display['corp_profile_action'] = 'update'
                    corp_memb_display['corp_memb_action'] = 'update'
                else:
                    corp_memb_display['action'] = 'mixed'
                    corp_memb_display['corp_profile_action'] = 'update'
                    corp_memb_display['corp_memb_action'] = 'insert'
            else:
                corp_memb_display['action'] = 'insert'
                corp_memb_display['corp_profile_action'] = 'insert'
                corp_memb_display['corp_memb_action'] = 'insert'
            if not self.dry_run:
                if corp_memb_display['action'] == 'insert':
                    self.summary_d['insert'] += 1
                else:
                    if corp_memb_display['action'] == 'update':
                        self.summary_d['update'] += 1
                    else:
                        self.summary_d['update_insert'] += 1
                self.do_import_corp_membership(corp_profile, corp_memb, corp_memb_display)
                if 'authorized_domains' in self.field_names:
                    update_authorized_domains(corp_profile, self.cmemb_data['authorized_domains'])
                if 'dues_rep' in self.field_names:
                    self.update_dues_reps(corp_profile, self.cmemb_data['dues_rep'])
                return
            corp_memb_display.update({'company_name':self.cmemb_data.get('name', ''), 
             'email':self.cmemb_data.get('email', ''), 
             'address':self.cmemb_data.get('address', ''), 
             'address2':self.cmemb_data.get('address2', ''), 
             'city':self.cmemb_data.get('city', ''), 
             'state':self.cmemb_data.get('state', ''), 
             'zip':self.cmemb_data.get('zip', ''), 
             'status_detail':self.cmemb_data.get('status_detail', '')})
            return corp_memb_display

    def update_dues_reps(self, corp_profile, dues_reps):
        """
        Update the dues reps for this corp_profile.
        """
        dues_reps = dues_reps.split(',')
        dues_reps_list = [name.strip() for name in dues_reps]
        dues_reps_users_list = []
        for username in dues_reps_list:
            u, = User.objects.filter(username=username)[:1] or [None]
            if u:
                dues_reps_users_list.append(u)

        if dues_reps_users_list:
            CorpMembershipRep.objects.filter(corp_profile=corp_profile, is_dues_rep=True).delete()
            for u in dues_reps_users_list:
                dues_rep = CorpMembershipRep(corp_profile=corp_profile,
                  user=u,
                  is_dues_rep=True)
                dues_rep.save()

    def do_import_corp_membership(self, corp_profile, corp_memb, action_info):
        """
        Database import here - insert or update
        """
        if not corp_profile:
            corp_profile = CorpProfile()
        else:
            self.assign_import_values_from_dict(corp_profile, action_info['corp_profile_action'])
            if not corp_profile.status is None:
                if corp_profile.status == '' or self.cmemb_data.get('status', '') == '':
                    corp_profile.status = True
                if not corp_profile.status_detail:
                    corp_profile.status_detail = 'active'
            else:
                corp_profile.status_detail = corp_profile.status_detail.lower()
            if not corp_profile.creator:
                corp_profile.creator = self.request_user
                corp_profile.creator_username = self.request_user.username
            if not corp_profile.owner:
                corp_profile.owner = self.request_user
                corp_profile.owner_username = self.request_user.username
            else:
                corp_profile.save()
                if not corp_memb:
                    corp_memb = CorpMembership(corp_profile=corp_profile,
                      creator=(self.request_user),
                      creator_username=(self.request_user.username),
                      owner=(self.request_user),
                      owner_username=(self.request_user.username))
                else:
                    self.assign_import_values_from_dict(corp_memb, action_info['corp_memb_action'])
                    if corp_memb.status is None or corp_memb.status == '' or self.cmemb_data.get('status', '') == '':
                        corp_memb.status = True
                    if not corp_memb.status_detail:
                        corp_memb.status_detail = 'active'
                    else:
                        corp_memb.status_detail = corp_memb.status_detail.lower()
                    if (corp_memb.approved or corp_memb).status:
                        if corp_memb.status_detail == 'active':
                            corp_memb.approved = True
                    corp_memb.corporate_membership_type = hasattr(corp_memb, 'corporate_membership_type') and corp_memb.corporate_membership_type or CorporateMembershipType.objects.all().order_by('id')[0]
                if hasattr(corp_memb, 'join_dt') and corp_memb.join_dt or corp_memb.status:
                    if corp_memb.status_detail == 'active':
                        corp_memb.join_dt = datetime.now()
                if not (hasattr(corp_memb, 'expiration_dt') and corp_memb.expiration_dt):
                    if corp_memb.corporate_membership_type:
                        expiration_dt = corp_memb.corporate_membership_type.get_expiration_dt(join_dt=(corp_memb.join_dt))
                        setattr(corp_memb, 'expiration_dt', expiration_dt)
            if not corp_memb.creator:
                corp_memb.creator = self.request_user
                corp_memb.creator_username = self.request_user.username
            corp_memb.owner = corp_memb.owner or self.request_user
            corp_memb.owner_username = self.request_user.username
        corp_memb.save()
        if self.mimport.bind_members:
            self.bind_members_to_corp_membership(corp_memb)

    def bind_members_to_corp_membership(self, corp_memb):
        corp_profile = corp_memb.corp_profile
        company_name = corp_profile.name
        user_ids = Profile.objects.filter(company__iexact=company_name).values_list('user__id',
          flat=True)
        if user_ids:
            memberships = MembershipDefault.objects.filter(user__id__in=user_ids).filter(status=True).exclude(status_detail='archive')
            for membership in memberships:
                if not membership.corp_profile_id:
                    membership.corp_profile_id = corp_profile.id
                    membership.corporate_membership_id = corp_memb.id
                    membership.expire_dt = corp_memb.expiration_dt
                    membership.save()

    def is_active(self, corp_memb):
        return all([
         corp_memb.status,
         corp_memb.status_detail == 'active',
         not corp_memb.expiration_dt or corp_memb.expiration_dt > datetime.now()])

    def assign_import_values_from_dict(self, instance, action):
        """
        Assign the import value from a dictionary object
        - self.cmemb_data.
        """
        if instance.__class__ == CorpProfile:
            assign_to_fields = self.corp_profile_fields
        else:
            assign_to_fields = self.corp_membership_fields
        for field_name in self.field_names:
            if field_name in assign_to_fields and any([
             action == 'insert',
             self.mimport.override,
             not hasattr(instance, field_name) or getattr(instance, field_name) == '' or getattr(instance, field_name) is None]):
                value = self.cmemb_data[field_name]
                value = self.clean_data(value, assign_to_fields[field_name])
                setattr(instance, field_name, value)

        for field_name in assign_to_fields:
            if field_name not in self.field_names and action == 'insert' and field_name not in self.private_settings and field_name not in ('creator',
                                                                                                                                            'owner',
                                                                                                                                            'creator_username',
                                                                                                                                            'owner_username'):
                value = self.get_default_value(assign_to_fields[field_name])
                if value is None:
                    setattr(instance, field_name, value)

        if action == 'insert':
            for field_name in assign_to_fields:
                if field_name not in self.field_names:
                    value = self.get_default_value(assign_to_fields[field_name])
                    if value is not None:
                        setattr(instance, field_name, value)

    def get_default_value(self, field):
        if field.null:
            return
        if field.has_default():
            return field.default
        field_type = field.get_internal_type()
        if field_type == 'BooleanField':
            return False
        if field_type == 'DateField':
            return date
        if field_type == 'DateTimeField':
            return datetime.now()
        if field_type == 'DecimalField':
            return Decimal(0)
        if field_type in ('IntegerField', 'PositiveIntegerField'):
            return 0
        if field_type == 'FloatField':
            return 0
        if field_type == 'ForeignKey':
            if field.name not in ('creator', 'owner'):
                try:
                    model = field.remote_field.parent_model()
                except AttributeError:
                    model = field.remote_field.model

                value, = model.objects.all()[:1] or [None]
                return value
            return
        return ''

    def clean_data--- This code section failed: ---

 L. 425         0  LOAD_FAST                'field'
                2  LOAD_METHOD              get_internal_type
                4  CALL_METHOD_0         0  '0 positional arguments'
                6  STORE_FAST               'field_type'

 L. 426         8  LOAD_FAST                'field_type'
               10  LOAD_CONST               ('CharField', 'EmailField', 'URLField', 'SlugField')
               12  COMPARE_OP               in
               14  POP_JUMP_IF_FALSE   156  'to 156'

 L. 428        16  LOAD_FAST                'value'
               18  POP_JUMP_IF_TRUE     24  'to 24'

 L. 429        20  LOAD_STR                 ''
               22  STORE_FAST               'value'
             24_0  COME_FROM            18  '18'

 L. 430        24  LOAD_GLOBAL              len
               26  LOAD_FAST                'value'
               28  CALL_FUNCTION_1       1  '1 positional argument'
               30  LOAD_FAST                'field'
               32  LOAD_ATTR                max_length
               34  COMPARE_OP               >
               36  POP_JUMP_IF_FALSE    52  'to 52'

 L. 432        38  LOAD_FAST                'value'
               40  LOAD_CONST               None
               42  LOAD_FAST                'field'
               44  LOAD_ATTR                max_length
               46  BUILD_SLICE_2         2 
               48  BINARY_SUBSCR    
               50  STORE_FAST               'value'
             52_0  COME_FROM            36  '36'

 L. 433        52  LOAD_FAST                'field'
               54  LOAD_ATTR                name
               56  LOAD_STR                 'time_zone'
               58  COMPARE_OP               ==
               60  POP_JUMP_IF_FALSE    92  'to 92'

 L. 434        62  LOAD_FAST                'value'
               64  LOAD_GLOBAL              pytz
               66  LOAD_ATTR                all_timezones
               68  COMPARE_OP               not-in
               70  POP_JUMP_IF_FALSE    92  'to 92'

 L. 435        72  LOAD_FAST                'value'
               74  LOAD_FAST                'self'
               76  LOAD_ATTR                t4_timezone_map
               78  COMPARE_OP               in
               80  POP_JUMP_IF_FALSE    92  'to 92'

 L. 436        82  LOAD_FAST                'self'
               84  LOAD_ATTR                t4_timezone_map
               86  LOAD_FAST                'value'
               88  BINARY_SUBSCR    
               90  STORE_FAST               'value'
             92_0  COME_FROM            80  '80'
             92_1  COME_FROM            70  '70'
             92_2  COME_FROM            60  '60'

 L. 437        92  SETUP_EXCEPT        108  'to 108'

 L. 438        94  LOAD_FAST                'field'
               96  LOAD_METHOD              to_python
               98  LOAD_FAST                'value'
              100  CALL_METHOD_1         1  '1 positional argument'
              102  STORE_FAST               'value'
              104  POP_BLOCK        
              106  JUMP_FORWARD        968  'to 968'
            108_0  COME_FROM_EXCEPT     92  '92'

 L. 439       108  DUP_TOP          
              110  LOAD_GLOBAL              exceptions
              112  LOAD_ATTR                ValidationError
              114  COMPARE_OP               exception-match
              116  POP_JUMP_IF_FALSE   150  'to 150'
              118  POP_TOP          
              120  POP_TOP          
              122  POP_TOP          

 L. 440       124  LOAD_FAST                'field'
              126  LOAD_METHOD              has_default
              128  CALL_METHOD_0         0  '0 positional arguments'
              130  POP_JUMP_IF_FALSE   142  'to 142'

 L. 441       132  LOAD_FAST                'field'
              134  LOAD_METHOD              get_default
              136  CALL_METHOD_0         0  '0 positional arguments'
              138  STORE_FAST               'value'
              140  JUMP_FORWARD        146  'to 146'
            142_0  COME_FROM           130  '130'

 L. 443       142  LOAD_STR                 ''
              144  STORE_FAST               'value'
            146_0  COME_FROM           140  '140'
              146  POP_EXCEPT       
              148  JUMP_FORWARD        968  'to 968'
            150_0  COME_FROM           116  '116'
              150  END_FINALLY      
          152_154  JUMP_FORWARD        968  'to 968'
            156_0  COME_FROM            14  '14'

 L. 445       156  LOAD_FAST                'field_type'
              158  LOAD_STR                 'BooleanField'
              160  COMPARE_OP               ==
              162  POP_JUMP_IF_FALSE   222  'to 222'

 L. 446       164  LOAD_FAST                'value'
              166  LOAD_STR                 'TRUE'
              168  COMPARE_OP               ==
              170  POP_JUMP_IF_FALSE   176  'to 176'

 L. 447       172  LOAD_CONST               True
              174  STORE_FAST               'value'
            176_0  COME_FROM           170  '170'

 L. 448       176  SETUP_EXCEPT        192  'to 192'

 L. 449       178  LOAD_FAST                'field'
              180  LOAD_METHOD              to_python
              182  LOAD_FAST                'value'
              184  CALL_METHOD_1         1  '1 positional argument'
              186  STORE_FAST               'value'
              188  POP_BLOCK        
              190  JUMP_FORWARD        968  'to 968'
            192_0  COME_FROM_EXCEPT    176  '176'

 L. 450       192  DUP_TOP          
              194  LOAD_GLOBAL              exceptions
              196  LOAD_ATTR                ValidationError
              198  COMPARE_OP               exception-match
              200  POP_JUMP_IF_FALSE   216  'to 216'
              202  POP_TOP          
              204  POP_TOP          
              206  POP_TOP          

 L. 451       208  LOAD_CONST               False
              210  STORE_FAST               'value'
              212  POP_EXCEPT       
              214  JUMP_FORWARD        968  'to 968'
            216_0  COME_FROM           200  '200'
              216  END_FINALLY      
          218_220  JUMP_FORWARD        968  'to 968'
            222_0  COME_FROM           162  '162'

 L. 452       222  LOAD_FAST                'field_type'
              224  LOAD_STR                 'DateField'
              226  COMPARE_OP               ==
          228_230  POP_JUMP_IF_FALSE   310  'to 310'

 L. 453       232  LOAD_FAST                'value'
          234_236  POP_JUMP_IF_FALSE   288  'to 288'

 L. 454       238  LOAD_GLOBAL              dparser
              240  LOAD_METHOD              parse
              242  LOAD_FAST                'value'
              244  CALL_METHOD_1         1  '1 positional argument'
              246  STORE_FAST               'value'

 L. 455       248  SETUP_EXCEPT        264  'to 264'

 L. 456       250  LOAD_FAST                'field'
              252  LOAD_METHOD              to_python
              254  LOAD_FAST                'value'
              256  CALL_METHOD_1         1  '1 positional argument'
              258  STORE_FAST               'value'
              260  POP_BLOCK        
              262  JUMP_FORWARD        288  'to 288'
            264_0  COME_FROM_EXCEPT    248  '248'

 L. 457       264  DUP_TOP          
              266  LOAD_GLOBAL              exceptions
              268  LOAD_ATTR                ValidationError
              270  COMPARE_OP               exception-match
          272_274  POP_JUMP_IF_FALSE   286  'to 286'
              276  POP_TOP          
              278  POP_TOP          
              280  POP_TOP          

 L. 458       282  POP_EXCEPT       
              284  JUMP_FORWARD        288  'to 288'
            286_0  COME_FROM           272  '272'
              286  END_FINALLY      
            288_0  COME_FROM           284  '284'
            288_1  COME_FROM           262  '262'
            288_2  COME_FROM           234  '234'

 L. 460       288  LOAD_FAST                'value'
          290_292  POP_JUMP_IF_TRUE    968  'to 968'

 L. 461       294  LOAD_FAST                'field'
              296  LOAD_ATTR                null
          298_300  POP_JUMP_IF_TRUE    968  'to 968'

 L. 462       302  LOAD_GLOBAL              date
              304  STORE_FAST               'value'
          306_308  JUMP_FORWARD        968  'to 968'
            310_0  COME_FROM           228  '228'

 L. 464       310  LOAD_FAST                'field_type'
              312  LOAD_STR                 'DateTimeField'
              314  COMPARE_OP               ==
          316_318  POP_JUMP_IF_FALSE   416  'to 416'

 L. 465       320  LOAD_FAST                'value'
          322_324  POP_JUMP_IF_FALSE   376  'to 376'

 L. 466       326  LOAD_GLOBAL              dparser
              328  LOAD_METHOD              parse
              330  LOAD_FAST                'value'
              332  CALL_METHOD_1         1  '1 positional argument'
              334  STORE_FAST               'value'

 L. 467       336  SETUP_EXCEPT        352  'to 352'

 L. 468       338  LOAD_FAST                'field'
              340  LOAD_METHOD              to_python
              342  LOAD_FAST                'value'
              344  CALL_METHOD_1         1  '1 positional argument'
              346  STORE_FAST               'value'
              348  POP_BLOCK        
              350  JUMP_FORWARD        376  'to 376'
            352_0  COME_FROM_EXCEPT    336  '336'

 L. 469       352  DUP_TOP          
              354  LOAD_GLOBAL              exceptions
              356  LOAD_ATTR                ValidationError
              358  COMPARE_OP               exception-match
          360_362  POP_JUMP_IF_FALSE   374  'to 374'
              364  POP_TOP          
              366  POP_TOP          
              368  POP_TOP          

 L. 470       370  POP_EXCEPT       
              372  JUMP_FORWARD        376  'to 376'
            374_0  COME_FROM           360  '360'
              374  END_FINALLY      
            376_0  COME_FROM           372  '372'
            376_1  COME_FROM           350  '350'
            376_2  COME_FROM           322  '322'

 L. 472       376  LOAD_FAST                'value'
          378_380  POP_JUMP_IF_TRUE    968  'to 968'

 L. 473       382  LOAD_FAST                'value'
              384  LOAD_STR                 ''
              386  COMPARE_OP               ==
          388_390  POP_JUMP_IF_FALSE   396  'to 396'

 L. 474       392  LOAD_CONST               None
              394  STORE_FAST               'value'
            396_0  COME_FROM           388  '388'

 L. 475       396  LOAD_FAST                'field'
              398  LOAD_ATTR                null
          400_402  POP_JUMP_IF_TRUE    968  'to 968'

 L. 476       404  LOAD_GLOBAL              datetime
              406  LOAD_METHOD              now
              408  CALL_METHOD_0         0  '0 positional arguments'
              410  STORE_FAST               'value'
          412_414  JUMP_FORWARD        968  'to 968'
            416_0  COME_FROM           316  '316'

 L. 477       416  LOAD_FAST                'field_type'
              418  LOAD_STR                 'DecimalField'
              420  COMPARE_OP               ==
          422_424  POP_JUMP_IF_FALSE   478  'to 478'

 L. 478       426  SETUP_EXCEPT        442  'to 442'

 L. 479       428  LOAD_FAST                'field'
              430  LOAD_METHOD              to_python
              432  LOAD_FAST                'value'
              434  CALL_METHOD_1         1  '1 positional argument'
              436  STORE_FAST               'value'
              438  POP_BLOCK        
              440  JUMP_FORWARD        968  'to 968'
            442_0  COME_FROM_EXCEPT    426  '426'

 L. 480       442  DUP_TOP          
              444  LOAD_GLOBAL              exceptions
              446  LOAD_ATTR                ValidationError
              448  COMPARE_OP               exception-match
          450_452  POP_JUMP_IF_FALSE   472  'to 472'
              454  POP_TOP          
              456  POP_TOP          
              458  POP_TOP          

 L. 481       460  LOAD_GLOBAL              Decimal
              462  LOAD_CONST               0
              464  CALL_FUNCTION_1       1  '1 positional argument'
              466  STORE_FAST               'value'
              468  POP_EXCEPT       
              470  JUMP_FORWARD        968  'to 968'
            472_0  COME_FROM           450  '450'
              472  END_FINALLY      
          474_476  JUMP_FORWARD        968  'to 968'
            478_0  COME_FROM           422  '422'

 L. 482       478  LOAD_FAST                'field_type'
              480  LOAD_CONST               ('IntegerField', 'PositiveIntegerField')
              482  COMPARE_OP               in
          484_486  POP_JUMP_IF_FALSE   546  'to 546'

 L. 483       488  SETUP_EXCEPT        526  'to 526'

 L. 484       490  LOAD_GLOBAL              int
              492  LOAD_FAST                'value'
              494  CALL_FUNCTION_1       1  '1 positional argument'
              496  STORE_FAST               'value'

 L. 485       498  LOAD_FAST                'field_type'
              500  LOAD_STR                 'PositiveIntegerField'
              502  COMPARE_OP               ==
          504_506  POP_JUMP_IF_FALSE   522  'to 522'
              508  LOAD_FAST                'value'
              510  LOAD_CONST               0
              512  COMPARE_OP               <
          514_516  POP_JUMP_IF_FALSE   522  'to 522'

 L. 486       518  LOAD_CONST               0
              520  STORE_FAST               'value'
            522_0  COME_FROM           514  '514'
            522_1  COME_FROM           504  '504'
              522  POP_BLOCK        
              524  JUMP_FORWARD        968  'to 968'
            526_0  COME_FROM_EXCEPT    488  '488'

 L. 487       526  POP_TOP          
              528  POP_TOP          
              530  POP_TOP          

 L. 488       532  LOAD_CONST               0
              534  STORE_FAST               'value'
              536  POP_EXCEPT       
              538  JUMP_FORWARD        968  'to 968'
              540  END_FINALLY      
          542_544  JUMP_FORWARD        968  'to 968'
            546_0  COME_FROM           484  '484'

 L. 489       546  LOAD_FAST                'field_type'
              548  LOAD_STR                 'FloatField'
              550  COMPARE_OP               ==
          552_554  POP_JUMP_IF_FALSE   590  'to 590'

 L. 490       556  SETUP_EXCEPT        570  'to 570'

 L. 491       558  LOAD_GLOBAL              float
              560  LOAD_FAST                'value'
              562  CALL_FUNCTION_1       1  '1 positional argument'
              564  STORE_FAST               'value'
              566  POP_BLOCK        
              568  JUMP_FORWARD        968  'to 968'
            570_0  COME_FROM_EXCEPT    556  '556'

 L. 492       570  POP_TOP          
              572  POP_TOP          
              574  POP_TOP          

 L. 493       576  LOAD_CONST               0
              578  STORE_FAST               'value'
              580  POP_EXCEPT       
              582  JUMP_FORWARD        968  'to 968'
              584  END_FINALLY      
          586_588  JUMP_FORWARD        968  'to 968'
            590_0  COME_FROM           552  '552'

 L. 494       590  LOAD_FAST                'field_type'
              592  LOAD_STR                 'AutoField'
              594  COMPARE_OP               ==
          596_598  POP_JUMP_IF_FALSE   634  'to 634'

 L. 495       600  SETUP_EXCEPT        614  'to 614'

 L. 496       602  LOAD_GLOBAL              int
              604  LOAD_FAST                'value'
              606  CALL_FUNCTION_1       1  '1 positional argument'
              608  STORE_FAST               'value'
              610  POP_BLOCK        
              612  JUMP_FORWARD        968  'to 968'
            614_0  COME_FROM_EXCEPT    600  '600'

 L. 497       614  POP_TOP          
              616  POP_TOP          
              618  POP_TOP          

 L. 498       620  LOAD_CONST               0
              622  STORE_FAST               'value'
              624  POP_EXCEPT       
              626  JUMP_FORWARD        968  'to 968'
              628  END_FINALLY      
          630_632  JUMP_FORWARD        968  'to 968'
            634_0  COME_FROM           596  '596'

 L. 499       634  LOAD_FAST                'field_type'
              636  LOAD_STR                 'ForeignKey'
              638  COMPARE_OP               ==
          640_642  POP_JUMP_IF_FALSE   968  'to 968'

 L. 500       644  LOAD_FAST                'value'
              646  STORE_FAST               'orignal_value'

 L. 502       648  SETUP_EXCEPT        662  'to 662'

 L. 503       650  LOAD_GLOBAL              int
              652  LOAD_FAST                'value'
              654  CALL_FUNCTION_1       1  '1 positional argument'
              656  STORE_FAST               'value'
              658  POP_BLOCK        
              660  JUMP_FORWARD        678  'to 678'
            662_0  COME_FROM_EXCEPT    648  '648'

 L. 504       662  POP_TOP          
              664  POP_TOP          
              666  POP_TOP          

 L. 505       668  LOAD_CONST               None
              670  STORE_FAST               'value'
              672  POP_EXCEPT       
              674  JUMP_FORWARD        678  'to 678'
              676  END_FINALLY      
            678_0  COME_FROM           674  '674'
            678_1  COME_FROM           660  '660'

 L. 507       678  LOAD_FAST                'value'
          680_682  POP_JUMP_IF_FALSE   762  'to 762'

 L. 508       684  SETUP_EXCEPT        700  'to 700'

 L. 509       686  LOAD_FAST                'field'
              688  LOAD_ATTR                remote_field
              690  LOAD_METHOD              parent_model
              692  CALL_METHOD_0         0  '0 positional arguments'
              694  STORE_FAST               'model'
              696  POP_BLOCK        
              698  JUMP_FORWARD        730  'to 730'
            700_0  COME_FROM_EXCEPT    684  '684'

 L. 510       700  DUP_TOP          
              702  LOAD_GLOBAL              AttributeError
              704  COMPARE_OP               exception-match
          706_708  POP_JUMP_IF_FALSE   728  'to 728'
              710  POP_TOP          
              712  POP_TOP          
              714  POP_TOP          

 L. 511       716  LOAD_FAST                'field'
              718  LOAD_ATTR                remote_field
              720  LOAD_ATTR                model
              722  STORE_FAST               'model'
              724  POP_EXCEPT       
              726  JUMP_FORWARD        730  'to 730'
            728_0  COME_FROM           706  '706'
              728  END_FINALLY      
            730_0  COME_FROM           726  '726'
            730_1  COME_FROM           698  '698'

 L. 512       730  LOAD_FAST                'model'
              732  LOAD_ATTR                objects
              734  LOAD_ATTR                filter
              736  LOAD_FAST                'value'
              738  LOAD_CONST               ('pk',)
              740  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
              742  LOAD_CONST               None
              744  LOAD_CONST               1
              746  BUILD_SLICE_2         2 
              748  BINARY_SUBSCR    
          750_752  JUMP_IF_TRUE_OR_POP   758  'to 758'
              754  LOAD_CONST               None
              756  BUILD_LIST_1          1 
            758_0  COME_FROM           750  '750'
              758  UNPACK_SEQUENCE_1     1 
              760  STORE_FAST               'value'
            762_0  COME_FROM           680  '680'

 L. 516       762  LOAD_FAST                'value'
          764_766  POP_JUMP_IF_TRUE    812  'to 812'
              768  LOAD_FAST                'field'
              770  LOAD_ATTR                name
              772  LOAD_STR                 'corporate_membership_type'
              774  COMPARE_OP               ==
          776_778  POP_JUMP_IF_FALSE   812  'to 812'

 L. 517       780  LOAD_GLOBAL              CorporateMembershipType
              782  LOAD_ATTR                objects
              784  LOAD_ATTR                filter

 L. 518       786  LOAD_FAST                'orignal_value'
              788  LOAD_CONST               ('name',)
              790  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
              792  LOAD_CONST               None
              794  LOAD_CONST               1
              796  BUILD_SLICE_2         2 
              798  BINARY_SUBSCR    
          800_802  JUMP_IF_TRUE_OR_POP   808  'to 808'
              804  LOAD_CONST               None
              806  BUILD_LIST_1          1 
            808_0  COME_FROM           800  '800'
              808  UNPACK_SEQUENCE_1     1 
              810  STORE_FAST               'value'
            812_0  COME_FROM           776  '776'
            812_1  COME_FROM           764  '764'

 L. 521       812  LOAD_FAST                'value'
          814_816  POP_JUMP_IF_TRUE    862  'to 862'
              818  LOAD_FAST                'field'
              820  LOAD_ATTR                name
              822  LOAD_STR                 'parent_entity'
              824  COMPARE_OP               ==
          826_828  POP_JUMP_IF_FALSE   862  'to 862'

 L. 522       830  LOAD_GLOBAL              Entity
              832  LOAD_ATTR                objects
              834  LOAD_ATTR                filter

 L. 523       836  LOAD_FAST                'orignal_value'
              838  LOAD_CONST               ('entity_name',)
              840  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
              842  LOAD_CONST               None
              844  LOAD_CONST               1
              846  BUILD_SLICE_2         2 
              848  BINARY_SUBSCR    
          850_852  JUMP_IF_TRUE_OR_POP   858  'to 858'
              854  LOAD_CONST               None
              856  BUILD_LIST_1          1 
            858_0  COME_FROM           850  '850'
              858  UNPACK_SEQUENCE_1     1 
              860  STORE_FAST               'value'
            862_0  COME_FROM           826  '826'
            862_1  COME_FROM           814  '814'

 L. 525       862  LOAD_FAST                'value'
          864_866  POP_JUMP_IF_TRUE    968  'to 968'
              868  LOAD_FAST                'field'
              870  LOAD_ATTR                null
          872_874  POP_JUMP_IF_TRUE    968  'to 968'

 L. 526       876  LOAD_FAST                'field'
              878  LOAD_ATTR                name
              880  LOAD_CONST               ('creator', 'owner')
              882  COMPARE_OP               not-in
          884_886  POP_JUMP_IF_FALSE   968  'to 968'

 L. 528       888  SETUP_EXCEPT        904  'to 904'

 L. 529       890  LOAD_FAST                'field'
              892  LOAD_ATTR                remote_field
              894  LOAD_METHOD              parent_model
              896  CALL_METHOD_0         0  '0 positional arguments'
              898  STORE_FAST               'model'
              900  POP_BLOCK        
              902  JUMP_FORWARD        934  'to 934'
            904_0  COME_FROM_EXCEPT    888  '888'

 L. 530       904  DUP_TOP          
              906  LOAD_GLOBAL              AttributeError
              908  COMPARE_OP               exception-match
          910_912  POP_JUMP_IF_FALSE   932  'to 932'
              914  POP_TOP          
              916  POP_TOP          
              918  POP_TOP          
            920_0  COME_FROM           106  '106'

 L. 531       920  LOAD_FAST                'field'
              922  LOAD_ATTR                remote_field
              924  LOAD_ATTR                model
              926  STORE_FAST               'model'
              928  POP_EXCEPT       
              930  JUMP_FORWARD        934  'to 934'
            932_0  COME_FROM           910  '910'
            932_1  COME_FROM           440  '440'
              932  END_FINALLY      
            934_0  COME_FROM           930  '930'
            934_1  COME_FROM           902  '902'

 L. 532       934  LOAD_FAST                'model'
              936  LOAD_ATTR                objects
            938_0  COME_FROM           190  '190'
              938  LOAD_METHOD              all
              940  CALL_METHOD_0         0  '0 positional arguments'
              942  LOAD_METHOD              order_by
              944  LOAD_STR                 'id'
              946  CALL_METHOD_1         1  '1 positional argument'
            948_0  COME_FROM           612  '612'
            948_1  COME_FROM           568  '568'
            948_2  COME_FROM           524  '524'
              948  LOAD_CONST               None
              950  LOAD_CONST               1
              952  BUILD_SLICE_2         2 
              954  BINARY_SUBSCR    
          956_958  JUMP_IF_TRUE_OR_POP   964  'to 964'
              960  LOAD_CONST               None
            962_0  COME_FROM           626  '626'
            962_1  COME_FROM           582  '582'
            962_2  COME_FROM           538  '538'
            962_3  COME_FROM           470  '470'
            962_4  COME_FROM           214  '214'
            962_5  COME_FROM           148  '148'
              962  BUILD_LIST_1          1 
            964_0  COME_FROM           956  '956'
              964  UNPACK_SEQUENCE_1     1 
              966  STORE_FAST               'value'
            968_0  COME_FROM           884  '884'
            968_1  COME_FROM           872  '872'
            968_2  COME_FROM           864  '864'
            968_3  COME_FROM           640  '640'
            968_4  COME_FROM           630  '630'
            968_5  COME_FROM           586  '586'
            968_6  COME_FROM           542  '542'
            968_7  COME_FROM           474  '474'
            968_8  COME_FROM           412  '412'
            968_9  COME_FROM           400  '400'
           968_10  COME_FROM           378  '378'
           968_11  COME_FROM           306  '306'
           968_12  COME_FROM           298  '298'
           968_13  COME_FROM           290  '290'
           968_14  COME_FROM           218  '218'
           968_15  COME_FROM           152  '152'

 L. 534       968  LOAD_FAST                'value'
              970  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `LOAD_FAST' instruction at offset 920