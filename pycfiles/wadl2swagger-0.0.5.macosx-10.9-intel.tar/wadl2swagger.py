# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/Thoughtworker/Envs/wadl2swagger/lib/python2.7/site-packages/wadltools/cli/wadl2swagger.py
# Compiled at: 2014-11-07 11:51:50
import os, errno, argparse, logging, wadltools
from wadltools import WADL, SwaggerConverter, BadWADLError
from collections import OrderedDict
import yaml

def mkdir_p(path):
    try:
        os.makedirs(path)
    except OSError as exc:
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else:
            raise


def main():
    parser = argparse.ArgumentParser()
    parser = argparse.ArgumentParser(add_help=True)
    parser.add_argument('--swagger-dir', type=str, default='swagger/', help='output folder for converted Swagger files')
    parser.add_argument('--merge-dir', type=str, default='defaults/', help='folder contains partial Swagger YAML files to merge with the WADL data')
    parser.add_argument('--autofix', dest='autofix', action='store_true', help='fix common Swagger issues (rather than fixing them by standardizing WADL)')
    parser.add_argument('--fail-fast', dest='failfast', action='store_true', help='Fail on the first problematic WADL or attempt to continue and convert the rest')
    parser.add_argument('--strict', dest='strict', action='store_true', help='fail on data that cannot be converted or just print a warning and skip it')
    parser.add_argument('wadl_file', nargs='+', metavar='WADL_FILE', help='wadl files to convert')
    parser.add_argument('-v', '--verbose', help='increase output verbosity', action='store_true')
    args = parser.parse_args()
    failed = {}
    if args.verbose:
        logging.basicConfig(level=logging.DEBUG, filename='wadl2swagger.log', filemode='w')
    else:
        logging.basicConfig(level=logging.INFO, filename='wadl2swagger.log', filemode='w')
    logging.getLogger('').addHandler(logging.StreamHandler())
    for wadl_file in args.wadl_file:
        filename, wadl_ext = os.path.splitext(os.path.split(wadl_file)[1])
        swagger_file = os.path.join(args.swagger_dir, filename + '.yaml')
        mkdir_p(os.path.dirname(swagger_file))
        converter = SwaggerConverter(args)
        try:
            swagger = converter.convert(filename, wadl_file, swagger_file)
            logging.info('Saving swagger to %s', swagger_file)
            save_swagger(swagger, swagger_file)
        except BadWADLError as e:
            failed[wadl_file] = e
            if args.failfast:
                raise e
            else:
                logging.error(str(e))
                None

    summarize_and_exit(failed)
    return


def summarize_and_exit(failed):
    logging.info('')
    if len(failed) == 0:
        logging.info('Successfully converted all WADL files')
        exit(0)
    else:
        logging.info('Failed to convert:')
        for wadl_file, error in failed.iteritems():
            logging.info('  %s : %s' % (wadl_file, error))

        exit(1)


def save_swagger(swagger, filename):
    with open(filename, 'w') as (yaml_file):
        yaml_file.write(yaml.dump(swagger, default_flow_style=False))


if __name__ == '__main__':
    main()