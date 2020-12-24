# uncompyle6 version 3.6.7
# Python bytecode 2.3 (62011)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build\bdist.win32\egg\dirstat\Dumpers\SVG.py
# Compiled at: 2006-06-19 05:16:20
from dirstat.Dumper import FileDumper

class Dumper(FileDumper):
    __module__ = __name__
    EXT = '.svg'

    def _start_dump(self):
        header = '<?xml version=\'1.0\' encoding=\'iso-8859-1\'?>\n<!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 1.0//EN" "http://www.w3.org/TR/2001/REC-SVG-20010904/DTD/svg10.dtd ">\n<svg width="%(sizex)dpx" viewBox="0 0 %(sizex)d %(sizey)d " height="%(sizey)dpx" xmlns="http://www.w3.org/2000/svg" >\n    <script>\n        var oldcolor;\n\n        var infoTipOffsetFactor = 1;\n        function hideFileAttr(evt){\n            var target = evt.getTarget();\n            var svgdoc = target.getOwnerDocument();\n            var filenametext = svgdoc.getElementById (\'filename\');\n            filenametext.getStyle().setProperty (\'visibility\', \'hidden\');\n            var filesizetext = svgdoc.getElementById (\'filesize\');\n            filesizetext.getStyle().setProperty (\'visibility\', \'hidden\');\n            var svgrect = svgdoc.getElementById (\'infotipRect\');\n            svgrect.getStyle().setProperty (\'visibility\', \'hidden\');\n\n            target.setAttribute(\'fill\',oldcolor);\n        }\n        function setFileAttr(evt,filename,filesize){\n            var target = evt.getTarget();\n            var svgdoc = target.getOwnerDocument();\n            var svgdocElement = svgdoc.getDocumentElement();\n\n            var filenametext = svgdoc.getElementById (\'filename\');\n            x = (infoTipOffsetFactor)*eval(evt.getClientX()+10);\n            y = (infoTipOffsetFactor)*eval(evt.getClientY()-40);\n\n            filenametext.getStyle().setProperty (\'visibility\', \'visible\');\n            svgobjfilename = filenametext.getFirstChild();\n            svgobjfilename.setData(filename);\n            var txtlen=filenametext.getComputedTextLength();\n\n            var filesizetext = svgdoc.getElementById (\'filesize\');\n            sx = (infoTipOffsetFactor)*eval(evt.getClientX()+10);\n            sy = y+13;\n\n            oldcolor=target.getAttribute(\'fill\');\n            target.setAttribute(\'fill\', \'red\');\n\n            filesizetext.getStyle().setProperty (\'visibility\', \'visible\');\n            svgobjfilesize = filesizetext.getFirstChild();\n            svgobjfilesize.setData(filesize);\n            var sizelen=filesizetext.getComputedTextLength();\n\n\n            if (y&lt;40)\n            {\n                y=y+100;\n                sy=sy+100;\n            }\n\n            var xlen=txtlen;\n            if (xlen&lt;sizelen) xlen=sizelen;\n\n            if ((txtlen+x&gt;%(sizex)d) || (sizelen+sx&gt;%(sizex)d))\n            {\n                x=%(sizex)d-txtlen-10;\n            }\n            sx=x+xlen-sizelen;\n\n            filenametext.setAttribute (\'x\', x);\n            filenametext.setAttribute (\'y\', y);\n            svgobjfilename.setData(filename);\n\n            filesizetext.setAttribute (\'x\', sx);\n            filesizetext.setAttribute (\'y\', sy);\n            svgobjfilesize.setData(filesize);\n\n            var svgrect = svgdoc.getElementById (\'infotipRect\');\n            svgrect.getStyle().setProperty (\'visibility\', \'visible\');\n            svgrect.setAttribute (\'x\', x-4);\n            svgrect.setAttribute (\'y\', y-11.5);\n            svgrect.setAttribute (\'width\', xlen+10);\n        }\n    </script>\n    <g style="stroke:black; stroke-width:1px">\n'
        size = self.get_size()
        self._file.write(header % {'sizex': size.x(), 'sizey': size.y()})

    def _end_dump(self):
        footer = '\n    </g>\n    <g id="infotips">\n    <rect id="infotipRect" x="20" y="0" width="100" height="30" rx="5" ry="5" style="visibility:hidden;fill:rgb(139,199,139);stroke-width:1; stroke:rgb(0,0,0);opacity:0.8;pointer-events:none"></rect>\n    <text y="%(sizey)d" x="10" id="filename" style="visibility:visible;font-weight:normal; font-family:\'Arial\';font-size:13;text-anchor:left;pointer-events:none"> </text>\n    <text y="%(sizey)d" x="10" id="filesize" style="visibility:hidden;fill:rgb(80,0,0);font-weight:normal; font-family:\'Arial\';font-size:13;text-anchor:left;pointer-events:none"> </text>\n    </g>\n</svg>\n'
        size = self.get_size()
        self._file.write(footer % {'sizex': size.x(), 'sizey': size.y()})

    def addrect(self, **kwargs):
        kwargs['filename'] = kwargs['filename'].replace('\\', '\\\\').replace("'", "\\'").replace('&', '&amp;').encode('iso-8859-1', 'replace')
        self._file.write('        <rect x="%(x)d" y="%(y)d" height="%(height)d" width="%(width)d" onmouseover="setFileAttr(evt,\'%(filename)s\',\'%(filesize)s\')" onmouseout="hideFileAttr(evt)" fill="%(color)s"/>\n' % kwargs)


def test():
    Dumper().dump()


if __name__ == '__main__':
    test()