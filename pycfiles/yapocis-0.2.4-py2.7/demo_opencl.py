# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.4-x86_64/egg/yapocis/examples/demo_opencl.py
# Compiled at: 2011-08-30 23:33:15
import pyopencl as cl, numpy, numpy.linalg as la, time
a = numpy.random.rand(50000).astype(numpy.float32)
b = numpy.random.rand(50000).astype(numpy.float32)
ctx = cl.create_some_context()
queue = cl.CommandQueue(ctx)
t = time.time()
mf = cl.mem_flags
a_buf = cl.Buffer(ctx, mf.READ_ONLY | mf.COPY_HOST_PTR, hostbuf=a)
b_buf = cl.Buffer(ctx, mf.READ_ONLY | mf.COPY_HOST_PTR, hostbuf=b)
dest_buf = cl.Buffer(ctx, mf.WRITE_ONLY, b.nbytes)
prg = cl.Program(ctx, '\n    __kernel void sum(__global const float *a,\n    __global const float *b, __global float *c)\n    {\n      int gid = get_global_id(0);\n      c[gid] = a[gid] + b[gid];\n    }\n    ').build()
prg.sum(queue, a.shape, None, a_buf, b_buf, dest_buf)
a_plus_b = numpy.empty_like(a)
cl.enqueue_copy(queue, a_plus_b, dest_buf)
print (
 la.norm(a_plus_b - (a + b)), la.norm(a_plus_b))
print 'Elapsed:', time.time() - t