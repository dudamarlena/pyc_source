# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/archipelagentvmcasting/appliancedecompresser.py
# Compiled at: 2013-03-20 13:50:16
import os, shutil, tarfile, tempfile, xmpp
from gzip import GzipFile as gz
from threading import Thread
from archipel.archipelLibvirtEntity import generate_mac_adress

class TNApplianceDecompresser(Thread):

    def __init__(self, working_dir, disk_exts, xvm2_package_path, entity, finish_callback, error_callback, package_uuid, requester):
        """
        Initialize a TNApplianceDecompresser.
        @type working_dir: string
        @param working_dir: the base dir where TNApplianceDecompresser will works
        @type disk_exts: array
        @param disk_exts: contains all the extensions that should be considered as a disks with the initial dot (ie: .gz)
        @type xvm2_package_path: string
        @param xvm2_package_path: path of the xvm2 file
        @type entity: L{TNArchipelVirtualMachine}
        @param entity: the virtual machine
        @type finish_callback: function
        @param finish_callback: called when decompression is done sucessfully
        @type error_callback: function
        @param error_callback: called when decompression has failed
        @type package_uuid: string
        @param package_uuid: UUID of the package
        @type requester: xmpp.Protocol.JID
        @param requester: the JID of the requester
        """
        self.working_dir = working_dir
        self.disk_extensions = disk_exts
        self.xvm2_package_path = xvm2_package_path
        self.entity = entity
        self.finish_callback = finish_callback
        self.error_callback = error_callback
        self.package_uuid = package_uuid
        self.requester = requester
        self.install_path = entity.folder
        self.description_file = None
        self.disk_files = {}
        self.snapshots_desc = []
        Thread.__init__(self)
        return

    def run(self):
        """
        Run the thread.
        """
        try:
            self.entity.log.info('TNApplianceDecompresser: unpacking to %s' % self.working_dir)
            try:
                self.entity.log.info('TNApplianceDecompresser: unpacking to %s' % self.working_dir)
                self.unpack()
            except Exception, ex:
                raise Exception('TNApplianceDecompresser: cannot unpack because unpack() has returned exception: %s' % str(ex))

            try:
                self.entity.log.info('TNApplianceDecompresser: defining UUID in description file as %s' % self.entity.uuid)
                self.update_description()
            except Exception, ex:
                raise Exception('TNApplianceDecompresser: cannot update description because update_description() has returned exception: %s' % str(ex))

            try:
                self.entity.log.info('TNApplianceDecompresser: installing package in %s' % self.install_path)
                self.install()
            except Exception, ex:
                raise Exception('TNApplianceDecompresser: cannot update install because install returned exception %s' % str(ex))

            self.entity.log.info('TNApplianceDecompresser: cleaning working directory %s ' % self.working_dir)
            self.clean()
            self.entity.log.info('TNApplianceDecompresser: Defining the virtual machine')
            self.entity.define(self.description_node)
            self.finish_callback()
        except Exception, ex:
            try:
                self.clean()
            except:
                pass
            else:
                self.error_callback(ex)
                self.entity.log.error(str(ex))

    def unpack(self):
        """
        Unpack the given xvm2 package.
        @rtype: boolean
        @return: True in case of success
        """
        self.package_path = self.xvm2_package_path
        self.temp_path = tempfile.mkdtemp(dir=self.working_dir)
        self.extract_path = os.path.join(self.temp_path, 'export')
        package = tarfile.open(name=self.package_path)
        package.extractall(path=self.extract_path)
        for aFile in os.listdir(self.extract_path):
            full_path = os.path.join(self.extract_path, aFile)
            self.entity.log.debug('TNApplianceDecompresser: parsing file %s' % full_path)
            if os.path.splitext(full_path)[(-1)] == '.gz':
                self.entity.log.info('Found one gziped disk: %s' % full_path)
                i = open(full_path, 'rb')
                o = open(full_path.replace('.gz', ''), 'w')
                self._gunzip(i, o)
                i.close()
                o.close()
                self.entity.log.info('File unziped at: %s' % full_path.replace('.gz', ''))
                self.disk_files[aFile.replace('.gz', '')] = full_path.replace('.gz', '')
            if os.path.splitext(full_path)[(-1)] in self.disk_extensions:
                self.entity.log.debug('Found one disk: %s' % full_path)
                self.disk_files[aFile] = full_path
            if aFile == 'description.xml':
                self.entity.log.debug('Found description.xml file: %s' % full_path)
                o = open(full_path, 'r')
                self.description_file = o.read()
                o.close()

        return True

    def update_description(self):
        """
        Define the uuid to write in the description file.
        @raise Exception: Exception if description file is empty
        @return: True in case of success
        """
        if not self.description_file:
            raise Exception('Description file is empty.')
        desc_string = self.description_file
        xml_desc = xmpp.simplexml.NodeBuilder(data=desc_string).getDom()
        name_node = xml_desc.getTag('name')
        uuid_node = xml_desc.getTag('uuid')
        if xml_desc.getTag('devices'):
            disk_nodes = xml_desc.getTag('devices').getTags('disk')
            for disk in disk_nodes:
                source = disk.getTag('source')
                if source:
                    source_file = os.path.basename(source.getAttr('file')).replace('.gz', '')
                    source.setAttr('file', os.path.join(self.entity.folder, source_file))

        if xml_desc.getTag('devices'):
            nics_nodes = xml_desc.getTag('devices').getTags('interface')
            for nic in nics_nodes:
                mac = nic.getTag('mac')
                if mac:
                    mac.setAttr('address', generate_mac_adress())
                else:
                    nic.addChild(name='mac', attrs={'address': generate_mac_adress()})

        name_node.setData(self.entity.uuid)
        uuid_node.setData(self.entity.uuid)
        self.description_node = xml_desc
        return True

    def recover_snapshots(self):
        """
        Recover any snapshots.
        """
        for snap in self.snapshots_desc:
            try:
                snap_node = xmpp.simplexml.NodeBuilder(data=snap).getDom()
                snap_node.getTag('domain').getTag('uuid').setData(self.entity.uuid)
                snap_str = str(snap_node).replace('xmlns="http://www.gajim.org/xmlns/undeclared" ', '')
                self.entity.domain.snapshotCreateXML(snap_str, 0)
            except Exception, ex:
                self.entity.log.error("TNApplianceDecompresser: can't recover snapshot: %s", str(ex))

    def install(self):
        """
        Install a untared and uuid defined package.
        @return: True in case of success
        """
        if not self.description_file:
            raise Exception('description file is empty')
        for (key, path) in self.disk_files.items():
            self.entity.log.debug('TNApplianceDecompresser: moving %s to %s' % (path, self.install_path))
            try:
                shutil.move(path, self.install_path)
            except:
                os.remove(self.install_path + '/' + key)
                shutil.move(path, self.install_path)

        f = open(self.install_path + '/current.package', 'w')
        f.write(self.package_uuid)
        f.close()
        return True

    def _gunzip(self, fileobjin, fileobjout):
        """
        Returns NamedTemporaryFile with unzipped content of fileobj.
        @type fileobjin: File
        @param fileobjin: file containing the archive
        @type fileobjout: File
        @param fileobjout: file where to put the unziped file
        """
        source = gz(fileobj=fileobjin, mode='rb')
        target = fileobjout
        try:
            while 1:
                data = source.read(65536)
                if data and len(data):
                    target.write(data)
                else:
                    target.flush()
                    break

        except Exception:
            target.close()
            raise
        else:
            return target

    def clean(self):
        """
        Clean the tempory path.
        """
        shutil.rmtree(self.temp_path)