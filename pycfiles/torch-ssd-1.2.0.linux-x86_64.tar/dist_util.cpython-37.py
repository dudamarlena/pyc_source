# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/b3ql/.virtualenvs/SSD/lib/python3.7/site-packages/ssd/utils/dist_util.py
# Compiled at: 2019-10-28 14:34:58
# Size of source mod 2**32: 2737 bytes
import pickle, torch
import torch.distributed as dist

def get_world_size():
    if not dist.is_available():
        return 1
    else:
        return dist.is_initialized() or 1
    return dist.get_world_size()


def get_rank():
    if not dist.is_available():
        return 0
    else:
        return dist.is_initialized() or 0
    return dist.get_rank()


def is_main_process():
    return get_rank() == 0


def synchronize():
    """
       Helper function to synchronize (barrier) among all processes when
       using distributed training
    """
    if not dist.is_available():
        return
    else:
        return dist.is_initialized() or None
    world_size = dist.get_world_size()
    if world_size == 1:
        return
    dist.barrier()


def _encode(encoded_data, data):
    encoded_bytes = pickle.dumps(data)
    storage = torch.ByteStorage.from_buffer(encoded_bytes)
    tensor = torch.ByteTensor(storage).to('cuda')
    s = tensor.numel()
    assert s <= 255, "Can't encode data greater than 255 bytes"
    encoded_data[0] = s
    encoded_data[1:s + 1] = tensor


def all_gather(data):
    """
    Run all_gather on arbitrary picklable data (not necessarily tensors)
    Args:
        data: any picklable object
    Returns:
        list[data]: list of data gathered from each rank
    """
    world_size = get_world_size()
    if world_size == 1:
        return [
         data]
    buffer = pickle.dumps(data)
    storage = torch.ByteStorage.from_buffer(buffer)
    tensor = torch.ByteTensor(storage).to('cuda')
    local_size = torch.LongTensor([tensor.numel()]).to('cuda')
    size_list = [torch.LongTensor([0]).to('cuda') for _ in range(world_size)]
    dist.all_gather(size_list, local_size)
    size_list = [int(size.item()) for size in size_list]
    max_size = max(size_list)
    tensor_list = []
    for _ in size_list:
        tensor_list.append(torch.ByteTensor(size=(max_size,)).to('cuda'))

    if local_size != max_size:
        padding = torch.ByteTensor(size=(max_size - local_size,)).to('cuda')
        tensor = torch.cat((tensor, padding), dim=0)
    dist.all_gather(tensor_list, tensor)
    data_list = []
    for size, tensor in zip(size_list, tensor_list):
        buffer = tensor.cpu().numpy().tobytes()[:size]
        data_list.append(pickle.loads(buffer))

    return data_list