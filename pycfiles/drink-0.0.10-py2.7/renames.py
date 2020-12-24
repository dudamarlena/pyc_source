# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/drink/renames.py
# Compiled at: 2011-04-12 18:10:04
mapping = {}
for obj in ('generic.Text generic.TextArea generic.ListPage tasks.TasksPage tasks.Task markdown.MarkdownPage').split():
    namespace, klass = obj.rsplit('.', 1)
    mapping['flaskbox.objects.%s %s' % (namespace, klass)] = 'drink.objects.%s %s' % (namespace, klass)