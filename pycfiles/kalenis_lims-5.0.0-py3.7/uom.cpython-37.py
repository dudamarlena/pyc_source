# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/trytond/modules/lims/uom.py
# Compiled at: 2019-01-16 09:41:18
# Size of source mod 2**32: 7621 bytes
from trytond.model import ModelView, ModelSQL, fields, Unique
from trytond.pool import Pool, PoolMeta
from trytond.pyson import Eval
__all__ = [
 'Uom', 'UomCategory', 'UomConversion', 'Template',
 'ConcentrationLevel', 'VolumeConversion']

class Uom(metaclass=PoolMeta):
    __name__ = 'product.uom'
    maximum_concentration = fields.Char('Maximum concentration')
    rsd_horwitz = fields.Char('% RSD Horwitz')

    @classmethod
    def __setup__(cls):
        super(Uom, cls).__setup__()
        cls.symbol.size = 30
        t = cls.__table__()
        cls._sql_constraints += [
         (
          'symbol_uniq', Unique(t, t.symbol),
          'UoM symbol must be unique')]

    def get_rec_name(self, name):
        return self.symbol


class UomCategory(metaclass=PoolMeta):
    __name__ = 'product.uom.category'
    lims_only_available = fields.Boolean('Only available in Lims')

    @staticmethod
    def default_lims_only_available():
        return False


class UomConversion(ModelSQL, ModelView):
    __doc__ = 'Uom Conversion'
    __name__ = 'lims.uom.conversion'
    initial_uom = fields.Many2One('product.uom', 'Initial UoM', required=True, domain=[
     ('category.lims_only_available', '=', True)])
    final_uom = fields.Many2One('product.uom', 'Final UoM', required=True, domain=[
     ('category.lims_only_available', '=', True)])
    initial_uom_volume = fields.Boolean('Volume involved in Initial UoM')
    final_uom_volume = fields.Boolean('Volume involved in Final UoM')
    conversion_formula = fields.Char('Conversion formula')

    @classmethod
    def get_conversion_formula(cls, initial_uom, final_uom):
        return initial_uom and final_uom or None
        values = cls.search([
         (
          'initial_uom', '=', initial_uom),
         (
          'final_uom', '=', final_uom)])
        if values:
            return values[0].conversion_formula


class Template(metaclass=PoolMeta):
    __name__ = 'product.template'

    @classmethod
    def __setup__(cls):
        super(Template, cls).__setup__()
        new_domain = [('category.lims_only_available', '!=', True)]
        cls.default_uom.domain = new_domain


class VolumeConversion(ModelSQL, ModelView):
    __doc__ = 'Volume Conversion'
    __name__ = 'lims.volume.conversion'
    brix = fields.Float('Brix', required=True, digits=(16,
     Eval('brix_digits', 2)),
      depends=['brix_digits'])
    density = fields.Float('Density', required=True, digits=(16,
     Eval('density_digits', 2)),
      depends=['density_digits'])
    soluble_solids = fields.Float('Soluble solids', required=True, digits=(
     16, Eval('soluble_solids_digits', 2)),
      depends=[
     'soluble_solids_digits'])
    brix_digits = fields.Function(fields.Integer('Brix digits'), 'get_configuration_field')
    density_digits = fields.Function(fields.Integer('Density digits'), 'get_configuration_field')
    soluble_solids_digits = fields.Function(fields.Integer('Soluble solids digits'), 'get_configuration_field')

    @classmethod
    def __setup__(cls):
        super(VolumeConversion, cls).__setup__()
        cls._order.insert(0, ('brix', 'ASC'))

    @staticmethod
    def default_brix_digits():
        Config = Pool().get('lims.configuration')
        config = Config(1)
        return getattr(config, 'brix_digits', 2)

    @staticmethod
    def default_density_digits():
        Config = Pool().get('lims.configuration')
        config = Config(1)
        return getattr(config, 'density_digits', 2)

    @staticmethod
    def default_soluble_solids_digits():
        Config = Pool().get('lims.configuration')
        config = Config(1)
        return getattr(config, 'soluble_solids_digits', 2)

    @classmethod
    def get_configuration_field(cls, volume_conversions, names):
        Config = Pool().get('lims.configuration')
        config = Config(1)
        result = {}
        for name in names:
            value = getattr(config, name, 2)
            result[name] = dict(((vc.id, value) for vc in volume_conversions))

        return result

    @classmethod
    def brixToDensity(cls, brix):
        if not brix:
            return
        else:
            brix = float(brix)
            values = cls.search([
             (
              'brix', '=', brix)],
              limit=1)
            if values:
                return values[0].density
            intrpltn = {'x_a':0, 
             'y_a':0, 
             'x_b':0, 
             'y_b':0}
            lower_values = cls.search([
             (
              'brix', '<', brix)],
              order=[
             ('brix', 'DESC')],
              limit=1)
            if not lower_values:
                return
            intrpltn['x_a'] = lower_values[0].brix
            intrpltn['y_a'] = lower_values[0].density
            upper_values = cls.search([
             (
              'brix', '>', brix)],
              order=[
             ('brix', 'ASC')],
              limit=1)
            return upper_values or None
        intrpltn['x_b'] = upper_values[0].brix
        intrpltn['y_b'] = upper_values[0].density
        value = intrpltn['y_a'] + (brix - intrpltn['x_a']) * ((intrpltn['y_b'] - intrpltn['y_a']) / (intrpltn['x_b'] - intrpltn['x_a']))
        return value

    @classmethod
    def brixToSolubleSolids(cls, brix):
        if not brix:
            return
        else:
            brix = float(brix)
            values = cls.search([
             (
              'brix', '=', brix)],
              limit=1)
            if values:
                return values[0].soluble_solids
            intrpltn = {'x_a':0, 
             'y_a':0, 
             'x_b':0, 
             'y_b':0}
            lower_values = cls.search([
             (
              'brix', '<', brix)],
              order=[
             ('brix', 'DESC')],
              limit=1)
            if not lower_values:
                return
            intrpltn['x_a'] = lower_values[0].brix
            intrpltn['y_a'] = lower_values[0].soluble_solids
            upper_values = cls.search([
             (
              'brix', '>', brix)],
              order=[
             ('brix', 'ASC')],
              limit=1)
            return upper_values or None
        intrpltn['x_b'] = upper_values[0].brix
        intrpltn['y_b'] = upper_values[0].soluble_solids
        value = intrpltn['y_a'] + (brix - intrpltn['x_a']) * ((intrpltn['y_b'] - intrpltn['y_a']) / (intrpltn['x_b'] - intrpltn['x_a']))
        return value


class ConcentrationLevel(ModelSQL, ModelView):
    __doc__ = 'Concentration Level'
    __name__ = 'lims.concentration.level'
    _rec_name = 'description'
    code = fields.Char('Code', required=True)
    description = fields.Char('Description', required=True)

    @classmethod
    def __setup__(cls):
        super(ConcentrationLevel, cls).__setup__()
        t = cls.__table__()
        cls._sql_constraints += [
         (
          'code_uniq', Unique(t, t.code),
          'Concentration level code must be unique')]

    def get_rec_name(self, name):
        if self.code:
            return self.code + ' - ' + self.description
        return self.description

    @classmethod
    def search_rec_name(cls, name, clause):
        field = None
        for field in ('code', 'description'):
            records = cls.search([(field,) + tuple(clause[1:])], limit=1)
            if records:
                break

        if records:
            return [
             (
              field,) + tuple(clause[1:])]
        return [
         (
          cls._rec_name,) + tuple(clause[1:])]