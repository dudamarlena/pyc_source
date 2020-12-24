# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/ilrt/migrationtool/browser/interfaces.py
# Compiled at: 2009-05-08 04:37:50
from zope import interface

class IATFieldIndexInfo(interface.Interface):
    """
       Provides info on Archetype fields and their indexes
       plus allows for moving keywords between fields
    """
    __module__ = __name__

    def fieldNameForIndex(self, indexName):
        """The name of the index may not be the same as the field on the object, and we need
           the actual field name in order to find its mutator. 
        """
        pass

    def getListFieldValues(self, obj, indexName):
        """Returns the current values for the given Lines field as a list.
        """
        pass

    def getSetter(self, obj, indexName):
        """Gets the setter function for the field based on the index name.
        """
        pass

    def moveKeyword(self, portal, old_keyword, new_keyword='', old_index='Subject', new_index='heifunction'):
        """Updates all objects using the old_keyword and index to the new ones.
           If no new keyword supplied it deletes the old ones.
           Returns the number of objects that have been updated.
        """
        pass


class IWorkflowMigrationView(interface.Interface):
    """
    Migrates content from one workflow to another via a manually
    tailored mapping implemented as an adjunct to the site migration tool
    """
    __module__ = __name__

    def listWorkflows(self):
        """ Return a list of id,title dictionarys for the workflows available
        """
        pass

    def setWorkflowMigration(self, wf_from, wf_to):
        """
        Set the worflows for the migration
        """
        pass

    def getWorkflowMigration(self):
        """
        Generate the state mapping data for transferring one
        workflow's states to the others
        """
        pass


class ISiteMigrationTool(interface.Interface):
    """Handles migrations between released sites. Adds methods to Plones core IMigrationTool
       Requires a theme egg or other third party product to hold the actual release migrations
    """
    __module__ = __name__

    def setMigration(self, migration_id):
        """ Set the migration object whose method is to be to run individually """
        pass

    def getMigrationMethods(self):
        """ List all the methods for a particular migration object """
        pass

    def runMigrationMethod(self, method):
        """ Run an individual method from a migration object """
        pass

    def registerUpgradePath(self, oldversion, newversion, function):
        """ Basic register func """
        pass

    def registerDowngradePath(self, oldversion, newversion, function):
        """ Basic register func """
        pass

    def getEgg():
        """ Return egg or product id that contains migrations used """
        pass

    def getExtensionContext():
        """ Return extension profile that contains migrations used """
        pass

    def setExtensionContext(context_id):
        """ Set extension profile that contains migrations used
            At this point look up installed instance version if its in quickinstaller
        """
        pass

    def loadMigrations():
        """ Search for migrations based on profile/migration naming convention """
        pass

    def om_icons():
        """ Exclamation icon if the site is not up to date """
        pass

    def needDowngrading(self):
        """ Need downgrading? """
        pass

    def _migrate(version, dirn='up'):
        """ Run the migration """
        pass

    def _upgrade(version):
        """ Run _migrate with dirn up """
        pass


class ISiteMigration(interface.Interface):
    """ The migration itself that calls utility methods e.g. to run generic setup files,
        install products etc. Or can run any bespoke methods if desired
    """
    __module__ = __name__
    migration = interface.Attribute('migration')
    versions = interface.Attribute('versions')

    def upgrade():
        """ Upgrade from 1 to 2 """
        pass

    def downgrade():
        """ Downgrade from 2 to 1 """
        pass