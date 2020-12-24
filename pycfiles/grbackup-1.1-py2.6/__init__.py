# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/grbackup/__init__.py
# Compiled at: 2013-06-09 14:11:40
__version__ = '1.1'
__description__ = 'Utilite to backup items from Google Reader'
requires = [
 'pymongo>=2.4',
 'redis']
README = 'grbackup is a Python library used\nto save all items from your Google Reader account into different places.\n\nUsage\n=====\n\n::\n\n   list subscriptions: grbackup -e email@gmail.com -p password -ls\n   list topics: grbackup -e email@gmail.com -p password -lt http://feed.com\n   list starred: grbackup -e email@gmail.com -p password -lx\n   list all items: grbackup -e email@gmail.com -p password -la\n\n   backup subscriptions: grbackup -e email@gmail.com -p password -bs -o json:/tmp/subscriptions.json\n   backup topics: grbackup -e email@gmail.com -p password -bt http://myfeed.com -o json:/tmp/myfeed.json\n   backup starred into MongoDB: grbackup -e email@gmail.com -p password -bx -o mongodb://localhost:27017\n   backup all items into Redis: grbackup -e email@gmail.com -p password -ba -o redis://localhost:6379/3\n'