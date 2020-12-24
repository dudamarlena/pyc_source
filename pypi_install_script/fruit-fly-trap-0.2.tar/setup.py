#
# Copyright (C) 2014-2018 Craig Hobbs
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#

import os

from setuptools import setup

PACKAGE_NAME = 'fruit-fly-trap'
MODULE_NAME = 'fruit_fly_trap'

def main():
    with open(os.path.join(os.path.abspath(os.path.dirname(__file__)), 'README.md'), encoding='utf-8') as readme_file:
        long_description = readme_file.read()

    setup(
        name=PACKAGE_NAME,
        description=('Tool to generate fruit fly trap cutouts.'),
        long_description=long_description,
        long_description_content_type='text/markdown',
        version='0.2',
        author='Craig Hobbs',
        author_email='craigahobbs@gmail.com',
        keywords='fruit fly trap',
        url='https://github.com/craigahobbs/fruit_fly_trap',
        license='MIT',
        classifiers=[
            'Development Status :: 5 - Production/Stable',
            'License :: OSI Approved :: MIT License',
            'Operating System :: OS Independent',
            'Programming Language :: Python :: 3.5',
            'Programming Language :: Python :: 3.6',
            'Programming Language :: Python :: 3.7',
            'Topic :: Utilities'
        ],
        package_dir={'': 'src'},
        packages=[MODULE_NAME],
        install_requires=[
            'fpdf >= 1.7.2',
        ],
        entry_points={
            'console_scripts': [PACKAGE_NAME + ' = ' + MODULE_NAME + ':main'],
        },
        test_suite='tests'
    )

if __name__ == '__main__':
    main()
