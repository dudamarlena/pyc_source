# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/soda/codegen/intel/ocl_kernel.py
# Compiled at: 2020-05-08 13:24:17
# Size of source mod 2**32: 7566 bytes
import collections, logging
from typing import Dict, List, TextIO
from haoda import ir, util
from soda import core
_logger = logging.getLogger().getChild(__name__)

def print_code(stencil: core.Stencil, output_file: TextIO) -> None:
    """Prints the top-level code with the given arguments.

  Prints the OpenCL kernels with proper pragmas and channel declarations and
  references.

  Args:
    stencil: Stencil object to print.
    output_file: TextIO to write to.
  """
    _logger.info('generate kernel code as %s' % output_file.name)
    printer = util.CppPrinter(output_file)
    println = printer.println
    println('#include <ihc_apint.h>', indent=0)
    println()
    println('#pragma OPENCL EXTENSION cl_intel_channels : enable', indent=0)
    println()
    super_source = stencil.dataflow_super_source
    for node in super_source.tpo_valid_node_gen():
        for fifo in node.fifos:
            println(f"channel {fifo.cl_type} {fifo.cl_expr};")

    println()
    width = len(str(sum(1 for _ in super_source.tpo_valid_node_gen()) - 1))
    instance_idx = collections.defaultdict(int)
    overall_idx = 0
    for node in super_source.tpo_valid_node_gen():
        module_trait, module_trait_id = super_source.module_table[node]
        print_kernel(f"{stencil.app_name}_{overall_idx:0{width}}_module_{module_trait_id}_instance_{instance_idx[module_trait_id]}",
          printer,
          node,
          module_trait,
          module_trait_id,
          burst_width=(stencil.burst_width))
        instance_idx[module_trait_id] += 1
        overall_idx += 1
        println()


def print_kernel(name: str, printer: util.Printer, node: ir.Module, module_trait: ir.ModuleTrait, module_trait_id: int, burst_width: int=256) -> None:
    if node.dram_reads:
        if node.dram_writes:
            raise ValueError('cannot read and write DRAM in the same module')
    else:
        println = printer.println
        for port, arg in zip(module_trait.loads, node.input_fifos):
            println('//  input <{0.cl_type}> <- {1}'.format(port, arg))

        for expr, arg in zip(module_trait.exprs, node.output_fifos):
            println('// output <{}> -> {}'.format(expr.cl_type, arg))

        printer.println('__kernel')
        kernel_attrs = ['reqd_work_group_size(1, 1, 1)', 'max_global_work_dim(0)']

        def print_kernel_attrs():
            for attr in kernel_attrs:
                println('__attribute(({}))'.format(attr))

        if node.dram_reads or node.dram_writes:
            params = ['__global {} {}* restrict {}'.format('__attribute((buffer_location("HBM{}")))'.format(bank), dram_ref.haoda_type.get_cl_vec_type(burst_width), util.get_port_name(dram_ref.var, bank)) for dram_ref, bank in node.dram_reads or node.dram_writes]
            params.append('ulong coalesced_data_num')
            kernel_attrs.append('uses_global_work_offset(0)')
            print_kernel_attrs()
            printer.print_func(name=('void {}'.format(name)), params=params, align=0)
        else:
            kernel_attrs.append('autorun')
            print_kernel_attrs()
            println('void {}()'.format(name))
        printer.do_scope(name)

        def get_delays(obj: ir.Node, delays: List[ir.DelayedRef]) -> ir.Node:
            if isinstance(obj, ir.DelayedRef):
                delays.append(obj)
            return obj

        delays = []
        for let in module_trait.lets:
            let.visit(get_delays, delays)

        for expr in module_trait.exprs:
            expr.visit(get_delays, delays)

        _logger.debug('delays: %s', delays)
        for delay in delays:
            println(delay.cl_buf_decl)
            println(delay.cl_ptr_decl)

        def mutate_dram_ref(obj, kwargs):
            if isinstance(obj, ir.DRAMRef):
                dram_throughput = len(obj.dram) * burst_width // obj.width_in_bits
                if node.dram_reads:
                    output_count = len({x[0].var for x in node.dram_reads})
                    fifo_throughput = len(node.output_fifos) // output_count
                else:
                    input_count = len({x[0].var for x in node.dram_writes})
                    fifo_throughput = len(node.input_fifos) // input_count
                if dram_throughput != fifo_throughput:
                    raise NotImplementedError(f"memory throughput {dram_throughput} != processing throughput {fifo_throughput}")
                coalescing_idx = kwargs['coalescing_idx']
                unroll_factor = kwargs['unroll_factor']
                elem_idx = coalescing_idx * unroll_factor + obj.offset
                return ir.Var(name='{buf}[{idx}]'.format(buf=(obj.dram_buf_name(obj.dram[(elem_idx % len(obj.dram))])),
                  idx=(elem_idx // len(obj.dram))),
                  idx=())
            else:
                if isinstance(obj, ir.Let) and isinstance(obj.name, ir.DRAMRef):
                    return ir.Var(name=('{} = {};'.format(obj.name.visit(mutate_dram_ref, kwargs), obj.expr.cl_expr)),
                      idx=())
                return obj

        if node.dram_reads or node.dram_writes:
            loop_args = ('ulong i = 0', 'i < coalesced_data_num', '++i')
        else:
            loop_args = ('', '', '')
    if delays:
        println('#pragma ivdep', indent=0)
    with (printer.for_)(*loop_args):
        for delay in delays:
            println('const {} {};'.format(delay.cl_type, delay.c_buf_load))

        for dram_ref, bank in node.dram_reads:
            println('{gentype} {buf}[{n}];'.format(gentype=(dram_ref.cl_type),
              n=(burst_width // dram_ref.width_in_bits),
              buf=(dram_ref.dram_buf_name(bank))))

        for dram_ref, bank in node.dram_reads:
            println('vstore{n}({vec_ptr}[i], 0, {buf});'.format(vec_ptr=(util.get_port_name(dram_ref.var, bank)),
              n=(burst_width // dram_ref.width_in_bits),
              buf=(dram_ref.dram_buf_name(bank))))

        for port, arg in zip(module_trait.loads, node.input_fifos):
            println('{0.cl_type} {0.ref_name} = read_channel_intel({1});'.format(port, arg))

        for dram_ref, bank in node.dram_writes:
            n = burst_width // dram_ref.width_in_bits
            buf = dram_ref.dram_buf_name(bank)
            println('{gentype} {buf}[{n}];'.format(gentype=(dram_ref.cl_type),
              n=n,
              buf=buf))

        mutate_kwargs = {'coalescing_idx':0, 
         'unroll_factor':len(node.input_fifos) or len(node.output_fifos)}
        for let in module_trait.lets:
            println(let.visit(mutate_dram_ref, mutate_kwargs).cl_expr)

        for expr, arg in zip(module_trait.exprs, node.output_fifos):
            println('write_channel_intel({}, {});'.format(arg, expr.visit(mutate_dram_ref, mutate_kwargs).cl_expr))

        for delay in delays:
            println(delay.c_buf_store)
            println('{} = {};'.format(delay.ptr, delay.cl_next_ptr_expr))

        for dram_ref, bank in node.dram_writes:
            println('{vec_ptr}[i] = vload{n}(0, {buf});'.format(vec_ptr=(util.get_port_name(dram_ref.var, bank)),
              n=(burst_width // dram_ref.width_in_bits),
              buf=(dram_ref.dram_buf_name(bank))))

    printer.un_scope()
    _logger.debug('printing: %s', module_trait)