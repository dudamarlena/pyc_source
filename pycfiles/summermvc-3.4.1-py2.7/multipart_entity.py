# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/summermvc/mvc/multipart_entity.py
# Compiled at: 2018-05-30 09:09:26
__all__ = [
 'MultipartParser']
__authors__ = ['Tim Chow']

class MultipartParser(object):

    def __init__(self, content, boundary):
        self._content = content
        self._boundary = '--' + boundary
        self._files = self.__parse()

    def __parse(self):
        parts = {}
        files = self._content.split(self._boundary)[1:-1]
        for file in files:
            part = {}
            phrases = file.split('\r\n')
            for ind, meta in enumerate(phrases[1:-1], start=1):
                if meta == '':
                    break
                pair = meta.split(':', 1)
                if len(pair) != 2:
                    continue
                part[pair[0].strip()] = pair[1].strip()

            cd = part.pop('Content-Disposition', '')
            for item in cd.split(';')[1:]:
                pair = item.split('=', 1)
                if len(pair) != 2:
                    continue
                part[pair[0].strip()] = pair[1].strip(' "')

            if 'name' in part:
                part['content'] = ('\r\n').join(phrases[ind + 1:-1])
                parts[part['name']] = part

        return parts

    @property
    def files(self):
        return self._files


if __name__ == '__main__':
    boundary = 'form_boundary'
    content = ('--{0}\r\nContent-Disposition: form-data; name="file1"; filename="file1.txt"\r\nContent-Type: text/plain\r\n\r\nthis is file1.txt\r\n--{0}\r\nContent-Disposition: form-data; name="file2"; filename="file2.txt"\r\nContent-Type: text/plain\r\n\r\n\r\nthis\r\nis\r\nfile2.txt\r\n\r\n--{0}--').format(boundary)
    multipart_entity = MultipartParser(content, boundary)
    print multipart_entity.files