# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/eveliver/distributed.py
# Compiled at: 2020-03-19 03:31:58
# Size of source mod 2**32: 870 bytes
import json, torch

def distributed_broadcast(args, l):
    if not type(l) == list:
        if not type(l) == dict:
            raise AssertionError
    if args.local_rank < 0:
        return l
    else:
        torch.distributed.barrier()
        process_number = torch.distributed.get_world_size()
        json.dump(l, open(f"tmp/{args.local_rank}.json", 'w'))
        torch.distributed.barrier()
        objs = list()
        for i in range(process_number):
            objs.append(json.load(open(f"tmp/{i}.json")))

        if type(objs[0]) == list:
            ret = list()
            for i in range(process_number):
                ret.extend(objs[i])

        else:
            ret = dict()
            for i in range(process_number):
                for k, v in objs.items():
                    assert k not in ret
                    ret[k] = v

        torch.distributed.barrier()
        return ret