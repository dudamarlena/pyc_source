# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: \Python34\Lib\site-packages\autohdl\manager.py
# Compiled at: 2015-05-18 14:09:04
# Size of source mod 2**32: 3916 bytes
import argparse, glob, logging, os, pprint, sys, subprocess
from autohdl import synplify
from autohdl import xilinx
from autohdl import configuration
alog = logging.getLogger(__name__)

def print_info(config):
    alog.info(('Main design settings:\n' + '#' * 40 + '\ntechnology : {technology}\npart       : {part}\npackage    : {package}\ntop module : {top}\nconstraints: {ucf}\neeprom size: {size} kilobytes\n' + '#' * 40 + '').format(technology=config.get('technology'), part=config.get('part'), package=config.get('package'), top=config.get('top_module'), ucf=config.get('constraints'), size=config.get('eeprom_kilobytes'), upload=config.get('upload')))


def cli_handler():
    parser = argparse.ArgumentParser(description='HDL Manager')
    parser.add_argument('-top', dest='top_module', help='set top module name')
    parser.add_argument('-synplify', nargs='?', const='batch', choices=['batch', 'gui'], help='synthesis step [default=batch]')
    parser.add_argument('-xilinx', nargs='?', const='batch', choices=['batch', 'gui'], help='implementation step [default=batch]')
    parser.add_argument('-mcs', nargs='?', help='generate .mcs from .bit file')
    parser.add_argument('-upload', action='store_true', help='upload firmware to WebDav server')
    parser.add_argument('-message', help='information about firmware')
    parser.add_argument('-debug', nargs='?', const='')
    res = parser.parse_args()
    return res


def validate(cfg):
    for k, s in (('top_module', 'Top module undefined'), ('constraints', 'There is no constraints files')):
        if not cfg.get(k):
            if 'batch' in (cfg.get('synplify'), cfg.get('xilinx')):
                sys.exit('[Error] {}, exit...'.format(s))
            else:
                alog.warning('{}'.format(s))
                continue


def set_debug(cfg):
    debug_module = cfg.get('debug')
    if debug_module is not None:
        import logging.config as lc
        from autohdl import LOGGING_DICT
        LOGGING_DICT.update({'loggers': {debug_module: {'handlers': ['cmd_debug', 'file_debug']}}})
        lc.dictConfig(LOGGING_DICT)


def kungfu(script_cfg):
    subprocess.call('hdl -v', shell=True)
    alog.info('Processing...')
    command_line_cfg = cli_handler()
    set_debug(vars(command_line_cfg))
    alog.debug('Command line args: ' + str(sys.argv))
    alog.debug(pprint.pformat(command_line_cfg))
    alog.debug('Script cfg:\n' + pprint.pformat(script_cfg))
    configuration.copy()
    cfg = configuration.load(script_cfg=script_cfg, command_line_cfg=command_line_cfg)
    alog.debug('Merged cfg:')
    alog.debug(pprint.pformat(cfg))
    validate(cfg)
    print_info(cfg)
    if len(sys.argv) == 1:
        cfg['synplify'] = 'batch'
        cfg['xilinx'] = 'batch'
        synplify.run(cfg)
        xilinx.run(cfg)
        if cfg.get('eeprom_kilobytes'):
            xilinx.bit_to_mcs(cfg)
        xilinx.copy_firmware(cfg)
    else:
        if cfg.get('synplify'):
            synplify.run(cfg)
        else:
            if cfg.get('xilinx'):
                xilinx.run(cfg)
                if cfg.get('eeprom_kilobytes'):
                    xilinx.bit_to_mcs(cfg)
                xilinx.copy_firmware(cfg)
            elif cfg.get('mcs'):
                xilinx.bit_to_mcs(cfg)
                xilinx.copy_firmware(cfg)


if __name__ == '__main__':
    print('test')