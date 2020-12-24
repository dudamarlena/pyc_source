# LOSH - lib object shell.
#
# setup.py

from setuptools import setup, find_namespace_packages

setup(
    name='losh',
    version='4',
    url='https://bitbucket.org/bthate/losh',
    author='Bart Thate',
    author_email='bthate@dds.nl',
    description="LOSH is a shell for libobj and contains no copyright or LICENSE.",
    long_description="""
R E A D M E
###########


LOSH is a shell for libobj and contains no copyright or LICENSE.


I N S T A L L


download the tarball from pypi, https://pypi.org/project/losh/#files


you can also download with pip3 and install globally.

::

 > sudo pip3 install losh --upgrade

if you want to develop on the library clone the source at bitbucket.org:

::

 > git clone https://bitbucket.org/botd/losh
 > cd losh
 > sudo python3 setup.py install


U S A G E


 > losh -x  (runs a command)
 > losh -s (runs a shell)
 > losh -d (daemon mode)
 > losh localhost \#losh losh (runs a irc bot)

logfiles can be found in ~/.losh/logs.
you can use the --owner option to set the owner of the bot to your own userhost.


R S S


add url:

 > losh -x rss https://news.ycombinator.com/rss
 ok 1

 run the rss commad to see what urls are registered:

 > losh -x rss
 0 https://news.ycombinator.com/rss


U D P


using udp to relay text into a channel, start the bot with -m udp and use
the loudp program to send text to the UDP to channel server:

 > tail -f ~/.losh/logs/losh.log | ./bin/loudp 


M O D U L E S


OB contains the following modules:

    lo                          - object library.
    lo.clk                      - clock functions.
    lo.dbs                      - database.
    lo.evt                      - basic event.
    lo.gnr                      - generic object functions.
    lo.hdl                      - handler.
    lo.ldr                      - module loader.
    lo.shl                      - shell code.
    lo.tms                      - time related functions.
    lo.thr                      - threads.
    lo.typ                      - typing.
    losh.cfg                    - config command.
    losh.cmd                    - list of commands.
    losh.irc                    - irc bot.
    losh.rss                    - feed fetcher.
    losh.shw                    - show runtime.
    losh.udp                    - udp to irc relay
    losh.usr                    - user management.


C O D I N G


if you want to add your own modules to the bot, you can put you .py files in a "mods" directory and use the -m option to point to that directory.

basic code is a function that gets an event as a argument:

 def command(event):
     << your code here >>

to give feedback to the user use the event.reply(txt) method:

 def command(event):
     event.reply("yooo %s" % event.origin)


have fun coding ;]


you can contact me on IRC/freenode/#dunkbots.

| Bart Thate (bthate@dds.nl, thatebart@gmail.com)
| botfather on #dunkbots irc.freenode.net
    
    """,
    long_description_content_type="text/x-rst",
    license='Public Domain',
    zip_safe=False,
    install_requires=["libobj", "feedparser"],
    packages=["losh",],
    scripts=["bin/losh"],
    classifiers=['Development Status :: 3 - Alpha',
                 'License :: Public Domain',
                 'Operating System :: Unix',
                 'Programming Language :: Python',
                 'Topic :: Utilities'
                ]
)
