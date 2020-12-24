# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.10-x86_64/egg/pyparts/parts.py
# Compiled at: 2015-03-07 08:59:35
# Size of source mod 2**32: 18220 bytes
"""Pyparts: command line tool to search for parts

Usage:
  pyparts [-k <apikey>] [-t <target>] [-c <config>] [--help] [--version] [--verbose] <command> [<args>...]

Options:
  -k <apikey>          Gives apikey
  -t <target>          Selects aggregator.      [default: octopart]
  -c --config <conf>   Use configuration file. [default: ~/.config/pyparts.cfg]
  -h --help            Show this screen.
  --version            Show version, copyleft and licensing info.
  --verbose            Show more details.

Commands:
  lookup         Search part
  specs          Get specs for a part
  datasheet      Download part's datasheet
  open           Open part's page in browser
  help           Give help for a command

See `pyparts help <command>` to get more information on a command
"""
import sys, shutil, logging, requests, tempfile, webbrowser, subprocess, pkg_resources
from enum import IntEnum
from docopt import docopt
from os.path import expanduser
from configparser import ConfigParser
from pyoctopart.octopart import Octopart
from pyoctopart.exceptions import OctopartException
__version__ = pkg_resources.require('pyparts')[0].version
__author__ = 'Bernard `Guyzmo` Pratz'
__contributors = []

class ReturnValues(IntEnum):
    OK = 0
    NO_RESULTS = 1
    NO_APIKEY = 2
    RUNTIME_ERROR = 255


def getTerminalSize():
    """
    Snippet courtesy of Johannes Weiß, as found on http://stackoverflow.com/a/566752/1290438
    returns tuple containing terminal height and width
    """
    import os
    env = os.environ

    def ioctl_GWINSZ(fd):
        try:
            import fcntl, termios, struct, os
            cr = struct.unpack('hh', fcntl.ioctl(fd, termios.TIOCGWINSZ, '1234'))
        except:
            return

        return cr

    cr = ioctl_GWINSZ(0) or ioctl_GWINSZ(1) or ioctl_GWINSZ(2)
    if not cr:
        try:
            fd = os.open(os.ctermid(), os.O_RDONLY)
            cr = ioctl_GWINSZ(fd)
            os.close(fd)
        except:
            pass

    if not cr:
        cr = (
         env.get('LINES', 25), env.get('COLUMNS', 80))
    return (
     int(cr[1]), int(cr[0]))


term_size = getTerminalSize()[1]
draw_pbar = lambda seen, size: sys.stdout.write('[{}>{}]\r'.format('-' * int(seen / size * term_size), ' ' * (term_size - int(seen / size * term_size))))

def download_file(url, filename=None, show_progress=draw_pbar):
    """
    Download a file and show progress

    url: the URL of the file to download
    filename: the filename to download it to (if not given, uses the url's filename part)
    show_progress: callback function to update a progress bar

    the show_progress function shall take two parameters: `seen` and `size`, and
    return nothing.

    This function returns the filename it has written the result to.
    """
    if filename is None:
        filename = url.split('/')[(-1)]
    r = requests.get(url, stream=True)
    size = int(r.headers['Content-Length'].strip())
    seen = 0
    show_progress(0, size)
    seen = 1024
    with open(filename, 'wb') as (f):
        for chunk in r.iter_content(chunk_size=1024):
            seen += 1024
            show_progress(seen, size)
            if chunk:
                f.write(chunk)
                f.flush()
                continue

    return filename


if 'win32' == sys.platform:
    platform_open_cmd = 'start'
else:
    if 'darwin' == sys.platform:
        platform_open_cmd = 'open'
    elif 'linux' in sys.platform:
        platform_open_cmd = 'xdg-open'

class PyPartsBase:

    def __init__(self, apikey, verbose=False):
        raise NotImplementedError

    def part_search(self, part_query):
        raise NotImplementedError

    def part_search(self, part_query):
        raise NotImplementedError

    def part_datasheet(self, part, command=None, path=None):
        raise NotImplementedError

    def part_show(self, part, printout=False):
        raise NotImplementedError


class PyPartsPartsIO(PyPartsBase):
    pass


class PyPartsOctopart(PyPartsBase):
    __doc__ = '\n    Implementation of the part browse engine\n    '

    def __init__(self, apikey, verbose=False):
        """
        instanciate an engine
        """
        self._e = Octopart(apikey=apikey, verbose=verbose)

    def part_search(self, part_query):
        """
        handles the part lookup/search for the given part query

        part_query: part string to search as product name

        outputs result on stdout
        """
        limit = 100
        results = self._e.parts_search(q=part_query, limit=limit)
        start = 0
        hits = results[0]['hits']
        if hits == 0:
            print('No result')
            return ReturnValues.NO_RESULTS
        print("Searched for: '{}'".format(results[0]['request']['q']))

        def show_result(r):
            print(' → {:30} {:30} {}'.format(r['item']['mpn'], r['item']['manufacturer']['name'], r['snippet']))

        for r in results[1]:
            show_result(r)

        while hits - limit > limit:
            start += limit
            hits -= limit
            results = self._e.parts_search(q=part_query, limit=limit, start=start)
            for r in results[1]:
                show_result(r)

        if hits - limit > 0:
            start += limit
            hits -= limit
            results = self._e.parts_search(q=part_query, limit=hits, start=start)
            for r in results[1]:
                show_result(r)

        return ReturnValues.OK

    def part_specs(self, part):
        """
        returns the specifications of the given part. If multiple parts are
        matched, only the first one will be output.

        part: the productname or sku

        prints the results on stdout
        """
        result = self._e.parts_match(queries=[{'mpn_or_sku': part}], exact_only=True, show_mpn=True, show_manufacturer=True, show_octopart_url=True, show_short_description=True, show_specs=True, show_category_uids=True, show_external_links=True, show_reference_designs=True, show_cad_models=True, show_datasheets=True, include_specs=True, include_category_uids=True, include_external_links=True, include_reference_designs=True, include_cad_models=True, include_datasheets=True)
        if result[1][0]['hits'] == 0:
            print('No result')
            return ReturnValues.NO_RESULTS
        result = result[1][0]['items'][0]
        print("Showing specs for '{}':".format(result['mpn']))
        print(' → Manufacturer:      {}'.format(result['manufacturer']['name']))
        print('  → Specifications:    ')
        for k, v in result['specs'].items():
            name = v['metadata']['name'] if v['metadata']['name'] else k
            min_value = v['min_value'] if v['min_value'] else ''
            max_value = v['max_value'] if v['max_value'] else ''
            unit = ' ({})'.format(v['metadata']['unit']['name']) if v['metadata']['unit'] else ''
            value = ','.join(v['value']) if len(v['value']) > 0 else ''
            if value and not (min_value or max_value):
                print('    → {:20}: {}{}'.format(name, value, unit))
            elif value and min_value and max_value:
                print('    → {:20}: {}{} (min: {}, max: {})'.format(name, value, unit, min_value, max_value))
            elif not value and min_value and max_value:
                print('    → {:20}:{} min: {}, max: {}'.format(name, unit, min_value, max_value))
            elif not value and min_value and not max_value:
                print('    → {:20}:{} min: {}'.format(name, unit, min_value))
            elif not value and not min_value and max_value:
                print('    → {:20}:{} max: {}'.format(name, unit, max_value))
                continue

        print(' → URI:               {}'.format(result['octopart_url']))
        if result['external_links']['evalkit_url'] or result['external_links']['freesample_url'] or result['external_links']['product_url']:
            print('  → External Links')
            if result['external_links']['evalkit_url']:
                print('    → Evaluation kit: {}'.format(result['external_links']['evalkit_url']))
            if result['external_links']['freesample_url']:
                print('    → Free Sample: {}'.format(result['external_links']['freesample_url']))
            if result['external_links']['product_url']:
                print('    → Product URI: {}'.format(result['external_links']['product_url']))
        if len(result['datasheets']) > 0:
            print('  → Datasheets')
            for datasheet in result['datasheets']:
                print('    → URL:      {}'.format(datasheet['url']))
                if datasheet['metadata']:
                    print('      → Updated:  {}'.format(datasheet['metadata']['last_updated']))
                    print('      → Nb Pages: {}'.format(datasheet['metadata']['num_pages']))
                    continue

        if len(result['reference_designs']) > 0:
            print('  → Reference designs: ')
        if len(result['cad_models']) > 0:
            print('  → CAD Models:        ')
        return ReturnValues.OK

    def part_datasheet(self, part, command=None, path=None):
        """
        downloads and/or shows the datasheet of a given part

        command: if set will use it to open the datasheet.
        path: if set will download the file under that path.

        if path is given alone, the file will only get downloaded,
        if command is given alone, the file will be downloaded in a temporary
        folder, which will be destroyed just after being opened.
        if both path and command are given, the file will be downloaded and
        stored in the chosen location.
        """
        result = self._e.parts_match(queries=[{'mpn_or_sku': part}], exact_only=True, show_mpn=True, show_datasheets=True, include_datasheets=True)
        if result[1][0]['hits'] == 0:
            print('No result')
            return ReturnValues.NO_RESULTS
        result = result[1][0]['items'][0]
        print("Downloading datasheet for '{}':".format(result['mpn']))
        try:
            if len(result['datasheets']) > 0:
                for datasheet in result['datasheets']:
                    if not path:
                        path = tempfile.mkdtemp()
                    out = path + '/' + result['mpn'] + '-' + datasheet['url'].split('/')[(-1)]
                    download_file(datasheet['url'], out)
                    print('Datasheet file saved as {}.'.format(out))
                    if command:
                        subprocess.call([command, out])
                        continue

        finally:
            if not path:
                shutil.rmtree(path)

        return ReturnValues.OK

    def part_show(self, part, printout=False):
        """
        Opens/shows the aggregator's URI for the part.

        printout: if set, only printout the URI, do not open the browser.
        """
        result = self._e.parts_match(queries=[{'mpn_or_sku': part}], exact_only=True, show_mpn=True, show_octopart_url=True)
        if result[1][0]['hits'] == 0:
            print('No result')
            return ReturnValues.NO_RESULTS
        result = result[1][0]['items'][0]
        if not printout:
            print("Opening page for part '{}'.".format(result['mpn']))
            webbrowser.open(result['octopart_url'], 2)
        else:
            print("Webpage for part '{}':".format(result['mpn']))
            print('    → URL:      {}'.format(result['octopart_url']))
        return ReturnValues.OK


def main():
    """
    entry point of the application.

    Parses the CLI commands and runs the actions.
    """
    args = CLI.parse_args(__doc__)
    if args['--verbose']:
        requests_log = logging.getLogger('requests.packages.urllib3')
        requests_log.setLevel(logging.DEBUG)
        logging.basicConfig(level=logging.DEBUG)
    if not args['-k']:
        print('No API key given. Please create an API key on <https://octopart.com/api/dashboard>')
        return ReturnValues.NO_APIKEY
    if args['-t'] == 'octopart':
        engine = PyPartsOctopart(args['-k'], verbose=args['--verbose'])
    else:
        if args['-t'] == 'parts.io':
            engine = PyPartsPartsIO(args['-k'], verbose=args['--verbose'])
        else:
            engine = PyPartsBase(args['-k'], verbose=args['--verbose'])
    try:
        if 'lookup' in args or 'search' in args:
            return engine.part_search(args['<part>'])
        if 'specs' in args:
            return engine.part_specs(args['<part>'])
        if 'datasheet' in args:
            if args['<action>'] == 'open':
                if args['--output']:
                    return engine.part_datasheet(args['<part>'], command=args['--command'], path=args['--output'])
                else:
                    return engine.part_datasheet(args['<part>'], command=args['--command'])
            elif args['<action>'] == 'save':
                return engine.part_datasheet(args['<part>'], path=args['--output'])
        elif 'show' in args:
            return engine.part_show(args['<part>'], printout=args['--print'])
    except OctopartException as err:
        print(err)
        return ReturnValues.RUNTIME_ERROR


class Config:
    __doc__ = '\n    Handles the configuration file\n    '

    def __init__(self, config='~/.config/pyparts.cfg'):
        self._conf = ConfigParser()
        self._conf.read(expanduser(config))

    def get_defaults(self):
        if 'general' not in self._conf:
            self._conf['general'] = {}
        if 'defaults' not in self._conf:
            self._conf['defaults'] = {}
        return dict(apikey=self._conf['general'].get('apikey', None), aggregator=self._conf['general'].get('aggregator', 'octopart'), open_cmd=self._conf['defaults'].get('open_cmd', platform_open_cmd), output_path=expanduser(self._conf['defaults'].get('output_path', '.')))


class CLI:
    lookup = "Usage: pyparts lookup [options] <part>\n\nSearch for a part's product name.\n\n\n"
    search = lookup.replace('lookup', 'search')
    specs = " Usage: pyparts specs [options] <part>\n\nOutputs the part's specifications.\n\n"
    datasheet = 'Usage: pyparts datasheet <part> <action> [options]\n\nDownload and show the datasheet(s) of a given part\n\nActions:\n    open    Open datasheet    save    Save datasheet\nOptions:\n    --command <cmd>  Command to use for opening.    [default: {open_cmd}]\n    --output <path>  Path to save the datasheet to. [default: {output_path}]\n\n'
    show = 'Usage: pyparts show [options] <part>\n\nOptions:\n--print          Do not open, just printout URL.\n\n'
    version = 'Pyparts v{version}: command line tool to search for parts\n\nCopyright ©2015 Bernard `Guyzmo` pratz <pyparts at m0g dot net>\nThis is free software; see the source for copying conditions.  There is NO\nwarranty; not even for MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.\n'
    help = __doc__

    @classmethod
    def parse_args(self, doc):
        args = docopt(doc, version=CLI.version.format(version=__version__), options_first=True)
        if args['<command>'] == 'help':
            if len(args['<args>']) > 0:
                sys.exit(subprocess.call([sys.argv[0], args['<args>'][0], '--help']))
            else:
                sys.exit(subprocess.call([sys.argv[0], '--help']))
        defaults = Config(args['--config']).get_defaults()
        if not args['-k']:
            args['-k'] = defaults['apikey']
        if not args['-t']:
            args['-t'] = defaults['aggregator']
        argv = [
         args['<command>']] + args['<args>']
        commands = list(filter(lambda x: not x.startswith('_'), dir(CLI)))
        if args['<command>'] in commands:
            arguments = docopt(getattr(CLI, args['<command>']).format(**defaults), argv=argv)
            del args['<command>']
            del args['<args>']
            arguments.update(args)
            if args['--verbose']:
                print(arguments)
            return arguments
        return args


if __name__ == '__main__':
    main()