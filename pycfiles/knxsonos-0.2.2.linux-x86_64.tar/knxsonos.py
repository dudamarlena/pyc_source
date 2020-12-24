# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/knxsonos/knxsonos.py
# Compiled at: 2016-04-09 17:13:59
import xml.etree.ElementTree as ET
from time import sleep
import sys, os, logging, sonos, knx
logger = logging.getLogger('knxsonos')
banner = "\nKnxSonos Copyright (C) 2010-2016 Trond Kjeldaas\nThis program comes with ABSOLUTELY NO WARRANTY;\nThis is free software, and you are welcome to redistribute it\nunder certain conditions; For more details see the file named\n'LICENSE' which should be included with the release.\n"

def loadCommand(cmd):
    if 'param' in cmd.attrib.keys():
        param = cmd.attrib['param']
    else:
        param = None
    command = cmd.attrib['command']
    return (
     command, param)


def loadMacros(element):
    macros = {}
    for macro in element.findall('macro'):
        macros[macro.attrib['name']] = []
        for action in macro.findall('action'):
            command, param = loadCommand(action)
            macros[macro.attrib['name']].append((command, param))

    return macros


def maybeExpandMacro(macros, cl):
    ret = []
    for c, p in cl:
        if c in macros.keys():
            ret.extend(maybeExpandMacro(macros, macros[c]))
        else:
            ret.append((c, p))

    return ret


def loadCommands(macros, element):
    cmd_map = []
    for cmd in element.findall('mapping'):
        command, param = loadCommand(cmd)
        command = maybeExpandMacro(macros, [(command, param)])
        cmd_map.append((cmd.attrib['groupAddress'],
         command))

    return cmd_map


def loadZoneConfig(global_macros, root, zone):
    Z = {'name': zone.attrib['name']}
    macros = dict(global_macros)
    macros.update(loadMacros(zone))
    Z['cmdMap'] = loadCommands(macros, root)
    Z['cmdMap'].extend(loadCommands(macros, zone))
    return Z


def loadConfig():
    cfgname = False
    try:
        if os.access(sys.argv[(sys.argv.index('-c') + 1)], os.R_OK):
            cfgname = sys.argv[(sys.argv.index('-c') + 1)]
    except ValueError:
        if os.access('knxsonos.config', os.R_OK):
            cfgname = 'knxsonos.config'

    if not cfgname:
        logger.error('ERROR: Failed to load configuration file.')
        logger.error('ERROR: Either specify one with the -c option, or make')
        logger.error('ERROR: sure that a file named knxsonos.config exists.')
        sys.exit(1)
    root = ET.parse(cfgname).getroot()
    knx = {'url': root.find('knx').attrib['url']}
    zones = []
    cmd_maps = {}
    global_macros = loadMacros(root)
    for zone in root.findall('zone'):
        Z = loadZoneConfig(global_macros, root, zone)
        zones.append(Z)

    return {'knx': knx, 'zones': zones}


def main():
    """The main entry point to knxsonos.py.
    This is installed as the script entry point.
    """
    try:
        status = 0
        logger.info(banner)
        cfg = loadConfig()
        knx_cmd_map = []
        c = sonos.SonosCtrl([ zone['name'] for zone in cfg['zones'] ])
        c.start()
        for zone in cfg['zones']:
            for ga, cmds in zone['cmdMap']:
                cmds2 = [ (c.getCmdDict().get(oneCmd, oneCmd), param) for oneCmd, param in cmds
                        ]
                knx_cmd_map.append((zone['name'], ga, cmds2))

        k = knx.KnxInterface(cfg['knx']['url'], knx_cmd_map)
        k.start()
        while True:
            try:
                sleep(1)
            except KeyboardInterrupt:
                k.stop()
                c.stop()
                exit(0)

    except SystemExit as err:
        if err.args:
            status = err.args[0]
        else:
            status = None

    return status


if __name__ == '__main__':
    main()