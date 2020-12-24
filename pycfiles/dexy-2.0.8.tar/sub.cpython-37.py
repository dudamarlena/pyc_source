# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ana/dev/dexy-clean/dexy/filters/sub.py
# Compiled at: 2020-03-18 15:12:33
# Size of source mod 2**32: 19155 bytes
from dexy.filters.process import SubprocessExtToFormatFilter
from dexy.filters.process import SubprocessFilter
from dexy.filters.process import SubprocessFormatFlagFilter
from dexy.filters.process import SubprocessInputFilter
from dexy.filters.process import SubprocessStdoutFilter
from dexy.utils import file_exists
import dexy.exceptions, json, os, shutil

class Kramdown(SubprocessStdoutFilter):
    __doc__ = '\n    Runs the kramdown markdown converter.\n\n    http://kramdown.gettalong.org/\n    '
    aliases = ['kramdown']
    _settings = {'added-in-version':'1.0.5', 
     'class':'SubprocessExtToFormatFilter', 
     'executable':'kramdown', 
     'version-command':'kramdown -version', 
     'output':True, 
     'format-specifier':'-o ', 
     'ext-to-format':{'.tex':'latex', 
      '.html':'html',  '.md':'kramdown',  '.txt':'kramdown'}, 
     'input-extensions':[
      '.*'], 
     'output-extensions':[
      '.html', '.tex', '.txt', '.md'], 
     'require-output':True, 
     'command-string':'%(prog)s %(format)s %(args)s "%(script_file)s"'}

    def command_string_args(self):
        args = self.default_command_string_args()
        fmt_specifier = self.setting('format-specifier')
        if fmt_specifier and fmt_specifier in args['args']:
            fmt = ''
        else:
            fmt_setting = self.setting('ext-to-format')[self.ext]
            if fmt_setting:
                fmt = '%s%s' % (fmt_specifier, fmt_setting)
            else:
                fmt = ''
        args['format'] = fmt
        return args


class Redcarpet(SubprocessStdoutFilter):
    __doc__ = '\n    Converts github-flavored markdown to HTML using redcarpet.\n    '
    aliases = ['redcarpet', 'ghmd']
    _settings = {'added-in-version':'1.0.1', 
     'executable':'redcarpet', 
     'input-extensions':[
      '.md', '.txt'], 
     'output-extensions':[
      '.html'], 
     'parse-autolink':('autolink option from redcarpet', True), 
     'parse-disabled-indented-code-blocks':('disabled-indented-code-blocks option from redcarpet', False), 
     'parse-fenced-code-blocks':('fenced-code-blocks option from redcarpet', True), 
     'parse-highlight':('highlight option from redcarpet', True), 
     'parse-lax-spacing':('lax-spacing option from redcarpet', True), 
     'parse-no-intra-emphasis':('no-intra-emphasis option from redcarpet', True), 
     'parse-quotes':('quotes option from redcarpet', True), 
     'parse-space-after-headers':('space-after-headers option from redcarpet', True), 
     'parse-strikethrough':('strikethrough option from redcarpet', True), 
     'parse-subscript':('subscript option from redcarpet', True), 
     'parse-superscript':('superscript option from redcarpet', True), 
     'parse-tables':('tables option from redcarpet', True), 
     'parse-underline':('underline option from redcarpet', True), 
     'render-filter-html':('filter-html option from redcarpet', False), 
     'render-no-images':('no-images option from redcarpet', False), 
     'render-no-links':('no-links option from redcarpet', False), 
     'render-no-styles':('no-styles option from redcarpet', False), 
     'render-safe-links-only':('safe-links-only option from redcarpet', False), 
     'render-with-toc-data':('with-toc-data option from redcarpet', False), 
     'render-hard-wrap':('hard-wrap option from redcarpet', False), 
     'render-prettify':('prettify option from redcarpet', False), 
     'render-xhtml':('xhtml option from redcarpet', False), 
     'pygments':('Pygments syntax highlighting (requires ananelson/redcarpet fork).', False)}

    def command_string(self):
        args = self.command_string_args()
        args['parse_args'] = ' '.join(('--%s' % name for name in args if name.startswith('parse-') if args[name]))
        args['render_args'] = ' '.join(('--%s' % name for name in args if name.startswith('render-') if args[name]))
        other_args = [
         'pygments']
        args['other_args'] = ' '.join(('--%s' % name for name in other_args if args[name]))
        return '%(prog)s %(parse_args)s %(render_args)s %(other_args)s %(script_file)s' % args


class TidyCheck(SubprocessFilter):
    __doc__ = '\n    Runs `tidy` to check for valid HTML.\n\n    This filter does not alter valid HTML. It raises an Exception if invalid\n    HTML is found.\n    '
    aliases = ['tidycheck']
    _settings = {'examples':[
      'tidy'], 
     'tags':[
      'html'], 
     'executable':'tidy', 
     'command-string':'%(prog)s -errors -quiet "%(script_file)s"', 
     'input-extensions':[
      '.html'], 
     'output-extensions':[
      '.txt']}

    def process(self):
        command = self.command_string()
        proc, stdout = self.run_command(command, self.setup_env())
        self.handle_subprocess_proc_return(command, proc.returncode, stdout)
        self.output_data.copy_from_file(self.input_data.storage.data_file())


class PdfToCairo(SubprocessFormatFlagFilter):
    __doc__ = '\n    Runs `pdftocairo` from the poppler library.\n\n    Converts PDF input to various output formats inclusing SVG.\n    '
    aliases = ['pdftocairo', 'pdf2cairo', 'pdf2svg', 'pdftosvg']
    _settings = {'command-string':'%(prog)s %(format)s %(args)s "%(script_file)s" "%(output_file)s"', 
     'executable':'pdftocairo', 
     'tags':[
      'pdf', 'image'], 
     'input-extensions':[
      '.pdf'], 
     'output-extensions':[
      '.svg', '.png', '.jpg', '.ps', '.eps', '.pdf'], 
     'ext-to-format':{'.png':'-png', 
      '.jpg':'-jpeg', 
      '.ps':'-ps', 
      '.eps':'-eps', 
      '.pdf':'-pdf', 
      '.svg':'-svg'}}

    def process(self):
        command = self.command_string()
        proc, stdout = self.run_command(command, self.setup_env())
        self.handle_subprocess_proc_return(command, proc.returncode, stdout)
        if not self.output_data.is_cached():
            for pagenum in ('1', '01', '001', '0001'):
                basename = os.path.join(self.workspace(), self.output_data.name)
                first_page_file = '%s-%s.png' % (basename, pagenum)
                if file_exists(first_page_file):
                    print("Copy from '%s'" % first_page_file)
                    self.output_data.copy_from_file(first_page_file)
                    break

        assert self.output_data.is_cached()
        if self.setting('add-new-files'):
            self.log_debug('adding new files found in %s for %s' % (self.workspace(), self.key))
            self.add_new_files()


class Pdf2ImgSubprocessFilter(SubprocessExtToFormatFilter):
    __doc__ = '\n    Runs ghostscript to convert PDF files to images.\n\n    An image file can only hold a single page of PDF, so this defaults to\n    returning page 1. The `page` setting can be used to specify other pages.\n    '
    aliases = ['pdf2img', 'pdftoimg', 'pdf2png']
    _settings = {'res':('Resolution of image.', 300), 
     'page':('Which page of the PDF to return as an image', 1), 
     'executable':'gs', 
     'version-command':'gs --version', 
     'tags':[
      'pdf', 'gs'], 
     'input-extensions':[
      '.pdf'], 
     'output-extensions':[
      '.png'], 
     'ext-to-format':{'.png':'png16m', 
      '.jpg':'jpeg'}, 
     'format-specifier':'-sDEVICE=', 
     'command-string':'%(prog)s -dSAFER -dNOPAUSE -dBATCH %(format)s -r%(res)s -sOutputFile="%%d-%(output_file)s" "%(script_file)s"'}

    def process(self):
        self.populate_workspace()
        command = self.command_string()
        proc, stdout = self.run_command(command, self.setup_env())
        self.handle_subprocess_proc_return(command, proc.returncode, stdout)
        page = self.setting('page')
        page_file = '%s-%s' % (page, self.output_data.basename())
        wd = self.parent_work_dir()
        page_path = os.path.join(wd, page_file)
        shutil.copyfile(page_path, self.output_filepath())


class RIntBatchSectionsFilter(SubprocessFilter):
    __doc__ = '\n    Experimental filter to run R in sections without using pexpect.\n    '
    aliases = ['rintmock']
    _settings = {'add-new-files':True, 
     'executable':'R CMD BATCH --quiet --no-timing', 
     'tags':[
      'rstats', 'repl', 'stats'], 
     'input-extensions':[
      '.txt', '.r', '.R'], 
     'output-extensions':[
      '.Rout', '.txt'], 
     'version-command':'R --version', 
     'write-stderr-to-stdout':False, 
     'data-type':'sectioned', 
     'command-string':'%(prog)s %(args)s "%(script_file)s" %(scriptargs)s "%(output_file)s" '}

    def command_string(self, section_name, section_text, wd):
        br = self.input_data.baserootname()
        args = self.default_command_string_args()
        args['script_file'] = '%s-%s%s' % (br, section_name, self.input_data.ext)
        args['output_file'] = '%s-%s-out%s' % (br, section_name, self.output_data.ext)
        work_filepath = os.path.join(wd, args['script_file'])
        with open(work_filepath, 'w') as (f):
            f.write(str(section_text))
        command = self.setting('command-string') % args
        return (command, args['output_file'])

    def process(self):
        self.populate_workspace()
        wd = self.parent_work_dir()
        for section_name, section_text in self.input_data.items():
            command, outfile = self.command_string(section_name, section_text, wd)
            proc, stdout = self.run_command(command, self.setup_env())
            self.handle_subprocess_proc_return(command, proc.returncode, stdout)
            with open(os.path.join(wd, outfile), 'r') as (f):
                self.output_data[section_name] = f.read()

        if self.setting('add-new-files'):
            self.add_new_files()
        self.output_data.save()


class EmbedFonts(SubprocessFilter):
    __doc__ = '\n    Runs ghostscript ps2pdf with prepress settings.\n\n    Allegedly this helps embed fonts and makes documents friendly for printing.\n    '
    aliases = ['embedfonts', 'prepress']
    _settings = {'input-extensions':[
      '.pdf'], 
     'output-extensions':[
      '.pdf'], 
     'executable':'ps2pdf', 
     'tags':[
      'pdf']}

    def preprocess_command_string(self):
        pf = self.work_input_filename()
        af = self.work_output_filename()
        return '%s -dPDFSETTINGS=/prepress %s %s' % (self.setting('executable'), pf, af)

    def pdffonts_command_string(self):
        return '%s %s' % ('pdffonts', self.result().name)

    def process(self):
        env = self.setup_env()
        command = self.preprocess_command_string()
        proc, stdout = self.run_command(command, env)
        self.handle_subprocess_proc_return(command, proc.returncode, stdout)
        command = self.pdffonts_command_string()
        proc, stdout = self.run_command(command, env)
        self.handle_subprocess_proc_return(command, proc.returncode, stdout)
        self.copy_canonical_file()


class AbcFilter(SubprocessFormatFlagFilter):
    __doc__ = '\n    Runs `abcm2ps` on .abc music files.\n    '
    aliases = ['abc']
    _settings = {'command-string':'%(prog)s %(args)s %(format)s -O %(output_file)s %(script_file)s', 
     'add-new-files':False, 
     'output':True, 
     'tags':[
      'music'], 
     'examples':[
      'abc'], 
     'executable':'abcm2ps', 
     'input-extensions':[
      '.abc'], 
     'output-extensions':[
      '.svg', '.html', '.xhtml', '.eps'], 
     'ext-to-format':{'.eps':'-E', 
      '.svg':'-g', 
      '.svg1':'-v', 
      '.html':'-X', 
      '.xhtml':'-X'}}

    def process(self):
        command = self.command_string()
        proc, stdout = self.run_command(command, self.setup_env())
        self.handle_subprocess_proc_return(command, proc.returncode, stdout)
        if self.ext in ('.svg', '.eps'):
            nameparts = os.path.splitext(self.output_data.name)
            output_filename = '%s001%s' % (nameparts[0], nameparts[1])
            output_filepath = os.path.join(self.workspace(), output_filename)
            self.output_data.copy_from_file(output_filepath)
        else:
            self.copy_canonical_file()
        if self.setting('add-new-files'):
            self.add_new_files()


class AbcMultipleFormatsFilter(SubprocessFilter):
    __doc__ = '\n    Runs `abcm2ps` on .abc music files, generating all output formats.\n    '
    aliases = ['abcm']
    _settings = {'input-extensions':[
      '.abc'], 
     'output-extensions':[
      '.json'], 
     'executable':'abcm2ps', 
     'tags':[
      'music'], 
     'add-new-files':False}

    def command_string(self, ext):
        clargs = self.command_line_args() or ''
        if any((x in clargs for x in ('-E', '-g', '-v', '-X'))):
            raise dexy.exceptions.UserFeedback('Please do not pass any output format flags!')
        elif ext in '.eps':
            output_flag = '-E'
        else:
            if ext in '.svg':
                output_flag = '-g'
            else:
                if ext in ('.html', '.xhtml'):
                    output_flag = '-X'
                else:
                    raise dexy.exceptions.InternalDexyProblem("bad ext '%s'" % ext)
        args = {'prog':self.setting('executable'), 
         'args':clargs, 
         'output_flag':output_flag, 
         'script_file':self.work_input_filename(), 
         'output_file':self.output_workfile(ext)}
        return '%(prog)s %(args)s %(output_flag)s -O %(output_file)s %(script_file)s' % args

    def output_workfile(self, ext):
        return '%s%s' % (self.output_data.baserootname(), ext)

    def process(self):
        output = {}
        wd = self.parent_work_dir()
        for ext in ('.eps', '.svg', '.html', '.xhtml'):
            command = self.command_string(ext)
            proc, stdout = self.run_command(command, self.setup_env())
            self.handle_subprocess_proc_return(command, proc.returncode, stdout)
            if ext in ('.svg', '.eps'):
                nameparts = os.path.splitext(self.output_workfile(ext))
                output_filename = '%s001%s' % (nameparts[0], nameparts[1])
                output_filepath = os.path.join(wd, output_filename)
            else:
                output_filename = self.output_workfile(ext)
                output_filepath = os.path.join(wd, output_filename)
            with open(output_filepath, 'r') as (f):
                output[ext] = f.read()

        self.output_data.set_data(json.dumps(output))


class ManPage(SubprocessStdoutFilter):
    __doc__ = '\n    Read command names from a file and fetch man pages for each.\n\n    Returns a JSON dict whose keys are the program names and values are man\n    pages.\n    '
    aliases = ['man']
    _settings = {'executable':'man', 
     'tags':[
      'utils'], 
     'version-command':'man --version', 
     'input-extensions':[
      '.txt'], 
     'output-extensions':[
      '.json']}

    def command_string(self, prog_name):
        return 'bash -c "set -e; set -o pipefail; man %s | col -b | strings"' % prog_name

    def process(self):
        man_info = {}
        for prog_name in str(self.input_data).split():
            command = self.command_string(prog_name)
            proc, stdout = self.run_command(command, self.setup_env())
            self.handle_subprocess_proc_return(command, proc.returncode, stdout)
            man_info[prog_name] = stdout

        self.output_data.set_data(json.dumps(man_info))


class ApplySed(SubprocessInputFilter):
    __doc__ = '\n    Runs `sed` on the input file.\n\n    Expects a sed script to be a dependency.\n    '
    aliases = ['used']
    _settings = {'executable':'sed', 
     'tags':[
      'utils'], 
     'data-type':'generic'}

    def process(self):
        for doc in self.doc.walk_input_docs():
            if doc.output_data().ext == '.sed':
                command = '%s -f %s' % (self.setting('executable'), doc.name)

        if not command:
            raise dexy.exceptions.UserFeedback('A .sed file must be passed as an input to %s' % self.key)
        proc, stdout = self.run_command(command, self.setup_env(), str(self.input_data))
        self.handle_subprocess_proc_return(command, proc.returncode, stdout)
        self.output_data.set_data(stdout.rstrip('\n'))


class Sed(SubprocessInputFilter):
    __doc__ = '\n    Runs a sed script.\n\n    Any dependencies are assumed to be text files and they have the sed script\n    applied to them.\n    '
    aliases = ['sed']
    _settings = {'executable':'sed', 
     'tags':[
      'utils'], 
     'input-extensions':[
      '.sed'], 
     'output-extensions':[
      '.sed', '.txt']}

    def command_string(self):
        return '%s -f %s' % (self.setting('executable'), self.work_input_filename())


class Taverna(SubprocessStdoutFilter):
    __doc__ = '\n    Runs workflows in Taverna via command line tool.\n    '
    aliases = ['taverna']
    _settings = {'executable':'taverna', 
     'tags':[
      'repro', 'workflow'], 
     'add-new-files':True, 
     'input-extensions':[
      '.t2flow'], 
     'output-extensions':[
      '.txt'], 
     'taverna-home':('Location of taverna home directory.', '$TAVERNA_HOME'), 
     'x-max':('Java -Xmx setting', '300m'), 
     'x-perm-max':('Java -XX:MaxPermSize setting', '140m')}

    def command_string(self):
        assert self.setting('taverna-home')
        return 'java -Xmx%(x-max)s -XX:MaxPermSize=%(x-perm-max)s \\\n                -Draven.profile=file://%(taverna-home)s/conf/current-profile.xml \\\n                -Dtaverna.startup=%(taverna-home)s \\\n                -Djava.system.class.loader=net.sf.taverna.raven.prelauncher.BootstrapClassLoader \\\n                -Draven.launcher.app.main=net.sf.taverna.t2.commandline.CommandLineLauncher \\\n                -Draven.launcher.show_splashscreen=false \\\n                -Djava.awt.headless=true \\\n                -jar "%(taverna-home)s/lib/"prelauncher-*.jar \\\n                %(script_file)s' % self.command_string_args()