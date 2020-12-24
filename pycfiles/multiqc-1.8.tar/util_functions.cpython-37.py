# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/philewels/GitHub/MultiQC/multiqc/utils/util_functions.py
# Compiled at: 2019-11-01 10:12:16
# Size of source mod 2**32: 4363 bytes
""" MultiQC Utility functions, used in a variety of places. """
from __future__ import print_function
import io, json, os, yaml, time, shutil, sys
from multiqc import config

def robust_rmtree(path, logger=None, max_retries=10):
    """Robustly tries to delete paths.
    Retries several times (with increasing delays) if an OSError
    occurs.  If the final attempt fails, the Exception is propagated
    to the caller.
    """
    for i in range(max_retries):
        try:
            shutil.rmtree(path)
            return
        except OSError:
            if logger:
                logger.info('Unable to remove path: {}'.format(path))
                logger.info('Retrying after {} seconds'.format(i ** 2))
            else:
                print(('Unable to remove path: {}'.format(path)), file=(sys.stderr))
                print(('Retrying after {} seconds'.format(i ** 2)), file=(sys.stderr))
            time.sleep(i ** 2)

    shutil.rmtree(path)


def write_data_file(data, fn, sort_cols=False, data_format=None):
    """ Write a data file to the report directory. Will not do anything
    if config.data_dir is not set.
    :param: data - a 2D dict, first key sample name (row header),
            second key field (column header).
    :param: fn - Desired filename. Directory will be prepended automatically.
    :param: sort_cols - Sort columns alphabetically
    :param: data_format - Output format. Defaults to config.data_format (usually tsv)
    :return: None """
    if config.data_dir is not None:
        if data_format is None:
            data_format = config.data_format
        fn = '{}.{}'.format(fn, config.data_format_extensions[data_format])

        class MQCJSONEncoder(json.JSONEncoder):

            def default(self, obj):
                if callable(obj):
                    try:
                        return obj(1)
                    except:
                        return

                return json.JSONEncoder.default(self, obj)

        with io.open((os.path.join(config.data_dir, fn)), 'w', encoding='utf-8') as (f):
            if data_format == 'json':
                jsonstr = json.dumps(data, indent=4, cls=MQCJSONEncoder, ensure_ascii=False)
                print((jsonstr.encode('utf-8', 'ignore').decode('utf-8')), file=f)
            else:
                if data_format == 'yaml':
                    yaml.dump(data, f, default_flow_style=False)
                else:
                    h = ['Sample']
                    for sn in sorted(data.keys()):
                        for k in data[sn].keys():
                            if type(data[sn][k]) is not dict and k not in h:
                                h.append(str(k))

                    if sort_cols:
                        h = sorted(h)
                    rows = [
                     '\t'.join(h)]
                    for sn in sorted(data.keys()):
                        l = [str(sn)] + [str(data[sn].get(k, '')) for k in h[1:]]
                        rows.append('\t'.join(l))

                    body = '\n'.join(rows)
                    print((body.encode('utf-8', 'ignore').decode('utf-8')), file=f)


def view_all_tags(ctx, param, value):
    """ List available tags and associated modules
    Called by eager click option: --view-tags
    """
    if not value or ctx.resilient_parsing:
        return
    avail_tags = dict()
    print('\nMultiQC Available module tag groups:\n')
    for mod_dict in filter(lambda mod: isinstance(mod, dict), config.module_order):
        mod_key, mod_val = list(mod_dict.items())[0]
        tags = list(mod_val.get('module_tag', []))
        for t in tags:
            if t not in avail_tags:
                avail_tags[t] = []
            avail_tags[t].append(mod_key)

    for t in sorted((avail_tags.keys()), key=(lambda s: s.lower())):
        print(' - {}:'.format(t))
        for ttgs in avail_tags[t]:
            print('   - {}'.format(ttgs))

    ctx.exit()