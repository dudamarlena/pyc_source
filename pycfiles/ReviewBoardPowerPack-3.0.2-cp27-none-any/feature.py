# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /rbpowerpack/sshdb/feature.py
# Compiled at: 2019-06-17 15:11:31
from __future__ import unicode_literals
import settings_local
from django.utils.translation import ugettext_lazy as _
from rbpowerpack.extension.features import Feature
from rbpowerpack.sshdb.secrets import has_valid_sshdb_secret_key
from rbpowerpack.sshdb.storage import enable_sshdb, disable_sshdb

class SSHDBFeature(Feature):
    """Feature support for SSH key scalability."""
    feature_id = b'sshdb'
    name = _(b'Distributed SSH Keys')
    summary = _(b'Automatically share your SSH keys across Review Board servers, making it easier to scale out your infrastructure.')
    enabled_settings_key = b'sshdb_enabled'
    enabled_by_default = False
    default_settings = {b'rbe_migration_done': False, 
       b'sshdb_keys_imported': False}

    def check_availability(self):
        """Return whether the feature is available to enable and use.

        This builds upon the default behavior to ensure that an active trial or
        full license is currently set, and that a valid SSHDB secret key
        (either through ``settings.SSHDB_SECRET_KEY`` or a valid length in
        ``settings.SECRET_KEY``) is set before allowing the feature to be
        enabled.

        Returns:
            tuple:
            A tuple of ``(available, unavailable_reason)``.

            ``available`` is a boolean indicating if the feature is available
            to be enabled and used.

            ``unavailable_reason`` is a string describing why the feature
            cannot be enabled. It should be ``None`` if ``available`` is
            ``True``.
        """
        available, unavailable_reason = super(SSHDBFeature, self).check_availability()
        if available:
            license = self.extension.license
            if license.unlicensed or license.in_perpetual_user_mode:
                available = False
                unavailable_reason = _(b'Requires a full license or an active trial of Power Pack.')
            elif not has_valid_sshdb_secret_key():
                available = False
                unavailable_reason = _(b'To enable this feature, a valid SSHDB_SECRET_KEY must be set to a 32-character unguessable string in %s.') % settings_local.__file__.replace(b'.pyc', b'.py')
        return (
         available, unavailable_reason)

    def enable(self):
        """Enable SSH key scalability.

        If this is the first time this has been enabled, this will load
        the existing SSH key into the database, if one is already configured.
        """
        import_keys = not self.extension.settings[b'sshdb_keys_imported']
        success = enable_sshdb(import_keys=import_keys)
        if success and import_keys:
            self.extension.settings[b'sshdb_keys_imported'] = True
            self.extension.settings.save()

    def disable(self):
        """Disable SSH key scalability."""
        disable_sshdb()