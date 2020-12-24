# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/haoda/backend/xilinx.py
# Compiled at: 2020-04-26 02:44:08
# Size of source mod 2**32: 25611 bytes
import collections, contextlib, glob, logging, os, subprocess, tarfile, tempfile, xml.etree.ElementTree as ET, xml.sax.saxutils, zipfile
from typing import BinaryIO, Iterable, Iterator, Mapping, Optional, TextIO, Tuple, Union
from haoda import util
from haoda.backend.common import Arg, Cat
_logger = logging.getLogger().getChild(__name__)

class Vivado(subprocess.Popen):
    __doc__ = 'Call vivado with the given Tcl commands and arguments.\n\n  This is a subclass of subprocess.Popen. A temporary directory will be created\n  and used as the working directory.\n\n  Args:\n    commands: A string of Tcl commands.\n    args: Iterable of strings as arguments to the Tcl commands.\n  '

    def __init__(self, commands, *args):
        self.cwd = tempfile.TemporaryDirectory(prefix='vivado-')
        with open((os.path.join(self.cwd.name, 'commands.tcl')), mode='w+') as (tcl_file):
            tcl_file.write(commands)
        cmd_args = [
         'vivado', '-mode', 'batch', '-source', tcl_file.name, '-nojournal',
          '-tclargs', *args]
        pipe_args = {'stdout':subprocess.PIPE, 
         'stderr':subprocess.PIPE}
        (super().__init__)(cmd_args, cwd=self.cwd.name, **pipe_args)

    def __exit__(self, *args):
        (super().__exit__)(*args)
        self.cwd.cleanup()


class VivadoHls(subprocess.Popen):
    __doc__ = 'Call vivado_hls with the given Tcl commands.\n\n  This is a subclass of subprocess.Popen. A temporary directory will be created\n  and used as the working directory.\n\n  Args:\n    commands: A string of Tcl commands.\n  '

    def __init__(self, commands):
        self.cwd = tempfile.TemporaryDirectory(prefix='vivado-hls-')
        with open((os.path.join(self.cwd.name, 'commands.tcl')), mode='w+') as (tcl_file):
            tcl_file.write(commands)
        cmd_args = [
         'vivado_hls', '-f', tcl_file.name]
        pipe_args = {'stdout':subprocess.PIPE,  'stderr':subprocess.PIPE}
        (super().__init__)(cmd_args, cwd=self.cwd.name, **pipe_args)

    def __exit__(self, *args):
        (super().__exit__)(*args)
        self.cwd.cleanup()


PACKAGEXO_COMMANDS = '\nset tmp_ip_dir "{tmpdir}/tmp_ip_dir"\nset tmp_project "{tmpdir}/tmp_project"\n\ncreate_project -force kernel_pack ${{tmp_project}}\nadd_files -norecurse [glob {hdl_dir}/*.v]\nforeach tcl_file [glob -nocomplain {hdl_dir}/*.tcl] {{\n  source ${{tcl_file}}\n}}\nset_property top {top_name} [current_fileset]\nupdate_compile_order -fileset sources_1\nupdate_compile_order -fileset sim_1\nipx::package_project -root_dir ${{tmp_ip_dir}} -vendor haoda -library xrtl -taxonomy /KernelIP -import_files -set_current false\nipx::unload_core ${{tmp_ip_dir}}/component.xml\nipx::edit_ip_in_project -upgrade true -name tmp_edit_project -directory ${{tmp_ip_dir}} ${{tmp_ip_dir}}/component.xml\nset_property core_revision 2 [ipx::current_core]\nforeach up [ipx::get_user_parameters] {{\n  ipx::remove_user_parameter [get_property NAME ${{up}}] [ipx::current_core]\n}}\nset_property sdx_kernel true [ipx::current_core]\nset_property sdx_kernel_type rtl [ipx::current_core]\nipx::create_xgui_files [ipx::current_core]\n{bus_ifaces}\nset_property xpm_libraries {{XPM_CDC XPM_MEMORY XPM_FIFO}} [ipx::current_core]\nset_property supported_families {{ }} [ipx::current_core]\nset_property auto_family_support_level level_2 [ipx::current_core]\nipx::update_checksums [ipx::current_core]\nipx::save_core [ipx::current_core]\nclose_project -delete\n\npackage_xo -force -xo_path "{xo_file}" -kernel_name {top_name} -ip_directory ${{tmp_ip_dir}} -kernel_xml {kernel_xml}{cpp_kernels}\n'
BUS_IFACE = '\nipx::associate_bus_interfaces -busif {} -clock ap_clk [ipx::current_core]\n'
S_AXI_NAME = 's_axi_control'
M_AXI_PREFIX = 'm_axi_'

class PackageXo(Vivado):
    __doc__ = 'Packages the given files into a Xilinx hardware object.\n\n  This is a subclass of subprocess.Popen. A temporary directory will be created\n  and used as the working directory.\n\n  Args:\n    xo_file: Name of the generated xo file.\n    top_name: Top-level module name.\n    kernel_xml: Name of a xml file containing description of the kernel.\n    hdl_dir: Directory name containing all HDL files.\n    m_axi_names: Variable names connected to the m_axi bus.\n    iface_names: Other interface names, default to (S_AXI_NAME,).\n    cpp_kernels: File names of C++ kernels.\n  '

    def __init__(self, xo_file, top_name, kernel_xml, hdl_dir, m_axi_names=(), iface_names=(
 S_AXI_NAME,), cpp_kernels=()):
        self.tmpdir = tempfile.TemporaryDirectory(prefix='package-xo-')
        if _logger.isEnabledFor(logging.INFO):
            for _, _, files in os.walk(hdl_dir):
                for filename in files:
                    _logger.info('packing: %s', filename)

        iface_names = list(iface_names)
        iface_names.extend(M_AXI_PREFIX + x for x in m_axi_names)
        kwargs = {'top_name':top_name, 
         'kernel_xml':kernel_xml, 
         'hdl_dir':hdl_dir, 
         'xo_file':xo_file, 
         'bus_ifaces':''.join(map(BUS_IFACE.format, iface_names)), 
         'tmpdir':self.tmpdir.name, 
         'cpp_kernels':''.join(map(' -kernel_files {}'.format, cpp_kernels))}
        super().__init__((PACKAGEXO_COMMANDS.format)(**kwargs))

    def __exit__(self, *args):
        (super().__exit__)(*args)
        self.tmpdir.cleanup()


HLS_COMMANDS = '\ncd "{project_dir}"\nopen_project "{project_name}"\nset_top {top_name}\n{add_kernels}\nopen_solution "{solution_name}"\nset_part {{{part_num}}}\ncreate_clock -period {clock_period} -name default\nconfig_compile -name_max_length 253\nconfig_interface -m_axi_addr64\nconfig_rtl -disable_start_propagation -reset_level {reset_level}{auto_prefix}\ncsynth_design\nexit\n'

class RunHls(VivadoHls):
    __doc__ = 'Runs Vivado HLS for the given kernels and generate HDL files\n\n  This is a subclass of subprocess.Popen. A temporary directory will be created\n  and used as the working directory.\n\n  Args:\n    tarfileobj: File object that will contain the reports and HDL files.\n    kernel_files: File names or tuple of file names and cflags of the kernels.\n    top_name: Top-level module name.\n    clock_period: Target clock period.\n    part_num: Target part number.\n  '

    def __init__(self, tarfileobj, kernel_files, top_name, clock_period, part_num, reset_low=True, auto_prefix=False):
        self.project_dir = tempfile.TemporaryDirectory(prefix='run-hls-')
        self.project_name = 'project'
        self.solution_name = top_name
        self.tarfileobj = tarfileobj
        kernels = []
        for kernel_file in kernel_files:
            if isinstance(kernel_file, str):
                kernels.append('add_files "{}" -cflags "-std=c++11"'.format(kernel_file))
            else:
                kernels.append(('add_files "{}" -cflags "-std=c++11 {}"'.format)(*kernel_file))

        kwargs = {'project_dir':self.project_dir.name, 
         'project_name':self.project_name, 
         'solution_name':self.solution_name, 
         'top_name':top_name, 
         'add_kernels':'\n'.join(kernels), 
         'part_num':part_num, 
         'clock_period':clock_period, 
         'reset_level':'low' if reset_low else 'high', 
         'auto_prefix':' -auto_prefix' if auto_prefix else ''}
        super().__init__((HLS_COMMANDS.format)(**kwargs))

    def __exit__(self, *args):
        self.wait()
        if self.returncode == 0:
            with tarfile.open(mode='w', fileobj=(self.tarfileobj)) as (tar):
                solution_dir = os.path.join(self.project_dir.name, self.project_name, self.solution_name)
                try:
                    tar.add((os.path.join(solution_dir, 'syn/report')), arcname='report')
                    tar.add((os.path.join(solution_dir, 'syn/verilog')), arcname='hdl')
                    tar.add((os.path.join(solution_dir, self.cwd.name, 'vivado_hls.log')), arcname=('log/' + self.solution_name + '.log'))
                    for pattern in ('*.sched.adb.xml', '*.verbose.sched.rpt', '*.verbose.sched.rpt.xml'):
                        for f in glob.glob(os.path.join(solution_dir, '.autopilot', 'db', pattern)):
                            tar.add(f, arcname=('report/' + os.path.basename(f)))

                except FileNotFoundError as e:
                    self.returncode = 1
                    _logger.error('%s', e)

        (super().__exit__)(*args)
        self.project_dir.cleanup()


XILINX_XML_NS = {'xd': 'http://www.xilinx.com/xd'}

def get_device_info(platform_path: str):
    """Extract device part number and target frequency from SDAccel platform.

  Currently only support 5.x platforms.

  Args:
    platform_path: Path to the platform directory, e.g.,
        '/opt/xilinx/platforms/xilinx_u200_qdma_201830_2'.

  Raises:
    ValueError: If cannot parse the platform properly.
  """
    device_name = os.path.basename(platform_path)
    try:
        platform_file = next(glob.iglob(os.path.join(glob.escape(platform_path), 'hw', '*.[xd]sa')))
    except StopIteration as e:
        raise ValueError('cannot find platform file for %s' % device_name) from e

    with zipfile.ZipFile(platform_file) as (platform):
        with platform.open(os.path.basename(platform_file)[:-4] + '.hpfm') as (metadata):
            platform_info = ET.parse(metadata).find('./xd:component/xd:platformInfo', XILINX_XML_NS)
            if platform_info is None:
                raise ValueError('cannot parse platform')
            clock_period = platform_info.find("./xd:systemClocks/xd:clock/[@xd:id='0']", XILINX_XML_NS)
            if clock_period is None:
                raise ValueError('cannot find clock period in platform')
            part_num = platform_info.find('xd:deviceInfo', XILINX_XML_NS)
            if part_num is None:
                raise ValueError('cannot find part number in platform')
            return {'clock_period':clock_period.attrib[('{{{xd}}}period'.format)(**XILINX_XML_NS)], 
             'part_num':part_num.attrib[('{{{xd}}}name'.format)(**XILINX_XML_NS)]}


KERNEL_XML_TEMPLATE = '\n<?xml version="1.0" encoding="UTF-8"?>\n<root versionMajor="1" versionMinor="6">\n  <kernel name="{name}" language="ip_c" vlnv="haoda:xrtl:{name}:1.0" attributes="" preferredWorkGroupSizeMultiple="0" workGroupSize="1" interrupt="true" hwControlProtocol="ap_ctrl_hs">\n    <ports>{ports}\n    </ports>\n    <args>{args}\n    </args>\n  </kernel>\n</root>\n'
S_AXI_PORT = f'\n      <port name="{S_AXI_NAME}" mode="slave" range="0x1000" dataWidth="32" portType="addressable" base="0x0"/>\n'
M_AXI_PORT_TEMPLATE = f'\n      <port name="{M_AXI_PREFIX}{{name}}" mode="master" range="0xFFFFFFFFFFFFFFFF" dataWidth="{{width}}" portType="addressable" base="0x0"/>\n'
AXIS_PORT_TEMPLATE = '\n      <port name="{name}" mode="{mode}" dataWidth="{width}" portType="stream"/>\n'
ARG_TEMPLATE = '\n      <arg name="{name}" addressQualifier="{addr_qualifier}" id="{arg_id}" port="{port_name}" size="{size:#x}" offset="{offset:#x}" hostOffset="0x0" hostSize="{host_size:#x}" type="{c_type}"/>\n'

def print_kernel_xml(name: str, args: Iterable[Arg], kernel_xml: TextIO):
    """Generate kernel.xml file.

  Args:
    top_name: Name of the kernel.
    args: Iterable of Arg. The `port` field should not include any prefix and
        could be an empty string to connect the argument to a default port.
    kernel_xml: File object to write to.
  """
    kernel_ports = S_AXI_PORT.rstrip('\n')
    kernel_args = ''
    offset = 16
    for arg_id, arg in enumerate(args):
        if arg.cat == Cat.SCALAR:
            addr_qualifier = 0
            host_size = arg.width // 8
            size = max(4, host_size)
            port_name = arg.port or S_AXI_NAME
        else:
            if arg.cat == Cat.MMAP:
                addr_qualifier = 1
                size = host_size = 8
                port_name = M_AXI_PREFIX + (arg.port or arg.name)
                kernel_ports += M_AXI_PORT_TEMPLATE.format(name=(arg.port or arg.name), width=(arg.width)).rstrip('\n')
            else:
                if arg.cat in {Cat.ISTREAM, Cat.OSTREAM}:
                    addr_qualifier = 4
                    size = host_size = 8
                    port_name = arg.port or arg.name
                    mode = 'read_only' if arg.cat == Cat.ISTREAM else 'write_only'
                    kernel_ports += AXIS_PORT_TEMPLATE.format(name=(arg.name), mode=mode,
                      width=(arg.width))
                else:
                    raise NotImplementedError(f"unknown arg category: {arg.cat}")
        kernel_args += ARG_TEMPLATE.format(name=(arg.name), addr_qualifier=addr_qualifier,
          arg_id=arg_id,
          port_name=port_name,
          c_type=(xml.sax.saxutils.escape(arg.ctype)),
          size=size,
          offset=offset,
          host_size=host_size).rstrip('\n')
        offset += size + 4

    kernel_xml.write(KERNEL_XML_TEMPLATE.format(name=name, ports=kernel_ports,
      args=kernel_args))


BRAM_FIFO_TEMPLATE = '`default_nettype none\n\n// first-word fall-through (FWFT) FIFO using block RAM\n// based on HLS generated code\nmodule {name} #(\n  parameter MEM_STYLE  = "block",\n  parameter DATA_WIDTH = {width},\n  parameter ADDR_WIDTH = {addr_width},\n  parameter DEPTH      = {depth}\n) (\n  input wire clk,\n  input wire reset,\n\n  // write\n  output wire                  if_full_n,\n  input  wire                  if_write_ce,\n  input  wire                  if_write,\n  input  wire [DATA_WIDTH-1:0] if_din,\n\n  // read\n  output wire                  if_empty_n,\n  input  wire                  if_read_ce,\n  input  wire                  if_read,\n  output wire [DATA_WIDTH-1:0] if_dout\n);\n\n(* ram_style = MEM_STYLE *)\nreg  [DATA_WIDTH-1:0] mem[0:DEPTH-1];\nreg  [DATA_WIDTH-1:0] q_buf;\nreg  [ADDR_WIDTH-1:0] waddr;\nreg  [ADDR_WIDTH-1:0] raddr;\nwire [ADDR_WIDTH-1:0] wnext;\nwire [ADDR_WIDTH-1:0] rnext;\nwire                  push;\nwire                  pop;\nreg  [ADDR_WIDTH-1:0] used;\nreg                   full_n;\nreg                   empty_n;\nreg  [DATA_WIDTH-1:0] q_tmp;\nreg                   show_ahead;\nreg  [DATA_WIDTH-1:0] dout_buf;\nreg                   dout_valid;\n\nlocalparam DepthM1 = DEPTH[ADDR_WIDTH-1:0] - 1\'d1;\n\nassign if_full_n  = full_n;\nassign if_empty_n = dout_valid;\nassign if_dout    = dout_buf;\nassign push       = full_n & if_write_ce & if_write;\nassign pop        = empty_n & if_read_ce & (~dout_valid | if_read);\nassign wnext      = !push              ? waddr              :\n                    (waddr == DepthM1) ? {{ADDR_WIDTH{{1\'b0}}}} : waddr + 1\'d1;\nassign rnext      = !pop               ? raddr              :\n                    (raddr == DepthM1) ? {{ADDR_WIDTH{{1\'b0}}}} : raddr + 1\'d1;\n\n// waddr\nalways @(posedge clk) begin\n  if (reset)\n    waddr <= {{ADDR_WIDTH{{1\'b0}}}};\n  else\n    waddr <= wnext;\nend\n\n// raddr\nalways @(posedge clk) begin\n  if (reset)\n    raddr <= {{ADDR_WIDTH{{1\'b0}}}};\n  else\n    raddr <= rnext;\nend\n\n// used\nalways @(posedge clk) begin\n  if (reset)\n    used <= {{ADDR_WIDTH{{1\'b0}}}};\n  else if (push && !pop)\n    used <= used + 1\'b1;\n  else if (!push && pop)\n    used <= used - 1\'b1;\nend\n\n// full_n\nalways @(posedge clk) begin\n  if (reset)\n    full_n <= 1\'b1;\n  else if (push && !pop)\n    full_n <= (used != DepthM1);\n  else if (!push && pop)\n    full_n <= 1\'b1;\nend\n\n// empty_n\nalways @(posedge clk) begin\n  if (reset)\n    empty_n <= 1\'b0;\n  else if (push && !pop)\n    empty_n <= 1\'b1;\n  else if (!push && pop)\n    empty_n <= (used != {{{{(ADDR_WIDTH-1){{1\'b0}}}},1\'b1}});\nend\n\n// mem\nalways @(posedge clk) begin\n  if (push)\n    mem[waddr] <= if_din;\nend\n\n// q_buf\nalways @(posedge clk) begin\n  q_buf <= mem[rnext];\nend\n\n// q_tmp\nalways @(posedge clk) begin\n  if (reset)\n    q_tmp <= {{DATA_WIDTH{{1\'b0}}}};\n  else if (push)\n    q_tmp <= if_din;\nend\n\n// show_ahead\nalways @(posedge clk) begin\n  if (reset)\n    show_ahead <= 1\'b0;\n  else if (push && used == {{{{(ADDR_WIDTH-1){{1\'b0}}}},pop}})\n    show_ahead <= 1\'b1;\n  else\n    show_ahead <= 1\'b0;\nend\n\n// dout_buf\nalways @(posedge clk) begin\n  if (reset)\n    dout_buf <= {{DATA_WIDTH{{1\'b0}}}};\n  else if (pop)\n    dout_buf <= show_ahead? q_tmp : q_buf;\nend\n\n// dout_valid\nalways @(posedge clk) begin\n  if (reset)\n    dout_valid <= 1\'b0;\n  else if (pop)\n    dout_valid <= 1\'b1;\n  else if (if_read_ce & if_read)\n    dout_valid <= 1\'b0;\nend\n\nendmodule  // fifo_bram\n\n`default_nettype wire\n'
SRL_FIFO_TEMPLATE = '`default_nettype none\n\n// first-word fall-through (FWFT) FIFO using shift register LUT\n// based on HLS generated code\nmodule {name} #(\n  parameter MEM_STYLE  = "shiftreg",\n  parameter DATA_WIDTH = {width},\n  parameter ADDR_WIDTH = {addr_width},\n  parameter DEPTH      = {depth}\n) (\n  input wire clk,\n  input wire reset,\n\n  // write\n  output wire                  if_full_n,\n  input  wire                  if_write_ce,\n  input  wire                  if_write,\n  input  wire [DATA_WIDTH-1:0] if_din,\n\n  // read\n  output wire                  if_empty_n,\n  input  wire                  if_read_ce,\n  input  wire                  if_read,\n  output wire [DATA_WIDTH-1:0] if_dout\n);\n\n  wire [ADDR_WIDTH - 1:0] shift_reg_addr;\n  wire [DATA_WIDTH - 1:0] shift_reg_data;\n  wire [DATA_WIDTH - 1:0] shift_reg_q;\n  wire                    shift_reg_ce;\n  reg  [ADDR_WIDTH:0]     out_ptr;\n  reg                     internal_empty_n;\n  reg                     internal_full_n;\n\n  reg [DATA_WIDTH-1:0] mem [0:DEPTH-1];\n\n  assign if_empty_n = internal_empty_n;\n  assign if_full_n = internal_full_n;\n  assign shift_reg_data = if_din;\n  assign if_dout = shift_reg_q;\n\n  assign shift_reg_addr = out_ptr[ADDR_WIDTH] == 1\'b0 ? out_ptr[ADDR_WIDTH-1:0] : {{ADDR_WIDTH{{1\'b0}}}};\n  assign shift_reg_ce = (if_write & if_write_ce) & internal_full_n;\n\n  assign shift_reg_q = mem[shift_reg_addr];\n\n  always @(posedge clk) begin\n    if (reset) begin\n      out_ptr <= ~{{ADDR_WIDTH+1{{1\'b0}}}};\n      internal_empty_n <= 1\'b0;\n      internal_full_n <= 1\'b1;\n    end else begin\n      if (((if_read && if_read_ce) && internal_empty_n) &&\n          (!(if_write && if_write_ce) || !internal_full_n)) begin\n        out_ptr <= out_ptr - 1\'b1;\n        if (out_ptr == {{(ADDR_WIDTH+1){{1\'b0}}}})\n          internal_empty_n <= 1\'b0;\n        internal_full_n <= 1\'b1;\n      end\n      else if (((if_read & if_read_ce) == 0 | internal_empty_n == 0) &&\n        ((if_write & if_write_ce) == 1 & internal_full_n == 1))\n      begin\n        out_ptr <= out_ptr + 1\'b1;\n        internal_empty_n <= 1\'b1;\n        if (out_ptr == DEPTH - {{{{(ADDR_WIDTH-1){{1\'b0}}}}, 2\'d2}})\n          internal_full_n <= 1\'b0;\n      end\n    end\n  end\n\n  integer i;\n  always @(posedge clk) begin\n    if (shift_reg_ce) begin\n      for (i = 0; i < DEPTH - 1; i = i + 1)\n        mem[i + 1] <= mem[i];\n      mem[0] <= shift_reg_data;\n    end\n  end\n\nendmodule  // fifo_srl\n\n`default_nettype wire\n'
AUTO_FIFO_TEMPLATE = '`default_nettype none\n\n// first-word fall-through (FWFT) FIFO\n// if its capacity > THRESHOLD bits, it uses block RAM, otherwise it will uses\n// shift register LUT\nmodule {name} #(\n  parameter DATA_WIDTH = 32,\n  parameter ADDR_WIDTH = 5,\n  parameter DEPTH      = 32,\n  parameter THRESHOLD  = 18432\n) (\n  input wire clk,\n  input wire reset,\n\n  // write\n  output wire                  if_full_n,\n  input  wire                  if_write_ce,\n  input  wire                  if_write,\n  input  wire [DATA_WIDTH-1:0] if_din,\n\n  // read\n  output wire                  if_empty_n,\n  input  wire                  if_read_ce,\n  input  wire                  if_read,\n  output wire [DATA_WIDTH-1:0] if_dout\n);\n\ngenerate\n  if (DATA_WIDTH * DEPTH > THRESHOLD) begin : bram\n    fifo_bram #(\n      .DATA_WIDTH(DATA_WIDTH),\n      .ADDR_WIDTH(ADDR_WIDTH),\n      .DEPTH     (DEPTH)\n    ) unit (\n      .clk  (clk),\n      .reset(reset),\n\n      .if_full_n  (if_full_n),\n      .if_write_ce(if_write_ce),\n      .if_write   (if_write),\n      .if_din     (if_din),\n\n      .if_empty_n(if_empty_n),\n      .if_read_ce(if_read_ce),\n      .if_read   (if_read),\n      .if_dout   (if_dout)\n    );\n  end else begin : srl\n    fifo_srl #(\n      .DATA_WIDTH(DATA_WIDTH),\n      .ADDR_WIDTH(ADDR_WIDTH),\n      .DEPTH     (DEPTH)\n    ) unit (\n      .clk  (clk),\n      .reset(reset),\n\n      .if_full_n  (if_full_n),\n      .if_write_ce(if_write_ce),\n      .if_write   (if_write),\n      .if_din     (if_din),\n\n      .if_empty_n(if_empty_n),\n      .if_read_ce(if_read_ce),\n      .if_read   (if_read),\n      .if_dout   (if_dout)\n    );\n  end\nendgenerate\n\nendmodule  // fifo\n\n`default_nettype wire\n'

class VerilogPrinter(util.Printer):
    __doc__ = 'A text-based Verilog printer.'

    def module(self, module_name: str, args: Iterable[str]) -> None:
        self.println('module %s (' % module_name)
        self.do_indent()
        self._out.write(' ' * self._indent * self._tab)
        self._out.write((',\n' + ' ' * self._indent * self._tab).join(args))
        self.un_indent()
        self.println('\n);')

    def endmodule(self, module_name: Optional[str]=None) -> None:
        if module_name is None:
            self.println('endmodule')
        else:
            self.println('endmodule // %s' % module_name)

    def begin(self) -> None:
        self.println('begin')
        self.do_indent()

    def end(self) -> None:
        self.un_indent()
        self.println('end')

    def parameter(self, key: str, value: str):
        self.println('parameter {} = {};'.format(key, value))

    @contextlib.contextmanager
    def initial(self) -> Iterator[None]:
        self.println('initial begin')
        self.do_indent()
        yield
        self.un_indent()
        self.println('end')

    @contextlib.contextmanager
    def always(self, condition: str) -> Iterator[None]:
        self.println('always @ (%s) begin' % condition)
        self.do_indent()
        yield
        self.un_indent()
        self.println('end')

    @contextlib.contextmanager
    def if_(self, condition: str) -> Iterator[None]:
        self.println('if (%s) begin' % condition)
        self.do_indent()
        yield
        self.end()

    def else_(self) -> None:
        self.un_indent()
        self.println('end else begin')
        self.do_indent()

    def module_instance(self, module_name: str, instance_name: str, args: Union[(Mapping[(str, str)], Iterable[str])]) -> None:
        self.println(('{module_name} {instance_name}('.format)(**locals()))
        self.do_indent()
        if isinstance(args, collections.Mapping):
            self._out.write(',\n'.join(' ' * self._indent * self._tab + ('.{}({})'.format)(*arg) for arg in args.items()))
        else:
            self._out.write(',\n'.join(' ' * self._indent * self._tab + arg for arg in args))
        self.un_indent()
        self.println('\n);')

    def fifo_module(self, width: int, depth: int, name: str='', threshold: int=1024) -> None:
        """Generate FIFO with the given parameters.

    Generate an FIFO module. If its capacity is larger than threshold, BRAM FIFO
        will be used. Otherwise, SRL FIFO will be used.

    Args:
      width: FIFO width.
      depth: FIFO depth.
      name: Optionally give the fifo a name, default to
          'fifo_w{width}_d{depth}_A'.
      threshold: Optionally give a threshold to decide whether to use BRAM or
          SRL. Defaults to 1024 bits.

    Raises:
      ValueError: If depth or width is invalid.
    """
        if width * depth > threshold:
            self.bram_fifo_module(width, depth)
        else:
            self.srl_fifo_module(width, depth)

    def bram_fifo_module(self, width: int, depth: int, name: str='') -> None:
        """Generate BRAM FIFO with the given parameters.

    Generate a BRAM FIFO module.

    Args:
      width: FIFO width.
      depth: FIFO depth.
      name: Optionally give the fifo a name, default to
          'fifo_w{width}_d{depth}_A'.

    Raises:
      ValueError: If depth or width is invalid.
    """
        if depth < 2:
            raise ValueError('Invalid BRAM FIFO depth: %d < 1' % depth)
        if not name:
            name = 'fifo_w{width}_d{depth}_A'.format(width=width, depth=depth)
        self._out.write(BRAM_FIFO_TEMPLATE.format(width=width, depth=depth,
          name=name,
          addr_width=((depth - 1).bit_length())))

    def srl_fifo_module(self, width: int, depth: int, name: str='') -> None:
        """Generate SRL FIFO with the given parameters.

    Generate a SRL FIFO module.

    Args:
      width: FIFO width.
      depth: FIFO depth.
      name: Optionally give the fifo a name, default to
          'fifo_w{width}_d{depth}_A'.

    Raises:
      ValueError: If depth or width is invalid.
    """
        if depth < 2:
            raise ValueError('Invalid SRL FIFO depth: %d < 1' % depth)
        if not name:
            name = 'fifo_w{width}_d{depth}_A'.format(width=width, depth=depth)
        addr_width = (depth - 1).bit_length()
        self._out.write(SRL_FIFO_TEMPLATE.format(width=width, depth=depth,
          name=name,
          addr_width=addr_width,
          depth_width=(addr_width + 1)))