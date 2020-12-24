# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/cjld/new_jittor/jittor/python/jittor/contrib.py
# Compiled at: 2020-03-24 04:19:25
# Size of source mod 2**32: 7297 bytes
import jittor as jt, numpy as np

def argmax_pool(x, size, stride, padding=0):
    y_shape = list(x.shape)
    y_shape[2] = (x.shape[2] + padding * 2 - size) // stride + 1
    y_shape[3] = (x.shape[3] + padding * 2 - size) // stride + 1
    y = jt.code(y_shape, (x.dtype), [x], cpu_src=f"\n            for (int i=0; i<outshape0; i++)\n            for (int j=0; j<outshape1; j++)\n            for (int k=0; k<outshape2; k++)\n            for (int l=0; l<outshape3; l++) {{\n                int kx=k*{stride}+{size}/2-{padding};\n                int ky=l*{stride}+{size}/2-{padding};\n                @out(i,j,k,l) = @in0(i,j,kx,ky);\n                for (int p=kx-{size}/2;p<=kx+{size}/2;p++)\n                for (int q=ky-{size}/2;q<=ky+{size}/2;q++)\n                    if (p>=0 && q>=0 && p<in0shape2 && q<in0shape3)\n                    if (@out(i,j,k,l) < @in0(i,j,p,q))\n                        @out(i,j,k,l) = @in0(i,j,p,q);\n            }}\n        ",
      cpu_grad_src=[
     f"\n            for (int i=0; i<outshape0; i++)\n            for (int j=0; j<outshape1; j++)\n            for (int k=0; k<outshape2; k++)\n            for (int l=0; l<outshape3; l++) @out(i,j,k,l) = 0;\n\n            for (int i=0; i<poutshape0; i++)\n            for (int j=0; j<poutshape1; j++)\n            for (int k=0; k<poutshape2; k++)\n            for (int l=0; l<poutshape3; l++) {{\n                int kx=k*{stride}+{size}/2-{padding};\n                int ky=l*{stride}+{size}/2-{padding};\n                int bo=1;\n                for (int p=kx-{size}/2;p<=kx+{size}/2 && bo;p++)\n                for (int q=ky-{size}/2;q<=ky+{size}/2 && bo;q++)\n                    if (p>=0 && q>=0 && p<in0shape2 && q<in0shape3)\n                    if (@pout(i,j,k,l) == @in0(i,j,p,q)) {{\n                        @out(i,j,p,q) += @dout(i,j,k,l);\n                        bo=0;\n                    }}\n            }}\n        "])
    return y


def concat(arr, dim):
    total_dim = 0
    for a in arr:
        total_dim += a.shape[dim]

    cdim = 0
    s = None
    indexes = [f"i{i}" for i in range(len(a.shape))]
    for a in arr:
        shape = list(a.shape)
        shape[dim] = total_dim
        indexes[dim] = f"i{dim}-{cdim}"
        b = a.reindex(shape, indexes)
        if len(arr) >= 10:
            b.stop_fuse()
        elif s is None:
            s = b
        else:
            s += b
        cdim += a.shape[dim]

    return s


def check(bc):
    bc = np.array(bc)
    if ((bc != 1) * (bc != bc.max(0))).sum() > 0:
        raise Exception('Shape not match.')
    else:
        return bc.max(0)


def slice_var_index(x, slices):
    if not isinstance(slices, tuple):
        slices = (
         slices,)
    if isinstance(slices[0], jt.Var):
        if len(slices) == 1:
            if slices[0].dtype == 'bool':
                return (
                 slices[0].where(),)
    bc = []
    ml = -1
    for idx, s in enumerate(slices):
        if isinstance(s, jt.Var):
            shape = s.shape
        else:
            if isinstance(s, np.ndarray):
                shape = list(s.shape)
            else:
                if isinstance(s, list):
                    shape = list(np.array(s).shape)
                else:
                    continue
                if len(shape) >= ml:
                    ml = len(shape)
                bc.append(shape)

    for idx, shape in enumerate(bc):
        if len(shape) < ml:
            shape = (ml - len(shape)) * [1] + shape
            bc[idx] = shape

    if len(bc) >= 1:
        bc_shape = check(bc)
        ss = []
        for idx, s in enumerate(slices):
            if isinstance(s, np.ndarray) or isinstance(s, list):
                ss.append(jt.array(s).broadcast(bc_shape.tolist()))
            elif isinstance(s, jt.Var):
                ss.append(s.broadcast(bc_shape.tolist()))
            else:
                ss.append(s)

        slices = ss
    out_shape = []
    out_index = []
    shape = x.shape
    cnt_list = 0
    extras_idx = []
    extras = []
    for i in range(len(shape)):
        if i >= len(slices):
            s = slice(None)
        else:
            s = slices[i]
        sp = shape[i]
        j = len(out_shape)
        if isinstance(s, int):
            if s < 0:
                s += sp
            out_index.append(str(s))
        elif isinstance(s, slice):
            if s == slice(None):
                out_shape.append(sp)
                out_index.append(f"i{j}")
                continue
            start = 0 if s.start is None else s.start
            stop = sp if s.stop is None else s.stop
            step = 1 if s.step is None else s.step
            if start < 0:
                start += sp
            if stop < 0:
                stop += sp
            out_shape.append(1 + int(max(0, (stop - start - 1) // step)))
            out_index.append(f"{start}+i{j}*{step}")
        elif isinstance(s, jt.Var):
            if cnt_list == 0:
                for idx in range(len(bc_shape)):
                    extras_idx.append(f"i{len(out_shape) + idx}")

                out_shape += bc_shape.tolist()
            out_index.append(f"@e{cnt_list}(" + ','.join(extras_idx) + ')')
            cnt_list += 1
            extras.append(s)
        else:
            raise Exception(f"Not support slice {s}")

    if len(out_shape) == 0:
        out_shape = [
         1]
    x.stop_fuse()
    return (out_shape, out_index, 0, [], extras)


def slice_var(x, slices):
    reindex_args = slice_var_index(x, slices)
    x.stop_fuse()
    return (x.reindex)(*reindex_args).stop_fuse()


def setitem(x, slices, value):
    reindex_args = slice_var_index(x, slices)
    reindex_reduce_args = (x.shape, reindex_args[1]) + reindex_args[3:]
    xslice = (x.stop_fuse().reindex)(*reindex_args).stop_fuse()
    value = jt.broadcast(value, xslice)
    one = jt.broadcast(1, xslice)
    if not isinstance(reindex_args[0][0], jt.Var):
        reindex_args = (
         x.shape,) + reindex_args[1:]
    mask = (one.reindex_reduce)(*('add', ), *reindex_reduce_args)
    data = (value.reindex_reduce)(*('add', ), *reindex_reduce_args)
    out = mask.ternary(data, x).stop_fuse()
    x.assign(out)
    return x


jt.Var.__getitem__ = jt.Var.slice_var = slice_var
jt.Var.__setitem__ = setitem

def adam(model, loss, lr=0.0003, betas=[0.9, 0.999], eps=1e-08):
    ps = jt.find_vars(model)
    gs = jt.grad(loss, ps)
    with jt.var_scope(('_'.join([model, 'adam'])), unique=True):
        adam_step = jt.make_var([1], init=(jt.zeros))
        adam_step += 1
        for p, g in zip(ps, gs):
            m = jt.make_var((p.shape), init=(jt.zeros))
            v = jt.make_var((p.shape), init=(jt.zeros))
            m.assign(betas[0] * m + (1 - betas[0]) * g)
            v.assign(betas[1] * v + (1 - betas[1]) * g * g)
            step_size = lr * jt.sqrt(1 - betas[1] ** adam_step) / (1 - betas[0] ** adam_step)
            p -= m * step_size / (jt.sqrt(v) + eps)