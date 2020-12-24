# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/fabrizio/Dropbox/free_range_factory/boot/boot_pkg/directory.py
# Compiled at: 2012-08-24 12:52:05
import glob, os, shutil, platform
before = []

def src_dir_modified(wd):
    """ src_dir_modified(wd)
        Check whether any VHDL file in folder "wd" has been modified.
    """
    global before
    now = []
    all_vhdl_files = glob.glob(os.path.join(wd, '*.vhd')) + glob.glob(os.path.join(wd, '*.vhdl'))
    for infile in all_vhdl_files:
        now.append([infile, os.stat(infile).st_mtime])

    if now == before:
        return False
    else:
        before = now
        print 'Source code has been modified.'
        return True


def dir_make_sure(wd, command):
    """ dir_make_sure(wd, command)
        Check that all directories and files inside "wd" are good.
        If the "build" directory exists, delete its content,
        if "build" directory does not exist, create it.
        Create  gtkwave conf. file and save in inside folder "build"
    """
    if os.path.isdir(wd):
        print 'Directory structure seems good.'
        if os.path.isdir(os.path.join(wd, 'build')) == False:
            try:
                os.path.os.mkdir(os.path.join(wd, 'build'))
                print '"build" directory created.'
            except:
                print 'Hum... you might not have writing permissions                        for the folder you are in... Exiting.'
                return False

        else:
            if command == 'clean_all_files':
                for root, dirs, files in os.walk(os.path.join(wd, 'build')):
                    for f in files:
                        os.unlink(os.path.join(root, f))

                    for d in dirs:
                        shutil.rmtree(os.path.join(root, d))

                print 'All files and folders inside "build" were deleted.'
            print 'Creating gtkwave configuration file inside "build" folder'
            gtkwave_cnf_cont = '# gtkwave custom configuration file\n' + '#\n# eliminate some keys\n#\n' + 'accel "/File/Read Sim Logfile" (null)\n' + 'accel "/File/Open New Window" (null)\n' + 'accel "/Edit/Toggle Trace Hier" (null)\n' + 'accel "/Edit/Toggle Group Open|Close" (null)\n' + 'accel "/Edit/Create Group" (null)\n' + 'accel "/Markers/Locking/Lock to Lesser Named Marker" (null)\n' + 'accel "/Markers/Locking/Lock to Greater Named Marker" (null)\n' + 'accel "/Markers/Locking/Unlock from Named Marker" (null)\n' + 'accel "/Markers/Copy Primary->B Marker" (null)\n' + 'accel "/File/Read Save File" (null)\n' + 'accel "/Edit/Cut" (null)\n' + 'accel "/File/Close" (null)\n' + 'accel "/Edit/Paste" (null)\n' + 'accel "/Edit/Copy" (null)\n' + 'accel "/File/Open New Tab" (null)\n'
            gtkwave_cnf_fl = os.path.join(wd, 'build', 'gtkwaverc')
            open(gtkwave_cnf_fl, 'w').write(gtkwave_cnf_cont)
            all_vhdl_files = glob.glob(os.path.join(wd, '*.vhd')) + glob.glob(os.path.join(wd, '*.vhdl'))
            if len(all_vhdl_files) == 0:
                print 'You do not seem to have any VHDL file.'
                return False
        return True
    else:
        print 'The selected top-level design file does not exist or is not a file.'
        return False


def guess_xilinx_ise_path():
    """ Try to guess the Xilinx xtclsh synthesis tool path by checking
        Xilinx ISE environment variables and generate a "source" command with
    """
    _txt = ''
    answer = ''
    command = ''
    if platform.architecture()[0] is '32bit':
        command = '/settings32.sh'
    elif platform.architecture()[0] is '64bit':
        command = '/settings64.sh'
    if os.environ.get('XILINX'):
        answer = os.environ.get('XILINX')
        _txt = 'source ' + answer + command
        print 'Xilinx ISE software tool detected at:', answer
    if not _txt:
        if os.path.isdir('/opt/Xilinx'):
            answer = '/opt/Xilinx/12.2/ISE_DS'
            _txt = 'source ' + answer + command
    if not _txt:
        _txt = 'Xilinx ISE not detected'
    return _txt