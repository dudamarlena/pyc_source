# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/oscar/Webs/Python/Peques/src/peques/management/commands/dropbox_download.py
# Compiled at: 2013-04-19 20:25:39
import os, errno, re, sys, time, datetime, gzip, glob
from PIL import Image, ExifTags
from PIL.ExifTags import TAGS
from optparse import make_option
from django.core.management.base import BaseCommand, CommandError
from django.conf import settings as conf
import peques.models as mymodels
from datetime import datetime
from pprint import pprint
from dropbox import client, rest, session

def get_exif(fn):
    """
    data = get_exif('img/2013-04-13 12.17.09.jpg')
    print data

    """
    ret = {}
    i = Image.open(fn)
    info = i._getexif()
    for tag, value in info.items():
        decoded = TAGS.get(tag, tag)
        ret[decoded] = value

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
    help = '\n    Tool that tries to parse the photos, saving it on the database and\n    converting the photos to fit the web:\n\n    ./manage.py parse_photos\n\n    '

    def handle(self, *app_labels, **options):
        """
        The command itself
        """
        APP_KEY = 'ba0nqlc4231mtjq'
        APP_SECRET = '81uj883ozr4ytff'
        ACCESS_TYPE = 'app_folder'
        print os.path.join(conf.PROJECT_DIR, 'media', 'uploads', 'dropbox', 'dropbox_token.txt')
        if not os.path.exists(os.path.join(conf.PROJECT_DIR, 'media', 'uploads', 'dropbox', 'dropbox_token.txt')):
            sess = session.DropboxSession(APP_KEY, APP_SECRET, ACCESS_TYPE)
            request_token = sess.obtain_request_token()
            url = sess.build_authorize_url(request_token)
            print 'url:', url
            print "Please visit this website and press the 'Allow' button, then hit 'Enter' here."
            raw_input()
            access_token = sess.obtain_access_token(request_token)
            TOKENS = os.path.join(conf.PROJECT_DIR, 'media', 'uploads', 'dropbox', 'dropbox_token.txt')
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
        dropboxdir = os.path.join(conf.PROJECT_DIR, 'media', 'uploads', 'dropbox')
        destdir = os.path.join(conf.PROJECT_DIR, 'media', 'uploads', 'photos')
        if os.path.exists(dropboxdir) == False:
            mkdir_p(dropboxdir)
        folder_metadata = c.metadata('/')
        print '-' * 80
        for cont in folder_metadata['contents']:
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

                total += 1

        print '[*** Resumen ***]'
        print '[***] Repetidas en db: %s' % repetidas
        print '[***] Repetidas en disco: %s' % descargadas
        print '[***] Total: %s' % total