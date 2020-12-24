# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/oscar/Webs/Python/django-rgallery/rgallery/management/commands/dropbox_photosync.py
# Compiled at: 2014-04-28 05:14:40
import os, errno, re, sys, time, datetime, gzip, glob, Image, ExifTags
from ExifTags import TAGS
from optparse import make_option
from django.core.management.base import BaseCommand, CommandError
from django.conf import settings as conf
import rgallery.models as mymodels
from datetime import datetime
from pprint import pprint
from sorl.thumbnail import get_thumbnail
from dropbox import client, rest, session

def get_exif(fn):
    """
    data = get_exif('img/2013-04-13 12.17.09.jpg')
    print data
    """
    ret = {}
    print fn
    i = Image.open(fn)
    info = i._getexif()
    try:
        for tag, value in info.items():
            decoded = TAGS.get(tag, tag)
            ret[decoded] = value

    except:
        now = datetime.now()
        ret['DateTimeOriginal'] = now.strftime('%Y:%m:%d %H:%M:%S')

    try:
        str(ret['DateTimeOriginal'])
    except:
        now = datetime.now()
        ret['DateTimeOriginal'] = now.strftime('%Y:%m:%d %H:%M:%S')

    return ret


def mkdir_p(path):
    try:
        os.makedirs(path)
    except OSError as exc:
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else:
            raise


class Command(BaseCommand):
    help = '\n    Tool that tries to download and parse photos from a Dropbox shared folder,\n    saving it on the database and converting the photos to fit the web:\n\n    ./manage.py dropbox_photosync\n\n    1.- First time it connects with Dropbox and stores the token information in\n        a token_file\n    2.- Next times it read the token from file to connect Dropbox\n    3.- Go to the shared folder and check if the image is already on database\n    4.- If not, this script download the image, converting it to fit the web and\n        save a record in the database.\n\n    To run this script from a crontab task we should do something like this:\n\n    */30 * * * * cd /path/to/rgallery-project/ ; source env/bin/activate ; cd src ; python manage.py dropbox_photosync > /dev/null\n\n    '

    def handle(self, *app_labels, **options):
        """
        The command itself
        """
        APP_KEY = conf.DROPBOX_APP_KEY
        APP_SECRET = conf.DROPBOX_APP_SECRET
        try:
            ACCESS_TYPE = conf.DROPBOX_ACCESS_TYPE
        except:
            ACCESS_TYPE = 'dropbox'

        dropboxdir = os.path.join(conf.PROJECT_DIR, 'media', 'uploads', 'dropbox')
        destdir = os.path.join(conf.PROJECT_DIR, 'media', 'uploads', 'photos')
        if os.path.exists(dropboxdir) == False:
            mkdir_p(dropboxdir)
        if os.path.exists(destdir) == False:
            mkdir_p(destdir)
        TOKENS = os.path.join(conf.PROJECT_DIR, 'media', 'uploads', 'dropbox', 'dropbox_token.txt')
        if not os.path.exists(TOKENS):
            sess = session.DropboxSession(APP_KEY, APP_SECRET, ACCESS_TYPE)
            request_token = sess.obtain_request_token()
            url = sess.build_authorize_url(request_token)
            print 'url:', url
            print "Please visit this website and press the 'Allow' button, then hit 'Enter' here."
            raw_input()
            access_token = sess.obtain_access_token(request_token)
            token_file = open(TOKENS, 'w')
            token_file.write('%s|%s' % (access_token.key, access_token.secret))
            token_file.close()
        else:
            token_file = open(TOKENS)
            token_key, token_secret = token_file.read().split('|')
            token_file.close()
            sess = session.DropboxSession(APP_KEY, APP_SECRET, ACCESS_TYPE)
            sess.set_token(token_key, token_secret)
        c = client.DropboxClient(sess)
        repetidas = 0
        descargadas = 0
        total = 0
        size = (1000, 1000)
        try:
            DROPBOX_PATH = conf.DROPBOX_ACCESS_PATH
        except:
            DROPBOX_PATH = '/'

        folder_metadata = c.metadata(DROPBOX_PATH)
        print '-' * 80
        for cont in folder_metadata['contents']:
            print cont

        for cont in folder_metadata['contents']:
            try:
                str(cont['mime_type'])
            except:
                cont['mime_type'] = ''

            if cont['mime_type'] == 'image/jpeg':
                origen_name = os.path.basename(cont['path'])
                try:
                    im = mymodels.Photo.objects.get(origen=os.path.basename(cont['path']))
                    repetidas += 1
                    print '[***] Repetida: %s' % os.path.basename(cont['path'])
                except:
                    print '[***] La imagen %s No esta en bd, descargar y agregar a bbdd y hacer thumb' % os.path.basename(cont['path'])
                    nombre_imagen = str(cont['path']).replace('/', '').replace(' ', '_').replace(':', '-')
                    f, metadata = c.get_file_and_metadata(cont['path'])
                    out = open(dropboxdir + '/' + nombre_imagen, 'wb')
                    out.write(f.read())
                    out.close()
                    print '      Descargada'
                    data_image = get_exif(dropboxdir + '/' + nombre_imagen)
                    capture_data = datetime.strptime(str(data_image['DateTimeOriginal']), '%Y:%m:%d %H:%M:%S')
                    im = mymodels.Photo(image='uploads/photos/' + nombre_imagen, origen=os.path.basename(cont['path']), insert_date=datetime.now(), capture_date=capture_data, status=True)
                    im.save()
                    print '      Agregada a bbdd'
                    im2 = Image.open(dropboxdir + '/' + nombre_imagen)
                    try:
                        for orientation in ExifTags.TAGS.keys():
                            if ExifTags.TAGS[orientation] == 'Orientation':
                                break

                        exif = dict(im2._getexif().items())
                        if exif[orientation] == 3:
                            im2 = im2.rotate(180, expand=True)
                        elif exif[orientation] == 6:
                            im2 = im2.rotate(270, expand=True)
                        elif exif[orientation] == 8:
                            im2 = im2.rotate(90, expand=True)
                    except:
                        pass

                    im2.thumbnail(size, Image.ANTIALIAS)
                    if os.path.exists(destdir + '/' + nombre_imagen) == False:
                        im2.save(destdir + '/' + nombre_imagen)
                        print '      Thumbnail en: %s/%s' % (destdir, nombre_imagen)
                    else:
                        descargadas += 1
                        nombre_imagen_repe = str(cont['path']).replace('/', '').replace(' ', '_').replace(':', '-').replace('.jpg', '') + '_1.jpg'
                        im.image = 'uploads/photos/' + nombre_imagen_repe
                        im.save()
                        im2.save(destdir + '/' + nombre_imagen_repe)
                        print '      Duplicada en disco, cambiado nombre a: %s' % nombre_imagen_repe
                    print 'Haciendo thumb 200x200'
                    im = get_thumbnail(im, '200x200')
                    print 'Haciendo thumb 800x800'
                    im = get_thumbnail(im, '800x800')

                total += 1

        print '[*** Resumen ***]'
        print '[***] Repetidas en db: %s' % repetidas
        print '[***] Repetidas en disco: %s' % descargadas
        print '[***] Total: %s' % total
        print '[***] Haciendo thumbs (200x200 y 800x00) de las que no tienen todavía'
        allphotos = mymodels.Photo.objects.all()
        for p in allphotos:
            im = get_thumbnail(p, '200x200')
            im = get_thumbnail(p, '800x800')

        print '[***] Hecho.'