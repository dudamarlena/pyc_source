# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-jkXn_D/South/south/management/commands/graphmigrations.py
# Compiled at: 2018-07-11 18:15:31
"""
Outputs a graphviz dot file of the dependencies.
"""
from __future__ import print_function
from optparse import make_option
import re, textwrap
from django.core.management.base import BaseCommand
from django.core.management.color import no_style
from south.migration import Migrations, all_migrations

class Command(BaseCommand):
    help = 'Outputs a GraphViz dot file of all migration dependencies to stdout.'

    def handle(self, **options):
        Migrations.calculate_dependencies()
        colors = [
         'crimson', 'darkgreen', 'darkgoldenrod', 'navy',
         'brown', 'darkorange', 'aquamarine', 'blueviolet']
        color_index = 0
        wrapper = textwrap.TextWrapper(width=40)
        print('digraph G {')
        for migrations in all_migrations():
            print('  subgraph %s {' % migrations.app_label())
            print('    node [color=%s];' % colors[color_index])
            for migration in migrations:
                label = '%s - %s' % (
                 migration.app_label(), migration.name())
                label = re.sub('_+', ' ', label)
                label = ('\\n').join(wrapper.wrap(label))
                print('    "%s.%s" [label="%s"];' % (
                 migration.app_label(), migration.name(), label))

            print('  }')
            color_index = (color_index + 1) % len(colors)

        for migrations in all_migrations():
            for migration in migrations:
                for other in migration.dependencies:
                    attrs = '[weight=2.0]'
                    if other.app_label() != migration.app_label():
                        attrs = '[style=bold]'
                    print('  "%s.%s" -> "%s.%s" %s;' % (
                     other.app_label(), other.name(),
                     migration.app_label(), migration.name(),
                     attrs))

        print('}')