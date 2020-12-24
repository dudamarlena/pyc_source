# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/fabrizio/Dropbox/free_range_factory/boot/boot_pkg/boot.py
# Compiled at: 2012-08-25 08:06:12
__doc__ = '\nFILE: boot.py\n\napplication to compile, simulate and synthesize your VHDL code.\nhow to run: ./boot\n\nCopyright (C) 2012 Fabrizio Tappero\n\nSite:     http://www.freerangefactory.org\nAuthor:   Fabrizio Tappero, fabrizio.tappero<at>gmail.com\nLicense:  GNU General Public License\n'
__author__ = 'Fabrizio Tappero'

def gui_up():
    import gtk
    gtk.main()
    return 0


def boot():
    from multiprocessing import Process, Pipe
    import gui, boot_process
    comm_i, comm_o = Pipe()
    compute_prc = Process(target=boot_process.comp_and_sim, args=(comm_o,))
    compute_prc.start()
    my_gui = gui.mk_gui()
    my_gui.add_conn(compute_prc, comm_i)
    gui_up()
    compute_prc.terminate()
    compute_prc.join()
    return 0


def main():
    import sys, argparse, quick_start, build
    _parser = argparse.ArgumentParser(description='Program to compile, simulate and synthesize ' + 'your VHDL code.', epilog='Program made by: freerangefactory.org')
    _parser.add_argument('-b', '--build', required=False, dest='build', action='store_const', const=True, default=False, help='Download and install necessary packages ' + '(Internet connection required).')
    _parser.add_argument('-qs', '--quick_start', required=False, dest='quick_start', action='store_const', const=True, default=False, help='Build a simple VHDL project.')
    _parser.add_argument('-l', '--log', required=False, dest='log', action='store_const', const=True, default=False, help='Start boot and log output into a local file.')
    _parser.add_argument('-v', '--version', required=False, dest='ver', action='store_const', const=True, default=False, help='Print the boot version number and exit.')
    args = _parser.parse_args()
    try:
        if args.build:
            build.build_all()
        elif args.quick_start:
            quick_start.make_vhdl_counter_project('src')
        elif args.log:
            sys.stdout = open('boot.log', 'w')
            boot()
        elif args.ver:
            import version
            print 'boot', version.boot_version
        else:
            boot()
    except KeyboardInterrupt:
        print 'bye bye.'

    return 0


if __name__ == '__main__':
    main()