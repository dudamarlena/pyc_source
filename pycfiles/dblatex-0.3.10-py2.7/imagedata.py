# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/dbtexmf/core/imagedata.py
# Compiled at: 2017-04-03 18:58:57
import sys, os, re, shutil, logging, urllib
from dbtexmf.core.error import signal_error
from commander import CommandRunner

class ObjectFilter:
    """
    Its purpose is to select some objects from a list according to specified
    criterions. It assumes that '*' applied to a criterion means 'any'.
    """

    def __init__(self):
        pass

    def _re_multi_or_star(self, searched):
        if not searched:
            searched = '\\w*'
        else:
            s = searched.split()
            searched = ('|').join([ '%s' % p for p in s ])
        searched += '|\\*'
        return '(' + searched + ')'

    def select(self, object_list, **filter_criterions):
        for criterion, value in filter_criterions.items():
            filter_criterions[criterion] = self._re_multi_or_star(value)

        founds = []
        for obj in object_list:
            object_criterions = obj.criterions()
            for criterion, re_expr in filter_criterions.items():
                data = object_criterions.get(criterion, '')
                m = re.search(re_expr, data)
                if not m:
                    break

            if m:
                founds.append(obj)

        return founds


class PoolManager:

    def __init__(self):
        self._used_pool = None
        self._pending_pools = []
        return

    def set_pool(self, pool):
        self._used_pool = pool
        for p in self._pending_pools:
            pool.preprend(p)

        self._pending_pools = []

    def prepend_pool(self, pool):
        if self._used_pool:
            self._used_pool.prepend(pool)
        else:
            self._pending_pools.append(pool)


class ImageSetup:
    """
    Central imagedata setup, filled by default object configurations and
    by the XML configuration
    """

    def __init__(self):
        self.converter_pool = PoolManager()
        self.format_pool = PoolManager()


_image_setup = ImageSetup()

def image_setup():
    global _image_setup
    return _image_setup


class ImageConverter:
    _log = logging.getLogger('dblatex')

    def __init__(self, imgsrc, imgdst='', docformat='', backend=''):
        self.imgsrc = imgsrc
        self.imgdst = imgdst or '*'
        self.docformat = docformat or '*'
        self.backend = backend or '*'
        self.command = CommandRunner(log=self._log)

    def criterions(self):
        return {'imgsrc': self.imgsrc, 'imgdst': self.imgdst, 
           'docformat': self.docformat, 
           'backend': self.backend}

    def add_command(self, *args, **kwargs):
        self.command.add_command(*args, **kwargs)

    def convert(self, input, output, format, doexec=1):
        rc = self.command.run(kw={'input': input, 'output': output, 'dst': format})
        if rc != 0:
            signal_error(self, '')


class ImageConverterPool:

    def __init__(self):
        self.converters = []
        self._filter = ObjectFilter()

    def add_converter(self, converter):
        self.converters.append(converter)

    def extend(self, other):
        self.converters.extend(other.converters)

    def prepend(self, other):
        self.converters = other.converters + self.converters

    def get_converters(self, imgsrc='', imgdst='', docformat='', backend=''):
        founds = self._filter.select(self.converters, imgsrc=imgsrc, imgdst=imgdst, docformat=docformat, backend=backend)
        return founds


class ImageConverters(ImageConverterPool):

    def __init__(self):
        ImageConverterPool.__init__(self)
        self.add_converter(GifConverter('gif'))
        self.add_converter(EpsConverter('eps', 'pdf'))
        self.add_converter(EpsConverter('eps', 'png'))
        self.add_converter(FigConverter('fig', 'pdf'))
        self.add_converter(FigConverter('fig', 'png'))
        self.add_converter(SvgConverter('svg'))
        image_setup().converter_pool.set_pool(self)


class GifConverter(ImageConverter):

    def __init__(self, imgsrc, imgdst='', docformat='', backend=''):
        ImageConverter.__init__(self, imgsrc='gif bmp', imgdst='*')
        self.add_command(['convert', '%(input)s', '%(output)s'])


class EpsConverter(ImageConverter):

    def __init__(self, imgsrc, imgdst='', docformat='', backend=''):
        ImageConverter.__init__(self, imgsrc='eps', imgdst=imgdst)
        if imgdst == 'pdf':
            self.add_command(['epstopdf', '--outfile=%(output)s', '%(input)s'], shell=True)
        elif imgdst == 'png':
            self.add_command(['convert', '%(input)s', '%(output)s'])


class FigConverter(ImageConverter):

    def __init__(self, imgsrc, imgdst='', docformat='', backend=''):
        ImageConverter.__init__(self, imgsrc='fig', imgdst=imgdst)
        self.add_command(['fig2dev', '-L', 'eps', '%(input)s'], stdout='%(output)s')
        if imgdst != 'eps':
            self.conv_next = EpsConverter('eps', imgdst=imgdst)
        else:
            self.conv_next = None
        return

    def convert(self, input, output, format):
        if self.conv_next:
            epsfile = 'tmp_fig.eps'
        else:
            epsfile = output
        ImageConverter.convert(self, input, epsfile, 'eps')
        if self.conv_next:
            self.conv_next.convert(epsfile, output, format)


class SvgConverter(ImageConverter):

    def __init__(self, imgsrc, imgdst='', docformat='', backend=''):
        ImageConverter.__init__(self, imgsrc='svg', imgdst=imgdst)
        self.add_command(['inkscape', '-z', '-D', '--export-%(dst)s=%(output)s',
         '%(input)s'])


class FormatRule:

    def __init__(self, imgsrc='', imgdst='', docformat='', backend=''):
        self.imgsrc = imgsrc or '*'
        self.imgdst = imgdst or '*'
        self.docformat = docformat or '*'
        self.backend = backend or '*'

    def criterions(self):
        return {'imgsrc': self.imgsrc, 'imgdst': self.imgdst, 
           'docformat': self.docformat, 
           'backend': self.backend}


class ImageFormatPool:

    def __init__(self):
        self.rules = []
        self._filter = ObjectFilter()

    def add_rule(self, rule):
        self.rules.append(rule)

    def prepend(self, other):
        self.rules = other.rules + self.rules

    def output_format(self, imgsrc='', docformat='', backend=''):
        founds = self._filter.select(self.rules, imgsrc=imgsrc, docformat=docformat, backend=backend)
        if founds:
            return founds[0].imgdst
        else:
            return ''


class ImageFormatRuleset(ImageFormatPool):

    def __init__(self):
        ImageFormatPool.__init__(self)
        self.add_rule(FormatRule(docformat='pdf', backend='xetex', imgdst='png'))
        self.add_rule(FormatRule(docformat='pdf', imgdst='pdf'))
        self.add_rule(FormatRule(docformat='dvi', imgdst='eps'))
        self.add_rule(FormatRule(docformat='ps', imgdst='eps'))
        image_setup().format_pool.set_pool(self)


class Imagedata:

    def __init__(self):
        self.paths = []
        self.input_format = 'png'
        self.output_format = 'pdf'
        self.docformat = 'pdf'
        self.backend = ''
        self.rules = ImageFormatRuleset()
        self.converters = ImageConverters()
        self.converted = {}
        self.log = logging.getLogger('dblatex')
        self.output_encoding = ''

    def set_encoding(self, output_encoding):
        self.output_encoding = output_encoding

    def set_format(self, docformat, backend):
        self.docformat = docformat
        self.backend = backend
        self.output_format = self.rules.output_format(docformat=docformat, backend=backend)

    def convert(self, fig):
        fig = urllib.url2pathname(fig)
        if os.path.sep != '/':
            fig = fig.replace(os.path.sep, '/')
        realfig, ext = self.scanformat(fig)
        if not realfig:
            self.log.warning("Image '%s' not found" % fig)
            return fig
        if self.converted.has_key(realfig):
            self.log.info("Image '%s' already converted as %s" % (
             fig, self.converted[realfig]))
            return self.converted[realfig]
        if not ext:
            ext = self.input_format
        if ext == self.output_format:
            return self._safe_file(fig, realfig, ext)
        count = len(self.converted)
        newfig = 'fig%d.%s' % (count, self.output_format)
        conv = self.converters.get_converters(imgsrc=ext, imgdst=self.output_format, backend=self.backend)
        if not conv:
            self.log.debug("Cannot convert '%s' to %s" % (fig,
             self.output_format))
            return self._safe_file(fig, realfig, ext)
        conv = conv[0]
        conv.log = self.log
        conv.convert(realfig, newfig, self.output_format)
        self.converted[realfig] = newfig
        return newfig

    def _safe_file(self, fig, realfig, ext):
        """
        Copy the file in the working directory if its path contains characters
        unsupported by latex, like spaces.
        """
        newfig = self._path_encode(fig)
        if newfig and newfig.find(' ') == -1:
            return newfig
        count = len(self.converted)
        newfig = 'figcopy%d.%s' % (count, ext)
        self.converted[realfig] = newfig
        shutil.copyfile(realfig, newfig)
        return newfig

    def _path_encode(self, fig):
        if self.output_encoding == 'utf8':
            return fig
        try:
            newfig = fig.decode('utf8').encode('ascii')
        except:
            newfig = ''

        return newfig

    def scanformat(self, fig):
        root, ext = os.path.splitext(fig)
        if ext:
            realfig = self.find(fig)
            return (
             realfig, ext[1:])
        if self.output_format == 'pdf':
            formats = ('png', 'pdf', 'jpg', 'eps', 'gif', 'fig', 'svg')
        else:
            formats = ('eps', 'fig', 'pdf', 'png', 'svg')
        for format in formats:
            realfig = self.find('%s.%s' % (fig, format))
            if realfig:
                self.log.info("Found %s for '%s'" % (format, fig))
                break

        if not realfig:
            realfig = self.find(fig)
            format = ''
        return (realfig, format)

    def find(self, fig):
        if os.path.isabs(fig):
            if os.path.isfile(fig):
                return fig
            else:
                return

        for path in self.paths:
            realfig = os.path.join(path, fig)
            if os.path.isfile(realfig):
                return realfig

        return