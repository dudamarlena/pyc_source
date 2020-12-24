# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ali/ownCloud/Project/python/django-aparnik-framework-project/testandbuildprojectframework/aparnik/contrib/filefields/management/commands/file_encrypt.py
# Compiled at: 2019-07-01 06:23:10
# Size of source mod 2**32: 6148 bytes
from django.core.management import BaseCommand
from django.utils.timezone import now
import dateutil.relativedelta as relativedelta
import subprocess, string, random, json, os
from PyPDF2 import PdfFileWriter, PdfFileReader
from aparnik.utils.utils import round
from aparnik.contrib.filefields.models import FileField
from aparnik.packages.educations.courses.models import CourseFile

def randomPasswordAndIV():
    """Generate a random password """
    password = ''
    iv = ''
    for i in range(64):
        password += random.choice(string.hexdigits)

    for i in range(32):
        iv += random.choice(string.hexdigits)

    return (
     password.lower(), iv.lower())


class Command(BaseCommand):
    help = 'Encrypt File fields'

    def handle(self, *args, **options):
        start_time = now()
        queryset = FileField.objects.encrypt_needed()
        for file in queryset:
            if not file.type:
                continue
            path = file.file_direct.path
            infile = path
            outfile = '%s.enc' % path
            if file.is_decrypt_needed:
                if file.type == FileField.FILE_PDF:
                    continue
                else:
                    subprocess.call(('openssl enc -aes-256-cbc -d -nosalt -K %s -iv %s -in %s -out %s' % (
                     file.password, file.iv, infile, outfile)),
                      shell=True,
                      close_fds=True)
                    if file.multi_quality:
                        path2 = '%s%s' % (file.file_direct.path, file.file_another_quality)
                        infile2 = path2
                        outfile2 = '%s.enc' % path2
                        subprocess.call(('openssl enc -aes-256-cbc -d -nosalt -K %s -iv %s -in %s -out %s' % (
                         file.password, file.iv, infile2, outfile2)),
                          shell=True,
                          close_fds=True)
                        os.remove(path2)
                        os.rename(outfile2, infile2)
                os.remove(path)
                os.rename(outfile, infile)
                file.is_decrypt_needed = False
                file.password = None
                file.iv = None
            elif not file.type:
                file.find_type()
                if not file.type:
                    continue
            if not file.type == FileField.FILE_VOICE:
                if file.type == FileField.FILE_MOVIE:
                    ffprobe_properties = "ffprobe -i '%s' -v quiet -print_format json -show_format -hide_banner" % path
                    metadata = subprocess.check_output(ffprobe_properties,
                      shell=True,
                      close_fds=True)
                    metadata = json.loads(metadata)
                    if 'duration' in metadata['format']:
                        duration = metadata['format']['duration']
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
                            with open(infile, 'rb') as (ifile):
                                with open(outfile, 'wb') as (ofile):
                                    reader = PdfFileReader(ifile)
                                    writer = PdfFileWriter()
                                    for i in range(reader.getNumPages()):
                                        writer.addPage(reader.getPage(i))

                                    writer.encrypt(str(key))
                                    writer.write(ofile)
                        else:
                            subprocess.call(('openssl enc -aes-256-cbc -nosalt -K %s -iv %s -in %s -out %s' % (key, iv, infile, outfile)), shell=True, close_fds=True)
                            if file.multi_quality:
                                path2 = '%s%s' % (file.file_direct.path, file.file_another_quality)
                                infile2 = path2
                                outfile2 = '%s.enc' % path2
                                subprocess.call(('openssl enc -aes-256-cbc -nosalt -K %s -iv %s -in %s -out %s' % (
                                 key, iv, infile2, outfile2)),
                                  shell=True, close_fds=True)
                                os.remove(path2)
                                os.rename(outfile2, infile2)
                            os.remove(path)
                            os.rename(outfile, infile)
                        file.password = key
                        file.iv = iv
                file.is_lock = False
                file.save()

        finished_time = now()
        print('encrypt done %s - time long: %ss.' % (now(), relativedelta(finished_time, start_time).seconds))