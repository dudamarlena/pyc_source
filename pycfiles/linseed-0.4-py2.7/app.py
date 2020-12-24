# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/linseed/app.py
# Compiled at: 2012-02-12 04:45:55
import os, baker, pkg_resources, linseed

@baker.command
def basic():
    """A simple, default linseed status line.

    This just tries to grab status information from every configured
    plugin.
    """
    mgr = linseed.InfoSourceManager()
    for k, v in mgr.items():
        print (
         k, str(v()))


@baker.command(params={'config_file': 'The python module containing the `format()` method.'}, default=True)
def custom(config_file='~/.linseed.conf'):
    """This loads a config file as a python module and print the
    results of calling that module's `format()` method.

    This loads `config_file` as a python module and looks for a method
    called 'format()' in that module. This then calls that method,
    passing an InfoSourceManager object as the first
    parameter. Finally, this prints whatever is returned from
    `format()`.

    """
    import imp
    config_file = os.path.abspath(os.path.expanduser(config_file))
    with open(config_file, 'r') as (f):
        config_module = imp.load_module('linseed_conf', f, config_file, (
         '.conf', 'r', imp.PY_SOURCE))
    try:
        mgr = linseed.InfoSourceManager()
        print config_module.format(mgr)
    except AttributeError as e:
        print ('Error with configuration: {0}').format(e)


@baker.command
def info_sources():
    """List the available 'info_source' extensions.
    """
    for p in pkg_resources.iter_entry_points('linseed.info_source'):
        p = p.load()
        print ('{0}\n\t{1}').format(p.name(), p.description())


def main():
    baker.run()


if __name__ == '__main__':
    main()