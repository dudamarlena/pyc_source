# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/oscar/Webs/Python/django-rgallery/rgallery/management/commands/parse_photos.py
# Compiled at: 2013-07-15 15:52:21
import os, errno, re, sys, time, datetime, gzip, glob
from PIL import Image, ExifTags
from PIL.ExifTags import TAGS
from optparse import make_option
from django.core.management.base import BaseCommand, CommandError
from django.conf import settings as conf
import rgallery.models as mymodels
from datetime import datetime

def mkdir_p(path):
    try:
        os.makedirs(path)
    except OSError as exc:
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else:
            raise


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


class Command(BaseCommand):
    help = '\n    Tool that tries to parse the photos, saving it on the database and\n    converting the photos to fit the web:\n\n    ./manage.py parse_photos\n\n    '

    def handle(self, *app_labels, **options):
        """
        The command itself
        """
        size = (1000, 1000)
        datadir = os.path.join(conf.PROJECT_DIR, 'media', 'uploads', 'gallery')
        destdir = os.path.join(conf.PROJECT_DIR, 'media', 'uploads', 'photos')
        mkdir_p(destdir)
        total = 0
        repetidas = 0
        repetidas_disco = 0
        print datadir
        for image in glob.glob(datadir + '/*.jpg'):
            data_image = get_exif(image)
            try:
                capture_data = datetime.strptime(str(data_image['DateTimeOriginal']), '%Y:%m:%d %H:%M:%S')
            except:
                capture_data = datetime.strptime(str(data_image['DateTime']), '%Y:%m:%d %H:%M:%S')

            try:
                im = mymodels.Photo.objects.get(origen=os.path.basename(image))
                repetidas += 1
                print '[***] La imagen ya existe en bbdd: %s' % os.path.basename(image)
            except:
                nombre_imagen = str(capture_data).replace(' ', '_').replace(':', '-') + '.jpg'
                print '[***] Nueva imagen: %s' % nombre_imagen
                im = mymodels.Photo(image='uploads/photos/' + nombre_imagen, origen=os.path.basename(image), insert_date=datetime.now(), capture_date=capture_data, status=True)
                im.save()
                print '      Agregada a bbdd'
                im2 = Image.open(image)
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
                    repetidas_disco += 1
                    nombre_imagen_repe = str(capture_data).replace(' ', '_').replace(':', '-') + '_1.jpg'
                    im.image = 'uploads/photos/' + nombre_imagen_repe
                    im.save()
                    im2.save(destdir + '/' + nombre_imagen_repe)
                    print '      Duplicada en disco, cambiado nombre a: %s' % nombre_imagen_repe

            total += 1

        print '[*** Resumen ***]'
        print '[***] Repetidas en db: %s' % repetidas
        print '[***] Repetidas en disco: %s' % repetidas_disco
        print '[***] Total: %s' % total