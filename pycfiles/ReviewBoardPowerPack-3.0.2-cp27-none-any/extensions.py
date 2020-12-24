# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /beanbag_licensing/extensions.py
# Compiled at: 2019-06-17 15:11:31
from __future__ import unicode_literals
import hashlib, hmac, logging, time, uuid
from django.conf import settings
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.utils import six
from reviewboard.admin.support import get_install_key
from reviewboard.extensions.base import Extension
from beanbag_licensing.auto_add import AutoAddMode, setup_auto_add_remove
from beanbag_licensing.errors import IncorrectSignatureError, TooManyUsersForLicenseError
from beanbag_licensing.keys import BEANBAG_PUBLIC_KEY
from beanbag_licensing.license import License

class LicenseSettings(object):
    """Manages license-related settings for the extension.

    This wraps the extension's settings, handling any license loading and
    user management.
    """

    def __init__(self, ext_settings, default_ext_settings, licensed_product_name, licensed_product_name_short, licensed_user_model):
        """Initialize the settings.

        Args:
            ext_settings (dict):
                Current settings from the extension.

            default_ext_settings (dict):
                Default settings for the extension.

            licensed_product_name (unicode):
                The full product name.

            licensed_product_name_short (unicode):
                A shortened version of the product name. This can be the
                same as ``licensed_product_name``.

            licensed_user_model (type):
                The Django model class used to store assigned seat user
                information.
        """
        self.settings = ext_settings
        self.licensed_product_name = licensed_product_name
        self.licensed_product_name_short = licensed_product_name_short
        self.licensed_user_model = licensed_user_model
        self.license = None
        self._licensed_user_ids = None
        default_ext_settings.update({b'auto_add_mode': AutoAddMode.DISABLED, 
           b'auto_add_groups': [], b'license_data': b'', 
           b'licensed_users_stamp': b''})
        self.settings.load()
        return

    def read_license(self, license_data):
        """Read license data using the configured public key.

        This is normally a simple wrapper around
        :py:meth:`License.read <beanbag_licensing.license.License.read>`,
        but allows for the usage of the test public key if running unit tests
        in a development environment.

        Args:
            license_data (bytes):
                The license data to read.

        Returns:
            beanbag_licensing.license.License:
            The license parsed by the data.

        Raises:
            beanbag_licensing.errors.IncorrectSignatureError:
                The license data could not be verified against the license
                signature or public key.
        """
        if not settings.PRODUCTION and getattr(settings, b'RUNNING_TEST', False):
            public_key = self.settings.get(b'license_public_key', BEANBAG_PUBLIC_KEY)
        else:
            public_key = BEANBAG_PUBLIC_KEY
        return License.read(license_data, public_key=public_key)

    def load_license(self):
        """Loads the license data from settings.

        If a license is found, it will be activated with the install key,
        and :py:attr:`license` will be set.

        If there is no license, or there was a failure in loading the
        license, an error will be logged and :py:attr:`license` will be None.

        Args:
            license_data (bytes):
                The license data to read.

        Returns:
            beanbag_licensing.license.License:
            The license parsed by the data.

        Raises:
            beanbag_licensing.errors.IncorrectSignatureError:
                The license data could not be verified against the license
                signature or public key.
        """
        self.license = None
        license_data = self.settings.get(b'license_data')
        if license_data:
            try:
                self.license = self.read_license(license_data)
            except IncorrectSignatureError:
                logging.error(b'Failed to load license for %s: incorrect signature', self.licensed_product_name_short)

        if not self.license:
            self.license = License.make_unlicensed(self.licensed_product_name)
        install_key = get_install_key()
        self.license.activate(install_key)
        if not self.license.valid_install_key:
            self.license = License.make_unlicensed(self.licensed_product_name)
            self.license.activate(install_key)
        return

    @property
    def licensed_user_ids(self):
        if self._licensed_user_ids is None:
            self._licensed_user_ids = list(self.licensed_users.values_list(b'user_id', flat=True))
        return self._licensed_user_ids

    @property
    def licensed_users(self):
        """Returns the list of registered LicensedUsers.

        If a license is set, then the list of LicensedUser instances will
        be returend.

        If the license has a user cap, then the results will be capped to
        that many users.
        """
        users = self.licensed_user_model.objects.all()
        if not self.license:
            return users.none()
        if self.license.has_user_cap:
            users = users[:self.license.user_cap]
        return users

    @property
    def all_licensed_users(self):
        """Return a list of all registered LicensedUsers, without caps.

        The licensed_users property caps the returned number of users,
        based on the license cap. This returns all licensed users,
        regardless of cap.
        """
        users = self.licensed_user_model.objects.all()
        if not self.license:
            return users.none()
        return users

    @property
    def licensed_user_count(self):
        """Returns the number of currently licensed users."""
        return len(self.licensed_user_ids)

    @property
    def hit_licensed_user_count(self):
        """Returns whether the licensed user cap was hit."""
        return not self.license or self.license.has_user_cap and self.licensed_user_count >= self.license.user_cap

    @property
    def licensed_users_remaining(self):
        """Returns the number of allowed licensed users remaining.

        If there is no license set, this will return 0.

        If the license has no user cap, this will assert. Callers must
        check for a cap before calling this.
        """
        if not self.license:
            return 0
        assert self.license.has_user_cap
        return self.license.user_cap - self.licensed_user_count

    def add_licensed_users(self, users, auto_added=False):
        """Add one or more licensed users.

        This will filter out any users that are already licensed.

        If the number of users exceeds the cap, then no user will be added,
        and a :py:exc:`beanbag_licensing.errors.TooManyUsersForLicenseError`
        will be raised.

        Args:
            users (list of django.contrib.auth.models.User):
                List of users to add to the license.

            auto_added (bool, optional):
                If ``True``, the ``auto_added`` flag for each user will be set.

        Returns:
            list of django.contrib.auth.models.User:
            The list of users added to the license. This may differ from the
            provided list, as it will only consider users not already on the
            license.

        Raises:
            beanbag_licensing.errors.TooManyUsersForLicenseError:
                Attempted to add more users to the license than allowed.
        """
        users = [ user for user in users if not self.is_user_licensed(user)
                ]
        if not self.license or self.license.has_user_cap and len(users) > self.licensed_users_remaining:
            raise TooManyUsersForLicenseError(len(users), self.licensed_users_remaining)
        if users:
            self.licensed_user_model.objects.bulk_create([ self.licensed_user_model(user=user, auto_added=auto_added) for user in users
                                                         ])
            self.sync_licensed_users()
        return users

    def remove_licensed_users(self, user_ids):
        """Removes one or more licensed users.

        Args:
            users (list of int):
                List of user IDs to remove from the license.

        Returns:
            list of django.contrib.auth.models.User:
            The list of users removed from the license. This may differ from
            the provided list, as it will only consider users who were on
            the license and still remain in the database.
        """
        to_remove = set(user_ids)
        users = []
        for user in User.objects.filter(pk__in=user_ids):
            if self.is_user_licensed(user):
                users.append(user)
            else:
                to_remove.remove(user.pk)

        if to_remove:
            self.licensed_user_model.objects.filter(user_id__in=to_remove).delete()
            self.sync_licensed_users()
        return users

    def is_user_licensed(self, user):
        """Returns whether a particular user is licensed."""
        return self.license is not None and user.is_authenticated() and user.pk in self.licensed_user_ids

    def sync_licensed_users(self):
        """Synchronizes the list of licensed users.

        This will store a stamp in settings, triggering a reload in any
        other server threads/processes, so that they'll regenerate their
        list of IDs.
        """
        self._licensed_user_ids = None
        self.settings[b'licensed_users_stamp'] = uuid.uuid4().get_hex()
        self.save()
        return

    def save(self):
        """Saves any license settings to the database."""
        self.settings.save()


class LicensedExtension(Extension):
    """Base class for a licensed extension.

    This is responsible for managing much of the state of the license and any
    licensed features for the extension.
    """
    is_configurable = True
    licensed_user_model = None
    licensed_product_name = None
    licensed_product_name_short = None
    license_url_names = {b'apply-license': None, 
       b'configure': None, 
       b'manage-users': None}

    def __init__(self, *args, **kwargs):
        super(LicensedExtension, self).__init__(*args, **kwargs)
        self.hooks_initialized = False
        if not hasattr(self, b'features'):
            self.features = {}
        self.license_settings = LicenseSettings(ext_settings=self.settings, default_ext_settings=self.default_settings, licensed_product_name=self.licensed_product_name, licensed_product_name_short=self.licensed_product_name_short, licensed_user_model=self.licensed_user_model)
        self.update_license()

    @property
    def license(self):
        return self.license_settings.license

    def update_license(self):
        self.license_settings.load_license()
        if self.license and self.license.valid:
            self.add_hooks()
        else:
            self.shutdown_hooks()

    def get_license_update_request(self):
        """Return a payload for fetching an updated license.

        This is used to communicate with the license portal to fetch a new
        license, if one is available. The payload should be sent shortly after
        generation, as it's time-sensitive.

        Returns:
            unicode:
            The update request payload to send.
        """
        license_data = self.settings.get(b'license_data').strip()
        if not license_data:
            return None
        else:
            license_sig = hashlib.sha256(license_data.encode(b'utf-8')).hexdigest()
            now = time.time()
            hmac_sig = hmac.new(key=license_sig.encode(b'utf-8'), msg=b'%d' % now, digestmod=hashlib.sha256)
            return b't=%d,v1=%s' % (now, hmac_sig.hexdigest())

    def get_license_model_data(self):
        """Return data for use in the License JavaScript model.

        This returns data for use with :js:class:`PowerPack.Admin.License`,
        which is used in the administration UI.

        Returns:
            dict:
            The license model data.
        """
        license = self.license
        license_settings = self.license_settings
        try:
            install_key = license.install_keys[0]
        except IndexError:
            install_key = None

        if license.unlicensed:
            license_type = b'UNLICENSED'
        elif license.trial:
            license_type = b'TRIAL'
        else:
            license_type = b'PURCHASED'
        return {b'applyLicenseURL': reverse(self.license_url_names[b'apply-license']), 
           b'company': license.company, 
           b'expired': license.expired, 
           b'expirationDate': license.expiration, 
           b'features': dict((feature.feature_id, feature.enabled or feature.always_enabled) for feature in six.itervalues(self.features)), 
           b'hardExpired': license.hard_expired, 
           b'hardExpirationDate': license.hard_expiration_date, 
           b'hasUserCap': license.has_user_cap, 
           b'installKey': install_key, 
           b'inPerpetualUserMode': license.in_perpetual_user_mode, 
           b'licenseType': license_type, 
           b'numPerpetualUsers': license.num_perpetual_users, 
           b'updateRequestPayload': self.get_license_update_request(), 
           b'userCap': license.user_cap, 
           b'userCount': license_settings.licensed_user_count}

    def get_features_json(self):
        """Return JSON data describing all licensed features.

        Returns:
            list of dict:
            A list of all licensed features.
        """
        return [ {b'always_enabled': feature.always_enabled, b'available': feature.available, b'id': feature.feature_id, b'name': feature.name, b'summary': feature.summary, b'unavailable_reason': feature.unavailable_reason} for feature in six.itervalues(self.features)
               ]

    def get_trial_url(self, request):
        raise NotImplementedError

    def get_purchase_url(self, request):
        raise NotImplementedError

    def add_hooks(self):
        if not self.hooks_initialized:
            self.hooks_initialized = True
            setup_auto_add_remove(self)
            self.enable_features()

    def shutdown_hooks(self):
        if self.hooks_initialized:
            self.hooks_initialized = False
            for hook in self.hooks:
                if hook.initialized:
                    if hasattr(hook, b'disable_hook'):
                        hook.disable_hook()
                    else:
                        hook.shutdown()

            self.disable_features()

    def enable_features(self):
        """Enables features on the extension.

        Subclasses can implement this to enable any hooks or activate any
        subsystems needed.
        """
        pass

    def disable_features(self):
        """Disables features on the extension.

        Subclasses can implement this to disable any hooks or deactivate any
        subsystems needed.
        """
        pass