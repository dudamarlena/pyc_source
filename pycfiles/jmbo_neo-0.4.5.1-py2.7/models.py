# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/neo/models.py
# Compiled at: 2014-01-17 10:34:23
import warnings
from StringIO import StringIO
import random, string
from lxml import etree, objectify
from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.signals import user_logged_out, user_logged_in
from django.db.models import signals
from django.core.cache import cache
from django.core.exceptions import ValidationError
from django.conf import settings
from django.contrib.auth.models import UserManager
from preferences import preferences
from foundry.models import Member, DefaultAvatar
from neo import api
from neo.utils import ConsumerWrapper, normalize_username
from neo.constants import modify_flag

class NeoProfile(models.Model):
    user = models.OneToOneField(User)
    consumer_id = models.PositiveIntegerField(primary_key=True)
    created = models.DateTimeField(auto_now_add=True)
    login_alias = models.CharField(max_length=50, unique=True)
    password = models.CharField(max_length=50)

    @staticmethod
    def generate_password(length=16, chars=string.digits + string.uppercase + string.lowercase):
        """
        Generate a random new password (NOT cryptographically secure).

        (Note that CIDB requires a minimum password length of 8.)
        """
        return ('').join(random.choice(chars) for _ in range(length))

    def reset_password(self, new_password=None):
        if new_password:
            self.password = new_password
        else:
            self.password = NeoProfile.generate_password()
        api.change_password(self.login_alias, new_password, token=api.get_forgot_password_token(self.login_alias).TempToken)
        self.save()

    def save(self, *args, **kwargs):
        """
        Always store login_alias in lowercase to be able to enforce uniqueness.
        """
        self.login_alias = self.login_alias.lower()
        super(NeoProfile, self).save(*args, **kwargs)


class NeoMemberManager(UserManager):

    def get_query_set(self):
        """
        Selects NeoProfile along with Member to avoid an inevitable second query
        """
        qs = super(NeoMemberManager, self).get_query_set()
        return qs.select_related('neoprofile')


NEO_ATTR = frozenset(('first_name', 'last_name', 'dob', 'email', 'mobile_number', 'receive_sms',
                      'receive_email', 'country', 'gender'))
ADDRESS_FIELDS = frozenset(('city', 'country', 'province', 'zipcode', 'address'))
JMBO_REQUIRED_FIELDS = frozenset(('username', 'mobile_number', 'email'))
USE_MCAL = settings.NEO.get('USE_MCAL', False)

def notify_logout(sender, **kwargs):
    try:
        neo_profile = kwargs['user'].neoprofile if kwargs['user'] else None
        if neo_profile:
            api.logout(neo_profile.consumer_id)
    except NeoProfile.DoesNotExist:
        pass

    return


def neo_login(sender, **kwargs):
    try:
        neo_profile = kwargs['user'].neoprofile
        if neo_profile:
            api.authenticate(neo_profile.login_alias, neo_profile.password)
    except NeoProfile.DoesNotExist:
        pass


user_logged_in.connect(neo_login)
user_logged_out.connect(notify_logout)

def stash_neo_fields(member, clear=False):
    stashed_fields = {}
    for key in NEO_ATTR.union(ADDRESS_FIELDS).difference(JMBO_REQUIRED_FIELDS):
        stashed_fields[key] = getattr(member, key)
        field = Member._meta.get_field_by_name(key)[0]
        if clear:
            if field.null:
                setattr(member, key, None)
            elif field.default != models.fields.NOT_PROVIDED:
                setattr(member, key, field.default)
            else:
                setattr(member, key, type(stashed_fields[key])())

    return stashed_fields


def wrap_member(member, login_alias=None, password=None):
    """
    Return a `ConsumerWrapper` reflecting the given `Member`.
    """
    wrapper = ConsumerWrapper()
    for a in NEO_ATTR:
        getattr(wrapper, 'set_%s' % a)(getattr(member, a))

    if login_alias:
        wrapper.set_username(login_alias)
    if password:
        wrapper.set_password(password)
    has_address = False
    for k in ADDRESS_FIELDS:
        if getattr(member, k, None):
            has_address = True
            break

    if has_address:
        wrapper.set_address(member.address, member.city, member.province, member.zipcode, member.country)
    return wrapper


def create_consumer(member):
    password = NeoProfile.generate_password()
    login_alias = normalize_username(member.username)
    wrapper = wrap_member(member, login_alias=login_alias, password=password)
    consumer_id, uri = api.create_consumer(wrapper.consumer)
    api.complete_registration(consumer_id)
    return NeoProfile(user=member, consumer_id=consumer_id, password=password, login_alias=login_alias)


def update_consumer(member):
    consumer_id = member.neoprofile.consumer_id
    old_member = cache.get('neo_consumer_%s' % member.pk, None)
    wrapper = ConsumerWrapper()
    if old_member is not None:
        for k in NEO_ATTR:
            current = getattr(member, k, None)
            old = old_member.get(k, None)
            if current != old:
                if old is None:
                    getattr(wrapper, 'set_%s' % k)(current, mod_flag=modify_flag['INSERT'])
                elif current is None:
                    getattr(wrapper, 'set_%s' % k)(old, mod_flag=modify_flag['DELETE'])
                else:
                    getattr(wrapper, 'set_%s' % k)(current, mod_flag=modify_flag['UPDATE'])

        has_address = False
        had_address = False
        address_changed = False
        for k in ADDRESS_FIELDS:
            current = getattr(member, k, None)
            old = old_member.get(k, None)
            if current:
                has_address = True
            if old:
                had_address = True
            if current != old:
                address_changed = True

        if address_changed:
            if not has_address:
                wrapper.set_address(old_member.address, old_member.city, old_member.province, old_member.zipcode, old_member.country, modify_flag['DELETE'])
            elif not had_address:
                wrapper.set_address(member.address, member.city, member.province, member.zipcode, member.country)
            else:
                wrapper.set_address(member.address, member.city, member.province, member.zipcode, member.country, mod_flag=modify_flag['UPDATE'])
    if not wrapper.is_empty:
        if not wrapper.profile_is_empty:
            wrapper.set_ids_for_profile(api.get_consumer_profile(consumer_id, username=member.neoprofile.login_alias, password=member.neoprofile.password))
        api.update_consumer(consumer_id, wrapper.consumer, username=member.neoprofile.login_alias, password=member.neoprofile.password)
    return


original_member_full_clean = Member.full_clean

def clean_member(member):
    if not member.pk:
        original_member_full_clean(member)
    if not member.is_profile_complete:
        member.is_profile_complete = True
        required_fields = preferences.RegistrationPreferences.required_fields
        for name in required_fields:
            if not getattr(member, name, None):
                member.is_profile_complete = False
                break

    if member.is_profile_complete:
        try:
            has_neoprofile = bool(member.neoprofile)
        except NeoProfile.DoesNotExist:
            has_neoprofile = False

        if member.pk and has_neoprofile:
            update_consumer(member)
        else:
            member.neoprofile = create_consumer(member)
            if member.pk:
                api.authenticate(member.neoprofile.login_alias, member.neoprofile.password)
    member.need_to_clean_member = False
    return


original_member_save = Member.save

def save_member(member, *args, **kwargs):
    if getattr(member, 'need_to_clean_member', True):
        try:
            member.full_clean()
        except ValidationError as e:
            warnings.warn('Consumer could not be created via Neo - %s' % str(e))

        member.need_to_clean_member = True
    stash_fields = member.is_profile_complete
    clear_fields = not USE_MCAL
    if stash_fields:
        stashed_fields = stash_neo_fields(member, clear=clear_fields)
    original_member_save(member, *args, **kwargs)
    if stash_fields:
        if clear_fields:
            for key, val in stashed_fields.iteritems():
                setattr(member, key, val)

        stashed_fields.update(dict((k, getattr(member, k)) for k in JMBO_REQUIRED_FIELDS))
        cache.set('neo_consumer_%s' % member.pk, stashed_fields, 1200)
    try:
        if member.neoprofile:
            member.neoprofile.user = member
            member.neoprofile.save()
    except NeoProfile.DoesNotExist:
        pass


def load_consumer(sender, *args, **kwargs):
    instance = kwargs['instance']
    if instance.id:
        cache_key = 'neo_consumer_%s' % instance.id
        if USE_MCAL:
            if not cache.has_key(cache_key):
                member_dict = dict((k, getattr(instance, k)) for k in NEO_ATTR.union(ADDRESS_FIELDS))
                cache.set(cache_key, member_dict, 1200)
        else:
            try:
                member_dict = cache.get(cache_key, None)
                if not member_dict:
                    neoprofile = instance.neoprofile
                    if neoprofile:
                        consumer = api.get_consumer(instance.neoprofile.consumer_id)
                        wrapper = ConsumerWrapper(consumer=consumer)
                        member_dict = dict((k, getattr(wrapper, k)) for k in NEO_ATTR)
                        member_dict.update(wrapper.address)
                if member_dict:
                    for key, val in member_dict.iteritems():
                        setattr(instance, key, val)

            except NeoProfile.DoesNotExist:
                pass

    return


signals.post_init.connect(load_consumer, sender=Member)

def dataloadtool_export(output, credentials_output, members, password_callback=None, pretty_print=False):
    """
    Export the given members as XML input for the CIDB Data Load Tool.

    :param output: File-like object to write to.
    :param members: Queryset of members to export. If this is a large queryset,
        consider using `iterator()` on it, to avoid excessive caching.

    :param password_callback:
        If supplied, use this function to set or generate new passwords as part
        of the export. This can be used, for example, to port member passwords
        from another source into CIDB.

        The function will be passed each `Member` in turn, and should return
        either a new (raw, unhashed) password, or `None`, to not include a
        password in the export. (To preserve what the default exported password
        would be, the function can explicitly return the member's
        `raw_password`, if it is set.)
    """

    def etree_from_gds(gds):
        sio = StringIO()
        gds.export(sio, 0, pretty_print=False)
        return etree.fromstring(sio.getvalue())

    password_path = objectify.ObjectPath('Consumer.UserAccount.LoginCredentials.Password')
    output.write('<Consumers>\n')
    last_username = ''
    import time, csv
    credentials_csv = csv.DictWriter(credentials_output, ['username', 'login_alias', 'password'])
    for i, member in enumerate(members.select_related('neoprofile').order_by('username').iterator()):
        try:
            wrapper = wrap_member(member, login_alias=member.neoprofile.login_alias, password=member.neoprofile.password)
        except (NeoProfile.DoesNotExist, AttributeError):
            password = NeoProfile.generate_password()
            if member.username.lower() == last_username:
                timestamp = str(int(time.time() * 1000000))[-10:]
                login_alias = '%s%s' % (member.username, timestamp)
            else:
                login_alias = member.username
            login_alias = normalize_username(login_alias)
            wrapper = wrap_member(member, login_alias=login_alias, password=password)
            credentials_csv.writerow({'username': member.username.encode('utf-8'), 
               'login_alias': login_alias.encode('utf-8'), 
               'password': password.encode('utf-8')})

        last_username = member.username.lower()
        elem = etree_from_gds(wrapper.consumer)
        elem.attrib['recordNumber'] = str(i)
        if password_callback is not None:
            new_password = password_callback(member)
            if new_password is not None:
                password_path.setattr(elem, new_password)
                objectify.deannotate(password_path(elem), cleanup_namespaces=True)
            elif password_path.hasattr(elem):
                old_password = password_path(elem)
                old_password.getparent().remove(old_password)
        output.write(etree.tostring(elem, pretty_print=pretty_print))
        output.write('\n')

    output.write('</Consumers>\n')
    return


Member.save = save_member
Member.full_clean = clean_member
Member.add_to_class('objects', NeoMemberManager())