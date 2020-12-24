# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/insights/parsers/tests/test_setup_named_chroot.py
# Compiled at: 2019-11-14 13:57:46
from insights.parsers import setup_named_chroot, SkipException
from insights.parsers.setup_named_chroot import SetupNamedChroot
from insights.tests import context_wrap
import doctest, pytest
CHROOT_CONTENT_FILTERED = ("\n#!/bin/bash\n# it MUST be listed last. (/var/named contains /var/named/chroot)\nROOTDIR_MOUNT='/etc/localtime /etc/named /etc/pki/dnssec-keys /etc/named.root.key /etc/named.conf\n/etc/named.dnssec.keys /etc/named.rfc1912.zones /etc/rndc.conf /etc/rndc.key /usr/lib64/bind\n/usr/lib/bind /etc/named.iscdlv.key /run/named /var/named /etc/protocols /etc/services'\n    for all in $ROOTDIR_MOUNT; do\n    for all in $ROOTDIR_MOUNT; do,\n    # Check if file is mount target. Do not use /proc/mounts because detecting\n").strip()
CHROOT_CONTENT_ALL = ('\n#!/bin/bash\n\n# Warning: the order is important\n# If a directory containing $ROOTDIR is listed here,\n# it MUST be listed last. (/var/named contains /var/named/chroot)\nROOTDIR_MOUNT=\'/etc/localtime /etc/named /etc/pki/dnssec-keys /etc/named.root.key /etc/named.conf\n/etc/named.dnssec.keys /etc/named.rfc1912.zones /etc/rndc.conf /etc/rndc.key /etc/named.iscdlv.key /etc/protocols /etc/services\n/usr/lib64/bind /usr/lib/bind /run/named\n/var/named\'\n\nusage()\n{\n  echo\n  echo \'This script setups chroot environment for BIND\'\n  echo \'Usage: setup-named-chroot.sh ROOTDIR [on|off]\'\n}\n\nif ! [ "$#" -eq 2 ]; then\n  echo \'Wrong number of arguments\'\n  usage\n  exit 1\nfi\n\nROOTDIR="$1"\n\n# Exit if ROOTDIR doesn\'t exist\nif ! [ -d "$ROOTDIR" ]; then\n  echo "Root directory $ROOTDIR doesn\'t exist"\n  usage\n  exit 1\nfi\n\nmount_chroot_conf()\n{\n  if [ -n "$ROOTDIR" ]; then\n    for all in $ROOTDIR_MOUNT; do\n      # Skip nonexistant files\n      [ -e "$all" ] || continue\n\n      # If mount source is a file\n      if ! [ -d "$all" ]; then\n        # mount it only if it is not present in chroot or it is empty\n        if ! [ -e "$ROOTDIR$all" ] || [ `stat -c\'%s\' "$ROOTDIR$all"` -eq 0 ]; then\n          touch "$ROOTDIR$all"\n          mount --bind "$all" "$ROOTDIR$all"\n        fi\n      else\n        # Mount source is a directory. Mount it only if directory in chroot is\n        # empty.\n        if [ -e "$all" ] && [ `ls -1A $ROOTDIR$all | wc -l` -eq 0 ]; then\n          mount --bind --make-private "$all" "$ROOTDIR$all"\n        fi\n      fi\n    done\n  fi\n}\n\numount_chroot_conf()\n{\n  if [ -n "$ROOTDIR" ]; then\n    for all in $ROOTDIR_MOUNT; do\n      # Check if file is mount target. Do not use /proc/mounts because detecting\n      # of modified mounted files can fail.\n      if mount | grep -q \'.* on \'"$ROOTDIR$all"\' .*\'; then\n        umount "$ROOTDIR$all"\n        # Remove temporary created files\n        [ -f "$all" ] && rm -f "$ROOTDIR$all"\n      fi\n    done\n  fi\n}\n\ncase "$2" in\n  on)\n    mount_chroot_conf\n    ;;\n  off)\n    umount_chroot_conf\n    ;;\n  *)\n    echo \'Second argument has to be "on" or "off"\'\n    usage\n    exit 1\nesac\n\nexit 0\n').strip()
EXCEPTION1 = ('\n').strip()
EXCEPTION2 = ('\nusage()\n{\n  echo\n  echo \'This script setups chroot environment for BIND\'\n  echo \'Usage: setup-named-chroot.sh ROOTDIR [on|off]\'\n}\n\nif ! [ "$#" -eq 2 ]; then\n  echo \'Wrong number of arguments\'\n  usage\n  exit 1\nfi\n').strip()

def test_setup_named_chroot_all():
    snc = SetupNamedChroot(context_wrap(CHROOT_CONTENT_ALL))
    assert snc['ROOTDIR_MOUNT'][(-1)] == '/var/named'
    assert len(snc) == 2


def test_setup_named_chroot_filtered():
    snc = SetupNamedChroot(context_wrap(CHROOT_CONTENT_FILTERED))
    assert 'ROOTDIR_MOUNT' in snc
    assert snc['ROOTDIR_MOUNT'][(-1)] != '/var/named'
    assert len(snc.raw) == 5


def test_doc_examples():
    env = {'snc': SetupNamedChroot(context_wrap(CHROOT_CONTENT_ALL))}
    failed, total = doctest.testmod(setup_named_chroot, globs=env)
    assert failed == 0


def test_setup_named_chroot_exception1():
    with pytest.raises(SkipException) as (e):
        SetupNamedChroot(context_wrap(EXCEPTION1))
    assert 'Empty file' in str(e)


def test_setup_named_chroot_exception2():
    with pytest.raises(SkipException) as (e):
        SetupNamedChroot(context_wrap(EXCEPTION2))
    assert 'Input content is not empty but there is no useful parsed data.' in str(e)