# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/collective/synchro/scripts/import_queue.py
# Compiled at: 2008-12-16 18:21:20
import sys, os, os.path
from tempfile import gettempdir
from optparse import OptionParser
import logging
from utils import lock
from utils import unlock
from utils import is_valid
logger = logging.getLogger('collective.synchro')

def main(args=None):
    parser = OptionParser()
    parser.add_option('-p', '--path', dest='path', help='the path of a synchro queue (required)', default=None)
    parser.add_option('-i', '--instance', dest='instance', help='the path to the instance (in zodb) where data is imported (required)', default=None)
    parser.add_option('-l', '--logdir', dest='logdir', help='log localisation (by default system temp dir)', default=gettempdir())
    parser.add_option('-V', '--vardir', dest='var', help='log localisation (by default system temp dir)', default=gettempdir())
    parser.add_option('-v', '--verbose', dest='verbose', action='store_true', help='log localisation (by default system temp dir)', default=False)
    parser.add_option('-q', '--quiet', dest='quiet', action='store_false', help='print logging message in stdout', default=True)
    (options, args) = parser.parse_args()
    if not options.path or not options.instance:
        parser.print_help()
        sys.exit(-1)
    level = logging.INFO
    if options.verbose and not options.quiet:
        level = logging.DEBUG
    if options.quiet:
        logging.basicConfig(level=level, format='%(asctime)s %(levelname)s %(message)s', filename=os.path.join(options.logdir, 'synchro.log'), filemode='a')
    else:
        logging.basicConfig(level=level)
    lock_file = os.path.join(options.var, 'import.lock')
    lock(lock_file, logger)
    try:
        queue = ImportQueue(options.path, options.instance)
    finally:
        unlock(lock_file)
    return


class ImportQueue(object):
    __module__ = __name__

    def __init__(self, path, instance):
        try:
            try:
                import Zope2 as Zope
            except ImportError:
                import Zope

            app = Zope.app()
            from Testing import makerequest
            app = makerequest.makerequest(app)
        except:
            logger.error('no zodb connexion')
            raise SystemError('You must launch this script with a zeoclient script (zeoclient run <scriptname>...)')

        if is_valid(path):
            from collective.synchro.queues import Queue
            queue = Queue(path)
        else:
            logger.error('%s is incorrect' % path)
            raise SystemError('Please provide a good queue structure')
        try:
            portal = app.unrestrictedTraverse(instance)
            if not hasattr(portal, 'meta_type'):
                raise
            if portal.meta_type != 'Plone Site':
                logger.error('%s is not a plone instance' % instance)
                raise
        except:
            logger.error('%s is not good' % instance)
            raise SystemError('You must be provide an valid plone instance')

        from AccessControl.SecurityManagement import newSecurityManager
        from AccessControl.SecurityManagement import noSecurityManager
        admin_username = 'adminimporter'
        acl_users = app.acl_users
        user = acl_users.getUser(admin_username)
        if user:
            user = user.__of__(acl_users)
            newSecurityManager(None, user)
            logger.info('Retrieved the admin user')
        else:
            acl_users._doAddUser(admin_username, '', ['Manager'], [])
            user = acl_users.getUser(admin_username)
            user = user.__of__(acl_users)
            newSecurityManager(None, user)
            logger.info('Created admin user')
        for file in queue.listQueue('IMPORT', 'TO_PROCESS'):
            queue.importFile(portal, file)

        import transaction
        transaction.commit()
        noSecurityManager()
        return