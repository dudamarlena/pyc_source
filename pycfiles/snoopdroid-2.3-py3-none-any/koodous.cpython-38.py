# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/nex/projects/snoopdroid/snoopdroid/koodous.py
# Compiled at: 2020-04-03 08:08:14
# Size of source mod 2**32: 2472 bytes
import requests
from halo import Halo
from terminaltables import AsciiTable
from .ui import info, highlight, green, red

def get_koodous_report(sha256):
    url = 'https://api.koodous.com/apks/{}'.format(sha256)
    res = requests.get(url)
    return res.json()


def koodous_lookup(packages):
    print(info('Looking up all extracted files on ' + highlight('Koodous') + ' (www.koodous.com).'))
    print(info('This might take a while...'))
    print('')
    table_data = []
    table_data.append(['Package name', 'File path', 'Trusted', 'Detected', 'Rating'])
    with Halo(text='', spinner='bouncingBar') as (spinner):
        total_packages = len(packages)
        counter = 0
        for package in packages:
            counter += 1
            spinner.text = 'Looking up {} [{}/{}]'.format(package.name, counter, total_packages)
            for file in package.files:
                report = get_koodous_report(file['sha256'])
                if 'package_name' in report:
                    trusted = 'no'
                    if report['trusted']:
                        trusted = green('yes')
                    detected = 'no'
                    if report['detected']:
                        detected = red('yes')
                    rating = '0'
                    if int(report['rating']) < 0:
                        rating = red(str(report['rating']))
                    row = [package.name, file['stored_path'], trusted, detected, rating]
                else:
                    row = [
                     package.name, file['stored_path'], '', '', '']
                table_data.append(row)

        else:
            spinner.succeed('Completed!')

    print('')
    table = AsciiTable(table_data)
    print(table.table)