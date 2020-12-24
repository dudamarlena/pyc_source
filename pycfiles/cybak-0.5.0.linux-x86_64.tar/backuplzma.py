# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/cybackup/backuplzma.py
# Compiled at: 2015-07-15 11:30:23
import sys, os
from os import path
import re, tarfile, logging, time, random
from dirwalker import file_lister
import config_handler, pash, termcolor, menu_generator
config_path = '/etc/cybak.cfg'
config = config_handler.Parser(filename=config_path)
if config.config_exists(config_path) != True:
    print 'No configuration file found. Using defaults.'

def build_exceptions(except_option):
    try:
        except_list = config.get_setting('EXCEPT', except_option).split(',')
        if except_list[(-1)] == ['']:
            except_list.pop()
    except AttributeError:
        except_list = []

    return except_list


dir_exceptions = build_exceptions('DIR_EXCEPT')
file_exceptions = build_exceptions('FILE_EXCEPT')
dest_dir = '/backup/'
if config.get_setting('DIR', 'DEST_DIR') != None:
    dest_dir = config.get_setting('DIR', 'DEST_DIR')
source_dir = os.environ['HOME']
if config.get_setting('DIR', 'SRC_DIR') != None:
    source_dir = config.get_setting('DIR', 'SRC_DIR')
file_handle = 'MyBackup'
if config.get_setting('NAME', 'FILENAME') != None:
    file_handle = config.get_setting('NAME', 'FILENAME')
timestamp = time.strftime('%Y%m%d.%H%M')
file_name = file_handle + '-' + timestamp + '.' + str(random.randint(100, 999))
print os.path.exists(dest_dir) or "Creating '", dest_dir, "' as a destination for backups."
os.makedirs(dest_dir)
if not os.path.exists(dest_dir):
    raise AssertionError("We tried to make a directory, but couldn't find it afterwards.")
else:
    print 'Found destination directory:', dest_dir
print ''
ignore_hidden = False
ignore_hidden_str = config.get_setting('EXCEPT', 'IGNORE_HIDDEN')
if ignore_hidden_str == 'True' or ignore_hidden_str == 'true':
    print 'Ignoring hidden files and folders...'
    ignore_hidden = True
print 'Files that will be ignored:'
for exc in file_exceptions:
    print '    ', exc

print 'Directories that will be ignored:'
for exc in dir_exceptions:
    print '    ', exc

print ''
total_list = file_lister(source_dir, ignore_hidden=True, file_exceptions=file_exceptions, dir_exceptions=dir_exceptions)
print 'Building file list and packing tarball...'
tar = tarfile.open(name=dest_dir + file_name + '.tar', mode='w')
for i in total_list:
    tar.add(name=i, recursive=True)

tar.close()
handle = dest_dir + file_name + '.tar'
proc = pash.ShellProc()
proc.run('du -sh ' + handle + " | column -t|cut -d ' ' -f 1")
size = proc.get_val('stdout').rstrip('\n')
print 'The total size of the files in the built tarball is: ',
termcolor.cprint(size, 'cyan')
print 'The compressed backup will likely be smaller than this.\n'
if len(sys.argv) > 1:
    if sys.argv[1] == 'auto':
        result = True
else:
    yn = menu_generator.YN_Menu(default='no')
    result = yn.run()
if result == False:
    print 'Operation cancelled, deleting tarball.'
    os.remove(handle)
    sys.exit(1)
print '\nApplying lzma compression... (this may take several minutes)'
command = 'lrzip ' + handle
proc.run(command)
data = proc.get_val('stdout').rstrip('\n').split('\n')
print 'Compression complete.'
print 'Ensuring the backup file exists...',
while os.path.exists(handle + '.lrz') == False:
    pass

print 'found it!\n'
print data[0]
command = 'du -sh ' + data[0].split(':')[1].lstrip(' ') + "| column -t | cut -d ' ' -f 1"
proc.run(command)
sys.stdout.write('Compressed backup size: ')
termcolor.cprint(proc.get_val('stdout'), 'cyan')
for index, i in enumerate(data[1].split(' ')):
    if i == 'Compression' and data[1].split(' ')[(index + 1)] == 'Ratio:':
        comp_ratio = data[1].split(' ')[(index + 2)].rstrip('.\n')

sys.stdout.write('Compression ratio: ')
termcolor.cprint(comp_ratio, 'cyan')
print '\nDeleting the uncompressed tarball.'
os.remove(handle)
print 'Backup complete. Have a nice day.'