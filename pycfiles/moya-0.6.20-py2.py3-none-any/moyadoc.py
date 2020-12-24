# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/will/projects/moya/moya/command/moyadoc.py
# Compiled at: 2015-12-04 13:25:09
from __future__ import unicode_literals
from __future__ import print_function
from .. import __version__
from .. import namespaces
from ..settings import SettingsContainer
from .. import build as moya_build
from fs.osfs import OSFS
from fs.path import join, splitext
from fs.watch import CREATED, MODIFIED, REMOVED, MOVED_DST, MOVED_SRC
from fs import utils
from fs.opener import fsopendir
from fs.errors import FSError
import sys, argparse, time
from os.path import dirname, expanduser
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

def _notify(title, message, icon=b'dialog-error'):
    """Show a notification message if pynotify is available"""
    try:
        import pynotify
    except ImportError:
        return

    pynotify.init(b'moya-doc')
    n = pynotify.Notification(title, message, icon)
    n.show()


class ReloadChangeWatcher(FileSystemEventHandler):

    def __init__(self, watch_fs, rebuild):
        self.watching_fs = watch_fs
        self.rebuild = rebuild
        self.last_build_failed = False
        super(ReloadChangeWatcher, self).__init__()

    def on_any_event(self, event):
        path = event.src_path
        ext = splitext(path)[1].lower()
        if ext not in ('.txt', ):
            return
        print((b'file "{}" changed, building...').format(path))
        try:
            self.rebuild()
        except Exception as e:
            _notify(b'moya-doc', (b'Failed to build ({})').format(e))
            import traceback
            traceback.print_exc(e)
            self.last_build_failed = True
        else:
            if self.last_build_failed:
                _notify(b'moya-doc', b'Build successful', icon=b'dialog-information')
            self.last_build_failed = False


class MoyaDoc(object):
    """
    Moya documentation generator

    This builds the documentation for Moya itself. For library documentation see 'moya doc'

    """
    builtin_namespaces = [
     b'default',
     b'db',
     b'fs',
     b'test',
     b'email',
     b'tables',
     b'forms',
     b'auth',
     b'admin',
     b'jsonrpc',
     b'image',
     b'thumbnail',
     b'widgets',
     b'feedback',
     b'blog',
     b'comments',
     b'links',
     b'wysihtml5',
     b'recaptcha']
    document_libs = [
     ('moya.auth', 'py:moya.libs.auth'),
     ('moya.forms', 'py:moya.libs.forms'),
     ('moya.widgets', 'py:moya.libs.widgets'),
     ('moya.admin', 'py:moya.libs.admin'),
     ('moya.jsonrpc', 'py:moya.libs.jsonrpc'),
     ('moya.thumbnail', 'py:moya.libs.thumbnail'),
     ('moya.widgets', 'py:moya.libs.widgets'),
     ('moya.feedback', 'py:moya.libs.feedback'),
     ('moya.blog', 'py:moya.libs.blog'),
     ('moya.comments', 'py:moya.libs.comments'),
     ('moya.tables', 'py:moya.libs.tables'),
     ('moya.links', 'py:moya.libs.links'),
     ('moya.wysihtml5', 'py:moya.libs.wysihtml5'),
     ('moya.google.recaptcha', 'py:moya.libs.recaptcha')]

    def get_argparse(self):
        parser = argparse.ArgumentParser(prog=b'moya-doc', description=self.__doc__)
        parser.add_argument(b'--version', dest=b'version', metavar=b'MAJOR.MINOR', default=None, help=b'version number to build')
        parser.add_argument(b'--watch', dest=b'watch', action=b'store_true', help=b'Watch source for changes and rebuild')
        parser.add_argument(b'--extract', b'-e', dest=b'extract', action=b'store_true', help=b'Extract tag information')
        parser.add_argument(b'--build', b'-b', dest=b'build', action=b'store_true', help=b'Build HTML docs')
        parser.add_argument(b'-no-browser', b'-n', dest=b'nobrowser', action=b'store_true', help=b"Don't launch the browser")
        parser.add_argument(b'-s', b'--settings', dest=b'settings', metavar=b'PATH', default=b'~/.moyadoc', help=b'Doc settings file')
        return parser

    def run(self):
        parser = self.get_argparse()
        args = parser.parse_args(sys.argv[1:])
        if args.version is None:
            major, minor = __version__.split(b'.')[:2]
            version = (b'{}.{}').format(major, minor)
        else:
            version = args.version
        try:
            with open(expanduser(args.settings), b'rt') as (f_ini):
                cfg = SettingsContainer.read_from_file(f_ini)
                print((b'Read settings from {}').format(args.settings))
        except IOError:
            cfg = SettingsContainer()

        from ..docgen.extracter import Extracter
        from ..docgen.builder import Builder
        from ..command import doc_project
        location = dirname(doc_project.__file__)
        try:
            base_docs_fs = OSFS(b'text')
        except FSError:
            sys.stderr.write(b'run me from moya/docs directory\n')
            return -1

        extract_fs = OSFS(join(b'doccode', version), create=True)
        languages = [ d for d in base_docs_fs.listdir(dirs_only=True) if len(d) == 2 ]

        def do_extract():
            print((b'Extracting docs v{}').format(version))
            utils.remove_all(extract_fs, b'/')
            try:
                archive, context, doc = moya_build.build_server(location, b'settings.ini')
            except Exception:
                raise
                return -1

            extract_fs.makedir(b'site/docs', recursive=True)
            extract_fs.makedir(b'site/tags', recursive=True)
            with extract_fs.opendir(b'site/tags') as (tags_fs):
                extracter = Extracter(archive, tags_fs)
                const_data = {}
                builtin_tags = []
                for namespace in self.builtin_namespaces:
                    xmlns = getattr(namespaces, namespace, None)
                    if xmlns is None:
                        raise ValueError((b"XML namespace '{}' is not in namespaces.py").format(namespace))
                    namespace_tags = archive.registry.get_elements_in_xmlns(xmlns).values()
                    builtin_tags.extend(namespace_tags)

                extracter.extract_tags(builtin_tags, const_data=const_data)
            for language in languages:
                with extract_fs.makeopendir(b'site/docs') as (language_fs):
                    doc_extracter = Extracter(None, language_fs)
                    docs_fs = base_docs_fs.opendir(language)
                    doc_extracter.extract_site_docs(docs_fs, dirname=language)

            return

        if args.extract:
            do_extract()
        if args.build:
            theme_path = cfg.get(b'paths', b'theme', None)
            dst_path = join(b'html', version)
            if theme_path is None:
                theme_fs = OSFS(b'theme')
            else:
                theme_fs = fsopendir(theme_path)
            output_path = cfg.get(b'paths', b'output', None)
            if output_path is None:
                output_base_fs = OSFS(dst_path, create=True)
            else:
                output_root_base_fs = fsopendir(output_path)
                output_base_fs = output_root_base_fs.makeopendir(dst_path, recursive=True)
            utils.remove_all(output_base_fs, b'/')

            def do_build():
                print((b'Building docs v{}').format(version))
                lib_info = {}
                lib_paths = {}
                for long_name, lib in self.document_libs:
                    lib_info[long_name] = moya_build.get_lib_info(lib)
                    lib_paths[long_name] = output_base_fs.getsyspath(join(b'libs', long_name, b'index.html'))

                for language in languages:
                    docs_fs = base_docs_fs.makeopendir(language)
                    output_fs = output_base_fs.makeopendir(language)
                    utils.remove_all(output_fs, b'/')
                    with extract_fs.opendir(b'site') as (extract_site_fs):
                        builder = Builder(extract_site_fs, output_fs, theme_fs)
                        from ..tools import timer
                        with timer(b'render time'):
                            builder.build({b'libs': lib_info, b'lib_paths': lib_paths})

            def extract_build():
                do_extract()
                do_build()

            do_build()
            if not args.nobrowser:
                import webbrowser
                index_url = b'file://' + output_base_fs.getsyspath(b'en/index.html')
                print(index_url)
                webbrowser.open(index_url)
            if args.watch:
                print(b'Watching for changes...')
                observer = Observer()
                path = base_docs_fs.getsyspath(b'/')
                reload_watcher = ReloadChangeWatcher(base_docs_fs, extract_build)
                observer.schedule(reload_watcher, path, recursive=True)
                observer.start()
                while 1:
                    try:
                        time.sleep(0.1)
                    except:
                        break

        return 0


def main():
    sys.exit(MoyaDoc().run())