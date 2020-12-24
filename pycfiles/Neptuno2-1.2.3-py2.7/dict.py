# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/neptuno/dict.py
# Compiled at: 2012-10-29 11:33:17


class Dict(dict):

    def __init__(self, **kw):
        for k, v in kw.iteritems():
            if isinstance(v, dict) or isinstance(v, Dict):
                self[k] = Dict(**v)
            elif isinstance(v, list):
                v2 = []
                for item in v:
                    if isinstance(item, dict) or isinstance(item, Dict):
                        v2.append(Dict(**item))
                    else:
                        v2.append(item)

                self[k] = v2
            elif isinstance(v, tuple):
                v2 = None
                for item in v:
                    if isinstance(v, dict) or isinstance(v, Dict):
                        if not v2:
                            v2 = (
                             Dict(**item),)
                        else:
                            v2 = v2 + (Dict(**item),)
                    elif not v2:
                        v2 = (
                         item,)
                    else:
                        v2 = v2 + (item,)

                self[k] = v2
            else:
                self[k] = v

        return

    def __getattr__(self, name):
        if self.has_key(name):
            return self[name]

    def __setattr__(self, name, value):
        self[name] = value


if __name__ == '__main__':
    origen = {'cargos': [{'id': 1, 'desc': 'uno'}, {'id': 2, 'desc': 'dos'}], 'tupla': ({'a': 1000}, {'a': 2000})}
    destino = Dict(**origen)
    print destino.cargos
    print destino.cargos[0].id
    print destino.tupla
    print destino.tupla[0].a