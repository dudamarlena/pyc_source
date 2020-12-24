# LBOT is a IRC bot that can serve RSS feed in your channel. no copyright. no LICENSE.
#
# setup.py

from setuptools import setup, find_namespace_packages

setup(
    name='lbot',
    version='4',
    url='https://bitbucket.org/botd/lbot',
    author='Bart Thate',
    author_email='bthate@dds.nl',
    description="LBOT is a IRC bot that can serve RSS feed in your channel. no copyright. no LICENSE.",
    long_description="""
R E A D M E
###########


LBOT is a IRC bot that can serve RSS feeds to your channel. no copyright. no LICENSE.


I N S T A L L


download the tarball from pypi, https://pypi.org/project/lbot/#files


you can also download with pip3 and install globally.

::

 > sudo pip3 install lbot --upgrade

if you want to develop on the library clone the source at bitbucket.org:

::

 > git clone https://bitbucket.org/botd/lbot
 > cd lbot
 > sudo python3 setup.py install


U S A G E

::

 > lbot <cmd>
 > lbot -m irc,rss localhost \#dunkbots lbot
 > lbot -s 
 > lbot -d 

logfiles can be found in ~/.lbot/logs. you can use the --owner option to set the owner of the bot to your own userhost.


C O N F I G U R A T I O N


to configure the BOTD service, you can use the config script with the following options:

::

 > sudo init.d/config <modules> <server> <channel> <nick> <owner>

for example:

::

 > sudo init.d/config udp,rss irc.freenode.net \#dunkbots mybot ~bart@shell.dds.nl

you can use the botd -x program option to configure BOTD:

::

 > lbot cfg krn modules udp,rss
 > lbot cfg irc server localhost
 > lbot cfg irc channel #dunkbots
 > lbot meet ~bart@127.0.0.1
 > lbot rss https://news.ycombinator.com/rss

use the -w option if you want to use a different work directory then ~/.lbot, for example:

::

 > sudo lbot -w /var/lib/botd -a /var/lob/botd cfg irc server irc.freenode.net



R S S


add url:

::

 > lbot rss https://news.ycombinator.com/rss
 ok 1

 run the rss commad to see what urls are registered:

 > lbot rss
 0 https://news.ycombinator.com/rss


U D P


using udp to relay text into a channel, start the bot with -m udp and use
the loudp program to send text to the UDP to channel server:

::

 > tail -f ~/.lbot/logs/lbot.log | ./bin/ludp 


M O D U L E S


OB contains the following modules:

::

    lo                          - object library.
    lo.clk                      - clock functions.
    lo.dbs                      - database.
    lo.evt                      - basic event.
    lo.gnr                      - generic object functions.
    lo.hdl                      - handler.
    lo.ldr                      - module loader.
    lo.tms                      - time related functions.
    lo.thr                      - threads.
    lo.typ                      - typing.
    lbot.cfg                    - config command.
    lbot.cmd                    - list of commands.
    lbot.irc                    - irc bot.
    lbot.rss                    - feed fetcher.
    lbot.shl                    - shell code.
    lbot.shw                    - show runtime.
    lbot.udp                    - udp to irc relay
    lbot.usr                    - user management.


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
    zip_safe=True,
    packages=["lo", "lbot"],
    scripts=["bin/lbot", 'bin/ludp'],
    classifiers=['Development Status :: 3 - Alpha',
                 'License :: Public Domain',
                 'Operating System :: Unix',
                 'Programming Language :: Python',
                 'Topic :: Utilities'
                ]
)
