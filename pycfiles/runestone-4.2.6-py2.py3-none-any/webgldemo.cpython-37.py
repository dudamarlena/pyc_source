# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /srv/RunestoneComponents/runestone/webgldemo/webgldemo.py
# Compiled at: 2020-04-16 12:40:55
# Size of source mod 2**32: 43567 bytes
from docutils import nodes
from docutils.parsers.rst import directives
from docutils.parsers.rst import Directive
import string, re, os
__author__ = 'wayne brown'

def setup(app):
    app.add_directive('webgldemo', WebglDemo)
    app.add_autoversioned_stylesheet('webgldemo.css')
    app.add_node(WebglDemoNode, html=(visit_webgldemo_node, depart_webgldemo_node))
    app.connect('doctree-resolved', process_webgldemo_nodes)
    app.connect('env-purge-doc', purge_webgldemos)
    app.add_directive('webglinteractive', WebglInteractive)
    app.add_autoversioned_stylesheet('webglinteractive.css')
    app.add_autoversioned_javascript('webglinteractive.js')
    app.add_autoversioned_javascript('FileSaver.min.js')
    app.add_autoversioned_javascript('Blob.js')
    app.add_node(WebglInteractiveNode,
      html=(
     visit_webglinteractive_node, depart_webglinteractive_node))
    app.connect('doctree-resolved', process_webglinteractive_nodes)
    app.connect('env-purge-doc', purge_webglinteractive)


def find_relative_path(env, options):
    documentName = env.temp_data['docname']
    documentPath, documentName = os.path.split(documentName)
    path_list = documentPath.split(os.sep)
    if len(path_list) > 1:
        levels_deep = len(path_list)
    else:
        if len(path_list[0]) > 0:
            levels_deep = 1
        else:
            levels_deep = 0
    folder_prefix = '_static' + os.sep
    for j in range(levels_deep):
        folder_prefix = '..' + os.sep + folder_prefix

    options['lib_folder_prefix'] = folder_prefix
    folder_prefix = ''
    for j in range(levels_deep):
        folder_prefix = '..' + os.sep + folder_prefix

    options['program_folder_prefix'] = folder_prefix


class WebglDemo(Directive):
    __doc__ = '\n.. webgldemo:: uniqueid\n    :htmlprogram: path/to/program/webgl_program.html\n    :width: -- width of rendering canvas in pixels (default is value set in HTML)\n    :height: -- height of rendering canvas in pixels (default is value set in HTML)\n    :width2: -- width of secondary rendering canvas in pixels (default is value set in HTML)\n    :height2: -- height of secondary rendering canvas in pixels (default is value set in HTML)\n\n    The following assumptions are made about the structure of a textbook that\n    uses this directive:\n        * All WebGL programs are stored under the _static folder, each in a\n          separate folder. (This causes the files to be automatically copied\n          to the "build" folder when a "runestone build" is performed.)\n          Therefore, the path to a WebGL program will always be some like:\n          _static/example_folder/example.html\n        * The parent folder of all WebGL HTML programs will always be\n          "_static". Therefore, ".." always refers to the "_static" folder.\n        * When a WebGL program is included into a lesson web page, the\n          references to other files must be adjusted based on the path\n          from the lesson page to the "_static" folder.\n        * A specific lesson can contain one or more webgl programs.\n            * HTML ids for tags must be unique for each separate program.\n            * Each webgldemo must have a unique id, which is used to rename\n              HTML element tags and Javascript variables.\n            * Your HTML program should name id\'s and variables with a "my_" prefix.\n              When the HTML program is included in the web page, the webgldemo\n              unique id is put in every location of "my_". This allows a demo\n              program to be used more than once on a page. For example,\n              if you have a webgldemo named W1 and you have tags in your\n              HTML like my_canvas, my_button, etc., then those names are\n              converted to W1_canvas, W1_button, etc. when the program is\n              loaded into the web page.\n            * A webgl program embedded in a lesson page always includes a\n              link to open the example program in a separate window. This\n              allows a student to use a browser\'s "view page source"\n              functionality to view only the webgl program, separate from\n              the textbook\'s lesson page.\n\n    Because of the above assumptions and conventions, the HTML description of\n    a webgl program is written as if it is a single, standalone program that\n    can be loaded into the student\'s web browser from a sub-folder of the _static\n    folder of the textbook.\n\n    When a webgl directive is executed, it does the following:\n        * It extracts the body of the webgl HTML code and inserts the contents\n          into the textbook page being built.\n        * It modifies the file paths to the Javascript files, shader files,\n            and model files so that they can be loaded from the lesson page\'s\n            location, not the location of the program in the _static folder.\n            These changes are summarized as follows:\n            Changes:  "../learn_webgl"  to  "../_static/learn_webgl"\n            Changes:  "../shaders"      to  "../_static/shaders"\n            Changes:  "../models"       to  "../_static/models"\n            Changes:  "src="./"         to  "src="../\' + node.webgl_components[\'htmlprogrampath\'] + "/")\n        * The Javascript code at the bottom of a webgl program needs to be\n          in the HTML code so that the runestone build process can modify\n          the paths to these webgl program resources. The "Learn Computer Graphics\n          using Webgl" textbook explains that in a "normal" webgl program, the\n          Javascript code at the bottom would typically be moved into an\n          appropriate Javascript code file.\n\n    The default size for a webgl canvas is 400 by 400 pixels. The size of the\n    canvas can be modified using the optional directive parameters.\n\n    A typical webglcode directive will look like this:\n\n        .. webgldemo:: W1\n            :htmlprogram: _static/01_example01/scale_about_origin.html\n            :width: 200\n            :height: 200\n\n    '
    required_arguments = 1
    optional_arguments = 0
    has_content = False
    option_spec = {'htmlprogram':directives.unchanged, 
     'width':directives.unchanged, 
     'height':directives.unchanged, 
     'width2':directives.unchanged, 
     'height2':directives.unchanged}

    def run(self):
        self.options['divid'] = self.arguments[0]
        if 'htmlprogram' in self.options:
            path, name = os.path.split(self.options['htmlprogram'])
            self.options['htmlprogrampath'] = path
            self.options['htmlprogram'] = name
            find_relative_path(self.state.document.settings.env, self.options)
            if 'width' in self.options:
                self.options['width'] = int(self.options['width'])
            else:
                self.options['width'] = 0
            if 'height' in self.options:
                self.options['height'] = int(self.options['height'])
            else:
                self.options['height'] = 0
            if 'width2' in self.options:
                self.options['width2'] = int(self.options['width2'])
            else:
                self.options['width2'] = 0
            if 'height2' in self.options:
                self.options['height2'] = int(self.options['height2'])
            else:
                self.options['height2'] = 0
        else:
            print('ERROR: An htmlprogram value is required for a webgldemo directive.')
        return [
         WebglDemoNode(self.options)]


class WebglDemoNode(nodes.General, nodes.Element):

    def __init__(self, content):
        super(WebglDemoNode, self).__init__()
        self.webgl_components = content


def visit_webgldemo_node(self, node):
    res = '<!-- webgldemo start -->\n'
    res += "<div id='%(divid)s_webgldemo' class='webgldemo_container'>\n"
    filename = os.path.join(node.webgl_components['htmlprogrampath'], node.webgl_components['htmlprogram'])
    file = open(filename, 'r')
    fileContents = file.read()
    file.close()
    startPos = fileContents.find('<body')
    startPos = fileContents.find('>', startPos) + 1
    endPos = fileContents.find('</body>')
    bodyCode = fileContents[startPos:endPos]
    bodyCode = bodyCode.replace('../', node.webgl_components['lib_folder_prefix'])
    bodyCode = bodyCode.replace('src="./', 'src="' + node.webgl_components['program_folder_prefix'] + node.webgl_components['htmlprogrampath'] + os.sep)
    if node.webgl_components['width'] > 0:
        if node.webgl_components['height'] > 0:
            width_re = re.compile('<canvas id="my_canvas" class="webgldemo_canvas" width="(\\d+)" height="(\\d+)">')
            if width_re.search(bodyCode):
                new_text = '<canvas id="my_canvas" class="webgldemo_canvas" width="' + str(node.webgl_components['width']) + '" height="' + str(node.webgl_components['height']) + '">'
                bodyCode = width_re.sub(new_text, bodyCode)
    if node.webgl_components['width2'] > 0:
        if node.webgl_components['height2'] > 0:
            width_re = re.compile('<canvas id="my_canvas_b" class="webgldemo_canvas" width="(\\d+)" height="(\\d+)">')
            if width_re.search(bodyCode):
                new_text = '<canvas id="my_canvas_b" class="webgldemo_canvas" width="' + str(node.webgl_components['width2']) + '" height="' + str(node.webgl_components['height2']) + '">'
                bodyCode = width_re.sub(new_text, bodyCode)
    bodyCode = bodyCode.replace('my_', node.webgl_components['divid'] + '_')
    bodyCode = bodyCode.replace('"my",', '"' + node.webgl_components['divid'] + '",')
    res += bodyCode
    programPath = node.webgl_components['htmlprogrampath'].replace('_static/', '')
    myLink = os.path.join(node.webgl_components['lib_folder_prefix'], programPath, node.webgl_components['htmlprogram'])
    res += '<a href="' + myLink + '" target="_blank">Open this webgl demo program in a new tab or window</a>'
    res += '</div>\n'
    res += '<!-- webgldemo end -->'
    res = res % node.webgl_components
    self.body.append(res)


def depart_webgldemo_node(self, node):
    """
    This is called at the start of processing an activecode node.  If activecode had recursive nodes
    etc and did not want to do all of the processing in visit_webgldemo_node any finishing touches could be
    added here.
    """
    pass


def process_webgldemo_nodes(app, env, docname):
    pass


def purge_webgldemos(app, env, docname):
    pass


class WebglInteractive(Directive):
    __doc__ = '\n.. webglinteractive:: uniqueid\n    :htmlprogram: path/to/program/webgl_program.html\n    :editList: comma separated list of files that can be edited\n    :viewList: comma sepatated list of files that can be viewed, but not edited\n    :width: -- width of rendering canvas in pixels (default is value in HTML)\n    :height: -- height of rendering canvas in pixels (default is value in HTML)\n    :width2: -- width of secondary rendering canvas in pixels (default is value in HTML)\n    :height2: -- height of secondary rendering canvas in pixels (default is value in HTML)\n    :hidecode: -- if present, the code is not initially displayed\n    :hideoutput: -- if present, the output area below the code is not initially displayed\n\n    The following assumptions are made about the structure of a textbook that\n    uses this directive:\n        * A lesson can contain one or more webgl programs.\n            * HTML ids for tags must be unique for each separate program.\n            * Each webgldemo must have a unique id, which is used to rename\n              HTML element tags and Javascript variables.\n            * Your HTML program should name id\'s and variables with a "my_" prefix.\n              When the HTML program is included in the web page, the webgldemo\n              unique id is put in every location of "my_". This allows a demo\n              program to be used more than once on a page. For example,\n              if you have a webgldemo named W1 and you have tags in your\n              HTML like my_canvas, my_button, etc., then those names are\n              converted to W1_canvas, W1_button, etc. when the program is\n              loaded into the web page.\n            * A webgl program embedded in a lesson page always includes a\n              link to open the example program in a separate window. This\n              allows a student to use a browser\'s "view page source"\n              functionality to view only the webgl program, separate from\n              the textbook\'s lesson page.\n        * The example webgl programs included in a lesson are stored in the\n          _static folders. (All files in the _static folders are automatically\n          copied to the _static folder of the deployed textbook.)\n        * Each webgl program has its own folder.\n\n    Because of the above assumptions and conventions, the HTML description of\n    a webgl program is written as if it is a single, standalone program that\n    can be loaded into the student\'s web browser from a sub-folder of the _static\n    folder of the textbook.\n\n    When a webgl directive is executed, it does the following:\n        * It extracts the body of the webgl HTML code and inserts the contents\n          into the textbook page being built.\n        * It modifies the file paths to the Javascript files, shader files,\n            and model files so that they can be loaded from the lesson page\'s\n            location, not the location of the program in the _static folder.\n            These changes are summarized as follows:\n            Changes:  "../learn_webgl"  to  "../_static/learn_webgl"\n            Changes:  "../shaders"      to  "../_static/shaders"\n            Changes:  "../models"       to  "../_static/models"\n            Changes:  "src="./"         to  "src="../\' + node.webgl_components[\'htmlprogrampath\'] + "/")\n        * The Javascript code at the bottom of a webgl program needs to be\n          in the HTML code so that the runestone build process can modify\n          the paths to these webgl program resources. The "Learn Computer Graphics\n          usign Webgl" textbook explains that in a "normal" webgl program, the\n          Javascript code at the bottom would typically be moved into an\n          appropriate Javascript code file.\n\n    The default size for a webgl canvas is 400 by 400 pixels. The size of the\n    canvas can be modified using the optional directive parameters.\n\n    A typical webglinteactive directive will look like this:\n\n        .. webglinteractive:: W1\n            :htmlprogram: _static/01_example01/scale_about_origin.html\n            :editlist: _static/01_example01/scale_about_origin_render.js, _static/01_example01/model.js\n            :width: 200\n            :height: 200\n\n    '
    required_arguments = 1
    optional_arguments = 0
    has_content = False
    option_spec = {'htmlprogram':directives.unchanged, 
     'editlist':directives.unchanged, 
     'viewlist':directives.unchanged, 
     'hidecode':directives.flag, 
     'hideoutput':directives.flag, 
     'width':directives.unchanged, 
     'height':directives.unchanged, 
     'width2':directives.unchanged, 
     'height2':directives.unchanged}

    def run(self):
        env = self.state.document.settings.env
        if not hasattr(env, 'webglinteractivecounter'):
            env.webglinteractivecounter = 0
        else:
            env.webglinteractivecounter += 1
            self.options['divid'] = self.arguments[0]
            self.options['hidecanvas'] = False
            self.options['hideoutput'] = 'hideoutput' in self.options
            self.options['hidecode'] = 'hidecode' in self.options
            if 'htmlprogram' in self.options:
                htmlprogram_folders = self.options['htmlprogram'].split('/')
                htmlprogram_path = '/'.join(htmlprogram_folders[0:-1])
                htmlprogram_path = htmlprogram_path.strip()
                self.options['htmlprogram'] = htmlprogram_folders[(-1)]
                self.options['htmlprogrampath'] = htmlprogram_path
            else:
                print('***** ERROR: An htmlprogram is required for a webglinteractive directive.')
            if 'editlist' in self.options:
                self.options['editlist'] = self.options['editlist'].split(',')
            else:
                self.options['editlist'] = []
            if 'viewlist' in self.options:
                self.options['viewlist'] = self.options['viewlist'].split(',')
            else:
                self.options['viewlist'] = []
            if 'width' in self.options:
                self.options['width'] = int(self.options['width'])
            else:
                self.options['width'] = 0
            if 'height' in self.options:
                self.options['height'] = int(self.options['height'])
            else:
                self.options['height'] = 0
            if 'width2' in self.options:
                self.options['width2'] = int(self.options['width2'])
            else:
                self.options['width2'] = 0
            if 'height2' in self.options:
                self.options['height2'] = int(self.options['height2'])
            else:
                self.options['height2'] = 0
        find_relative_path(self.state.document.settings.env, self.options)
        return [
         WebglInteractiveNode(self.options)]


OUTPUT_OPTIONS = '\n<div>\nShow:\n<input type="checkbox" id="%(divid)s_webgl_displayInfo" name="Display" value="InfoMessages" checked=\'checked\' />\n<span id="webgl_infoMessages" class="webgl_infoMessages">Process information &nbsp&nbsp</span>\n<input type="checkbox" id="%(divid)s_webgl_displayWarnings" name="Display" value="Warnings" checked=\'checked\' />\n<span id="webgl_warningMessages" class="webgl_warningMessages">Warnings &nbsp&nbsp</span>\n<input type="checkbox" id="%(divid)s_webgl_displayErrors" name="Display" value="Errors" checked=\'checked\' />\n<span id="webgl_errorMessages" class="webgl_errorMessages">Errors</span>\n</div>\n'
OUTPUT_WINDOW = '\n<div id="%(divid)s_webgl_output_div" class="webgl_output_div">\n</div>\n'
TAB_BEGIN = "<div id='%(divid)s_editors' class='webgl_code'>"
TAB_END = '</div>'
SHOW_HIDE_SCRIPT = '\n    <script type=\'text/javascript\'>\n        %(divid)s_directive.show_webgl("%(divid)s_show_code",1);\n        %(divid)s_directive.show_webgl("%(divid)s_show_canvas",2);\n        %(divid)s_directive.show_webgl("%(divid)s_show_info",3);\n        %(divid)s_directive.set_height_of_webgl_editors("%(divid)s");\n        %(divid)s_directive.bring_first_editor_to_front("%(divid)s");\n    </script>\n'
TAB_TITLES_LIST_BEGIN = "<ul class='webgl_nav_tabs' id='%(divid)s_tab'>"
TAB_TITLES_LIST_END = '</ul>'
TAB_LIST_ELEMENT = "\n<li>\n    <a data-toggle='tab' href='#%(divid)s_%(tabname)s'><span>%(tabtitle)s</span></a>\n</li>\n"
TAB_CONTENTS_BEGIN = '<div style=\'width:100%%; position:relative;\'>\n<div class="webgl_code">'
TAB_CONTENTS_END = '\n<div style="clear:both;"></div>\n</div>\n</div>\n'
TAB_DIV_BEGIN = "<div class='webgl_tab_content' id='%(divid)s_%(tabname)s'>"
TAB_DIV_END = '</div>'
TABBED_EDITOR = '\n<textarea id="%(tabid)s_textarea" class="webgl_tabbed_editor">\n%(fileContents)s\n</textarea>\n\n<script>\n    %(divid)s_directive.createCodeMirrorEditor(\'%(tabid)s\', \'%(filename)s\', \'%(fileextension)s\' %(readonly)s);\n</script>\n'

class WebglInteractiveNode(nodes.General, nodes.Element):

    def __init__(self, content):
        super(WebglInteractiveNode, self).__init__()
        self.webgl_components = content


def add_commands(options):
    res = ''
    res += "<button class='btn btn-success' id='%(divid)s_runb' onclick='%(divid)s_directive.restart();'>Re-start</button>\n"
    res += 'Show: \n'
    if options['hidecode']:
        res += '<input type=\'checkbox\' id=\'%(divid)s_show_code\' onclick=\'%(divid)s_directive.show_webgl("%(divid)s_show_code",1);\' />Code &nbsp\n'
    else:
        res += '<input type=\'checkbox\' id=\'%(divid)s_show_code\' onclick=\'%(divid)s_directive.show_webgl("%(divid)s_show_code",1);\' checked=\'checked\' />Code &nbsp\n'
    if options['hidecanvas']:
        res += '<input type=\'checkbox\' id=\'%(divid)s_show_canvas\' onclick=\'%(divid)s_directive.show_webgl("%(divid)s_show_canvas",2);\' />Canvas &nbsp\n'
    else:
        res += '<input type=\'checkbox\' id=\'%(divid)s_show_canvas\' onclick=\'%(divid)s_directive.show_webgl("%(divid)s_show_canvas",2);\' checked=\'checked\' />Canvas &nbsp\n'
    if options['hideoutput']:
        res += '<input type=\'checkbox\' id=\'%(divid)s_show_info\' onclick=\'%(divid)s_directive.show_webgl("%(divid)s_show_info",3);\'/>Run Info\n'
    else:
        res += '<input type=\'checkbox\' id=\'%(divid)s_show_info\' onclick=\'%(divid)s_directive.show_webgl("%(divid)s_show_info",3);\' checked=\'checked\' />Run Info\n'
    res += "<button class='btn webgl-default' id='%(divid)s_saveall' onclick='%(divid)s_directive.downloadAllFiles();'\n"
    res += "title='Download a copy of all the original\nfiles required for this WebGL program.'>Download Files</button>\n"
    res += "<button class='btn webgl-default' id='%(divid)s_save_edited' onclick='%(divid)s_directive.downloadEditedFiles();'\n"
    res += "title='Download a copy of all the\nfiles in the editor panels.'>Download Edited Files</button>\n"
    return res


def change_html_code_ids(bodyCode, webgl_components):
    if webgl_components['width'] > 0:
        if webgl_components['height'] > 0:
            width_re = re.compile('<canvas id="my_canvas" class="webgldemo_canvas" width="(\\d+)" height="(\\d+)">')
            if width_re.search(bodyCode):
                new_text = '<canvas id="my_canvas" class="webgldemo_canvas" width="' + str(webgl_components['width']) + '" height="' + str(webgl_components['height']) + '">'
                bodyCode = width_re.sub(new_text, bodyCode)
    if webgl_components['width2'] > 0:
        if webgl_components['height2'] > 0:
            width_re = re.compile('<canvas id="my_canvas_b" class="webgldemo_canvas" width="(\\d+)" height="(\\d+)">')
            if width_re.search(bodyCode):
                new_text = '<canvas id="my_canvas_b" class="webgldemo_canvas" width="' + str(webgl_components['width2']) + '" height="' + str(webgl_components['height2']) + '">'
                bodyCode = width_re.sub(new_text, bodyCode)
    bodyCode = bodyCode.replace('my_', webgl_components['divid'] + '_')
    bodyCode = bodyCode.replace('"my",', '"' + webgl_components['divid'] + '",')
    return bodyCode


def add_code_editors(options):
    res = ''
    res += TAB_TITLES_LIST_BEGIN
    number_to_edit = len(options['editlist'])
    for j in range(0, number_to_edit):
        tab_name = options['editlist'][j]
        folders = tab_name.split('/')
        if len(folders) > 1:
            tab_title = folders[(len(folders) - 1)].strip()
        else:
            tab_title = tab_name.strip()
        tab_name = tab_title.replace('.', '_').strip()
        res += TAB_LIST_ELEMENT % {'divid':options['divid'], 
         'tabname':tab_name, 
         'tabtitle':tab_title}

    number_to_view = len(options['viewlist'])
    for j in range(0, number_to_view):
        tab_name = options['viewlist'][j]
        folders = tab_name.split('/')
        if len(folders) > 1:
            tab_title = folders[(len(folders) - 1)].strip()
        else:
            tab_title = tab_name.strip()
        tab_name = tab_title.replace('.', '_').strip()
        res += TAB_LIST_ELEMENT % {'divid':options['divid'], 
         'tabname':tab_name, 
         'tabtitle':tab_title}

    res += TAB_TITLES_LIST_END
    res += TAB_CONTENTS_BEGIN
    for j in range(0, number_to_edit):
        edit_name = options['editlist'][j]
        folders = edit_name.split('/')
        if len(folders) > 1:
            file_name = folders[(len(folders) - 1)].strip()
        else:
            file_name = edit_name.strip()
        dot_pos = file_name.find('.')
        fileExtension = file_name[dot_pos + 1:]
        tab_name = file_name.replace('.', '_').strip()
        tab_id = options['divid'] + '_' + tab_name
        tab_file = options['editlist'][j].strip()
        tab_file = os.path.abspath(tab_file)
        file = open(tab_file, 'r')
        fileContents = file.read()
        file.close()
        if fileExtension == 'html':
            fileContents = change_html_code_ids(fileContents, options)
        res += TAB_DIV_BEGIN % {'divid':options['divid'],  'tabname':tab_name}
        res += TABBED_EDITOR % {'divid':options['divid'], 
         'tabid':tab_id, 
         'tabfile':edit_name, 
         'fileContents':fileContents, 
         'filename':file_name, 
         'fileextension':fileExtension, 
         'readonly':''}
        res += TAB_DIV_END

    for j in range(0, number_to_view):
        view_name = options['viewlist'][j]
        folders = view_name.split('/')
        if len(folders) > 1:
            file_name = folders[(len(folders) - 1)].strip()
        else:
            file_name = view_name.strip()
        dot_pos = file_name.find('.')
        fileExtension = file_name[dot_pos + 1:]
        tab_name = file_name.replace('.', '_').strip()
        tab_id = options['divid'] + '_' + tab_name
        tab_file = options['viewlist'][j].strip()
        tab_file = os.path.abspath(tab_file)
        file = open(tab_file, 'r')
        fileContents = file.read()
        file.close()
        if fileExtension == 'html':
            fileContents = change_html_code_ids(fileContents, options)
        res += TAB_DIV_BEGIN % {'divid':options['divid'],  'tabname':tab_name}
        res += TABBED_EDITOR % {'divid':options['divid'], 
         'tabid':tab_id, 
         'tabfile':view_name, 
         'fileContents':fileContents, 
         'filename':file_name, 
         'fileextension':fileExtension, 
         'readonly':', true'}
        res += TAB_DIV_END

    res += TAB_CONTENTS_END
    return res


def visit_webglinteractive_node(self, node):
    res = '<!-- webglinteractive start -->'
    res += "\n  <script>\n    var %(divid)s_directive = new WebglInteractive_directive( '%(divid)s' );\n  </script>\n  "
    res += "<div class='webgl_container' id='%(divid)s_webgl_container'>\n"
    res += "<div class='webgl_cmds' id='%(divid)s_webgl_cmds'>\n"
    res += add_commands(node.webgl_components)
    res += '</div>\n'
    res += "<div class='webgl_row2' id='%(divid)s_webgl_row2'>\n"
    res += "<div class='webgl_editors' id='%(divid)s_webgl_editors'>\n"
    res += add_code_editors(node.webgl_components)
    res += '</div>\n'
    res += "<div class='webgl_canvas' id='%(divid)s_webgl_canvas'>"
    filename = node.webgl_components['htmlprogrampath'] + '/' + node.webgl_components['htmlprogram']
    filename = os.path.realpath(filename)
    file = open(filename, 'r')
    fileContents = file.read()
    file.close()
    html_file_name = '../' + node.webgl_components['htmlprogrampath'] + '/' + node.webgl_components['htmlprogram']
    res += '<span style="display: none;">' + html_file_name + '</span>'
    startPos = fileContents.find('<body')
    startPos = fileContents.find('>', startPos) + 1
    endPos = fileContents.find('</body>')
    bodyCode = fileContents[startPos:endPos]
    bodyCode = bodyCode.replace('../', node.webgl_components['lib_folder_prefix'])
    bodyCode = bodyCode.replace('src="./', 'src="' + node.webgl_components['program_folder_prefix'] + node.webgl_components['htmlprogrampath'] + os.sep)
    bodyCode = change_html_code_ids(bodyCode, node.webgl_components)
    res += bodyCode
    res += '</div>\n'
    res += "<div style='clear:both;'></div>"
    res += '</div>\n'
    res += "<div class='webgl_output' id='%(divid)s_webgl_output'>"
    res += OUTPUT_OPTIONS
    res += OUTPUT_WINDOW
    res += '</div>\n'
    res += "<div style='clear:both;'></div>\n"
    programPath = node.webgl_components['htmlprogrampath'].replace('_static/', '')
    myLink = os.path.join(node.webgl_components['lib_folder_prefix'], programPath, node.webgl_components['htmlprogram'])
    res += '<a href="' + myLink + '" target="_blank">Open this webgl program in a new tab or window</a>'
    res += '</div>\n'
    res += SHOW_HIDE_SCRIPT
    res += '<!-- webglinteractive end -->'
    res += '<p> </p>\n'
    res = res % node.webgl_components
    self.body.append(res)


def depart_webglinteractive_node(self, node):
    """ This is called at the start of processing an activecode node.  If activecode had recursive nodes
        etc and did not want to do all of the processing in depart_webglinteractive_node any finishing touches could be
        added here.
    """
    pass


def process_webglinteractive_nodes(app, env, docname):
    pass


def purge_webglinteractive(app, env, docname):
    pass