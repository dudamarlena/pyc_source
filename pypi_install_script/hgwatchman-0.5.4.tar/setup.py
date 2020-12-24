from distutils.core import setup, Extension

setup(
    name='hgwatchman',
    version='0.5.4',
    author='Siddharth Agarwal',
    author_email='sid0@fb.com',
    maintainer='Siddharth Agarwal',
    maintainer_email='sid0@fb.com',
    url='https://bitbucket.org/facebook/hgwatchman',
    description='Watchman integration for Mercurial',
    long_description="""
This extension integrates Watchman with Mercurial for faster status queries.
    """.strip(),
    keywords='hg watchman mercurial inotify file-watching',
    license='GPLv2+',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: POSIX :: Linux',
        'Topic :: Software Development :: Version Control',
        'License :: OSI Approved :: GNU General Public License v2 or later (GPLv2+)',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
    ],
    packages=['hgwatchman', 'hgwatchman.pywatchman'],
    ext_modules = [
        Extension('hgwatchman.pywatchman.bser',
                  sources=['hgwatchman/pywatchman/bser.c']),
    ]
)
