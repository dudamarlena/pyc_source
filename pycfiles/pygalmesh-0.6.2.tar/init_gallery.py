# uncompyle6 version 3.6.7
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/pyGallerid/scripts/init_gallery.py
# Compiled at: 2012-01-31 10:40:19
__doc__ = '\nScript for initializing the pyGallerid database.\n'
import os, sys
from pyramid_zodbconn import db_from_uri
import transaction
from pyramid.paster import get_appsettings, setup_logging
from ..models import appmaker, retrieve_user, retrieve_gallery, retrieve_about
from ..models.user import User
from ..models.gallery import Gallery, GalleryDocument

def usage(argv):
    cmd = os.path.basename(argv[0])
    print 'usage: %s <config_uri> <username> <email> <password> [<description>]\n(example: "%s development.ini myname mymail@mydomain.com qwerty)' % (
     cmd, cmd)
    sys.exit(1)


def main(argv=sys.argv):
    if len(argv) < 5:
        usage(argv)
    config_uri = argv[1]
    username = argv[2]
    email = argv[3]
    password = argv[4]
    if len(argv) > 5:
        description = argv[5]
    else:
        description = "Benjamin Hepp's Photography"
    setup_logging(config_uri)
    settings = get_appsettings(config_uri)
    db = db_from_uri(settings['zodbconn.uri'])
    conn = db.open()
    zodb_root = conn.root()
    with transaction.manager:
        create_gallery(zodb_root, settings, username, email, password, description)
        transaction.commit()


def create_gallery(zodb_root, settings, username, email, password, description):
    app = appmaker(zodb_root)
    user = retrieve_user(app, username)
    if user is not None:
        raise ValueError('A user with name %s already exists' % username)
    user = User(username, email, password)
    app.add(user)
    gallery = retrieve_gallery(user)
    if gallery is not None:
        raise ValueError('The user %s already has a gallery' % username)
    gallery = Gallery(description, user=user, path=settings['image_dir'])
    user.add(gallery)
    about = retrieve_about(user)
    if about is not None:
        raise ValueError('The user %s already has an about page' % username)
    about = GalleryDocument('about', 'About', 'Description')
    user.add(about)
    return