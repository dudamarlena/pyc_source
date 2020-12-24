# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/nushell/examples/len/nu_plugin_len.py
# Compiled at: 2019-10-24 12:25:31
# Size of source mod 2**32: 1368 bytes
from nushell.sink import FilterPlugin

def runFilter(plugin, params):
    """sink will be executed by the calling SinkPlugin when method is "sink"
       and should be able to parse the dictionary of params and respond
       appropriately. Since this is a sink, whatever you print to stdout
       will show for the user. Useful functions:

       plugin.logger.<level>
    """
    value = plugin.get_string_primitive(params)
    intLength = len(value)
    plugin.print_int_response(intLength)


def main():
    plugin = FilterPlugin(name='len', usage='Catch an asciinema pokemon on demand.')
    plugin.run(runFilter)


if __name__ == __main__:
    main()