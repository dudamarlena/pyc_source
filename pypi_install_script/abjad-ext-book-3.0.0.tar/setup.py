#! /usr/bin/env python
import pathlib
import setuptools


subpackage_name = 'book'


def read_version():
    root_path = pathlib.Path(__file__).parent
    version_path = root_path / 'abjadext' / subpackage_name / '_version.py'
    with version_path.open() as file_pointer:
        file_contents = file_pointer.read()
    local_dict = {}
    exec(file_contents, None, local_dict)
    return local_dict['__version__']


if __name__ == '__main__':
    setuptools.setup(
        author='Josiah Wolf Oberholtzer',
        author_email='josiah.oberholtzer@gmail.com',
        classifiers=[
            'Development Status :: 3 - Alpha',
            'License :: OSI Approved :: GNU General Public License (GPL)',
            'Programming Language :: Python :: 3.6',
            'Programming Language :: Python :: Implementation :: CPython',
            'Topic :: Artistic Software',
            ],
        extras_require={
            'test': [
                'mypy',
                'pytest-helpers-namespace',
                'pytest>=3.5.0',
                'pytest-cov',
                ],
            },
        include_package_data=True,
        install_requires=[
            'PyPDF2 >= 1.26.0',
            'abjad >= 2.21',
            'uqbar >= 0.2.12',
            ],
        license='MIT',
        long_description=pathlib.Path('README.md').read_text(),
        keywords=', '.join([
            'music composition',
            'music notation',
            'formalized score control',
            'lilypond',
            'cli',
            ]),
        name='abjad-ext-{}'.format(subpackage_name),
        packages=['abjadext'],
        platforms='Any',
        url='http://www.projectabjad.org',
        version=read_version(),
    )
