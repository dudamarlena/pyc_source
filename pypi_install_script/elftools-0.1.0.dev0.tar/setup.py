# elftools: Engelmann's Libre fMRI Tools
#
# Copyright (c) 2018, Jeffrey M. Engelmann
#
# elftools is released under the revised (3-clause) BSD license.
# For details, see LICENSE.txt
#

import sys
import os
import io
import setuptools
import numpy

def main():
    """Configure and build the elftools package"""

    # Set the version string
    # This is automatically updated by bumpversion (see .bumpversion.cfg)
    version = '0.1.0.dev0'

    # Dependency lists
    python_requires='>=3.6'
    install_requires=['numpy>=1.15.0', 'matplotlib>=2.2.3']

    # Set package metadata
    name = 'elftools'
    description = "Engelmann's Libre fMRI Tools"
    jme = 'Jeffrey M. Engelmann'
    jme_email = 'jme2041@gmail.com'
    url = 'https://github.com/jme2041/elftools'

    # Get the package's long description from README.md
    here = os.path.abspath(os.path.dirname(__file__))
    with io.open(os.path.join(here, 'README.md'), encoding='utf-8') as f:
        long_description = f.read().replace(
            '(LICENSE.txt)',
            '(%s/blob/master/LICENSE.txt)' % url)
    long_description_content_type='text/markdown'

    # Configure the jfmri extension module
    define_macros = []
    define_macros.append(('NPY_NO_DEPRECATED_API', 'NPY_1_9_API_VERSION'))

    jfmri_module = setuptools.Extension(
        name ='jfmri',
        sources=['src/jfmri.c'],
        include_dirs=[numpy.get_include()],
        define_macros=define_macros)

    # Call setuptools.setup for the package
    setuptools.setup(
        name=name,
        version=version,
        description=description,
        long_description=long_description,
        long_description_content_type=long_description_content_type,
        license='BSD 3-Clause License',
        url=url,
        author=jme,
        author_email=jme_email,
        maintainer=jme,
        maintainer_email=jme_email,
        classifiers=[
            'Development Status :: 2 - Pre-Alpha',
            'License :: OSI Approved :: BSD License',
            'Programming Language :: C',
            'Programming Language :: Python :: 3.7',
            'Programming Language :: Python :: Implementation :: CPython',
            'Operating System :: MacOS :: MacOS X',
            'Operating System :: POSIX :: Linux',
            'Environment :: Console',
            'Natural Language :: English',
            'Intended Audience :: Science/Research',
            'Topic :: Scientific/Engineering :: Bio-Informatics'
        ],
        keywords='mri fmri nifti binary file viewer',
        packages=setuptools.find_packages(exclude=['src', 'test']),
        ext_modules=[jfmri_module],
        test_suite='test.get_suite',
        python_requires=python_requires,
        install_requires=install_requires)

if __name__ == '__main__':
    sys.exit(main())

