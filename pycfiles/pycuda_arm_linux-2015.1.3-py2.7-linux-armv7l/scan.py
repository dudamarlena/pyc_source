# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-armv7l/egg/pycuda/scan.py
# Compiled at: 2015-06-16 13:16:13
"""Scan primitive."""
from __future__ import division
from __future__ import absolute_import
import six
__copyright__ = '\nCopyright 2011 Andreas Kloeckner\nCopyright 2008-2011 NVIDIA Corporation\n'
__license__ = '\nLicensed under the Apache License, Version 2.0 (the "License");\nyou may not use this file except in compliance with the License.\nYou may obtain a copy of the License at\n\n    http://www.apache.org/licenses/LICENSE-2.0\n\nUnless required by applicable law or agreed to in writing, software\ndistributed under the License is distributed on an "AS IS" BASIS,\nWITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.\nSee the License for the specific language governing permissions and\nlimitations under the License.\n\nDerived from thrust/detail/backend/cuda/detail/fast_scan.inl\nwithin the Thrust project, https://code.google.com/p/thrust/\n\nDirect browse link:\nhttps://code.google.com/p/thrust/source/browse/thrust/detail/backend/cuda/detail/fast_scan.inl\n'
import numpy as np, pycuda.driver as driver, pycuda.gpuarray as gpuarray
from pycuda.compiler import SourceModule
from pycuda.tools import dtype_to_ctype
import pycuda._mymako as mako
from pycuda._cluda import CLUDA_PREAMBLE
SHARED_PREAMBLE = CLUDA_PREAMBLE + '\n#define WG_SIZE ${wg_size}\n#define SCAN_EXPR(a, b) ${scan_expr}\n\n${preamble}\n\ntypedef ${scan_type} scan_type;\n'
SCAN_INTERVALS_SOURCE = mako.template.Template(SHARED_PREAMBLE + '//CL//\n#define K ${wg_seq_batches}\n\n<%def name="make_group_scan(name, with_bounds_check)">\n    WITHIN_KERNEL\n    void ${name}(LOCAL_MEM_ARG scan_type *array\n    % if with_bounds_check:\n      , const unsigned n\n    % endif\n    )\n    {\n        scan_type val = array[LID_0];\n\n        <% offset = 1 %>\n\n        % while offset <= wg_size:\n            if (LID_0 >= ${offset}\n            % if with_bounds_check:\n              && LID_0 < n\n            % endif\n            )\n            {\n                scan_type tmp = array[LID_0 - ${offset}];\n                val = SCAN_EXPR(tmp, val);\n            }\n\n            local_barrier();\n            array[LID_0] = val;\n            local_barrier();\n\n            <% offset *= 2 %>\n        % endwhile\n    }\n</%def>\n\n${make_group_scan("scan_group", False)}\n${make_group_scan("scan_group_n", True)}\n\nKERNEL\nREQD_WG_SIZE(WG_SIZE, 1, 1)\nvoid ${name_prefix}_scan_intervals(\n    GLOBAL_MEM scan_type *input,\n    const unsigned int N,\n    const unsigned int interval_size,\n    GLOBAL_MEM scan_type *output,\n    GLOBAL_MEM scan_type *group_results)\n{\n    // padded in WG_SIZE to avoid bank conflicts\n    // index K in first dimension used for carry storage\n    LOCAL_MEM scan_type ldata[K + 1][WG_SIZE + 1];\n\n    const unsigned int interval_begin = interval_size * GID_0;\n    const unsigned int interval_end   = min(interval_begin + interval_size, N);\n\n    const unsigned int unit_size  = K * WG_SIZE;\n\n    unsigned int unit_base = interval_begin;\n\n    %for is_tail in [False, True]:\n\n        %if not is_tail:\n            for(; unit_base + unit_size <= interval_end; unit_base += unit_size)\n        %else:\n            if (unit_base < interval_end)\n        %endif\n\n        {\n            // Algorithm: Each work group is responsible for one contiguous\n            // \'interval\', of which there are just enough to fill all compute\n            // units.  Intervals are split into \'units\'. A unit is what gets\n            // worked on in parallel by one work group.\n\n            // Each unit has two axes--the local-id axis and the k axis.\n            //\n            // * * * * * * * * * * ----> lid\n            // * * * * * * * * * *\n            // * * * * * * * * * *\n            // * * * * * * * * * *\n            // * * * * * * * * * *\n            // |\n            // v k\n\n            // This is a three-phase algorithm, in which first each interval\n            // does its local scan, then a scan across intervals exchanges data\n            // globally, and the final update adds the exchanged sums to each\n            // interval.\n\n            // Exclusive scan is realized by performing a right-shift inside\n            // the final update.\n\n            // read a unit\'s worth of data from global\n\n            for(unsigned int k = 0; k < K; k++)\n            {\n                const unsigned int offset = k*WG_SIZE + LID_0;\n\n                %if is_tail:\n                if (unit_base + offset < interval_end)\n                %endif\n                {\n                    ldata[offset % K][offset / K] = input[unit_base + offset];\n                }\n            }\n\n            // carry in from previous unit, if applicable.\n            if (LID_0 == 0 && unit_base != interval_begin)\n                ldata[0][0] = SCAN_EXPR(ldata[K][WG_SIZE - 1], ldata[0][0]);\n\n            local_barrier();\n\n            // scan along k (sequentially in each work item)\n            scan_type sum = ldata[0][LID_0];\n\n            %if is_tail:\n                const unsigned int offset_end = interval_end - unit_base;\n            %endif\n\n            for(unsigned int k = 1; k < K; k++)\n            {\n                %if is_tail:\n                if (K * LID_0 + k < offset_end)\n                %endif\n                {\n                    scan_type tmp = ldata[k][LID_0];\n                    sum = SCAN_EXPR(sum, tmp);\n                    ldata[k][LID_0] = sum;\n                }\n            }\n\n            // store carry in out-of-bounds (padding) array entry in the K direction\n            ldata[K][LID_0] = sum;\n            local_barrier();\n\n            // tree-based parallel scan along local id\n            %if not is_tail:\n                scan_group(&ldata[K][0]);\n            %else:\n                scan_group_n(&ldata[K][0], offset_end / K);\n            %endif\n\n            // update local values\n            if (LID_0 > 0)\n            {\n                sum = ldata[K][LID_0 - 1];\n\n                for(unsigned int k = 0; k < K; k++)\n                {\n                    %if is_tail:\n                    if (K * LID_0 + k < offset_end)\n                    %endif\n                    {\n                        scan_type tmp = ldata[k][LID_0];\n                        ldata[k][LID_0] = SCAN_EXPR(sum, tmp);\n                    }\n                }\n            }\n\n            local_barrier();\n\n            // write data\n            for(unsigned int k = 0; k < K; k++)\n            {\n                const unsigned int offset = k*WG_SIZE + LID_0;\n\n                %if is_tail:\n                if (unit_base + offset < interval_end)\n                %endif\n                {\n                    output[unit_base + offset] = ldata[offset % K][offset / K];\n                }\n            }\n\n            local_barrier();\n        }\n\n    % endfor\n\n    // write interval sum\n    if (LID_0 == 0)\n    {\n        group_results[GID_0] = output[interval_end - 1];\n    }\n}\n')
INCLUSIVE_UPDATE_SOURCE = mako.template.Template(SHARED_PREAMBLE + '//CL//\nKERNEL\nREQD_WG_SIZE(WG_SIZE, 1, 1)\nvoid ${name_prefix}_final_update(\n    GLOBAL_MEM scan_type *output,\n    const unsigned int N,\n    const unsigned int interval_size,\n    GLOBAL_MEM scan_type *group_results)\n{\n    const unsigned int interval_begin = interval_size * GID_0;\n    const unsigned int interval_end   = min(interval_begin + interval_size, N);\n\n    if (GID_0 == 0)\n        return;\n\n    // value to add to this segment\n    scan_type prev_group_sum = group_results[GID_0 - 1];\n\n    // advance result pointer\n    output += interval_begin + LID_0;\n\n    for(unsigned int unit_base = interval_begin;\n        unit_base < interval_end;\n        unit_base += WG_SIZE, output += WG_SIZE)\n    {\n        const unsigned int i = unit_base + LID_0;\n\n        if(i < interval_end)\n        {\n            *output = SCAN_EXPR(prev_group_sum, *output);\n        }\n    }\n}\n')
EXCLUSIVE_UPDATE_SOURCE = mako.template.Template(SHARED_PREAMBLE + '//CL//\nKERNEL\nREQD_WG_SIZE(WG_SIZE, 1, 1)\nvoid ${name_prefix}_final_update(\n    GLOBAL_MEM scan_type *output,\n    const unsigned int N,\n    const unsigned int interval_size,\n    GLOBAL_MEM scan_type *group_results)\n{\n    LOCAL_MEM scan_type ldata[WG_SIZE];\n\n    const unsigned int interval_begin = interval_size * GID_0;\n    const unsigned int interval_end   = min(interval_begin + interval_size, N);\n\n    // value to add to this segment\n    scan_type carry = ${neutral};\n    if(GID_0 != 0)\n    {\n        scan_type tmp = group_results[GID_0 - 1];\n        carry = SCAN_EXPR(carry, tmp);\n    }\n\n    scan_type val = carry;\n\n    // advance result pointer\n    output += interval_begin + LID_0;\n\n    for (unsigned int unit_base = interval_begin;\n        unit_base < interval_end;\n        unit_base += WG_SIZE, output += WG_SIZE)\n    {\n        const unsigned int i = unit_base + LID_0;\n\n        if(i < interval_end)\n        {\n            scan_type tmp = *output;\n            ldata[LID_0] = SCAN_EXPR(carry, tmp);\n        }\n\n        local_barrier();\n\n        if (LID_0 != 0)\n            val = ldata[LID_0 - 1];\n        /*\n        else (see above)\n            val = carry OR last tail;\n        */\n\n        if (i < interval_end)\n            *output = val;\n\n        if(LID_0 == 0)\n            val = ldata[WG_SIZE - 1];\n\n        local_barrier();\n    }\n}\n')

class _ScanKernelBase(object):

    def __init__(self, dtype, scan_expr, neutral=None, name_prefix='scan', options=[], preamble='', devices=None):
        if isinstance(self, ExclusiveScanKernel) and neutral is None:
            raise ValueError('neutral element is required for exclusive scan')
        dtype = self.dtype = np.dtype(dtype)
        self.neutral = neutral
        self.scan_wg_size = 128
        self.update_wg_size = 256
        self.scan_wg_seq_batches = 6
        kw_values = dict(preamble=preamble, name_prefix=name_prefix, scan_type=dtype_to_ctype(dtype), scan_expr=scan_expr, neutral=neutral)
        scan_intervals_src = str(SCAN_INTERVALS_SOURCE.render(wg_size=self.scan_wg_size, wg_seq_batches=self.scan_wg_seq_batches, **kw_values))
        scan_intervals_prg = SourceModule(scan_intervals_src, options=options, no_extern_c=True)
        self.scan_intervals_knl = scan_intervals_prg.get_function(name_prefix + '_scan_intervals')
        self.scan_intervals_knl.prepare('PIIPP')
        final_update_src = str(self.final_update_tp.render(wg_size=self.update_wg_size, **kw_values))
        final_update_prg = SourceModule(final_update_src, options=options, no_extern_c=True)
        self.final_update_knl = final_update_prg.get_function(name_prefix + '_final_update')
        self.final_update_knl.prepare('PIIP')
        return

    def __call__(self, input_ary, output_ary=None, allocator=None, stream=None):
        allocator = allocator or input_ary.allocator
        if output_ary is None:
            output_ary = input_ary
        if isinstance(output_ary, (str, six.text_type)) and output_ary == 'new':
            output_ary = gpuarray.empty_like(input_ary, allocator=allocator)
        if input_ary.shape != output_ary.shape:
            raise ValueError('input and output must have the same shape')
        if not input_ary.flags.forc:
            raise RuntimeError('ScanKernel cannot deal with non-contiguous arrays')
        n, = input_ary.shape
        if not n:
            return output_ary
        else:
            unit_size = self.scan_wg_size * self.scan_wg_seq_batches
            dev = driver.Context.get_device()
            max_groups = 3 * dev.get_attribute(driver.device_attribute.MULTIPROCESSOR_COUNT)
            from pytools import uniform_interval_splitting
            interval_size, num_groups = uniform_interval_splitting(n, unit_size, max_groups)
            block_results = allocator(self.dtype.itemsize * num_groups)
            dummy_results = allocator(self.dtype.itemsize)
            self.scan_intervals_knl.prepared_async_call((
             num_groups, 1), (self.scan_wg_size, 1, 1), stream, input_ary.gpudata, n, interval_size, output_ary.gpudata, block_results)
            self.scan_intervals_knl.prepared_async_call((1, 1), (self.scan_wg_size, 1, 1), stream, block_results, num_groups, interval_size, block_results, dummy_results)
            self.final_update_knl.prepared_async_call((
             num_groups, 1), (self.update_wg_size, 1, 1), stream, output_ary.gpudata, n, interval_size, block_results)
            return output_ary


class InclusiveScanKernel(_ScanKernelBase):
    final_update_tp = INCLUSIVE_UPDATE_SOURCE


class ExclusiveScanKernel(_ScanKernelBase):
    final_update_tp = EXCLUSIVE_UPDATE_SOURCE