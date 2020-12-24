# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ana/dev/dexy-clean/dexy/filters/phantomjs.py
# Compiled at: 2020-03-18 15:12:33
# Size of source mod 2**32: 5885 bytes
from dexy.exceptions import UserFeedback
from dexy.filters.process import SubprocessFilter
import os

class CasperJsSvg2PdfFilter(SubprocessFilter):
    __doc__ = '\n    Converts an SVG file to PDF by running it through casper js.\n\n    # TODO convert this to phantomjs, no benefit to using casper here (js is\n    # not user facing) and more restrictive\n    '
    aliases = ['svg2pdf']
    _settings = {'add-new-files':True, 
     'executable':'casperjs', 
     'version-command':'casperjs --version', 
     'input-extensions':[
      '.svg'], 
     'output-extensions':[
      '.pdf'], 
     'width':('Width of page to capture.', 200), 
     'height':('Height of page to capture.', 200), 
     'command-string':'%(prog)s %(args)s script.js'}

    def script_js(self, width, height):
        args = {'width':width, 
         'height':height, 
         'svgfile':self.work_input_filename(), 
         'pdffile':self.work_output_filename()}
        return "\n        var casper = require('casper').create({\n             viewportSize : {width : %(width)s, height : %(height)s}\n        });\n        casper.start('%(svgfile)s', function() {\n            this.capture('%(pdffile)s');\n        });\n\n        casper.run();\n        " % args

    def custom_populate_workspace(self):
        width = self.setting('width')
        height = self.setting('height')
        js = self.script_js(width, height)
        wd = self.parent_work_dir()
        scriptfile = os.path.join(wd, 'script.js')
        self.log_debug('scriptfile: %s' % scriptfile)
        self.log_debug('js for scriptfile: %s' % js)
        with open(scriptfile, 'w') as (f):
            f.write(js)


class PhantomJsRenderSubprocessFilter(SubprocessFilter):
    __doc__ = '\n    Renders HTML to PNG/PDF using phantom.js.\n    \n    If the HTML relies on local assets such as CSS or image files, these should\n    be specified as inputs.\n\n    See phantomjs documentation for paper sizing options.\n    http://phantomjs.org/api/webpage/property/paper-size.html\n    '
    aliases = ['phrender']
    _settings = {'add-new-files':True, 
     'examples':[
      'phrender'], 
     'executable':'phantomjs', 
     'paper-size':("Paper size (e.g. phantomjs 'pageSize.format' setting).", 'A4'), 
     'orientation':('e.g. landscape or portrait orientation.', None), 
     'page-width':('Paper width for page.paperSize phantom setting.', None), 
     'page-height':('Paper height for page.paperSize phantom setting.', None), 
     'border':('Border around page.', None), 
     'page-header-height':('Height of header to print on each page.', None), 
     'page-header-contents':('Custom HTML header to print on each page.', None), 
     'page-footer-height':('Height of footer to print on each page.', None), 
     'page-footer-contents':('Custom HTML footer to print on each page.', None), 
     'version-command':'phantomjs --version', 
     'command-string':'%(prog)s %(args)s script.js', 
     'input-extensions':[
      '.html', '.htm', '.txt'], 
     'output-extensions':[
      '.png', '.pdf']}

    def custom_populate_workspace(self):
        timeout = self.setup_timeout()
        if not timeout:
            raise Exception('must have timeout')
        args = {'address':self.work_input_filename(), 
         'output':self.work_output_filename(), 
         'timeout':timeout}
        page_width = self.setting('page-width')
        page_height = self.setting('page-height')
        border = self.setting('border')
        orientation = self.setting('orientation')
        if page_width is not None and page_height is not None:
            args['paper_size'] = "width: '%s',\nheight: '%s',\n" % (page_width, page_height)
        else:
            args['paper_size'] = "format: '%s',\n" % format
            if orientation is not None:
                args['paper_size'] += "orientation: '%s',\n" % orientation
        if border is not None:
            args['paper_size'] += "border: '%s',\n" % border
        if self.setting('page-header-height') is not None:
            args['paper_size'] += 'header: {\n                height: "%s",\n                contents: phantom.callback(function(pageNum, numPages) {\n                    return %s\n                })\n                },\n            ' % (self.setting('page-header-height'), self.setting('page-header-contents'))
        if self.setting('page-footer-height') is not None:
            args['paper_size'] += 'footer: {\n                height: "%s",\n                contents: phantom.callback(function(pageNum, numPages) {\n                    return %s\n                })\n                },\n            ' % (self.setting('page-footer-height'), self.setting('page-footer-contents'))
        self.log_debug('args are: %s' % args)
        js = "\n        address = '%(address)s'\n        output = '%(output)s'\n        var page = new WebPage(),\n            address, output, size;\n\n        page.paperSize = {\n            %(paper_size)s\n        };\n\n        page.open(address, function (status) {\n            if (status !== 'success') {\n                console.log('Unable to load the address!');\n            } else {\n                window.setTimeout(function () {\n                page.render(output);\n                phantom.exit();\n                }, %(timeout)s);\n            }\n        });\n        " % args
        wd = self.parent_work_dir()
        scriptfile = os.path.join(wd, 'script.js')
        self.log_debug('scriptfile: %s' % scriptfile)
        self.log_debug('js for scriptfile: %s' % js)
        with open(scriptfile, 'w') as (f):
            f.write(js)