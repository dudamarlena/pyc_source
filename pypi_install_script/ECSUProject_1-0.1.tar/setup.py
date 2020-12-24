from distutils.core import setup

setup(
    name='ECSUProject_1',
    version='0.1',
    description='Demo for building a Python project',
    author='Lin Chen',
    author_email='lchen@ecsu.edu',
    url='http://lin-chen-va.github.io',
    packages=['myFormat', 'myFormat/sub', ],
    package_data={'myFormat':['other/*']},
    scripts=['convert',],
    license='Creative Commons Attribution-Noncommercial-Share Alike license',
    long_description=open('README').read(),
    classifiers=[
      'Development Status :: 4 - Beta',
      'Environment :: X11 Applications :: GTK',
      'Intended Audience :: End Users/Desktop',
      'Intended Audience :: Developers',
      'License :: OSI Approved :: GNU General Public License (GPL)',
      'Operating System :: POSIX :: Linux',
      'Programming Language :: Python',
      'Topic :: Desktop Environment',
      'Topic :: Text Processing :: Fonts'
      ],
)
