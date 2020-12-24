# uncompyle6 version 3.6.7
# Python bytecode 2.3 (62011)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build\bdist.win32\egg\dirstat\Dumpers\HTML.py
# Compiled at: 2006-06-19 05:16:20
from dirstat.Dumper import FileDumper
HEADER = '<html>\n<head>\n<!-- IE stuff for security zone -->\n<!-- saved from url=(0014)about:internet -->\n<title>Repertoire </title>\n<script language=\'javascript\'>\n<!--\nfunction fileinfo(elm,filename,filesize) {\n document.getElementById("filename").innerHTML=filename;\n document.getElementById("filesize").innerHTML=filesize;\n // document.getElementById("tooltip").innerHTML = "<b>Nom du fichier : </b>"+filename+"<br /><b>Taille du fichier : </b>"+filesize;\n // show();\n elm._oldcolor=elm.style.backgroundColor;\n elm.style.backgroundColor="#ff0000";\n}\nfunction fileout(elm) {\n document.getElementById("filename").innerHTML="";\n document.getElementById("filesize").innerHTML="";\n // document.getElementById("tooltip").innerHTML = "";\n // hide();\n elm.style.backgroundColor=elm._oldcolor;\n}\ntooltipOn = false;\nfunction show(){\n  if (true){\n    document.getElementById("tooltip").xwidth = document.getElementById("tooltip").offsetWidth;\n    document.getElementById("tooltip").xheight = document.getElementById("tooltip").offsetHeight;\n    mainwidth = 0\n    mainheight = 0\n    if( typeof( window.innerWidth ) == \'number\' ) {\n      mainwidth = window.innerWidth;\n      mainheight = window.innerHeight;\n    } else if( document.documentElement && ( document.documentElement.clientWidth || document.documentElement.clientHeight ) ) {\n      mainwidth = document.documentElement.clientWidth;\n      mainheight = document.documentElement.clientHeight;\n    } else if( document.body && ( document.body.clientWidth || document.body.clientHeight ) ) {\n      mainwidth = document.body.clientWidth;\n      mainheight = document.body.clientHeight;\n    }\n    document.getElementById("tooltip").mainwidth = mainwidth\n    document.getElementById("tooltip").mainheight = mainheight\n    // document.getElementById("tooltip").innerHTML = "";\n    tooltipOn = true;\n  }\n}\nfunction hide(){\n  tooltipOn = false\n}\nfunction getPosition(p){\n  x = (navigator.appName.substring(0,3) == "Net") ? p.pageX : event.x+document.body.scrollLeft;\n  y = (navigator.appName.substring(0,3) == "Net") ? p.pageY : event.y+document.body.scrollTop;\n  if(tooltipOn){\n    xleft = x-120;\n    xtop = y+25;\n    xwidth = document.getElementById("tooltip").xwidth;\n    xheight = document.getElementById("tooltip").xheight;\n\n    mainwidth = document.getElementById("tooltip").mainwidth\n    mainheight = document.getElementById("tooltip").mainheight\n\n    if (xleft+xwidth>mainwidth) { xleft = mainwidth-xwidth; }\n    if (xleft<0) { xleft = 0; }\n    if (xtop+xheight>mainheight) { xtop = mainheight-xheight; }\n    if (xtop<0) { xtop = 0; }\n\n    document.getElementById("tooltip").style.top = xtop;\n    document.getElementById("tooltip").style.left = xleft;\n    document.getElementById("tooltip").style.visibility = "visible";\n  }\n  else{\n    document.getElementById("tooltip").style.visibility = "hidden";\n    document.getElementById("tooltip").style.top = 0;\n    document.getElementById("tooltip").style.left = 0;\n  }\n}\n// document.onmousemove = getPosition;\ndocument.write(\'<div id="tooltip" class="tooltip"></div>\');\nvar swappanelstatus = 0;\nfunction swappanel() {\n    if (swappanelstatus==0)\n    {\n        document.getElementById("panelinfo").style.visibility = "hidden";\n        document.getElementById("panellegend").style.visibility = "visible";\n    }\n    else\n    {\n        document.getElementById("panellegend").style.visibility = "hidden";\n        document.getElementById("panelinfo").style.visibility = "visible";\n    }\n    swappanelstatus = 1-swappanelstatus;\n}\n-->\n</script>\n<style type=\'text/css\'>\n<!--\n.tooltip {\n  z-index:800;\n  position:absolute;\n  font-family:Verdana,Arial,Lucida,Sans-Serif;\n  font-size:11px;\n  border: solid 1px #808080;\n  background-color:#E4E0D8;\n  visibility:hidden;\n  padding:1;\n}\n.info {\n  position:absolute;\n  left:5;\n  top:5;\n  width:%(sizex)s;\n  height:30;\n  font-family:Verdana,Arial,Lucida,Sans-Serif;\n  font-size:11px;\n  font-weight:bold;\n  border: solid 1px #808080;\n  background-color:#E4E0D8;\n  white-space: nowrap;\n  overflow: visible;\n}\n.rect {\n  position:absolute;\n  border-style:solid;\n  border-width:1px;\n  margin : solid 0 #fff;\n\n  font-weight:bold;\n  text-align:center;\n  font-family:Verdana,Arial,Lucida,Sans-Serif;\n  font-size:11px;\n  white-space: nowrap;\n  overflow: visible;\n}\n.paneltexte ,\n.panel {\n  position:absolute;\n  left:5;\n  top:40;\n  width:%(sizex)s;\n  height:%(sizey)s;\n  background-color:none;\n  border-color:#000;\n  border-style:solid;\n  border-width:1px;\n  margin : solid 0 #fff;\n}\n#panelinfo {\n  visibility : visible;\n}\n#panellegend {\n  visibility : hidden;\n}\n#panelmetadata {\n  left:5;\n  top:5;\n  width:%(sizexmd)s;\n  height:%(sizeymd)s;\n\n  margin : solid 1 #fff;\n  margin:0;\n  padding: 5px;\n}\n#panelmetadata p {\n  font-family:Verdana,Arial,Lucida,Sans-Serif;\n  font-size:11px;\n}\n#filename {\n  padding-left: 10px;\n  padding-right: 10px;\n  padding-top: 2px;\n  padding-bottom: 1px;\n}\n#filesize {\n  padding-left: 10px;\n  padding-right: 10px;\n  padding-top: 1px;\n  padding-bottom: 2px;\n}\n-->\n</style>\n</head>\n<body>\n<span class=\'info\' onclick=\'javascript:swappanel()\'>\n<span id=\'filename\'></span><br />\n<span id=\'filesize\'></span>\n</span>\n<span class=\'panel\' id=\'panelinfo\'>\n'
FOOTER_PART1 = "\n</span>\n\n<span class='panel' id='panellegend'>\n<span class='paneltexte' id='panelmetadata'>\n"
FOOTER_PART2 = '\n</span>\n'
FOOTER_PART3 = '\n</span>\n\n</body>\n</html>\n'

class Dumper(FileDumper):
    __module__ = __name__
    EXT = '.html'

    def _start_dump(self):
        size = self.get_size()
        self.__dump_params = {'sizex': size.x(), 'sizey': size.y(), 'sizexmd': size.x() / 2 - 20, 'sizeymd': size.y() - 20}
        header = HEADER
        self._file.write(header % self.__dump_params)

    def _end_dump(self):
        footer = FOOTER_PART1
        self._file.write(footer % self.__dump_params)
        params = {'Generator': 'pydirstat', 'Version': '0.9.12'}
        for param in self.get_metadata():
            self._file.write('<p><b>%s</b> : %s</p>\n' % (param[0], param[1]))

        footer = FOOTER_PART2
        self._file.write(footer % self.__dump_params)
        (types, colors, method_by_type) = self.get_colors()
        border = 5
        if self.__dump_params['sizey'] < border * 2 * len(types) * 1.3:
            border = 0
        height = int((self.__dump_params['sizey'] - border * 2.0 * len(types)) / len(types))
        ypos = border
        for typename in types:
            ypos
            kwargs = {}
            kwargs['innertext'] = typename == '_' and 'Unknown' or typename
            kwargs['x'] = int(self.__dump_params['sizex'] / 2 + 5)
            kwargs['width'] = int(self.__dump_params['sizex'] / 2 - 10)
            kwargs['y'] = ypos
            kwargs['height'] = height - 2 * border
            kwargs['filename'] = ''
            kwargs['filesize'] = ''
            kwargs['color'] = colors[typename]
            filelisting = []
            if typename in method_by_type:
                if 'type:extension' in method_by_type[typename]:
                    for mask in method_by_type[typename]['type:extension']:
                        filelisting.append('*.' + mask)

                if 'type:extensionlower' in method_by_type[typename]:
                    for mask in method_by_type[typename]['type:extensionlower']:
                        filelisting.append('*.' + mask)

                if 'type:contain' in method_by_type[typename]:
                    for mask in method_by_type[typename]['type:contain']:
                        filelisting.append('*' + mask + '*')

                if 'type:exactmatch' in method_by_type[typename]:
                    for mask in method_by_type[typename]['type:exactmatch']:
                        filelisting.append(mask)

            filelisting.sort()
            kwargs['filename'] = (', ').join(filelisting)
            if typename == 'file':
                if len(filelisting) > 0:
                    kwargs['filename'] += ' and '
                kwargs['filename'] += 'any other file'
            if typename == 'dir':
                if len(filelisting) > 0:
                    kwargs['filename'] += ' and '
                kwargs['filename'] += 'any directory'
            self.addrect(**kwargs)
            ypos += height

        footer = FOOTER_PART3
        self._file.write(footer % self.__dump_params)

    def addrect(self, **kwargs):
        filename = kwargs['filename'].replace('\\', '\\\\').replace("'", '&apos;').replace('"', '&quot;').replace('&', '&amp;')
        if type(filename) != type(''):
            try:
                filename = filename.decode('utf8', 'replace')
            except LookupError:
                pass

        filename = filename.encode('iso-8859-1', 'replace')
        kwargs['filename'] = filename
        kwargs['colorx'] = kwargs['color'].get_htmlcolor_extended(lambda x: int(x * 0.6))
        color = kwargs['color'].get_rgb()
        if color[0] + color[1] + color[2] > 3 * 128:
            kwargs['colort'] = kwargs['color'].__class__(0, 0, 0)
        else:
            kwargs['colort'] = kwargs['color'].__class__(255, 255, 255)
        if 'innertext' not in kwargs:
            kwargs['innertext'] = ''
        self._file.write('<span class=\'rect\' onMouseOver=\'fileinfo(this,"%(filename)s","%(filesize)s")\' onMouseOut=\'fileout(this)\' style=\'left:%(x)dpx;top:%(y)dpx;width:%(width)dpx;height:%(height)dpx;background-color:%(color)s;border-color:%(colorx)s;color:%(colort)s\' />%(innertext)s</span>\n' % kwargs)


def test():
    Dumper().dump()


if __name__ == '__main__':
    test()