# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/futuregrid/image/management/IMBcfg2GroupManagerServer.py
# Compiled at: 2012-09-06 11:03:15
"""
Description: Command line front end for image generator
"""
import socket, sys
from xml.dom.ext import PrettyPrint
from xml.dom.minidom import Document, parse
bundlePath = '/var/lib/bcfg2/Bundler/'
groupPath = '/var/lib/bcfg2/Metadata/'
port = 45678

def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(('', port))
    sock.listen(1)
    while True:
        (channel, details) = sock.accept()
        name = channel.recv(512)
        print 'DEBUG: Received name: ' + name
        channel.send('OK')
        os = channel.recv(512)
        print 'DEBUG: Received OS: ' + os
        channel.send('OK')
        version = channel.recv(512)
        print 'DEBUG: Received version: ' + version
        channel.send('OK')
        packages = channel.recv(4096)
        print 'DEBUG: Recevied packages: ' + packages
        channel.send('OK')
        channel.close()
        writebundleXML(name, packages)
        modifyGroups(name, os, version)


def modifyGroups(name, os, version):
    filename = groupPath + 'groups.xml'
    file = open(filename, 'r')
    groups = parse(file)
    groupsNode = groups.childNodes[0]
    newGroup = groups.createElement('Group')
    newGroup.setAttribute('profile', 'true')
    newGroup.setAttribute('public', 'true')
    newGroup.setAttribute('name', name)
    groupsNode.appendChild(newGroup)
    osGroup = groups.createElement('Group')
    osGroup.setAttribute('name', os + '-' + version)
    newGroup.appendChild(osGroup)
    bundleGroup = groups.createElement('Bundle')
    bundleGroup.setAttribute('name', name)
    newGroup.appendChild(bundleGroup)
    file.close()
    file = open(filename, 'w')
    PrettyPrint(groups, file)


def writebundleXML(name, packages):
    bundle = Document()
    bundleHead = bundle.createElement('Bundle')
    bundleHead.setAttribute('name', name)
    bundle.appendChild(bundleHead)
    pkgs = packages.split(' ')
    for package in pkgs:
        p = bundle.createElement('Package')
        p.setAttribute('name', package)
        bundleHead.appendChild(p)

    file = open(bundlePath + name + '.xml', 'w')
    PrettyPrint(bundle, file)


if __name__ == '__main__':
    main()