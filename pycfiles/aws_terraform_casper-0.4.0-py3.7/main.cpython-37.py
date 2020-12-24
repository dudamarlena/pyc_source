# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/casper/main.py
# Compiled at: 2020-02-03 17:04:46
# Size of source mod 2**32: 7063 bytes
"""
Casper.

Usage:
    casper.py build [--root-dir=<dir> --bucket-name=<bn> --state-file=<sf> --aws-profile=<profile> --exclude-dirs=<ed> --exclude-state-res=<esr> --loglevel=<lvl>]
    casper.py scan  [--root-dir=<dir> --bucket-name=<bn> --state-file=<sf> --aws-profile=<profile> --services=<svc> --exclude-dirs=<ed> --exclude-cloud-res=<ecr> --rebuild --detailed --output-file=<f>  --loglevel=<lvl>]
    casper.py -h | --help
    casper.py --version

Options:
    -h --help                               Show this screen.
    --version                               Show version.
    --root-dir=<dir>                        The root terraform directory [default: .].
    --bucket-name=<bn>                      If specified, state is saved to and retrieved from that s3 bucket instead of locally.
    --state-file=<sf>                       Name used to save state file [default: terraform_state].
    --exclude-dirs=<ed>                     Comma separated list of directories to ignore.
    --exclude-state-res=<res>               Comma separated list of terraform state resources to ignore.
    --aws-profile=<profile>                 AWS profile to use.
    --services=<svc>                        Comma separated list of services to scan, default is to scan all supported services.
    --exclude-cloud-res=<ecr>               Comma separated list of resources ids to ignore.
    --rebuild                               Rebuild and save state first before scanning.
    --detailed                              Retrieve and include details about the resources discovered through scan.
    --output-file=<f>                       Output full result to specified file.
    --loglevel=<lvl>                        Log level [default: INFO].

"""
from docopt import docopt
import os, json, logging, logging.config
from casper.services.base import SUPPORTED_SERVICES
from casper import Casper, version

def _setup_logging(loglevel='INFO'):
    logger = logging.getLogger('casper')
    numeric_level = getattr(logging, loglevel.upper(), None)
    if not isinstance(numeric_level, int):
        raise ValueError('Invalid log level: %s' % loglevel)
    logger.setLevel(numeric_level)
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    ch.setFormatter(formatter)
    logger.addHandler(ch)


def run(build_command, scan_command, root_dir, aws_profile, detailed, output_file, exclude_cloud_res, services_list, exclude_state_res, exclude_dirs, state_file, bucket_name, loglevel):
    _setup_logging(loglevel=loglevel)
    logger = logging.getLogger('casper')
    if exclude_cloud_res:
        exclude_cloud_res = set(exclude_cloud_res)
    else:
        casper = Casper(start_directory=root_dir,
          bucket_name=bucket_name,
          state_file=state_file,
          profile=aws_profile,
          exclude_resources=exclude_cloud_res)
        if build_command:
            if exclude_state_res:
                exclude_state_res = set(exclude_state_res)
            if exclude_dirs:
                exclude_dirs = set(exclude_dirs)
            counters = casper.build(exclude_state_res=exclude_state_res,
              exclude_directories=exclude_dirs)
            states = counters['state']
            resource_groups = counters['resource_group']
            resources = counters['resource']
            print('')
            print('Terraform')
            print('--------------------------------------------------------')
            print(f"{states} state(s) checked")
            print(f"{resource_groups} supported resource group(s) discovered")
            print(f"{resources} state resource(s) saved to bucket")
            print('')
        elif scan_command:
            if services_list:
                services = [s for s in services_list if s in SUPPORTED_SERVICES]
                if len(services) == 0:
                    logger.warning('No supported service specified')
            elif len(services) < len(services_list):
                logger.warning('Ignoring one or more unsupported services')
        else:
            services = SUPPORTED_SERVICES.keys()
    svc_ghost = {}
    for svc in services:
        svc_ghost[svc] = casper.scan(service_name=svc, detailed=detailed)

    print('')
    for svc in services:
        print(svc.upper())
        print('--------------------------------------------------------')
        for key in svc_ghost[svc].keys():
            count = svc_ghost[svc][key]['count']
            if count > 0:
                print(f"{count} ghost {key} found")

        print('')

    if output_file:
        with open(output_file, 'w') as (fid):
            fid.write(json.dumps(svc_ghost, indent=4, sort_keys=True, default=str))
        print('--------------------------------------------------------')
        print(f"Full result written to {os.path.join(os.getcwd(), output_file)}")


def cli():
    args = docopt(__doc__)
    if args['--version']:
        print(f"Casper v{version.__version__}")
        return
    build_command = args['build']
    scan_command = args['scan']
    aws_profile = args['--aws-profile']
    bucket_name = args['--bucket-name']
    if bucket_name is None:
        casper_bucket = os.environ.get('CASPER_BUCKET', None)
        if casper_bucket:
            bucket_name = casper_bucket
    state_file = args['--state-file']
    root_dir = args['--root-dir']
    exclude_dirs = args['--exclude-dirs']
    if exclude_dirs:
        exclude_dirs = exclude_dirs.split(',')
    exclude_state_res = args['--exclude-state-res']
    if exclude_state_res:
        exclude_state_res = exclude_state_res.split(',')
    services = args['--services']
    if services:
        services = services.split(',')
    exclude_cloud_res = args['--exclude-cloud-res']
    if exclude_cloud_res:
        exclude_cloud_res = exclude_cloud_res.split(',')
    rebuild = args['--rebuild']
    detailed = args['--detailed']
    output_file = args['--output-file']
    if rebuild:
        build_command = True
    loglevel = args['--loglevel']
    run(build_command=build_command,
      scan_command=scan_command,
      root_dir=root_dir,
      aws_profile=aws_profile,
      detailed=detailed,
      output_file=output_file,
      exclude_cloud_res=exclude_cloud_res,
      services_list=services,
      exclude_state_res=exclude_state_res,
      exclude_dirs=exclude_dirs,
      state_file=state_file,
      bucket_name=bucket_name,
      loglevel=loglevel)


if __name__ == '__main__':
    cli()