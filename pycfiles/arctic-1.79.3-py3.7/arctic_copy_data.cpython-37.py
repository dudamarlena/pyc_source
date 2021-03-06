# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/arctic/scripts/arctic_copy_data.py
# Compiled at: 2019-02-02 17:02:31
# Size of source mod 2**32: 4990 bytes
import argparse, logging, os, pwd
from multiprocessing import Pool
from arctic.decorators import _get_host
from arctic.store.audit import ArcticTransaction
from .utils import setup_logging
from ..date import DateRange, to_pandas_closed_closed, CLOSED_OPEN, OPEN_CLOSED
from ..hosts import get_arctic_lib
logger = logging.getLogger(__name__)
USER = pwd.getpwuid(os.getuid())[0]

def copy_symbols_helper(src, dest, log, force, splice):

    def _copy_symbol(symbols):
        for symbol in symbols:
            with ArcticTransaction(dest, symbol, USER, log) as (mt):
                existing_data = dest.has_symbol(symbol)
                if existing_data:
                    if force:
                        logger.warn('Symbol: %s already exists in destination, OVERWRITING' % symbol)
                    else:
                        if splice:
                            logger.warn('Symbol: %s already exists in destination, splicing in new data' % symbol)
                        else:
                            logger.warn('Symbol: {} already exists in {}@{}, use --force to overwrite or --splice to join with existing data'.format(symbol, _get_host(dest).get('l'), _get_host(dest).get('mhost')))
                            continue
                version = src.read(symbol)
                new_data = version.data
                if existing_data:
                    if splice:
                        original_data = dest.read(symbol).data
                        preserve_start = to_pandas_closed_closed(DateRange(None, (new_data.index[0].to_pydatetime()), interval=CLOSED_OPEN)).end
                        preserve_end = to_pandas_closed_closed(DateRange((new_data.index[(-1)].to_pydatetime()), None,
                          interval=OPEN_CLOSED)).start
                        if not original_data.index.tz:
                            preserve_start = preserve_start.replace(tzinfo=None)
                            preserve_end = preserve_end.replace(tzinfo=None)
                        before = original_data.loc[:preserve_start]
                        after = original_data[preserve_end:]
                        new_data = before.append(new_data).append(after)
                mt.write(symbol, new_data, metadata=(version.metadata))

    return _copy_symbol


def main():
    usage = '\n    Copy data from one MongoDB instance to another.\n\n    Example:\n        arctic_copy_data --log "Copying data" --src user.library@host1 --dest user.library@host2 symbol1 symbol2\n    '
    setup_logging()
    p = argparse.ArgumentParser(usage=usage)
    p.add_argument('--src', required=True, help='Source MongoDB like: library@hostname:port')
    p.add_argument('--dest', required=True, help='Destination MongoDB like: library@hostname:port')
    p.add_argument('--log', required=True, help='Data CR')
    p.add_argument('--force', default=False, action='store_true', help='Force overwrite of existing data for symbol.')
    p.add_argument('--splice', default=False, action='store_true', help='Keep existing data before and after the new data.')
    p.add_argument('--parallel', default=1, type=int, help='Number of imports to run in parallel.')
    p.add_argument('symbols', nargs='+', type=str, help='List of symbol regexes to copy from source to dest.')
    opts = p.parse_args()
    src = get_arctic_lib(opts.src)
    dest = get_arctic_lib(opts.dest)
    logger.info('Copying data from %s -> %s' % (opts.src, opts.dest))
    required_symbols = set()
    for symbol in opts.symbols:
        required_symbols.update(src.list_symbols(regex=symbol))

    required_symbols = sorted(required_symbols)
    logger.info('Copying: {} symbols'.format(len(required_symbols)))
    if len(required_symbols) < 1:
        logger.warn('No symbols found that matched those provided.')
        return
    else:
        copy_symbol = copy_symbols_helper(src, dest, opts.log, opts.force, opts.splice)
        if opts.parallel > 1:
            logger.info('Starting: {} jobs'.format(opts.parallel))
            pool = Pool(processes=(opts.parallel))
            chunk_size = len(required_symbols) / opts.parallel
            chunk_size = max(chunk_size, 1)
            chunks = [required_symbols[offs:offs + chunk_size] for offs in range(0, len(required_symbols), chunk_size)]
            assert sum((len(x) for x in chunks)) == len(required_symbols)
            pool.apply(copy_symbol, chunks)
        else:
            copy_symbol(required_symbols)


if __name__ == '__main__':
    main()