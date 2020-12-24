# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/eveliver/visualization.py
# Compiled at: 2020-03-20 06:25:06
# Size of source mod 2**32: 1370 bytes
import torch

def write_mean_std_max_min_absmean(writer, name, tensor, step):
    if tensor.shape[0] == 0:
        return
    name = 'zz.' + name
    writer.add_scalar((name + 'mean'), (torch.mean(tensor).item()), global_step=step)
    writer.add_scalar((name + 'std'), (torch.std(tensor).item()), global_step=step)
    writer.add_scalar((name + 'max'), (torch.max(tensor).item()), global_step=step)
    writer.add_scalar((name + 'min'), (torch.min(tensor).item()), global_step=step)
    writer.add_scalar((name + 'absmean'), (torch.mean(torch.abs(tensor)).item()), global_step=step)
    writer.add_histogram((name + 'histogram'), (tensor.detach().cpu().data.numpy()), global_step=step)


def write_statistics(writer, model, step):
    for name, parameter in model.named_parameters():
        if parameter.dtype not in [torch.float, torch.double, torch.half]:
            pass
        else:
            if parameter.is_sparse:
                write_mean_std_max_min_absmean(writer, name + '/', parameter._values(), step)
            else:
                write_mean_std_max_min_absmean(writer, name + '/', parameter, step)
            if parameter.grad is not None:
                if parameter.grad.is_sparse:
                    write_mean_std_max_min_absmean(writer, name + '/grad-', parameter.grad._values(), step)
                else:
                    write_mean_std_max_min_absmean(writer, name + '/grad-', parameter.grad, step)