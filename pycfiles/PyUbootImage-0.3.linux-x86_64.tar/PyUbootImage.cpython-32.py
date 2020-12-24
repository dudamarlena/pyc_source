# uncompyle6 version 3.7.4
# Python bytecode 3.2 (3180)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/lib/python3.2/site-packages/PyUbootImage/PyUbootImage.py
# Compiled at: 2012-06-15 11:06:16
"""
PyUbootImage library for reading u-boot image files as defined in the official u-boot sources.
"""
import sys
IH_OS_INVALID = 0
IH_OS_OPENBSD = 1
IH_OS_NETBSD = 2
IH_OS_FREEBSD = 3
IH_OS_4_4BSD = 4
IH_OS_LINUX = 5
IH_OS_SVR4 = 6
IH_OS_ESIX = 7
IH_OS_SOLARIS = 8
IH_OS_IRIX = 9
IH_OS_SCO = 10
IH_OS_DELL = 11
IH_OS_NCR = 12
IH_OS_LYNXOS = 13
IH_OS_VXWORKS = 14
IH_OS_PSOS = 15
IH_OS_QNX = 16
IH_OS_U_BOOT = 17
IH_OS_RTEMS = 18
IH_OS_ARTOS = 19
IH_OS_UNITY = 20
IH_OS_INTEGRITY = 21
IH_OS_LOOKUP = [
 'Invalid OS',
 'OpenBSD',
 'NetBSD',
 'FreeBSD',
 '4.4BSD',
 'Linux',
 'SVR4',
 'Esix',
 'Solaris',
 'Irix',
 'SCO',
 'Dell',
 'NCR',
 'LynxOS',
 'VxWorks',
 'pSOS',
 'QNX',
 'Firmware',
 'RTEMS',
 'ARTOS',
 'Unity',
 'INTEGRITY']
IH_ARCH_INVALID = 0
IH_ARCH_ALPHA = 1
IH_ARCH_ARM = 2
IH_ARCH_I386 = 3
IH_ARCH_IA64 = 4
IH_ARCH_MIPS = 5
IH_ARCH_MIPS64 = 6
IH_ARCH_PPC = 7
IH_ARCH_S390 = 8
IH_ARCH_SH = 9
IH_ARCH_SPARC = 10
IH_ARCH_SPARC64 = 11
IH_ARCH_M68K = 12
IH_ARCH_NIOS = 13
IH_ARCH_MICROBLAZE = 14
IH_ARCH_NIOS2 = 15
IH_ARCH_BLACKFIN = 16
IH_ARCH_AVR32 = 17
IH_ARCH_ST200 = 18
IH_ARCH_LOOKUP = [
 'Invalid',
 'Alpha',
 'ARM',
 'Intel',
 'IA64',
 'MIPS',
 'MIPS',
 'PowerPC',
 'IBM',
 'SuperH',
 'Sparc',
 'Sparc',
 'M68K',
 'Nios-32',
 'MicroBlaze',
 'Nios-II',
 'Blackfin',
 'AVR32',
 'STMicroelectronics']
IH_TYPE_INVALID = 0
IH_TYPE_STANDALONE = 1
IH_TYPE_KERNEL = 2
IH_TYPE_RAMDISK = 3
IH_TYPE_MULTI = 4
IH_TYPE_FIRMWARE = 5
IH_TYPE_SCRIPT = 6
IH_TYPE_FILESYSTEM = 7
IH_TYPE_FLATDT = 8
IH_TYPE_KWBIMAGE = 9
IH_TYPE_LOOKUP = [
 'Invalid Image',
 'Standalone Program',
 'OS Kernel Image',
 'RAMDisk Image',
 'Multi-File Image',
 'Firmware Image',
 'Script file',
 'Filesystem Image (any type)',
 'Binary Flat Device Tree Blob',
 'Kirkwood Boot Image']
IH_COMP_NONE = 0
IH_COMP_GZIP = 1
IH_COMP_BZIP2 = 2
IH_COMP_LZMA = 3
IH_COMP_LOOKUP = [
 'None', 'gzip', 'bzip2', 'lzma']
IH_COMP_EXT_LOOKUP = [
 'dat', 'gz', 'bz2', 'lzma']
IH_MAGIC = 654645590
IH_NMLEN = 32

class uboot_image:
    """Main class of this library containing
        all the header fields and an array of binary images.
        
        Image Types
         "Standalone Programs" are directly runnable in the environment
                provided by U-Boot; it is expected that (if they behave
                well) you can continue to work in U-Boot after return from
                the Standalone Program.
         "OS Kernel Images" are usually images of some Embedded OS which
                will take over control completely. Usually these programs
                will install their own set of exception handlers, device
                drivers, set up the MMU, etc. - this means, that you cannot
                expect to re-enter U-Boot except by resetting the CPU.
         "RAMDisk Images" are more or less just data blocks, and their
                parameters (address, size) are passed to an OS kernel that is
                being started.
         "Multi-File Images" contain several images, typically an OS
                (Linux) kernel image and one or more data images like
                RAMDisks. This construct is useful for instance when you want
                to boot over the network using BOOTP etc., where the boot
                server provides just a single image file, but you want to get
                for instance an OS kernel and a RAMDisk image.

                "Multi-File Images" start with a list of image sizes, each
                image size (in bytes) specified by an "uint32_t" in network
                byte order. This list is terminated by an "(uint32_t)0".
                Immediately after the terminating 0 follow the images, one by
                one, all aligned on "uint32_t" boundaries (size rounded up to
                a multiple of 4 bytes - except for the last file).

         "Firmware Images" are binary images containing firmware (like
                U-Boot or FPGA images) which usually will be programmed to
                flash memory.

         "Script files" are command sequences that will be executed by
                U-Boot's command interpreter; this feature is especially
                useful when you configure U-Boot to use a real shell (hush)
                as command interpreter (=> Shell Scripts).
        """

    def readInteger(self, myfile, length):
        """ Assemble multibyte integer from file"""
        ret = 0
        for i in range(0, length):
            ret = ret * 256 + (ord(myfile.read(1)) & 255)

        return ret

    def readIntegers(self, myfile, lenghts):
        """ Assemble multibyte integer array from file returning their list"""
        ret = []
        for length in lengths:
            val = self.readInteger(buf, myfile, lenght)
            ret.append(val)

        return ret

    def readShort(self, myfile):
        """ Assemble 2 bytes integer """
        return self.readInteger(myfile, 2)

    def readInt(self, myfile):
        """ Assemble 4 bytes integer """
        return self.readInteger(myfile, 4)

    def readLong(self, myfile):
        """ Assemble 8 byte integer """
        return self.readInteger(myfile, 8)

    def makeInteger(self, buf, start, lenght):
        """ Assemble multibyte integer from array"""
        ret = 0
        for i in range(start, start + lenght):
            if sys.version_info[0] < 3:
                ret = ret * 256 + (ord(buf[i]) & 255)
            else:
                ret = ret * 256 + (int(buf[i]) & 255)

        return (
         ret, start + lenght)

    def makeIntegers(self, buf, start, lenghts):
        """ Assemble a set of consecutive multibyte
                integers given their lenghts and return them
                in a list"""
        ret = []
        for length in lenghts:
            val, start = self.makeInteger(buf, start, length)
            ret.append(val)

        ret.append(start)
        return ret

    def v(self, lookup, n):
        """Utility method to use this libraries lookup tables"""
        if n < 0 or n >= len(lookup):
            return '<not supported %02X>' % n
        return lookup[n]

    def __init__(self):
        """Main constructor that build not-initialized object"""
        self.ih_magic = 0
        self.ih_hcrc = 0
        self.ih_time = 0
        self.ih_size = 0
        self.ih_load = 0
        self.ih_ep = 0
        self.ih_dcrc = 0
        self.ih_os = 0
        self.ih_arch = 0
        self.ih_type = 0
        self.ih_comp = 0
        self.ih_name = ''
        self.parts = []

    def fill(self, buf):
        """Fill the header only with the values read from buf array"""
        self.ih_magic, self.ih_hcrc, self.ih_time, self.ih_size, self.ih_load, self.ih_ep, self.ih_dcrc, self.ih_os, self.ih_arch, self.ih_type, self.ih_comp, end = self.makeIntegers(buf, 0, (4,
                                                                                                                                                                                                4,
                                                                                                                                                                                                4,
                                                                                                                                                                                                4,
                                                                                                                                                                                                4,
                                                                                                                                                                                                4,
                                                                                                                                                                                                4,
                                                                                                                                                                                                1,
                                                                                                                                                                                                1,
                                                                                                                                                                                                1,
                                                                                                                                                                                                1))
        self.ih_name = buf[end:end + IH_NMLEN]
        return end + IH_NMLEN

    def checkMagic(self):
        """Check if the magic number contained in ih_magic field is correct or not"""
        return self.ih_magic == IH_MAGIC

    def parse(self, buf):
        """Read image header and extract the binary images"""
        end = self.fill(buf)
        if self.ih_type == IH_TYPE_MULTI:
            parts = self.getMultiParts(buf, end)
        else:
            self.parts = [
             buf[end:end + self.ih_size]]
        return self

    def os_name(self):
        return self.v(IH_OS_LOOKUP, self.ih_os)

    def arch_name(self):
        return self.v(IH_ARCH_LOOKUP, self.ih_arch)

    def type_name(self):
        return self.v(IH_TYPE_LOOKUP, self.ih_type)

    def comp_name(self):
        return self.v(IH_COMP_LOOKUP, self.ih_comp)

    def getInfo(self):
        """Return a dictionary with a human-readable version
                of the content of the header"""
        return {'MAGIC': self.ih_magic, 
         'HCRC': self.ih_hcrc, 
         'TIME': self.ih_time, 
         'SIZE': self.ih_size, 
         'LOAD': self.ih_load, 
         'EP': self.ih_ep, 
         'DCRC': self.ih_dcrc, 
         'OS': self.os_name(), 
         'ARCH': self.arch_name(), 
         'TYPE': self.type_name(), 
         'COMP': self.comp_name(), 
         'NAME': self.ih_name, 
         'PARTS': len(self.parts)}

    def getMultiParts(self, buf, start):
        """Internal method used by parse() to separate binary images"""
        ofs = []
        p = []
        while True:
            val, start = self.makeInteger(buf, start, 4)
            if val == 0:
                break
            ofs.append(val)

        for size in ofs:
            part = buf[start:start + size]
            pad = size % 4
            if pad != 0:
                size += 4 - pad
            start += size
            p.append(part)

        self.parts = p


if __name__ == '__main__':
    if len(sys.argv) < 2:
        sys.stdout.write('Usage: %s path_to_u-boot_image\n' % sys.argv[0])
        sys.exit(0)
    f = open(sys.argv[1], 'rb')
    image_data = f.read()
    f.close()
    image = uboot_image().parse(image_data)
    if not image.checkMagic():
        sys.stdout.write('Bad magic number!\n')
        sys.exit(1)
    sys.stdout.write('Found image!\n\t' + '\n\t'.join([a[0].ljust(5) + ': ' + str(a[1] if type(a[1]) != bytes else a[1].decode('latin-1')) for a in image.getInfo().items()]) + '\n')
    format_string = 'part_%02d.' + IH_COMP_EXT_LOOKUP[image.ih_comp]
    i = 0
    for part in image.parts:
        f = open(format_string % i, 'wb')
        f.write(part)
        f.close()
        i += 1

    sys.exit(0)