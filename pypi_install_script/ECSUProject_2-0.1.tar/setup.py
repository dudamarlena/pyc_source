from setuptools import setup

setup(
    name='ECSUProject_2',
    version='0.1',
    description='Demo for building a Python project',
    author='Lin Chen',
    author_email='lchen@ecsu.edu',
    url='http://lin-chen-va.github.io',
    install_requires=['numpy>=1.14.0', 'biopython>=1.60'],
    packages=['myFormat', 'myFormat/sub', ],
    package_dir={'':'src'},
    package_data={'myFormat':['other/*']},
    scripts=['src/convert',],
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
