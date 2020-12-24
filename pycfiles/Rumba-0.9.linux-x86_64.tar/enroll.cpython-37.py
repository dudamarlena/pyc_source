# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/lib/python3.7/site-packages/rumba/prototypes/enroll.py
# Compiled at: 2018-04-23 11:23:30
# Size of source mod 2**32: 4154 bytes
import argparse, socket, time, re, sys

def printalo(byt):
    print(repr(byt).replace('\\n', '\n'))


def get_response(s):
    data = bytes()
    while 1:
        data += s.recv(1024)
        lines = str(data).replace('\\n', '\n').split('\n')
        if lines[(-1)].find('IPCM') != -1:
            return lines[:len(lines) - 1]


description = 'Python script to enroll IPCPs'
epilog = '2016 Vincenzo Maffione <v.maffione@nextworks.it>'
argparser = argparse.ArgumentParser(description=description, epilog=epilog)
argparser.add_argument('--ipcm-conf', help='Path to the IPCM configuration file', type=str,
  required=True)
argparser.add_argument('--enrollee-name', help='Name of the enrolling IPCP', type=str,
  required=True)
argparser.add_argument('--dif', help='Name of DIF to enroll to', type=str,
  required=True)
argparser.add_argument('--lower-dif', help='Name of the lower level DIF', type=str,
  required=True)
argparser.add_argument('--enroller-name', help='Name of the remote neighbor IPCP to enroll to', type=str,
  required=True)
args = argparser.parse_args()
socket_name = None
fin = open(args.ipcm_conf, 'r')
while 1:
    line = fin.readline()
    if line == '':
        break
    m = re.search('"(\\S+ipcm-console.sock)', line)
    if m != None:
        socket_name = m.group(1)
        break

fin.close()
if socket_name == None:
    print('Cannot find %s' % socket_name)
    quit(1)
else:
    s = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    connected = False
    trials = 0
    while trials < 4:
        try:
            s.connect(socket_name)
            connected = True
            break
        except:
            pass

        trials += 1
        time.sleep(1)

    if connected:
        try:
            get_response(s)
            cmd = 'list-ipcps\n'
            s.sendall(cmd.encode('ascii'))
            print('Looking up identifier for IPCP %s' % args.enrollee_name)
            lines = get_response(s)
            print(lines)
            enrollee_id = None
            for line in lines:
                rs = '^\\s*(\\d+)\\s*\\|\\s*' + args.enrollee_name.replace('.', '\\.')
                m = re.match(rs, line)
                if m != None:
                    enrollee_id = m.group(1)

            if enrollee_id == None:
                print('Could not find the ID of enrollee IPCP %s' % args.enrollee_name)
                raise Exception()
            cmd = 'enroll-to-dif %s %s %s %s 1\n' % (
             enrollee_id, args.dif, args.lower_dif, args.enroller_name)
            print(cmd)
            s.sendall(cmd.encode('ascii'))
            lines = get_response(s)
            print(lines)
        except:
            s.close()
            raise

    else:
        print('Failed to connect to "%s"' % socket_name)
        sys.exit(-1)
s.close()