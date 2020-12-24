# LIBOBJ - library object.
#
# setup.py

from setuptools import setup, find_namespace_packages

setup(
    name='libobj',
    version='8',
    url='https://bitbucket.org/bthate/libobj',
    author='Bart Thate',
    author_email='bthate@dds.nl',
    description="LIBOBJ is an object library and contains no copyright or LICENSE.",
    long_description="""R E A D M E
###########

LIBOBJ is an object library and contains no copyright or license.


I N S T A L L


download the tarball from pypi, https://pypi.org/project/libobj/#files


you can also download with pip3 and install globally.

::

 > sudo pip3 install libobj --upgrade

if you want to develop on the library clone the source at bitbucket.org:

::

 > git clone https://bitbucket.org/botd/libobj
 > cd libobj
 > sudo python3 setup.py install


M O D U L E S


LIBOBJ contains the following modules:

::

    lo				- object library.
    lo.clk			- clock functions.
    lo.csl			- console.
    lo.hdl			- handler.
    lo.shl			- shell code.
    lo.tms 			- time related functions.
    lo.thr			- threads.
    lo.typ			- typing.
 

have fun coding ;]


I N F O


you can contact me on IRC/freenode/#dunkbots.

| Bart Thate (bthate@dds.nl, thatebart@gmail.com)
| botfather on #dunkbots irc.freenode.net
    
    """,
    long_description_content_type="text/x-rst",
    license='Public Domain',
    packages=["lo",],
    classifiers=['Development Status :: 3 - Alpha',
                 'License :: Public Domain',
                 'Operating System :: Unix',
                 'Programming Language :: Python',
                 'Topic :: Utilities'
                ]
)
