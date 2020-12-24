# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\tgmigrate\release.py
# Compiled at: 2006-12-04 02:08:27
version = '0.2'
description = 'sqlalchemy migrate command'
long_description = 'tgmigrate is an turbogears command extension which provide sqlalchemy migrate support.\n\nhttp://erosson.com/migrate/\n\nThe early version of tgmigrate gives turbogears developers a quick evaluation if sqlalchemy migrate is helpful for us.\n\n\nInstall\n----------------\neasy_install tgmigrate\n\n\nUsage\n----------------\n\nAfter install, tgmigrate plug an "migrate" command into tg-admin console utility.\n\nThe basic syntax is ::\n\n    tg-admin migrate [command]\n\ntgmigrate takes care the dburi and repository name for you.\n\nThe reference procedure is:\n\n1. quickstart project as usual::\n    \n    $ tg-admin quickstart -i -s demo\n    \n2. setup sqlalchemy dburi in demo/dev.cfg\n\n3. create initial database\n\n    $ tg-admin sql create\n    \n4. create repository "migration" \n\n    $ tg-admin migrate create\n    \nnote the default repository folder named "migration" is created in your project folder.\n\n5. move your database to version control\n\n    $ tg-admin migrate version_control\n    \nor briefly::\n    \n    $ tg-admin migrate vc\n    \n6. Now you could watch the current version in both database and repository\n\nshow repository version::\n\n    $ tg-admin migrate v \n    (tg-admin migrate version)\n\nshow database version::\n    \n    $ tg-admin migrate dbv \n    (tg-admin migrate db_version)\n    \nthen follow the migration doc http://erosson.com/migrate/docs/versioning.html to do the further stuff.\n\nPlease post your comments or suggestions on TurboGears google group http://groups.google.com/group/turbogears\n\n\nreference\n--------------\nYou could use:: \n\n    $ tg-admin migrate help\n\nto get all available commands and help\n\nThe available commands are\n\n$ tg-admin migrate [command]\n\ncommand = [\n\'help\',\n\'create\',\n\'script\',\n\'commit\',\n\'version\',\n\'source\',\n\'version_control\',\n\'db_version\',\n\'upgrade\',\n\'downgrade\',\n\'drop_version_control\',\n\'manage\',\n\'test\']\n\n'
author = 'Fred Lin'
email = 'gasolin+tg@gmail.com'
copyright = 'Fred Lin 2006'
url = 'docs.turbogears.org'
download_url = 'http://www.python.org/pypi/tgmigrate/'
license = 'MIT'