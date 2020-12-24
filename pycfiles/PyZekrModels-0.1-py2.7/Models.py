# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/PyZekrModels/Models.py
# Compiled at: 2012-12-29 05:02:46
"""
Created on 22 avr. 2010

@author: Assem Chelli
@contact: Assem.ch [at] gmail.com
@license: AGPL
"""
import os.path, re
from zipfile import ZipFile

class Ta7rif(Exception):
    """ raise when an error in Holy Quran text

    example:
    ========
        >>> raise Ta7rif(type="new",value=u"ابراهام",original="ابراهيم",aya_gid=0,msg="word changed")

    @param type:type of ta7rif
    @type type:string
    @param value:value of ta7rif
    @type value:unicode
    @param original:the original value
    @type original:unicode
    @param aya_gid:the general id of aya
    @type aya_gid:int
    @param msg:the message of error
    @type msg:unicode

    TODO: some translations can't be loaded cause a problem of ascii

    """

    def __init__(self, type='new', value='undefined', original=None, aya_gid=None, msg=''):
        self.type = type
        self.aya_gid = aya_gid
        self.value = value
        self.original = original
        self.msg = msg

    def __str__(self):
        return '\nTa7rif in Holy Quran :\n\tType:' + str(self.type) + '\n\tvalue:' + str(self.value) + '\n\toriginalvalue:' + str(self.original) + '\n\taya_gid:' + str(self.aya_gid) + '\n\n' + str(self.msg)


class TranslationModel:
    """ Translation Modelz reader

        @author: Assem Chelli
        @contact: Assem.ch [at] gmail.com
        @license: AGPL

        """

    def __init__(self, path='./example.zip'):
        """
            @param path:the path of model directory or zip file
            @attention: add the last slash for directories
            """
        print path
        assert os.path.exists(path), 'path does not exist!!'
        if os.path.isfile(path):
            self.path = self.open_zip(path)
        else:
            assert False, 'type of path is not defined : %s' % path

    def open_zip(self, zip, temp='/tmp/alfanous/'):
        """ """
        ZF = ZipFile(zip)
        if not os.path.exists(temp):
            os.mkdir(temp)
        ZF.extractall(temp)
        return temp

    def translation_properties(self):
        """ get the properties of the translation """
        tpfile = open(self.path + 'translation.properties', 'r')
        wordrx = re.compile('[^=\r\n#]+')
        D = {}
        for line in tpfile.readlines():
            res = wordrx.findall(line)
            if len(res) == 2:
                D[res[0]] = res[1]

        return D

    def translation_lines(self, props):
        """ return the lines list of translation """
        tfile = open(self.path + props['file'], 'r')
        linerx = re.compile('[^' + props['lineDelimiter'] + ']+')
        return linerx.findall(tfile.read())

    def document_list(self):
        """ a generator of documents
            @attention: raise a ta7rif exception if the number of lines is not 6236
            """
        props = self.translation_properties()
        lines = self.translation_lines(props)
        if len(lines) != 6236:
            raise Ta7rif(type='ayas number', value=str(len(lines)), original='6236', msg='the number of lines is not 6236')
        for i in range(6236):
            doc = {'gid': i + 1, 'id': props['id'].decode(props['encoding']), 'text': lines[i].decode(props['encoding']), 'type': 'translation', 'lang': props['language'].decode(props['encoding']), 'country': props['country'].decode(props['encoding']), 'author': props['name'].decode(props['encoding']), 'copyright': props['copyright'].decode(props['encoding']), 'binary': None}
            yield doc

        return


if __name__ == '__main__':
    TM = TranslationModel('./example.zip')
    props = TM.translation_properties()