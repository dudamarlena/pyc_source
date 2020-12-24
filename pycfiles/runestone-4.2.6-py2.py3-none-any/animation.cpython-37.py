# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/bmiller/Runestone/RunestoneComponents/runestone/animation/animation.py
# Compiled at: 2019-11-02 08:12:59
# Size of source mod 2**32: 3295 bytes
__author__ = 'bmiller'
from docutils import nodes
from docutils.parsers.rst import directives
from runestone.common.runestonedirective import RunestoneIdDirective

def setup(app):
    app.add_directive('animation', Animation)
    app.add_autoversioned_javascript('animationbase.js')


SRC = '\n<div id="%(divid)s">\n<canvas id="%(divid)s_canvas" width="400" height="400" style="border:4px solid blue"></canvas>\n<br />\n<button onclick="%(divid)s_anim = %(divid)s_init(\'%(divid)s\')">Initialize</button>\n<button onclick="%(divid)s_anim.run(\'%(divid)s_anim\')">Run</button>\n<button onclick="%(divid)s_anim.stop()">Stop</button> </br>\n<button onclick="%(divid)s_anim.begin()">Beginning</button>\n<button onclick="%(divid)s_anim.forward()">Step Forward</button>\n<button onclick="%(divid)s_anim.backward()">Step Backward</button>\n<button onclick="%(divid)s_anim.end()">End</button>\n\n<script type="text/javascript">\n%(divid)s_init = function(divid)\n{\n   var a = new Animator(new %(model)s(), new %(viewer)s(), divid)\n   a.init()\n   return a\n}\n</script>\n\n</div>\n'
SCRIPTTAG = '<script type="text/javascript" src="../_static/%s"></script>\n'

class Animation(RunestoneIdDirective):
    required_arguments = 1
    optional_arguments = 1
    final_argument_whitespace = True
    has_content = False
    option_spec = {'modelfile':directives.unchanged, 
     'viewerfile':directives.unchanged, 
     'model':directives.unchanged, 
     'viewer':directives.unchanged}

    def run(self):
        super(Animation, self).run()
        res = ''
        if 'modelfile' in self.options:
            res = res + SCRIPTTAG % self.options['modelfile']
        if 'viewerfile' in self.options:
            res = res + SCRIPTTAG % self.options['viewerfile']
        res = res + SRC % self.options
        rawnode = nodes.raw((self.block_text), res, format='html')
        rawnode.source, rawnode.line = self.state_machine.get_source_and_line(self.lineno)
        return [
         rawnode]


source = '\n.. animation:: testanim\n   :modelfile: sortmodels.js\n   :viewerfile: sortviewers.js\n   :model: SortModel\n   :viewer: BarViewer\n\n'
if __name__ == '__main__':
    from docutils.core import publish_parts
    directives.register_directive('animation', Animation)
    doc_parts = publish_parts(source,
      settings_overrides={'output_encoding':'utf8', 
     'initial_header_level':2},
      writer_name='html')
    print(doc_parts['html_body'])