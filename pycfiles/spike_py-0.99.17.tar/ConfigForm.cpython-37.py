# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/mad/Documents/spike/spike/util/ConfigForm.py
# Compiled at: 2018-11-07 05:49:54
# Size of source mod 2**32: 28754 bytes
from __future__ import print_function
import sys, os, unittest
from collections import OrderedDict, defaultdict
import ConfigParser, threading, webbrowser, random, socket, wtforms
from wtforms import Form, validators, ValidationError
from jinja2 import Template
from flask import Flask, Response, render_template, request, url_for, redirect
from PyQt4 import QtGui
HOST = 'localhost'
PORT = 5000
DEBUG = False
STARTWEB = False
METHOD = 'POST'
__version__ = '0.2'
COLOR_TOOLTIP = 'PapayaWhip'
head = '\n<!DOCTYPE html>\n<html>\n<head>\n\n<script src="https://ajax.googleapis.com/ajax/libs/jquery/1.11.2/jquery.min.js"></script>\n<script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.4/js/bootstrap.min.js"></script>\n<script src="https://cdnjs.cloudflare.com/ajax/libs/bootstrap-select/1.7.2/js/bootstrap-select.min.js"></script>\n<script>\n\n$(document).ready(function(){$(\'[data-toggle="tooltip"]\').tooltip();});\n\n</script>\n\n<!-- Css -->\n<link rel="stylesheet" href="http://maxcdn.bootstrapcdn.com/bootstrap/3.3.4/css/bootstrap.min.css"><!-- Scripts -->\n<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/bootstrap-select/1.7.2/css/bootstrap-select.css">\n\n<style>\n.CF-tooltip + .tooltip > .tooltip-inner { background-color: PapayaWhip; text-align : left}\n.CF-tooltip + .tooltip > .tooltip-arrow { border-bottom-color: PapayaWhip; }\n#namefile, #namefile_button\n{\n    display:inline;\n}\n\n\n</style>\n\n<title>{{title}}</title>\n</head>\n\n'
foot = '\n<p><small><i>ConfigForm, version %s  - author : M.A. Delsuc</i></small></p>\n' % __version__
cfFieldDef = {'%boolean%':(
  wtforms.StringField, bool), 
 '%text%':(
  wtforms.StringField, str), 
 '%float%':(
  wtforms.FloatField, float), 
 '%integer%':(
  wtforms.IntegerField, int), 
 '%radio%':(
  wtforms.RadioField, str), 
 '%file%':(
  wtforms.FileField, str), 
 '%infile%':(
  wtforms.FileField, str), 
 '%outfile%':(
  wtforms.StringField, str), 
 '%select%':(
  wtforms.SelectField, str), 
 '%hidden%':(
  wtforms.HiddenField, str)}
cfFieldKeys = cfFieldDef.keys()
if DEBUG:
    print(cfFieldKeys)
cfvalDef = {'%options':validators.AnyOf, 
 '%extension':validators.Regexp, 
 '%min':validators.NumberRange, 
 '%max':validators.NumberRange, 
 '%length':None, 
 '%tooltip':None}
cfvalDefKeys = cfvalDef.keys()
if DEBUG:
    print(cfvalDefKeys)

def dForm(dico):
    """
    This function creates a wtforms object from the description given in the (Ordered) dict dico 
    dico = {"name_of_field" : Field(), ...}

    This is the key, wtforms requires a class describing the form, we have to build it dynamically.
    """

    class C(Form):
        pass

    for i, j in dico.items():
        setattr(C, i, j)

    return C


def dynatemplate(kw, method, action, class_):
    """builds a simplistic template string, see  dTemplate()  - used for tests -"""
    temp = [
     '<form method="{0}" action="{1}">'.format(method, action)]
    for i in kw:
        temp.append('<div>{{{{ form.{0}.label }}}}: {{{{ form.{0}(class="{1}") }}}}</div>'.format(i, class_))

    temp.append('</form>')
    return '\n'.join(temp)


def dTemplate(dico, method, action, class_):
    """
    This function creates a simple Template object from the description given in the (Ordered) dict dico
    method is either POST or GET
    action is the callback url
    class_ is the css class attached to each field
    
    used for tests
    """
    return Template(dynatemplate(dico, method, action, class_))


class FIND_FOLDER_FILE(QtGui.QWidget):
    __doc__ = '\n    PyQt interface for chosing the folder for the processing.\n    '

    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.curDir = os.getcwd()

    def browse(self, kind):
        """
        Search for a folder or a file
        """
        print('saving config')
        if kind == 'folder':
            self.selected = QtGui.QFileDialog.getExistingDirectory(self, 'Select Folder', self.curDir)
        else:
            if kind == 'file':
                self.selected = QtGui.QFileDialog.getOpenFileName(self, 'Open file', self.curDir)
        print('#################### self.selected ', self.selected)


def search_folder_file(kind):
    """
    Opens the PyQt interface for searching the folder
    When the folder is chosen the program stops the Qt interface. 
    """
    app = QtGui.QApplication(sys.argv)
    ff = FIND_FOLDER_FILE()
    ff.browse(kind)
    return ff.selected


class cfField(object):
    __doc__ = '\n    This class holds all the parameters of an option in the config file\n\n    subparse_comment() loads it    \n    '

    def __init__(self, name, value):
        self.name = name
        self.value = value
        self.class_ = 'CF'
        self.type_ = '%text%'
        self.length = 60
        self.tooltip = []
        self.tooltip_color = COLOR_TOOLTIP
        self.doc = ''
        self.section = ''
        self.lopt = None
        self.meta = None
        self.validators = [validators.DataRequired()]

    def subparse_comment(self, line):
        """parse the comment, and search for meta comments"""
        import re
        words = re.findall('%.+?%', line)
        if not words:
            words = [
             line]
        print(words)
        word = words.pop(0)
        if word not in cfFieldKeys:
            self.doc.append(line)
            return
        self.type_ = word
        self.meta = line
        for word in words:
            val = word[:-1].split(':')
            if val[0] in cfvalDefKeys:
                if val[0] == '%min':
                    if cfFieldDef[self.type_][1] == str:
                        self.validators.append(validators.Length(min=(int(val[1]))))
                        self.tooltip.append('minimum length : %d' % int(val[1]))
                    else:
                        self.validators.append(validators.NumberRange(min=(float(val[1]))))
                        self.tooltip.append('minimum value : %d' % float(val[1]))
                elif val[0] == '%max':
                    if cfFieldDef[self.type_][1] == str:
                        self.validators.append(validators.Length(max=(int(val[1]))))
                        self.length = int(val[1])
                        self.tooltip.append('maximum length : %d' % int(val[1]))
                    else:
                        self.validators.append(validators.NumberRange(max=(float(val[1]))))
                        self.tooltip.append('maximum value : %d' % float(val[1]))
                elif val[0] == '%extension':
                    print('%Etension:xxx% is currently not implemented')
                    print('XX EXT', val[0], '%s$' % (val[1],))
                    self.tooltip.append('file extension : %s' % (val[1],))
                elif val[0] == '%options':
                    lopt = val[1:]
                    self.lopt = lopt
                    self.validators.append(validators.AnyOf(values=lopt))
                    self.tooltip.append('choose one entry')
                elif val[0] == '%tooltip':
                    self.tooltip.append(val[1])
                elif val[0] == '%length':
                    try:
                        lgt = int(val[1])
                    except:
                        lgt = 60
                        print('WARNING, wrong value in line ', line)

                    self.length = lgt

    def opt_templ(self):
        """build the template for an option stored in cfField"""
        if self.type_ != '%hidden%':
            doc = '<br/>\n'.join(self.doc)
            style_tooltip = "'background-color:{0} ; color:Black' ".format(self.tooltip_color)
            html_tooltip = '<p style=' + style_tooltip + '>' + '<br/>'.join(self.tooltip) + '</p>'
            if self.tooltip:
                ttip = 'data-toggle="tooltip" data-html="true" data-placement="top"  title="{}" class = "CF-tooltip" '.format(html_tooltip)
                print('ttip ', ttip)
            else:
                ttip = ''
            if self.type_ in ('%text%', '%outfile%'):
                print('self.section, self.name ', self.section, self.name)
                templ = '<div class="{2}"><p>{3}<br/><a style="color:black" href="#" {4}>{{{{ form.{0}_{1}.label}}}}</a>:                     {{{{form.{0}_{1}(class="{2}",SIZE="{5}")}}}}</p></div>'.format(self.section, self.name, self.class_, doc, ttip, self.length)
            else:
                if self.type_ in '%select%':
                    print('self.section, self.name ', self.section, self.name)
                    templ = '<div class="{2}" ><p>{3}<br/><a style="color:black" href="#" {4}>{{{{ form.{0}_{1}.label}}}}</a>:                          {{{{form.{0}_{1}(class="selectpicker")}}}} </p></div>'.format(self.section, self.name, self.class_, doc, ttip)
                else:
                    if self.type_ in '%infile%':
                        templ = ' \n                    </br>\n                    <button  type="submit" name="submitform" value="chose_file-{0}_{1}"  class="btn btn-default"> Chose File </button>\n                      {{% if form.{0}_{1}.infilename %}}\n                        <p style="color:blue;"> {{{{form.{0}_{1}.infilename}}}} </p>\n                      {{% endif %}}\n                '.format(self.section, self.name)
                    else:
                        if self.type_ in '%boolean%':
                            print('self.section, self.name ', self.section, self.name)
                            templ = '<div class="{2}"><p>{3}<br/><a style="color:black" href="#" {4}>{{{{ form.{0}_{1}.label}}}}</a>:                   <input type="checkbox" name="{0}_{1}" checked> </p>  </div>  \n'.format(self.section, self.name, self.class_, doc, ttip)
                        else:
                            print('self.section, self.name ', self.section, self.name)
                            templ = '<div class="{2}"><p>{3}<br/><a style="color:black" href="#" {4}>{{{{ form.{0}_{1}.label}}}}</a>:                     {{{{form.{0}_{1}(class="{2}")}}}}</p></div>'.format(self.section, self.name, self.class_, doc, ttip)
        else:
            templ = '{{{{form.{0}_{1}}}}}'.format(self.section, self.name)
        return templ

    def __repr__(self):
        return '%s_%s %s %s %s\n%s' % (self.section, self.name, self.value, self.type_, self.validators, self.doc)

    def __str__(self):
        return self.__repr__()


class ConfigForm(object):
    __doc__ = '\n    This class reads a configparser file\n    creates a HTML form for it\n    starts a broswer on it (using Flask) which allows to modify the values and store them back.\n\n    '

    def __init__(self, cffilename):
        global HOST
        global PORT
        self.cffilename = cffilename
        self.cp = ConfigParser.ConfigParser()
        self.configfile = open(cffilename).readlines()
        self.cp.read(cffilename)
        self.doc_sec = {}
        self.doc_opt = {}
        self.options = OrderedDict()
        self.read_comments()
        self.parse_comments()
        self.method = METHOD
        self.callback = '/callback'
        self.class_ = 'CF'
        self.port = PORT
        self.host = HOST
        self.template = None
        self.form = None

    def reload(self):
        """reload the content from the file"""
        self.configfile = open(self.cffilename).readlines()
        self.cp = ConfigParser.ConfigParser()
        self.cp.read(self.cffilename)
        self.read_comments()
        self.parse_comments()
        self.template = None
        self.form = None

    def read_comments(self):
        """
        this method reads the comments associated to sections and options
        comments should be put BEFORE the commented entry
        ## comments (double #) are silently skipped
        """
        currentsection = 'initial'
        currentoption = None
        currentcom = []
        doc_sec = defaultdict(list)
        doc_opt = defaultdict(list)
        for l in self.configfile:
            l.strip()
            if l.startswith('##'):
                continue
            if l.startswith('#'):
                currentcom.append(l[1:].strip())
                continue
            m = self.cp.SECTCRE.match(l)
            if m:
                currentsection = m.group('header').strip().lower()
                currentoption = None
                doc_sec[currentsection] += currentcom
                currentcom = []
            m = self.cp.OPTCRE.match(l)
            if m:
                currentoption = m.group('option').strip().lower()
                doc_opt[currentoption] += currentcom
                currentcom = []

        self.doc_sec = doc_sec
        self.doc_opt = doc_opt

    def parse_comments(self):
        """parse self.doc_opt and generates self.options"""
        global DEBUG
        for sec in self.cp.sections():
            for opt in self.cp.options(sec):
                cle = '%s_%s' % (sec, opt)
                cff = cfField(opt, self.cp.get(sec, opt))
                cff.doc = []
                cff.section = sec
                cff.opt = opt
                for l in self.doc_opt[opt]:
                    cff.subparse_comment(l)

                if DEBUG:
                    print(cff)
                    print()
                self.options[cle] = cff

    def sect_templ(self, sec):
        """build the template for a section 'sec' """
        doc = '<br/>\n'.join(self.doc_sec[sec])
        print('doc ', doc)
        options_list = [cff.opt_templ() for cff in self.options.values() if cff.section == sec]
        options_templ = '  \n'.join(options_list)
        print('options_templ ', options_templ)
        sec_templ = '\n<div class={0}.section>\n<hr>\n    <div class="jumbotron" style="background-color:Bisque;">\n    <h2  class="text-center">{1}</h2>\n    </div> \n<div class="container">\n<b>{2}</b>\n{3}\n</div>\n</div>\n\n        '.format(self.class_, sec, doc, options_templ)
        return sec_templ

    def buildtemplate(self):
        """builds the jinja2 template string, from the config file"""
        templ = [
         head]
        templ += ['<body>']
        templ += ['<div class="container">']
        templ += [
         '\n            <h1 style="text-align: center;">Configuration for file :  </h1>\n            <h1 style="text-align: center;">{{filename}}</h1>\n        ']
        templ += ['<form method="{0}" action="{1}">'.format(self.method, self.callback)]
        for sec in self.cp.sections():
            templ.append(self.sect_templ(sec))

        templ.append('<hr>\n    <input type="submit" name="submitform" value="Reload Values from file" class="btn btn-default" />')
        templ.append('    <input type="submit" name="submitform" value="Validate Values" class="btn btn-default"/>\n')
        templ.append('</form>')
        templ.append(foot)
        templ += ['</div>']
        templ += [
         '\n</body>\n</html>\n        ']
        return '\n'.join(templ)

    def buildforms(self):
        """build the wtform on the fly from the config file"""
        dico = OrderedDict()
        values = {}
        for cle, content in self.options.items():
            Field_type = cfFieldDef[content.type_][0]
            if content.type_ == '%select%':
                dico[cle] = Field_type((content.name), choices=(zip(content.lopt, content.lopt)), validators=(content.validators))
            else:
                dico[cle] = Field_type((content.name), validators=(content.validators))
            values[cle] = content.value

        df = dForm(dico)
        form = df(**values)
        return form

    def render(self):
        """associate template and wtform to produce html"""
        if self.form is None:
            self.form = self.buildforms()
        if self.template is None:
            self.template = Template(self.buildtemplate())
        html = self.template.render(form=(self.form), title='ConfigForm', filename=(self.cffilename))
        return html

    def produce(self):
        """produces the text of the current defined config file, as a list, one line per entry"""
        text = [
         '## File generated by ConfigForm v %s' % __version__]
        for sec in self.cp.sections():
            text.append('##########################################')
            text += ['# %s' % d for d in self.doc_sec[sec]]
            text.append('[%s]' % sec)
            text.append('')
            for opt in self.cp.options(sec):
                cle = '%s_%s' % (sec, opt)
                text += ['# %s' % d for d in self.options[cle].doc]
                if self.options[cle].meta is not None:
                    text.append('# %s' % self.options[cle].meta)
                text.append('%s = %s' % (opt, self.form[cle].data))
                text.append('')

        return text

    def writeback(self, filename):
        """writes back the config file with the current values"""
        with open(filename, 'w') as (F):
            F.write('\n'.join(self.produce()))


def BuildApp(cffile):
    app = Flask(__name__, static_url_path='/static')
    app.config['SECRET_KEY'] = 'kqjsdhf'
    cf = ConfigForm(cffile)
    cf.callback = '/callback'
    if DEBUG:
        print(cf.doc_sec.keys())

    @app.route('/')
    def index():
        return cf.render()

    @app.route('/callback', methods=[cf.method])
    def callback():
        principal_types = [
         str, float, int]
        bool_cles = []
        not_bool_errors = 0
        text = [
         head]
        text += ['<body>']
        text += ['<div class="container">']
        if request.form['submitform'] == 'Reload Values from file':
            cf.reload()
            return redirect(url_for('index'))
            if request.form['submitform'].find('chose_file') != -1:
                print(' section and name for chose file is : ', request.form['submitform'].split('-')[1])
                cf.infilename = request.form['submitform'].split('-')[1]
                return redirect(url_for('ask_folder'))
                for cle, content in cf.options.items():
                    print('############## cle', cle)
                    print('############## content', content)
                    type_ = cfFieldDef[content.type_][1]
                    if type_ in principal_types:
                        try:
                            cf.form[cle].data = type_(request.form[cle])
                        except:
                            try:
                                cf.form[cle].data = request.form[cle]
                            except:
                                try:
                                    cf.form[cle].data = cf.form[cle].infilename
                                except:
                                    print('no file chosen')
                                    cf.form[cle].data = None

                    else:
                        if request.form.getlist(cle) == []:
                            cf.form[cle].data = False
                        else:
                            cf.form[cle].data = True
                        bool_cles.append(cle)
                    if DEBUG:
                        print('DEBUG')
                        text.append('%s : %s<br/>' % (cle, request.form[cle]))

                text_fine = [
                 '<h1>Everything is fine</h1>\n<p>All entries validated</p>']
                text_fine.append('<p> <a href="{}">write file {}</a>'.format(url_for('write'), cf.cffilename))
                if not cf.form.validate():
                    if len(bool_cles) > 0:
                        text_error = []
                        for name, msges in cf.form.errors.items():
                            nmspl = name.split('_')
                            sec = nmspl[0]
                            opt = '_'.join(nmspl[1:])
                            name_cle = sec + '_' + opt
                            if name_cle not in bool_cles:
                                not_bool_errors += 1
                                for msg in msges:
                                    text_error.append('<li>in section <b>{}</b> entry <b>{}</b> : {}</li>\n'.format(sec, opt, msg))

                        if not_bool_errors > 0:
                            text.append('<h1>Error in config file</h1><p>The following error are detected :</p>')
                            text += text_error
                            text.append('</ul>')
            else:
                text += text_fine
        else:
            text += text_fine
        text.append('<p class="btn btn-default"> <a href="%s">back to form</a> </p> ' % (url_for('index'),))
        text.append(foot)
        text += ['</div>']
        text += [
         '\n            </body>\n            </html>\n                    ']
        valid = '\n'.join(text)
        return valid

    @app.route('/write')
    def write():
        tmpf = '_tempfile.cfg'
        while os.path.exists(tmpf):
            tmpf = '_tempfile_%d.cfg' % int(1000000.0 * random.random())

        print(tmpf)
        cf.writeback(tmpf)
        os.rename(cf.cffilename, cf.cffilename + '~')
        os.rename(tmpf, cf.cffilename)
        return redirect(url_for('bye'))

    @app.route('/ask_folder')
    def ask_folder():
        cf.form[cf.infilename].infilename = search_folder_file('file')
        return redirect(url_for('index'))

    @app.route('/show')
    def show():
        return '<pre>' + '\n'.join(cf.produce()) + '</pre>'

    @app.route('/bye')
    def bye():
        """quitting"""
        return '<H1>Bye !</H1>'

    return app


class ConfigFormTests(unittest.TestCase):
    __doc__ = 'unittests'

    def setUp(self):
        self.verbose = 1

    def announce(self):
        if self.verbose > 0:
            print(self.shortDescription())
            print('----------')

    def _test_dForm(self):
        """testing dForm"""
        self.announce()
        otest = OrderedDict()
        otest['urQRd'] = wtforms.SelectField('do urQRd processing', choices=[(True, 'yes'), (False, 'no')])
        otest['urank'] = wtforms.IntegerField('choose urQRd rank', [validators.NumberRange(min=4, max=100)])
        otest['File'] = wtforms.FileField('File to process')
        df = dForm(otest)
        form2 = df(urank=123)
        temp = dTemplate(otest, 'POST', '/param', 'classX')
        html = temp.render(form=form2)
        print(html)
        self.assertTrue(html.startswith('<form method="POST" action="/param">'))

    def test_render(self):
        """test render"""
        filename = 'test.cfg'
        cf = ConfigForm(filename)


def main():
    """called at start-up"""
    global DEBUG
    global HOST
    global PORT
    global STARTWEB
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('configfile', nargs='?', default='config.cfg', help='the configuration file to analyse, default is config.cfg')
    parser.add_argument('--doc', action='store_true', help='print a description of the program')
    parser.add_argument('-w', '--webserver', default=HOST, help=('the hostname of the server, default is %s' % HOST))
    parser.add_argument('-p', '--port', type=int, default=PORT, help=('the port on which the servers run, default is %d' % PORT))
    parser.add_argument('-s', '--start', help='start the browser on http://WEBSERVER:PORT', action='store_true')
    parser.add_argument('-d', '--debug', default=DEBUG, help='enter debug mode', action='store_true')
    args = parser.parse_args()
    if args.doc:
        print(__doc__)
        sys.exit(0)
    PORT = args.port
    DEBUG = args.debug
    STARTWEB = args.start
    HOST = args.webserver
    filename = args.configfile
    print('Processing ', filename)
    input_file = open(filename).readlines()
    url = 'http://{0}:{1}'.format(HOST, PORT)
    print(url)
    app = BuildApp(filename)
    if STARTWEB:
        threading.Timer(1.5, lambda : webbrowser.open(url)).start()
    try:
        app.run(host=HOST, port=PORT, debug=DEBUG)
    except socket.error:
        print('wrong port number', file=(sys.stderr))
        print('try using another port number (defined in the application header)', file=(sys.stderr))
        return 3
    else:
        return 0


if __name__ == '__main__':
    sys.exit(main())