# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: \Python34\Lib\site-packages\autohdl\xilinx.py
# Compiled at: 2015-05-17 03:37:22
# Size of source mod 2**32: 8007 bytes
import os, shutil, subprocess, sys, time
from time import strftime
import locale, copy, logging, autohdl.utils as utils, re
from autohdl import toolchain
from autohdl import IMPLEMENT_PATH, SYNTHESIS_PATH, NETLIST_EXT
alog = logging.getLogger(__name__)
XTCL_SCRIPT = 'project new {project_name}.xise\n\nproject set family "{family}"\nproject set device "{device}"\nproject set package "{package}"\nproject set speed "{speed}"\n\nproject set top_level_module_type "EDIF"\nproject set "Preferred Language" "Verilog"\nproject set "Verilog Macros" "I_HAVE_ONLY_FUCKING_XST"\n#project set "FPGA Start-Up Clock" "JTAG Clock"\n\n{xfiles}\n\nproject set top "{top}"\n\n{process_run}\n\nproject close\n'
PROCESS_WITH_HANDLER = 'process run "Generate Programming File"\n\nset my_status [ process get "Generate Programming File" status ]\nputs $my_status\nif {( $my_status == "up_to_date" ) ||\n    ( $my_status == "warnings" ) } {\n     puts "Process Ok"\n} else {\n    puts "Process failed"\n    exit 1\n}\n'

def bit_to_mcs(cfg):
    extend_cfg(cfg)
    try:
        if [
         'eeprom_kilobytes']:
            proc = '{tool} -u 0 {top} -s {size} -w'.format(tool=toolchain.Tool().get('ise_promgen'), top=cfg['bit_file'], size=cfg['eeprom_kilobytes'])
            subprocess.check_call(proc)
        else:
            alog.warning('EEPROM size was not set')
    except subprocess.CalledProcessError as e:
        alog.error(e)
        sys.exit(1)


def copy_firmware(cfg):
    firmware_ext = ('.bit', '.mcs')
    build_timestamp = strftime('%y%m%d_%H%M%S', time.localtime())
    dest_dir = os.path.join(cfg['dsn_root'], 'resource')
    search_dir = os.path.join(cfg['dsn_root'], 'autohdl', 'implement', cfg['top_module'])
    fw_old = [i for i in os.listdir(dest_dir) if os.path.splitext(i)[1] in firmware_ext and cfg['dsn_name'] + '_' + cfg['top_module'] in i]
    for ext in firmware_ext:
        src_path = os.path.join(search_dir, cfg['top_module'] + ext)
        if os.path.exists(src_path):
            dst_path = '{path}/{dsn}_{top}_{time}{ext}'.format(path=dest_dir, dsn=cfg['dsn_name'], top=cfg['top_module'], time=build_timestamp, ext=ext)
            dst_path_old = None
            for fname_old in fw_old:
                pattern = '{dsn}_{top}_{date}{ext}'.format(dsn=cfg['dsn_name'], top=cfg['top_module'], date='\\d{6}_\\d{6}', ext=ext)
                if re.search(pattern=pattern, string=fname_old):
                    dst_path_old = os.path.join(dest_dir, fname_old)
                    if not utils.is_same_contents(src_path, dst_path_old):
                        alog.info('Remove old firmware: ' + dst_path_old)
                        os.remove(dst_path_old)
                        alog.info('Copy new firmware: ' + dst_path)
                        shutil.copy(src_path, dst_path)
                    else:
                        alog.info('No need to replace, same contents: ' + dst_path_old)
                        continue

            if not dst_path_old:
                alog.info('Copy new firmware ' + dst_path)
                shutil.copy(src_path, dst_path)
            else:
                continue


def clean(cfg):
    for i in range(3):
        if os.path.exists(cfg['prj_dir']):
            try:
                shutil.rmtree(cfg['prj_dir'])
                break
            except Exception as e:
                alog.warning(e)
                time.sleep(1)

            continue

    if os.path.exists(cfg['prj_dir']):
        message = "Can't clean xilinx project {}".format(cfg['prj_dir'])
        alog.error(message)
        sys.exit(message)


def mk_dir(cfg):
    for i in range(3):
        if not os.path.exists(cfg['prj_dir']):
            try:
                os.makedirs(cfg['prj_dir'])
                break
            except Exception as e:
                alog.warning(e)
                time.sleep(1)

            continue

    if not os.path.exists(cfg['prj_dir']):
        message = "Can't make xilinx project {}".format(cfg['prj_dir'])
        alog.error(message)
        sys.exit(message)


def mk_script(cfg):
    src = [i.replace('\\', '/') for i in cfg['src'] if os.path.splitext(i)[1] in NETLIST_EXT]
    src.append(cfg['syn_constraint'])
    src.append(cfg['syn_netlist'])
    xfiles = ['xfile add "{}"'.format(afile.replace('\\', '/')) for afile in src]
    if cfg['xilinx'] == 'batch':
        proc_run = PROCESS_WITH_HANDLER
    else:
        proc_run = ''
    res = XTCL_SCRIPT.format(project_name=cfg['prj_name'], family=cfg['technology'], device=cfg['part'], package=cfg['package'], speed=cfg['speed_grade'], xfiles='\n'.join(xfiles), top=cfg['top_module'], process_run=proc_run)
    with open(cfg['prj_script'], 'w') as (f):
        f.write(res)


def run_tool(cfg):
    command = '{program} {arguments}'.format(program=toolchain.Tool().get('ise_batch'), arguments=cfg['prj_script'])
    subprocess.check_call(command)
    if cfg['xilinx'] == 'gui':
        command = '{program} {arguments}'.format(program=toolchain.Tool().get('ise_gui'), arguments=cfg['prj_gui_file'])
        subprocess.check_call(command)


def load_env_settings():
    try:
        wrapper = toolchain.Tool().get('ise_wrapper')
        encoding = locale.getdefaultlocale()[1]
        res = subprocess.check_output('cmd /c "call {0} & set"'.format(wrapper.replace('/', '\\')))
        res = res.decode(encoding)
        d = {}
        for i in res.split(os.linesep):
            res = i.split('=')
            if len(res) == 2:
                d.update({res[0]: res[1]})
                continue

        alog.info('Load xilinx env from: ' + wrapper)
        return d
    except Exception as exp:
        alog.error(exp)


def extend_cfg(cfg):
    cfg['prj_dir'] = os.path.abspath(os.path.join(IMPLEMENT_PATH, cfg['top_module'])).replace('\\', '/')
    cfg['prj_name'] = os.path.join(cfg['prj_dir'], cfg['top_module']).replace('\\', '/')
    cfg['prj_script'] = os.path.abspath(os.path.join(cfg['prj_dir'], cfg['top_module'] + '.tcl')).replace('\\', '/')
    cfg['syn_netlist'] = os.path.abspath(os.path.join(SYNTHESIS_PATH, cfg['top_module'], cfg['top_module'] + '.edf')).replace('\\', '/')
    cfg['syn_constraint'] = os.path.abspath(os.path.join(SYNTHESIS_PATH, cfg['top_module'], 'synplicity.ucf')).replace('\\', '/')
    cfg['prj_gui_file'] = os.path.abspath(os.path.join(cfg['prj_dir'], cfg['top_module'] + '.xise')).replace('\\', '/')
    cfg['bit_file'] = os.path.abspath(os.path.join(cfg['prj_dir'], cfg['top_module'] + '.bit')).replace('\\', '/')


def run(cfg):
    cfg = copy.deepcopy(cfg)
    extend_cfg(cfg)
    clean(cfg)
    mk_dir(cfg)
    mk_script(cfg)
    run_tool(cfg)