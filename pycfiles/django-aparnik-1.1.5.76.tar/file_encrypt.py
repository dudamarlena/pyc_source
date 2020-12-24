# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ali/ownCloud/Project/python/django-aparnik-framework-project/testandbuildprojectframework/aparnik/contrib/filefields/management/commands/file_encrypt.py
# Compiled at: 2019-05-11 05:36:48
from __future__ import unicode_literals
from django.core.management import BaseCommand
from django.utils.timezone import now
from dateutil.relativedelta import relativedelta
import subprocess, magic, string, random, json, os
from pyPdf import PdfFileWriter, PdfFileReader
from aparnik.utils.utils import round
from aparnik.contrib.filefields.models import FileField
from aparnik.packages.educations.courses.models import CourseFile

def randomPasswordAndIV():
    """Generate a random password """
    password = b''
    iv = b''
    for i in range(64):
        password += random.choice(string.hexdigits)

    for i in range(32):
        iv += random.choice(string.hexdigits)

    return (
     password.lower(), iv.lower())


class Command(BaseCommand):
    help = b'Encrypt File fields'

    def handle(self, *args, **options):
        start_time = now()
        queryset = FileField.objects.filter(is_lock=True)
        for file in queryset:
            if not file.file_direct.storage.exists(file.file_direct.name):
                continue
            path = file.file_direct.path
            infile = path
            outfile = b'%s.enc' % path
            if file.is_decrypt_needed:
                if file.type == FileField.FILE_PDF:
                    with open(infile, b'rb') as (ifile):
                        with open(outfile, b'wb') as (ofile):
                            reader = PdfFileReader(ifile)
                            print str(file.password)
                            if reader.isEncrypted:
                                reader.decrypt(unicode(b'1da72c67efb2ccdcf43fef8c6afacdd405659effaadcdae31cabb2ead8df43ab'))
                            writer = PdfFileWriter()
                            for i in range(reader.getNumPages()):
                                writer.addPage(reader.getPage(i))

                            writer.write(ofile)
                else:
                    subprocess.call(b'openssl enc -aes-256-cbc -d -nosalt -K %s -iv %s -in %s -out %s' % (
                     file.password, file.iv, infile, outfile), shell=True, close_fds=True)
                os.remove(path)
                os.rename(outfile, infile)
                file.is_decrypt_needed = False
                file.password = None
                file.iv = None
            else:
                f = magic.Magic(mime=True, uncompress=False)
                mime = f.from_file(path)
                file.type = file.detect_mime_type(mime)
                if not file.type:
                    f = magic.Magic()
                    mime = f.from_file(path)
                    file.type = file.detect_by_readable_description(mime)
                if not file.type:
                    continue
                if file.type == FileField.FILE_VOICE or file.type == FileField.FILE_MOVIE:
                    ffprobe_properties = b"ffprobe -i '%s' -v quiet -print_format json -show_format -hide_banner" % path
                    metadata = subprocess.check_output(ffprobe_properties, shell=True, close_fds=True)
                    metadata = json.loads(metadata)
                    if b'duration' in metadata[b'format']:
                        duration = metadata[b'format'][b'duration']
                        file.seconds = int(round(duration))
                        for f in file.shop_file_obj.all():
                            if isinstance(f, CourseFile):
                                f.seconds = file.seconds
                                f.save()

                    else:
                        continue
                if file.is_encrypt_needed:
                    key, iv = randomPasswordAndIV()
                    if file.type == FileField.FILE_PDF:
                        iv = None
                        with open(infile, b'rb') as (ifile):
                            with open(outfile, b'wb') as (ofile):
                                reader = PdfFileReader(ifile)
                                writer = PdfFileWriter()
                                for i in range(reader.getNumPages()):
                                    writer.addPage(reader.getPage(i))

                                writer.encrypt(str(key))
                                writer.write(ofile)
                    else:
                        subprocess.call(b'openssl enc -aes-256-cbc -nosalt -K %s -iv %s -in %s -out %s' % (key, iv, infile, outfile), shell=True, close_fds=True)
                    os.remove(path)
                    os.rename(outfile, infile)
                    file.password = key
                    file.iv = iv
            file.is_lock = False
            file.save()

        finished_time = now()
        print b'encrypt done %s - time long: %ss.' % (now(), relativedelta(finished_time, start_time).seconds)
        return