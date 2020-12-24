__author__ = 'Dror Paz, Israel Hydrological Service'
__CreatedOn__ = '2018/08/15'
__Version__ = '2018_08_15'

from distutils.core import setup

def readme():
    with open('README.rst') as f:
        return f.read()

setup(
    name = 'runable_tempfile',
    version = '1.0.1',
    description = 'Temporary file that can be opened in external app and deleted afterward',
    long_description = '''
    This class creates a temporary file which can be be opened in external program and be deleted only after the
    external program closes.
    A separate python instance will remain active in memory until no program uses the file (searched by filename),
    than deletes the file and closes.
    ''',
    author='Dror Paz',
    author_email='pazdror@gmail.com',
    url='https://gitlab.com/pazdror/runable_tempfile',
    packages=['runable_tempfile'],
    install_requires=['psutil'],
    classifiers=['Programming Language :: Python',
                 'Programming Language :: Python :: 3',
                 'Operating System :: OS Independent',
                 'Development Status :: 5 - Production/Stable',
                 'Intended Audience :: Science/Research',
                 'Topic :: Scientific/Engineering',
                 'Topic :: Software Development :: Libraries :: Python Modules'
                 ],
    keywords='tempfile temporary file launch NamedTemporaryFile'

)

#                 'Intended Audience:: Developers',
