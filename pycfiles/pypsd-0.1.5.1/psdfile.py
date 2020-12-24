# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Work\Python\workplace\pypsd\pypsd\psdfile.py
# Compiled at: 2009-08-18 12:33:12
import os, unicodedata, string, logging, logging.config
from sections import *
logging.config.fileConfig('%s/conf/logging.conf' % os.path.dirname(__file__))
validFilenameChars = '-_.() %s%s' % (string.ascii_letters, string.digits)

def make_valid_filename(path, layer_name, layer_id):
    old_layer_name = layer_name
    if type(layer_name) == str:
        layer_name = layer_name.decode()
    cleanedFilename = unicodedata.normalize('NFKD', layer_name).encode('ASCII', 'ignore')
    layer_name = ('').join((c for c in cleanedFilename if c in validFilenameChars))
    path = path[::-1].replace(old_layer_name[::-1], layer_name[::-1], 1)[::-1]
    if os.path.exists(path) or cleanedFilename == '':
        layer_name += str(layer_id)
    return layer_name


def normAbsPath(path):
    return os.path.abspath(os.path.normcase(path))


class PSDFile(object):
    """
        Main class. Contains all information about PSD file.
        The file format for Photoshop 3.0 is divided into five major parts.
        - File Header
        - Color Mode Data
        - Image Resources
        - Layer and Mask Information
        - Image Data
        """

    def __init__(self, fileName=None, stream=None):
        import psyco
        psyco.profile()
        self.logger = logging.getLogger('pypsd.psdfile.PSDFile')
        self.logger.debug('__init__ method. In: fileName=%s' % fileName)
        self.stream = stream
        self.fileName = fileName
        self.header = None
        self.colorMode = None
        self.imageResources = None
        self.layerMask = None
        self.imageData = None
        return

    def parse(self):
        """
                Parse PDF file and fill all self field.
                """
        if not self.stream:
            if self.fileName is None:
                raise BaseException('File Name not specified.')
            if not os.path.exists(self.fileName):
                raise IOError("Can't find file specified.")
        try:
            if not self.stream:
                stream = open(self.fileName, mode='rb')
            else:
                stream = self.stream
            stream.seek(0, 2)
            streamsize = stream.tell()
            stream.seek(0)
            self.logger.debug('File size is: %d bytes' % streamsize)
            self.header = PSDHeader(stream, self)
            self.logger.debug('Header:\n%s' % self.header)
            self.colorMode = PSDColorMode(stream, self)
            self.logger.debug('Color mode:%s' % self.colorMode)
            self.imageResources = PSDImageResources(stream, self)
            self.logger.debug('Image Resources:%s' % self.imageResources)
            self.layerMask = PSDLayerMask(stream, self)
            self.logger.debug('Layer Masks:%s' % self.layerMask)
            self.layerMask.groupLayers()
            for l in self.layerMask.layers:
                if l.is_base_layer:
                    self.logger.debug("Layer 'Canvas'.")
                else:
                    self.logger.debug('Layer %s\t%d Parent %s' % (l.name, l.layerId,
                     l.parent.layerId if l.parent else 'None'))

        finally:
            if not self.stream:
                stream.close()

        return

    def extractInfo(self):
        return PsdInfo(self)

    def save(self, dest=None, saveInvis=False, dirName=None, indexNames=False, inFolders=True):
        if not dest:
            dest = os.getcwd()
        if not dirName:
            psdBaseName = os.path.basename(self.fileName)
            psdFileName = os.path.splitext(psdBaseName)
            dirName = psdFileName[0]
        dest = os.path.join(dest, dirName)
        dest = normAbsPath(dest)
        if not os.path.exists(dest):
            os.mkdir(dest)
        for layer in self.layerMask.layers:
            name = layer.name
            id = layer.layerId
            type = layer.layerType['code']
            toSave = True
            if type != 0:
                if inFolders:
                    toSave = False
                    if type in (1, 2):
                        name = make_valid_filename('%s' % name, name, id)
                        dest = normAbsPath(dest + '/%s' % name)
                        os.path.exists(dest) or os.mkdir(dest)
                elif type == 3:
                    dest = normAbsPath(dest + '/..')
            if not layer.visible and not saveInvis:
                toSave = False
            if sum(layer.image.size) == 0:
                toSave = False
            if toSave:
                layer.saved = True
                if indexNames:
                    try:
                        layer.image.save('%s/%d.png' % (dest, id), 'PNG')
                    except SystemError, e:
                        self.logger.error("Can't save %s layer." % name)
                        raise e

                else:
                    name = make_valid_filename('%s/%s.png' % (dest, name), name, id)
                    layer.name = name
                    try:
                        layer.image.save('%s/%s.png' % (dest, name), 'PNG')
                    except SystemError, e:
                        self.logger.error("Can't save %s layer." % name)
                        raise e

        return dirName

    def __str__(self):
        return 'File Name:%s\n%s\n%s\n%s\n%s\n%s' % (
         '',
         self.header,
         self.colorMode,
         self.imageResources,
         self.layerMask,
         self.imageData)


class _PsdHeaderInfo(dict):

    def __init__(self, psd):
        self['height'] = psd.header.height
        self['width'] = psd.header.width
        self['depth'] = psd.header.depth
        self['colorMode'] = psd.header.colorMode['code']

    def __getattr__(self, key):
        try:
            return self[key]
        except KeyError:
            raise AttributeError


class _PsdLayerInfo(dict):

    def __init__(self, layer):
        self['id'] = layer.layerId
        self['opacity'] = layer.opacity
        self['name'] = layer.name
        self['text'] = layer.text
        self['position'] = {'top': layer.rectangle['top'], 'left': layer.rectangle['left'], 'bottom': layer.rectangle['bottom'], 
           'right': layer.rectangle['right']}
        self['dimensions'] = {'height': layer.rectangle['height'], 'width': layer.rectangle['width']}

    def __getattr__(self, key):
        try:
            return self[key]
        except KeyError:
            raise AttributeError


class PsdInfo(dict):

    def __init__(self, psd):
        self['header'] = _PsdHeaderInfo(psd)
        layers = []
        for layer in psd.layerMask.layers:
            if layer.layerType['code'] != 0 or layer.is_base_layer or not layer.visible:
                continue
            layers.append(_PsdLayerInfo(layer))

        self['layers'] = layers

    def __getattr__(self, key):
        try:
            return self[key]
        except KeyError:
            raise AttributeError