# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/soda/codegen/xilinx/opencl.py
# Compiled at: 2020-04-29 14:13:41
# Size of source mod 2**32: 4780 bytes
import os, shutil, sys, tempfile
from soda.codegen.xilinx import header
from soda.codegen.xilinx import host
from soda.codegen.xilinx import hls_kernel as kernel
from soda.codegen.xilinx import rtl_kernel

def add_arguments(parser):
    parser.add_argument('--xocl',
      type=str, dest='output_dir', metavar='dir', nargs='?', const='', help='directory to generate kernel and host code; default names areused; default to the current working directory; may be overridden by --xocl-header, --xocl-host, or --xocl-kernel')
    parser.add_argument('--xocl-header',
      type=str, dest='header_file', metavar='file', help='host C++ header code; overrides --xocl')
    parser.add_argument('--xocl-host',
      type=str, dest='host_file', metavar='file', help='host C++ source code for the Xilinx OpenCL flow; overrides --xocl')
    parser.add_argument('--xocl-kernel',
      type=str, dest='kernel_file', metavar='file', help='Vivado HLS C++ kernel code for the Xilinx OpenCL flow; overrides --xocl')
    parser.add_argument('--xocl-platform',
      type=str, dest='xocl_platform', metavar='dir', help='SDAccel platform directory of the Xilinx OpenCL flow')
    parser.add_argument('--xocl-hw-xo', type=str, dest='xo_file', metavar='file', help='hardware object file for the Xilinx OpenCL flow')
    parser.add_argument('--xocl-hw-xo-rpt',
      type=str, dest='xo_rpt', metavar='file', help='Vivado HLS report for the Xilinx OpenCL hardware object')
    parser.add_argument('--xocl-interface',
      type=str, dest='interface', metavar='(m_axi|axis)', default='m_axi',
      help='interface type of the Xilinx OpenCL hardware object')


def print_code(stencil, args):
    if args.kernel_file is not None:
        with tempfile.TemporaryFile(mode='w+') as (tmp):
            kernel.print_code(stencil, tmp)
            tmp.seek(0)
            if args.kernel_file == '-':
                shutil.copyfileobj(tmp, sys.stdout)
            else:
                with open(args.kernel_file, 'w') as (kernel_file):
                    shutil.copyfileobj(tmp, kernel_file)
    elif args.host_file is not None:
        with tempfile.TemporaryFile(mode='w+') as (tmp):
            host.print_code(stencil, tmp)
            tmp.seek(0)
            if args.host_file == '-':
                shutil.copyfileobj(tmp, sys.stdout)
            else:
                with open(args.host_file, 'w') as (host_file):
                    shutil.copyfileobj(tmp, host_file)
    else:
        if args.header_file is not None:
            with tempfile.TemporaryFile(mode='w+') as (tmp):
                header.print_code(stencil, tmp)
                tmp.seek(0)
                if args.header_file == '-':
                    shutil.copyfileobj(tmp, sys.stdout)
                else:
                    with open(args.header_file, 'w') as (header_file):
                        shutil.copyfileobj(tmp, header_file)
        if args.xo_file is not None:
            with tempfile.TemporaryFile(mode='w+b') as (tmp):
                rtl_kernel.print_code(stencil, tmp, platform=(args.xocl_platform), rpt_file=(args.xo_rpt),
                  interface=(args.interface))
                tmp.seek(0)
                if args.xo_file == '-':
                    shutil.copyfileobj(tmp, sys.stdout)
                else:
                    with open(args.xo_file, 'wb') as (xo_file):
                        shutil.copyfileobj(tmp, xo_file)
        if args.output_dir is not None:
            if args.kernel_file is None or args.host_file is None or args.header_file is None:
                if args.kernel_file is None:
                    dram_in = args.dram_in if args.dram_in else '_'
                    dram_out = args.dram_out if args.dram_out else '_'
                    kernel_file_name = os.path.join(args.output_dir, '%s_kernel-tile%s-unroll%d-ddr%s.cpp' % (
                     stencil.app_name,
                     'x'.join('%d' % x for x in stencil.tile_size[:-1]),
                     stencil.unroll_factor, dram_in + '-' + dram_out))
                else:
                    kernel_file_name = args.kernel_file
                with tempfile.TemporaryFile(mode='w+') as (tmp):
                    kernel.print_code(stencil, tmp)
                    tmp.seek(0)
                    with open(kernel_file_name, 'w') as (kernel_file):
                        shutil.copyfileobj(tmp, kernel_file)
                if args.host_file is None:
                    host_file_name = os.path.join(args.output_dir, stencil.app_name + '.cpp')
                else:
                    host_file_name = args.host_file
                with tempfile.TemporaryFile(mode='w+') as (tmp):
                    host.print_code(stencil, tmp)
                    tmp.seek(0)
                    with open(host_file_name, 'w') as (host_file):
                        shutil.copyfileobj(tmp, kernel_file)
                if args.header_file is None:
                    header_file_name = os.path.join(args.output_dir, stencil.app_name + '.h')
                else:
                    header_file_name = args.header_file
                with tempfile.TemporaryFile(mode='w+') as (tmp):
                    header.print_code(stencil, tmp)
                    tmp.seek(0)
                    with open(header_file_name, 'w') as (header_file):
                        shutil.copyfileobj(tmp, header_file)