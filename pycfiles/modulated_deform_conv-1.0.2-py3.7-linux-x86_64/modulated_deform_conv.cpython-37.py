# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/modulated_deform_conv.py
# Compiled at: 2020-03-17 01:03:08
# Size of source mod 2**32: 36975 bytes
import math, torch
import torch.nn as nn
from torch.autograd import Function
from torch.autograd.function import once_differentiable
from torch.nn.modules.utils import _pair, _triple
import MDCONV_CUDA

class DeformConv2dFunction(torch.autograd.Function):

    @staticmethod
    def forward(ctx, input, offset, weight, bias=None, stride=1, padding=0, dilation=1, groups=1, deformable_groups=1, in_step=64):
        ctx.stride = _pair(stride)
        ctx.padding = _pair(padding)
        ctx.dilation = _pair(dilation)
        ctx.groups = groups
        ctx.deformable_groups = deformable_groups
        ctx.in_step = in_step
        ctx.with_bias = bias is not None
        if not ctx.with_bias:
            bias = input.new_empty(0)
        if not input.is_cuda:
            raise NotImplementedError
        if weight.requires_grad or offset.requires_grad or input.requires_grad:
            ctx.save_for_backward(input, offset, weight, bias)
        output = input.new_empty(DeformConv2dFunction._infer_shape(ctx, input, weight))
        MDCONV_CUDA.deform_conv2d_forward_cuda(input, weight, bias, offset, output, weight.shape[2], weight.shape[3], ctx.stride[0], ctx.stride[1], ctx.padding[0], ctx.padding[1], ctx.dilation[0], ctx.dilation[1], ctx.groups, ctx.deformable_groups, ctx.in_step, ctx.with_bias)
        return output

    @staticmethod
    def backward(ctx, grad_output):
        grad_output = grad_output.contiguous()
        if not grad_output.is_cuda:
            raise NotImplementedError
        input, offset, weight, bias = ctx.saved_tensors
        grad_input = torch.zeros_like(input)
        grad_offset = torch.zeros_like(offset)
        grad_weight = torch.zeros_like(weight)
        grad_bias = torch.zeros_like(bias)
        MDCONV_CUDA.deform_conv2d_backward_cuda(input, weight, bias, offset, grad_input, grad_weight, grad_bias, grad_offset, grad_output, weight.shape[2], weight.shape[3], ctx.stride[0], ctx.stride[1], ctx.padding[0], ctx.padding[1], ctx.dilation[0], ctx.dilation[1], ctx.groups, ctx.deformable_groups, ctx.in_step, ctx.with_bias)
        if not ctx.with_bias:
            grad_bias = None
        return (
         grad_input, grad_offset, grad_weight, grad_bias, None, None, None, None, None, None)

    @staticmethod
    def _infer_shape(ctx, input, weight):
        n = input.size(0)
        channels_out = weight.size(0)
        height, width = input.shape[2:4]
        kernel_h, kernel_w = weight.shape[2:4]
        height_out = (height + 2 * ctx.padding[0] - (ctx.dilation[0] * (kernel_h - 1) + 1)) // ctx.stride[0] + 1
        width_out = (width + 2 * ctx.padding[1] - (ctx.dilation[1] * (kernel_w - 1) + 1)) // ctx.stride[1] + 1
        return (n, channels_out, height_out, width_out)


class ModulatedDeformConv2dFunction(Function):

    @staticmethod
    def forward--- This code section failed: ---

 L.  97         0  LOAD_GLOBAL              _pair
                2  LOAD_FAST                'stride'
                4  CALL_FUNCTION_1       1  '1 positional argument'
                6  LOAD_FAST                'ctx'
                8  STORE_ATTR               stride

 L.  98        10  LOAD_GLOBAL              _pair
               12  LOAD_FAST                'padding'
               14  CALL_FUNCTION_1       1  '1 positional argument'
               16  LOAD_FAST                'ctx'
               18  STORE_ATTR               padding

 L.  99        20  LOAD_GLOBAL              _pair
               22  LOAD_FAST                'dilation'
               24  CALL_FUNCTION_1       1  '1 positional argument'
               26  LOAD_FAST                'ctx'
               28  STORE_ATTR               dilation

 L. 100        30  LOAD_FAST                'groups'
               32  LOAD_FAST                'ctx'
               34  STORE_ATTR               groups

 L. 101        36  LOAD_FAST                'deformable_groups'
               38  LOAD_FAST                'ctx'
               40  STORE_ATTR               deformable_groups

 L. 102        42  LOAD_FAST                'in_step'
               44  LOAD_FAST                'ctx'
               46  STORE_ATTR               in_step

 L. 103        48  LOAD_FAST                'bias'
               50  LOAD_CONST               None
               52  COMPARE_OP               is-not
               54  LOAD_FAST                'ctx'
               56  STORE_ATTR               with_bias

 L. 104        58  LOAD_FAST                'ctx'
               60  LOAD_ATTR                with_bias
               62  POP_JUMP_IF_TRUE     74  'to 74'

 L. 105        64  LOAD_FAST                'input'
               66  LOAD_METHOD              new_empty
               68  LOAD_CONST               0
               70  CALL_METHOD_1         1  '1 positional argument'
               72  STORE_FAST               'bias'
             74_0  COME_FROM            62  '62'

 L. 106        74  LOAD_FAST                'input'
               76  LOAD_ATTR                is_cuda
               78  POP_JUMP_IF_TRUE     84  'to 84'

 L. 107        80  LOAD_GLOBAL              NotImplementedError
               82  RAISE_VARARGS_1       1  'exception instance'
             84_0  COME_FROM            78  '78'

 L. 108        84  LOAD_FAST                'weight'
               86  LOAD_ATTR                requires_grad
               88  POP_JUMP_IF_TRUE    108  'to 108'
               90  LOAD_FAST                'mask'
               92  LOAD_ATTR                requires_grad
               94  POP_JUMP_IF_TRUE    108  'to 108'
               96  LOAD_FAST                'offset'
               98  LOAD_ATTR                requires_grad
              100  POP_JUMP_IF_TRUE    108  'to 108'
              102  LOAD_FAST                'input'
              104  LOAD_ATTR                requires_grad
              106  POP_JUMP_IF_FALSE   126  'to 126'
            108_0  COME_FROM           100  '100'
            108_1  COME_FROM            94  '94'
            108_2  COME_FROM            88  '88'

 L. 109       108  LOAD_FAST                'ctx'
              110  LOAD_METHOD              save_for_backward
              112  LOAD_FAST                'input'
              114  LOAD_FAST                'offset'
              116  LOAD_FAST                'mask'
              118  LOAD_FAST                'weight'
              120  LOAD_FAST                'bias'
              122  CALL_METHOD_5         5  '5 positional arguments'
              124  POP_TOP          
            126_0  COME_FROM           106  '106'

 L. 110       126  LOAD_FAST                'input'
              128  LOAD_METHOD              new_empty
              130  LOAD_GLOBAL              ModulatedDeformConv2dFunction
              132  LOAD_METHOD              _infer_shape
              134  LOAD_FAST                'ctx'
              136  LOAD_FAST                'input'
              138  LOAD_FAST                'weight'
              140  CALL_METHOD_3         3  '3 positional arguments'
              142  CALL_METHOD_1         1  '1 positional argument'
              144  STORE_FAST               'output'

 L. 112       146  LOAD_GLOBAL              MDCONV_CUDA
              148  LOAD_METHOD              modulated_deform_conv2d_forward_cuda

 L. 113       150  LOAD_FAST                'input'
              152  LOAD_FAST                'weight'
              154  LOAD_FAST                'bias'
              156  LOAD_FAST                'offset'
              158  LOAD_FAST                'mask'
              160  LOAD_FAST                'output'

 L. 114       162  LOAD_FAST                'weight'
              164  LOAD_ATTR                shape
              166  LOAD_CONST               2
              168  BINARY_SUBSCR    
              170  LOAD_FAST                'weight'
              172  LOAD_ATTR                shape
              174  LOAD_CONST               3
              176  BINARY_SUBSCR    

 L. 115       178  LOAD_FAST                'ctx'
              180  LOAD_ATTR                stride
              182  LOAD_CONST               0
              184  BINARY_SUBSCR    
              186  LOAD_FAST                'ctx'
              188  LOAD_ATTR                stride
              190  LOAD_CONST               1
              192  BINARY_SUBSCR    

 L. 116       194  LOAD_FAST                'ctx'
              196  LOAD_ATTR                padding
              198  LOAD_CONST               0
              200  BINARY_SUBSCR    
              202  LOAD_FAST                'ctx'
              204  LOAD_ATTR                padding
              206  LOAD_CONST               1
              208  BINARY_SUBSCR    

 L. 117       210  LOAD_FAST                'ctx'
              212  LOAD_ATTR                dilation
              214  LOAD_CONST               0
              216  BINARY_SUBSCR    
              218  LOAD_FAST                'ctx'
              220  LOAD_ATTR                dilation
              222  LOAD_CONST               1
              224  BINARY_SUBSCR    

 L. 118       226  LOAD_FAST                'ctx'
              228  LOAD_ATTR                groups
              230  LOAD_FAST                'ctx'
              232  LOAD_ATTR                deformable_groups
              234  LOAD_FAST                'ctx'
              236  LOAD_ATTR                in_step
              238  LOAD_FAST                'ctx'
              240  LOAD_ATTR                with_bias
              242  CALL_METHOD_18       18  '18 positional arguments'
              244  POP_TOP          

 L. 128       246  LOAD_FAST                'output'
              248  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `COME_FROM' instruction at offset 126_0

    @staticmethod
    @once_differentiable
    def backward(ctx, grad_output):
        grad_output = grad_output.contiguous()
        if not grad_output.is_cuda:
            raise NotImplementedError
        input, offset, mask, weight, bias = ctx.saved_tensors
        grad_input = torch.zeros_like(input)
        grad_offset = torch.zeros_like(offset)
        grad_mask = torch.zeros_like(mask)
        grad_weight = torch.zeros_like(weight)
        grad_bias = torch.zeros_like(bias)
        MDCONV_CUDA.modulated_deform_conv2d_backward_cuda(input, weight, bias, offset, mask, grad_input, grad_weight, grad_bias, grad_offset, grad_mask, grad_output, weight.shape[2], weight.shape[3], ctx.stride[0], ctx.stride[1], ctx.padding[0], ctx.padding[1], ctx.dilation[0], ctx.dilation[1], ctx.groups, ctx.deformable_groups, ctx.in_step, ctx.with_bias)
        if not ctx.with_bias:
            grad_bias = None
        return (grad_input, grad_offset, grad_mask, grad_weight, grad_bias, None, None, None, None, None, None)

    @staticmethod
    def _infer_shape(ctx, input, weight):
        n = input.size(0)
        channels_out = weight.size(0)
        height, width = input.shape[2:4]
        kernel_h, kernel_w = weight.shape[2:4]
        height_out = (height + 2 * ctx.padding[0] - (ctx.dilation[0] * (kernel_h - 1) + 1)) // ctx.stride[0] + 1
        width_out = (width + 2 * ctx.padding[1] - (ctx.dilation[1] * (kernel_w - 1) + 1)) // ctx.stride[1] + 1
        return (n, channels_out, height_out, width_out)


class DeformConv3dFunction(Function):

    @staticmethod
    def forward(ctx, input, offset, weight, bias=None, stride=1, padding=0, dilation=1, groups=1, deformable_groups=1, in_step=64):
        ctx.stride = _triple(stride)
        ctx.padding = _triple(padding)
        ctx.dilation = _triple(dilation)
        ctx.groups = groups
        ctx.deformable_groups = deformable_groups
        ctx.in_step = in_step
        ctx.with_bias = bias is not None
        if not ctx.with_bias:
            bias = input.new_empty(0)
        if not input.is_cuda:
            raise NotImplementedError
        if weight.requires_grad or offset.requires_grad or input.requires_grad:
            ctx.save_for_backward(input, offset, weight, bias)
        output = input.new_empty(DeformConv3dFunction._infer_shape(ctx, input, weight))
        MDCONV_CUDA.deform_conv3d_forward_cuda(input, weight, bias, offset, output, weight.shape[2], weight.shape[3], weight.shape[4], ctx.stride[0], ctx.stride[1], ctx.stride[2], ctx.padding[0], ctx.padding[1], ctx.padding[2], ctx.dilation[0], ctx.dilation[1], ctx.dilation[2], ctx.groups, ctx.deformable_groups, ctx.in_step, ctx.with_bias)
        return output

    @staticmethod
    @once_differentiable
    def backward(ctx, grad_output):
        grad_output = grad_output.contiguous()
        if not grad_output.is_cuda:
            raise NotImplementedError
        input, offset, weight, bias = ctx.saved_tensors
        grad_input = torch.zeros_like(input)
        grad_offset = torch.zeros_like(offset)
        grad_weight = torch.zeros_like(weight)
        grad_bias = torch.zeros_like(bias)
        MDCONV_CUDA.deform_conv3d_backward_cuda(input, weight, bias, offset, grad_input, grad_weight, grad_bias, grad_offset, grad_output, weight.shape[2], weight.shape[3], weight.shape[4], ctx.stride[0], ctx.stride[1], ctx.stride[2], ctx.padding[0], ctx.padding[1], ctx.padding[2], ctx.dilation[0], ctx.dilation[1], ctx.dilation[2], ctx.groups, ctx.deformable_groups, ctx.in_step, ctx.with_bias)
        if not ctx.with_bias:
            grad_bias = None
        return (grad_input, grad_offset, grad_weight, grad_bias, None, None, None, None, None, None)

    @staticmethod
    def _infer_shape(ctx, input, weight):
        n = input.size(0)
        channels_out = weight.size(0)
        height, width, length = input.shape[2:5]
        kernel_h, kernel_w, kernel_l = weight.shape[2:5]
        height_out = (height + 2 * ctx.padding[0] - (ctx.dilation[0] * (kernel_h - 1) + 1)) // ctx.stride[0] + 1
        width_out = (width + 2 * ctx.padding[1] - (ctx.dilation[1] * (kernel_w - 1) + 1)) // ctx.stride[1] + 1
        length_out = (length + 2 * ctx.padding[2] - (ctx.dilation[2] * (kernel_l - 1) + 1)) // ctx.stride[2] + 1
        return (n, channels_out, height_out, width_out, length_out)


class ModulatedDeformConv3dFunction(Function):

    @staticmethod
    def forward--- This code section failed: ---

 L. 267         0  LOAD_GLOBAL              _triple
                2  LOAD_FAST                'stride'
                4  CALL_FUNCTION_1       1  '1 positional argument'
                6  LOAD_FAST                'ctx'
                8  STORE_ATTR               stride

 L. 268        10  LOAD_GLOBAL              _triple
               12  LOAD_FAST                'padding'
               14  CALL_FUNCTION_1       1  '1 positional argument'
               16  LOAD_FAST                'ctx'
               18  STORE_ATTR               padding

 L. 269        20  LOAD_GLOBAL              _triple
               22  LOAD_FAST                'dilation'
               24  CALL_FUNCTION_1       1  '1 positional argument'
               26  LOAD_FAST                'ctx'
               28  STORE_ATTR               dilation

 L. 270        30  LOAD_FAST                'groups'
               32  LOAD_FAST                'ctx'
               34  STORE_ATTR               groups

 L. 271        36  LOAD_FAST                'deformable_groups'
               38  LOAD_FAST                'ctx'
               40  STORE_ATTR               deformable_groups

 L. 272        42  LOAD_FAST                'in_step'
               44  LOAD_FAST                'ctx'
               46  STORE_ATTR               in_step

 L. 273        48  LOAD_FAST                'bias'
               50  LOAD_CONST               None
               52  COMPARE_OP               is-not
               54  LOAD_FAST                'ctx'
               56  STORE_ATTR               with_bias

 L. 274        58  LOAD_FAST                'ctx'
               60  LOAD_ATTR                with_bias
               62  POP_JUMP_IF_TRUE     74  'to 74'

 L. 275        64  LOAD_FAST                'input'
               66  LOAD_METHOD              new_empty
               68  LOAD_CONST               0
               70  CALL_METHOD_1         1  '1 positional argument'
               72  STORE_FAST               'bias'
             74_0  COME_FROM            62  '62'

 L. 276        74  LOAD_FAST                'input'
               76  LOAD_ATTR                is_cuda
               78  POP_JUMP_IF_TRUE     84  'to 84'

 L. 277        80  LOAD_GLOBAL              NotImplementedError
               82  RAISE_VARARGS_1       1  'exception instance'
             84_0  COME_FROM            78  '78'

 L. 278        84  LOAD_FAST                'weight'
               86  LOAD_ATTR                requires_grad
               88  POP_JUMP_IF_TRUE    108  'to 108'
               90  LOAD_FAST                'mask'
               92  LOAD_ATTR                requires_grad
               94  POP_JUMP_IF_TRUE    108  'to 108'
               96  LOAD_FAST                'offset'
               98  LOAD_ATTR                requires_grad
              100  POP_JUMP_IF_TRUE    108  'to 108'
              102  LOAD_FAST                'input'
              104  LOAD_ATTR                requires_grad
              106  POP_JUMP_IF_FALSE   126  'to 126'
            108_0  COME_FROM           100  '100'
            108_1  COME_FROM            94  '94'
            108_2  COME_FROM            88  '88'

 L. 279       108  LOAD_FAST                'ctx'
              110  LOAD_METHOD              save_for_backward
              112  LOAD_FAST                'input'
              114  LOAD_FAST                'offset'
              116  LOAD_FAST                'mask'
              118  LOAD_FAST                'weight'
              120  LOAD_FAST                'bias'
              122  CALL_METHOD_5         5  '5 positional arguments'
              124  POP_TOP          
            126_0  COME_FROM           106  '106'

 L. 280       126  LOAD_FAST                'input'
              128  LOAD_METHOD              new_empty
              130  LOAD_GLOBAL              ModulatedDeformConv3dFunction
              132  LOAD_METHOD              _infer_shape
              134  LOAD_FAST                'ctx'
              136  LOAD_FAST                'input'
              138  LOAD_FAST                'weight'
              140  CALL_METHOD_3         3  '3 positional arguments'
              142  CALL_METHOD_1         1  '1 positional argument'
              144  STORE_FAST               'output'

 L. 282       146  LOAD_GLOBAL              MDCONV_CUDA
              148  LOAD_METHOD              modulated_deform_conv3d_forward_cuda

 L. 283       150  LOAD_FAST                'input'
              152  LOAD_FAST                'weight'
              154  LOAD_FAST                'bias'
              156  LOAD_FAST                'offset'
              158  LOAD_FAST                'mask'
              160  LOAD_FAST                'output'

 L. 284       162  LOAD_FAST                'weight'
              164  LOAD_ATTR                shape
              166  LOAD_CONST               2
              168  BINARY_SUBSCR    
              170  LOAD_FAST                'weight'
              172  LOAD_ATTR                shape
              174  LOAD_CONST               3
              176  BINARY_SUBSCR    
              178  LOAD_FAST                'weight'
              180  LOAD_ATTR                shape
              182  LOAD_CONST               4
              184  BINARY_SUBSCR    

 L. 285       186  LOAD_FAST                'ctx'
              188  LOAD_ATTR                stride
              190  LOAD_CONST               0
              192  BINARY_SUBSCR    
              194  LOAD_FAST                'ctx'
              196  LOAD_ATTR                stride
              198  LOAD_CONST               1
              200  BINARY_SUBSCR    
              202  LOAD_FAST                'ctx'
              204  LOAD_ATTR                stride
              206  LOAD_CONST               2
              208  BINARY_SUBSCR    

 L. 286       210  LOAD_FAST                'ctx'
              212  LOAD_ATTR                padding
              214  LOAD_CONST               0
              216  BINARY_SUBSCR    
              218  LOAD_FAST                'ctx'
              220  LOAD_ATTR                padding
              222  LOAD_CONST               1
              224  BINARY_SUBSCR    
              226  LOAD_FAST                'ctx'
              228  LOAD_ATTR                padding
              230  LOAD_CONST               2
              232  BINARY_SUBSCR    

 L. 287       234  LOAD_FAST                'ctx'
              236  LOAD_ATTR                dilation
              238  LOAD_CONST               0
              240  BINARY_SUBSCR    
              242  LOAD_FAST                'ctx'
              244  LOAD_ATTR                dilation
              246  LOAD_CONST               1
              248  BINARY_SUBSCR    
              250  LOAD_FAST                'ctx'
              252  LOAD_ATTR                dilation
              254  LOAD_CONST               2
              256  BINARY_SUBSCR    

 L. 288       258  LOAD_FAST                'ctx'
              260  LOAD_ATTR                groups
              262  LOAD_FAST                'ctx'
              264  LOAD_ATTR                deformable_groups
              266  LOAD_FAST                'ctx'
              268  LOAD_ATTR                in_step
              270  LOAD_FAST                'ctx'
              272  LOAD_ATTR                with_bias
              274  CALL_METHOD_22       22  '22 positional arguments'
              276  POP_TOP          

 L. 299       278  LOAD_FAST                'output'
              280  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `COME_FROM' instruction at offset 126_0

    @staticmethod
    @once_differentiable
    def backward(ctx, grad_output):
        grad_output = grad_output.contiguous()
        if not grad_output.is_cuda:
            raise NotImplementedError
        input, offset, mask, weight, bias = ctx.saved_tensors
        grad_input = torch.zeros_like(input)
        grad_offset = torch.zeros_like(offset)
        grad_mask = torch.zeros_like(mask)
        grad_weight = torch.zeros_like(weight)
        grad_bias = torch.zeros_like(bias)
        MDCONV_CUDA.modulated_deform_conv3d_backward_cuda(input, weight, bias, offset, mask, grad_input, grad_weight, grad_bias, grad_offset, grad_mask, grad_output, weight.shape[2], weight.shape[3], weight.shape[4], ctx.stride[0], ctx.stride[1], ctx.stride[2], ctx.padding[0], ctx.padding[1], ctx.padding[2], ctx.dilation[0], ctx.dilation[1], ctx.dilation[2], ctx.groups, ctx.deformable_groups, ctx.in_step, ctx.with_bias)
        if not ctx.with_bias:
            grad_bias = None
        return (grad_input, grad_offset, grad_mask, grad_weight, grad_bias, None, None, None, None, None, None)

    @staticmethod
    def _infer_shape(ctx, input, weight):
        n = input.size(0)
        channels_out = weight.size(0)
        height, width, length = input.shape[2:5]
        kernel_h, kernel_w, kernel_l = weight.shape[2:5]
        height_out = (height + 2 * ctx.padding[0] - (ctx.dilation[0] * (kernel_h - 1) + 1)) // ctx.stride[0] + 1
        width_out = (width + 2 * ctx.padding[1] - (ctx.dilation[1] * (kernel_w - 1) + 1)) // ctx.stride[1] + 1
        length_out = (length + 2 * ctx.padding[2] - (ctx.dilation[2] * (kernel_l - 1) + 1)) // ctx.stride[2] + 1
        return (n, channels_out, height_out, width_out, length_out)


deform_conv2d = DeformConv2dFunction.apply
modulated_deform_conv2d = ModulatedDeformConv2dFunction.apply
deform_conv3d = DeformConv3dFunction.apply
modulated_deform_conv3d = ModulatedDeformConv3dFunction.apply

class DeformConv2d(nn.Module):

    def __init__(self, in_channels, out_channels, kernel_size, stride=1, padding=0, dilation=1, groups=1, deformable_groups=1, bias=False, in_step=64):
        super(DeformConv2d, self).__init__()
        if not in_channels % groups == 0:
            raise AssertionError('in_channels {} cannot be divisible by groups {}'.format(in_channels, groups))
        else:
            assert out_channels % groups == 0, 'out_channels {} cannot be divisible by groups {}'.format(out_channels, groups)
            self.in_channels = in_channels
            self.out_channels = out_channels
            self.kernel_size = _pair(kernel_size)
            self.stride = _pair(stride)
            self.padding = _pair(padding)
            self.dilation = _pair(dilation)
            self.groups = groups
            self.deformable_groups = deformable_groups
            self.in_step = in_step
            self.weight = nn.Parameter((torch.Tensor)(out_channels, in_channels // self.groups, *self.kernel_size))
            self.with_bias = bias
            if self.with_bias:
                self.bias = nn.Parameter(torch.Tensor(out_channels))
            else:
                self.bias = None
        self.reset_parameters()

    def reset_parameters(self):
        n = self.in_channels
        for k in self.kernel_size:
            n *= k

        stdv = 1.0 / math.sqrt(n)
        self.weight.data.uniform_(-stdv, stdv)
        if self.with_bias:
            self.bias.data.fill_(0)

    def forward(self, x, offset):
        return deform_conv2d(x, offset, self.weight, self.bias, self.stride, self.padding, self.dilation, self.groups, self.deformable_group, self.in_step)


class ModulatedDeformConv2d(nn.Module):

    def __init__(self, in_channels, out_channels, kernel_size, stride=1, padding=0, dilation=1, groups=1, deformable_groups=1, bias=False, in_step=64):
        super(ModulatedDeformConv2d, self).__init__()
        if not in_channels % groups == 0:
            raise AssertionError('in_channels {} cannot be divisible by groups {}'.format(in_channels, groups))
        else:
            assert out_channels % groups == 0, 'out_channels {} cannot be divisible by groups {}'.format(out_channels, groups)
            self.in_channels = in_channels
            self.out_channels = out_channels
            self.kernel_size = _pair(kernel_size)
            self.stride = _pair(stride)
            self.padding = _pair(padding)
            self.dilation = _pair(dilation)
            self.groups = groups
            self.deformable_groups = deformable_groups
            self.in_step = in_step
            self.weight = nn.Parameter((torch.Tensor)(out_channels, in_channels // self.groups, *self.kernel_size))
            self.with_bias = bias
            if self.with_bias:
                self.bias = nn.Parameter(torch.Tensor(out_channels))
            else:
                self.bias = None
        self.reset_parameters()

    def reset_parameters(self):
        n = self.in_channels
        for k in self.kernel_size:
            n *= k

        stdv = 1.0 / math.sqrt(n)
        self.weight.data.uniform_(-stdv, stdv)
        if self.with_bias:
            self.bias.data.fill_(0)

    def forward(self, x, offset, mask):
        return modulated_deform_conv2d(x, offset, mask, self.weight, self.bias, self.stride, self.padding, self.dilation, self.groups, self.deformable_group, self.in_step)


class DeformConv3d(nn.Module):

    def __init__(self, in_channels, out_channels, kernel_size, stride=1, padding=0, dilation=1, groups=1, deformable_groups=1, bias=False, in_step=64):
        super(DeformConv3d, self).__init__()
        if not in_channels % groups == 0:
            raise AssertionError('in_channels {} cannot be divisible by groups {}'.format(in_channels, groups))
        else:
            assert out_channels % groups == 0, 'out_channels {} cannot be divisible by groups {}'.format(out_channels, groups)
            self.in_channels = in_channels
            self.out_channels = out_channels
            self.kernel_size = _triple(kernel_size)
            self.stride = _triple(stride)
            self.padding = _triple(padding)
            self.dilation = _triple(dilation)
            self.groups = groups
            self.deformable_groups = deformable_groups
            self.in_step = in_step
            self.weight = nn.Parameter((torch.Tensor)(out_channels, in_channels // self.groups, *self.kernel_size))
            self.with_bias = bias
            if self.with_bias:
                self.bias = nn.Parameter(torch.Tensor(out_channels))
            else:
                self.bias = None
        self.reset_parameters()

    def reset_parameters(self):
        n = self.in_channels
        for k in self.kernel_size:
            n *= k

        stdv = 1.0 / math.sqrt(n)
        self.weight.data.uniform_(-stdv, stdv)
        if self.with_bias:
            self.bias.data.fill_(0)

    def forward(self, x, offset):
        return deform_conv3d(x, offset, self.weight, self.bias, self.stride, self.padding, self.dilation, self.groups, self.deformable_group, self.in_step)


class ModulatedDeformConv3d(nn.Module):

    def __init__(self, in_channels, out_channels, kernel_size, stride=1, padding=0, dilation=1, groups=1, deformable_groups=1, bias=False, in_step=64):
        super(ModulatedDeformConv3d, self).__init__()
        if not in_channels % groups == 0:
            raise AssertionError('in_channels {} cannot be divisible by groups {}'.format(in_channels, groups))
        else:
            assert out_channels % groups == 0, 'out_channels {} cannot be divisible by groups {}'.format(out_channels, groups)
            self.in_channels = in_channels
            self.out_channels = out_channels
            self.kernel_size = _triple(kernel_size)
            self.stride = _triple(stride)
            self.padding = _triple(padding)
            self.dilation = _triple(dilation)
            self.groups = groups
            self.deformable_groups = deformable_groups
            self.in_step = in_step
            self.weight = nn.Parameter((torch.Tensor)(out_channels, in_channels // self.groups, *self.kernel_size))
            self.with_bias = bias
            if self.with_bias:
                self.bias = nn.Parameter(torch.Tensor(out_channels))
            else:
                self.bias = None
        self.reset_parameters()

    def reset_parameters(self):
        n = self.in_channels
        for k in self.kernel_size:
            n *= k

        stdv = 1.0 / math.sqrt(n)
        self.weight.data.uniform_(-stdv, stdv)
        if self.with_bias:
            self.bias.data.fill_(0)

    def forward(self, x, offset, mask):
        return modulated_deform_conv3d(x, offset, mask, self.weight, self.bias, self.stride, self.padding, self.dilation, self.groups, self.deformable_group, self.in_step)


class DeformConv2dPack(DeformConv2d):

    def __init__(self, *args, **kwargs):
        (super(DeformConv2dPack, self).__init__)(*args, **kwargs)
        self.conv_offset = nn.Conv2d((self.in_channels),
          (self.deformable_groups * 2 * self.kernel_size[0] * self.kernel_size[1]),
          kernel_size=(self.kernel_size),
          stride=(_pair(self.stride)),
          padding=(_pair(self.padding)),
          bias=True)
        self.init_offset()

    def init_offset(self):
        n = self.in_channels
        for k in self.kernel_size:
            n *= k

        stdv = 1.0 / math.sqrt(n)
        self.conv_offset.weight.data.uniform_(-stdv, stdv)
        self.conv_offset.bias.data.zero_()

    def forward(self, x):
        offset = self.conv_offset(x)
        return deform_conv2d(x, offset, self.weight, self.bias, self.stride, self.padding, self.dilation, self.groups, self.deformable_group, self.in_step)


class ModulatedDeformConv2dPack(ModulatedDeformConv2d):

    def __init__(self, *args, **kwargs):
        (super(ModulatedDeformConv2dPack, self).__init__)(*args, **kwargs)
        self.conv_offset = nn.Conv2d((self.in_channels),
          (self.deformable_groups * 2 * self.kernel_size[0] * self.kernel_size[1]),
          kernel_size=(self.kernel_size),
          stride=(_pair(self.stride)),
          padding=(_pair(self.padding)),
          bias=True)
        self.conv_mask = nn.Conv2d((self.in_channels),
          (self.deformable_groups * self.kernel_size[0] * self.kernel_size[1]),
          kernel_size=(self.kernel_size),
          stride=(_pair(self.stride)),
          padding=(_pair(self.padding)),
          bias=True)
        self.init_offset_mask()

    def init_offset_mask(self):
        n = self.in_channels
        for k in self.kernel_size:
            n *= k

        stdv = 1.0 / math.sqrt(n)
        self.conv_offset.weight.data.uniform_(-stdv, stdv)
        self.conv_offset.bias.data.zero_()
        self.conv_mask.weight.data.uniform_(-stdv, stdv)
        self.conv_mask.bias.data.zero_()

    def forward(self, x):
        offset = self.conv_offset(x)
        mask = self.conv_mask(x)
        return deform_conv2d(x, offset, mask, self.weight, self.bias, self.stride, self.padding, self.dilation, self.groups, self.deformable_group, self.in_step)


class DeformConv3dPack(DeformConv3d):

    def __init__(self, *args, **kwargs):
        (super(DeformConv3dPack, self).__init__)(*args, **kwargs)
        self.conv_offset = nn.Conv3d((self.in_channels),
          (self.deformable_groups * 3 * self.kernel_size[0] * self.kernel_size[1] * self.kernel_size[2]),
          kernel_size=(self.kernel_size),
          stride=(self.stride),
          padding=(self.padding),
          bias=True)
        self.init_offset()

    def init_offset(self):
        n = self.in_channels
        for k in self.kernel_size:
            n *= k

        stdv = 1.0 / math.sqrt(n)
        self.conv_offset.weight.data.uniform_(-stdv, stdv)
        self.conv_offset.bias.data.zero_()

    def forward(self, x):
        offset = self.conv_offset(x)
        return deform_conv3d(x, offset, self.weight, self.bias, self.stride, self.padding, self.dilation, self.groups, self.deformable_group, self.in_step)


class ModulatedDeformConv3dPack(ModulatedDeformConv3d):

    def __init__(self, *args, **kwargs):
        (super(ModulatedDeformConv2dPack, self).__init__)(*args, **kwargs)
        self.conv_offset = nn.Conv3d((self.in_channels),
          (self.deformable_groups * 3 * self.kernel_size[0] * self.kernel_size[1] * self.kernel_size[2]),
          kernel_size=(self.kernel_size),
          stride=(self.stride),
          padding=(self.padding),
          bias=True)
        self.conv_mask = nn.Conv3d((self.in_channels),
          (self.deformable_groups * self.kernel_size[0] * self.kernel_size[1] * self.kernel_size[2]),
          kernel_size=(self.kernel_size),
          stride=(self.stride),
          padding=(self.padding),
          bias=True)
        self.init_offset_mask()

    def init_offset_mask(self):
        n = self.in_channels
        for k in self.kernel_size:
            n *= k

        stdv = 1.0 / math.sqrt(n)
        self.conv_offset.weight.data.uniform_(-stdv, stdv)
        self.conv_offset.bias.data.zero_()
        self.conv_mask.weight.data.uniform_(-stdv, stdv)
        self.conv_mask.bias.data.zero_()

    def forward(self, x):
        offset = self.conv_offset(x)
        mask = self.conv_mask(x)
        return deform_conv3d(x, offset, mask, self.weight, self.bias, self.stride, self.padding, self.dilation, self.groups, self.deformable_group, self.in_step)