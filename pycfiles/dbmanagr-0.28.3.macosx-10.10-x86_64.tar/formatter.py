# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/site-packages/dbmanagr/formatter.py
# Compiled at: 2015-10-11 07:17:06


class DefaultFormatter(object):

    def __init__(self):
        pass

    def format(self, item):
        return unicode(item)

    def format_item(self, item):
        return self.format(item)

    def format_row(self, item):
        return (', ').join(map(unicode, item))

    def format_column(self, item):
        return self.format(item)

    def format_node(self, item):
        return unicode(item)

    def format_column_node(self, item):
        return self.format(item)

    def format_name_node(self, item):
        return self.format(item)

    def format_table_node(self, item):
        return self.format(item)

    def format_foreign_key_node(self, item):
        return self.format(item)


class SimplifiedFormatter(DefaultFormatter):

    def __init__(self, default_format='{title}\t{subtitle}', item_format='{title}\t{subtitle}'):
        self.default_format = default_format
        self.item_format = item_format

    def format(self, item):
        return self.default_format.format(title=self.escape(item.title()), subtitle=self.escape(item.subtitle()), autocomplete=self.escape(item.autocomplete()), uid=self.escape(item.uid()), validity=self.escape(item.validity()), icon=self.escape(item.icon()), value=self.escape(item.value()))

    def format_row(self, item):
        return self.format(item)

    def escape(self, value):
        return value


class TestFormatter(SimplifiedFormatter):

    def format(self, item):
        return ('{title}\t{autocomplete}').format(title=item.title(), autocomplete=item.autocomplete())


class JsonFormatter(SimplifiedFormatter):

    def __init__(self):
        SimplifiedFormatter.__init__(self, default_format='   {{ "uid": "{uid}", "arg": "{title}", "autocomplete": "{autocomplete}", "valid": "{validity}", "title": "{title}", "subtitle": "{subtitle}", "icon": "{icon}" }}', item_format='   {{ "uid": "{uid}", "arg": "{title}", "autocomplete": "{autocomplete}", "valid": "{validity}", "title": "{title}", "subtitle": "{subtitle}", "icon": "{icon}" }}')


class SimpleFormatter(SimplifiedFormatter):

    def __init__(self):
        SimplifiedFormatter.__init__(self, default_format='{uid}\t{title}\t{subtitle}\t{autocomplete}', item_format='{uid}\t{title}\t{subtitle}\t{autocomplete}')


class AutocompleteFormatter(SimplifiedFormatter):

    def __init__(self):
        SimplifiedFormatter.__init__(self, default_format='{autocomplete}', item_format='{autocomplete}')


class Formatter(object):
    formatter = DefaultFormatter()

    @staticmethod
    def set(arg):
        Formatter.formatter = arg

    @staticmethod
    def format(item):
        return Formatter.formatter.format(item)

    @staticmethod
    def format_row(item):
        return Formatter.formatter.format_row(item)

    @staticmethod
    def format_column(item):
        return Formatter.formatter.format_column(item)

    @staticmethod
    def format_node(item):
        return Formatter.formatter.format_node(item)

    @staticmethod
    def format_column_node(item):
        return Formatter.formatter.format_column_node(item)

    @staticmethod
    def format_table_node(item):
        return Formatter.formatter.format_table_node(item)

    @staticmethod
    def format_name_node(item):
        return Formatter.formatter.format_name_node(item)

    @staticmethod
    def format_foreign_key_node(item):
        return Formatter.formatter.format_foreign_key_node(item)