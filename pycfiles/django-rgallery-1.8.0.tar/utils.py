# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/oscar/Webs/Python/django-rgallery/rgallery/management/commands/utils.py
# Compiled at: 2015-06-04 09:20:57
import os, io, errno, re
from datetime import datetime
from subprocess import Popen, PIPE
from django.template.defaultfilters import slugify
from django.template import Context, Template
from django.conf import settings as conf
import exifread
from PIL import Image
from PIL import ExifTags
from PIL.ExifTags import TAGS
from sorl.thumbnail import get_thumbnail
from shutil import copyfile
from taggit.models import Tag
from rgallery.engine import expire_view_cache
import rgallery.models as mymodels

def mkdir_p(path):
    try:
        os.makedirs(path)
    except OSError as exc:
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else:
            raise


def namedup(nombre, photodestdir):
    nombre_imagen = '%s%s' % (
     slugify(str(os.path.splitext(nombre)[0]).replace('/', '').replace(' ', '_').replace(':', '-')),
     str(os.path.splitext(nombre)[1]))
    if os.path.exists(os.path.join(photodestdir, nombre_imagen)) == True:
        nombre_imagen = '%s_1%s' % (
         slugify(str(os.path.splitext(nombre)[0]).replace('/', '').replace(' ', '_').replace(':', '-')),
         str(os.path.splitext(nombre)[1]))
        print '       Duped in disk, name changed to: %s' % nombre_imagen
    return nombre_imagen


def img_get_exif(fn):
    """
    data = get_exif('img/2013-04-13 12.17.09.jpg')
    print data
    """
    ret = {}
    i = Image.open(fn)
    if hasattr(i, '_getexif'):
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


def img_get_exif_io(f):
    """
    image = self.request.FILES.getlist('file')[0]
    data = get_exif(image)
    print data
    """
    ret = {}
    f.open('rb')
    buf = io.BytesIO(f.read())
    ret = exifread.process_file(buf)
    try:
        str(ret['DateTimeOriginal'])
    except:
        now = datetime.now()
        ret['DateTimeOriginal'] = now.strftime('%Y:%m:%d %H:%M:%S')

    return ret


def img_rotate(im2):
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

    return im2


def video_get_exif(fn):
    rotate = '0'
    creation = datetime.strftime(datetime.now(), '%Y-%m-%d %H:%M:%S')
    process = Popen([conf.FFPROBE, '-show_streams', str(fn)], stdout=PIPE, stderr=PIPE)
    stdout, stderr = process.communicate()
    for line in iter(stdout.splitlines()):
        if re.search('TAG:rotate', line):
            rotate = line.split('=')[1]
        if re.search('TAG:creation_time', line):
            creation = line.split('=')[1]

    return (
     rotate, creation)


def video_convert(video, file, srcdir, destdir, video_name, rotate):
    try:
        src = file.path
    except:
        src = video

    dst = os.path.join(destdir, video_name)
    thumbname = '%s%s' % (slugify(str(os.path.splitext(os.path.basename(video_name))[0])), '.png')
    thumb = os.path.join(destdir, thumbname)
    rotate, data_video = video_get_exif(dst)
    transpose = ''
    size = conf.FFMPEG_THUMB_SIZE
    if rotate == '90':
        transpose = '-vf "transpose=1"'
        size = conf.FFMPEG_THUMB_SIZE_INVERSE
    grabimage = "%s -y -i '%s' -vframes 1 -ss 00:00:00 -an -vcodec %s -f                  rawvideo -s %s %s %s " % (conf.FFMPEG, src,
     conf.FFMPEG_VCODEC_THUMB,
     size,
     transpose,
     thumb)
    os.system(grabimage)
    try:
        copyfile(src, dst)
    except:
        pass

    return thumbname


def mediasync(file, srcdir, photodestdir, videodestdir, thumbs, backend, client, img_duped, vid_duped, img_total, vid_total, total, tags=''):
    filename = os.path.basename(backend.filepath(file))
    if backend.is_image(file):
        try:
            im = mymodels.Photo.objects.get(origen=filename)
            img_duped += 1
            print '%04d - Duped: %s' % (img_duped, filename)
        except:
            print '%04d - Video %s not in database, downloading, thumbing and adding to database' % (
             total, filename)
            nombre_imagen = namedup(filename, photodestdir)
            img = backend.download(client, file, nombre_imagen, srcdir, photodestdir)
            print '       Saved: %s/%s' % (photodestdir, nombre_imagen)
            data_image = []
            if backend.name() == 'form':
                data_image = img_get_exif_io(file)
                try:
                    capture_data = datetime.strptime(str(data_image['EXIF DateTimeOriginal']), '%Y:%m:%d %H:%M:%S')
                except:
                    capture_data = datetime.now()

            else:
                data_image = img_get_exif(img)
                try:
                    capture_data = datetime.strptime(str(data_image['DateTimeOriginal']), '%Y:%m:%d %H:%M:%S')
                except:
                    capture_data = datetime.now()

            last_photo = mymodels.Photo.objects.order_by('-capture_date')[0]
            if capture_data > last_photo.capture_date:
                im = mymodels.Photo(image='uploads/photos/' + nombre_imagen, origen=filename, insert_date=datetime.now(), capture_date=capture_data, status=True)
                im.save()
                if len(tags) > 0:
                    for tag in tags:
                        try:
                            t = Tag.objects.get(slug=tag)
                            im.tags.add(t)
                        except:
                            im.tags.add(tag)

                im.save()
                img_total += 1
                print '       Added to database (%s)' % im.origen
                im2 = Image.open(img)
                im2 = img_rotate(im2)
                im2.save(os.path.join(photodestdir, nombre_imagen))
                for thumb in thumbs:
                    print '       Thumb %sx%s' % (thumb, thumb)
                    c = Context({'image': im, 'thumb': '%sx%s' % (thumb,
                               thumb)})
                    t = Template('{% load thumbnail %}{% thumbnail image thumb\n                                  crop="top" as img %}{{ img.url }}\n                                  {% endthumbnail %}')
                    t.render(c)
                    get_thumbnail(im, '%sx%s' % (thumb, thumb))

            else:
                print '       Image capture date (%s) is lower thanlast image date (%s)' % (
                 capture_data,
                 last_photo.capture_date)

    if backend.is_video(file):
        try:
            im = mymodels.Photo.objects.get(origen=filename)
            vid_duped += 1
            print '%04d - Duped: %s' % (vid_duped, filename)
        except:
            print '%04d - Video %s not in database, downloading,thumbing and adding to database' % (
             total, filename)
            video_name = namedup(filename, videodestdir)
            video = backend.download(client, file, video_name, srcdir, videodestdir)
            print '       Saved: %s/%s' % (videodestdir, video_name)
            rotate, data_video = video_get_exif(video)
            capture_data = datetime.strptime(str(data_video), '%Y-%m-%d %H:%M:%S')
            thumbname = video_convert(video, file, srcdir, videodestdir, video_name, rotate)
            vid = mymodels.Photo(title=capture_data, image='uploads/videos/' + thumbname, video='uploads/videos/' + video_name, origen=filename, insert_date=datetime.now(), capture_date=capture_data, status=True)
            vid.save()
            if len(tags) > 0:
                for tag in tags:
                    try:
                        t = Tag.objects.get(slug=tag)
                        vid.tags.add(t)
                    except:
                        vid.tags.add(tag)

            vid.save()
            vid_total += 1
            print '       Added to database (%s)' % vid.origen
            for thumb in thumbs:
                print '       Thumb %sx%s' % (thumb, thumb)
                get_thumbnail(vid.image, '%sx%s' % (thumb, thumb))

    total += 1
    return (
     img_duped, img_total, vid_duped, vid_total, total)