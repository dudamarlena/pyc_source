# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/will/projects/moya/moya/command/sub/extract.py
# Compiled at: 2016-12-08 16:29:22
from __future__ import unicode_literals
from __future__ import print_function
from ...command import SubCommand
from ...wsgi import WSGIApplication
from ...console import Cell
from ...template.moyatemplates import Template
from datetime import datetime
from fs.path import join
import os.path
from collections import defaultdict
import polib, pytz

class Extract(SubCommand):
    """Extract translatable text from libraries"""
    help = b'extract translatable text'

    def add_arguments(self, parser):
        parser.add_argument(dest=b'libs', default=None, metavar=b'LIB NAME', nargs=b'+', help=b'Extract text from these libs')
        parser.add_argument(b'-l', b'--location', dest=b'location', default=None, metavar=b'PATH', help=b'location of the Moya server code')
        parser.add_argument(b'-i', b'--ini', dest=b'settings', default=None, metavar=b'SETTINGSPATH', help=b'path to projects settings file')
        parser.add_argument(b'-m', b'--merge', dest=b'merge', action=b'store_true', help=b'merge translatable strings with existing .pot file')
        parser.add_argument(b'-o', b'--overwrite', dest=b'overwrite', action=b'store_true', help=b'overwrite existing .pot file')
        return

    def run(self):
        args = self.args
        application = WSGIApplication(self.location, self.get_settings(), disable_autoreload=True, master_settings=self.master_settings)
        archive = application.archive
        try:
            libs = [ archive.libs[lib_name] for lib_name in args.libs ]
        except KeyError:
            self.console.error((b'No lib with name "{}" installed').format(lib_name))
            return -1

        table = []
        for lib in libs:
            template_text = set()
            extract_text = defaultdict(lambda : {b'occurrences': []})
            if not lib.translations_location:
                table.append([lib.long_name,
                 Cell(b'translations not enabled', fg=b'red', bold=True),
                 b''])
                continue
            filename = (b'{}.pot').format(lib.long_name.replace(b'.', b'_'))
            translations_dir = lib.load_fs.getsyspath(lib.translations_location)

            def add_text(path, line, text, comment=None, plural=None, attr=None, context=None):
                rel_path = os.path.relpath(path, translations_dir)
                entry = extract_text[(text, plural, attr, context)]
                if attr is not None and context is not None:
                    context = (b"attribute '{}'").format(attr)
                if plural is not None:
                    entry[b'msgid'] = text
                    entry[b'msgid_plural'] = plural
                    entry[b'msgstr_plural'] = {b'0': b'', b'1': b''}
                else:
                    entry[b'msgid'] = text
                if context is not None:
                    entry[b'msgctxt'] = context
                entry[b'occurrences'].append((rel_path, line))
                if comment is not None:
                    entry[b'comment'] = comment
                return

            with self.console.progress((b'extracting {}').format(lib), len(lib.documents)) as (progress):
                for doc in lib.documents:
                    progress.step()
                    for element in doc.elements.itervalues():
                        if element._translate_text:
                            text = element._text.strip()
                            if text:
                                add_text(element._location, element.source_line, text, comment=unicode(element))
                        for name, attribute in element._tag_attributes.items():
                            if attribute.translate or name in element._translatable_attrs:
                                text = element._attrs.get(name, b'').strip()
                                if text:
                                    add_text(element._location, element.source_line, text, attr=name, comment=(b"attribute '{}' of {}").format(name, unicode(element)))

                    if b'location' in lib.templates_info:
                        engine = archive.get_template_engine(b'moya')
                        with lib.load_fs.opendir(lib.templates_info[b'location']) as (templates_fs):
                            for path in templates_fs.walk.files():
                                sys_path = templates_fs.getsyspath(path, allow_none=True) or path
                                contents = templates_fs.getbytes(path)
                                template = Template(contents, path)
                                template.parse(engine.env)
                                for trans_text in template.translatable_text:
                                    line, start, end = trans_text.location
                                    text = trans_text.text
                                    comment = trans_text.comment
                                    plural = trans_text.plural
                                    translatable_text = (
                                     path, line, start, text, plural)
                                    if translatable_text not in template_text:
                                        add_text(sys_path, line, text, comment, plural=plural, context=trans_text.context)
                                        template_text.add(translatable_text)

            now = pytz.UTC.localize(datetime.utcnow())
            po = polib.POFile()
            for text in extract_text.values():
                po.append(polib.POEntry(**text))

            po.metadata = {b'POT-Creation-Date': now.strftime(b'%Y-%m-%d %H:%M%z'), 
               b'Project-Id-Version': lib.version, 
               b'Language': lib.default_language or b'en', 
               b'MIME-Version': b'1.0', 
               b'Content-Type': b'text/plain; charset=utf-8', 
               b'Content-Transfer-Encoding': b'8Bit', 
               b'Plural-Forms': b'nplurals=2; plural=(n != 1);'}
            if lib.translations_location:
                lib.load_fs.makedir(lib.translations_location, recreate=True)
                translations_location = lib.load_fs.getsyspath(lib.translations_location)
                translation_path = os.path.join(translations_location, filename)
                if os.path.exists(translation_path) and not args.overwrite:
                    if not args.merge:
                        self.console.error((b'message file "{}" exists, see --merge or --overwrite options').format(filename))
                        return -1
                    existing_po = polib.pofile(translation_path)
                    po.merge(existing_po)
                    po.save(translation_path)
                else:
                    po.save(translation_path)
                locale_fs = lib.load_fs.opendir(lib.translations_location)
                for lang in lib.languages:
                    locale_fs.makedirs((b'{}/LC_MESSAGES/').format(lang), recreate=True)

                table.append([lib.long_name,
                 Cell(join(lib.translations_location, filename), fg=b'green', bold=True),
                 Cell(len(po), bold=True)])

        self.console.table(table, header_row=[b'lib', b'file', b'no. strings'])
        return