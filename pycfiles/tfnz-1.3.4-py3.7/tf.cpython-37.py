# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/tfnz/cli/tf.py
# Compiled at: 2018-05-18 20:34:30
# Size of source mod 2**32: 12081 bytes
import sys, re, os, os.path, argparse
from sys import argv, stderr
from messidge import default_location, create_account
from tfnz.location import Location
from tfnz.volume import Volume
from tfnz.docker import Docker
from tfnz.endpoint import Cluster
from tfnz.cli import base_argparse, systemd, Interactive

def main_impl():
    try:
        default_location(prefix='~/.20ft')
    except RuntimeError:
        if len(argv) != 3:
            print("\nEither there is no a 20ft account on this machine, and you need \nto request access from your administrator; or the ~/.20ft/default_location\nfile has been deleted. Run something like...\n\n    echo 'location.20ft.nz' > ~/.20ft/default_location\n\nIf you already have an account on another machine you can merely \ncopy the directory ~/.20ft (and it's contents) to this machine.",
              file=stderr)
            return
        create_account((argv[1]), (argv[2]), prefix='~/.20ft')
        print('Created OK for: %s\n' % argv[1])
        return
    else:
        parser = base_argparse('tfnz')
        launch_group = parser.add_argument_group('launch options')
        launch_group.add_argument('-v', '--verbose', help='verbose logging', action='store_true')
        launch_group.add_argument('-q', '--quiet', help='no logging', action='store_true')
        launch_group.add_argument('-ti', '--interactive', help='interactive, connect stdin and stdout', action='store_true')
        launch_group.add_argument('-e', '--env', help='set an environment variable, possibly from current', action='append',
          metavar='[VAR=value | VAR]')
        launch_group.add_argument('-f', '--file', help='write a pre-boot file', action='append', metavar='src:dest')
        launch_group.add_argument('-m', '--mount', help='mount a volume', action='append', metavar='[uuid:mountpoint | tag:mountpoint]')
        launch_group.add_argument('-p', '--publish', help='add a local->remote tcp proxy', action='append', metavar='8080:80')
        launch_group.add_argument('-w', '--web', help='publish on web endpoint', metavar='subdomain.my.com[:www.my.com[:certname]]')
        development_group = parser.add_argument_group('development options')
        development_group.add_argument('--ssh', help='create an ssh/sftp wrapped shell on given port', metavar='2222')
        development_group.add_argument('-s', help='shorthand for --ssh 2222', action='store_true')
        development_group.add_argument('-z', '--sleep', help='launch the container asleep (instead of entrypoint)', action='store_true')
        server_group = parser.add_argument_group('server options')
        server_group.add_argument('--systemd', help='create a systemd service', metavar='user@server.my.com')
        server_group.add_argument('--identity', help='specify an identity file to use with --systemd', metavar='~/.ssh/some_id.pem')
        parser.add_argument('source', help="if '.' runs the most recently added docker image; else this is the tag or hex id of an image to run.")
        parser.add_argument('command', help='run this command/entrypoint instead', nargs='?')
        parser.add_argument('args', help='arguments to pass to a script or subprocess', nargs=(argparse.REMAINDER))
        args = parser.parse_args()
        preboot = []
        if args.file is not None:
            for e in args.file:
                match = re.match('^[\\w:]*[\\w.\\-\\/]+:[\\w.\\-\\/]+$', e)
                if not match:
                    print('Pre-boot copies need to be in source:destination pairs', file=(sys.stderr))
                    print(("....error in '%s'" % e), file=(sys.stderr))
                    return
                    files = e.split(':')
                    if files[1][-1:] == '/':
                        files[1] += files[0]
                    try:
                        with open(files[0], 'rb') as (f):
                            preboot.append((files[1], f.read()))
                    except FileNotFoundError:
                        print(('Could not find the source pre-boot file: ' + files[0]), file=(sys.stderr))
                        return

        endpoint = None
        rewrite = None
        cert = None
        fqdns = None
        if args.web is not None:
            fqdns = args.web.split(':')
            if len(fqdns) == 0 or len(fqdns[0]) == 0:
                print('Cannot publish to an endpoint without an address', file=(sys.stderr))
                return
            endpoint = fqdns[0]
            if len(fqdns) > 1:
                if len(fqdns[1]) > 0:
                    rewrite = fqdns[1]
            if len(fqdns) > 2 and len(fqdns[2]) > 0:
                cert = (
                 fqdns[2] + '.crt', fqdns[2] + '.key')
                if not os.path.exists(cert[0]):
                    print(('Cannot find certificate for ssl: ' + cert[0]), file=(sys.stderr))
                    return
                if not os.path.exists(cert[1]):
                    print(('Cannot find key for ssl: ' + cert[1]), file=(sys.stderr))
                    return
        location = None
        try:
            location = Location(location=(args.location), location_ip=(args.local), quiet=(args.quiet), debug_log=(args.verbose))
        except BaseException as e:
            try:
                print(('Failed while connecting to location: ' + str(e)), file=(sys.stderr))
                return location
            finally:
                e = None
                del e

        if args.systemd is not None:
            systemd(location, args, argv, preboot, cert)
            return location
        if args.source == '.':
            args.source = Docker.last_image()
        e_vars = set()
        environment = []
        if args.env is not None:
            for e in args.env:
                match_single = re.match('^[[0-9A-Za-z:_]+$', e)
                if match_single:
                    if e not in os.environ:
                        print("Environment variable '%s' was not found in the local environment.", file=(sys.stderr))
                        return location
                    e += "='%s'" % os.environ[e]
                match_extended = re.match('^[0-9A-Za-z:_]+=', e)
                if not match_extended:
                    print("Environment variables need to be passed as 'name' or 'name=value' pairs", file=(sys.stderr))
                    print(("....error in '%s'" % e), file=(sys.stderr))
                    return location
                    variable = match_extended.group(0)[:-1]
                    if variable in e_vars:
                        print('Can only pass one value per environment variable.', file=(sys.stderr))
                        print(("....error in '%s'" % e), file=(sys.stderr))
                        return location
                    value = e[len(variable) + 1:]
                    e_vars.add(variable)
                    environment.append((variable, value))

        l_ports = set()
        portmap = []
        if args.publish is not None:
            for e in args.publish:
                match = re.match('\\d+:\\d+$', e)
                if not match:
                    print('Portmaps need to be passed as number:number pairs', file=(sys.stderr))
                    print(("....error in '%s'" % e), file=(sys.stderr))
                    return location
                    local, remote = e.split(':')
                    if local in l_ports:
                        print('Cannot bind a local port twice.', file=(sys.stderr))
                        print(("....error in '%s'" % e), file=(sys.stderr))
                        return location
                    l_ports.add(local)
                    portmap.append((local, remote))

        volumes = []
        mount_points = set()
        if args.mount is not None:
            for m in args.mount:
                if ':' not in m:
                    print('Volumes need to be passed as uuid:mountpoint pairs', file=(sys.stderr))
                    print(("....error in '%s'" % m), file=(sys.stderr))
                    return location
                find = m.rfind(':')
                key = m[:find]
                mount = m[find + 1:]
                intersection = Volume.trees_intersect(mount_points, mount)
                if intersection is not None:
                    print(('Error in volumes: %s is a subtree of %s' % (intersection[0], intersection[1])), file=(sys.stderr))
                    return location
                try:
                    volumes.append((location.volumes.get(location.user_pk, key), mount))
                except KeyError:
                    print('Could not find volume: ' + key)
                    return location
                else:
                    mount_points.add(mount)

        if args.command is not None:
            if args.args is not None:
                args.command = [
                 args.command]
                args.command.extend(args.args)
        try:
            node = location.node()
            container = node.spawn_container((args.source), env=environment,
              pre_boot_files=preboot,
              volumes=volumes,
              stdout_callback=(Interactive.stdout_callback),
              termination_callback=(location.complete),
              command=(args.command),
              sleep=(args.sleep))
            container.wait_until_ready()
        except BaseException as e:
            try:
                print(('Failed while spawning container: ' + str(e)), file=(sys.stderr))
                return location
            finally:
                e = None
                del e

        try:
            for m in portmap:
                container.attach_tunnel((m[1]), localport=(m[0]))

        except OSError as e:
            try:
                print('Failed while creating a tunnel onto the container: ' + str(e))
                return location
            finally:
                e = None
                del e

        try:
            if args.ssh or args.s:
                container.create_ssh_server(2222 if args.s else int(args.ssh))
        except OSError as e:
            try:
                print('Failed while creating an ssh server onto the container: ' + str(e))
                return location
            finally:
                e = None
                del e

        try:
            if args.web is not None:
                container.wait_until_ready()
                clstr = Cluster(containers=[container], rewrite=rewrite)
                ep = location.endpoint_for(endpoint)
                ep.publish(clstr, (fqdns[0]), ssl=cert)
        except ValueError as e:
            try:
                print('Failed while publishing to an endpoint: ' + str(e))
                return location
            finally:
                e = None
                del e

        interactive = None
        if args.interactive:
            interactive = Interactive(container)
        try:
            try:
                location.run()
            except BaseException as e:
                try:
                    print(e)
                finally:
                    e = None
                    del e

        finally:
            if interactive is not None:
                interactive.stop()

        return location


def main():
    maybe_location = main_impl()
    if maybe_location is not None:
        maybe_location.disconnect()


if __name__ == '__main__':
    main()