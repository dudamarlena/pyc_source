# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.8-intel/egg/ccp_sde_parser/split_tables.py
# Compiled at: 2012-11-04 23:12:21
"""Splits the monolithic dump JSON file into a file per table."""
import StringIO, gc, os
from progressbar import ProgressBar, Bar, ETA, Percentage, Widget
import sys, json

class TableNameWidget(Widget):

    def __init__(self):
        self.current_table = 'None'

    def update(self, pbar):
        return 'Table: %s' % self.current_table


def main():
    if len(sys.argv) < 3:
        print 'Must specify both a JSON dump file and a directory.'
        print 'Usage: %s MONOLITHIC_JSON OUTPUT_DIRECTORY\n' % sys.argv[0]
        sys.exit(1)
    target_dir = sys.argv[2]
    json_file = sys.argv[1]
    if not os.path.isfile(json_file) or not os.access(json_file, os.R_OK):
        print 'File %s does not exist or is not readable.' % json_file
        print 'Usage: %s MONOLITHIC_JSON OUTPUT_DIRECTORY\n' % sys.argv[0]
        sys.exit(1)
    if not os.path.isdir(target_dir):
        print 'Directory %s does not exist, creating.' % target_dir
        os.mkdir(target_dir)
    with open(json_file) as (yf):
        current_table = None
        line_num = 0
        table_name = None
        tname = TableNameWidget()
        inp = yf.read().splitlines()
        pbar = ProgressBar(widgets=[tname, Bar(), ' ', Percentage(), ' ', ETA()], maxval=len(inp)).start()
        for line in inp:
            line_num += 1
            if line == '---':
                current_table = StringIO.StringIO()
                continue
            elif line == '...':
                table = json.loads(current_table.getvalue())
                table_name = table['table_name']
                tname.current_table = table_name
                with open(os.path.join(target_dir, '%s.json' % table_name), 'w') as (tf):
                    tf.write(current_table.getvalue())
                current_table.close()
                del table
                table_name = None
                gc.collect()
                pbar.update(line_num)
                continue
            else:
                current_table.write(line)

        pbar.finish()
    return


if __name__ == '__main__':
    main()