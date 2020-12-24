# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ewheeler/dev/pygrowup/pygrowup/pygrowup.py
# Compiled at: 2015-06-26 06:09:56
# Size of source mod 2**32: 22728 bytes
import os, math, decimal, logging, json
from decimal import Decimal as D
from . import exceptions
module_dir = os.path.split(os.path.abspath(__file__))[0]

class Observation(object):

    def __init__(self, indicator, measurement, age_in_months, sex, height, american, logger_name):
        self.logger = logging.getLogger(logger_name)
        self.indicator = indicator
        self.measurement = measurement
        self.position = None
        self.age = D(age_in_months)
        self.sex = sex.upper()
        self.height = height
        self.american = american
        self.table_indicator = None
        self.table_age = None
        self.table_sex = None
        if self.indicator in ('wfl', 'wfh'):
            if self.height in ('', ' ', None):
                raise exceptions.InvalidMeasurement('no length or height')

    @property
    def age_in_weeks(self):
        return self.age * D('30.4374') / D(7)

    @property
    def rounded_height(self):
        """ Rounds height to closest half centimeter -- the resolution
            of the WHO tables. Oddly, the WHO tables do not include
            decimal places for whole centimeters, so some strange
            rounding is necessary (e.g., 89 not 89.0).
        """
        correction = D('0.5') if D(self.height) >= D(0) else D('-0.5')
        rounded = int(D(self.height) / D('0.5') + correction) * D('0.5')
        if rounded.as_tuple().digits[(-1)] == 0:
            return D(int(rounded)).to_eng_string()
        return rounded.to_eng_string()

    def get_zscores(self, growth):
        table_name = self.resolve_table()
        table = getattr(growth, table_name)
        if self.indicator in ('wfh', 'wfl'):
            assert self.height is not None
            if D(self.height) < D(45):
                raise exceptions.InvalidMeasurement('too short')
            if D(self.height) > D(120):
                raise exceptions.InvalidMeasurement('too tall')
            closest_height = self.rounded_height
            self.logger.debug('looking up scores with: %s' % closest_height)
            scores = table.get(closest_height)
            if scores is not None:
                return scores
            raise exceptions.DataNotFound('SCORES NOT FOUND BY HEIGHT: %s => %s' % (
             self.height, closest_height))
        elif self.indicator in ('lhfa', 'wfa', 'bmifa', 'hcfa'):
            if self.age_in_weeks <= D(13):
                closest_week = str(int(math.floor(self.age_in_weeks)))
                scores = table.get(closest_week)
                if scores is not None:
                    return scores
                raise exceptions.DataNotFound('SCORES NOT FOUND BY WEEK: %s =>  %s' % (
                 str(self.age_in_weeks),
                 closest_week))
            closest_month = str(int(math.floor(self.age)))
            scores = table.get(closest_month)
            if scores is not None:
                return scores
            raise exceptions.DataNotFound('SCORES NOT FOUND BY MONTH: %s => %s' % (
             str(self.age),
             closest_month))

    def resolve_table(self):
        """ Choose a WHO/CDC table to use, making adjustments
        based on age, length, or height. If, for example, the
        indicator is set to wfl while the child is too long for
        the recumbent tables, this method will make the lookup
        in the wfh table. """
        if self.indicator == 'wfl' and D(self.height) > D(86):
            self.logger.warning('too long for recumbent')
            self.table_indicator = 'wfh'
            self.table_age = '2_5'
        else:
            if self.indicator == 'wfh' and D(self.height) < D(65):
                self.logger.warning('too short for standing')
                self.table_indicator = 'wfl'
                self.table_age = '0_2'
            else:
                self.table_indicator = self.indicator
        if self.table_indicator == 'wfl':
            self.table_age = '0_2'
        if self.table_indicator == 'wfh':
            self.table_age = '2_5'
        if self.sex == 'M':
            self.table_sex = 'boys'
        if self.sex == 'F':
            self.table_sex = 'girls'
        if self.indicator in ('wfa', 'lhfa', 'hcfa'):
            self.table_age = '0_5'
            if self.age <= D(3):
                if self.age_in_weeks <= D(13):
                    self.table_age = '0_13'
                if self.american:
                    if self.age >= D(24):
                        if self.indicator == 'hcfa':
                            raise exceptions.InvalidAge('TOO OLD: %d' % self.age)
                        self.table_age = '2_20'
            elif self.indicator in ('bmifa', ):
                pass
            if self.age > D(240):
                raise exceptions.InvalidAge('TOO OLD: %d' % self.age)
            else:
                if self.age <= D(3) and self.age_in_weeks <= D(13):
                    self.table_age = '0_13'
                else:
                    if self.age < D(24):
                        self.table_age = '0_2'
                    else:
                        if self.age >= D(24) and self.age <= D(60):
                            self.table_age = '2_5'
                        else:
                            if self.age >= D(24) and self.age > D(60):
                                self.table_age = '2_20'
                            else:
                                raise exceptions.DataNotFound()
        elif self.table_age is None:
            if self.table_indicator == 'wfl':
                self.table_age = '0_2'
            if self.table_indicator == 'wfh':
                self.table_age = '2_5'
            if self.age < D(24):
                if self.table_indicator == 'wfh':
                    self.logger.warning('too young for standing')
                    self.table_indicator == 'wfl'
                self.table_age = '0_2'
            else:
                if self.age >= D(24):
                    if self.table_indicator == 'wfl':
                        self.logger.warning('too old for recumbent')
                        self.table_indicator == 'wfh'
                    self.table_age = '2_5'
                else:
                    raise exceptions.DataNotFound()
        table = '%(table_indicator)s_%(table_sex)s_%(table_age)s' % {'table_indicator': self.table_indicator,  'table_sex': self.table_sex, 
         'table_age': self.table_age}
        self.logger.debug(table)
        if not all([self.table_indicator, self.table_sex, self.table_age]):
            raise exceptions.DataError()
        return table


class Calculator(object):

    def __reformat_table(self, table_name):
        """ Reformat list of dicts to single dict
        with each item keyed by age, length, or height."""
        list_of_dicts = getattr(self, table_name)
        if 'Length' in list_of_dicts[0]:
            field_name = 'Length'
        else:
            if 'Height' in list_of_dicts[0]:
                field_name = 'Height'
            else:
                if 'Month' in list_of_dicts[0]:
                    field_name = 'Month'
                else:
                    if 'Week' in list_of_dicts[0]:
                        field_name = 'Week'
                    else:
                        raise exceptions.DataError('error loading: %s' % table_name)
        new_dict = {'field_name': field_name}
        for d in list_of_dicts:
            new_dict.update({d[field_name]: d})

        setattr(self, table_name, new_dict)

    def __init__(self, adjust_height_data=False, adjust_weight_scores=False, include_cdc=False, logger_name='pygrowup', log_level='INFO'):
        self.logger = logging.getLogger(logger_name)
        self.logger.setLevel(getattr(logging, log_level))
        self.context = decimal.getcontext()
        self.adjust_height_data = adjust_height_data
        self.adjust_weight_scores = adjust_weight_scores
        self.include_cdc = include_cdc
        WHO_tables = [
         'wfl_boys_0_2_zscores.json', 'wfl_girls_0_2_zscores.json',
         'wfh_boys_2_5_zscores.json', 'wfh_girls_2_5_zscores.json',
         'lhfa_boys_0_5_zscores.json', 'lhfa_girls_0_5_zscores.json',
         'hcfa_boys_0_5_zscores.json', 'hcfa_girls_0_5_zscores.json',
         'wfa_boys_0_5_zscores.json', 'wfa_girls_0_5_zscores.json',
         'wfa_boys_0_13_zscores.json', 'wfa_girls_0_13_zscores.json',
         'lhfa_boys_0_13_zscores.json', 'lhfa_girls_0_13_zscores.json',
         'hcfa_boys_0_13_zscores.json', 'hcfa_girls_0_13_zscores.json',
         'bmifa_boys_0_13_zscores.json', 'bmifa_girls_0_13_zscores.json',
         'bmifa_boys_0_2_zscores.json', 'bmifa_girls_0_2_zscores.json',
         'bmifa_boys_2_5_zscores.json', 'bmifa_girls_2_5_zscores.json']
        CDC_tables = [
         'lhfa_boys_2_20_zscores.cdc.json',
         'lhfa_girls_2_20_zscores.cdc.json',
         'wfa_boys_2_20_zscores.cdc.json',
         'wfa_girls_2_20_zscores.cdc.json',
         'bmifa_boys_2_20_zscores.cdc.json',
         'bmifa_girls_2_20_zscores.cdc.json']
        table_dir = os.path.join(module_dir, 'tables')
        tables_to_load = WHO_tables
        if self.include_cdc:
            tables_to_load = tables_to_load + CDC_tables
        for table in tables_to_load:
            table_file = os.path.join(table_dir, table)
            with open(table_file, 'r') as (f):
                table_name, underscore, zscore_part = table.split('.')[0].rpartition('_')
                setattr(self, table_name, json.load(f))
                self._Calculator__reformat_table(table_name)

    def lhfa(self, measurement=None, age_in_months=None, sex=None, height=None):
        """ Calculate length/height-for-age """
        return self.zscore_for_measurement('lhfa', measurement=measurement, age_in_months=age_in_months, sex=sex, height=height)

    def wfl(self, measurement=None, age_in_months=None, sex=None, height=None):
        """ Calculate weight-for-length """
        return self.zscore_for_measurement('wfl', measurement=measurement, age_in_months=age_in_months, sex=sex, height=height)

    def wfh(self, measurement=None, age_in_months=None, sex=None, height=None):
        """ Calculate weight-for-height """
        return self.zscore_for_measurement('wfh', measurement=measurement, age_in_months=age_in_months, sex=sex, height=height)

    def wfa(self, measurement=None, age_in_months=None, sex=None, height=None):
        """ Calculate weight-for-age """
        return self.zscore_for_measurement('wfa', measurement=measurement, age_in_months=age_in_months, sex=sex, height=height)

    def bmifa(self, measurement=None, age_in_months=None, sex=None, height=None):
        """ Calculate body-mass-index-for-age """
        return self.zscore_for_measurement('bmifa', measurement=measurement, age_in_months=age_in_months, sex=sex, height=height)

    def hcfa(self, measurement=None, age_in_months=None, sex=None, height=None):
        """ Calculate head-circumference-for-age """
        return self.zscore_for_measurement('hcfa', measurement=measurement, age_in_months=age_in_months, sex=sex, height=height)

    def zscore_for_measurement(self, indicator, measurement, age_in_months, sex, height=None):
        assert sex is not None
        assert isinstance(sex, str)
        assert sex.upper() in ('M', 'F')
        assert age_in_months is not None
        assert indicator is not None
        assert indicator.lower() in ('lhfa', 'wfl', 'wfh', 'wfa', 'bmifa', 'hcfa')
        assert measurement not in ('', ' ', None)
        y = D(measurement)
        if y <= D(0):
            raise exceptions.InvalidMeasurement('measurement must be greater than zero')
        self.logger.debug('MEASUREMENT: %d' % y)
        obs = Observation(indicator, measurement, age_in_months, sex, height, self.include_cdc, self.logger.name)
        if indicator == 'wfl':
            if D('65.7') < y < D('120.7'):
                y = y - D('0.7')
        if indicator == 'wfh':
            if self.adjust_height_data:
                y = y + D('0.7')
        zscores = obs.get_zscores(self)
        if zscores is None:
            raise exceptions.DataNotFound()
        box_cox_power = D(zscores.get('L'))
        self.logger.debug('BOX-COX: %d' % box_cox_power)
        median_for_age = D(zscores.get('M'))
        self.logger.debug('MEDIAN: %d' % median_for_age)
        coefficient_of_variance_for_age = D(zscores.get('S'))
        self.logger.debug('COEF VAR: %d' % coefficient_of_variance_for_age)
        base = self.context.divide(y, median_for_age)
        self.logger.debug('BASE: %d' % base)
        power = base ** box_cox_power
        self.logger.debug('POWER: %d' % power)
        numerator = D(str(power)) - D(1)
        self.logger.debug('NUMERATOR: %d' % numerator)
        denomenator = self.context.multiply(coefficient_of_variance_for_age, box_cox_power)
        self.logger.debug('DENOMENATOR: %d' % denomenator)
        zscore = self.context.divide(numerator, denomenator)
        self.logger.debug('ZSCORE: %d' % zscore)
        if not self.adjust_weight_scores:
            return zscore.quantize(D('.01'))
        if indicator not in ('wfl', 'wfh', 'wfa'):
            return zscore.quantize(D('.01'))
        if abs(zscore) <= D(3):
            return zscore.quantize(D('.01'))

        def calc_stdev(sd):
            base = self.context.add(D(1), self.context.multiply(self.context.multiply(box_cox_power, coefficient_of_variance_for_age), D(sd)))
            exponent = self.context.divide(D(1), box_cox_power)
            power = math.pow(base, exponent)
            stdev = self.context.multiply(median_for_age, D(str(power)))
            return D(stdev)

        if zscore > D(3):
            logging.info('Z greater than 3')
            SD2pos_c = calc_stdev(2)
            SD3pos_c = calc_stdev(3)
            SD23pos_c = SD3pos_c - SD2pos_c
            sub = self.context.subtract(D(y), SD3pos_c)
            div = self.context.divide(sub, SD23pos_c)
            zscore = self.context.add(D(3), div)
            return zscore.quantize(D('.01'))
        if zscore < D(-3):
            SD2neg_c = calc_stdev(-2)
            SD3neg_c = calc_stdev(-3)
            SD23neg_c = SD2neg_c - SD3neg_c
            sub = self.context.subtract(D(y), SD3neg_c)
            div = self.context.divide(sub, SD23neg_c)
            zscore = self.context.add(D(-3), div)
            return zscore.quantize(D('.01'))