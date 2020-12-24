# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/will/projects/moya/moya/command/sub/start.py
# Compiled at: 2016-12-08 16:29:22
from __future__ import unicode_literals
from __future__ import print_function
from __future__ import absolute_import
import fs.copy
from fs.opener import open_fs
from fs import walk
from ...command import SubCommand
from ...console import Cell
from ...command.sub import templatebuilder
from ...compat import text_type, raw_input
import sys
try:
    import readline
except ImportError:
    pass

import random

def make_secret(size=64, allowed_chars=b'0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!#$%&()*+,-./:;<=>?@[]^_`{|}~'):
    """make a secret key"""
    try:
        choice = random.SystemRandom().choice
    except:
        choice = random.choice

    return (b'').join(choice(allowed_chars) for _ in range(size))


def make_name(*names):
    names = [ (b'').join(c for c in name.lower() if c.isalpha() or c.isdigit()) for name in names
            ]
    return (b'.').join(names)


def copy_new(src, dst):
    """Copy files from src fs to dst fst only if they don't exist on dst"""
    fs.copy.copy_structure(src, dst)
    copied_files = []
    for path in src.walk.files():
        if not dst.exists(path):
            fs.copy.copy_file(src, path, dst, path)
            copied_files.append(path)

    return copied_files


class Question(object):
    text = b'Which pill do you take?'
    alert = None
    extra = None
    responses = None
    examples = None
    required = True
    accept_defaults = False

    @classmethod
    def ask(cls, console, default=None):
        question_text = cls.text + b' '
        while True:
            if cls.alert:
                console.wraptext(cls.alert, fg=b'red', bold=True)
            console(question_text, bold=True)
            if default is not None:
                console.text((b' {} ').format(default or b'<leave blank>'), fg=b'blue', bold=True)
            else:
                console.nl()
            if not (cls.accept_defaults and default is not None):
                if cls.extra:
                    console.table([[cls.extra]])
                if cls.examples:
                    console(b'e.g. ', fg=b'blue', bold=True)(cls.examples[0], fg=b'green').nl()
                    for e in cls.examples[1:]:
                        console(b'     ')(e, fg=b'green').nl()

            if cls.accept_defaults and default is not None:
                response = cls.process_input(default)
                if not isinstance(response, text_type):
                    response = response.decode(sys.getdefaultencoding(), b'replace')
                break
            try:
                response = raw_input()
            except KeyboardInterrupt:
                console.nl().text(b'\rCanceled', bold=True, fg=b'red')
                raise

            if not isinstance(response, text_type):
                response = response.decode(sys.getdefaultencoding(), b'replace')
            response = cls.process_input(response)
            if not response and default is not None:
                response = default
            if cls.required and not response.strip():
                console.text(b'This question requires an answer to continue', fg=b'red')
                continue
            if cls.responses is not None and response not in cls.responses:
                console.text(b'Not a valid response, please try again', fg=b'red')
                continue
            break

        return cls.process_response(response)

    @classmethod
    def process_input(cls, text):
        return text

    @classmethod
    def process_response(cls, response):
        return response


class YesNoQuestion(Question):
    responses = [
     b'y', b'yes', b'n', b'no']

    @classmethod
    def process_input(cls, response):
        return response.strip().lower()

    @classmethod
    def process_response(cls, response):
        return response.lower() in ('y', 'yes')


class Name(Question):
    text = b'What is your name?'


class Email(Question):
    text = b'What is your email address?'


class Organization(Question):
    text = b'What is your organization?'
    extra = b'This may be your employer, organization or your own name'


class URL(Question):
    text = b'What is your homepage URL?'
    required = False


class DoMount(YesNoQuestion):
    text = b'Do you want to mount this library?'


class ProjectTitle(Question):
    text = b'What is the title of your project?'


class ProjectLongName(Question):
    text = b"What is the 'long name' of your project?"
    extra = b"Moya 'long names' are globally unique identifiers. A long name consists of two or more words separated by dots. The first word should be unique to you (i.e. your name or organization), subsequent words should identify the project."
    examples = [b'bob.blog',
     b'acmesoftware.kitchen.sink']


class ProjectDirName(Question):
    text = b'Where should Moya write the project files?'


class Preview(YesNoQuestion):
    text = b'Would you like to preview the files that will be generated?'


class ContinueWrite(YesNoQuestion):
    text = b'Write project files?'


class DirNotEmpty(Question):
    text = b'The destination directory is not empty! If you continue, files may be overwritten and data lost.'
    extra = b"'cancel' to exit without writing files\n'overwrite' to overwrite any existing files\n'new' to write only new files."
    responses = [b'overwrite', b'cancel', b'new']


class Database(YesNoQuestion):
    text = b'Do you want database support?'


class Auth(YesNoQuestion):
    text = b'Enable Moya auth support?'
    extra = b'Enable if you want to support users with authentication and permissions (a requirement for most dynamic sites).'


class Signup(YesNoQuestion):
    text = b'Enable Moya signup support?'
    enable = b'Enable to allow users to create accounts.'


class JSONRPC(YesNoQuestion):
    text = b'Enable JSON RPC support for your site?'
    extra = b'Enable to provide an API you can use to expose code and data (see http://json-rpc.org/).'


class Pages(YesNoQuestion):
    text = b'Enable pages application?'
    extra = b'moya.pages is a simple content management system useful for about/contact pages etc.'


class Blog(YesNoQuestion):
    text = b'Enable blog application?'
    extra = b'moya.blog is a simple, but feature complete, blog system.'


class Feedback(YesNoQuestion):
    text = b'Enable feedback application?'
    extra = b'moya.feedback provides a feedback form visitors can use to email you.'


class LibraryTitle(Question):
    text = b'What is the title of your library?'


class LibraryURL(Question):
    text = b'What is the URL of your library?'
    extra = b"It's a good idea to provide a URL for your library that contains more information about it. Leave this blank if you want to fill it in later."
    examples = [b'http://example.org/moya/awesomelib.html']
    required = False


class LibraryLongName(Question):
    text = b"What is the 'long name' of your library?"
    extra = b"Moya 'long names' are globally unique identifiers. A long name consistst of two or more words separated by dots. The first word should be unique to you (i.e. your name or organization), subsequent words should identify the library."
    examples = [b'bob.blog',
     b'acmesoftware.kitchen.sink']


class LibraryNamespace(Question):
    text = b'What xml namespace do you want to use for your library?'
    extra = b"The namespace will be used for any tags you define. You can leave this blank if you won't be creating any tags, or if you prefer to enter this later."
    examples = [b'http://acmesoftware.com/namespaces/libs',
     b'http://example.org/blog']
    required = False


class Mount(Question):
    text = b'What URL would you like to mount the new library on?'
    examples = [b'/blog/',
     b'/shop/beetles/']
    required = False


class AppName(Question):
    text = b'What should the application be named?'
    extra = b"A mounted application requires a 'short name', which should be a single word, no space or dots."
    examples = [b'myblog',
     b'beetlesshop']
    required = False


class Start(SubCommand):
    """Start a Moya library or project"""
    help = b'command line wizard to create a project or library'

    def add_arguments(Self, parser):
        parser.add_argument(b'--templatize', dest=b'templatize', metavar=b'PATH', help=b'make a filesystem template (used internally, not required for general use)')
        subparser = parser.add_subparsers(title=b'start sub-command', dest=b'type', help=b'what to create')

        def add_common(parser):
            parser.add_argument(b'-l', dest=b'project_location', default=b'./', metavar=b'PATH', help=b'location of the Moya server code')
            parser.add_argument(b'-i', b'--ini', dest=b'settings', default=None, metavar=b'SETTINGSPATH', help=b'path to project settings file')
            parser.add_argument(b'-o', dest=b'location', metavar=b'PATH', default=None, help=b'location of new project / library')
            parser.add_argument(b'-a', b'--accept-defaults', dest=b'acceptdefaults', action=b'store_true', default=False, help=b'automatically accept all defaults')
            parser.add_argument(b'-t', b'--title', dest=b'title', help=b'project / library title')
            parser.add_argument(b'-f', b'--force', dest=b'force', action=b'store_true', default=False, help=b'force overwriting of files if destination directory is not empty')
            parser.add_argument(b'-n', b'--new', dest=b'new', action=b'store_true', default=False, help=b'write new files only')
            return parser

        add_common(subparser.add_parser(b'project', help=b'start a new Moya project', description=b'Start a new Moya project'))
        parser = add_common(subparser.add_parser(b'library', help=b'start a new library in a Moya project', description=b'Start a new library in a Moya project'))
        parser.add_argument(b'--mount', dest=b'mount', default=None, metavar=b'URL PATH', help=b'URL where the library should be mounted')
        parser.add_argument(b'--longname', dest=b'longname', default=None, metavar=b'LONG NAME', help=b'Name of the installed library')
        parser.add_argument(b'--name', dest=b'name', default=None, metavar=b'APPLICATION NAME', help=b'Application name if the lib is mounted')
        return parser

    def run(self):
        args = self.args
        Question.accept_defaults = args.acceptdefaults
        if args.templatize:
            return self.templatize(args.templatize)
        if args.type.lower() == b'project':
            return self.start_project()
        if args.type.lower() == b'library':
            return self.start_library()
        raise ValueError(b"Type should be either 'project' or 'library'")

    def templatize(self, path):
        from fs.opener import open_fs
        from fs.path import splitext, split
        fs = open_fs(path)
        text_ext = [b'', b'.py', b'.ini', b'.xml', b'.html', b'.txt', b'.json']
        bin_ext = [b'.png', b'.jpg', b'.ico', b'.gif']

        def check_path(path):
            dirname, filename = split(path)
            return filename not in ('.svn', '.hg')

        for path in fs.walk.files():
            if check_path(path):
                continue
            _, ext = splitext(path)
            ext = ext.lower()
            if ext in text_ext:
                print((b'@TEXT {}').format(path))
                for line in fs.open(path, b'rt'):
                    print(line.rstrip())

            elif ext in bin_ext:
                print((b'@BIN {}').format(path))
                with fs.open(path, b'rb') as (f):
                    chunk = f.read(64)
                    while chunk:
                        print((b'').join(b'%02x' % ord(b) for b in chunk))
                        chunk = f.read(64)

    def get_timezone(self):
        try:
            with open(b'/etc/timezone') as (f):
                timezone = f.read()
        except IOError:
            timezone = b'UTC'

        return timezone

    def start_project(self):
        console = self.console
        if not self.args.acceptdefaults:
            console.table([[Cell(b'Moya Project Wizard', bold=True, fg=b'green', center=True)],
             [
              b'This will ask you a few questions, then create a new Moya project based on your answers.\n\nDefault values are shown in blue (hit return to accept defaults). Some defaults may be taken from your ".moyarc" file, if it exists.']])
        author = self.get_author_details()
        project = {}
        project[b'title'] = ProjectTitle.ask(console, default=self.args.title)
        longname = make_name(author[b'organization'], project[b'title'])
        project[b'database'] = Database.ask(console, default=b'y')
        if project[b'database']:
            project[b'auth'] = Auth.ask(console, default=b'y')
            project[b'signup'] = Signup.ask(console, default=b'y')
            project[b'pages'] = Pages.ask(console, default=b'y')
            project[b'blog'] = Blog.ask(console, default=b'y')
        project[b'feedback'] = Feedback.ask(console, default=b'y')
        project[b'comments'] = project.get(b'blog', False) or project.get(b'pages', False)
        project[b'wysihtml5'] = project.get(b'blog', False) or project.get(b'pages', False)
        project[b'jsonrpc'] = JSONRPC.ask(console, default=b'y')
        dirname = longname.split(b'.', 1)[(-1)].replace(b'.', b'_')
        dirname = ProjectDirName.ask(console, default=b'./' + dirname)
        data = {b'author': author, 
           b'project': project, 
           b'timezone': self.get_timezone(), 
           b'secret': make_secret()}
        from ...command.sub import project_template
        memfs = open_fs(b'mem://')
        templatebuilder.compile_fs_template(memfs, project_template.template, data=data)
        dest_fs = open_fs(self.args.location or dirname, create=True, writeable=True)
        continue_overwrite = b'overwrite'
        if not dest_fs.isempty(b'.'):
            if self.args.force:
                continue_overwrite = b'overwrite'
            elif self.args.new:
                continue_overwrite = b'new'
            else:
                continue_overwrite = DirNotEmpty.ask(console, default=b'cancel')
        if continue_overwrite == b'overwrite':
            fs.copy.copy_dir(memfs, b'/', dest_fs, b'/')
            console.table([[Cell(b'Project files written successfully!', fg=b'green', bold=True, center=True)],
             [
              b'See readme.txt in the project directory for the next steps.\n\nBrowse to http://moyaproject.com/gettingstarted/ if you need further help.']])
            return 0
        if continue_overwrite == b'new':
            files_copied = copy_new(memfs, dest_fs)
            table = [
             [
              Cell((b'{} new file(s) written').format(len(files_copied)), fg=b'green', bold=True, center=True)]]
            for path in files_copied:
                table.append([Cell(dest_fs.desc(path), bold=True, fg=b'black')])

            console.table(table)
            return 0
        console.text(b'No project files written.', fg=b'red', bold=True).nl()
        return -1

    def start_library(self):
        console = self.console
        from ...tools import get_moya_dir
        from os.path import join, abspath
        project_path = None
        if self.args.location is not None:
            library_path = self.args.location
        else:
            try:
                project_path = get_moya_dir(self.args.project_location)
            except:
                console.error(b"Please run 'moya start library' inside your project directory, or specifiy the -o switch")
                return False

            library_path = abspath(join(project_path, b'./local/'))
        cfg = None
        if not self.args.location and project_path:
            from ... import build
            cfg = build.read_config(project_path, self.get_settings())
        if not self.args.acceptdefaults:
            console.table([[Cell(b'Moya Library Wizard', bold=True, fg=b'green', center=True)],
             [
              b'This will ask you a few questions, then create a new library in your Moya project based on your answers.\n\nDefault values are shown in grey (simply hit return to accept defaults). Some defaults may be taken from your ".moyarc" file, if it exists.\n']])
        author = self.get_author_details()
        library = {}
        library[b'title'] = LibraryTitle.ask(console, default=self.args.title)
        longname = self.args.longname or make_name(author[b'organization'], library[b'title'])
        longname = library[b'longname'] = LibraryLongName.ask(console, default=longname)
        library[b'url'] = LibraryURL.ask(console, default=b'')
        library[b'namespace'] = LibraryNamespace.ask(console, default=b'')
        mount = None
        appname = None
        do_mount = DoMount.ask(console, default=b'yes')
        if do_mount:
            mount = Mount.ask(console, default=self.args.mount or (b'/{}/').format(make_name(library[b'title'])))
            appname = AppName.ask(console, default=self.args.name or make_name(library[b'title']))
        data = dict(author=author, library=library, timezone=self.get_timezone())
        actions = []
        from ...command.sub import library_template
        memfs = open_fs(b'mem://')
        templatebuilder.compile_fs_template(memfs, library_template.template, data=data)
        dest_fs = open_fs(join(library_path, library[b'longname']), create=True, writeable=True)
        continue_overwrite = b'overwrite'
        if not dest_fs.isempty(b'/'):
            if self.args.force:
                continue_overwrite = b'overwrite'
            elif self.args.new:
                continue_overwrite = b'new'
            else:
                continue_overwrite = DirNotEmpty.ask(console, default=b'cancel')
        if continue_overwrite != b'cancel':
            if continue_overwrite == b'overwrite':
                fs.copy.copy_dir(memfs, b'/', dest_fs, b'/')
                actions.append((b'Written library files to {}').format(dest_fs.getsyspath(b'.')))
            elif continue_overwrite == b'new':
                files_copied = copy_new(memfs, dest_fs)
                table = [
                 [
                  Cell((b'{} new file(s) written').format(len(files_copied)), fg=b'green', bold=True, center=True)]]
                for path in files_copied:
                    table.append([Cell(dest_fs.desc(path), bold=True, fg=b'black')])

                console.table(table)
                return 0
            if cfg:
                project_cfg = cfg[b'project']
                location = project_cfg[b'location']
                server_name = b'main'
                if location:
                    with open_fs(project_path) as (project_fs):
                        with project_fs.opendir(location) as (server_fs):
                            from lxml.etree import fromstring, ElementTree, parse
                            from lxml.etree import XML, Comment
                            server_xml_path = server_fs.getsyspath(project_cfg[b'startup'])
                            root = parse(server_xml_path)
                            import_tag = XML((b'<import location="./local/{longname}" />\n\n').format(**library))
                            import_tag.tail = b'\n'
                            install_tag = None
                            if mount:
                                tag = b'<install name="{appname}" lib="{longname}" mount="{mount}" />'
                            else:
                                tag = b'<install name="{appname}" lib="{longname}" />'
                            install_tag = XML(tag.format(appname=appname, longname=longname, mount=mount))
                            install_tag.tail = b'\n\n'

                            def has_child(node, tag, **attribs):
                                for el in node.findall(tag):
                                    if all(el.get(k, None) == v for k, v in attribs.items()):
                                        return True

                                return False

                            for server in root.findall((b"{{http://moyaproject.com}}server[@docname='{}']").format(server_name)):
                                add_import_tag = not has_child(server, b'{http://moyaproject.com}import', location=(b'./local/{}').format(longname))
                                add_install_tag = not has_child(server, b'{http://moyaproject.com}install', lib=longname) and install_tag is not None
                                if add_import_tag or add_install_tag:
                                    comment = Comment(b"Added by 'moya start library'")
                                    comment.tail = b'\n'
                                    server.append(comment)
                                if add_import_tag:
                                    server.append(import_tag)
                                    actions.append(b'Added <import> tag')
                                if add_install_tag:
                                    server.append(install_tag)
                                    actions.append(b'Added <install> tag')
                                    if mount:
                                        actions.append((b'Mounted application on {}').format(mount))

                            root.write(server_xml_path)
            table = [
             [
              Cell(b'Library files written successfully!', fg=b'green', bold=True, center=True)]]
            actions_text = (b'\n').join(b' * ' + action for action in actions)
            table.append([Cell(actions_text, fg=b'blue', bold=True)])
            table.append([b'A new library has been added to the project, containing some simple example functionality.\nSee http://moyaproject.com/docs/creatinglibraries/ for more information.'])
            console.table(table)
            return 0
        else:
            console.text(b'No project files written.', fg=b'red', bold=True).nl()
            return -1

    def get_author_details(self):
        console = self.console
        moyarc = self.moyarc
        author = {}
        author[b'name'] = Name.ask(console, default=moyarc.get(b'author', b'name', None))
        author[b'email'] = Email.ask(console, default=moyarc.get(b'author', b'email', None))
        author[b'url'] = URL.ask(console, default=moyarc.get(b'author', b'url', None))
        author[b'organization'] = Organization.ask(console, default=moyarc.get(b'author', b'organization', None))
        return author