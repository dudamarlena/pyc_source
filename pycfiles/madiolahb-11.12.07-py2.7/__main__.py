# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/madiolahb/__main__.py
# Compiled at: 2011-12-07 23:15:58


def main():
    from core import fill_character
    import acting, argparse, chardesc, movement, sys
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', '-o', type=argparse.FileType('w'), default=sys.stdout)
    parser.add_argument('--format', '-f', choices=('JSON', 'YAML'), default='JSON')
    parser.add_argument('--input', '-i', type=argparse.FileType('r'), default=sys.stdin)
    subp = parser.add_subparsers()
    acting.register_commands(subp)
    chardesc.register_commands(subp)
    movement.register_commands(subp)
    args = parser.parse_args()
    lw = None
    if args.format == 'JSON':
        import json
        lw = json.load(args.input)
    elif args.format == 'YAML':
        import yaml
        lw = yaml.load(args.input)
    fill_character(lw)
    args.func(lw, **args.__dict__)
    if args.format == 'JSON':
        import json
        json.dump(lw, args.output)
    elif args.format == 'YAML':
        import yaml
        yaml.dump(lw, args.output)
    return


if __name__ == '__main__':
    main()