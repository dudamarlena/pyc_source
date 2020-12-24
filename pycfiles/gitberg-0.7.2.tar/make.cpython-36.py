# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/eric/github/local/gitberg/gitenberg/make.py
# Compiled at: 2018-10-20 14:41:52
# Size of source mod 2**32: 2243 bytes
"""
Makes an organized git repo of a book folder
"""
import codecs, os
from os.path import abspath, dirname
import jinja2, sh
from .parameters import GITHUB_ORG

class NewFilesHandler:
    __doc__ = ' NewFilesHandler - templates and copies additional files to book repos\n\n    '
    README_FILENAME = 'README.rst'

    def __init__(self, book):
        self.book = book
        package_loader = jinja2.PackageLoader('gitenberg', 'templates')
        self.env = jinja2.Environment(loader=package_loader)

    def add_new_files(self):
        self.template_readme()
        self.copy_files()

    def template_readme(self):
        template = self.env.get_template('README.rst.j2')
        readme_text = (template.render)(authors=self.book.meta.authors_short(), **self.book.meta.metadata)
        readme_path = os.path.join(self.book.local_path, self.README_FILENAME)
        with codecs.open(readme_path, 'w', 'utf-8') as (readme_file):
            readme_file.write(readme_text)

    def copy_files(self):
        """ Copy the LICENSE and CONTRIBUTING files to each folder repo 
        Generate covers if needed. Dump the metadata.
        """
        files = [
         'LICENSE', 'CONTRIBUTING.rst']
        this_dir = dirname(abspath(__file__))
        for _file in files:
            sh.cp('{0}/templates/{1}'.format(this_dir, _file), '{0}/'.format(self.book.local_path))

        if self.book.meta.rdf_path:
            sh.cp(self.book.meta.rdf_path, '{0}/'.format(self.book.local_path))
        if 'GITenberg' not in self.book.meta.subjects:
            if not self.book.meta.subjects:
                self.book.meta.metadata['subjects'] = []
            self.book.meta.metadata['subjects'].append('GITenberg')
        self.save_meta()

    def save_meta(self):
        if not self.book.meta._version:
            self.book.meta.metadata['_version'] = '0.0.1'
        self.book.meta.dump_file(os.path.join(self.book.local_path, 'metadata.yaml'))