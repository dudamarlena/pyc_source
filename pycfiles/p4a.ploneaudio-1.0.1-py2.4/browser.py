# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/p4a/ploneaudio/ataudio/browser.py
# Compiled at: 2007-11-27 08:53:01
import transaction
from zope import component
from p4a.audio.migration import IMigrator
from p4a.ploneaudio.ataudio.interfaces import IATAudio

class ATAudioMigrationView(object):
    """A view for migrating ATAudio content to Plone4ArtistsAudio.
    """
    __module__ = __name__

    @property
    def should_migrate(self):
        return bool(self.request.form.get('migrate', False))

    @property
    def dry_run(self):
        return bool(self.request.form.get('dry_run', True))

    def migrate(self):
        """Invoke the migration mechanism and return a status message.
        """
        migrator = component.getUtility(IMigrator)
        transaction.begin()
        count = migrator.migrate(self.context, IATAudio)
        msg_suffix = ''
        if self.dry_run:
            transaction.abort()
            msg_suffix = ', which were rolled back due to running in "dry run" mode'
        else:
            transaction.commit()
        if count > 0:
            msg = 'Successfully migrated %i object(s)' % count
            msg += msg_suffix
        else:
            msg = 'No objects were migrated'
        return msg

    def __call__(self):
        kwargs = {}
        if self.should_migrate:
            self.request.form['portal_status_message'] = self.migrate()
        return self.index(**kwargs)