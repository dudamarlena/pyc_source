# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/scpketer/Dev/rknfind/.env/lib/python3.7/site-packages/rknfind/__main__.py
# Compiled at: 2019-09-21 08:13:35
# Size of source mod 2**32: 6208 bytes
from sys import exit, stderr
from pathlib import Path
from datetime import datetime
from pkg_resources import get_distribution, resource_filename
from appdirs import AppDirs
distrib = get_distribution('rknfind')
dirs = AppDirs(appname=(distrib.project_name), version=(distrib.version))
pkgdir = Path(resource_filename('rknfind', ''))
rkn_git = 'https://github.com/zapret-info/z-i'
rkn_sfp = 'https://github.com/zapret-info/z-i/raw/master/dump.csv'
try:
    from git import refresh
    refresh()
    _feature_git = True
    from rknfind.rkn.dump import GitProvider
    provider = GitProvider(rkn_git)
    _sync_args = []
    _sync_kwargs = {'depth': 1}
except ImportError:
    _feature_git = False
    from rknfind.rkn.dump import SimpleFileProvider
    provider = SimpleFileProvider(rkn_sfp)
    _sync_args = []
    _sync_kwargs = {}

try:
    import peewee
    _feature_peewee = True
except ImportError:
    _feature_peewee = False

def main():
    from rknfind.app.i18n import tl
    from rknfind.rkn import csv
    from rknfind.util import json
    from rknfind.app.cli import args
    arguments = args.get_args()
    if not arguments.filter:
        print(tl('No filters provided, exiting.'))
        exit(0)
    else:
        print(tl('Synchronizing dump file...'))
        try:
            (provider.sync)(*_sync_args, **_sync_kwargs)
        except KeyboardInterrupt:
            print(tl('Aborted.'))
            exit(0)
        except Exception:
            print((tl('Failed to synchronize dump file.')), file=stderr)
            if not provider.file_path().exists():
                print(tl('Dump file is not downloaded yet, cannot proceed.'))
                exit(1)
        else:
            last_update = provider.last_update()
            print(last_update.strftime(tl('Done. Last update: %d-%m-%Y %H:%M:%S')))
        if arguments.json:
            from json import dumps
        if arguments.export:
            if not _feature_peewee:
                print(tl('peewee is not installed, unable to export to SQLite database.\nFollow instructions at GitHub to install required dependencies.'))
            else:
                from rknfind.db import model
                from peewee import SqliteDatabase
                database = model.database
                database.init(arguments.export)
                database.create_tables([model.BlockAddress, model.BlockDomain,
                 model.BlockEntry, model.BlockURL],
                  safe=True)

                @database.atomic()
                def store(entry):
                    db_entry = model.BlockEntry.create(decree=(entry.decree), date=(entry.date),
                      issuer=(entry.issuer))
                    addr_data = []
                    for addr in entry.addr:
                        addr_data.append({'address':addr,  'entry':db_entry})

                    model.BlockAddress.insert_many(addr_data).execute()
                    url_data = []
                    for url in entry.url:
                        url_data.append({'url':url,  'entry':db_entry})

                    model.BlockURL.insert_many(url_data).execute()
                    domain_data = []
                    for domain in entry.domain:
                        domain_data.append({'domain':domain,  'entry':db_entry})

                    model.BlockDomain.insert_many(domain_data).execute()

    print(tl('Now searching...'))
    fd = open((provider.file_path()), encoding='windows-1251')
    fd.readline()
    try:
        results = 0
        skip = 0
        for entry in csv.entries(fd):
            param_matches = 0
            for search_param in arguments.filter:
                field = search_param[0]
                occurence = search_param[1]
                if entry.match(field if field != '*' else None, occurence, arguments.glob, arguments.regexp):
                    param_matches += 1

            if param_matches >= len(arguments.filter):
                if arguments.export:
                    if _feature_peewee:
                        store(entry)
            if arguments.offset:
                if skip < arguments.offset:
                    skip += 1
                    continue
                if arguments.json:
                    entry_str = json(entry)
                else:
                    entry_format = {'decree':entry.decree, 
                     'issuer':entry.issuer, 
                     'urls':', '.join(entry.url), 
                     'addresses':', '.join(entry.addr), 
                     'domains':', '.join(entry.domain), 
                     'date':entry.date}
                    entry_str = (tl('== BEGIN ENTRY ==\nDecree:    {decree}\nIssuer:    {issuer}\nURLs:      {urls}\nAddresses: {addresses}\nDomains:   {domains}\nDate:      {date}\n== END ENTRY ==\n').format)(**entry_format)
                print(entry_str)
                if arguments.limit:
                    results += 1
                    if results >= arguments.limit:
                        break

    except KeyboardInterrupt:
        print(tl('\nAborted.'))