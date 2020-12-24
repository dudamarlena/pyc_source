# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pyvigicrues/__main__.py
# Compiled at: 2019-01-01 18:57:00
# Size of source mod 2**32: 686 bytes
import argparse, sys, json
from pyvigicrues.client import VigicruesClient

def main():
    """Main function"""
    parser = argparse.ArgumentParser()
    parser.add_argument('-s', '--stationid', required=True, help='Station ID (Ex: H523102501)')
    parser.add_argument('-t', '--type', required=True, help='Station ID (Ex: H for Height / Q for Speed)')
    args = parser.parse_args()
    client = VigicruesClient(args.stationid, args.type)
    try:
        print(json.dumps(client.get_data(), indent=2))
    except BaseException as exp:
        print(exp)
        return 1


if __name__ == '__main__':
    sys.exit(main())