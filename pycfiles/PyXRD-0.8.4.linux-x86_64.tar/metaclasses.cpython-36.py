# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python3.6/dist-packages/pyxrd/refinement/refinables/metaclasses.py
# Compiled at: 2020-03-07 03:51:50
# Size of source mod 2**32: 1775 bytes
from mvc.models.metaclasses import ModelMeta
from .models import RefinementInfo

class PyXRDRefinableMeta(ModelMeta):
    __doc__ = '\n        A metaclass for regular mvc Models with refinable properties.\n    '

    def __call__(cls, *args, **kwargs):
        """
        Strips the refinement info data from the keyword argument dictionary,
        passes the stripped dictionary to create the actual class instance,
        creates the attributes on the instance and returns it.
        """
        prop_infos = dict()
        for prop in cls.Meta.all_properties:
            if getattr(prop, 'refinable', False):
                ref_info_name = prop.get_refinement_info_name()
                info_args = kwargs.pop(ref_info_name, None)
                if info_args:
                    prop_infos[ref_info_name] = (RefinementInfo.from_json)(*info_args)
                else:
                    prop_infos[ref_info_name] = RefinementInfo(prop.minimum, prop.maximum, False)

        instance = (ModelMeta.__call__)(cls, *args, **kwargs)
        for ref_info_name, ref_info in prop_infos.items():
            setattr(instance, ref_info_name, ref_info)

        return instance