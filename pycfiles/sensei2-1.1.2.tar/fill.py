# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /media/xacce/addit/Projects/inventory/venv/src/sensei2/sensei2/management/commands/fill.py
# Compiled at: 2015-11-10 12:22:06
import sys
from django.core.management import BaseCommand
from sensei2.sensei.sensei_room import Sensei
from termcolor import cprint

class Command(BaseCommand):

    def handle(self, *args, **options):
        group = sys.argv[2]
        sensei = Sensei(group)
        try:
            sensei.teach()
        except Exception as e:
            cprint('\n\nSensei stopped. Need more meditate', 'red')