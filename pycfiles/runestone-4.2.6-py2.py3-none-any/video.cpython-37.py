# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /srv/RunestoneComponents/runestone/video/video.py
# Compiled at: 2020-04-16 12:40:55
# Size of source mod 2**32: 8248 bytes
__author__ = 'bmiller'
from docutils import nodes
from docutils.parsers.rst import directives
from docutils.parsers.rst import Directive
from runestone.server.componentdb import addQuestionToDB, addHTMLToDB
from runestone.common.runestonedirective import RunestoneIdDirective, RunestoneDirective

def setup(app):
    app.add_directive('video', Video)
    app.add_directive('youtube', Youtube)
    app.add_directive('vimeo', Vimeo)


CODE = '<div id="%(divid)s" class="video_popup runestone" >\n<video %(controls)s %(preload)s %(loop)s poster="%(thumb)s">\n    %(sources)s\n    No supported video types\n</video>\n</div>\n'
POPUP = '<a id="%(divid)s_thumb" style=\'position:relative;\'>\n    <img src="%(thumb)s" />\n    <div class=\'video-play-overlay\'></div>\n</a>\n<script>\n    jQuery(function ($) {\n       $(\'#%(divid)s_thumb\').click(function (e) {\n                $(\'#%(divid)s\').modal();\n                return false;\n        });\n    });\n</script>\n\n'
INLINE = '<script>\n   jQuery(function($) {\n      var rb = new RunestoneBase();\n      $(\'#%(divid)s_thumb\').click(function(e) {\n         $(\'#%(divid)s\').show();\n         $(\'#%(divid)s_thumb\').hide();\n         rb.logBookEvent({\'event\':\'video\',\'act\':\'play\',\'div_id\': \'%(divid)s\'});\n         // Log the run event\n      });\n      $(\'#%(divid)s video\').one("click", function(){\n        this.play();\n      });\n      $(\'#%(divid)s video\').one("play", function(){\n        rb.logBookEvent({\'event\':\'video\',\'act\':\'play\',\'div_id\': \'%(divid)s\'});\n      });\n   });\n</script>\n'
SOURCE = '<source src="%s" type="video/%s"></source>'

class Video(RunestoneIdDirective):
    __doc__ = '\n.. video:: id\n   :controls:  Show the controls or not\n   :loop: loop the video\n   :thumb: url to thumbnail image\n   :preload: set the video to preload in the bg\n\n   url to video format 1\n   url to video format 2\n   ...\n    '
    required_arguments = 1
    optional_arguments = 1
    final_argument_whitespace = True
    has_content = True
    option_spec = {'controls':directives.flag, 
     'loop':directives.flag, 
     'thumb':directives.uri, 
     'preload':directives.flag}

    def run(self):
        super(Video, self).run()
        addQuestionToDB(self)
        mimeMap = {'mov':'mp4', 
         'webm':'webm',  'm4v':'m4v'}
        sources = [SOURCE % (directives.uri(line), mimeMap[line[line.rindex('.') + 1:]]) for line in self.content]
        if 'controls' in self.options:
            self.options['controls'] = 'controls'
        else:
            if 'loop' in self.options:
                self.options['loop'] = 'loop'
            else:
                self.options['loop'] = ''
            if 'preload' in self.options:
                self.options['preload'] = 'preload="auto"'
            else:
                self.options['preload'] = 'preload="none"'
            self.options['sources'] = '\n    '.join(sources)
            res = CODE % self.options
            if 'popup' in self.options:
                res += POPUP % self.options
            else:
                res += INLINE % self.options
        addHTMLToDB(self.options['divid'], self.options['basecourse'], res)
        return [nodes.raw((self.block_text), res, format='html')]


def align(argument):
    """Conversion function for the "align" option."""
    return directives.choice(argument, ('left', 'center', 'right'))


def httpOption(argument):
    """Conversion function for the "http" option."""
    return directives.choice(argument, ('http', 'https'))


class IframeVideo(RunestoneIdDirective):
    has_content = False
    required_arguments = 1
    optional_arguments = 0
    final_argument_whitespace = False
    option_spec = {'height':directives.nonnegative_int, 
     'width':directives.nonnegative_int, 
     'align':align, 
     'http':httpOption, 
     'divid':directives.unchanged}
    default_width = 500
    default_height = 281

    def run(self):
        super(IframeVideo, self).run()
        self.options['video_id'] = directives.uri(self.arguments[0])
        if not self.options.get('width'):
            self.options['width'] = self.default_width
        if not self.options.get('height'):
            self.options['height'] = self.default_height
        if not self.options.get('align'):
            self.options['align'] = 'left'
        if not self.options.get('http'):
            self.options['http'] = 'https'
        if not self.options.get('divid'):
            self.options['divid'] = self.arguments[0]
        res = self.html % self.options
        addHTMLToDB(self.options['divid'], self.options['basecourse'], res)
        raw_node = nodes.raw((self.block_text), res, format='html')
        raw_node.source, raw_node.line = self.state_machine.get_source_and_line(self.lineno)
        return [
         raw_node]


class Youtube(IframeVideo):
    __doc__ = '\n.. youtube:: YouTubeID\n   :divid: the runestone id for this video\n   :height: 315\n   :width: 560\n   :align: left\n   :http: http\n   :start: None\n   :end: None\n   '
    html = '\n    <div class="runestone" style="margin-left: auto; margin-right:auto">\n        <div id="%(divid)s" class="align-%(align)s youtube-video" data-video-height="%(height)d" data-video-width="%(width)d" data-video-videoid="%(video_id)s" data-video-divid="%(divid)s" data-video-start="%(start)d" data-video-end="%(end)s" ></div>\n        <p class="runestone_caption"><span class="runestone_caption_text">Video: (%(divid)s)</span> </p>\n    </div>\n    '
    option_spec = IframeVideo.option_spec
    option_spec.update({'start':directives.nonnegative_int, 
     'end':directives.nonnegative_int})

    def run(self):
        if not self.options.get('start'):
            self.options['start'] = 0
        if not self.options.get('end'):
            self.options['end'] = -1
        raw_node = super(Youtube, self).run()
        addQuestionToDB(self)
        return raw_node


class Vimeo(IframeVideo):
    __doc__ = '\n.. vimeo:: vimeoID\n   :height: 315\n   :width: 560\n   :align: left\n   :http: http\n    '
    html = '<iframe src="%(http)s://player.vimeo.com/video/%(video_id)s"     width="%(width)u" height="%(height)u" frameborder="0"     webkitAllowFullScreen mozallowfullscreen allowFullScreen     class="align-%(align)s" seamless ></iframe>'


source = 'This is some text.\n\n.. video:: divid\n   :controls:\n   :thumb: _static/turtlestill.png\n   :loop:\n\n   http://knuth.luther.edu/~bmiller/foo.mov\n   http://knuth.luther.edu/~bmiller/foo.webm\n\nThis is some more text.\n'
if __name__ == '__main__':
    from docutils.core import publish_parts
    directives.register_directive('video', Video)
    doc_parts = publish_parts(source,
      settings_overrides={'output_encoding':'utf8', 
     'initial_header_level':2},
      writer_name='html')
    print(doc_parts['html_body'])