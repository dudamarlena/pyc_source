# uncompyle6 version 3.6.7
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-i686/egg/chemesis3/chemesis3_base.py
# Compiled at: 2011-09-13 02:53:02
import _chemesis3_base, new
new_instancemethod = new.instancemethod
try:
    _swig_property = property
except NameError:
    pass

def _swig_setattr_nondynamic(self, class_type, name, value, static=1):
    if name == 'thisown':
        return self.this.own(value)
    if name == 'this':
        if type(value).__name__ == 'PySwigObject':
            self.__dict__[name] = value
            return
    method = class_type.__swig_setmethods__.get(name, None)
    if method:
        return method(self, value)
    if not static or hasattr(self, name):
        self.__dict__[name] = value
    else:
        raise AttributeError('You cannot add attributes to %s' % self)
    return


def _swig_setattr(self, class_type, name, value):
    return _swig_setattr_nondynamic(self, class_type, name, value, 0)


def _swig_getattr(self, class_type, name):
    if name == 'thisown':
        return self.this.own()
    method = class_type.__swig_getmethods__.get(name, None)
    if method:
        return method(self)
    raise AttributeError, name
    return


def _swig_repr(self):
    try:
        strthis = 'proxy of ' + self.this.__repr__()
    except:
        strthis = ''

    return '<%s.%s; %s >' % (self.__class__.__module__, self.__class__.__name__, strthis)


import types
try:
    _object = types.ObjectType
    _newclass = 1
except AttributeError:

    class _object:
        pass


    _newclass = 0

del types
CHEMESIS3_SOURCE_NEUROSPACES = _chemesis3_base.CHEMESIS3_SOURCE_NEUROSPACES
AddressingNeurospaces2Chemesis = _chemesis3_base.AddressingNeurospaces2Chemesis
AddressingChemesis2Neurospaces = _chemesis3_base.AddressingChemesis2Neurospaces
PoolSize = _chemesis3_base.PoolSize
ReactionSize = _chemesis3_base.ReactionSize
SetDiffusionPool1 = _chemesis3_base.SetDiffusionPool1
SetDiffusionPool2 = _chemesis3_base.SetDiffusionPool2
solver_reaction_serial_2_index = _chemesis3_base.solver_reaction_serial_2_index
NumItems = _chemesis3_base.NumItems
NEUROSPACES_2_CHEMESIS3_MAX_FUNCTIONS = _chemesis3_base.NEUROSPACES_2_CHEMESIS3_MAX_FUNCTIONS
Chemesis3AddressAggregator = _chemesis3_base.Chemesis3AddressAggregator
Chemesis3AddressableSet = _chemesis3_base.Chemesis3AddressableSet
Chemesis3AddressPoolVariable = _chemesis3_base.Chemesis3AddressPoolVariable
Chemesis3AddressReactionVariable = _chemesis3_base.Chemesis3AddressReactionVariable
Chemesis3AddressVariable = _chemesis3_base.Chemesis3AddressVariable
AVOGADRO = _chemesis3_base.AVOGADRO
RK_INT = _chemesis3_base.RK_INT
TRAPEZOIDAL_INT = _chemesis3_base.TRAPEZOIDAL_INT
GEAR_INT = _chemesis3_base.GEAR_INT
EPC_INT = _chemesis3_base.EPC_INT
FEULER_INT = _chemesis3_base.FEULER_INT
EEULER_INT = _chemesis3_base.EEULER_INT
AB2_INT = _chemesis3_base.AB2_INT
AB3_INT = _chemesis3_base.AB3_INT
AB4_INT = _chemesis3_base.AB4_INT
AB5_INT = _chemesis3_base.AB5_INT
BEULER_INT = _chemesis3_base.BEULER_INT
CRANK_INT = _chemesis3_base.CRANK_INT

class ch3_pool(_object):
    __swig_setmethods__ = {}
    __setattr__ = lambda self, name, value: _swig_setattr(self, ch3_pool, name, value)
    __swig_getmethods__ = {}
    __getattr__ = lambda self, name: _swig_getattr(self, ch3_pool, name)
    __repr__ = _swig_repr
    __swig_setmethods__['mc'] = _chemesis3_base.ch3_pool_mc_set
    __swig_getmethods__['mc'] = _chemesis3_base.ch3_pool_mc_get
    if _newclass:
        mc = _swig_property(_chemesis3_base.ch3_pool_mc_get, _chemesis3_base.ch3_pool_mc_set)
    __swig_setmethods__['iReactions'] = _chemesis3_base.ch3_pool_iReactions_set
    __swig_getmethods__['iReactions'] = _chemesis3_base.ch3_pool_iReactions_get
    if _newclass:
        iReactions = _swig_property(_chemesis3_base.ch3_pool_iReactions_get, _chemesis3_base.ch3_pool_iReactions_set)
    __swig_setmethods__['piReactions'] = _chemesis3_base.ch3_pool_piReactions_set
    __swig_getmethods__['piReactions'] = _chemesis3_base.ch3_pool_piReactions_get
    if _newclass:
        piReactions = _swig_property(_chemesis3_base.ch3_pool_piReactions_get, _chemesis3_base.ch3_pool_piReactions_set)
    __swig_setmethods__['piReactionFlags'] = _chemesis3_base.ch3_pool_piReactionFlags_set
    __swig_getmethods__['piReactionFlags'] = _chemesis3_base.ch3_pool_piReactionFlags_get
    if _newclass:
        piReactionFlags = _swig_property(_chemesis3_base.ch3_pool_piReactionFlags_get, _chemesis3_base.ch3_pool_piReactionFlags_set)
    __swig_setmethods__['iPools'] = _chemesis3_base.ch3_pool_iPools_set
    __swig_getmethods__['iPools'] = _chemesis3_base.ch3_pool_iPools_get
    if _newclass:
        iPools = _swig_property(_chemesis3_base.ch3_pool_iPools_get, _chemesis3_base.ch3_pool_iPools_set)
    __swig_setmethods__['piPools'] = _chemesis3_base.ch3_pool_piPools_set
    __swig_getmethods__['piPools'] = _chemesis3_base.ch3_pool_piPools_get
    if _newclass:
        piPools = _swig_property(_chemesis3_base.ch3_pool_piPools_get, _chemesis3_base.ch3_pool_piPools_set)
    __swig_setmethods__['piPoolsFlags'] = _chemesis3_base.ch3_pool_piPoolsFlags_set
    __swig_getmethods__['piPoolsFlags'] = _chemesis3_base.ch3_pool_piPoolsFlags_get
    if _newclass:
        piPoolsFlags = _swig_property(_chemesis3_base.ch3_pool_piPoolsFlags_get, _chemesis3_base.ch3_pool_piPoolsFlags_set)
    __swig_setmethods__['iDiffusions'] = _chemesis3_base.ch3_pool_iDiffusions_set
    __swig_getmethods__['iDiffusions'] = _chemesis3_base.ch3_pool_iDiffusions_get
    if _newclass:
        iDiffusions = _swig_property(_chemesis3_base.ch3_pool_iDiffusions_get, _chemesis3_base.ch3_pool_iDiffusions_set)
    __swig_setmethods__['piDiffusions'] = _chemesis3_base.ch3_pool_piDiffusions_set
    __swig_getmethods__['piDiffusions'] = _chemesis3_base.ch3_pool_piDiffusions_get
    if _newclass:
        piDiffusions = _swig_property(_chemesis3_base.ch3_pool_piDiffusions_get, _chemesis3_base.ch3_pool_piDiffusions_set)
    __swig_setmethods__['piDiffusionsFlags'] = _chemesis3_base.ch3_pool_piDiffusionsFlags_set
    __swig_getmethods__['piDiffusionsFlags'] = _chemesis3_base.ch3_pool_piDiffusionsFlags_get
    if _newclass:
        piDiffusionsFlags = _swig_property(_chemesis3_base.ch3_pool_piDiffusionsFlags_get, _chemesis3_base.ch3_pool_piDiffusionsFlags_set)
    __swig_setmethods__['dConcentrationInit'] = _chemesis3_base.ch3_pool_dConcentrationInit_set
    __swig_getmethods__['dConcentrationInit'] = _chemesis3_base.ch3_pool_dConcentrationInit_get
    if _newclass:
        dConcentrationInit = _swig_property(_chemesis3_base.ch3_pool_dConcentrationInit_get, _chemesis3_base.ch3_pool_dConcentrationInit_set)
    __swig_setmethods__['dConcentration'] = _chemesis3_base.ch3_pool_dConcentration_set
    __swig_getmethods__['dConcentration'] = _chemesis3_base.ch3_pool_dConcentration_get
    if _newclass:
        dConcentration = _swig_property(_chemesis3_base.ch3_pool_dConcentration_get, _chemesis3_base.ch3_pool_dConcentration_set)
    __swig_setmethods__['dVolume'] = _chemesis3_base.ch3_pool_dVolume_set
    __swig_getmethods__['dVolume'] = _chemesis3_base.ch3_pool_dVolume_get
    if _newclass:
        dVolume = _swig_property(_chemesis3_base.ch3_pool_dVolume_get, _chemesis3_base.ch3_pool_dVolume_set)
    __swig_setmethods__['dUnits'] = _chemesis3_base.ch3_pool_dUnits_set
    __swig_getmethods__['dUnits'] = _chemesis3_base.ch3_pool_dUnits_get
    if _newclass:
        dUnits = _swig_property(_chemesis3_base.ch3_pool_dUnits_get, _chemesis3_base.ch3_pool_dUnits_set)
    __swig_setmethods__['dQuantity'] = _chemesis3_base.ch3_pool_dQuantity_set
    __swig_getmethods__['dQuantity'] = _chemesis3_base.ch3_pool_dQuantity_get
    if _newclass:
        dQuantity = _swig_property(_chemesis3_base.ch3_pool_dQuantity_get, _chemesis3_base.ch3_pool_dQuantity_set)
    __swig_setmethods__['iConserve'] = _chemesis3_base.ch3_pool_iConserve_set
    __swig_getmethods__['iConserve'] = _chemesis3_base.ch3_pool_iConserve_get
    if _newclass:
        iConserve = _swig_property(_chemesis3_base.ch3_pool_iConserve_get, _chemesis3_base.ch3_pool_iConserve_set)
    __swig_setmethods__['dQuantityTotal'] = _chemesis3_base.ch3_pool_dQuantityTotal_set
    __swig_getmethods__['dQuantityTotal'] = _chemesis3_base.ch3_pool_dQuantityTotal_get
    if _newclass:
        dQuantityTotal = _swig_property(_chemesis3_base.ch3_pool_dQuantityTotal_get, _chemesis3_base.ch3_pool_dQuantityTotal_set)
    __swig_setmethods__['dConcentrationTotal'] = _chemesis3_base.ch3_pool_dConcentrationTotal_set
    __swig_getmethods__['dConcentrationTotal'] = _chemesis3_base.ch3_pool_dConcentrationTotal_get
    if _newclass:
        dConcentrationTotal = _swig_property(_chemesis3_base.ch3_pool_dConcentrationTotal_get, _chemesis3_base.ch3_pool_dConcentrationTotal_set)

    def __init__(self, *args):
        this = _chemesis3_base.new_ch3_pool(*args)
        try:
            self.this.append(this)
        except:
            self.this = this

    __swig_destroy__ = _chemesis3_base.delete_ch3_pool
    __del__ = lambda self: None


ch3_pool_swigregister = _chemesis3_base.ch3_pool_swigregister
ch3_pool_swigregister(ch3_pool)

class ch3_reaction(_object):
    __swig_setmethods__ = {}
    __setattr__ = lambda self, name, value: _swig_setattr(self, ch3_reaction, name, value)
    __swig_getmethods__ = {}
    __getattr__ = lambda self, name: _swig_getattr(self, ch3_reaction, name)
    __repr__ = _swig_repr
    __swig_setmethods__['mc'] = _chemesis3_base.ch3_reaction_mc_set
    __swig_getmethods__['mc'] = _chemesis3_base.ch3_reaction_mc_get
    if _newclass:
        mc = _swig_property(_chemesis3_base.ch3_reaction_mc_get, _chemesis3_base.ch3_reaction_mc_set)
    __swig_setmethods__['iSubstrates'] = _chemesis3_base.ch3_reaction_iSubstrates_set
    __swig_getmethods__['iSubstrates'] = _chemesis3_base.ch3_reaction_iSubstrates_get
    if _newclass:
        iSubstrates = _swig_property(_chemesis3_base.ch3_reaction_iSubstrates_get, _chemesis3_base.ch3_reaction_iSubstrates_set)
    __swig_setmethods__['piSubstrates'] = _chemesis3_base.ch3_reaction_piSubstrates_set
    __swig_getmethods__['piSubstrates'] = _chemesis3_base.ch3_reaction_piSubstrates_get
    if _newclass:
        piSubstrates = _swig_property(_chemesis3_base.ch3_reaction_piSubstrates_get, _chemesis3_base.ch3_reaction_piSubstrates_set)
    __swig_setmethods__['iProducts'] = _chemesis3_base.ch3_reaction_iProducts_set
    __swig_getmethods__['iProducts'] = _chemesis3_base.ch3_reaction_iProducts_get
    if _newclass:
        iProducts = _swig_property(_chemesis3_base.ch3_reaction_iProducts_get, _chemesis3_base.ch3_reaction_iProducts_set)
    __swig_setmethods__['piProducts'] = _chemesis3_base.ch3_reaction_piProducts_set
    __swig_getmethods__['piProducts'] = _chemesis3_base.ch3_reaction_piProducts_get
    if _newclass:
        piProducts = _swig_property(_chemesis3_base.ch3_reaction_piProducts_get, _chemesis3_base.ch3_reaction_piProducts_set)
    __swig_setmethods__['dBackwardRate'] = _chemesis3_base.ch3_reaction_dBackwardRate_set
    __swig_getmethods__['dBackwardRate'] = _chemesis3_base.ch3_reaction_dBackwardRate_get
    if _newclass:
        dBackwardRate = _swig_property(_chemesis3_base.ch3_reaction_dBackwardRate_get, _chemesis3_base.ch3_reaction_dBackwardRate_set)
    __swig_setmethods__['dBackwardSolved'] = _chemesis3_base.ch3_reaction_dBackwardSolved_set
    __swig_getmethods__['dBackwardSolved'] = _chemesis3_base.ch3_reaction_dBackwardSolved_get
    if _newclass:
        dBackwardSolved = _swig_property(_chemesis3_base.ch3_reaction_dBackwardSolved_get, _chemesis3_base.ch3_reaction_dBackwardSolved_set)
    __swig_setmethods__['dForwardRate'] = _chemesis3_base.ch3_reaction_dForwardRate_set
    __swig_getmethods__['dForwardRate'] = _chemesis3_base.ch3_reaction_dForwardRate_get
    if _newclass:
        dForwardRate = _swig_property(_chemesis3_base.ch3_reaction_dForwardRate_get, _chemesis3_base.ch3_reaction_dForwardRate_set)
    __swig_setmethods__['dForwardSolved'] = _chemesis3_base.ch3_reaction_dForwardSolved_set
    __swig_getmethods__['dForwardSolved'] = _chemesis3_base.ch3_reaction_dForwardSolved_get
    if _newclass:
        dForwardSolved = _swig_property(_chemesis3_base.ch3_reaction_dForwardSolved_get, _chemesis3_base.ch3_reaction_dForwardSolved_set)

    def __init__(self, *args):
        this = _chemesis3_base.new_ch3_reaction(*args)
        try:
            self.this.append(this)
        except:
            self.this = this

    __swig_destroy__ = _chemesis3_base.delete_ch3_reaction
    __del__ = lambda self: None


ch3_reaction_swigregister = _chemesis3_base.ch3_reaction_swigregister
ch3_reaction_swigregister(ch3_reaction)

class ch3_diffusion(_object):
    __swig_setmethods__ = {}
    __setattr__ = lambda self, name, value: _swig_setattr(self, ch3_diffusion, name, value)
    __swig_getmethods__ = {}
    __getattr__ = lambda self, name: _swig_getattr(self, ch3_diffusion, name)
    __repr__ = _swig_repr
    __swig_setmethods__['mc'] = _chemesis3_base.ch3_diffusion_mc_set
    __swig_getmethods__['mc'] = _chemesis3_base.ch3_diffusion_mc_get
    if _newclass:
        mc = _swig_property(_chemesis3_base.ch3_diffusion_mc_get, _chemesis3_base.ch3_diffusion_mc_set)
    __swig_setmethods__['dDiffusionConstant'] = _chemesis3_base.ch3_diffusion_dDiffusionConstant_set
    __swig_getmethods__['dDiffusionConstant'] = _chemesis3_base.ch3_diffusion_dDiffusionConstant_get
    if _newclass:
        dDiffusionConstant = _swig_property(_chemesis3_base.ch3_diffusion_dDiffusionConstant_get, _chemesis3_base.ch3_diffusion_dDiffusionConstant_set)
    __swig_setmethods__['ppool1'] = _chemesis3_base.ch3_diffusion_ppool1_set
    __swig_getmethods__['ppool1'] = _chemesis3_base.ch3_diffusion_ppool1_get
    if _newclass:
        ppool1 = _swig_property(_chemesis3_base.ch3_diffusion_ppool1_get, _chemesis3_base.ch3_diffusion_ppool1_set)
    __swig_setmethods__['ppool2'] = _chemesis3_base.ch3_diffusion_ppool2_set
    __swig_getmethods__['ppool2'] = _chemesis3_base.ch3_diffusion_ppool2_get
    if _newclass:
        ppool2 = _swig_property(_chemesis3_base.ch3_diffusion_ppool2_get, _chemesis3_base.ch3_diffusion_ppool2_set)
    __swig_setmethods__['dLength1'] = _chemesis3_base.ch3_diffusion_dLength1_set
    __swig_getmethods__['dLength1'] = _chemesis3_base.ch3_diffusion_dLength1_get
    if _newclass:
        dLength1 = _swig_property(_chemesis3_base.ch3_diffusion_dLength1_get, _chemesis3_base.ch3_diffusion_dLength1_set)
    __swig_setmethods__['dArea1'] = _chemesis3_base.ch3_diffusion_dArea1_set
    __swig_getmethods__['dArea1'] = _chemesis3_base.ch3_diffusion_dArea1_get
    if _newclass:
        dArea1 = _swig_property(_chemesis3_base.ch3_diffusion_dArea1_get, _chemesis3_base.ch3_diffusion_dArea1_set)
    __swig_setmethods__['dLength2'] = _chemesis3_base.ch3_diffusion_dLength2_set
    __swig_getmethods__['dLength2'] = _chemesis3_base.ch3_diffusion_dLength2_get
    if _newclass:
        dLength2 = _swig_property(_chemesis3_base.ch3_diffusion_dLength2_get, _chemesis3_base.ch3_diffusion_dLength2_set)
    __swig_setmethods__['dArea2'] = _chemesis3_base.ch3_diffusion_dArea2_set
    __swig_getmethods__['dArea2'] = _chemesis3_base.ch3_diffusion_dArea2_get
    if _newclass:
        dArea2 = _swig_property(_chemesis3_base.ch3_diffusion_dArea2_get, _chemesis3_base.ch3_diffusion_dArea2_set)
    __swig_setmethods__['dFlux1'] = _chemesis3_base.ch3_diffusion_dFlux1_set
    __swig_getmethods__['dFlux1'] = _chemesis3_base.ch3_diffusion_dFlux1_get
    if _newclass:
        dFlux1 = _swig_property(_chemesis3_base.ch3_diffusion_dFlux1_get, _chemesis3_base.ch3_diffusion_dFlux1_set)
    __swig_setmethods__['dFlux2'] = _chemesis3_base.ch3_diffusion_dFlux2_set
    __swig_getmethods__['dFlux2'] = _chemesis3_base.ch3_diffusion_dFlux2_get
    if _newclass:
        dFlux2 = _swig_property(_chemesis3_base.ch3_diffusion_dFlux2_get, _chemesis3_base.ch3_diffusion_dFlux2_set)
    __swig_setmethods__['dUnits'] = _chemesis3_base.ch3_diffusion_dUnits_set
    __swig_getmethods__['dUnits'] = _chemesis3_base.ch3_diffusion_dUnits_get
    if _newclass:
        dUnits = _swig_property(_chemesis3_base.ch3_diffusion_dUnits_get, _chemesis3_base.ch3_diffusion_dUnits_set)

    def __init__(self, *args):
        this = _chemesis3_base.new_ch3_diffusion(*args)
        try:
            self.this.append(this)
        except:
            self.this = this

    __swig_destroy__ = _chemesis3_base.delete_ch3_diffusion
    __del__ = lambda self: None


ch3_diffusion_swigregister = _chemesis3_base.ch3_diffusion_swigregister
ch3_diffusion_swigregister(ch3_diffusion)

class ch3_species(_object):
    __swig_setmethods__ = {}
    __setattr__ = lambda self, name, value: _swig_setattr(self, ch3_species, name, value)
    __swig_getmethods__ = {}
    __getattr__ = lambda self, name: _swig_getattr(self, ch3_species, name)
    __repr__ = _swig_repr
    __swig_setmethods__['dValency'] = _chemesis3_base.ch3_species_dValency_set
    __swig_getmethods__['dValency'] = _chemesis3_base.ch3_species_dValency_get
    if _newclass:
        dValency = _swig_property(_chemesis3_base.ch3_species_dValency_get, _chemesis3_base.ch3_species_dValency_set)
    __swig_setmethods__['iPools'] = _chemesis3_base.ch3_species_iPools_set
    __swig_getmethods__['iPools'] = _chemesis3_base.ch3_species_iPools_get
    if _newclass:
        iPools = _swig_property(_chemesis3_base.ch3_species_iPools_get, _chemesis3_base.ch3_species_iPools_set)
    __swig_setmethods__['ppool'] = _chemesis3_base.ch3_species_ppool_set
    __swig_getmethods__['ppool'] = _chemesis3_base.ch3_species_ppool_get
    if _newclass:
        ppool = _swig_property(_chemesis3_base.ch3_species_ppool_get, _chemesis3_base.ch3_species_ppool_set)

    def __init__(self, *args):
        this = _chemesis3_base.new_ch3_species(*args)
        try:
            self.this.append(this)
        except:
            self.this = this

    __swig_destroy__ = _chemesis3_base.delete_ch3_species
    __del__ = lambda self: None


ch3_species_swigregister = _chemesis3_base.ch3_species_swigregister
ch3_species_swigregister(ch3_species)

class Chemesis3Options(_object):
    __swig_setmethods__ = {}
    __setattr__ = lambda self, name, value: _swig_setattr(self, Chemesis3Options, name, value)
    __swig_getmethods__ = {}
    __getattr__ = lambda self, name: _swig_getattr(self, Chemesis3Options, name)
    __repr__ = _swig_repr
    __swig_setmethods__['iOptions'] = _chemesis3_base.Chemesis3Options_iOptions_set
    __swig_getmethods__['iOptions'] = _chemesis3_base.Chemesis3Options_iOptions_get
    if _newclass:
        iOptions = _swig_property(_chemesis3_base.Chemesis3Options_iOptions_get, _chemesis3_base.Chemesis3Options_iOptions_set)

    def __init__(self, *args):
        this = _chemesis3_base.new_Chemesis3Options(*args)
        try:
            self.this.append(this)
        except:
            self.this = this

    __swig_destroy__ = _chemesis3_base.delete_Chemesis3Options
    __del__ = lambda self: None


Chemesis3Options_swigregister = _chemesis3_base.Chemesis3Options_swigregister
Chemesis3Options_swigregister(Chemesis3Options)

class simobj_Chemesis3(_object):
    __swig_setmethods__ = {}
    __setattr__ = lambda self, name, value: _swig_setattr(self, simobj_Chemesis3, name, value)
    __swig_getmethods__ = {}
    __getattr__ = lambda self, name: _swig_getattr(self, simobj_Chemesis3, name)
    __repr__ = _swig_repr
    __swig_setmethods__['pcName'] = _chemesis3_base.simobj_Chemesis3_pcName_set
    __swig_getmethods__['pcName'] = _chemesis3_base.simobj_Chemesis3_pcName_get
    if _newclass:
        pcName = _swig_property(_chemesis3_base.simobj_Chemesis3_pcName_get, _chemesis3_base.simobj_Chemesis3_pcName_set)
    __swig_setmethods__['iStatus'] = _chemesis3_base.simobj_Chemesis3_iStatus_set
    __swig_getmethods__['iStatus'] = _chemesis3_base.simobj_Chemesis3_iStatus_get
    if _newclass:
        iStatus = _swig_property(_chemesis3_base.simobj_Chemesis3_iStatus_get, _chemesis3_base.simobj_Chemesis3_iStatus_set)
    __swig_setmethods__['iErrorCount'] = _chemesis3_base.simobj_Chemesis3_iErrorCount_set
    __swig_getmethods__['iErrorCount'] = _chemesis3_base.simobj_Chemesis3_iErrorCount_get
    if _newclass:
        iErrorCount = _swig_property(_chemesis3_base.simobj_Chemesis3_iErrorCount_get, _chemesis3_base.simobj_Chemesis3_iErrorCount_set)
    __swig_setmethods__['iSerialStart'] = _chemesis3_base.simobj_Chemesis3_iSerialStart_set
    __swig_getmethods__['iSerialStart'] = _chemesis3_base.simobj_Chemesis3_iSerialStart_get
    if _newclass:
        iSerialStart = _swig_property(_chemesis3_base.simobj_Chemesis3_iSerialStart_get, _chemesis3_base.simobj_Chemesis3_iSerialStart_set)
    __swig_setmethods__['iSerialEnd'] = _chemesis3_base.simobj_Chemesis3_iSerialEnd_set
    __swig_getmethods__['iSerialEnd'] = _chemesis3_base.simobj_Chemesis3_iSerialEnd_get
    if _newclass:
        iSerialEnd = _swig_property(_chemesis3_base.simobj_Chemesis3_iSerialEnd_get, _chemesis3_base.simobj_Chemesis3_iSerialEnd_set)
    __swig_setmethods__['c3o'] = _chemesis3_base.simobj_Chemesis3_c3o_set
    __swig_getmethods__['c3o'] = _chemesis3_base.simobj_Chemesis3_c3o_get
    if _newclass:
        c3o = _swig_property(_chemesis3_base.simobj_Chemesis3_c3o_get, _chemesis3_base.simobj_Chemesis3_c3o_set)
    __swig_setmethods__['dTime'] = _chemesis3_base.simobj_Chemesis3_dTime_set
    __swig_getmethods__['dTime'] = _chemesis3_base.simobj_Chemesis3_dTime_get
    if _newclass:
        dTime = _swig_property(_chemesis3_base.simobj_Chemesis3_dTime_get, _chemesis3_base.simobj_Chemesis3_dTime_set)
    __swig_setmethods__['dStep'] = _chemesis3_base.simobj_Chemesis3_dStep_set
    __swig_getmethods__['dStep'] = _chemesis3_base.simobj_Chemesis3_dStep_get
    if _newclass:
        dStep = _swig_property(_chemesis3_base.simobj_Chemesis3_dStep_get, _chemesis3_base.simobj_Chemesis3_dStep_set)
    __swig_setmethods__['pcts'] = _chemesis3_base.simobj_Chemesis3_pcts_set
    __swig_getmethods__['pcts'] = _chemesis3_base.simobj_Chemesis3_pcts_get
    if _newclass:
        pcts = _swig_property(_chemesis3_base.simobj_Chemesis3_pcts_get, _chemesis3_base.simobj_Chemesis3_pcts_set)
    __swig_setmethods__['ped'] = _chemesis3_base.simobj_Chemesis3_ped_set
    __swig_getmethods__['ped'] = _chemesis3_base.simobj_Chemesis3_ped_get
    if _newclass:
        ped = _swig_property(_chemesis3_base.simobj_Chemesis3_ped_get, _chemesis3_base.simobj_Chemesis3_ped_set)
    __swig_setmethods__['peq'] = _chemesis3_base.simobj_Chemesis3_peq_set
    __swig_getmethods__['peq'] = _chemesis3_base.simobj_Chemesis3_peq_get
    if _newclass:
        peq = _swig_property(_chemesis3_base.simobj_Chemesis3_peq_get, _chemesis3_base.simobj_Chemesis3_peq_set)
    __swig_setmethods__['dConcentrationMinimum'] = _chemesis3_base.simobj_Chemesis3_dConcentrationMinimum_set
    __swig_getmethods__['dConcentrationMinimum'] = _chemesis3_base.simobj_Chemesis3_dConcentrationMinimum_get
    if _newclass:
        dConcentrationMinimum = _swig_property(_chemesis3_base.simobj_Chemesis3_dConcentrationMinimum_get, _chemesis3_base.simobj_Chemesis3_dConcentrationMinimum_set)
    __swig_setmethods__['iPools'] = _chemesis3_base.simobj_Chemesis3_iPools_set
    __swig_getmethods__['iPools'] = _chemesis3_base.simobj_Chemesis3_iPools_get
    if _newclass:
        iPools = _swig_property(_chemesis3_base.simobj_Chemesis3_iPools_get, _chemesis3_base.simobj_Chemesis3_iPools_set)
    __swig_setmethods__['ppool'] = _chemesis3_base.simobj_Chemesis3_ppool_set
    __swig_getmethods__['ppool'] = _chemesis3_base.simobj_Chemesis3_ppool_get
    if _newclass:
        ppool = _swig_property(_chemesis3_base.simobj_Chemesis3_ppool_get, _chemesis3_base.simobj_Chemesis3_ppool_set)
    __swig_setmethods__['iReactions'] = _chemesis3_base.simobj_Chemesis3_iReactions_set
    __swig_getmethods__['iReactions'] = _chemesis3_base.simobj_Chemesis3_iReactions_get
    if _newclass:
        iReactions = _swig_property(_chemesis3_base.simobj_Chemesis3_iReactions_get, _chemesis3_base.simobj_Chemesis3_iReactions_set)
    __swig_setmethods__['preaction'] = _chemesis3_base.simobj_Chemesis3_preaction_set
    __swig_getmethods__['preaction'] = _chemesis3_base.simobj_Chemesis3_preaction_get
    if _newclass:
        preaction = _swig_property(_chemesis3_base.simobj_Chemesis3_preaction_get, _chemesis3_base.simobj_Chemesis3_preaction_set)
    __swig_setmethods__['iDiffusions'] = _chemesis3_base.simobj_Chemesis3_iDiffusions_set
    __swig_getmethods__['iDiffusions'] = _chemesis3_base.simobj_Chemesis3_iDiffusions_get
    if _newclass:
        iDiffusions = _swig_property(_chemesis3_base.simobj_Chemesis3_iDiffusions_get, _chemesis3_base.simobj_Chemesis3_iDiffusions_set)
    __swig_setmethods__['pdiffusion'] = _chemesis3_base.simobj_Chemesis3_pdiffusion_set
    __swig_getmethods__['pdiffusion'] = _chemesis3_base.simobj_Chemesis3_pdiffusion_get
    if _newclass:
        pdiffusion = _swig_property(_chemesis3_base.simobj_Chemesis3_pdiffusion_get, _chemesis3_base.simobj_Chemesis3_pdiffusion_set)
    __swig_setmethods__['iSpecies'] = _chemesis3_base.simobj_Chemesis3_iSpecies_set
    __swig_getmethods__['iSpecies'] = _chemesis3_base.simobj_Chemesis3_iSpecies_get
    if _newclass:
        iSpecies = _swig_property(_chemesis3_base.simobj_Chemesis3_iSpecies_get, _chemesis3_base.simobj_Chemesis3_iSpecies_set)
    __swig_setmethods__['pspecies'] = _chemesis3_base.simobj_Chemesis3_pspecies_set
    __swig_getmethods__['pspecies'] = _chemesis3_base.simobj_Chemesis3_pspecies_get
    if _newclass:
        pspecies = _swig_property(_chemesis3_base.simobj_Chemesis3_pspecies_get, _chemesis3_base.simobj_Chemesis3_pspecies_set)
    __swig_setmethods__['iAggregators'] = _chemesis3_base.simobj_Chemesis3_iAggregators_set
    __swig_getmethods__['iAggregators'] = _chemesis3_base.simobj_Chemesis3_iAggregators_get
    if _newclass:
        iAggregators = _swig_property(_chemesis3_base.simobj_Chemesis3_iAggregators_get, _chemesis3_base.simobj_Chemesis3_iAggregators_set)
    __swig_setmethods__['pdAggregators'] = _chemesis3_base.simobj_Chemesis3_pdAggregators_set
    __swig_getmethods__['pdAggregators'] = _chemesis3_base.simobj_Chemesis3_pdAggregators_get
    if _newclass:
        pdAggregators = _swig_property(_chemesis3_base.simobj_Chemesis3_pdAggregators_get, _chemesis3_base.simobj_Chemesis3_pdAggregators_set)

    def __init__(self, *args):
        this = _chemesis3_base.new_simobj_Chemesis3(*args)
        try:
            self.this.append(this)
        except:
            self.this = this

    __swig_destroy__ = _chemesis3_base.delete_simobj_Chemesis3
    __del__ = lambda self: None


simobj_Chemesis3_swigregister = _chemesis3_base.simobj_Chemesis3_swigregister
simobj_Chemesis3_swigregister(simobj_Chemesis3)
CHEMESIS3_STATUS_PHASE_0 = _chemesis3_base.CHEMESIS3_STATUS_PHASE_0
CHEMESIS3_STATUS_PHASE_1 = _chemesis3_base.CHEMESIS3_STATUS_PHASE_1
CHEMESIS3_STATUS_PHASE_2 = _chemesis3_base.CHEMESIS3_STATUS_PHASE_2
CHEMESIS3_STATUS_PHASE_3 = _chemesis3_base.CHEMESIS3_STATUS_PHASE_3
CHEMESIS3_STATUS_PHASE_4 = _chemesis3_base.CHEMESIS3_STATUS_PHASE_4
CHEMESIS3_STATUS_PHASE_5 = _chemesis3_base.CHEMESIS3_STATUS_PHASE_5
Chemesis3Advance = _chemesis3_base.Chemesis3Advance
Chemesis3CompileP1 = _chemesis3_base.Chemesis3CompileP1
Chemesis3Error = _chemesis3_base.Chemesis3Error
Chemesis3GetVersion = _chemesis3_base.Chemesis3GetVersion
Chemesis3Initiate = _chemesis3_base.Chemesis3Initiate
Chemesis3NewP2 = _chemesis3_base.Chemesis3NewP2
Chemesis3SingleStep = _chemesis3_base.Chemesis3SingleStep
Chemesis3SingleStepDiffusions = _chemesis3_base.Chemesis3SingleStepDiffusions
Chemesis3SingleStepPools = _chemesis3_base.Chemesis3SingleStepPools
Chemesis3SingleStepReactions = _chemesis3_base.Chemesis3SingleStepReactions

class ch3_MathComponent(_object):
    __swig_setmethods__ = {}
    __setattr__ = lambda self, name, value: _swig_setattr(self, ch3_MathComponent, name, value)
    __swig_getmethods__ = {}
    __getattr__ = lambda self, name: _swig_getattr(self, ch3_MathComponent, name)
    __repr__ = _swig_repr
    __swig_setmethods__['iType'] = _chemesis3_base.ch3_MathComponent_iType_set
    __swig_getmethods__['iType'] = _chemesis3_base.ch3_MathComponent_iType_get
    if _newclass:
        iType = _swig_property(_chemesis3_base.ch3_MathComponent_iType_get, _chemesis3_base.ch3_MathComponent_iType_set)
    __swig_setmethods__['iSerial'] = _chemesis3_base.ch3_MathComponent_iSerial_set
    __swig_getmethods__['iSerial'] = _chemesis3_base.ch3_MathComponent_iSerial_get
    if _newclass:
        iSerial = _swig_property(_chemesis3_base.ch3_MathComponent_iSerial_get, _chemesis3_base.ch3_MathComponent_iSerial_set)
    __swig_setmethods__['iPrototype'] = _chemesis3_base.ch3_MathComponent_iPrototype_set
    __swig_getmethods__['iPrototype'] = _chemesis3_base.ch3_MathComponent_iPrototype_get
    if _newclass:
        iPrototype = _swig_property(_chemesis3_base.ch3_MathComponent_iPrototype_get, _chemesis3_base.ch3_MathComponent_iPrototype_set)

    def __init__(self, *args):
        this = _chemesis3_base.new_ch3_MathComponent(*args)
        try:
            self.this.append(this)
        except:
            self.this = this

    __swig_destroy__ = _chemesis3_base.delete_ch3_MathComponent
    __del__ = lambda self: None


ch3_MathComponent_swigregister = _chemesis3_base.ch3_MathComponent_swigregister
ch3_MathComponent_swigregister(ch3_MathComponent)
MATH_TYPE_Pool = _chemesis3_base.MATH_TYPE_Pool
MATH_TYPE_Reaction = _chemesis3_base.MATH_TYPE_Reaction
MATH_TYPE_Diffusion = _chemesis3_base.MATH_TYPE_Diffusion

class Chemesis3TranslationService(_object):
    __swig_setmethods__ = {}
    __setattr__ = lambda self, name, value: _swig_setattr(self, Chemesis3TranslationService, name, value)
    __swig_getmethods__ = {}
    __getattr__ = lambda self, name: _swig_getattr(self, Chemesis3TranslationService, name)
    __repr__ = _swig_repr
    __swig_setmethods__['pctsd'] = _chemesis3_base.Chemesis3TranslationService_pctsd_set
    __swig_getmethods__['pctsd'] = _chemesis3_base.Chemesis3TranslationService_pctsd_get
    if _newclass:
        pctsd = _swig_property(_chemesis3_base.Chemesis3TranslationService_pctsd_get, _chemesis3_base.Chemesis3TranslationService_pctsd_set)
    __swig_setmethods__['kinetic_inspector'] = _chemesis3_base.Chemesis3TranslationService_kinetic_inspector_set
    __swig_getmethods__['kinetic_inspector'] = _chemesis3_base.Chemesis3TranslationService_kinetic_inspector_get
    if _newclass:
        kinetic_inspector = _swig_property(_chemesis3_base.Chemesis3TranslationService_kinetic_inspector_get, _chemesis3_base.Chemesis3TranslationService_kinetic_inspector_set)

    def __init__(self, *args):
        this = _chemesis3_base.new_Chemesis3TranslationService(*args)
        try:
            self.this.append(this)
        except:
            self.this = this

    __swig_destroy__ = _chemesis3_base.delete_Chemesis3TranslationService
    __del__ = lambda self: None


Chemesis3TranslationService_swigregister = _chemesis3_base.Chemesis3TranslationService_swigregister
Chemesis3TranslationService_swigregister(Chemesis3TranslationService)
PRE_PROTO_TRAVERSAL = _chemesis3_base.PRE_PROTO_TRAVERSAL

class Chemesis3TranslationServiceData(_object):
    __swig_setmethods__ = {}
    __setattr__ = lambda self, name, value: _swig_setattr(self, Chemesis3TranslationServiceData, name, value)
    __swig_getmethods__ = {}
    __getattr__ = lambda self, name: _swig_getattr(self, Chemesis3TranslationServiceData, name)
    __repr__ = _swig_repr
    __swig_setmethods__['pneuro'] = _chemesis3_base.Chemesis3TranslationServiceData_pneuro_set
    __swig_getmethods__['pneuro'] = _chemesis3_base.Chemesis3TranslationServiceData_pneuro_get
    if _newclass:
        pneuro = _swig_property(_chemesis3_base.Chemesis3TranslationServiceData_pneuro_get, _chemesis3_base.Chemesis3TranslationServiceData_pneuro_set)
    __swig_setmethods__['ppistRoot'] = _chemesis3_base.Chemesis3TranslationServiceData_ppistRoot_set
    __swig_getmethods__['ppistRoot'] = _chemesis3_base.Chemesis3TranslationServiceData_ppistRoot_get
    if _newclass:
        ppistRoot = _swig_property(_chemesis3_base.Chemesis3TranslationServiceData_ppistRoot_get, _chemesis3_base.Chemesis3TranslationServiceData_ppistRoot_set)
    __swig_setmethods__['phsleRoot'] = _chemesis3_base.Chemesis3TranslationServiceData_phsleRoot_set
    __swig_getmethods__['phsleRoot'] = _chemesis3_base.Chemesis3TranslationServiceData_phsleRoot_get
    if _newclass:
        phsleRoot = _swig_property(_chemesis3_base.Chemesis3TranslationServiceData_phsleRoot_get, _chemesis3_base.Chemesis3TranslationServiceData_phsleRoot_set)
    __swig_setmethods__['iModel'] = _chemesis3_base.Chemesis3TranslationServiceData_iModel_set
    __swig_getmethods__['iModel'] = _chemesis3_base.Chemesis3TranslationServiceData_iModel_get
    if _newclass:
        iModel = _swig_property(_chemesis3_base.Chemesis3TranslationServiceData_iModel_get, _chemesis3_base.Chemesis3TranslationServiceData_iModel_set)

    def __init__(self, *args):
        this = _chemesis3_base.new_Chemesis3TranslationServiceData(*args)
        try:
            self.this.append(this)
        except:
            self.this = this

    __swig_destroy__ = _chemesis3_base.delete_Chemesis3TranslationServiceData
    __del__ = lambda self: None


Chemesis3TranslationServiceData_swigregister = _chemesis3_base.Chemesis3TranslationServiceData_swigregister
Chemesis3TranslationServiceData_swigregister(Chemesis3TranslationServiceData)
Chemesis3ConnectDistributor = _chemesis3_base.Chemesis3ConnectDistributor
Chemesis3ConnectQueuer = _chemesis3_base.Chemesis3ConnectQueuer
Chemesis3Construct = _chemesis3_base.Chemesis3Construct
Chemesis3NeurospacesKinetics2Chemesis3 = _chemesis3_base.Chemesis3NeurospacesKinetics2Chemesis3
new_Chemesis3PoolPointer = _chemesis3_base.new_Chemesis3PoolPointer
copy_Chemesis3PoolPointer = _chemesis3_base.copy_Chemesis3PoolPointer
delete_Chemesis3PoolPointer = _chemesis3_base.delete_Chemesis3PoolPointer
Chemesis3PoolPointer_assign = _chemesis3_base.Chemesis3PoolPointer_assign
Chemesis3PoolPointer_value = _chemesis3_base.Chemesis3PoolPointer_value
new_DoubleArray = _chemesis3_base.new_DoubleArray
delete_DoubleArray = _chemesis3_base.delete_DoubleArray
DoubleArray_getitem = _chemesis3_base.DoubleArray_getitem
DoubleArray_setitem = _chemesis3_base.DoubleArray_setitem
new_IntArray = _chemesis3_base.new_IntArray
delete_IntArray = _chemesis3_base.delete_IntArray
IntArray_getitem = _chemesis3_base.IntArray_getitem
IntArray_setitem = _chemesis3_base.IntArray_setitem
new_Chemesis3PoolArray = _chemesis3_base.new_Chemesis3PoolArray
delete_Chemesis3PoolArray = _chemesis3_base.delete_Chemesis3PoolArray
Chemesis3PoolArray_getitem = _chemesis3_base.Chemesis3PoolArray_getitem
Chemesis3PoolArray_setitem = _chemesis3_base.Chemesis3PoolArray_setitem
new_Chemesis3ReactionArray = _chemesis3_base.new_Chemesis3ReactionArray
delete_Chemesis3ReactionArray = _chemesis3_base.delete_Chemesis3ReactionArray
Chemesis3ReactionArray_getitem = _chemesis3_base.Chemesis3ReactionArray_getitem
Chemesis3ReactionArray_setitem = _chemesis3_base.Chemesis3ReactionArray_setitem
new_Chemesis3DiffusionArray = _chemesis3_base.new_Chemesis3DiffusionArray
delete_Chemesis3DiffusionArray = _chemesis3_base.delete_Chemesis3DiffusionArray
Chemesis3DiffusionArray_getitem = _chemesis3_base.Chemesis3DiffusionArray_getitem
Chemesis3DiffusionArray_setitem = _chemesis3_base.Chemesis3DiffusionArray_setitem