# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /srv/RunestoneComponents/runestone/activecode/activecode.py
# Compiled at: 2020-04-16 12:40:55
# Size of source mod 2**32: 16051 bytes
from __future__ import print_function
__author__ = 'bmiller'
from docutils import nodes
from docutils.parsers.rst import directives
from .textfield import *
from sqlalchemy import Table
from runestone.server.componentdb import addQuestionToDB, addHTMLToDB, engine, meta
from runestone.common.runestonedirective import RunestoneIdDirective, RunestoneNode, add_i18n_js, add_skulpt_js
try:
    from html import escape
except ImportError:
    from cgi import escape

if engine:
    Source_code = Table('source_code', meta, autoload=True, autoload_with=engine)

def setup(app):
    app.add_directive('activecode', ActiveCode)
    app.add_directive('actex', ActiveExercise)
    app.add_role('textfield', textfield_role)
    app.add_config_value('activecode_div_class', 'runestone explainer ac_section alert alert-warning', 'html')
    app.add_config_value('activecode_hide_load_history', False, 'html')
    app.add_config_value('wasm_uri', '/_static', 'html')
    app.add_autoversioned_javascript('jquery.highlight.js')
    app.add_autoversioned_javascript('sql-wasm.js')
    app.add_javascript('https://cdn.jsdelivr.net/npm/handsontable@7.2.2/dist/handsontable.full.js')
    app.add_stylesheet('https://cdn.jsdelivr.net/npm/handsontable@7.2.2/dist/handsontable.full.min.css')
    app.add_node(ActivcodeNode, html=(visit_ac_node, depart_ac_node))
    app.connect('doctree-resolved', process_activcode_nodes)
    app.connect('env-purge-doc', purge_activecodes)


TEMPLATE_START = '\n<div data-childcomponent="%(divid)s" class="%(divclass)s">\n'
TEMPLATE_END = '\n<textarea data-component="activecode" id=%(divid)s data-lang="%(language)s" %(autorun)s\n    %(hidecode)s %(include)s %(timelimit)s %(coach)s %(codelens)s %(enabledownload)s %(chatcodes)s\n    data-audio=\'%(ctext)s\' %(sourcefile)s %(datafile)s %(stdin)s %(tie)s %(dburl)s %(nopair)s\n    %(cargs)s %(largs)s %(rargs)s %(iargs)s %(gradebutton)s %(caption)s %(hidehistory)s %(wasmuri)s>\n%(initialcode)s\n</textarea>\n</div>\n'

class ActivcodeNode(nodes.General, nodes.Element, RunestoneNode):

    def __init__(self, content, **kwargs):
        (super(ActivcodeNode, self).__init__)(name=content['name'], **kwargs)
        self.ac_components = content


def visit_ac_node(self, node):
    node.delimiter = '_start__{}_'.format(node.ac_components['divid'])
    self.body.append(node.delimiter)
    res = TEMPLATE_START % node.ac_components
    self.body.append(res)


def depart_ac_node(self, node):
    """ This is called at the start of processing an activecode node.  If activecode had recursive nodes
        etc and did not want to do all of the processing in visit_ac_node any finishing touches could be
        added here.
    """
    res = TEMPLATE_END % node.ac_components
    self.body.append(res)
    addHTMLToDB(node.ac_components['divid'], node.ac_components['basecourse'], ''.join(self.body[self.body.index(node.delimiter) + 1:]))
    self.body.remove(node.delimiter)


def process_activcode_nodes(app, env, docname):
    pass


def purge_activecodes(app, env, docname):
    pass


class ActiveCode(RunestoneIdDirective):
    __doc__ = '\n.. activecode:: uniqueid\n   :nocanvas:  -- do not create a canvas\n   :autograde: unittest\n   :nopre: -- do not create an output component\n   :above: -- put the canvas above the code\n   :autorun: -- run this activecode as soon as the page is loaded\n   :caption: this is the caption\n   :include: div1,div2 -- invisibly include code from another activecode\n   :hidecode: -- Don\'t show the editor initially\n   :nocodelens: -- Do not show the codelens button\n   :timelimit: -- set the time limit for this program in seconds\n   :language: python, html, javascript, java, python2, python3\n   :chatcodes: -- Enable users to talk about this code snippet with others\n   :tour_1: audio tour track\n   :tour_2: audio tour track\n   :tour_3: audio tour track\n   :tour_4: audio tour track\n   :tour_5: audio tour track\n   :stdin: : A file to simulate stdin (java, python2, python3)\n   :datafile: : A datafile for the program to read (java, python2, python3)\n   :sourcefile: : source files (java, python2, python3)\n   :available_files: : other additional files (java, python2, python3)\n   :enabledownload: -- allow textfield contents to be downloaded as *.py file\n   :nopair: -- disable pair programming features\n   :dburl: url to load database for sql mode\n\n    If this is a homework problem instead of an example in the text\n    then the assignment text should go here.  The assignment text ends with\n    the line containing four tilde ~\n    ~~~~\n    print("hello world")\n    ====\n    print("Hidden code, such as unit tests come after the four = signs")\n\nconfig values (conf.py):\n\n- activecode_div_class - custom CSS class of the component\'s outermost div\n- activecode_hide_load_history - if True, hide the load history button\n- wasm_uri - Path or Full URL to folder containing WASM files for SQL. /_static is default\n    '
    required_arguments = 1
    optional_arguments = 1
    has_content = True
    option_spec = RunestoneIdDirective.option_spec.copy()
    option_spec.update({'nocanvas':directives.flag, 
     'nopre':directives.flag, 
     'above':directives.flag, 
     'autorun':directives.flag, 
     'caption':directives.unchanged, 
     'include':directives.unchanged, 
     'hidecode':directives.flag, 
     'language':directives.unchanged, 
     'chatcodes':directives.flag, 
     'tour_1':directives.unchanged, 
     'tour_2':directives.unchanged, 
     'tour_3':directives.unchanged, 
     'tour_4':directives.unchanged, 
     'tour_5':directives.unchanged, 
     'nocodelens':directives.flag, 
     'coach':directives.flag, 
     'gradebutton':directives.flag, 
     'timelimit':directives.unchanged, 
     'stdin':directives.unchanged, 
     'datafile':directives.unchanged, 
     'sourcefile':directives.unchanged, 
     'available_files':directives.unchanged, 
     'enabledownload':directives.flag, 
     'compileargs':directives.unchanged, 
     'linkargs':directives.unchanged, 
     'interpreterargs':directives.unchanged, 
     'runargs':directives.unchanged, 
     'tie':directives.unchanged, 
     'nopair':directives.flag, 
     'dburl':directives.unchanged})

    def run(self):
        super(ActiveCode, self).run()
        addQuestionToDB(self)
        env = self.state.document.settings.env
        if not hasattr(env, 'activecodecounter'):
            env.activecodecounter = 0
        else:
            env.activecodecounter += 1
            self.options['name'] = self.arguments[0].strip()
            explain_text = None
            if self.content:
                if '~~~~' in self.content:
                    idx = self.content.index('~~~~')
                    explain_text = self.content[:idx]
                    self.content = self.content[idx + 1:]
                source = '\n'.join(self.content)
            else:
                source = '\n'
            self.options['initialcode'] = source
            str = source.replace('\n', '*nline*')
            str0 = str.replace('"', '*doubleq*')
            str1 = str0.replace('(', '*open*')
            str2 = str1.replace(')', '*close*')
            str3 = str2.replace("'", '*singleq*')
            self.options['argu'] = str3
            complete = ''
            no_of_buttons = 0
            okeys = list(self.options.keys())
            for k in okeys:
                if 'tour_' in k:
                    x, label = k.split('_')
                    no_of_buttons = no_of_buttons + 1
                    complete = complete + self.options[k] + '*atype*'

            newcomplete = complete.replace('"', '*doubleq*')
            self.options['ctext'] = newcomplete
            self.options['no_of_buttons'] = no_of_buttons
            if 'caption' not in self.options:
                self.options['caption'] = ''
            else:
                self.options['caption'] = "data-caption='%s'" % self.options['caption']
            if 'include' not in self.options:
                self.options['include'] = ''
            else:
                lst = self.options['include'].split(',')
                lst = [x.strip() for x in lst]
                self.options['include'] = 'data-include="' + ' '.join(lst) + '"'
            if 'hidecode' in self.options:
                self.options['hidecode'] = 'data-hidecode="true"'
            else:
                self.options['hidecode'] = ''
            if 'enabledownload' in self.options:
                self.options['enabledownload'] = 'data-enabledownload="true"'
            else:
                self.options['enabledownload'] = ''
            if 'chatcodes' in self.options:
                self.options['chatcodes'] = 'data-chatcodes="true"'
            else:
                self.options['chatcodes'] = ''
            if 'language' not in self.options:
                self.options['language'] = 'python'
            else:
                if self.options['language'] == 'html':
                    self.options['language'] = 'htmlmixed'
                    self.options['initialcode'] = escape(self.options['initialcode'])
                else:
                    if 'nocodelens' in self.options or self.options['language'] not in ('python',
                                                                                        'java',
                                                                                        'c',
                                                                                        'cpp'):
                        self.options['codelens'] = ''
                    else:
                        self.options['codelens'] = 'data-codelens="true"'
                    if 'nopair' in self.options:
                        self.options['nopair'] = 'data-nopair="true"'
                    else:
                        self.options['nopair'] = ''
                    if 'timelimit' not in self.options:
                        self.options['timelimit'] = 'data-timelimit=25000'
                    else:
                        self.options['timelimit'] = 'data-timelimit=%s' % self.options['timelimit']
                    if 'autorun' not in self.options:
                        self.options['autorun'] = ''
                    else:
                        self.options['autorun'] = 'data-autorun="true"'
                    if 'coach' in self.options:
                        self.options['coach'] = 'data-coach="true"'
                    else:
                        self.options['coach'] = ''
                    if 'stdin' in self.options:
                        self.options['stdin'] = "data-stdin='%s'" % self.options['stdin']
                    else:
                        self.options['stdin'] = ''
                    if 'datafile' not in self.options:
                        self.options['datafile'] = ''
                    else:
                        self.options['datafile'] = "data-datafile='%s'" % self.options['datafile']
                    if 'sourcefile' not in self.options:
                        self.options['sourcefile'] = ''
                    else:
                        self.options['sourcefile'] = "data-sourcefile='%s'" % self.options['sourcefile']
                    if 'tie' in self.options:
                        self.options['tie'] = "data-tie='{}'".format(self.options['tie'])
                    else:
                        self.options['tie'] = ''
                    if 'dburl' in self.options:
                        self.options['dburl'] = "data-dburl='{}'".format(self.options['dburl'])
                    else:
                        self.options['dburl'] = ''
                    for opt, tp in (('compileargs', 'cargs'), ('linkargs', 'largs'),
                                    ('runargs', 'rargs'), ('interpreterargs', 'iargs')):
                        if opt in self.options:
                            self.options[tp] = 'data-{}="{}"'.format(opt, escape(self.options[opt]))
                        else:
                            self.options[tp] = ''

                    if 'gradebutton' not in self.options:
                        self.options['gradebutton'] = ''
                    else:
                        self.options['gradebutton'] = 'data-gradebutton=true'
                    self.options['divclass'] = env.config.activecode_div_class
                    if env.config.activecode_hide_load_history:
                        self.options['hidehistory'] = 'data-hidehistory=true'
                    else:
                        self.options['hidehistory'] = ''
                if env.config.wasm_uri:
                    self.options['wasmuri'] = f"data-wasm={env.config.wasm_uri}"
                else:
                    self.options['wasmuri'] = ''
            if self.content:
                if '====' in self.content:
                    idx = self.content.index('====')
                    source = '\n'.join(self.content[:idx])
                    suffix = '\n'.join(self.content[idx + 1:])
                else:
                    source = '\n'.join(self.content)
                    suffix = '\n'
            else:
                source = '\n'
            suffix = '\n'
        course_name = env.config.html_context['course_id']
        divid = self.options['divid']
        if engine:
            engine.execute(Source_code.delete().where(Source_code.c.acid == divid).where(Source_code.c.course_id == course_name))
            engine.execute(Source_code.insert().values(acid=divid,
              course_id=course_name,
              main_code=source,
              suffix_code=suffix,
              includes=(self.options['include']),
              available_files=(self.options.get('available_files', ''))))
        else:
            if not (hasattr(env, 'dberr_activecode_reported') and env.dberr_activecode_reported):
                env.dberr_activecode_reported = True
                print('Unable to save to source_code table in activecode.py. Possible problems:')
                print('  1. dburl or course_id are not set in conf.py for your book')
                print('  2. unable to connect to the database using dburl')
                print('')
                print('This should only affect the grading interface. Everything else should be fine.')
            acnode = ActivcodeNode((self.options), rawsource=(self.block_text))
            acnode.source, acnode.line = self.state_machine.get_source_and_line(self.lineno)
            self.add_name(acnode)
            if explain_text:
                self.state.nested_parse(explain_text, self.content_offset, acnode)
            return [acnode]


class ActiveExercise(ActiveCode):
    required_arguments = 1
    optional_arguments = 0
    has_content = True

    def run(self):
        self.options['hidecode'] = 'data-hidecode=true'
        self.options['gradebutton'] = 'data-gradebutton=true'
        self.options['coach'] = 'data-coach=true'
        return super(ActiveExercise, self).run()


if __name__ == '__main__':
    a = ActiveCode()