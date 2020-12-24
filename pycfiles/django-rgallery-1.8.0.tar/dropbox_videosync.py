# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/oscar/Webs/Python/django-rgallery/rgallery/management/commands/dropbox_videosync.py
# Compiled at: 2013-07-15 16:15:06
import os, errno, re, sys, time, datetime, gzip, glob
from hachoir_core.error import HachoirError
from hachoir_core.cmd_line import unicodeFilename
from hachoir_parser import createParser
from hachoir_core.tools import makePrintable
from hachoir_metadata import extractMetadata
from hachoir_core.i18n import getTerminalCharset
from shutil import copyfile
from optparse import make_option
from django.core.management.base import BaseCommand, CommandError
from django.conf import settings as conf
import rgallery.models as mymodels
from datetime import datetime
from pprint import pprint
from dropbox import client, rest, session

def get_exif(fn):
    """
    data = get_exif('img/2013-04-13 12.17.09.jpg')
    print data
    """
    filename = fn
    filename, realname = unicodeFilename(filename), filename
    parser = createParser(filename, realname)
    if not parser:
        print '[EEE] No puedo parsear %s' % filename
        exit(1)
    try:
        metadata = extractMetadata(parser)
    except HachoirError as err:
        print '[EEE] Metadata extraction error: %s' % unicode(err)
        metadata = None

    if not metadata:
        print '[EEE] Unable to extract metadata'
        exit(1)
    text = metadata.exportPlaintext()
    charset = getTerminalCharset()
    for line in text:
        mes = makePrintable(line, charset)
        if 'Creation date' in mes:
            return mes.split(': ')[1]

    return


def mkdir_p(path):
    try:
        os.makedirs(path)
    except OSError as exc:
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else:
            raise


class Command(BaseCommand):
    help = '\n    Tool that tries to download and parse photos from a Dropbox shared folder,\n    saving it on the database and converting the photos to fit the web:\n\n    ./manage.py dropbox_videosync\n\n    1.- First time it connects with Dropbox and stores the token information in\n        a token_file\n    2.- Next times it read the token from file to connect Dropbox\n    3.- Go to the shared folder and check if the image is already on database\n    4.- If not, this script download the image, converting it to fit the web and\n        save a record in the database.\n\n    To run this script from a crontab task we should do something like this:\n\n    */30 * * * * cd /path/to/rgallery-project/ ; source env/bin/activate ; cd src ; python manage.py dropbox_videosync > /dev/null\n\n    '

    def handle(self, *app_labels, **options):
        """
        The command itself
        """
        APP_KEY = conf.DROPBOX_APP_KEY
        APP_SECRET = conf.DROPBOX_APP_SECRET
        ACCESS_TYPE = 'dropbox'
        dropboxdir = os.path.join(conf.PROJECT_DIR, 'media', 'uploads', 'dropbox')
        destdir = os.path.join(conf.PROJECT_DIR, 'media', 'uploads', 'videos')
        photosvideos = os.path.join(conf.PROJECT_DIR, 'media', 'uploads', 'photos_videos')
        if os.path.exists(dropboxdir) == False:
            mkdir_p(dropboxdir)
        if os.path.exists(destdir) == False:
            mkdir_p(destdir)
        if os.path.exists(photosvideos) == False:
            mkdir_p(photosvideos)
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
        folder_metadata = c.metadata('/Web/')
        print '-' * 80
        for cont in folder_metadata['contents']:
            try:
                str(cont['mime_type'])
            except:
                cont['mime_type'] = ''

            if cont['mime_type'] == 'video/mp4' or cont['mime_type'] == 'video/3gpp':
                origen_name = os.path.basename(cont['path'])
                print 'origen_name=%s' % origen_name
                try:
                    im = mymodels.Video.objects.get(origen=os.path.basename(cont['path']))
                    repetidas += 1
                    print '[***] Repetido: %s' % os.path.basename(cont['path'])
                except:
                    print '[***] El video %s No esta en bd, descargar y agregar a bbdd y hacer thumb' % os.path.basename(cont['path'])
                    nombre_imagen = str(cont['path']).replace('/', '').replace(' ', '_').replace(':', '-')
                    f, metadata = c.get_file_and_metadata(cont['path'])
                    out = open(dropboxdir + '/' + nombre_imagen, 'wb')
                    out.write(f.read())
                    out.close()
                    print '      [i] Descargado'
                    data_image = get_exif(dropboxdir + '/' + nombre_imagen)
                    print '      [i] Nombre imagen: %s' % nombre_imagen
                    print '      [i] Exif data: %s' % data_image
                    video_filepath = conf.MEDIA_ROOT + '/uploads/dropbox/' + nombre_imagen
                    video_filepath_final = conf.MEDIA_ROOT + '/uploads/videos/' + nombre_imagen
                    video_filepath_final_url = conf.MEDIA_URL + 'uploads/videos/' + nombre_imagen
                    video_thumbfile = conf.MEDIA_ROOT + '/uploads/photos_videos/' + nombre_imagen + '.png'
                    video_thumbfile_url = 'uploads/photos_videos/' + nombre_imagen + '.png'
                    print '      [i] thumbfile: %s' % video_thumbfile
                    print '      [i] thumburl: %s' % video_thumbfile_url
                    ZERO14_FFMPEG = '/opt/local/bin/ffmpeg'
                    ZERO14_FFMPEG_VCODEC_THUMB = 'png'
                    ZERO14_FFMPEG_THUMB_SIZE = '320x240'
                    grabimage = '%s -y -i %s -vframes 1 -ss 00:00:02 -an -vcodec %s -f rawvideo -s %s %s ' % (ZERO14_FFMPEG, video_filepath,
                     ZERO14_FFMPEG_VCODEC_THUMB,
                     ZERO14_FFMPEG_THUMB_SIZE,
                     video_thumbfile)
                    os.system(grabimage)
                    copyfile(video_filepath, video_filepath_final)
                    capture_data = datetime.strptime(str(data_image), '%Y-%m-%d %H:%M:%S')
                    vid = mymodels.Video(title=capture_data, image=video_thumbfile_url, video=video_filepath_final_url, origen=os.path.basename(cont['path']), insert_date=datetime.now(), capture_date=capture_data, status=True)
                    vid.save()
                    print '      Agregado a bbdd'

                total += 1

        print '[*** Resumen ***]'
        print '[***] Repetidos en db: %s' % repetidas
        print '[***] Repetidos en disco: %s' % descargadas
        print '[***] Total: %s' % total