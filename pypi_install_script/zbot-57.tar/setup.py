#!/usr/bin/env python3
#
#

import os
import sys

if sys.version_info.major < 3: print("you need to run zbot with python3") ; os._exit(1)

try: use_setuptools()
except: pass

try:
    from setuptools import setup
except Exception as ex: print(str(ex)) ; os._exit(1)

from distutils import sysconfig
site_packages_path = sysconfig.get_python_lib()

setup(
    name='zbot',
    version='57',
    url='https://pikacode.com/milla/zbot',
    author='Bart Thate',
    author_email='milla@dds.nl',
    description='uses zbot.workdir in the current working directory, use -d <directory> if you need to access other directories.',
    license='MIT',
    include_package_data=True,
    zip_safe=False,
    install_requires=["distribute", "beautifulsoup4", "sleekxmpp", "natural", "feedparser", ],
    scripts=["bin/zbot", "bin/zout", "bin/zbot-sed", ],
    packages=['zbot', 
              'zbot.plugs',
             ],
    long_description = """ xmpp, irc, shell, cli, json - if you need to log effects of medicine, wait for version 100, email at milla@dds.nl

documentation is at http://pythonhosted.org/zbot/

:: 

  milla@reppa:~/zbot.dev/first$ ./bin/zbot -s -l warn

  ZBOT #44 -=- ! Thu Jan 23 16:28:55 2014

  16:28:55 -=- ! E G G S
  16:28:55 -=- !  
  16:28:55 -=- ! zbot egg: /usr/local/lib/python3.3/dist-packages/zbot-43-py3.3.egg
  16:28:55 -=- !  
  16:28:55 -=- ! C O N F I G
  16:28:55 -=- !  
  16:28:55 -=- ! loglevel=warn
  16:28:55 -=- ! workdir=/home/milla/zbot.dev/first/zbot.workdir
  16:28:55 -=- ! do_shell=True
  16:28:55 -=- ! rootlist=['/home/milla/zbot.dev/first/zbot.workdir', 
                           'Public/zbot.workdir/2014-01-23', 
                           'Dropbox/backups/zbot.workdir/2014-01-23']
  16:28:55 -=- !  
  16:28:55 -=- ! B O O T
  16:28:55 -=- !  
  16:28:55 -=- ! plugs /home/milla/zbot.dev/first/zbot/plugs
  16:28:55 -=- < 

  milla@reppa:~/zbot.dev/first$ ./bin/zbot dump log
  {"added": "Thu Jan 23 16:26:26 2014", "date": "Thu Jan 23 16:26:26 2014", "log": "dizzy"}
  {"added": "Thu Jan 23 16:26:07 2014", "date": "Thu Jan 23 16:26:07 2014", "log": "orap"}

Onderwerp:

Vraag 4

Kunt u maatregelen nemen om ervoor te zorgen dat psychiatrische patiënten
met hoge psychische nood ook in het weekend voldoende hulp krijgen?

Antwoord op vraag 4

Personen die in acute psychische nood verkeren kunnen 24 uur per dag en
zeven dagen in de week terecht bij de crisisdienst van een psychiatrische
instelling. Voor personen die kampen met acute suïcidale problemen bieden
de Stichting Ex6 en de Stichting 113online via de telefoon en via internet
anoniem crisiscounseling eveneens met een 24 uur bereikbaarheid.
Er wordt dus in voldoende mate voorzien in hulpverlening aan mensen met
acute psychische problemen die in het weekend opspelen.

Vragen: cijfers.

http://nos.nl/artikel/618625-geen-sterftecijfer-14-ziekenhuizen.html

""",
    data_files=[('doc', ["LICENSE",]), ("doc/path", ["docs/path/adressen", "docs/path/lijst", "docs/path/morgen",  "docs/path/nietmeer", "docs/path/nodig",  
                                                      "docs/path/onderwerp", "docs/path/oordeel",  "docs/path/oplossingen",  "docs/path/persoonlijk", 
                                                      "docs/path/route",  "docs/path/taal", "docs/path/trade", "docs/path/vorig", "docs/path/wel", "docs/path/zien"])],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Other Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: Unix',
        'Programming Language :: Python',
        'Topic :: Communications :: Email',
        'Topic :: Software Development :: Libraries :: Python Modules'],
)
