from setuptools import setup

setup(
    name='obdev',
    version='1',
    url='https://github.com/bthate/obdev',
    author='Bart Thate',
    author_email='bthate@dds.nl',
    description="OBDEV is the development environment for the OB package. OB is a event handler library and uses a timestamped JSON file backend to provide persistence. no copyright or LICENSE.",
    long_description="""R E A D M E

OB is a pure python3 event handler and uses a timestamped, type in filename, JSON stringified, files on filesystem backend.
OB has been placed in the Public Domain and contains no copyright or LICENSE.


if you need OB to have access to your local directory use this: 

 > export PYTHONPATH="."

this will add your current directory to the pythonpath so the packages in it 
can be found by OB.

installation is through pypi:

 > sudo pip3 install ob

you can also run the bot from the tarball at pypi and run it directly or 
install with setup.py:

 > python3 setup.py install --user

installing from the github repository is also possible:

 > git clone http://github.com/bthate/ob

lastely, you can also run directly from the tarball, see https://pypi.org/project/ob/#files

ob provides the following modules::

 ob     - object library.
 ob.clk - clocks,repeaters.
 ob.cls - base classes.
 ob.dbs - database management.
 ob.dpt - dispatch function.
 ob.err - possible errors.
 ob.evt - event handling.
 ob.flt - list of bots.
 ob.hdl - handlers code.
 ob.krn - kernel bootup,initialisation
 ob.ldr - module loader.
 ob.log - logging system and callback.
 ob.pst - persistency. 
 ob.shl - shell related code.
 ob.thr - thread management.
 ob.tms - time related code.
 ob.trc - stack inspection.
 ob.trm - terminal code.
 ob.typ - type system.
 ob.utl - utility functions

H A V E   F U N 

enjoy the coding ! ;]


Bart

bthate@dds.nl | botfather #dunkbots irc.freenode.net | https://pypi.org/project/ob 
    
    """,
    license='Public Domain',
    zip_safe=True,
    install_requires=["ob", "obot", "obsh"],
    packages=["obdev"],
    scripts=["bin/obclean", "bin/obdo", "bin/obkill", "bin/obstatus", "bin/obtest"],
    classifiers=['Development Status :: 3 - Alpha',
                 'License :: Public Domain',
                 'Operating System :: Unix',
                 'Programming Language :: Python',
                 'Topic :: Utilities'
                ]
)
