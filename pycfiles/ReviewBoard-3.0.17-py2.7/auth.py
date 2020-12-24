# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/reviewboard/accounts/forms/auth.py
# Compiled at: 2020-02-11 04:03:56
from __future__ import unicode_literals
import re, sre_constants
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm as DjangoAuthenticationForm
from django.core.exceptions import ValidationError
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext_lazy as _
from djblets.auth.ratelimit import is_ratelimited
from djblets.siteconfig.forms import SiteSettingsForm
from reviewboard.admin.checks import get_can_enable_dns, get_can_enable_ldap

class ActiveDirectorySettingsForm(SiteSettingsForm):
    """A form for configuring the Active Directory authentication backend."""
    auth_ad_domain_name = forms.CharField(label=_(b'Domain name'), help_text=_(b'Enter the domain name to use, (ie. example.com). This will be used to query for LDAP servers and to bind to the domain.'), required=True, widget=forms.TextInput(attrs={b'size': b'40'}))
    auth_ad_use_tls = forms.BooleanField(label=_(b'Use TLS for authentication'), required=False)
    auth_ad_find_dc_from_dns = forms.BooleanField(label=_(b'Find DC from DNS'), help_text=_(b'Query DNS to find which domain controller to use'), required=False)
    auth_ad_domain_controller = forms.CharField(label=_(b'Domain controller'), help_text=_(b'If not using DNS to find the DC, specify the domain controller(s) here (eg. ctrl1.example.com ctrl2.example.com:389)'), required=False, widget=forms.TextInput(attrs={b'size': b'40'}))
    auth_ad_ou_name = forms.CharField(label=_(b'OU name'), help_text=_(b'Optionally restrict users to specified OU.'), required=False, widget=forms.TextInput(attrs={b'size': b'40'}))
    auth_ad_group_name = forms.CharField(label=_(b'Group name'), help_text=_(b'Optionally restrict users to specified group.'), required=False, widget=forms.TextInput(attrs={b'size': b'40'}))
    auth_ad_search_root = forms.CharField(label=_(b'Custom search root'), help_text=_(b'Optionally specify a custom search root, overriding the built-in computed search root. If set, "OU name" is ignored.'), required=False, widget=forms.TextInput(attrs={b'size': b'40'}))
    auth_ad_recursion_depth = forms.IntegerField(label=_(b'Recursion Depth'), help_text=_(b'Depth to recurse when checking group membership. 0 to turn off, -1 for unlimited.'), required=False, widget=forms.TextInput(attrs={b'size': b'40'}))

    def load(self):
        """Load the data for the form."""
        can_enable_dns, reason = get_can_enable_dns()
        if not can_enable_dns:
            self.disabled_fields[b'auth_ad_find_dc_from_dns'] = reason
        can_enable_ldap, reason = get_can_enable_ldap()
        if not can_enable_ldap:
            self.disabled_fields[b'auth_ad_use_tls'] = True
            self.disabled_fields[b'auth_ad_group_name'] = True
            self.disabled_fields[b'auth_ad_recursion_depth'] = True
            self.disabled_fields[b'auth_ad_ou_name'] = True
            self.disabled_fields[b'auth_ad_search_root'] = True
            self.disabled_fields[b'auth_ad_find_dc_from_dns'] = True
            self.disabled_fields[b'auth_ad_domain_controller'] = True
            self.disabled_reasons[b'auth_ad_domain_name'] = reason
        super(ActiveDirectorySettingsForm, self).load()

    class Meta:
        title = _(b'Active Directory Authentication Settings')
        fieldsets = (
         (
          None,
          {b'fields': ('auth_ad_domain_name', 'auth_ad_use_tls', 'auth_ad_find_dc_from_dns', 'auth_ad_domain_controller')}),
         (
          _(b'Access Control Settings'),
          {b'fields': ('auth_ad_ou_name', 'auth_ad_group_name')}),
         (
          _(b'Advanced Settings'),
          {b'fields': ('auth_ad_search_root', 'auth_ad_recursion_depth')}))


class StandardAuthSettingsForm(SiteSettingsForm):
    """A form for configuring the builtin authentication backend."""
    auth_enable_registration = forms.BooleanField(label=_(b'Enable registration'), help_text=_(b'Allow users to register new accounts.'), required=False)
    auth_registration_show_captcha = forms.BooleanField(label=_(b'Show a captcha for registration'), required=False)
    recaptcha_public_key = forms.CharField(label=_(b'reCAPTCHA Public Key'), required=False, widget=forms.TextInput(attrs={b'size': b'60'}))
    recaptcha_private_key = forms.CharField(label=_(b'reCAPTCHA Private Key'), required=False, widget=forms.TextInput(attrs={b'size': b'60'}))

    def __init__(self, *args, **kwargs):
        super(StandardAuthSettingsForm, self).__init__(*args, **kwargs)
        self.fields[b'auth_registration_show_captcha'].help_text = mark_safe(_(b'Displays a captcha using <a href="%(recaptcha_url)s">reCAPTCHA</a> on the registration page. To enable this, you will need to go <a href="%(register_url)s">here</A> to register an account and type in your new keys below.') % {b'recaptcha_url': b'http://www.google.com/recaptcha', 
           b'register_url': b'https://www.google.com/recaptcha/admin#createsite'})

    def clean_recaptcha_public_key(self):
        """Validate that the reCAPTCHA public key is specified if needed."""
        key = self.cleaned_data[b'recaptcha_public_key'].strip()
        if self.cleaned_data[b'auth_registration_show_captcha'] and not key:
            raise ValidationError(_(b'This field is required.'))
        return key

    def clean_recaptcha_private_key(self):
        """Validate that the reCAPTCHA private key is specified if needed."""
        key = self.cleaned_data[b'recaptcha_private_key'].strip()
        if self.cleaned_data[b'auth_registration_show_captcha'] and not key:
            raise ValidationError(_(b'This field is required.'))
        return key

    class Meta:
        title = _(b'Registration Settings')
        fieldsets = (
         (
          None,
          {b'fields': ('auth_enable_registration', )}),
         (
          _(b'reCAPTCHA Settings'),
          {b'fields': ('auth_registration_show_captcha', 'recaptcha_public_key', 'recaptcha_private_key')}))


class HTTPBasicSettingsForm(SiteSettingsForm):
    """A form for configuring the HTTP Digest authentication backend."""
    auth_digest_file_location = forms.CharField(label=_(b'.htpasswd File location'), help_text=_(b'Location of the .htpasswd file which stores the usernames and passwords in digest format'), widget=forms.TextInput(attrs={b'size': b'60'}))
    auth_digest_realm = forms.CharField(label=_(b'HTTP Digest Realm'), help_text=_(b'Realm used for HTTP Digest authentication'), widget=forms.TextInput(attrs={b'size': b'40'}))

    class Meta:
        title = _(b'HTTP Digest Authentication Settings')


class LDAPSettingsForm(SiteSettingsForm):
    """A form for configuring the LDAP authentication backend."""
    auth_ldap_uri = forms.CharField(label=_(b'LDAP Server'), help_text=_(b'The LDAP server to authenticate with. For example: ldap://localhost:389'), widget=forms.TextInput(attrs={b'size': b'40'}))
    auth_ldap_base_dn = forms.CharField(label=_(b'LDAP Base DN'), help_text=_(b'The LDAP Base DN for performing LDAP searches.  For example: ou=users,dc=example,dc=com'), required=True, widget=forms.TextInput(attrs={b'size': b'40'}))
    auth_ldap_uid = forms.CharField(label=_(b'Username Attribute'), help_text=_(b"The attribute in the LDAP server that stores a user's login name."), required=True)
    auth_ldap_given_name_attribute = forms.CharField(label=_(b'Given Name Attribute'), initial=b'givenName', help_text=_(b"The attribute in the LDAP server that stores the user's given name."), required=False)
    auth_ldap_surname_attribute = forms.CharField(label=_(b'Surname Attribute'), initial=b'sn', help_text=_(b"The attribute in the LDAP server that stores the user's surname."), required=False)
    auth_ldap_full_name_attribute = forms.CharField(label=_(b'Full Name Attribute'), help_text=_(b'The attribute in the LDAP server that stores the user\'s full name.  This takes precedence over the "Given Name Attribute" and "Surname Attribute."'), required=False)
    auth_ldap_email_domain = forms.CharField(label=_(b'E-Mail Domain'), help_text=_(b'The domain name appended to the username to construct the user\'s e-mail address. This takes precedence over "E-Mail LDAP Attribute."'), required=False, widget=forms.TextInput(attrs={b'size': b'40'}))
    auth_ldap_email_attribute = forms.CharField(label=_(b'E-Mail LDAP Attribute'), help_text=_(b"The attribute in the LDAP server that stores the user's e-mail address. For example: mail"), required=False)
    auth_ldap_tls = forms.BooleanField(label=_(b'Use TLS for authentication'), required=False)
    auth_ldap_uid_mask = forms.CharField(label=_(b'Custom LDAP User Search Filter'), required=False, widget=forms.TextInput(attrs={b'size': b'40'}))
    auth_ldap_anon_bind_uid = forms.CharField(label=_(b'Review Board LDAP Bind Account'), help_text=_(b'The full distinguished name of a user account with sufficient access to perform lookups of users and groups in the LDAP server. If the LDAP server permits such lookups via anonymous bind, you may leave this field blank.'), required=False, widget=forms.TextInput(attrs={b'size': b'40'}))
    auth_ldap_anon_bind_passwd = forms.CharField(label=_(b'Review Board LDAP Bind Password'), widget=forms.PasswordInput(attrs={b'size': b'30'}, render_value=True), help_text=_(b'The password for the Review Board LDAP Bind Account.'), required=False)

    def __init__(self, *args, **kwargs):
        super(LDAPSettingsForm, self).__init__(*args, **kwargs)
        self.fields[b'auth_ldap_uid_mask'].help_text = mark_safe(_(b'A custom LDAP search filter, corresponding to RFC 2254. If left unset, this option is equivalent to <tt>(usernameattribute=%(varname)s)</tt>. Use <tt>"%(varname)s"</tt> wherever the username would normally go. Specify this value only if the default cannot locate all users.') % {b'varname': b'%s'})

    def load(self):
        """Load the data for the form."""
        can_enable_ldap, reason = get_can_enable_ldap()
        if not can_enable_ldap:
            self.disabled_fields[b'auth_ldap_uri'] = True
            self.disabled_fields[b'auth_ldap_given_name_attribute'] = True
            self.disabled_fields[b'auth_ldap_surname_attribute'] = True
            self.disabled_fields[b'auth_ldap_full_name_attribute'] = True
            self.disabled_fields[b'auth_ldap_email_domain'] = True
            self.disabled_fields[b'auth_ldap_email_attribute'] = True
            self.disabled_fields[b'auth_ldap_tls'] = True
            self.disabled_fields[b'auth_ldap_base_dn'] = True
            self.disabled_fields[b'auth_ldap_uid'] = True
            self.disabled_fields[b'auth_ldap_uid_mask'] = True
            self.disabled_fields[b'auth_ldap_anon_bind_uid'] = True
            self.disabled_fields[b'auth_ldap_anon_bind_password'] = True
            self.disabled_reasons[b'auth_ldap_uri'] = reason
        super(LDAPSettingsForm, self).load()

    class Meta:
        title = _(b'LDAP Authentication Settings')
        fieldsets = (
         (
          None,
          {b'fields': ('auth_ldap_uri', 'auth_ldap_tls', 'auth_ldap_anon_bind_uid', 'auth_ldap_anon_bind_passwd',
 'auth_ldap_base_dn')}),
         (
          _(b'User Lookups'),
          {b'fields': ('auth_ldap_uid', 'auth_ldap_given_name_attribute', 'auth_ldap_surname_attribute',
 'auth_ldap_full_name_attribute', 'auth_ldap_email_attribute', 'auth_ldap_email_domain',
 'auth_ldap_uid_mask')}))


class LegacyAuthModuleSettingsForm(SiteSettingsForm):
    """A form for configuring old-style custom authentication backends.

    Newer authentication backends are registered via the extensions framework,
    but there used to be a method by which users just put in a list of python
    module paths. This form allows that configuration to be edited.
    """
    custom_backends = forms.CharField(label=_(b'Backends'), help_text=_(b'A comma-separated list of old-style custom auth backends. These are represented as Python module paths.'), widget=forms.TextInput(attrs={b'size': b'40'}))

    def load(self):
        """Load the data for the form."""
        self.fields[b'custom_backends'].initial = (b', ').join(self.siteconfig.get(b'auth_custom_backends'))
        super(LegacyAuthModuleSettingsForm, self).load()

    def save(self):
        """Save the form."""
        self.siteconfig.set(b'auth_custom_backends', re.split(b',\\s*', self.cleaned_data[b'custom_backends']))
        super(LegacyAuthModuleSettingsForm, self).save()

    class Meta:
        title = _(b'Legacy Authentication Module Settings')
        save_blacklist = ('custom_backends', )


class NISSettingsForm(SiteSettingsForm):
    """A form for configuring the NIS authentication backend."""
    auth_nis_email_domain = forms.CharField(label=_(b'E-Mail Domain'), widget=forms.TextInput(attrs={b'size': b'40'}))

    class Meta:
        title = _(b'NIS Authentication Settings')


class X509SettingsForm(SiteSettingsForm):
    """A form for configuring the X509 certificate authentication backend."""
    auth_x509_username_field = forms.ChoiceField(label=_(b'Username Field'), choices=(
     (
      b'SSL_CLIENT_S_DN', _(b'DN (Distinguished Name)')),
     (
      b'SSL_CLIENT_S_DN_CN', _(b'CN (Common Name)')),
     (
      b'SSL_CLIENT_S_DN_Email', _(b'E-mail address')),
     (
      b'CUSTOM', _(b'Custom Field'))), help_text=_(b'The X.509 certificate field from which the Review Board username will be extracted.'), required=True)
    auth_x509_custom_username_field = forms.CharField(label=_(b'Custom Username Field'), help_text=_(b'The custom X.509 certificate field from which the Review Board username will be extracted. (only used if Username Field is "Custom Field"'), required=False, widget=forms.TextInput(attrs={b'size': b'40'}))
    auth_x509_username_regex = forms.CharField(label=_(b'Username Regex'), help_text=_(b"Optional regex used to convert the selected X.509 certificate field to a usable Review Board username. For example, if using the e-mail field to retrieve the username, use this regex to get the username from an e-mail address: '(\\s+)@yoursite.com'. There must be only one group in the regex."), required=False, widget=forms.TextInput(attrs={b'size': b'40'}))
    auth_x509_autocreate_users = forms.BooleanField(label=_(b'Automatically create new user accounts.'), help_text=_(b'Enabling this option will cause new user accounts to be automatically created when a new user with an X.509 certificate accesses Review Board.'), required=False)

    def clean_auth_x509_username_regex(self):
        """Validate that the specified regular expression is valid."""
        regex = self.cleaned_data[b'auth_x509_username_regex']
        try:
            re.compile(regex)
        except sre_constants.error as e:
            raise ValidationError(e)

        return regex

    class Meta:
        title = _(b'X.509 Client Certificate Authentication Settings')


class AuthenticationForm(DjangoAuthenticationForm):
    """Form used for user logins.

    This extends Django's built-in AuthenticationForm implementation to allow
    users to specify their e-mail address in place of their username. In
    addition, it also tracks the number of failed login attempts for a given
    time frame, and informs the user whether the maximum number of attempts
    have been exceeded.
    """
    username = forms.CharField(label=_(b'Username'), widget=forms.TextInput(attrs={b'autofocus': b'autofocus'}))

    def clean_username(self):
        """Validate the 'username' field.

        In case the given text is not a user found on the system, attempt a
        look-up using it as an e-mail address and change the user-entered text
        so that login can succeed.
        """
        username = self.cleaned_data.get(b'username')
        if not User.objects.filter(username=username).exists():
            try:
                username = User.objects.get(email=username).username
            except (User.DoesNotExist, User.MultipleObjectsReturned):
                pass

        return username

    def clean(self):
        """Validate the authentication form.

        In case authentication has failed for the given user, Djblets's rate
        limiting feature will increment the number of failed login attempts
        until the maximum number of attempts have been reached. The user
        will have to wait until the rate limit time period is over before
        trying again.

        Returns:
            dict:
            The cleaned data for all fields in the form.

        Raises:
            django.core.exceptions.ValidationError:
                The data in the form was not valid.
        """
        request = self.request
        if is_ratelimited(request, increment=False):
            raise forms.ValidationError(_(b'Maximum number of login attempts exceeded.'))
        try:
            self.cleaned_data = super(AuthenticationForm, self).clean()
        except ValidationError:
            is_ratelimited(request, increment=True)
            raise

        return self.cleaned_data