# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/futuregrid/image/management/IMGenerateScript.py
# Compiled at: 2012-09-06 11:03:15
"""
It generates the images for different OS
"""
__author__ = 'Javier Diaz, Andrew Younge'
from optparse import OptionParser
from types import *
import re, logging, logging.handlers, glob, random, os, sys, socket
from subprocess import *
import time, re
from xml.dom.minidom import Document, parse
logger = None

def main():
    global baseimageuri
    global http_server
    global namedir
    global onlybaseimage
    global size
    global tempdir
    random.seed()
    randid = str(random.getrandbits(32))
    base_os = ''
    spacer = '-'
    latest_ubuntu = 'lucid'
    latest_debian = 'lenny'
    latest_rhel = '5.5'
    latest_centos = '5.6'
    latest_fedora = '13'
    parser = OptionParser()
    parser.add_option('-o', '--os', dest='os', help='specify destination Operating System')
    parser.add_option('-v', '--version', dest='version', help='Operating System version')
    parser.add_option('-a', '--arch', dest='arch', help='Destination hardware architecture')
    parser.add_option('-s', '--software', dest='software', help='Software stack to be automatically installed')
    parser.add_option('-d', '--debug', action='store_true', dest='debug', help='Enable debugging')
    parser.add_option('-u', '--user', dest='user', help='FutureGrid username')
    parser.add_option('-n', '--name', dest='givenname', help='Desired recognizable name of the image')
    parser.add_option('-e', '--description', dest='desc', help='Short description of the image and its purpose')
    parser.add_option('-t', '--tempdir', dest='tempdir', help='directory to be use in to generate the image')
    parser.add_option('-c', '--httpserver', dest='httpserver', help='httpserver to download config files')
    parser.add_option('-i', '--baseimageuri', dest='baseimageuri', help='Base Image URI. This is used to generate the user image')
    parser.add_option('-b', '--baseimage', action='store_true', default=False, dest='baseimage', help='Generate Base Image')
    parser.add_option('-l', '--logfile', default='fg-image-generate.log', dest='logfile', help='Generate Base Image')
    parser.add_option('-z', '--size', default=1.5, dest='size', help='Size of the Image. The default one is 1.5GB.')
    (ops, args) = parser.parse_args()
    log_filename = ops.logfile
    logger = logging.getLogger('GenerateScript')
    logger.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler = logging.FileHandler(log_filename)
    handler.setLevel(logging.DEBUG)
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.propagate = False
    logger.info('Starting image generator...')
    if os.getuid() != 0:
        logger.error('Sorry, you need to run with root privileges')
        sys.exit(1)
    size = float(ops.size)
    size = int(size * 1024)
    baseimageuri = ops.baseimageuri
    onlybaseimage = ops.baseimage
    if type(ops.httpserver) is not NoneType:
        http_server = ops.httpserver
    else:
        logger.error('You need to provide the http server that contains files needed to create images')
        sys.exit(1)
    if type(ops.tempdir) is not NoneType:
        tempdir = ops.tempdir
        if tempdir[len(tempdir) - 1:] != '/':
            tempdir += '/'
    else:
        tempdir = '/tmp/'
    if type(ops.user) is not NoneType:
        user = ops.user
    else:
        user = 'default'
    logger.debug('FG User: ' + user)
    namedir = user + '' + randid
    arch = ops.arch
    logger.debug('Selected Architecture: ' + arch)
    if ops.software != 'None':
        packages = re.split('[, ]', ops.software)
        packs = (' ').join(packages)
        logger.debug('Selected software packages: ' + packs)
    else:
        packs = 'wget'
    if baseimageuri == None:
        create_base_os = True
    else:
        create_base_os = False
    version = ops.version
    if ops.os == 'ubuntu':
        base_os = base_os + 'ubuntu' + spacer
        logger.info('Building Ubuntu ' + version + ' image')
        img = buildUbuntu(namedir, version, arch, packs, tempdir, create_base_os)
    elif ops.os == 'debian':
        base_os = base_os + 'debian' + spacer
    elif ops.os == 'rhel':
        base_os = base_os + 'rhel' + spacer
    elif ops.os == 'centos':
        base_os = base_os + 'centos' + spacer
        logger.info('Building Centos ' + version + ' image')
        img = buildCentos(namedir, version, arch, packs, tempdir, create_base_os)
    elif ops.os == 'fedora':
        base_os = base_os + 'fedora' + spacer
    if type(ops.givenname) is NoneType:
        ops.givenname = img
    if type(ops.desc) is NoneType:
        ops.desc = ' '
    manifest(user, img, ops.os, version, arch, packs, ops.givenname, ops.desc, tempdir)
    print img
    return


def handleBaseImage(tempdir, name):
    if size > int(1536.0):
        runCmd('mkdir ' + tempdir + '' + name + '_old')
        runCmd('/bin/mount -o loop ' + baseimageuri + ' ' + tempdir + '' + name + '_old')
        runCmd('dd if=/dev/zero of=' + tempdir + '' + name + '.img bs=1024k seek=' + str(size) + ' count=0')
        runCmd('/sbin/mke2fs -F -j ' + tempdir + '' + name + '.img')
        runCmd('mount -o loop ' + tempdir + '' + name + '.img ' + tempdir + '' + name)
        os.system('mv -f ' + tempdir + '' + name + '_old/* ' + tempdir + '' + name + '/')
        runCmd('/bin/umount ' + tempdir + '' + name + '_old')
        if os.path.dirname(baseimageuri).rstrip('/') != tempdir.rstrip('/'):
            runCmd('rm -rf ' + os.path.dirname(baseimageuri) + ' ' + tempdir + '' + name + '_old')
    else:
        runCmd('mv ' + baseimageuri + ' ' + tempdir + '' + name + '.img')
        if os.path.dirname(baseimageuri).rstrip('/') != tempdir.rstrip('/'):
            runCmd('rm -rf ' + os.path.dirname(baseimageuri))
        runCmd('/bin/mount -o loop ' + tempdir + '' + name + '.img ' + tempdir + '' + name)


def createBaseImageDisk(tempdir, name):
    runCmd('dd if=/dev/zero of=' + tempdir + '' + name + '.img bs=1024k seek=' + str(size) + ' count=0')
    runCmd('/sbin/mke2fs -F -j ' + tempdir + '' + name + '.img')
    runCmd('/bin/mount -o loop ' + tempdir + '' + name + '.img ' + tempdir + '' + name)


def buildUbuntu(name, version, arch, pkgs, tempdir, base_os):
    output = ''
    namedir = name
    ubuntuLog = logging.getLogger('GenerateScript.ubuntu')
    runCmd('mkdir ' + tempdir + '' + name)
    if not base_os:
        ubuntuLog.info('Retrieving Image: ubuntu-' + version + '-' + arch + '-base.img')
        handleBaseImage(tempdir, name)
    elif base_os:
        ubuntuLog.info('Generation Image: centos-' + version + '-' + arch + '-base.img')
        ubuntuLog.info('Creating Disk for the image')
        createBaseImageDisk(tempdir, name)
    if base_os:
        ubuntuLog.info('Installing base OS')
        start = time.time()
        runCmd('debootstrap --include=grub,language-pack-en,openssh-server --components=main,universe,multiverse ' + version + ' ' + tempdir + '' + name)
        end = time.time()
        ubuntuLog.info('TIME base OS:' + str(end - start))
        ubuntuLog.info('Copying configuration files')
        os.system('echo "nameserver 129.79.1.1" >> ' + tempdir + '' + name + '/etc/resolv.conf')
        os.system('echo "nameserver 172.29.202.149" >> ' + tempdir + '' + name + '/etc/resolv.conf')
        os.system('echo "127.0.0.1 localhost.localdomain localhost" > ' + tempdir + '' + name + '/etc/hosts')
        ubuntuLog.info('Configuring repositories')
        f = open(tempdir + '' + name + '/etc/apt/sources.list', 'w')
        f.write('deb http://ftp.ussg.indiana.edu/linux/ubuntu/ ' + version + ' main restricted \ndeb-src http://ftp.ussg.indiana.edu/linux/ubuntu/ ' + version + ' main restricted \ndeb http://ftp.ussg.indiana.edu/linux/ubuntu/ ' + version + '-updates main restricted \ndeb-src http://ftp.ussg.indiana.edu/linux/ubuntu/ ' + version + '-updates main restricted \ndeb http://ftp.ussg.indiana.edu/linux/ubuntu/ ' + version + ' universe \ndeb-src http://ftp.ussg.indiana.edu/linux/ubuntu/ ' + version + ' universe \ndeb http://ftp.ussg.indiana.edu/linux/ubuntu/ ' + version + '-updates universe \ndeb-src http://ftp.ussg.indiana.edu/linux/ubuntu/ ' + version + '-updates universe \ndeb http://ftp.ussg.indiana.edu/linux/ubuntu/ ' + version + ' multiverse \ndeb-src http://ftp.ussg.indiana.edu/linux/ubuntu/ ' + version + ' multiverse \ndeb http://ftp.ussg.indiana.edu/linux/ubuntu/ ' + version + '-updates multiverse \ndeb-src http://ftp.ussg.indiana.edu/linux/ubuntu/ ' + version + '-updates multiverse \n')
        f.close()
        os.system('mkdir -p ' + tempdir + '' + name + '/root/.ssh')
        runCmd('mount --bind /proc ' + tempdir + '' + name + '/proc')
        runCmd('mount --bind /dev ' + tempdir + '' + name + '/dev')
        ubuntuLog.info('Mounted proc and dev')
        runCmd('/usr/sbin/chroot ' + tempdir + '' + name + ' apt-key adv --keyserver keyserver.ubuntu.com --recv-keys 98932BEC')
        runCmd('/usr/sbin/chroot ' + tempdir + '' + name + ' apt-get update')
        os.system('mkdir -p /usr/sbin')
        os.system('echo "#!/bin/sh" >' + tempdir + '' + name + '/usr/sbin/policy-rc.d')
        os.system('echo "exit 101" >>' + tempdir + '' + name + '/usr/sbin/policy-rc.d')
        os.system('chmod +x ' + tempdir + '' + name + '/usr/sbin/policy-rc.d')
        start = time.time()
        ubuntuLog.info('Installing some util packages')
        runCmd('/usr/sbin/chroot ' + tempdir + '' + name + ' /usr/bin/env PATH=/usr/local/sbin:/usr/sbin:/sbin:/bin:/usr/bin apt-get -y install wget nfs-common gcc make man curl time')
        cmd = '/usr/sbin/chroot ' + tempdir + '' + name + ' /usr/bin/env PATH=/usr/local/sbin:/usr/sbin:/sbin:/bin:/usr/bin apt-get -y install libcrypto++8'
        p = Popen(cmd.split(), stdout=PIPE, stderr=PIPE)
        std = p.communicate()
        if p.returncode != 0:
            runCmd('/usr/sbin/chroot ' + tempdir + '' + name + ' /usr/bin/env PATH=/usr/local/sbin:/usr/sbin:/sbin:/bin:/usr/bin apt-get -y install libcrypto++9')
        else:
            ubuntuLog.debug(cmd)
        end = time.time()
        ubuntuLog.info('TIME util packages:' + str(end - start))
        os.system('echo "localhost" > ' + tempdir + '' + name + '/etc/hostname')
        runCmd('hostname localhost')
        runCmd('wget ' + http_server + '/conf/ubuntu/interfaces -O ' + tempdir + '' + name + '/etc/network/interfaces')
        ubuntuLog.info('Injected networking configuration')
    if not onlybaseimage:
        if not base_os:
            runCmd('/usr/sbin/chroot ' + tempdir + '' + name + ' rm -f /etc/mtab~*  /etc/mtab.tmp')
            runCmd('mount --bind /proc ' + tempdir + '' + name + '/proc')
            runCmd('mount --bind /dev ' + tempdir + '' + name + '/dev')
            ubuntuLog.info('Mounted proc and dev')
            os.system('mkdir -p /usr/sbin')
            os.system('echo "#!/bin/sh" >' + tempdir + '' + name + '/usr/sbin/policy-rc.d')
            os.system('echo "exit 101" >>' + tempdir + '' + name + '/usr/sbin/policy-rc.d')
            os.system('chmod +x ' + tempdir + '' + name + '/usr/sbin/policy-rc.d')
        start = time.time()
        if pkgs != None:
            ubuntuLog.info('Installing user-defined packages')
            runCmd('/usr/sbin/chroot ' + tempdir + '' + name + ' mkdir -p /boot/grub/')
            runCmd('/usr/sbin/chroot ' + tempdir + '' + name + ' touch /boot/grub/menu.lst')
            installusers = '/tmp/_installuserpackages'
            f = open(tempdir + '' + name + installusers, 'w')
            f.write('#!/bin/bash\n' + 'export DEBIAN_FRONTEND=noninteractive' + '\n' + 'apt-get ' + '-y install ' + pkgs)
            f.close()
            runCmd('/usr/sbin/chroot ' + tempdir + '' + name + ' chmod +x ' + installusers)
            runCmd('/usr/sbin/chroot ' + tempdir + '' + name + ' /usr/bin/env -i PATH=/usr/local/sbin:/usr/sbin:/sbin:/bin:/usr/bin ' + installusers)
            ubuntuLog.info('Installed user-defined packages')
        end = time.time()
        ubuntuLog.info('TIME user packages:' + str(end - start))
        os.system("sed -i 's/PasswordAuthentication yes/PasswordAuthentication no/g' " + tempdir + '' + name + '/etc/ssh/sshd_config')
        os.system('echo "PasswordAuthentication no" | tee -a ' + tempdir + '' + name + '/etc/ssh/sshd_config > /dev/null')
        os.system("sed -i 's/StrictHostKeyChecking ask/StrictHostKeyChecking no/g' " + tempdir + '' + name + '/etc/ssh/ssh_config')
        os.system('echo "StrictHostKeyChecking no" | tee -a ' + tempdir + '' + name + '/etc/ssh/ssh_config > /dev/null')
    os.system('rm -f ' + tempdir + '' + name + '/usr/sbin/policy-rc.d')
    cleanup(name)
    return name


def buildDebian(name, version, arch, pkgs, tempdir):
    namedir = name
    runCmd('')


def buildRHEL(name, version, arch, pkgs, tempdir):
    namedir = name
    runCmd('')


def buildCentos(name, version, arch, pkgs, tempdir, base_os):
    output = ''
    namedir = name
    centosLog = logging.getLogger('GenerateScript.centos')
    runCmd('mkdir ' + tempdir + '' + name)
    if not base_os:
        centosLog.info('Procesing Image: centos-' + version + '-' + arch + '-base.img')
        handleBaseImage(tempdir, name)
    elif base_os:
        centosLog.info('Generation Image: centos-' + version + '-' + arch + '-base.img')
        centosLog.info('Creating Disk for the image')
        createBaseImageDisk(tempdir, name)
    if base_os:
        centosLog.info('Create directories image')
        runCmd('mkdir -p ' + tempdir + '' + name + '/var/lib/rpm ' + tempdir + '' + name + '/var/log ' + tempdir + '' + name + '/dev/pts ' + tempdir + '' + name + '/dev/shm')
        runCmd('touch ' + tempdir + '' + name + '/var/log/yum.log')
        centosLog.info('Getting appropiate release package')
        if version == '5':
            runCmd('wget ' + http_server + '/conf/centos/centos-release-5.rpm -O /tmp/centos-release.rpm')
        elif version == '6':
            runCmd('wget ' + http_server + '/conf/centos/centos-release-6.rpm -O /tmp/centos-release.rpm')
        runCmd('rpm -ihv --nodeps --root ' + tempdir + '' + name + ' /tmp/centos-release.rpm')
        runCmd('rm -f /tmp/centos-release.rpm')
        centosLog.info('Installing base OS')
        start = time.time()
        runCmd('yum --installroot=' + tempdir + '' + name + ' -y groupinstall Core')
        end = time.time()
        centosLog.info('TIME base OS:' + str(end - start))
        centosLog.info('Copying configuration files')
        os.system('echo "search idpm" > ' + tempdir + '' + name + '/etc/resolv.conf')
        os.system('echo "nameserver 129.79.1.1" >> ' + tempdir + '' + name + '/etc/resolv.conf')
        os.system('echo "nameserver 172.29.202.149" >> ' + tempdir + '' + name + '/etc/resolv.conf')
        runCmd('cp /etc/sysconfig/network ' + tempdir + '' + name + '/etc/sysconfig/')
        os.system('echo "127.0.0.1 localhost.localdomain localhost" > ' + tempdir + '' + name + '/etc/hosts')
        os.system('mkdir -p ' + tempdir + '' + name + '/root/.ssh')
        runCmd('mount --bind /proc ' + tempdir + '' + name + '/proc')
        runCmd('mount --bind /dev ' + tempdir + '' + name + '/dev')
        centosLog.info('Mounted proc and dev')
        centosLog.info('Installing some util packages')
        start = time.time()
        if re.search('^5', version):
            runCmd('/usr/sbin/chroot ' + tempdir + '' + name + ' rpm -ivh ' + http_server + '/conf/centos/epel-release-5-4.noarch.rpm')
            runCmd('wget ' + http_server + '/inca_conf/fgperf.repo_centos5 -O ' + tempdir + '' + name + '/etc/yum.repos.d/fgperf.repo')
        elif re.search('^6', version):
            runCmd('/usr/sbin/chroot ' + tempdir + '' + name + ' rpm -ivh ' + http_server + '/conf/centos/epel-release-6-5.noarch.rpm')
            runCmd('/usr/sbin/chroot ' + tempdir + '' + name + ' yum -y install plymouth openssh-clients')
        runCmd('/usr/sbin/chroot ' + tempdir + '' + name + ' yum -y install wget nfs-utils gcc make man curl time')
        end = time.time()
        centosLog.info('TIME util packages:' + str(end - start))
        runCmd('wget ' + http_server + '/conf/centos/ifcfg-eth0 -O ' + tempdir + '' + name + '/etc/sysconfig/network-scripts/ifcfg-eth0')
        centosLog.info('Injected generic networking configuration')
    if not onlybaseimage:
        if not base_os:
            runCmd('/usr/sbin/chroot ' + tempdir + '' + name + ' rm -f /etc/mtab~*  /etc/mtab.tmp')
            runCmd('mount --bind /proc ' + tempdir + '' + name + '/proc')
            runCmd('mount --bind /dev ' + tempdir + '' + name + '/dev')
            centosLog.info('Mounted proc and dev')
        start = time.time()
        if pkgs != None:
            centosLog.info('Installing user-defined packages')
            runCmd('/usr/sbin/chroot ' + tempdir + '' + name + ' yum -y install ' + pkgs)
            centosLog.info('Installed user-defined packages')
        end = time.time()
        centosLog.info('TIME user packages:' + str(end - start))
        os.system("sed -i 's/PasswordAuthentication yes/PasswordAuthentication no/g' " + tempdir + '' + name + '/etc/ssh/sshd_config')
        os.system('echo "PasswordAuthentication no" | tee -a ' + tempdir + '' + name + '/etc/ssh/sshd_config > /dev/null')
        if os.path.isfile(tempdir + '' + name + '/etc/ssh/ssh_config'):
            os.system("sed -i 's/StrictHostKeyChecking ask/StrictHostKeyChecking no/g' " + tempdir + '' + name + '/etc/ssh/ssh_config')
        os.system('echo "StrictHostKeyChecking no" | tee -a ' + tempdir + '' + name + '/etc/ssh/ssh_config > /dev/null')
        os.system("sed -i 's/enforcing/disabled/g' " + tempdir + '' + name + '/etc/selinux/config')
    cleanup(name)
    return name


def buildFedora(name, version, arch, pkgs, tempdir):
    runCmd('')


def runCmd(cmd):
    cmdLog = logging.getLogger('GenerateScript.exec')
    cmdLog.debug(cmd)
    p = Popen(cmd.split(), stdout=PIPE, stderr=PIPE)
    std = p.communicate()
    if len(std[0]) > 0:
        cmdLog.debug('stdout: ' + std[0])
    if p.returncode != 0:
        cmdLog.error('Command: ' + cmd + ' failed, status: ' + str(p.returncode) + ' --- ' + std[1])
        cleanup(namedir)
        cmd = 'rm -f ' + tempdir + '' + namedir + '.img'
        cmdLog.debug('Executing: ' + cmd)
        os.system(cmd)
        print 'error'
        print str(p.returncode) + '---' + std[1]
        sys.exit(p.returncode)


def cleanup(name):
    cleanupLog = logging.getLogger('GenerateScript.cleanup')
    if name.strip() != '':
        os.system('umount ' + tempdir + '' + name + '/proc')
        os.system('umount ' + tempdir + '' + name + '/dev')
        cmd = 'umount ' + tempdir + '' + name
        cleanupLog.debug('Executing: ' + cmd)
        stat = os.system(cmd)
        if stat == 0:
            cmd = 'rm -rf ' + tempdir + '' + name
            cleanupLog.debug('Executing: ' + cmd)
            os.system(cmd)
    else:
        cleanupLog.error('error in clean up')
    cleanupLog.debug('Cleaned up mount points')
    time.sleep(10)


def manifest(user, name, os, version, arch, pkgs, givenname, description, tempdir):
    manifestLog = logging.getLogger('GenerateScript.manifest')
    manifest = Document()
    head = manifest.createElement('manifest')
    manifest.appendChild(head)
    userNode = manifest.createElement('user')
    userVal = manifest.createTextNode(user)
    userNode.appendChild(userVal)
    head.appendChild(userNode)
    imgNameNode = manifest.createElement('name')
    imgNameVal = manifest.createTextNode(name)
    imgNameNode.appendChild(imgNameVal)
    head.appendChild(imgNameNode)
    imgGivenNameNode = manifest.createElement('givenname')
    imgGivenNameVal = manifest.createTextNode(givenname)
    imgGivenNameNode.appendChild(imgGivenNameVal)
    head.appendChild(imgGivenNameNode)
    descNode = manifest.createElement('description')
    descVal = manifest.createTextNode(description)
    descNode.appendChild(descVal)
    head.appendChild(descNode)
    osNode = manifest.createElement('os')
    osNodeVal = manifest.createTextNode(os)
    osNode.appendChild(osNodeVal)
    head.appendChild(osNode)
    versionNode = manifest.createElement('version')
    versionNodeVal = manifest.createTextNode(version)
    versionNode.appendChild(versionNodeVal)
    head.appendChild(versionNode)
    archNode = manifest.createElement('arch')
    archNodeVal = manifest.createTextNode(arch)
    archNode.appendChild(archNodeVal)
    head.appendChild(archNode)
    packagesNode = manifest.createElement('packages')
    packages = pkgs.split(' ')
    for p in packages:
        packageNode = manifest.createElement('package')
        packageNodeVal = manifest.createTextNode(p)
        packageNode.appendChild(packageNodeVal)
        packagesNode.appendChild(packageNode)

    head.appendChild(packagesNode)
    filename = '' + tempdir + '' + name + '.manifest.xml'
    file = open(filename, 'w')
    output = manifest.toprettyxml()
    file.write(output)
    file.close()
    manifestLog.info('Genereated manifest file: ' + filename)


def push_bcfg2_group(name, pkgs, os, version):
    bcfg2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    bcfg2.connect((bcfg2_url, bcfg2_port))
    success = True
    bcfg2.send(name)
    ret = bcfg2.recv(100)
    if ret != 'OK':
        logger.error('Incorrect reply from the server:' + ret)
        success = False
    else:
        bcfg2.send(os)
        ret = bcfg2.recv(100)
        if ret != 'OK':
            logger.error('Incorrect reply from the server:' + ret)
            success = False
        else:
            bcfg2.send(version)
            ret = bcfg2.recv(100)
            if ret != 'OK':
                logger.error('Incorrect reply from the server:' + ret)
                success = False
            else:
                bcfg2.send(pkgs)
                ret = bcfg2.recv(100)
                if ret != 'OK':
                    logger.error('Incorrect reply from the server:' + ret)
                    success = False
    return success


if __name__ == '__main__':
    main()