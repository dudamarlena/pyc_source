# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/bruno1/Developing/Python-Files/express_vpn/express/statuscheck.py
# Compiled at: 2017-07-25 00:35:04
# Size of source mod 2**32: 944 bytes
import subprocess

def checkstatus(self):
    checkvpn = '/usr/bin/expressvpn status'
    self.stdoutdata = subprocess.getoutput(checkvpn)
    conn = self.stdoutdata.startswith('Connected')
    print(self.conn)
    return conn


def connected():
    if self.checkstatus():
        self.location_string = self.stdoutdata[13:]
        self.loc_alias2 = self.server.index[(self.server['location'] == self.location_string)][0]
        self.alias_icon = self.server.loc[(self.loc_alias2, 'icon2')]
        pixmap = QPixmap(self.alias_icon)
        self.label_7.setPixmap(pixmap)
        self.lb_status.setText('VPN OK')
        self.label_8.setText(self.location_string)
    else:
        alias_icon = self.files + 'novpn1.png'
        pixmap = QPixmap(alias_icon)
        print(pixmap)
        self.label_7.setPixmap(pixmap)
        self.label_8.setText('No VPN Connected')
        self.lb_status.setText('Connect to a Server')