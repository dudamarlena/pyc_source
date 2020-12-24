# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/oebakery/cmd_config.py
# Compiled at: 2009-11-02 08:05:00


def do_config(argv):
    parser = OptionParser('Usage: oe config [FILE] [options]\n\n  Configure OpenEmbedded development environment. Choose a local.conf from\n  the conf/local.conf.d directory.  If FILE is given, use that. If FILE is\n  not given, present user with a menu of available configuration files.')
    (options, args) = parser.parse_args(argv)
    if len(args) > 1:
        parser.print_help()
        return
    topdir = cd_topdir()
    if len(args) == 0:
        return do_config_menu()
    if len(args) == 1:
        return do_config_file(argv[0])


def do_config_menu():
    if not os.path.isdir('conf/local.conf.d'):
        print >> sys.stderr, 'ERROR: conf/local.conf.d directory not found'
        return
    print 'Choose configuration file (local.conf will be a symlink to it)\n'
    files = []
    for file in dircache.listdir('conf/local.conf.d'):
        if file[-1:] == '~':
            continue
        files.append(file)
        print ' %s: %s' % (('%s' % len(files)).rjust(3), file)

    answer = raw_input('\nEnter configuration name or number: ')
    try:
        number = int(answer)
        if number > len(files) or number <= 0:
            print >> sys.stderr, 'ERROR: invalid number'
            return
        file = files[(number - 1)]
    except:
        if answer not in files:
            print >> sys.stderr, 'ERROR: bad configuration name'
            return
        file = answer

    return do_config_file(file)


def do_config_file(filename):
    if not os.path.exists('conf/local.conf.d/%s' % filename):
        print >> sys.stderr, 'ERROR: %s configuration file not found' % filename
        return
    if os.path.exists('conf/local.conf') and not os.path.islink('conf/local.conf'):
        print >> sys.stderr, 'ERROR: conf/local.conf is not a symlink, refusing to remove it'
        return
    if os.path.islink('conf/local.conf'):
        os.remove('conf/local.conf')
    os.symlink('local.conf.d/%s' % filename, 'conf/local.conf')