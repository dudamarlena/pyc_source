#!/usr/bin/env python3
#-*- coding: utf-8 -*-

import os
import sys
import shutil
import setuptools

if sys.version_info < (3,):
    sys.exit('Sorry, Python3 is required for youngseq.')

# ------------------Package Meta-Data------------------
AUTHOR = 'Jason Young'
EMAIL = 'Jason.Young.NLP@gmail.com'

PACKAGE_NAME = 'fairseq_doc'
VERSION = None
SOURCE_URL = 'https://github.com/Jason-Young-NLP/YoungSeq'
DESCRIPTION = 'Young\'s Sequence-Sequence Research Toolkit Extended on FAIRSeq'

# This Package's directory absolute path is set here.
PACKAGE_DIR_ABSOLUTE_PATH = os.path.abspath(os.path.dirname(__file__))

# Distribution directory 'dist' path is set here.
PACKAGE_DIST_DIR_ABSOLUTE_PATH = os.path.join(PACKAGE_DIR_ABSOLUTE_PATH, 'dist')

# Building directory 'build' path is set here.
PACKAGE_BUILD_DIR_ABSOLUTE_PATH = os.path.join(PACKAGE_DIR_ABSOLUTE_PATH, 'build')

# EggInfo directory 'PACKAGE_NAME.egg-info' path is set here.
PACKAGE_EGGINFO_DIR_ABSOLUTE_PATH = os.path.join(PACKAGE_DIR_ABSOLUTE_PATH, '{}.egg-info'.format(PACKAGE_NAME))

# Version is set here.
VERSION_ABSOLUTE_PATH = os.path.join(PACKAGE_DIR_ABSOLUTE_PATH, PACKAGE_NAME, '__version__.py')

PACKAGE_INFO = {}
# Version is set here
if VERSION:
    PACKAGE_INFO['__version__'] = VERSION
else:
    with open(VERSION_ABSOLUTE_PATH, 'r', encoding='utf-8') as version_file:
        exec(version_file.read(), PACKAGE_INFO)

# License is set here
LICENSE_ABSOLUTE_PATH = os.path.join(PACKAGE_DIR_ABSOLUTE_PATH, 'LICENSE')
try:
    with open(LICENSE_ABSOLUTE_PATH, 'r', encoding='utf-8') as license_file:
        LICENSE = license_file.read()
except FileNotFoundError:
    LICENSE = 'BSD Licence'

# Long-Description is set here
README_ABSOLUTE_PATH = os.path.join(PACKAGE_DIR_ABSOLUTE_PATH, 'README.md')
try:
    with open(README_ABSOLUTE_PATH, 'r', encoding='utf-8') as readme_file:
        LONG_DESCRIPTION = '\n' + readme_file.read()
except FileNotFoundError:
    LONG_DESCRIPTION = DESCRIPTION

# Required Packages and Optional Packages
if sys.platform == 'darwin':
    extra_compile_args = ['-stdlib=libc++']
else:
    extra_compile_args = ['-std=c++11']
bleu = setuptools.Extension(
    'fairseq_doc.libbleu',
    sources=[
        'fairseq_doc/clib/libbleu/libbleu.cpp',
        'fairseq_doc/clib/libbleu/module.cpp',
    ],
    extra_compile_args=extra_compile_args,
)
# Required
REQUIRED = [
        'cffi',
        'fastBPE',
        'numpy',
        'regex',
        'sacrebleu',
        'torch',
        'tqdm',
        ]
# Optional
EXTRAS = {
        # '': [''],
        }

# Upload command class of the setup.py.
class UploadCommand(setuptools.Command):
    """Let setup.py support the command \'upload\'."""

    description = 'Building and Publishing this Package: {}'.format(PACKAGE_NAME)
    user_options = []

    @staticmethod
    def status(str):
        """Printing things in bold."""
        print('\033[1m{}\033[0m'.format(str))

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        try:
            self.status('Removing previous dists ...')
            shutil.rmtree(PACKAGE_DIST_DIR_ABSOLUTE_PATH)
            self.status('Removing previous builds ...')
            shutil.rmtree(PACKAGE_BUILD_DIR_ABSOLUTE_PATH)
            self.status('Removing previous egg-infos ...')
            shutil.rmtree(PACKAGE_EGGINFO_DIR_ABSOLUTE_PATH)
        except OSError:
            pass

        self.status('Building Source and Wheel (universal) distribution ...')
        os.system('{} setup.py sdist '.format(sys.executable))

        self.status('Uploading the package to PyPI via Twine ...')
        os.system('twine upload --repository-url https://upload.pypi.org/legacy/ dist/*')

        #self.status('Pushing git tags…')
        #os.system('git tag v{}'.format(PACKAGE_INFO['__version__']))
        #os.system('git push --tags')
        #os.system('git push -u origin master')

        sys.exit()


def setup_my_package():
    setuptools.setup(
        author=AUTHOR,
        author_email=EMAIL,
        name=PACKAGE_NAME,
        version=PACKAGE_INFO['__version__'],
        url=SOURCE_URL,
        license=LICENSE,
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        long_description_content_type='text/markdown',
        packages=setuptools.find_packages(exclude=('tests',)),
        install_requires=REQUIRED,
        extras_require=EXTRAS,
        include_package_data=True,
        ext_modules=[bleu],
        classifiers=[
            'Intended Audience :: Science/Research',
            'Programming Language :: Python :: 3',
            'License :: OSI Approved :: Apache Software License',
            'Operating System :: OS Independent',
            'Topic :: Scientific/Engineering :: Artificial Intelligence',
        ],
        cmdclass={
            'upload': UploadCommand,
        },
        entry_points={
            'console_scripts': [
                'fairseq_doc-eval-lm = fd_cli.eval_lm:cli_main',
                'fairseq_doc-generate = fd_cli.generate:cli_main',
                'fairseq_doc-interactive = fd_cli.interactive:cli_main',
                'fairseq_doc-preprocess = fd_cli.preprocess:cli_main',
                'fairseq_doc-score = fd_cli.score:main',
                'fairseq_doc-train = fd_cli.train:cli_main',
                'fairseq_doc-validate = fd_cli.validate:cli_main',
                'fairseq_doc-docnmt-train = fd_cli.docnmt_train:cli_main',
                'fairseq_doc-docnmt-preprocess =  fd_cli.docnmt_preprocess:cli_main',
                'fairseq_doc-docnmt-generate = fd_cli.docnmt_generate:cli_main',
            ],
        },
    )


if __name__ == '__main__':
    setup_my_package()
