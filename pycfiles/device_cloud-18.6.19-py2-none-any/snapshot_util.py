# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: ./snapshot_util.py
# Compiled at: 2017-11-02 11:31:49
"""
Description:
This script is designed to trigger a software rollback.  The process
is as follows:
  * take system snapshot
  * install software
  * set flag to trigger rollback
  * start watch dog process
  * restart the agent

How it works:
If the agent fails to restart within the default time frame (3 min.),
the watch dog will return an error and the system will reboot.  The
initramfs has special scripts installed to detect the rollback flag
and do the actual rollback.  Once the rollback is complete, the system
boots into the state at the time of the snapshot.

Requirements:
This script was primarily designed for Wind River Linux IDP, which has
the required dependencies to support rollback.  The filesystem must
provide the following:
  * lvm partition with Wind River Linux IDP OS
  * lvm tools
  * initramfs with special rollback scripts
  * this snapshot utility
  * sudoers access without password, if not running as root

Typical Usage:
This script is meant to be called during the software update phases.
There are four phases:
  * pre_install
  * install
  * post_install
  * err_install
Snapshots are typically taken during the pre_install phase.  When to
perform a rollback is user defined, but the following scenarios are
recommended:

Scenario 1: post_install
A software update might succeed, but fail to connect to the cloud if a
bad software package was used.  In order not to brick the device, test
the connectivity in the post_install phase.  In short, this means
setting the trigger flag and starting the watch dog, then restarting
the agent.  If the agent fails to clear the flags (e.g.  the agent
failed to connect to the cloud), the watch dog will reboot and cause a
rollback.  Add the following to the post_install script:
  * snapshot_util.py -t
  * snapshot_util.py -w
  * systemctl restart device-manager
Note: this test expects the system to have a functional network.  If
reboot on completion was set in the update.json file, a sleep will be
required in this phase to allow the watch dog to time out (3 min).
Recommend a 4 minute sleep.

Scenario 2: err_install
Rollback on ANY software update failure.  If this behaviour is
desired, do the following in the err_install phase:
  * snapshot_util.py -t
  * reboot
The initramfs will see the flags and start the rollback.
Note: any logs or other meta data should be uploaded or stored off
device before rebooting.

Note:
It is possible to clear the trigger flags with this utiltity for
testing purposes:
  * snapshot_util.py -c

"""
import os, subprocess, sys, getopt
IOT_ROOT = '/var/lib/python-device-cloud'
IOT_ROLLBACK_FLAG = IOT_ROOT + '/ota_rollback_enabled'
IOT_TRIGGER_TIMER_FLAG = IOT_ROOT + '/ota_timer_triggered'
IOT_BOOTONCE_FLAG = IOT_ROOT + '/ota_bootonce'
IOT_ROLLBACK_MARKER = IOT_ROOT + '/rollback_inprogress'
REBOOT_DELAY_IN_SECONDS = 60
SUCCESS = 0
ERROR = 1
TIME_DELAY = 1

def exec_cmd(cmd):
    """Execute the shell cmd return status, stdout, stderr"""
    print "Executing command '%s'" % cmd
    output, err = ('', '')
    retcode = 0
    try:
        proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output, err = proc.communicate()
        retcode = proc.returncode
    except OSError:
        print 'Failed to execute the command: %s %s' % (output, err)
        print 'Command error:\n' + err
        return 1

    if retcode == 0:
        print 'Command executed successfully: %s%s' % (output, err)
    else:
        print 'Failed to execute the command: %s %s' % (output, err)
        print 'Command error:\n' + err
    return (
     retcode, output, err)


def take_snapshot():
    """ Take a snapshot of the running system and save it in the snapshot volume """
    cmd = 'df / | tail -1'
    ret, rootdev, err = exec_cmd(cmd)
    rootdev = rootdev.split(' ')
    rootdev = rootdev[0]
    if not ret:
        cmd = 'sudo /usr/sbin/lvdisplay ' + rootdev + ' -c 2> /dev/null'
        ret, lv_info, err = exec_cmd(cmd)
    if not ret and not lv_info.strip():
        print 'ERROR: %s not a LVM volume' % rootdev
        return ERROR
    else:
        if not ret:
            lv_info_part = lv_info.split(':')
            vg_lv_part = lv_info_part[0].split('/')
            vg_name = vg_lv_part[2]
            lv_name = vg_lv_part[3]
            cmd = 'sudo /usr/sbin/lvs ' + rootdev + ' -o LV_SIZE --noheadings --units G'
            ret, lv_size, err = exec_cmd(cmd)
        if not ret:
            snapshot_vl = '/dev/' + vg_name + '/' + lv_name + '_snapshot'
            cmd = 'sudo /usr/sbin/lvchange --refresh ' + rootdev + ' --noudevsync --monitor n'
            ret2, out, err = exec_cmd(cmd)
            cmd = 'sudo /usr/sbin/lvscan | grep ' + snapshot_vl
            ret2, out, err = exec_cmd(cmd)
            if not ret2 and out.strip():
                cmd = 'sudo /usr/sbin/lvchange --refresh ' + rootdev + '_snapshot --noudevsync --monitor n'
                ret2, out, err = exec_cmd(cmd)
                print 'INFO: Removing previous %s' % snapshot_vl
                cmd = 'sudo /usr/sbin/lvremove --noudevsync -f ' + snapshot_vl + ' &> /dev/null'
                ret2, out, err = exec_cmd(cmd)
            lv_size = lv_size.rstrip()
            print 'INFO: Creating new ' + snapshot_vl + ' with volume size ' + lv_size
            cmd = 'sudo /usr/sbin/lvcreate --noudevsync -s -n ' + snapshot_vl + ' -L ' + lv_size + ' ' + rootdev
            ret, out, err = exec_cmd(cmd)
        cmd = 'sudo /usr/sbin/lvdisplay'
        ret_junk, out, err = exec_cmd(cmd)
        if not ret:
            return SUCCESS
        return ERROR


def check_rollback_support():
    """ Set lvm support flag """
    cmd = "sudo /usr/sbin/lvscan | grep ACTIVE | awk '{print $1}' 2> /dev/null"
    ret, lv_info, err = exec_cmd(cmd)
    if not ret and lv_info:
        lvm_support = True
    else:
        print 'WARN: there is no LVM volume found'
        lvm_support = False
    return lvm_support


def set_trigger_flag():
    """ Write a trigger flag for the watchdog """
    cmd = 'date +%s > ' + IOT_TRIGGER_TIMER_FLAG
    ret, out, err = exec_cmd(cmd)
    if ret:
        print 'ERROR:failed to write trigger flag %s\n' % err
        return ERROR
    return SUCCESS


def set_rollback_enabled_flag():
    """ Write a rollback trigger flag for initramfs """
    print 'INFO: setting rollback enabled flag ...\n'
    cmd = 'touch %s' % IOT_ROLLBACK_FLAG
    ret, out, err = exec_cmd(cmd)
    if ret:
        print 'ERROR: %s failed \n' % cmd
        print 'ERROR: %s \n' % err
        return ERROR
    return SUCCESS


def start_watchdog():
    """ Start the watch dog """
    print 'INFO: iot-watchdog is to start to monitor agent ...\n'
    exec_cmd('sudo pkill -9 watchdog >& /dev/null')
    cmd = 'sudo /usr/sbin/watchdog -f -c /etc/python-device-cloud/iot-watchdog.conf'
    ret, out, err = exec_cmd(cmd)
    if ret:
        print 'ERROR: %s failed \n' % cmd
        print 'ERROR: %s \n' % err
        return ERROR
    return SUCCESS


def usage():
    """ Usage """
    print 'Usage:\n\t-s\tTake Snapshot (LVM)\n\t-t\tSet watchdog trigger file\n\t-w\tStart watchdog\n\t-c\tClear trigger files\n\t-h\tThis output\n'
    print '\nNote: Each flag must be set sequentially.  For detailed usage notes, run\n\t $ pydoc snapshot_util'
    sys.exit(ERROR)


if __name__ == '__main__':
    watchdog = False
    snapshot = False
    trigger = False
    rollback = False
    opt = ''
    clear = False
    print 'INFO: Starting snapshot...'
    optlist, args = getopt.getopt(sys.argv[1:], 'wstch')
    for opt, arg in optlist:
        if opt == '-w':
            print 'Watchdog enabled...'
            watchdog = True
        elif opt == '-s':
            print 'Preparing to take snapshot...'
            snapshot = True
        elif opt == '-t':
            print 'Setting watch dog trigger flag ...'
            trigger = True
        elif opt == '-r':
            print 'Setting rollback enabled trigger flag ...'
            rollback = True
        elif opt == '-c':
            print 'Clearing trigger flags ...'
            clear = True
        elif opt == '-h':
            usage()
        else:
            print 'Error, unrecognised parameter'
            usage()

    if opt == '':
        usage()
    if check_rollback_support() == False:
        print 'Error: LVM is not supported.'
        sys.exit(ERROR)
    if snapshot == True:
        print 'taking snapshot'
        if take_snapshot() != SUCCESS:
            print 'ERROR: snapshot failed.  This error is not recoverable.\nUnable to rollback.'
            sys.exit(ERROR)
        else:
            exec_cmd('touch ' + IOT_ROLLBACK_MARKER)
    if trigger == True:
        print 'created trigger flag'
        if set_trigger_flag() != SUCCESS:
            print 'ERROR: set trigger flag failed.  This error is not recoverable.\nUnable to rollback.'
            sys.exit(ERROR)
    if rollback == True:
        if set_rollback_enabled_flag() != SUCCESS:
            print 'ERROR: set rollback enabled flag failed.  This error is not recoverable.\nUnable to rollback.'
            exec_cmd('rm -f ' + IOT_TRIGGER_TIMER_FLAG)
            sys.exit(ERROR)
    if watchdog == True:
        print 'starting watchdog'
        if start_watchdog() != SUCCESS:
            print 'ERROR: Unable to start watchdog.  This error is not recoverable.\nUnable to rollback.'
            sys.exit(ERROR)
    if clear == True:
        files = [
         IOT_ROLLBACK_FLAG, IOT_TRIGGER_TIMER_FLAG]
        for f in files:
            if os.path.isfile(f):
                try:
                    os.remove(f)
                except (OSError, IOError) as err:
                    error = str(err)
                    print error + 'Unable to remove file'

    sys.exit(SUCCESS)