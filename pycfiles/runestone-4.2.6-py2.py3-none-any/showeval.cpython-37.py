# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /srv/RunestoneComponents/runestone/showeval/showeval.py
# Compiled at: 2020-04-16 12:40:55
# Size of source mod 2**32: 4796 bytes
__author__ = 'tconzett'
from docutils import nodes
from docutils.parsers.rst import directives
from docutils.parsers.rst import Directive
from runestone.server.componentdb import addQuestionToDB, addHTMLToDB
from runestone.common.runestonedirective import RunestoneIdDirective

def setup(app):
    app.add_directive('showeval', ShowEval)
    app.add_config_value('showeval_div_class', 'runestone explainer alert alert-warning', 'html')


CODE = '\n<div data-childcomponent="showeval" class="%(divclass)s" id="%(divid)s" data-tracemode="%(trace_mode)s">\n    <button class="btn btn-success" id="%(divid)s_nextStep">Next Step</button>\n    <button class="btn btn-default" id ="%(divid)s_reset">Reset</button>\n    <div class="evalCont" style="background-color: #FDFDFD;">%(preReqLines)s</div>\n    <div class="evalCont" id="%(divid)s"></div>\n    <script>\n    if (typeof window.raw_steps === "undefined") {\n    window.raw_steps = {};\n    }\n    raw_steps["%(divid)s"] = %(steps)s;\n    </script>\n</div>\n'

class ShowEval(RunestoneIdDirective):
    __doc__ = "\n.. showeval:: unique_id_goes_here\n   :trace_mode: boolean  <- Required option that enables 'Trace Mode'\n\n   some code\n   more code\n   ~~~~\n   more {{code}}{{what code becomes in step 1}}\n   more {{what code becomes in step 1}}{{what code becomes in step2}}  ##Optional comment for step 2\n   as many steps as you want {{the first double braces}}{{animate into the second}} wherever.\n\n\nconfig values (conf.py):\n\n- showeval_div_class - custom CSS class of the component's outermost div\n    "
    required_arguments = 1
    optional_arguments = 0
    final_argument_whitespace = True
    has_content = True
    option_spec = {'trace_mode': directives.unchanged_required}

    def run(self):
        super(ShowEval, self).run()
        addQuestionToDB(self)
        self.options['trace_mode'] = self.options['trace_mode'].lower()
        self.options['preReqLines'] = ''
        self.options['steps'] = []
        env = self.state.document.settings.env
        self.options['divclass'] = env.config.showeval_div_class
        is_dynamic = env.config.html_context.get('dynamic_pages', False)
        is_dynamic = True if is_dynamic == 'True' else False
        step = False
        count = 0
        for line in self.content:
            if step == True:
                if line != '':
                    if is_dynamic:
                        esc_line = str(line).replace('{', '\\{')
                    else:
                        esc_line = str(line)
                    self.options['steps'].append(esc_line)
                else:
                    if '~~~~' in line:
                        step = True
            else:
                self.options['preReqLines'] += line + '<br />\n'

        res = CODE % self.options
        addHTMLToDB(self.options['divid'], self.options['basecourse'], res)
        return [nodes.raw((self.block_text), res, format='html')]