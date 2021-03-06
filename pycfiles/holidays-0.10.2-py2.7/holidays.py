# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-intel/egg/holidays.py
# Compiled at: 2020-03-21 18:36:09
from datetime import date, datetime, timedelta
from dateutil.easter import easter, EASTER_ORTHODOX
from dateutil.parser import parse
from dateutil.relativedelta import relativedelta as rd
from dateutil.relativedelta import MO, TU, WE, TH, FR, SA, SU
import inspect, six, sys, warnings
__version__ = '0.10.2'
MON, TUE, WED, THU, FRI, SAT, SUN = range(7)
WEEKEND = (SAT, SUN)
JAN, FEB, MAR, APR, MAY, JUN, JUL, AUG, SEP, OCT, NOV, DEC = range(1, 13)

class HolidayBase(dict):
    PROVINCES = []

    def __init__(self, years=[], expand=True, observed=True, prov=None, state=None):
        self.observed = observed
        self.expand = expand
        if isinstance(years, int):
            years = [
             years]
        self.years = set(years)
        if not getattr(self, 'prov', False):
            self.prov = prov
        self.state = state
        for year in list(self.years):
            self._populate(year)

    def __setattr__(self, key, value):
        if key == 'observed' and len(self) > 0:
            dict.__setattr__(self, key, value)
            if value is True:
                years = list(self.years)
                self.years = set()
                self.clear()
                for year in years:
                    self._populate(year)

            else:
                for k, v in list(self.items()):
                    if v.find('Observed') >= 0:
                        del self[k]

        else:
            return dict.__setattr__(self, key, value)

    def __keytransform__(self, key):
        if isinstance(key, datetime):
            key = key.date()
        elif isinstance(key, date):
            key = key
        elif isinstance(key, int) or isinstance(key, float):
            key = datetime.utcfromtimestamp(key).date()
        elif isinstance(key, six.string_types):
            try:
                key = parse(key).date()
            except (ValueError, OverflowError):
                raise ValueError("Cannot parse date from string '%s'" % key)

        else:
            raise TypeError("Cannot convert type '%s' to date." % type(key))
        if self.expand and key.year not in self.years:
            self.years.add(key.year)
            self._populate(key.year)
        return key

    def __contains__(self, key):
        return dict.__contains__(self, self.__keytransform__(key))

    def __getitem__(self, key):
        if isinstance(key, slice) and (not key.start or not key.stop):
            raise ValueError('Both start and stop must be given.')
        start = self.__keytransform__(key.start)
        stop = self.__keytransform__(key.stop)
        if key.step is None:
            step = 1
        else:
            if isinstance(key.step, timedelta):
                step = key.step.days
            else:
                if isinstance(key.step, int):
                    step = key.step
                else:
                    raise TypeError("Cannot convert type '%s' to int." % type(key.step))
                if step == 0:
                    raise ValueError('Step value must not be zero.')
                date_diff = stop - start
                if date_diff.days < 0 <= step or date_diff.days >= 0 > step:
                    step *= -1
                days_in_range = []
                for delta_days in range(0, date_diff.days, step):
                    day = start + timedelta(days=delta_days)
                    try:
                        dict.__getitem__(self, day)
                        days_in_range.append(day)
                    except KeyError:
                        pass

            return days_in_range
        return dict.__getitem__(self, self.__keytransform__(key))

    def __setitem__(self, key, value):
        if key in self:
            if self.get(key).find(value) < 0 and value.find(self.get(key)) < 0:
                value = '%s, %s' % (value, self.get(key))
            else:
                value = self.get(key)
        return dict.__setitem__(self, self.__keytransform__(key), value)

    def update(self, *args):
        args = list(args)
        for arg in args:
            if isinstance(arg, dict):
                for key, value in list(arg.items()):
                    self[key] = value

            elif isinstance(arg, list):
                for item in arg:
                    self[item] = 'Holiday'

            else:
                self[arg] = 'Holiday'

    def append(self, *args):
        return self.update(*args)

    def get(self, key, default=None):
        return dict.get(self, self.__keytransform__(key), default)

    def get_list(self, key):
        return [ h for h in self.get(key, '').split(', ') if h ]

    def pop(self, key, default=None):
        if default is None:
            return dict.pop(self, self.__keytransform__(key))
        else:
            return dict.pop(self, self.__keytransform__(key), default)

    def __eq__(self, other):
        return dict.__eq__(self, other) and self.__dict__ == other.__dict__

    def __ne__(self, other):
        return dict.__ne__(self, other) or self.__dict__ != other.__dict__

    def __add__(self, other):
        if isinstance(other, int) and other == 0:
            return self
        else:
            if not isinstance(other, HolidayBase):
                raise TypeError()
            HolidaySum = createHolidaySum(self, other)
            country = getattr(self, 'country', None) or getattr(other, 'country', None)
            if self.country and other.country and self.country != other.country:
                c1 = self.country
                if not isinstance(c1, list):
                    c1 = [
                     c1]
                c2 = other.country
                if not isinstance(c2, list):
                    c2 = [
                     c2]
                country = c1 + c2
            prov = getattr(self, 'prov', None) or getattr(other, 'prov', None)
            if self.prov and other.prov and self.prov != other.prov:
                p1 = self.prov if isinstance(self.prov, list) else [self.prov]
                p2 = other.prov if isinstance(other.prov, list) else [other.prov]
                prov = p1 + p2
            return HolidaySum(years=self.years | other.years, expand=self.expand or other.expand, observed=self.observed or other.observed, country=country, prov=prov)

    def __radd__(self, other):
        return self.__add__(other)

    def _populate(self, year):
        pass


def createHolidaySum(h1, h2):

    class HolidaySum(HolidayBase):

        def __init__(self, country, **kwargs):
            self.country = country
            self.holidays = []
            if getattr(h1, 'holidays', False):
                for h in h1.holidays:
                    self.holidays.append(h)

            else:
                self.holidays.append(h1)
            if getattr(h2, 'holidays', False):
                for h in h2.holidays:
                    self.holidays.append(h)

            else:
                self.holidays.append(h2)
            HolidayBase.__init__(self, **kwargs)

        def _populate(self, year):
            for h in self.holidays[::-1]:
                h._populate(year)
                self.update(h)

    return HolidaySum


def list_supported_countries():
    """List all supported countries incl. their abbreviation."""
    return [ name for name, obj in inspect.getmembers(sys.modules[__name__], inspect.isclass) if obj.__module__ is __name__
           ]


def CountryHoliday(country, years=[], prov=None, state=None, expand=True, observed=True):
    try:
        country_holiday = globals()[country](years=years, prov=prov, state=state, expand=expand, observed=observed)
    except KeyError:
        raise KeyError('Country %s not available' % country)

    return country_holiday


class Aruba(HolidayBase):

    def __init__(self, **kwargs):
        self.country = 'AW'
        HolidayBase.__init__(self, **kwargs)

    def _populate(self, year):
        self[date(year, JAN, 1)] = "Aña Nobo [New Year's Day]"
        self[date(year, JAN, 25)] = 'Dia Di Betico [Betico Day]'
        self[easter(year) + rd(days=-48)] = 'Dialuna di Carnaval             [Carnaval Monday]'
        self[date(year, MAR, 18)] = 'Dia di Himno y Bandera             [National Anthem & Flag Day]'
        self[easter(year) + rd(weekday=FR(-1))] = 'Bierna Santo [Good Friday]'
        self[easter(year) + rd(days=1)] = 'Di Dos Dia di Pasco di Resureccion             [Easter Monday]'
        if year >= 2014:
            kings_day = date(year, APR, 27)
            if kings_day.weekday() == 6:
                kings_day = kings_day - rd(days=1)
            self[kings_day] = "Aña di Rey [King's Day]"
        if 1891 <= year <= 2013:
            queens_day = date(year, APR, 30)
            if year <= 1948:
                queens_day = date(year, AUG, 31)
            if queens_day.weekday() == 6:
                if year < 1980:
                    queens_day = queens_day + rd(days=1)
                else:
                    queens_day = queens_day - rd(days=1)
            self[queens_day] = "Aña di La Reina [Queen's Day]"
        self[date(year, MAY, 1)] = 'Dia di Obrero [Labour Day]'
        self[easter(year) + rd(days=39)] = 'Dia di Asuncion [Ascension Day]'
        self[date(year, DEC, 25)] = 'Pasco di Nacemento [Christmas]'
        self[date(year, DEC, 26)] = 'Di Dos Dia di Pasco di             Nacemento [Second Christmas]'


class AW(Aruba):
    pass


class Argentina(HolidayBase):

    def __init__(self, **kwargs):
        self.country = 'AR'
        HolidayBase.__init__(self, **kwargs)

    def _populate(self, year):
        if not self.observed and date(year, JAN, 1).weekday() in WEEKEND:
            pass
        else:
            self[date(year, JAN, 1)] = "Año Nuevo [New Year's Day]"
        name = "Día de Carnaval [Carnival's Day]"
        self[easter(year) - rd(days=48)] = name
        self[easter(year) - rd(days=47)] = name
        name = "Día Nacional de la Memoria por la Verdad y la Justicia [Memory's National Day for the Truth and Justice]"
        if not self.observed and date(year, MAR, 24).weekday() in WEEKEND:
            pass
        else:
            self[date(year, MAR, 24)] = name
        name_thu = 'Semana Santa (Jueves Santo)  [Holy day (Holy Thursday)]'
        name_fri = 'Semana Santa (Viernes Santo)  [Holy day (Holy Friday)]'
        name_easter = 'Día de Pascuas [Easter Day]'
        self[easter(year) + rd(weekday=TH(-1))] = name_thu
        self[easter(year) + rd(weekday=FR(-1))] = name_fri
        if not self.observed and easter(year).weekday() in WEEKEND:
            pass
        else:
            self[easter(year)] = name_easter
        if not self.observed and date(year, APR, 2).weekday() in WEEKEND:
            pass
        else:
            self[date(year, APR, 2)] = 'Día del Veterano y de los Caidos en la Guerra de Malvinas [Veterans Day and the Fallen in the Malvinas War]'
        name = 'Día del Trabajo [Labour Day]'
        if not self.observed and date(year, MAY, 1).weekday() in WEEKEND:
            pass
        else:
            self[date(year, MAY, 1)] = name
        name = 'Día de la Revolucion de Mayo [May Revolution Day]'
        if not self.observed and date(year, MAY, 25).weekday() in WEEKEND:
            pass
        else:
            self[date(year, MAY, 25)] = name
        name = 'Día Pase a la Inmortalidad del General Martín Miguel de Güemes [Day Pass to the Immortality of General Martín Miguel de Güemes]'
        if not self.observed and date(year, JUN, 17).weekday() in WEEKEND:
            pass
        else:
            self[date(year, JUN, 17)] = name
        name = 'Día Pase a la Inmortalidad del General D. Manuel Belgrano [Day Pass to the Immortality of General D. Manuel Belgrano]'
        if not self.observed and date(year, JUN, 20).weekday() in WEEKEND:
            pass
        else:
            self[date(year, JUN, 20)] = name
        name = 'Día de la Independencia [Independence Day]'
        if not self.observed and date(year, JUL, 9).weekday() in WEEKEND:
            pass
        else:
            self[date(year, JUL, 9)] = name
        name = 'Día Pase a la Inmortalidad del General D. José de San Martin [Day Pass to the Immortality of General D. José de San Martin]'
        if not self.observed and date(year, AUG, 17).weekday() in WEEKEND:
            pass
        else:
            self[date(year, AUG, 17)] = name
        if not self.observed and date(year, OCT, 12).weekday() in WEEKEND:
            pass
        elif year < 2010:
            self[date(year, OCT, 12)] = 'Día de la Raza [Columbus day]'
        else:
            self[date(year, OCT, 12)] = 'Día del Respeto a la Diversidad Cultural [Respect for Cultural Diversity Day]'
        name = 'Día Nacional de la Soberanía [National Sovereignty Day]'
        if not self.observed and date(year, NOV, 20).weekday() in WEEKEND:
            pass
        elif year >= 2010:
            self[date(year, NOV, 20)] = name
        if not self.observed and date(year, DEC, 8).weekday() in WEEKEND:
            pass
        else:
            self[date(year, DEC, 8)] = 'La Inmaculada Concepción [Immaculate Conception]'
        self[date(year, DEC, 25)] = 'Navidad [Christmas]'


class AR(Argentina):
    pass


class Belarus(HolidayBase):
    """
    http://president.gov.by/en/holidays_en/
    http://www.belarus.by/en/about-belarus/national-holidays
    """

    def __init__(self, **kwargs):
        self.country = 'BY'
        HolidayBase.__init__(self, **kwargs)

    def _populate(self, year):
        if year <= 1998:
            return
        self[date(year, JAN, 1)] = 'Новый год'
        self[date(year, JAN, 7)] = 'Рождество Христово (православное Рождество)'
        self[date(year, MAR, 8)] = 'День женщин'
        self[easter(year, method=EASTER_ORTHODOX) + rd(days=9)] = 'Радуница'
        self[date(year, MAY, 1)] = 'Праздник труда'
        self[date(year, MAY, 9)] = 'День Победы'
        self[date(year, JUL, 3)] = 'День Независимости Республики Беларусь (День Республики)'
        self[date(year, NOV, 7)] = 'День Октябрьской революции'
        self[date(year, DEC, 25)] = 'Рождество Христово (католическое Рождество)'


class BY(Belarus):
    pass


class Brazil(HolidayBase):
    """
    https://pt.wikipedia.org/wiki/Feriados_no_Brasil
    """
    STATES = [
     'AC', 'AL', 'AP', 'AM', 'BA', 'CE', 'DF', 'ES', 'GO', 'MA', 'MT',
     'MS', 'MG', 'PA', 'PB', 'PE', 'PI', 'RJ', 'RN', 'RS', 'RO', 'RR',
     'SC', 'SP', 'SE', 'TO']

    def __init__(self, **kwargs):
        self.country = 'BR'
        HolidayBase.__init__(self, **kwargs)

    def _populate(self, year):
        self[date(year, JAN, 1)] = 'Ano novo'
        self[date(year, APR, 21)] = 'Tiradentes'
        self[date(year, MAY, 1)] = 'Dia Mundial do Trabalho'
        self[date(year, SEP, 7)] = 'Independência do Brasil'
        self[date(year, OCT, 12)] = 'Nossa Senhora Aparecida'
        self[date(year, NOV, 2)] = 'Finados'
        self[date(year, NOV, 15)] = 'Proclamação da República'
        self[date(year, DEC, 25)] = 'Natal'
        self[easter(year) - rd(days=2)] = 'Sexta-feira Santa'
        self[easter(year)] = 'Páscoa'
        self[easter(year) + rd(days=60)] = 'Corpus Christi'
        quaresma = easter(year) - rd(days=46)
        self[quaresma] = 'Quarta-feira de cinzas (Início da Quaresma)'
        self[quaresma - rd(weekday=TU(-1))] = 'Carnaval'
        if self.state == 'AC':
            self[date(year, JAN, 23)] = 'Dia do evangélico'
            self[date(year, JUN, 15)] = 'Aniversário do Acre'
            self[date(year, SEP, 5)] = 'Dia da Amazônia'
            self[date(year, NOV, 17)] = 'Assinatura do Tratado de Petrópolis'
        if self.state == 'AL':
            self[date(year, JUN, 24)] = 'São João'
            self[date(year, JUN, 29)] = 'São Pedro'
            self[date(year, SEP, 16)] = 'Emancipação política de Alagoas'
            self[date(year, NOV, 20)] = 'Consciência Negra'
        if self.state == 'AP':
            self[date(year, MAR, 19)] = 'Dia de São José'
            self[date(year, JUL, 25)] = 'São Tiago'
            self[date(year, OCT, 5)] = 'Criação do estado'
            self[date(year, NOV, 20)] = 'Consciência Negra'
        if self.state == 'AM':
            self[date(year, SEP, 5)] = 'Elevação do Amazonas à categoria de província'
            self[date(year, NOV, 20)] = 'Consciência Negra'
            self[date(year, DEC, 8)] = 'Dia de Nossa Senhora da Conceição'
        if self.state == 'BA':
            self[date(year, JUL, 2)] = 'Independência da Bahia'
        if self.state == 'CE':
            self[date(year, MAR, 19)] = 'São José'
            self[date(year, MAR, 25)] = 'Data Magna do Ceará'
        if self.state == 'DF':
            self[date(year, APR, 21)] = 'Fundação de Brasília'
            self[date(year, NOV, 30)] = 'Dia do Evangélico'
        if self.state == 'ES':
            self[date(year, OCT, 28)] = 'Dia do Servidor Público'
        if self.state == 'GO':
            self[date(year, OCT, 28)] = 'Dia do Servidor Público'
        if self.state == 'MA':
            self[date(year, JUL, 28)] = 'Adesão do Maranhão à independência do Brasil'
            self[date(year, DEC, 8)] = 'Dia de Nossa Senhora da Conceição'
        if self.state == 'MT':
            self[date(year, NOV, 20)] = 'Consciência Negra'
        if self.state == 'MS':
            self[date(year, OCT, 11)] = 'Criação do estado'
        if self.state == 'MG':
            self[date(year, APR, 21)] = 'Data Magna de MG'
        if self.state == 'PA':
            self[date(year, AUG, 15)] = 'Adesão do Grão-Pará à independência do Brasil'
        if self.state == 'PB':
            self[date(year, AUG, 5)] = 'Fundação do Estado'
        if self.state == 'PE':
            self[date(year, MAR, 6)] = 'Revolução Pernambucana (Data Magna)'
            self[date(year, JUN, 24)] = 'São João'
        if self.state == 'PI':
            self[date(year, MAR, 13)] = 'Dia da Batalha do Jenipapo'
            self[date(year, OCT, 19)] = 'Dia do Piauí'
        if self.state == 'RJ':
            self[date(year, APR, 23)] = 'Dia de São Jorge'
            self[date(year, OCT, 28)] = 'Dia do Funcionário Público'
            self[date(year, NOV, 20)] = 'Zumbi dos Palmares'
        if self.state == 'RN':
            self[date(year, JUN, 29)] = 'Dia de São Pedro'
            self[date(year, OCT, 3)] = 'Mártires de Cunhaú e Uruaçuu'
        if self.state == 'RS':
            self[date(year, SEP, 20)] = 'Revolução Farroupilha'
        if self.state == 'RO':
            self[date(year, JAN, 4)] = 'Criação do estado'
            self[date(year, JUN, 18)] = 'Dia do Evangélico'
        if self.state == 'RR':
            self[date(year, OCT, 5)] = 'Criação de Roraima'
        if self.state == 'SC':
            self[date(year, AUG, 11)] = 'Criação da capitania, separando-se de SP'
        if self.state == 'SP':
            self[date(year, JUL, 9)] = 'Revolução Constitucionalista de 1932'
        if self.state == 'SE':
            self[date(year, JUL, 8)] = 'Autonomia política de Sergipe'
        if self.state == 'TO':
            self[date(year, JAN, 1)] = 'Instalação de Tocantins'
            self[date(year, SEP, 8)] = 'Nossa Senhora da Natividade'
            self[date(year, OCT, 5)] = 'Criação de Tocantins'


class BR(Brazil):
    pass


class Bulgaria(HolidayBase):
    """
    Official holidays in Bulgaria in their current form. This class does not
    any return holidays before 1990, as holidays in the People's Republic of
    Bulgaria and earlier were different.

    Most holidays are fixed and if the date falls on a Saturday or a Sunday,
    the following Monday is a non-working day. The exceptions are (1) the
    Easter holidays, which are always a consecutive Friday, Saturday, and
    Sunday; and (2) the National Awakening Day which, while an official holiday
    and a non-attendance day for schools, is still a working day.

    Sources (Bulgarian):
    - http://lex.bg/laws/ldoc/1594373121
    - https://www.parliament.bg/bg/24

    Sources (English):
    - https://en.wikipedia.org/wiki/Public_holidays_in_Bulgaria
    """

    def __init__(self, **kwargs):
        self.country = 'BG'
        HolidayBase.__init__(self, **kwargs)

    def _populate(self, year):
        if year < 1990:
            return
        self[date(year, JAN, 1)] = 'Нова година'
        self[date(year, MAR, 3)] = 'Ден на Освобождението на България от османско иго'
        self[date(year, MAY, 1)] = 'Ден на труда и на международната работническа солидарност'
        self[date(year, MAY, 6)] = 'Гергьовден, Ден на храбростта и Българската армия'
        self[date(year, MAY, 24)] = 'Ден на българската просвета и култура и на славянската писменост'
        self[date(year, SEP, 6)] = 'Ден на Съединението'
        self[date(year, SEP, 22)] = 'Ден на Независимостта на България'
        self[date(year, NOV, 1)] = 'Ден на народните будители'
        self[date(year, DEC, 24)] = 'Бъдни вечер'
        self[date(year, DEC, 25)] = 'Рождество Христово'
        self[date(year, DEC, 26)] = 'Рождество Христово'
        self[easter(year, method=EASTER_ORTHODOX) - rd(days=2)] = 'Велики петък'
        self[easter(year, method=EASTER_ORTHODOX) - rd(days=1)] = 'Велика събота'
        self[easter(year, method=EASTER_ORTHODOX)] = 'Великден'


class BG(Bulgaria):
    pass


class Canada(HolidayBase):
    PROVINCES = [
     'AB', 'BC', 'MB', 'NB', 'NL', 'NS', 'NT', 'NU', 'ON', 'PE',
     'QC', 'SK', 'YU']

    def __init__(self, **kwargs):
        self.country = 'CA'
        self.prov = kwargs.pop('prov', 'ON')
        HolidayBase.__init__(self, **kwargs)

    def _populate(self, year):
        if year >= 1867:
            name = "New Year's Day"
            self[date(year, JAN, 1)] = name
            if self.observed and date(year, JAN, 1).weekday() == SUN:
                self[date(year, JAN, 1) + rd(days=+1)] = name + ' (Observed)'
            elif self.observed and date(year, JAN, 1).weekday() == SAT:
                expand = self.expand
                self.expand = False
                self[date(year, JAN, 1) + rd(days=-1)] = name + ' (Observed)'
                self.expand = expand
            if self.observed and date(year, DEC, 31).weekday() == FRI:
                self[date(year, DEC, 31)] = name + ' (Observed)'
        if self.prov in ('AB', 'SK', 'ON') and year >= 2008:
            self[date(year, FEB, 1) + rd(weekday=MO(+3))] = 'Family Day'
        elif self.prov in ('AB', 'SK') and year >= 2007:
            self[date(year, FEB, 1) + rd(weekday=MO(+3))] = 'Family Day'
        elif self.prov == 'AB' and year >= 1990:
            self[date(year, FEB, 1) + rd(weekday=MO(+3))] = 'Family Day'
        elif self.prov == 'NB' and year >= 2018:
            self[date(year, FEB, 1) + rd(weekday=MO(+3))] = 'Family Day'
        elif self.prov == 'BC':
            if year >= 2013 and year <= 2018:
                self[date(year, FEB, 1) + rd(weekday=MO(+2))] = 'Family Day'
            elif year > 2018:
                self[date(year, FEB, 1) + rd(weekday=MO(+3))] = 'Family Day'
        elif self.prov == 'MB' and year >= 2008:
            self[date(year, FEB, 1) + rd(weekday=MO(+3))] = 'Louis Riel Day'
        elif self.prov == 'PE' and year >= 2010:
            self[date(year, FEB, 1) + rd(weekday=MO(+3))] = 'Islander Day'
        elif self.prov == 'PE' and year == 2009:
            self[date(year, FEB, 1) + rd(weekday=MO(+2))] = 'Islander Day'
        elif self.prov == 'NS' and year >= 2015:
            self[date(year, FEB, 1) + rd(weekday=MO(+3))] = 'Heritage Day'
        elif self.prov == 'YU':
            dt = date(year, MAR, 1) + rd(weekday=SU(-1)) + rd(weekday=FR(-1))
            self[dt] = 'Heritage Day'
        if self.prov == 'NL' and year >= 1900:
            dt = date(year, MAR, 17)
            dt1 = date(year, MAR, 17) + rd(weekday=MO(-1))
            dt2 = date(year, MAR, 17) + rd(weekday=MO(+1))
            if dt2 - dt <= dt - dt1:
                self[dt2] = "St. Patrick's Day"
            else:
                self[dt1] = "St. Patrick's Day"
        if self.prov != 'QC' and year >= 1867:
            self[easter(year) + rd(weekday=FR(-1))] = 'Good Friday'
        if self.prov == 'QC' and year >= 1867:
            self[easter(year) + rd(weekday=MO)] = 'Easter Monday'
        if self.prov == 'NL' and year == 2010:
            self[date(2010, 4, 19)] = "St. George's Day"
        elif self.prov == 'NL' and year >= 1990:
            dt = date(year, APR, 23)
            dt1 = dt + rd(weekday=MO(-1))
            dt2 = dt + rd(weekday=MO(+1))
            if dt2 - dt < dt - dt1:
                self[dt2] = "St. George's Day"
            else:
                self[dt1] = "St. George's Day"
        if self.prov not in ('NB', 'NS', 'PE', 'NL', 'QC') and year >= 1953:
            self[date(year, MAY, 24) + rd(weekday=MO(-1))] = 'Victoria Day'
        elif self.prov == 'QC' and year >= 1953:
            name = "National Patriots' Day"
            self[date(year, MAY, 24) + rd(weekday=MO(-1))] = name
        if self.prov == 'NT' and year >= 1996:
            self[date(year, JUN, 21)] = 'National Aboriginal Day'
        if self.prov == 'QC' and year >= 1925:
            self[date(year, JUN, 24)] = 'St. Jean Baptiste Day'
            if self.observed and date(year, JUN, 24).weekday() == SUN:
                self[date(year, JUN, 25)] = 'St. Jean Baptiste Day (Observed)'
        if self.prov == 'NL' and year >= 1997:
            dt = date(year, JUN, 24)
            dt1 = dt + rd(weekday=MO(-1))
            dt2 = dt + rd(weekday=MO(+1))
            if dt2 - dt <= dt - dt1:
                self[dt2] = 'Discovery Day'
            else:
                self[dt1] = 'Discovery Day'
        elif self.prov == 'YU' and year >= 1912:
            self[date(year, AUG, 1) + rd(weekday=MO(+3))] = 'Discovery Day'
        if self.prov != 'NL' and year >= 1867:
            if year >= 1983:
                name = 'Canada Day'
            else:
                name = 'Dominion Day'
            self[date(year, JUL, 1)] = name
            if year >= 1879 and self.observed and date(year, JUL, 1).weekday() in WEEKEND:
                self[date(year, JUL, 1) + rd(weekday=MO)] = name + ' (Observed)'
        elif year >= 1867:
            if year >= 1983:
                name = 'Memorial Day'
            else:
                name = 'Dominion Day'
            self[date(year, JUL, 1)] = name
            if year >= 1879 and self.observed and date(year, JUL, 1).weekday() in WEEKEND:
                self[date(year, JUL, 1) + rd(weekday=MO)] = name + ' (Observed)'
        if self.prov == 'NU' and year >= 2001:
            self[date(year, JUL, 9)] = 'Nunavut Day'
            if self.observed and date(year, JUL, 9).weekday() == SUN:
                self[date(year, JUL, 10)] = 'Nunavut Day (Observed)'
        elif self.prov == 'NU' and year == 2000:
            self[date(2000, 4, 1)] = 'Nunavut Day'
        if self.prov in ('ON', 'MB', 'NT') and year >= 1900:
            self[date(year, AUG, 1) + rd(weekday=MO)] = 'Civic Holiday'
        elif self.prov == 'AB' and year >= 1974:
            self[date(year, AUG, 1) + rd(weekday=MO)] = 'Heritage Day'
        elif self.prov == 'BC' and year >= 1974:
            self[date(year, AUG, 1) + rd(weekday=MO)] = 'British Columbia Day'
        elif self.prov == 'NB' and year >= 1900:
            self[date(year, AUG, 1) + rd(weekday=MO)] = 'New Brunswick Day'
        elif self.prov == 'SK' and year >= 1900:
            self[date(year, AUG, 1) + rd(weekday=MO)] = 'Saskatchewan Day'
        if year >= 1894:
            self[date(year, SEP, 1) + rd(weekday=MO)] = 'Labour Day'
        if self.prov not in ('NB', 'NS', 'PE', 'NL') and year >= 1931:
            if year == 1935:
                self[date(1935, 10, 25)] = 'Thanksgiving'
            else:
                self[date(year, OCT, 1) + rd(weekday=MO(+2))] = 'Thanksgiving'
        name = 'Remembrance Day'
        provinces = ('ON', 'QC', 'NS', 'NL', 'NT', 'PE', 'SK')
        if self.prov not in provinces and year >= 1931:
            self[date(year, NOV, 11)] = name
        elif self.prov in ('NS', 'NL', 'NT', 'PE', 'SK') and year >= 1931:
            self[date(year, NOV, 11)] = name
            if self.observed and date(year, NOV, 11).weekday() == SUN:
                name = name + ' (Observed)'
                self[date(year, NOV, 11) + rd(weekday=MO)] = name
        if year >= 1867:
            self[date(year, DEC, 25)] = 'Christmas Day'
            if self.observed and date(year, DEC, 25).weekday() == SAT:
                self[date(year, DEC, 24)] = 'Christmas Day (Observed)'
            elif self.observed and date(year, DEC, 25).weekday() == SUN:
                self[date(year, DEC, 26)] = 'Christmas Day (Observed)'
        if year >= 1867:
            name = 'Boxing Day'
            name_observed = name + ' (Observed)'
            if self.observed and date(year, DEC, 26).weekday() in WEEKEND:
                self[date(year, DEC, 26) + rd(weekday=MO)] = name_observed
            elif self.observed and date(year, DEC, 26).weekday() == 0:
                self[date(year, DEC, 27)] = name_observed
            else:
                self[date(year, DEC, 26)] = name


class CA(Canada):
    pass


class Chile(HolidayBase):

    def __init__(self, **kwargs):
        self.country = 'CL'
        HolidayBase.__init__(self, **kwargs)

    def _populate(self, year):
        self[date(year, JAN, 1)] = "Año Nuevo [New Year's Day]"
        name_fri = 'Semana Santa (Viernes Santo)  [Holy day (Holy Friday)]'
        name_easter = 'Día de Pascuas [Easter Day]'
        self[easter(year) + rd(weekday=FR(-1))] = name_fri
        self[easter(year)] = name_easter
        name = 'Día del Trabajo [Labour Day]'
        self[date(year, MAY, 1)] = name
        name = 'Día de las Glorias Navales [Naval Glories Day]'
        self[date(year, MAY, 21)] = name
        name = 'San Pedro y San Pablo [Saint Peter and Saint Paul]'
        self[date(year, JUN, 29)] = name
        name = 'Virgen del Carmen [Virgin of Carmen]'
        self[date(year, JUL, 16)] = name
        name = 'Asunsión de la Virgen [Assumption of the Virgin]'
        self[date(year, AUG, 15)] = name
        name = 'Día de la Independencia [Independence Day]'
        self[date(year, SEP, 18)] = name
        name = 'Día de las Glorias del Ejército de Chile [Day of Glories of the Army of Chile]'
        self[date(year, SEP, 19)] = name
        name = 'Fiestas Patrias [National Holidays]'
        if year > 2014 and date(year, SEP, 19).weekday() in [WED, THU]:
            self[date(year, SEP, 20)] = name
        if year < 2010:
            self[date(year, OCT, 12)] = 'Día de la Raza [Columbus day]'
        else:
            self[date(year, OCT, 12)] = 'Día del Respeto a la Diversidad [Day of the Meeting  of Two Worlds]'
        name = 'Día Nacional de las Iglesias Evangélicas y Protestantes  [National Day of the  Evangelical and  Protestant Churches]'
        self[date(year, OCT, 31)] = name
        name = 'Día de Todos los Santos [All Saints Day]'
        self[date(year, NOV, 1)] = name
        self[date(year, DEC, 8)] = 'La Inmaculada Concepción [Immaculate Conception]'
        self[date(year, DEC, 25)] = 'Navidad [Christmas]'


class CL(Chile):
    pass


class Colombia(HolidayBase):

    def __init__(self, **kwargs):
        self.country = 'CO'
        HolidayBase.__init__(self, **kwargs)

    def _populate(self, year):
        if self.observed and date(year, JAN, 1).weekday() in WEEKEND:
            pass
        else:
            self[date(year, JAN, 1)] = "Año Nuevo [New Year's Day]"
        self[date(year, MAY, 1)] = 'Día del Trabajo [Labour Day]'
        name = 'Día de la Independencia [Independence Day]'
        if self.observed and date(year, JUL, 20).weekday() in WEEKEND:
            pass
        else:
            self[date(year, JUL, 20)] = name
        self[date(year, AUG, 7)] = 'Batalla de Boyacá [Battle of Boyacá]'
        if self.observed and date(year, DEC, 8).weekday() in WEEKEND:
            pass
        else:
            self[date(year, DEC, 8)] = 'La Inmaculada Concepción [Immaculate Conception]'
        self[date(year, DEC, 25)] = 'Navidad [Christmas]'
        name = 'Día de los Reyes Magos [Epiphany]'
        if date(year, JAN, 6).weekday() == MON or not self.observed:
            self[date(year, JAN, 6)] = name
        else:
            self[date(year, JAN, 6) + rd(weekday=MO)] = name + '(Observed)'
        name = "Día de San José [Saint Joseph's Day]"
        if date(year, MAR, 19).weekday() == MON or not self.observed:
            self[date(year, MAR, 19)] = name
        else:
            self[date(year, MAR, 19) + rd(weekday=MO)] = name + '(Observed)'
        name = 'San Pedro y San Pablo [Saint Peter and Saint Paul]'
        if date(year, JUN, 29).weekday() == MON or not self.observed:
            self[date(year, JUN, 29)] = name
        else:
            self[date(year, JUN, 29) + rd(weekday=MO)] = name + '(Observed)'
        name = 'La Asunción [Assumption of Mary]'
        if date(year, AUG, 15).weekday() == MON or not self.observed:
            self[date(year, AUG, 15)] = name
        else:
            self[date(year, AUG, 15) + rd(weekday=MO)] = name + '(Observed)'
        name = 'Descubrimiento de América [Discovery of America]'
        if date(year, OCT, 12).weekday() == MON or not self.observed:
            self[date(year, OCT, 12)] = name
        else:
            self[date(year, OCT, 12) + rd(weekday=MO)] = name + '(Observed)'
        name = "Dia de Todos los Santos [All Saint's Day]"
        if date(year, NOV, 1).weekday() == MON or not self.observed:
            self[date(year, NOV, 1)] = name
        else:
            self[date(year, NOV, 1) + rd(weekday=MO)] = name + '(Observed)'
        name = 'Independencia de Cartagena [Independence of Cartagena]'
        if date(year, NOV, 11).weekday() == MON or not self.observed:
            self[date(year, NOV, 11)] = name
        else:
            self[date(year, NOV, 11) + rd(weekday=MO)] = name + '(Observed)'
        self[easter(year) + rd(weekday=TH(-1))] = 'Jueves Santo [Maundy Thursday]'
        self[easter(year) + rd(weekday=FR(-1))] = 'Viernes Santo [Good Friday]'
        name = 'Ascensión del señor [Ascension of Jesus]'
        hdate = easter(year) + rd(days=+39)
        if hdate.weekday() == MON or not self.observed:
            self[hdate] = name
        else:
            self[hdate + rd(weekday=MO)] = name + '(Observed)'
        name = 'Corpus Christi [Corpus Christi]'
        hdate = easter(year) + rd(days=+60)
        if hdate.weekday() == MON or not self.observed:
            self[hdate] = name
        else:
            self[hdate + rd(weekday=MO)] = name + '(Observed)'
        name = 'Sagrado Corazón [Sacred Heart]'
        hdate = easter(year) + rd(days=+68)
        if hdate.weekday() == MON or not self.observed:
            self[hdate] = name
        else:
            self[hdate + rd(weekday=MO)] = name + '(Observed)'


class CO(Colombia):
    pass


class Mexico(HolidayBase):

    def __init__(self, **kwargs):
        self.country = 'MX'
        HolidayBase.__init__(self, **kwargs)

    def _populate(self, year):
        name = "Año Nuevo [New Year's Day]"
        self[date(year, JAN, 1)] = name
        if self.observed and date(year, JAN, 1).weekday() == SUN:
            self[date(year, JAN, 1) + rd(days=+1)] = name + ' (Observed)'
        elif self.observed and date(year, JAN, 1).weekday() == SAT:
            expand = self.expand
            self.expand = False
            self[date(year, JAN, 1) + rd(days=-1)] = name + ' (Observed)'
            self.expand = expand
        if self.observed and date(year, DEC, 31).weekday() == FRI:
            self[date(year, DEC, 31)] = name + ' (Observed)'
        name = 'Día de la Constitución [Constitution Day]'
        if 2006 >= year >= 1917:
            self[date(year, FEB, 5)] = name
        elif year >= 2007:
            self[date(year, FEB, 1) + rd(weekday=MO(+1))] = name
        name = "Natalicio de Benito Juárez [Benito Juárez's birthday]"
        if 2006 >= year >= 1917:
            self[date(year, MAR, 21)] = name
        elif year >= 2007:
            self[date(year, MAR, 1) + rd(weekday=MO(+3))] = name
        if year >= 1923:
            self[date(year, MAY, 1)] = 'Día del Trabajo [Labour Day]'
            if self.observed and date(year, MAY, 1).weekday() == SAT:
                self[date(year, MAY, 1) + rd(days=-1)] = name + ' (Observed)'
            elif self.observed and date(year, MAY, 1).weekday() == SUN:
                self[date(year, MAY, 1) + rd(days=+1)] = name + ' (Observed)'
        name = 'Día de la Independencia [Independence Day]'
        self[date(year, SEP, 16)] = name
        if self.observed and date(year, SEP, 16).weekday() == SAT:
            self[date(year, SEP, 16) + rd(days=-1)] = name + ' (Observed)'
        elif self.observed and date(year, SEP, 16).weekday() == SUN:
            self[date(year, SEP, 16) + rd(days=+1)] = name + ' (Observed)'
        name = 'Día de la Revolución [Revolution Day]'
        if 2006 >= year >= 1917:
            self[date(year, NOV, 20)] = name
        elif year >= 2007:
            self[date(year, NOV, 1) + rd(weekday=MO(+3))] = name
        name = 'Transmisión del Poder Ejecutivo Federal'
        name += ' [Change of Federal Government]'
        if (2018 - year) % 6 == 0:
            self[date(year, DEC, 1)] = name
            if self.observed and date(year, DEC, 1).weekday() == SAT:
                self[date(year, DEC, 1) + rd(days=-1)] = name + ' (Observed)'
            elif self.observed and date(year, DEC, 1).weekday() == SUN:
                self[date(year, DEC, 1) + rd(days=+1)] = name + ' (Observed)'
        self[date(year, DEC, 25)] = 'Navidad [Christmas]'
        if self.observed and date(year, DEC, 25).weekday() == SAT:
            self[date(year, DEC, 25) + rd(days=-1)] = name + ' (Observed)'
        elif self.observed and date(year, DEC, 25).weekday() == SUN:
            self[date(year, DEC, 25) + rd(days=+1)] = name + ' (Observed)'


class MX(Mexico):
    pass


class Ukraine(HolidayBase):
    """
    http://zakon1.rada.gov.ua/laws/show/322-08/paran454#n454
    """

    def __init__(self, **kwargs):
        self.country = 'UA'
        HolidayBase.__init__(self, **kwargs)

    def _populate(self, year):
        if year < 1918:
            return
        if year >= 1898:
            self[date(year, JAN, 1)] = 'Новий рік'
        if year >= 1991:
            self[date(year, JAN, 7)] = 'Різдво Христове (православне)'
        if year > 1965:
            self[date(year, MAR, 8)] = 'Міжнародний жіночий день'
        if year >= 1991:
            self[easter(year, method=EASTER_ORTHODOX)] = 'Пасха (Великдень)'
        if year >= 1991:
            self[easter(year, method=EASTER_ORTHODOX) + rd(days=49)] = 'Трійця'
        if year > 2017:
            name = 'День праці'
        elif 1917 < year <= 2017:
            name = 'День міжнародної солідарності трудящих'
        self[date(year, MAY, 1)] = name
        if 1928 < year < 2018:
            self[date(year, MAY, 2)] = 'День міжнародної солідарності трудящих'
        name = 'День перемоги'
        if year >= 1965:
            self[date(year, MAY, 9)] = name
        if 1945 <= year < 1947:
            self[date(year, MAY, 9)] = name
            self[date(year, SEP, 3)] = 'День перемоги над Японією'
        if year >= 1997:
            self[date(year, JUN, 28)] = 'День Конституції України'
        name = 'День незалежності України'
        if year > 1991:
            self[date(year, AUG, 24)] = name
        elif year == 1991:
            self[date(year, JUL, 16)] = name
        if year >= 2015:
            self[date(year, OCT, 14)] = 'День захисника України'
        name = 'День Конституції СРСР'
        if 1981 <= year < 1991:
            self[date(year, OCT, 7)] = name
        elif 1937 <= year < 1981:
            self[date(year, DEC, 5)] = name
        if 1917 < year < 2000:
            if year <= 1991:
                name = 'Річниця Великої Жовтневої соціалістичної революції'
            else:
                name = 'Річниця жовтневого перевороту'
            self[date(year, NOV, 7)] = name
            self[date(year, NOV, 8)] = name
        if year >= 2017:
            self[date(year, DEC, 25)] = 'Різдво Христове (католицьке)'
        if 1917 <= year < 1951:
            self[date(year, JAN, 22)] = "День пам'яті 9 січня 1905 року"
        if 1917 < year < 1929:
            self[date(year, MAR, 18)] = 'День паризької комуни'


class UA(Ukraine):
    pass


class UnitedStates(HolidayBase):
    STATES = [
     'AL', 'AK', 'AS', 'AZ', 'AR', 'CA', 'CO', 'CT', 'DE', 'DC', 'FL',
     'GA', 'GU', 'HI', 'ID', 'IL', 'IN', 'IA', 'KS', 'KY', 'LA', 'ME',
     'MD', 'MH', 'MA', 'MI', 'FM', 'MN', 'MS', 'MO', 'MT', 'NE', 'NV',
     'NH', 'NJ', 'NM', 'NY', 'NC', 'ND', 'MP', 'OH', 'OK', 'OR', 'PW',
     'PA', 'PR', 'RI', 'SC', 'SD', 'TN', 'TX', 'UT', 'VT', 'VA', 'VI',
     'WA', 'WV', 'WI', 'WY']

    def __init__(self, **kwargs):
        self.country = 'US'
        HolidayBase.__init__(self, **kwargs)

    def _populate(self, year):
        if year > 1870:
            name = "New Year's Day"
            self[date(year, JAN, 1)] = name
            if self.observed and date(year, JAN, 1).weekday() == SUN:
                self[date(year, JAN, 1) + rd(days=+1)] = name + ' (Observed)'
            elif self.observed and date(year, JAN, 1).weekday() == SAT:
                expand = self.expand
                self.expand = False
                self[date(year, JAN, 1) + rd(days=-1)] = name + ' (Observed)'
                self.expand = expand
            if self.observed and date(year, DEC, 31).weekday() == FRI:
                self[date(year, DEC, 31)] = name + ' (Observed)'
        if self.state == 'PR':
            self[date(year, JAN, 6)] = 'Epiphany'
        if self.state == 'VI':
            self[date(year, JAN, 6)] = "Three King's Day"
        name = 'Lee Jackson Day'
        if self.state == 'VA' and year >= 2000:
            dt = date(year, JAN, 1) + rd(weekday=MO(+3)) + rd(weekday=FR(-1))
            self[dt] = name
        elif self.state == 'VA' and year >= 1983:
            self[date(year, JAN, 1) + rd(weekday=MO(+3))] = name
        elif self.state == 'VA' and year >= 1889:
            self[date(year, JAN, 19)] = name
        if self.state in ('DC', 'LA', 'MD', 'VA') and year >= 1789:
            name = 'Inauguration Day'
            if (year - 1789) % 4 == 0 and year >= 1937:
                self[date(year, JAN, 20)] = name
                if date(year, JAN, 20).weekday() == SUN:
                    self[date(year, JAN, 21)] = name + ' (Observed)'
            elif (year - 1789) % 4 == 0:
                self[date(year, MAR, 4)] = name
                if date(year, MAR, 4).weekday() == SUN:
                    self[date(year, MAR, 5)] = name + ' (Observed)'
        if year >= 1986:
            name = 'Martin Luther King Jr. Day'
            if self.state == 'AL':
                name = 'Robert E. Lee/Martin Luther King Birthday'
            elif self.state in ('AS', 'MS'):
                name = "Dr. Martin Luther King Jr. and Robert E. Lee's Birthdays"
            elif self.state in ('AZ', 'NH'):
                name = 'Dr. Martin Luther King Jr./Civil Rights Day'
            elif self.state == 'GA' and year < 2012:
                name = "Robert E. Lee's Birthday"
            elif self.state == 'ID' and year >= 2006:
                name = 'Martin Luther King, Jr. - Idaho Human Rights Day'
            self[date(year, JAN, 1) + rd(weekday=MO(+3))] = name
        name = "Lincoln's Birthday"
        if (self.state in ('CT', 'IL', 'IA', 'NJ', 'NY') and year >= 1971 or self.state == 'CA') and 1971 <= year <= 2009:
            self[date(year, FEB, 12)] = name
            if self.observed and date(year, FEB, 12).weekday() == SAT:
                self[date(year, FEB, 11)] = name + ' (Observed)'
            elif self.observed and date(year, FEB, 12).weekday() == SUN:
                self[date(year, FEB, 13)] = name + ' (Observed)'
        if self.state == 'CA' and year >= 2014 or self.state == 'FL' and year >= 2011 or self.state == 'NY' and year >= 2004 or self.state == 'WI' and year >= 1976:
            self[date(year, FEB, 15)] = 'Susan B. Anthony Day'
        name = "Washington's Birthday"
        if self.state == 'AL':
            name = 'George Washington/Thomas Jefferson Birthday'
        elif self.state == 'AS':
            name = "George Washington's Birthday and Daisy Gatson Bates Day"
        elif self.state in ('PR', 'VI'):
            name = "Presidents' Day"
        if self.state not in ('DE', 'FL', 'GA', 'NM', 'PR'):
            if year > 1970:
                self[date(year, FEB, 1) + rd(weekday=MO(+3))] = name
            elif year >= 1879:
                self[date(year, FEB, 22)] = name
        elif self.state == 'GA':
            if date(year, DEC, 24).weekday() != WED:
                self[date(year, DEC, 24)] = name
            else:
                self[date(year, DEC, 26)] = name
        elif self.state in ('PR', 'VI'):
            self[date(year, FEB, 1) + rd(weekday=MO(+3))] = name
        if self.state == 'LA' and year >= 1857:
            self[easter(year) + rd(days=-47)] = 'Mardi Gras'
        if self.state == 'GU' and year >= 1970:
            self[date(year, MAR, 1) + rd(weekday=MO)] = 'Guam Discovery Day'
        if self.state == 'IL' and year >= 1978:
            self[date(year, MAR, 1) + rd(weekday=MO)] = 'Casimir Pulaski Day'
        if self.state == 'TX' and year >= 1874:
            self[date(year, MAR, 2)] = 'Texas Independence Day'
        if self.state == 'VT' and year >= 1800:
            self[date(year, MAR, 1) + rd(weekday=TU)] = 'Town Meeting Day'
        if self.state == 'MA' and year >= 1901:
            name = 'Evacuation Day'
            self[date(year, MAR, 17)] = name
            if date(year, MAR, 17).weekday() in WEEKEND:
                self[date(year, MAR, 17) + rd(weekday=MO)] = name + ' (Observed)'
        if self.state == 'PR':
            self[date(year, MAR, 22)] = 'Emancipation Day'
            if self.observed and date(year, MAR, 22).weekday() == SUN:
                self[date(year, MAR, 23)] = 'Emancipation Day (Observed)'
        if self.state == 'HI' and year >= 1949:
            name = 'Prince Jonah Kuhio Kalanianaole Day'
            self[date(year, MAR, 26)] = name
            if self.observed and date(year, MAR, 26).weekday() == SAT:
                self[date(year, MAR, 25)] = name + ' (Observed)'
            elif self.observed and date(year, MAR, 26).weekday() == SUN:
                self[date(year, MAR, 27)] = name + ' (Observed)'
        name = "Steward's Day"
        if self.state == 'AK' and year >= 1955:
            self[date(year, APR, 1) + rd(days=-1, weekday=MO(-1))] = name
        elif self.state == 'AK' and year >= 1918:
            self[date(year, MAR, 30)] = name
        name = 'César Chávez Day'
        if self.state == 'CA' and year >= 1995:
            self[date(year, MAR, 31)] = name
            if self.observed and date(year, MAR, 31).weekday() == SUN:
                self[date(year, APR, 1)] = name + ' (Observed)'
        elif self.state == 'TX' and year >= 2000:
            self[date(year, MAR, 31)] = name
        if self.state == 'VI':
            self[date(year, MAR, 31)] = 'Transfer Day'
        if self.state == 'DC' and year >= 2005:
            name = 'Emancipation Day'
            self[date(year, APR, 16)] = name
            if self.observed and date(year, APR, 16).weekday() == SAT:
                self[date(year, APR, 15)] = name + ' (Observed)'
            elif self.observed and date(year, APR, 16).weekday() == SUN:
                self[date(year, APR, 17)] = name + ' (Observed)'
        if self.state in ('ME', 'MA') and year >= 1969:
            self[date(year, APR, 1) + rd(weekday=MO(+3))] = "Patriots' Day"
        elif self.state in ('ME', 'MA') and year >= 1894:
            self[date(year, APR, 19)] = "Patriots' Day"
        if self.state == 'VI':
            self[easter(year) + rd(weekday=TH(-1))] = 'Holy Thursday'
        if self.state in ('CT', 'DE', 'GU', 'IN', 'KY', 'LA', 'NJ', 'NC', 'PR', 'TN',
                          'TX', 'VI'):
            self[easter(year) + rd(weekday=FR(-1))] = 'Good Friday'
        if self.state == 'VI':
            self[easter(year) + rd(weekday=MO)] = 'Easter Monday'
        name = 'Confederate Memorial Day'
        if self.state in ('AL', 'GA', 'MS', 'SC') and year >= 1866:
            if self.state == 'GA' and year >= 2016:
                name = 'State Holiday'
            self[date(year, APR, 1) + rd(weekday=MO(+4))] = name
        elif self.state == 'TX' and year >= 1931:
            self[date(year, JAN, 19)] = name
        if self.state == 'TX' and year >= 1875:
            self[date(year, APR, 21)] = 'San Jacinto Day'
        if self.state == 'NE' and year >= 1989:
            self[date(year, APR, 30) + rd(weekday=FR(-1))] = 'Arbor Day'
        elif self.state == 'NE' and year >= 1875:
            self[date(year, APR, 22)] = 'Arbor Day'
        if self.state == 'IN' and (year >= 2006 and year % 2 == 0 or year >= 2015):
            dt = date(year, MAY, 1) + rd(weekday=MO)
            self[dt + rd(days=+1)] = 'Primary Election Day'
        if self.state == 'MO' and year >= 1949:
            name = 'Truman Day'
            self[date(year, MAY, 8)] = name
            if self.observed and date(year, MAY, 8).weekday() == SAT:
                self[date(year, MAY, 7)] = name + ' (Observed)'
            elif self.observed and date(year, MAY, 8).weekday() == SUN:
                self[date(year, MAY, 10)] = name + ' (Observed)'
        if year > 1970:
            self[date(year, MAY, 31) + rd(weekday=MO(-1))] = 'Memorial Day'
        elif year >= 1888:
            self[date(year, MAY, 30)] = 'Memorial Day'
        name = 'Jefferson Davis Birthday'
        if self.state == 'AL' and year >= 1890:
            self[date(year, JUN, 1) + rd(weekday=MO)] = name
        if self.state == 'HI' and year >= 1872:
            self[date(year, JUN, 11)] = 'Kamehameha Day'
            if self.observed and year >= 2011:
                if date(year, JUN, 11).weekday() == SAT:
                    self[date(year, JUN, 10)] = 'Kamehameha Day (Observed)'
                elif date(year, JUN, 11).weekday() == SUN:
                    self[date(year, JUN, 12)] = 'Kamehameha Day (Observed)'
        if self.state == 'TX' and year >= 1980:
            self[date(year, JUN, 19)] = 'Emancipation Day In Texas'
        name = 'West Virginia Day'
        if self.state == 'WV' and year >= 1927:
            self[date(year, JUN, 20)] = name
            if self.observed and date(year, JUN, 20).weekday() == SAT:
                self[date(year, JUN, 19)] = name + ' (Observed)'
            elif self.observed and date(year, JUN, 20).weekday() == SUN:
                self[date(year, JUN, 21)] = name + ' (Observed)'
        if self.state == 'VI':
            self[date(year, JUL, 3)] = 'Emancipation Day'
        if year > 1870:
            name = 'Independence Day'
            self[date(year, JUL, 4)] = name
            if self.observed and date(year, JUL, 4).weekday() == SAT:
                self[date(year, JUL, 4) + rd(days=-1)] = name + ' (Observed)'
            elif self.observed and date(year, JUL, 4).weekday() == SUN:
                self[date(year, JUL, 4) + rd(days=+1)] = name + ' (Observed)'
        if self.state == 'GU' and year >= 1945:
            self[date(year, JUL, 21)] = 'Liberation Day (Guam)'
        if self.state == 'UT' and year >= 1849:
            name = 'Pioneer Day'
            self[date(year, JUL, 24)] = name
            if self.observed and date(year, JUL, 24).weekday() == SAT:
                self[date(year, JUL, 24) + rd(days=-1)] = name + ' (Observed)'
            elif self.observed and date(year, JUL, 24).weekday() == SUN:
                self[date(year, JUL, 24) + rd(days=+1)] = name + ' (Observed)'
        if self.state == 'PR':
            self[date(year, JUL, 25)] = 'Constitution Day'
            if self.observed and date(year, JUL, 25).weekday() == SUN:
                self[date(year, JUL, 26)] = 'Constitution Day (Observed)'
        if self.state == 'RI' and year >= 1948:
            self[date(year, AUG, 1) + rd(weekday=MO(+2))] = 'Victory Day'
        if self.state == 'HI' and year >= 1959:
            self[date(year, AUG, 1) + rd(weekday=FR(+3))] = 'Statehood Day'
        if self.state == 'VT' and year >= 1778:
            name = 'Bennington Battle Day'
            self[date(year, AUG, 16)] = name
            if self.observed and date(year, AUG, 16).weekday() == SAT:
                self[date(year, AUG, 15)] = name + ' (Observed)'
            elif self.observed and date(year, AUG, 16).weekday() == SUN:
                self[date(year, AUG, 17)] = name + ' (Observed)'
        if self.state == 'TX' and year >= 1973:
            self[date(year, AUG, 27)] = 'Lyndon Baines Johnson Day'
        if year >= 1894:
            self[date(year, SEP, 1) + rd(weekday=MO)] = 'Labor Day'
        if self.state not in ('AK', 'AR', 'DE', 'FL', 'HI', 'NV'):
            if self.state == 'SD':
                name = 'Native American Day'
            elif self.state == 'VI':
                name = 'Columbus Day and Puerto Rico Friendship Day'
            else:
                name = 'Columbus Day'
            if year >= 1970:
                self[date(year, OCT, 1) + rd(weekday=MO(+2))] = name
            elif year >= 1937:
                self[date(year, OCT, 12)] = name
        if self.state == 'AK' and year >= 1867:
            self[date(year, OCT, 18)] = 'Alaska Day'
            if self.observed and date(year, OCT, 18).weekday() == SAT:
                self[date(year, OCT, 18) + rd(days=-1)] = name + ' (Observed)'
            elif self.observed and date(year, OCT, 18).weekday() == SUN:
                self[date(year, OCT, 18) + rd(days=+1)] = name + ' (Observed)'
        if self.state == 'NV' and year >= 1933:
            dt = date(year, OCT, 31)
            if year >= 2000:
                dt += rd(weekday=FR(-1))
            self[dt] = 'Nevada Day'
            if self.observed and dt.weekday() == SAT:
                self[dt + rd(days=-1)] = 'Nevada Day (Observed)'
            elif self.observed and dt.weekday() == SUN:
                self[dt + rd(days=+1)] = 'Nevada Day (Observed)'
        if self.state == 'VI':
            self[date(year, NOV, 1)] = 'Liberty Day'
        if self.state in ('DE', 'HI', 'IL', 'IN', 'LA', 'MT', 'NH', 'NJ', 'NY', 'WV') and year >= 2008 and year % 2 == 0 or self.state in ('IN',
                                                                                                                                           'NY') and year >= 2015:
            dt = date(year, NOV, 1) + rd(weekday=MO)
            self[dt + rd(days=+1)] = 'Election Day'
        if self.state == 'GU':
            self[date(year, NOV, 2)] = "All Souls' Day"
        if year > 1953:
            name = 'Veterans Day'
        else:
            name = 'Armistice Day'
        if 1978 > year > 1970:
            self[date(year, OCT, 1) + rd(weekday=MO(+4))] = name
        elif year >= 1938:
            self[date(year, NOV, 11)] = name
            if self.observed and date(year, NOV, 11).weekday() == SAT:
                self[date(year, NOV, 11) + rd(days=-1)] = name + ' (Observed)'
            elif self.observed and date(year, NOV, 11).weekday() == SUN:
                self[date(year, NOV, 11) + rd(days=+1)] = name + ' (Observed)'
        if self.state == 'PR':
            self[date(year, NOV, 19)] = 'Discovery Day'
            if self.observed and date(year, NOV, 19).weekday() == SUN:
                self[date(year, NOV, 20)] = 'Discovery Day (Observed)'
        if year > 1870:
            self[date(year, NOV, 1) + rd(weekday=TH(+4))] = 'Thanksgiving'
        if self.state in ('DE', 'FL', 'NH', 'NC', 'OK', 'TX', 'WV') and year >= 1975 or self.state == 'IN' and year >= 2010 or self.state == 'MD' and year >= 2008 or self.state in ('NV',
                                                                                                                                                                                     'NM'):
            if self.state in ('DE', 'NH', 'NC', 'OK', 'WV'):
                name = 'Day After Thanksgiving'
            elif self.state in ('FL', 'TX'):
                name = 'Friday After Thanksgiving'
            elif self.state == 'IN':
                name = "Lincoln's Birthday"
            elif self.state == 'MD' and year >= 2008:
                name = 'American Indian Heritage Day'
            elif self.state == 'NV':
                name = 'Family Day'
            elif self.state == 'NM':
                name = "Presidents' Day"
            dt = date(year, NOV, 1) + rd(weekday=TH(+4))
            self[dt + rd(days=+1)] = name
        if self.state == 'GA' and year >= 1986:
            if year >= 2016:
                name = 'State Holiday'
            else:
                name = "Robert E. Lee's Birthday"
            self[date(year, NOV, 29) + rd(weekday=FR(-1))] = name
        if self.state == 'GU':
            self[date(year, DEC, 8)] = 'Lady of Camarin Day'
        if self.state == 'AS' or self.state in ('KS', 'MI', 'NC') and year >= 2013 or self.state == 'TX' and year >= 1981 or self.state == 'WI' and year >= 2012:
            name = 'Christmas Eve'
            self[date(year, DEC, 24)] = name
            name = name + ' (Observed)'
            if self.observed and date(year, DEC, 24).weekday() == FRI:
                self[date(year, DEC, 24) + rd(days=-1)] = name
            elif self.observed and date(year, DEC, 24).weekday() in WEEKEND:
                self[date(year, DEC, 24) + rd(weekday=FR(-1))] = name
        if year > 1870:
            name = 'Christmas Day'
            self[date(year, DEC, 25)] = 'Christmas Day'
            if self.observed and date(year, DEC, 25).weekday() == SAT:
                self[date(year, DEC, 25) + rd(days=-1)] = name + ' (Observed)'
            elif self.observed and date(year, DEC, 25).weekday() == SUN:
                self[date(year, DEC, 25) + rd(days=+1)] = name + ' (Observed)'
        if self.state == 'NC' and year >= 2013:
            name = 'Day After Christmas'
            self[date(year, DEC, 26)] = name
            name = name + ' (Observed)'
            if self.observed and date(year, DEC, 26).weekday() in WEEKEND:
                self[date(year, DEC, 26) + rd(weekday=MO)] = name
            elif self.observed and date(year, DEC, 26).weekday() == MON:
                self[date(year, DEC, 26) + rd(days=+1)] = name
        elif self.state == 'TX' and year >= 1981:
            self[date(year, DEC, 26)] = 'Day After Christmas'
        elif self.state == 'VI':
            self[date(year, DEC, 26)] = 'Christmas Second Day'
        if self.state in ('KY', 'MI') and year >= 2013 or self.state == 'WI' and year >= 2012:
            name = "New Year's Eve"
            self[date(year, DEC, 31)] = name
            if self.observed and date(year, DEC, 31).weekday() == SAT:
                self[date(year, DEC, 30)] = name + ' (Observed)'


class US(UnitedStates):
    pass


class NewZealand(HolidayBase):
    PROVINCES = [
     'NTL', 'AUK', 'TKI', 'HKB', 'WGN', 'MBH', 'NSN', 'CAN',
     'STC', 'WTL', 'OTA', 'STL', 'CIT']

    def __init__(self, **kwargs):
        self.country = 'NZ'
        HolidayBase.__init__(self, **kwargs)

    def _populate(self, year):
        if year < 1894:
            return
        name = "New Year's Day"
        jan1 = date(year, JAN, 1)
        self[jan1] = name
        if self.observed and jan1.weekday() in WEEKEND:
            self[date(year, JAN, 3)] = name + ' (Observed)'
        name = "Day after New Year's Day"
        jan2 = date(year, JAN, 2)
        self[jan2] = name
        if self.observed and jan2.weekday() in WEEKEND:
            self[date(year, JAN, 4)] = name + ' (Observed)'
        if year > 1973:
            name = 'New Zealand Day'
            if year > 1976:
                name = 'Waitangi Day'
            feb6 = date(year, FEB, 6)
            self[feb6] = name
            if self.observed and year >= 2014 and feb6.weekday() in WEEKEND:
                self[feb6 + rd(weekday=MO)] = name + ' (Observed)'
        self[easter(year) + rd(weekday=FR(-1))] = 'Good Friday'
        self[easter(year) + rd(weekday=MO)] = 'Easter Monday'
        if year > 1920:
            name = 'Anzac Day'
            apr25 = date(year, APR, 25)
            self[apr25] = name
            if self.observed and year >= 2014 and apr25.weekday() in WEEKEND:
                self[apr25 + rd(weekday=MO)] = name + ' (Observed)'
        if year >= 1952:
            name = "Queen's Birthday"
        elif year > 1901:
            name = "King's Birthday"
        if year == 1952:
            self[date(year, JUN, 2)] = name
        elif year > 1937:
            self[date(year, JUN, 1) + rd(weekday=MO(+1))] = name
        elif year == 1937:
            self[date(year, JUN, 9)] = name
        elif year == 1936:
            self[date(year, JUN, 23)] = name
        elif year > 1911:
            self[date(year, JUN, 3)] = name
        elif year > 1901:
            self[date(year, NOV, 9)] = name
        name = 'Labour Day'
        if year >= 1910:
            self[date(year, OCT, 1) + rd(weekday=MO(+4))] = name
        elif year > 1899:
            self[date(year, OCT, 1) + rd(weekday=WE(+2))] = name
        name = 'Christmas Day'
        dec25 = date(year, DEC, 25)
        self[dec25] = name
        if self.observed and dec25.weekday() in WEEKEND:
            self[date(year, DEC, 27)] = name + ' (Observed)'
        name = 'Boxing Day'
        dec26 = date(year, DEC, 26)
        self[dec26] = name
        if self.observed and dec26.weekday() in WEEKEND:
            self[date(year, DEC, 28)] = name + ' (Observed)'
        if self.prov in ('NTL', 'Northland', 'AUK', 'Auckland'):
            if 1963 < year <= 1973 and self.prov in ('NTL', 'Northland'):
                name = 'Waitangi Day'
                dt = date(year, FEB, 6)
            else:
                name = 'Auckland Anniversary Day'
                dt = date(year, JAN, 29)
            if dt.weekday() in (TUE, WED, THU):
                self[dt + rd(weekday=MO(-1))] = name
            else:
                self[dt + rd(weekday=MO)] = name
        elif self.prov in ('TKI', 'Taranaki', 'New Plymouth'):
            name = 'Taranaki Anniversary Day'
            self[date(year, MAR, 1) + rd(weekday=MO(+2))] = name
        elif self.prov in ('HKB', "Hawke's Bay"):
            name = "Hawke's Bay Anniversary Day"
            labour_day = date(year, OCT, 1) + rd(weekday=MO(+4))
            self[labour_day + rd(weekday=FR(-1))] = name
        elif self.prov in ('WGN', 'Wellington'):
            name = 'Wellington Anniversary Day'
            jan22 = date(year, JAN, 22)
            if jan22.weekday() in (TUE, WED, THU):
                self[jan22 + rd(weekday=MO(-1))] = name
            else:
                self[jan22 + rd(weekday=MO)] = name
        elif self.prov in ('MBH', 'Marlborough'):
            name = 'Marlborough Anniversary Day'
            labour_day = date(year, OCT, 1) + rd(weekday=MO(+4))
            self[labour_day + rd(weeks=1)] = name
        elif self.prov in ('NSN', 'Nelson'):
            name = 'Nelson Anniversary Day'
            feb1 = date(year, FEB, 1)
            if feb1.weekday() in (TUE, WED, THU):
                self[feb1 + rd(weekday=MO(-1))] = name
            else:
                self[feb1 + rd(weekday=MO)] = name
        elif self.prov in ('CAN', 'Canterbury'):
            name = 'Canterbury Anniversary Day'
            showday = date(year, NOV, 1) + rd(weekday=TU) + rd(weekday=FR(+2))
            self[showday] = name
        elif self.prov in ('STC', 'South Canterbury'):
            name = 'South Canterbury Anniversary Day'
            dominion_day = date(year, SEP, 1) + rd(weekday=MO(4))
            self[dominion_day] = name
        elif self.prov in ('WTL', 'Westland'):
            name = 'Westland Anniversary Day'
            dec1 = date(year, DEC, 1)
            if year == 2005:
                self[date(year, DEC, 5)] = name
            elif dec1.weekday() in (TUE, WED, THU):
                self[dec1 + rd(weekday=MO(-1))] = name
            else:
                self[dec1 + rd(weekday=MO)] = name
        elif self.prov in ('OTA', 'Otago'):
            name = 'Otago Anniversary Day'
            mar23 = date(year, MAR, 23)
            if mar23.weekday() in (TUE, WED, THU):
                dt = mar23 + rd(weekday=MO(-1))
            else:
                dt = mar23 + rd(weekday=MO)
            if dt == easter(year) + rd(weekday=MO):
                dt += rd(days=1)
            self[dt] = name
        elif self.prov in ('STL', 'Southland'):
            name = 'Southland Anniversary Day'
            jan17 = date(year, JAN, 17)
            if year > 2011:
                self[easter(year) + rd(weekday=TU)] = name
            elif jan17.weekday() in (TUE, WED, THU):
                self[jan17 + rd(weekday=MO(-1))] = name
            else:
                self[jan17 + rd(weekday=MO)] = name
        elif self.prov in ('CIT', 'Chatham Islands'):
            name = 'Chatham Islands Anniversary Day'
            nov30 = date(year, NOV, 30)
            if nov30.weekday() in (TUE, WED, THU):
                self[nov30 + rd(weekday=MO(-1))] = name
            else:
                self[nov30 + rd(weekday=MO)] = name


class NZ(NewZealand):
    pass


class Australia(HolidayBase):
    PROVINCES = [
     'ACT', 'NSW', 'NT', 'QLD', 'SA', 'TAS', 'VIC', 'WA']

    def __init__(self, **kwargs):
        self.country = 'AU'
        self.prov = kwargs.pop('prov', None)
        HolidayBase.__init__(self, **kwargs)
        return

    def _populate(self, year):
        name = "New Year's Day"
        jan1 = date(year, JAN, 1)
        self[jan1] = name
        if self.observed and jan1.weekday() in WEEKEND:
            self[jan1 + rd(weekday=MO)] = name + ' (Observed)'
        jan26 = date(year, JAN, 26)
        if year >= 1935:
            if self.prov == 'NSW' and year < 1946:
                name = 'Anniversary Day'
            else:
                name = 'Australia Day'
            self[jan26] = name
            if self.observed and year >= 1946 and jan26.weekday() in WEEKEND:
                self[jan26 + rd(weekday=MO)] = name + ' (Observed)'
        elif year >= 1888 and self.prov != 'SA':
            name = 'Anniversary Day'
            self[jan26] = name
        if self.prov == 'SA':
            name = 'Adelaide Cup'
            if year >= 2006:
                self[date(year, MAR, 1) + rd(weekday=MO(+2))] = name
            else:
                self[date(year, MAR, 1) + rd(weekday=MO(+3))] = name
        if self.prov == 'ACT' and year >= 1913:
            name = 'Canberra Day'
            if year >= 1913 and year <= 1957:
                self[date(year, MAR, 12)] = name
            elif year >= 1958 and year <= 2007:
                self[date(year, MAR, 1) + rd(weekday=MO(+3))] = name
            elif year >= 2008 and year != 2012:
                self[date(year, MAR, 1) + rd(weekday=MO(+2))] = name
            elif year == 2012:
                self[date(year, MAR, 12)] = name
        self[easter(year) + rd(weekday=FR(-1))] = 'Good Friday'
        if self.prov in ('ACT', 'NSW', 'NT', 'QLD', 'SA', 'VIC'):
            self[easter(year) + rd(weekday=SA(-1))] = 'Easter Saturday'
        if self.prov in ('ACT', 'NSW', 'QLD', 'VIC'):
            self[easter(year)] = 'Easter Sunday'
        self[easter(year) + rd(weekday=MO)] = 'Easter Monday'
        if year > 1920:
            name = 'Anzac Day'
            apr25 = date(year, APR, 25)
            self[apr25] = name
            if self.observed:
                if apr25.weekday() == SAT and self.prov in ('WA', 'NT'):
                    self[apr25 + rd(weekday=MO)] = name + ' (Observed)'
                elif apr25.weekday() == SUN and self.prov in ('ACT', 'QLD', 'SA', 'WA',
                                                              'NT'):
                    self[apr25 + rd(weekday=MO)] = name + ' (Observed)'
        if self.prov == 'WA' and year > 1832:
            if year >= 2015:
                name = 'Western Australia Day'
            else:
                name = 'Foundation Day'
            self[date(year, JUN, 1) + rd(weekday=MO(+1))] = name
        if year >= 1952:
            name = "Queen's Birthday"
        elif year > 1901:
            name = "King's Birthday"
        if year >= 1936:
            name = "Queen's Birthday"
            if self.prov == 'QLD':
                if year == 2012:
                    self[date(year, JUN, 11)] = "Queen's Diamond Jubilee"
                if year < 2016 and year != 2012:
                    dt = date(year, JUN, 1) + rd(weekday=MO(+2))
                    self[dt] = name
                else:
                    dt = date(year, OCT, 1) + rd(weekday=MO)
                    self[dt] = name
            elif self.prov == 'WA':
                self[date(year, OCT, 1) + rd(weekday=MO(-1))] = name
            elif self.prov in ('NSW', 'VIC', 'ACT', 'SA', 'NT', 'TAS'):
                dt = date(year, JUN, 1) + rd(weekday=MO(+2))
                self[dt] = name
        elif year > 1911:
            self[date(year, JUN, 3)] = name
        elif year > 1901:
            self[date(year, NOV, 9)] = name
        if self.prov == 'NT':
            name = 'Picnic Day'
            self[date(year, AUG, 1) + rd(weekday=MO)] = name
        if self.prov == 'NSW':
            if year >= 1912:
                name = 'Bank Holiday'
                self[date(year, 8, 1) + rd(weekday=MO)] = name
        name = 'Labour Day'
        if self.prov in ('NSW', 'ACT', 'SA'):
            self[date(year, OCT, 1) + rd(weekday=MO)] = name
        elif self.prov == 'WA':
            self[date(year, MAR, 1) + rd(weekday=MO)] = name
        elif self.prov == 'VIC':
            self[date(year, MAR, 1) + rd(weekday=MO(+2))] = name
        elif self.prov == 'QLD':
            if 2013 <= year <= 2015:
                self[date(year, OCT, 1) + rd(weekday=MO)] = name
            else:
                self[date(year, MAY, 1) + rd(weekday=MO)] = name
        elif self.prov == 'NT':
            name = 'May Day'
            self[date(year, MAY, 1) + rd(weekday=MO)] = name
        elif self.prov == 'TAS':
            name = 'Eight Hours Day'
            self[date(year, MAR, 1) + rd(weekday=MO(+2))] = name
        if self.prov == 'ACT':
            name = 'Family & Community Day'
            if 2007 <= year <= 2009:
                self[date(year, NOV, 1) + rd(weekday=TU)] = name
            elif year == 2010:
                self[date(year, SEP, 26)] = name
            elif year == 2011:
                self[date(year, OCT, 10)] = name
            elif year == 2012:
                self[date(year, OCT, 8)] = name
            elif year == 2013:
                self[date(year, SEP, 30)] = name
            elif year == 2014:
                self[date(year, SEP, 29)] = name
            elif year == 2015:
                self[date(year, SEP, 28)] = name
            elif year == 2016:
                self[date(year, SEP, 26)] = name
            elif year == 2017:
                self[date(year, SEP, 25)] = name
        if self.prov == 'ACT':
            name = 'Reconciliation Day'
            if year >= 2018:
                self[date(year, 5, 27) + rd(weekday=MO)] = name
        if self.prov == 'VIC':
            if year >= 2015:
                self[date(year, SEP, 24) + rd(weekday=FR)] = 'Grand Final Day'
            self[date(year, NOV, 1) + rd(weekday=TU)] = 'Melbourne Cup'
        if self.prov == 'QLD':
            name = 'The Royal Queensland Show'
            self[date(year, AUG, 5) + rd(weekday=FR) + rd(weekday=WE)] = name
        name = 'Christmas Day'
        dec25 = date(year, DEC, 25)
        self[dec25] = name
        if self.observed and dec25.weekday() in WEEKEND:
            self[date(year, DEC, 27)] = name + ' (Observed)'
        if self.prov == 'SA':
            name = 'Proclamation Day'
        else:
            name = 'Boxing Day'
        dec26 = date(year, DEC, 26)
        self[dec26] = name
        if self.observed and dec26.weekday() in WEEKEND:
            self[date(year, DEC, 28)] = name + ' (Observed)'


class AU(Australia):
    pass


class Germany(HolidayBase):
    """Official holidays for Germany in its current form.

    This class doesn't return any holidays before 1990-10-03.

    Before that date the current Germany was separated into the "German
    Democratic Republic" and the "Federal Republic of Germany" which both had
    somewhat different holidays. Since this class is called "Germany" it
    doesn't really make sense to include the days from the two former
    countries.

    Note that Germany doesn't have rules for holidays that happen on a
    Sunday. Those holidays are still holiday days but there is no additional
    day to make up for the "lost" day.

    Also note that German holidays are partly declared by each province there
    are some weired edge cases:

        - "Mariä Himmelfahrt" is only a holiday in Bavaria (BY) if your
          municipality is mostly catholic which in term depends on census data.
          Since we don't have this data but most municipalities in Bavaria
          *are* mostly catholic, we count that as holiday for whole Bavaria.
        - There is an "Augsburger Friedensfest" which only exists in the town
          Augsburg. This is excluded for Bavaria.
        - "Gründonnerstag" (Thursday before easter) is not a holiday but pupil
           don't have to go to school (but only in Baden Württemberg) which is
           solved by adjusting school holidays to include this day. It is
           excluded from our list.
        - "Fronleichnam" is a holiday in certain, explicitly defined
          municipalities in Saxony (SN) and Thuringia (TH). We exclude it from
          both provinces.
    """
    PROVINCES = [
     'BW', 'BY', 'BE', 'BB', 'HB', 'HH', 'HE', 'MV', 'NI', 'NW',
     'RP', 'SL', 'SN', 'ST', 'SH', 'TH']

    def __init__(self, **kwargs):
        self.country = 'DE'
        self.prov = kwargs.pop('prov', None)
        HolidayBase.__init__(self, **kwargs)
        return

    def _populate(self, year):
        if year <= 1989:
            return
        if year > 1990:
            self[date(year, JAN, 1)] = 'Neujahr'
            if self.prov in ('BW', 'BY', 'ST'):
                self[date(year, JAN, 6)] = 'Heilige Drei Könige'
            self[easter(year) - rd(days=2)] = 'Karfreitag'
            if self.prov == 'BB':
                self[easter(year)] = 'Ostersonntag'
            self[easter(year) + rd(days=1)] = 'Ostermontag'
            self[date(year, MAY, 1)] = 'Erster Mai'
            if self.prov == 'BE' and year == 2020:
                self[date(year, MAY, 8)] = '75. Jahrestag der Befreiung vom Nationalsozialismus und der Beendigung des Zweiten Weltkriegs in Europa'
            self[easter(year) + rd(days=39)] = 'Christi Himmelfahrt'
            if self.prov == 'BB':
                self[easter(year) + rd(days=49)] = 'Pfingstsonntag'
            self[easter(year) + rd(days=50)] = 'Pfingstmontag'
            if self.prov in ('BW', 'BY', 'HE', 'NW', 'RP', 'SL'):
                self[easter(year) + rd(days=60)] = 'Fronleichnam'
            if self.prov in ('BY', 'SL'):
                self[date(year, AUG, 15)] = 'Mariä Himmelfahrt'
        self[date(year, OCT, 3)] = 'Tag der Deutschen Einheit'
        if self.prov in ('BB', 'MV', 'SN', 'ST', 'TH'):
            self[date(year, OCT, 31)] = 'Reformationstag'
        if self.prov in ('HB', 'SH', 'NI', 'HH') and year >= 2018:
            self[date(year, OCT, 31)] = 'Reformationstag'
        if year == 2017:
            self[date(year, OCT, 31)] = 'Reformationstag'
        if self.prov in ('BW', 'BY', 'NW', 'RP', 'SL'):
            self[date(year, NOV, 1)] = 'Allerheiligen'
        if year <= 1994 or self.prov == 'SN':
            base_data = date(year, NOV, 23)
            weekday_delta = WE(-2) if base_data.weekday() == 2 else WE(-1)
            self[base_data + rd(weekday=weekday_delta)] = 'Buß- und Bettag'
        if year >= 2019:
            if self.prov == 'TH':
                self[date(year, SEP, 20)] = 'Weltkindertag'
            if self.prov == 'BE':
                self[date(year, MAR, 8)] = 'Internationaler Frauentag'
        self[date(year, DEC, 25)] = 'Erster Weihnachtstag'
        self[date(year, DEC, 26)] = 'Zweiter Weihnachtstag'


class DE(Germany):
    pass


class Austria(HolidayBase):
    PROVINCES = [
     'B', 'K', 'N', 'O', 'S', 'ST', 'T', 'V', 'W']

    def __init__(self, **kwargs):
        self.country = 'AT'
        self.prov = kwargs.pop('prov', kwargs.pop('state', 'W'))
        HolidayBase.__init__(self, **kwargs)

    def _populate(self, year):
        self[date(year, JAN, 1)] = 'Neujahr'
        self[date(year, JAN, 6)] = 'Heilige Drei Könige'
        self[easter(year) + rd(weekday=MO)] = 'Ostermontag'
        self[date(year, MAY, 1)] = 'Staatsfeiertag'
        self[easter(year) + rd(days=39)] = 'Christi Himmelfahrt'
        self[easter(year) + rd(days=50)] = 'Pfingstmontag'
        self[easter(year) + rd(days=60)] = 'Fronleichnam'
        self[date(year, AUG, 15)] = 'Mariä Himmelfahrt'
        if 1919 <= year <= 1934:
            self[date(year, NOV, 12)] = 'Nationalfeiertag'
        if year >= 1967:
            self[date(year, OCT, 26)] = 'Nationalfeiertag'
        self[date(year, NOV, 1)] = 'Allerheiligen'
        self[date(year, DEC, 8)] = 'Mariä Empfängnis'
        self[date(year, DEC, 25)] = 'Christtag'
        self[date(year, DEC, 26)] = 'Stefanitag'


class AT(Austria):
    pass


class Denmark(HolidayBase):

    def __init__(self, **kwargs):
        self.country = 'DK'
        HolidayBase.__init__(self, **kwargs)

    def _populate(self, year):
        self[date(year, JAN, 1)] = 'Nytårsdag'
        self[easter(year) + rd(weekday=SU(-2))] = 'Palmesøndag'
        self[easter(year) + rd(weekday=TH(-1))] = 'Skærtorsdag'
        self[easter(year) + rd(weekday=FR(-1))] = 'Langfredag'
        self[easter(year)] = 'Påskedag'
        self[easter(year) + rd(weekday=MO)] = 'Anden påskedag'
        self[easter(year) + rd(weekday=FR(+4))] = 'Store bededag'
        self[easter(year) + rd(days=39)] = 'Kristi himmelfartsdag'
        self[easter(year) + rd(days=49)] = 'Pinsedag'
        self[easter(year) + rd(days=50)] = 'Anden pinsedag'
        self[date(year, DEC, 25)] = 'Juledag'
        self[date(year, DEC, 26)] = 'Anden juledag'


class DK(Denmark):
    pass


class UnitedKingdom(HolidayBase):

    def __init__(self, **kwargs):
        self.country = 'UK'
        HolidayBase.__init__(self, **kwargs)

    def _populate(self, year):
        if year >= 1974:
            name = "New Year's Day"
            self[date(year, JAN, 1)] = name
            if self.observed and date(year, JAN, 1).weekday() == SUN:
                self[date(year, JAN, 1) + rd(days=+1)] = name + ' (Observed)'
            elif self.observed and date(year, JAN, 1).weekday() == SAT:
                self[date(year, JAN, 1) + rd(days=+2)] = name + ' (Observed)'
        if self.country in ('UK', 'Scotland'):
            name = 'New Year Holiday'
            if self.country == 'UK':
                name += ' [Scotland]'
            self[date(year, JAN, 2)] = name
            if self.observed and date(year, JAN, 2).weekday() in WEEKEND:
                self[date(year, JAN, 2) + rd(days=+2)] = name + ' (Observed)'
            elif self.observed and date(year, JAN, 2).weekday() == MON:
                self[date(year, JAN, 2) + rd(days=+1)] = name + ' (Observed)'
        if self.country in ('UK', 'Northern Ireland', 'Ireland'):
            name = "St. Patrick's Day"
            if self.country == 'UK':
                name += ' [Northern Ireland]'
            self[date(year, MAR, 17)] = name
            if self.observed and date(year, MAR, 17).weekday() in WEEKEND:
                self[date(year, MAR, 17) + rd(weekday=MO)] = name + ' (Observed)'
        if self.country != 'Ireland':
            self[easter(year) + rd(weekday=FR(-1))] = 'Good Friday'
        if self.country != 'Scotland':
            name = 'Easter Monday'
            if self.country == 'UK':
                name += ' [England, Wales, Northern Ireland]'
            self[easter(year) + rd(weekday=MO)] = name
        if year >= 1978:
            name = 'May Day'
            if year == 2020 and self.country != 'Ireland':
                self[date(year, MAY, 8)] = name
            else:
                if year == 1995:
                    dt = date(year, MAY, 8)
                else:
                    dt = date(year, MAY, 1)
                if dt.weekday() == MON:
                    self[dt] = name
                elif dt.weekday() == TUE:
                    self[dt + rd(days=+6)] = name
                elif dt.weekday() == WED:
                    self[dt + rd(days=+5)] = name
                elif dt.weekday() == THU:
                    self[dt + rd(days=+4)] = name
                elif dt.weekday() == FRI:
                    self[dt + rd(days=+3)] = name
                elif dt.weekday() == SAT:
                    self[dt + rd(days=+2)] = name
                elif dt.weekday() == SUN:
                    self[dt + rd(days=+1)] = name
        if self.country != 'Ireland':
            name = 'Spring Bank Holiday'
            if year == 2012:
                self[date(year, JUN, 4)] = name
            elif year >= 1971:
                self[date(year, MAY, 31) + rd(weekday=MO(-1))] = name
        if self.country == 'Ireland':
            self[date(year, JUN, 1) + rd(weekday=MO)] = 'June Bank Holiday'
        if self.country == 'Isle of Man':
            self[date(year, JUN, 1) + rd(weekday=FR)] = 'TT Bank Holiday'
        if self.country == 'Isle of Man':
            self[date(year, JUL, 5)] = 'Tynwald Day'
        if self.country in ('UK', 'Northern Ireland'):
            name = 'Battle of the Boyne'
            if self.country == 'UK':
                name += ' [Northern Ireland]'
            self[date(year, JUL, 12)] = name
        if self.country in ('UK', 'Scotland', 'Ireland'):
            name = 'Summer Bank Holiday'
            if self.country == 'UK':
                name += ' [Scotland]'
            self[date(year, AUG, 1) + rd(weekday=MO)] = name
        if self.country not in ('Scotland', 'Ireland') and year >= 1971:
            name = 'Late Summer Bank Holiday'
            if self.country == 'UK':
                name += ' [England, Wales, Northern Ireland]'
            self[date(year, AUG, 31) + rd(weekday=MO(-1))] = name
        if self.country == 'Ireland':
            name = 'October Bank Holiday'
            self[date(year, OCT, 31) + rd(weekday=MO(-1))] = name
        if self.country in ('UK', 'Scotland'):
            name = "St. Andrew's Day"
            if self.country == 'UK':
                name += ' [Scotland]'
            self[date(year, NOV, 30)] = name
        name = 'Christmas Day'
        self[date(year, DEC, 25)] = name
        if self.observed and date(year, DEC, 25).weekday() == SAT:
            self[date(year, DEC, 27)] = name + ' (Observed)'
        elif self.observed and date(year, DEC, 25).weekday() == SUN:
            self[date(year, DEC, 27)] = name + ' (Observed)'
        name = 'Boxing Day'
        self[date(year, DEC, 26)] = name
        if self.observed and date(year, DEC, 26).weekday() == SAT:
            self[date(year, DEC, 28)] = name + ' (Observed)'
        elif self.observed and date(year, DEC, 26).weekday() == SUN:
            self[date(year, DEC, 28)] = name + ' (Observed)'
        if self.country != 'Ireland':
            if year == 1977:
                self[date(year, JUN, 7)] = 'Silver Jubilee of Elizabeth II'
            elif year == 1981:
                self[date(year, JUL, 29)] = 'Wedding of Charles and Diana'
            elif year == 1999:
                self[date(year, DEC, 31)] = 'Millennium Celebrations'
            elif year == 2002:
                self[date(year, JUN, 3)] = 'Golden Jubilee of Elizabeth II'
            elif year == 2011:
                self[date(year, APR, 29)] = 'Wedding of William and Catherine'
            elif year == 2012:
                self[date(year, JUN, 5)] = 'Diamond Jubilee of Elizabeth II'


class UK(UnitedKingdom):
    pass


class GB(UnitedKingdom):
    pass


class England(UnitedKingdom):

    def __init__(self, **kwargs):
        self.country = 'England'
        HolidayBase.__init__(self, **kwargs)


class Wales(UnitedKingdom):

    def __init__(self, **kwargs):
        self.country = 'Wales'
        HolidayBase.__init__(self, **kwargs)


class Scotland(UnitedKingdom):

    def __init__(self, **kwargs):
        self.country = 'Scotland'
        HolidayBase.__init__(self, **kwargs)


class IsleOfMan(UnitedKingdom):

    def __init__(self, **kwargs):
        self.country = 'Isle of Man'
        HolidayBase.__init__(self, **kwargs)


class NorthernIreland(UnitedKingdom):

    def __init__(self, **kwargs):
        self.country = 'Northern Ireland'
        HolidayBase.__init__(self, **kwargs)


class Ireland(UnitedKingdom):

    def __init__(self, **kwargs):
        self.country = 'Ireland'
        HolidayBase.__init__(self, **kwargs)


class IE(Ireland):
    pass


class Spain(HolidayBase):
    PROVINCES = [
     'AND', 'ARG', 'AST', 'CAN', 'CAM', 'CAL', 'CAT', 'CVA',
     'EXT', 'GAL', 'IBA', 'ICA', 'MAD', 'MUR', 'NAV', 'PVA', 'RIO']

    def __init__(self, **kwargs):
        self.country = 'ES'
        self.prov = kwargs.pop('prov', kwargs.pop('state', ''))
        HolidayBase.__init__(self, **kwargs)

    def _populate(self, year):
        self[date(year, JAN, 1)] = 'Año nuevo'
        self[date(year, JAN, 6)] = 'Epifanía del Señor'
        if self.prov and self.prov in ('CVA', 'MUR', 'MAD', 'NAV', 'PVA'):
            self[date(year, MAR, 19)] = 'San José'
        if self.prov and self.prov != 'CAT':
            self[easter(year) + rd(weeks=-1, weekday=TH)] = 'Jueves Santo'
        self[easter(year) + rd(weeks=-1, weekday=FR)] = 'Viernes Santo'
        if self.prov and self.prov in ('CAT', 'PVA', 'NAV', 'CVA', 'IBA'):
            self[easter(year) + rd(weekday=MO)] = 'Lunes de Pascua'
        self[date(year, MAY, 1)] = 'Día del Trabajador'
        if self.prov and self.prov in ('CAT', 'GAL'):
            self[date(year, JUN, 24)] = 'San Juan'
        self[date(year, AUG, 15)] = 'Asunción de la Virgen'
        self[date(year, OCT, 12)] = 'Día de la Hispanidad'
        self[date(year, NOV, 1)] = 'Todos los Santos'
        self[date(year, DEC, 6)] = 'Día de la constitución Española'
        self[date(year, DEC, 8)] = 'La Inmaculada Concepción'
        self[date(year, DEC, 25)] = 'Navidad'
        if self.prov and self.prov in ('CAT', 'IBA'):
            self[date(year, DEC, 26)] = 'San Esteban'
        if self.prov:
            if self.prov == 'AND':
                self[date(year, FEB, 28)] = 'Día de Andalucia'
            elif self.prov == 'ARG':
                self[date(year, APR, 23)] = 'Día de San Jorge'
            elif self.prov == 'AST':
                self[date(year, MAR, 8)] = 'Día de Asturias'
            elif self.prov == 'CAN':
                self[date(year, FEB, 28)] = 'Día de la Montaña'
            elif self.prov == 'CAM':
                self[date(year, FEB, 28)] = 'Día de Castilla - La Mancha'
            elif self.prov == 'CAL':
                self[date(year, APR, 23)] = 'Día de Castilla y Leon'
            elif self.prov == 'CAT':
                self[date(year, SEP, 11)] = 'Día Nacional de Catalunya'
            elif self.prov == 'CVA':
                self[date(year, OCT, 9)] = 'Día de la Comunidad Valenciana'
            elif self.prov == 'EXT':
                self[date(year, SEP, 8)] = 'Día de Extremadura'
            elif self.prov == 'GAL':
                self[date(year, JUL, 25)] = 'Día Nacional de Galicia'
            elif self.prov == 'IBA':
                self[date(year, MAR, 1)] = 'Día de las Islas Baleares'
            elif self.prov == 'ICA':
                self[date(year, MAY, 30)] = 'Día de Canarias'
            elif self.prov == 'MAD':
                self[date(year, MAY, 2)] = 'Día de Comunidad De Madrid'
            elif self.prov == 'MUR':
                self[date(year, JUN, 9)] = 'Día de la Región de Murcia'
            elif self.prov == 'NAV':
                self[date(year, SEP, 27)] = 'Día de Navarra'
            elif self.prov == 'PVA':
                self[date(year, OCT, 25)] = 'Día del Páis Vasco'
            elif self.prov == 'RIO':
                self[date(year, JUN, 9)] = 'Día de La Rioja'


class ES(Spain):
    pass


class EuropeanCentralBank(HolidayBase):

    def __init__(self, **kwargs):
        self.country = 'EU'
        HolidayBase.__init__(self, **kwargs)

    def _populate(self, year):
        self[date(year, JAN, 1)] = "New Year's Day"
        e = easter(year)
        self[e - rd(days=2)] = 'Good Friday'
        self[e + rd(days=1)] = 'Easter Monday'
        self[date(year, MAY, 1)] = '1 May (Labour Day)'
        self[date(year, DEC, 25)] = 'Christmas Day'
        self[date(year, DEC, 26)] = '26 December'


class ECB(EuropeanCentralBank):
    pass


class TAR(EuropeanCentralBank):
    pass


class Czechia(HolidayBase):

    def __init__(self, **kwargs):
        self.country = 'CZ'
        HolidayBase.__init__(self, **kwargs)

    def _populate(self, year):
        self[date(year, JAN, 1)] = 'Den obnovy samostatného českého státu' if year >= 2000 else 'Nový rok'
        e = easter(year)
        if year <= 1951 or year >= 2016:
            self[e - rd(days=2)] = 'Velký pátek'
        self[e + rd(days=1)] = 'Velikonoční pondělí'
        if year >= 1951:
            self[date(year, MAY, 1)] = 'Svátek práce'
        if year >= 1992:
            self[date(year, MAY, 8)] = 'Den vítězství'
        elif year >= 1947:
            self[date(year, MAY, 9)] = 'Den vítězství nad hitlerovským fašismem'
        if year >= 1951:
            self[date(year, JUL, 5)] = 'Den slovanských věrozvěstů Cyrila a Metoděje'
            self[date(year, JUL, 6)] = 'Den upálení mistra Jana Husa'
        if year >= 2000:
            self[date(year, SEP, 28)] = 'Den české státnosti'
        if year >= 1951:
            self[date(year, OCT, 28)] = 'Den vzniku samostatného československého státu'
        if year >= 1990:
            self[date(year, NOV, 17)] = 'Den boje za svobodu a demokracii'
        if year >= 1990:
            self[date(year, DEC, 24)] = 'Štědrý den'
        if year >= 1951:
            self[date(year, DEC, 25)] = '1. svátek vánoční'
            self[date(year, DEC, 26)] = '2. svátek vánoční'


class CZ(Czechia):
    pass


class Czech(Czechia):

    def __init__(self, **kwargs):
        warnings.warn('Czech is deprecated, use Czechia instead.', DeprecationWarning)
        super(Czech, self).__init__(**kwargs)


class Slovakia(HolidayBase):

    def __init__(self, **kwargs):
        self.country = 'SK'
        HolidayBase.__init__(self, **kwargs)

    def _populate(self, year):
        self[date(year, JAN, 1)] = 'Deň vzniku Slovenskej republiky'
        self[date(year, JAN, 6)] = 'Zjavenie Pána (Traja králi a vianočnýsviatok pravoslávnych kresťanov)'
        e = easter(year)
        self[e - rd(days=2)] = 'Veľký piatok'
        self[e + rd(days=1)] = 'Veľkonočný pondelok'
        self[date(year, MAY, 1)] = 'Sviatok práce'
        if year >= 1997:
            self[date(year, MAY, 8)] = 'Deň víťazstva nad fašizmom'
        self[date(year, JUL, 5)] = 'Sviatok svätého Cyrila a svätého Metoda'
        self[date(year, AUG, 29)] = 'Výročie Slovenského národného povstania'
        self[date(year, SEP, 1)] = 'Deň Ústavy Slovenskej republiky'
        self[date(year, SEP, 15)] = 'Sedembolestná Panna Mária'
        if year == 2018:
            self[date(year, OCT, 30)] = '100. výročie prijatia Deklarácie slovenského národa'
        self[date(year, NOV, 1)] = 'Sviatok Všetkých svätých'
        if year >= 2001:
            self[date(year, NOV, 17)] = 'Deň boja za slobodu a demokraciu'
        self[date(year, DEC, 24)] = 'Štedrý deň'
        self[date(year, DEC, 25)] = 'Prvý sviatok vianočný'
        self[date(year, DEC, 26)] = 'Druhý sviatok vianočný'


class SK(Slovakia):
    pass


class Slovak(Slovakia):

    def __init__(self, **kwargs):
        warnings.warn('Slovak is deprecated, use Slovakia instead.', DeprecationWarning)
        super(Slovak, self).__init__(**kwargs)


class Poland(HolidayBase):

    def __init__(self, **kwargs):
        self.country = 'PL'
        HolidayBase.__init__(self, **kwargs)

    def _populate(self, year):
        self[date(year, JAN, 1)] = 'Nowy Rok'
        if year >= 2011:
            self[date(year, JAN, 6)] = 'Święto Trzech Króli'
        e = easter(year)
        self[e] = 'Niedziela Wielkanocna'
        self[e + rd(days=1)] = 'Poniedziałek Wielkanocny'
        if year >= 1950:
            self[date(year, MAY, 1)] = 'Święto Państwowe'
        if year >= 1919:
            self[date(year, MAY, 3)] = 'Święto Narodowe Trzeciego Maja'
        self[e + rd(days=49)] = 'Zielone Świątki'
        self[e + rd(days=60)] = 'Dzień Bożego Ciała'
        self[date(year, AUG, 15)] = 'Wniebowzięcie Najświętszej Marii Panny'
        self[date(year, NOV, 1)] = 'Uroczystość Wszystkich świętych'
        if 1937 <= year <= 1945 or year >= 1989:
            self[date(year, NOV, 11)] = 'Narodowe Święto Niepodległości'
        self[date(year, DEC, 25)] = 'Boże Narodzenie (pierwszy dzień)'
        self[date(year, DEC, 26)] = 'Boże Narodzenie (drugi dzień)'


class Polish(Poland):

    def __init__(self, **kwargs):
        warnings.warn('Polish is deprecated, use Poland instead.', DeprecationWarning)
        super(Polish, self).__init__(**kwargs)


class PL(Poland):
    pass


class Portugal(HolidayBase):

    def __init__(self, **kwargs):
        self.country = 'PT'
        HolidayBase.__init__(self, **kwargs)

    def _populate(self, year):
        self[date(year, JAN, 1)] = 'Ano Novo'
        e = easter(year)
        self[e - rd(days=2)] = 'Sexta-feira Santa'
        self[e] = 'Páscoa'
        if year < 2013 or year > 2015:
            self[e + rd(days=60)] = 'Corpo de Deus'
            self[date(year, OCT, 5)] = 'Implantação da República'
            self[date(year, NOV, 1)] = 'Dia de Todos os Santos'
            self[date(year, DEC, 1)] = 'Restauração da Independência'
        self[date(year, 4, 25)] = 'Dia da Liberdade'
        self[date(year, 5, 1)] = 'Dia do Trabalhador'
        self[date(year, 6, 10)] = 'Dia de Portugal'
        self[date(year, 8, 15)] = 'Assunção de Nossa Senhora'
        self[date(year, DEC, 8)] = 'Imaculada Conceição'
        self[date(year, DEC, 25)] = 'Christmas Day'


class PT(Portugal):
    pass


class PortugalExt(Portugal):
    """
    Adds extended days that most people have as a bonus from their companies:
    - Carnival
    - the day before and after xmas
    - the day before the new year
    - Lisbon's city holiday
    """

    def _populate(self, year):
        super(PortugalExt, self)._populate(year)
        e = easter(year)
        self[e - rd(days=47)] = 'Carnaval'
        self[date(year, DEC, 24)] = 'Vespera de Natal'
        self[date(year, DEC, 26)] = '26 de Dezembro'
        self[date(year, DEC, 31)] = 'Vespera de Ano novo'
        self[date(year, 6, 13)] = 'Dia de Santo António'


class PTE(PortugalExt):
    pass


class Netherlands(HolidayBase):
    SUN = 6

    def __init__(self, **kwargs):
        self.country = 'NL'
        HolidayBase.__init__(self, **kwargs)

    def _populate(self, year):
        self[date(year, JAN, 1)] = 'Nieuwjaarsdag'
        easter_date = easter(year)
        self[easter_date] = 'Eerste paasdag'
        self[easter_date + rd(days=1)] = 'Tweede paasdag'
        self[easter_date + rd(days=39)] = 'Hemelvaart'
        self[easter_date + rd(days=49)] = 'Eerste Pinksterdag'
        self[easter_date + rd(days=50)] = 'Tweede Pinksterdag'
        self[date(year, DEC, 25)] = 'Eerste Kerstdag'
        self[date(year, DEC, 26)] = 'Tweede Kerstdag'
        if year >= 1945 and year % 5 == 0:
            self[date(year, MAY, 5)] = 'Bevrijdingsdag'
        if year >= 2014:
            kings_day = date(year, APR, 27)
            if kings_day.weekday() == self.SUN:
                kings_day = kings_day - rd(days=1)
            self[kings_day] = 'Koningsdag'
        if 1891 <= year <= 2013:
            queens_day = date(year, APR, 30)
            if year <= 1948:
                queens_day = date(year, AUG, 31)
            if queens_day.weekday() == self.SUN:
                if year < 1980:
                    queens_day = queens_day + rd(days=1)
                else:
                    queens_day = queens_day - rd(days=1)
            self[queens_day] = 'Koninginnedag'


class NL(Netherlands):
    pass


class Norway(HolidayBase):
    """
    Norwegian holidays.
    Note that holidays falling on a sunday is "lost",
    it will not be moved to another day to make up for the collision.

    In Norway, ALL sundays are considered a holiday (https://snl.no/helligdag).
    Initialize this class with include_sundays=False
    to not include sundays as a holiday.

    Primary sources:
    https://lovdata.no/dokument/NL/lov/1947-04-26-1
    https://no.wikipedia.org/wiki/Helligdager_i_Norge
    https://www.timeanddate.no/merkedag/norge/
    """

    def __init__(self, include_sundays=True, **kwargs):
        """

        :param include_sundays: Whether to consider sundays as a holiday
        (which they are in Norway)
        :param kwargs:
        """
        self.country = 'NO'
        self.include_sundays = include_sundays
        HolidayBase.__init__(self, **kwargs)

    def _populate(self, year):
        if self.include_sundays:
            first_day_of_year = date(year, JAN, 1)
            first_sunday_of_year = first_day_of_year + rd(days=SUN - first_day_of_year.weekday())
            cur_date = first_sunday_of_year
            while cur_date < date(year + 1, 1, 1):
                assert cur_date.weekday() == SUN
                self[cur_date] = 'Søndag'
                cur_date += rd(days=7)

        self[date(year, JAN, 1)] = 'Første nyttårsdag'
        if year >= 1947:
            self[date(year, MAY, 1)] = 'Arbeidernes dag'
            self[date(year, MAY, 17)] = 'Grunnlovsdag'
        self[date(year, DEC, 25)] = 'Første juledag'
        self[date(year, DEC, 26)] = 'Andre juledag'
        e = easter(year)
        maundy_thursday = e - rd(days=3)
        good_friday = e - rd(days=2)
        resurrection_sunday = e
        easter_monday = e + rd(days=1)
        ascension_thursday = e + rd(days=39)
        pentecost = e + rd(days=49)
        pentecost_day_two = e + rd(days=50)
        assert maundy_thursday.weekday() == THU
        assert good_friday.weekday() == FRI
        assert resurrection_sunday.weekday() == SUN
        assert easter_monday.weekday() == MON
        assert ascension_thursday.weekday() == THU
        assert pentecost.weekday() == SUN
        assert pentecost_day_two.weekday() == MON
        self[maundy_thursday] = 'Skjærtorsdag'
        self[good_friday] = 'Langfredag'
        self[resurrection_sunday] = 'Første påskedag'
        self[easter_monday] = 'Andre påskedag'
        self[ascension_thursday] = 'Kristi himmelfartsdag'
        self[pentecost] = 'Første pinsedag'
        self[pentecost_day_two] = 'Andre pinsedag'


class NO(Norway):
    pass


class Italy(HolidayBase):
    PROVINCES = [
     'AN', 'AO', 'BA', 'BL', 'BO',
     'BZ', 'BS', 'CB', 'CT', 'Cesena',
     'CH', 'CS', 'KR', 'EN', 'FE', 'FI',
     'FC', 'Forli', 'FR', 'GE', 'GO', 'IS',
     'SP', 'LT', 'MN', 'MS', 'MI',
     'MO', 'MB', 'NA', 'PD', 'PA',
     'PR', 'PG', 'PE', 'PC', 'PI',
     'PD', 'PT', 'RA', 'RE',
     'RI', 'RN', 'RM', 'RO', 'SA',
     'SR', 'TE', 'TO', 'TS', 'Pesaro', 'PU',
     'Urbino', 'VE', 'VC', 'VI']

    def __init__(self, **kwargs):
        self.country = 'IT'
        self.prov = kwargs.pop('prov', kwargs.pop('state', ''))
        HolidayBase.__init__(self, **kwargs)

    def _populate(self, year):
        self[date(year, JAN, 1)] = 'Capodanno'
        self[date(year, JAN, 6)] = 'Epifania del Signore'
        self[easter(year)] = 'Pasqua di Resurrezione'
        self[easter(year) + rd(weekday=MO)] = "Lunedì dell'Angelo"
        if year >= 1946:
            self[date(year, APR, 25)] = 'Festa della Liberazione'
        self[date(year, MAY, 1)] = 'Festa dei Lavoratori'
        if year >= 1948:
            self[date(year, JUN, 2)] = 'Festa della Repubblica'
        self[date(year, AUG, 15)] = 'Assunzione della Vergine'
        self[date(year, NOV, 1)] = 'Tutti i Santi'
        self[date(year, DEC, 8)] = 'Immacolata Concezione'
        self[date(year, DEC, 25)] = 'Natale'
        self[date(year, DEC, 26)] = 'Santo Stefano'
        if self.prov:
            if self.prov == 'AN':
                self[date(year, MAY, 4)] = 'San Ciriaco'
            elif self.prov == 'AO':
                self[date(year, SEP, 7)] = 'San Grato'
            elif self.prov in 'BA':
                self[date(year, DEC, 6)] = 'San Nicola'
            elif self.prov == 'BL':
                self[date(year, NOV, 11)] = 'San Martino'
            elif self.prov in 'BO':
                self[date(year, OCT, 4)] = 'San Petronio'
            elif self.prov == 'BZ':
                self[date(year, AUG, 15)] = 'Maria Santissima Assunta'
            elif self.prov == 'BS':
                self[date(year, FEB, 15)] = 'Santi Faustino e Giovita'
            elif self.prov == 'CB':
                self[date(year, APR, 23)] = 'San Giorgio'
            elif self.prov == 'CT':
                self[date(year, FEB, 5)] = "Sant'Agata"
            elif self.prov in ('FC', 'Cesena'):
                self[date(year, JUN, 24)] = 'San Giovanni Battista'
            if self.prov in ('FC', 'Forlì'):
                self[date(year, FEB, 4)] = 'Madonna del Fuoco'
            elif self.prov == 'CH':
                self[date(year, MAY, 11)] = 'San Giustino di Chieti'
            elif self.prov == 'CS':
                self[date(year, FEB, 12)] = 'Madonna del Pilerio'
            elif self.prov == 'KR':
                self[date(year, OCT, 9)] = 'San Dionigi'
            elif self.prov == 'EN':
                self[date(year, JUL, 2)] = 'Madonna della Visitazione'
            elif self.prov == 'FE':
                self[date(year, APR, 23)] = 'San Giorgio'
            elif self.prov == 'FI':
                self[date(year, JUN, 24)] = 'San Giovanni Battista'
            elif self.prov == 'FR':
                self[date(year, JUN, 20)] = 'San Silverio'
            elif self.prov == 'GE':
                self[date(year, JUN, 24)] = 'San Giovanni Battista'
            elif self.prov == 'GO':
                self[date(year, MAR, 16)] = 'Santi Ilario e Taziano'
            elif self.prov == 'IS':
                self[date(year, MAY, 19)] = 'San Pietro Celestino'
            elif self.prov == 'SP':
                self[date(year, MAR, 19)] = 'San Giuseppe'
            elif self.prov == 'LT':
                self[date(year, APR, 25)] = 'San Marco evangelista'
            elif self.prov == 'ME':
                self[date(year, JUN, 3)] = 'Madonna della Lettera'
            elif self.prov == 'MI':
                self[date(year, DEC, 7)] = "Sant'Ambrogio"
            elif self.prov == 'MN':
                self[date(year, MAR, 18)] = "Sant'Anselmo da Baggio"
            elif self.prov == 'MS':
                self[date(year, OCT, 4)] = "San Francesco d'Assisi"
            elif self.prov == 'MO':
                self[date(year, JAN, 31)] = 'San Geminiano'
            elif self.prov == 'MB':
                self[date(year, JUN, 24)] = 'San Giovanni Battista'
            elif self.prov == 'NA':
                self[date(year, SEP, 19)] = 'San Gennaro'
            elif self.prov == 'PD':
                self[date(year, JUN, 13)] = "Sant'Antonio di Padova"
            elif self.prov == 'PA':
                self[date(year, JUL, 15)] = 'San Giovanni'
            elif self.prov == 'PR':
                self[date(year, JAN, 13)] = "Sant'Ilario di Poitiers"
            elif self.prov == 'PG':
                self[date(year, JAN, 29)] = "Sant'Ercolano e San Lorenzo"
            elif self.prov == 'PC':
                self[date(year, JUL, 4)] = "Sant'Antonino di Piacenza"
            elif self.prov == 'RM':
                self[date(year, JUN, 29)] = 'Santi Pietro e Paolo'
            elif self.prov == 'TO':
                self[date(year, JUN, 24)] = 'San Giovanni Battista'
            elif self.prov == 'TS':
                self[date(year, NOV, 3)] = 'San Giusto'
            elif self.prov == 'VI':
                self[date(year, APR, 25)] = 'San Marco'


class IT(Italy):
    pass


class Sweden(HolidayBase):
    """
    Swedish holidays.
    Note that holidays falling on a sunday are "lost",
    it will not be moved to another day to make up for the collision.
    In Sweden, ALL sundays are considered a holiday
    (https://sv.wikipedia.org/wiki/Helgdagar_i_Sverige).
    Initialize this class with include_sundays=False
    to not include sundays as a holiday.
    Primary sources:
    https://sv.wikipedia.org/wiki/Helgdagar_i_Sverige and
    http://www.riksdagen.se/sv/dokument-lagar/dokument/svensk-forfattningssamling/lag-1989253-om-allmanna-helgdagar_sfs-1989-253
    """

    def __init__(self, include_sundays=True, **kwargs):
        """
        :param include_sundays: Whether to consider sundays as a holiday
        (which they are in Sweden)
        :param kwargs:
        """
        self.country = 'SE'
        self.include_sundays = include_sundays
        HolidayBase.__init__(self, **kwargs)

    def _populate(self, year):
        if self.include_sundays:
            first_day_of_year = date(year, JAN, 1)
            first_sunday_of_year = first_day_of_year + rd(days=SUN - first_day_of_year.weekday())
            cur_date = first_sunday_of_year
            while cur_date < date(year + 1, 1, 1):
                assert cur_date.weekday() == SUN
                self[cur_date] = 'Söndag'
                cur_date += rd(days=7)

        self[date(year, JAN, 1)] = 'Nyårsdagen'
        self[date(year, JAN, 6)] = 'Trettondedag jul'
        if year >= 1939:
            self[date(year, MAY, 1)] = 'Första maj'
        if year >= 2005:
            self[date(year, JUN, 6)] = 'Sveriges nationaldag'
        self[date(year, DEC, 24)] = 'Julafton'
        self[date(year, DEC, 25)] = 'Juldagen'
        self[date(year, DEC, 26)] = 'Annandag jul'
        self[date(year, DEC, 31)] = 'Nyårsafton'
        e = easter(year)
        maundy_thursday = e - rd(days=3)
        good_friday = e - rd(days=2)
        easter_saturday = e - rd(days=1)
        resurrection_sunday = e
        easter_monday = e + rd(days=1)
        ascension_thursday = e + rd(days=39)
        pentecost = e + rd(days=49)
        pentecost_day_two = e + rd(days=50)
        assert maundy_thursday.weekday() == THU
        assert good_friday.weekday() == FRI
        assert easter_saturday.weekday() == SAT
        assert resurrection_sunday.weekday() == SUN
        assert easter_monday.weekday() == MON
        assert ascension_thursday.weekday() == THU
        assert pentecost.weekday() == SUN
        assert pentecost_day_two.weekday() == MON
        self[good_friday] = 'Långfredagen'
        self[resurrection_sunday] = 'Påskdagen'
        self[easter_monday] = 'Annandag påsk'
        self[ascension_thursday] = 'Kristi himmelsfärdsdag'
        self[pentecost] = 'Pingstdagen'
        if year <= 2004:
            self[pentecost_day_two] = 'Annandag pingst'
        self[date(year, JUN, 19) + rd(weekday=FR)] = 'Midsommarafton'
        if year >= 1953:
            self[date(year, JUN, 20) + rd(weekday=SA)] = 'Midsommardagen'
        else:
            self[date(year, JUN, 24)] = 'Midsommardagen'
        self[date(year, OCT, 31) + rd(weekday=SA)] = 'Alla helgons dag'
        if year <= 1953:
            self[date(year, MAR, 25)] = 'Jungfru Marie bebådelsedag'


class SE(Sweden):
    pass


class Japan(HolidayBase):

    def __init__(self, **kwargs):
        self.country = 'JP'
        HolidayBase.__init__(self, **kwargs)

    def _populate(self, year):
        if year < 1949 or year > 2099:
            raise NotImplementedError
        self[date(year, JAN, 1)] = '元日'
        if year <= 1999:
            self[date(year, JAN, 15)] = '成人の日'
        else:
            self[date(year, JAN, 1) + rd(weekday=MO(+2))] = '成人の日'
        self[date(year, FEB, 11)] = '建国記念の日'
        if year >= 2020:
            self[date(year, FEB, 23)] = '天皇誕生日'
        self[self._vernal_equinox_day(year)] = '春分の日'
        if year <= 1988:
            self[date(year, APR, 29)] = '天皇誕生日'
        elif year <= 2006:
            self[date(year, APR, 29)] = 'みどりの日'
        else:
            self[date(year, APR, 29)] = '昭和の日'
        self[date(year, MAY, 3)] = '憲法記念日'
        if year >= 2007:
            self[date(year, MAY, 4)] = 'みどりの日'
        self[date(year, MAY, 5)] = 'こどもの日'
        if 1996 <= year <= 2002:
            self[date(year, JUL, 20)] = '海の日'
        elif year >= 2003:
            self[date(year, JUL, 1) + rd(weekday=MO(+3))] = '海の日'
        if year >= 2016:
            self[date(year, AUG, 11)] = '山の日'
        if 1966 <= year <= 2002:
            self[date(year, SEP, 15)] = '敬老の日'
        elif year >= 2003:
            self[date(year, SEP, 1) + rd(weekday=MO(+3))] = '敬老の日'
        self[self._autumnal_equinox_day(year)] = '秋分の日'
        if 1966 <= year <= 1999:
            self[date(year, OCT, 10)] = '体育の日'
        elif year >= 2000:
            self[date(year, OCT, 1) + rd(weekday=MO(+2))] = '体育の日'
        self[date(year, NOV, 3)] = '文化の日'
        self[date(year, NOV, 23)] = '勤労感謝の日'
        if 1989 <= year <= 2018:
            self[date(year, DEC, 23)] = '天皇誕生日'
        if year == 2019:
            self[date(year, MAY, 1)] = '天皇の即位の日'
            self[date(year, OCT, 22)] = '即位礼正殿の儀が行われる日'
        self._add_national_holidays(year)
        self._add_substitute_holidays(year)

    def _vernal_equinox_day(self, year):
        day = 20
        if year % 4 == 0:
            if year <= 1956:
                day = 21
            elif year >= 2092:
                day = 19
        elif year % 4 == 1:
            if year <= 1989:
                day = 21
        elif year % 4 == 2:
            if year <= 2022:
                day = 21
        elif year % 4 == 3:
            if year <= 2055:
                day = 21
        return date(year, MAR, day)

    def _autumnal_equinox_day(self, year):
        day = 22
        if year % 4 == 0:
            if year <= 2008:
                day = 23
        elif year % 4 == 1:
            if year <= 2041:
                day = 23
        elif year % 4 == 2:
            if year <= 2074:
                day = 23
        elif year % 4 == 3:
            if year <= 1979:
                day = 24
            else:
                day = 23
        return date(year, SEP, day)

    def _add_national_holidays(self, year):
        if year in (1993, 1999, 2004, 1988, 1994, 2005, 1989, 1995, 2000, 2006, 1990,
                    2001, 1991, 1996, 2002):
            self[date(year, MAY, 4)] = '国民の休日'
        if year in (2032, 2049, 2060, 2077, 2088, 2094):
            self[date(year, SEP, 21)] = '国民の休日'
        if year in (2009, 2015, 2026, 2037, 2043, 2054, 2065, 2071, 2099):
            self[date(year, SEP, 22)] = '国民の休日'
        if year == 2019:
            self[date(year, APR, 30)] = '国民の休日'
            self[date(year, MAY, 2)] = '国民の休日'

    def _add_substitute_holidays(self, year):
        table = (
         (
          1, 2,
          (1978, 1984, 1989, 1995, 2006, 2012, 2017, 2023, 2034, 2040, 2045)),
         (
          1, 16, (1978, 1984, 1989, 1995)),
         (
          2, 12,
          (1979, 1990, 1996, 2001, 2007, 2018, 2024, 2029, 2035, 2046)),
         (
          2, 24, (2020, )),
         (
          3, 21, (1988, 2005, 2016, 2033, 2044, 2050)),
         (
          3, 22, (1982, 1999, 2010, 2027)),
         (
          4, 30,
          (1973, 1979, 1984, 1990, 2001, 2007, 2012, 2018, 2029, 2035, 2040, 2046)),
         (
          5, 4, (1981, 1987, 1992, 1998)),
         (
          5, 6,
          (1985, 1991, 1996, 2002, 2013, 2019, 2024, 2030, 2041, 2047, 2008, 2014, 2025, 2031,
 2036, 2042, 2009, 2015, 2020, 2026, 2037, 2043, 2048)),
         (
          7, 21, (1997, )),
         (
          8, 12, (2019, 2024, 2030, 2041, 2047)),
         (
          9, 16, (1974, 1985, 1991, 1996, 2002)),
         (
          9, 23, (2024, )),
         (
          9, 24, (1973, 1984, 1990, 2001, 2007, 2018, 2029, 2035, 2046)),
         (
          10, 11, (1976, 1982, 1993, 1999)),
         (
          11, 4,
          (1974, 1985, 1991, 1996, 2002, 2013, 2019, 2024, 2030, 2041, 2047)),
         (
          11, 24,
          (1975, 1980, 1986, 1997, 2003, 2008, 2014, 2025, 2031, 2036, 2042)),
         (
          12, 24, (1990, 2001, 2007, 2012, 2018)))
        for holiday in table:
            month = holiday[0]
            day = holiday[1]
            years = holiday[2]
            if year in years:
                self[date(year, month, day)] = '振替休日'


class JP(Japan):
    pass


class France(HolidayBase):
    """Official French holidays.

    Some provinces have specific holidays, only those are included in the
    PROVINCES, because these provinces have different administrative status,
    which makes it difficult to enumerate.

    For religious holidays usually happening on Sundays (Easter, Pentecost),
    only the following Monday is considered a holiday.

    Primary sources:
        https://fr.wikipedia.org/wiki/Fêtes_et_jours_fériés_en_France
        https://www.service-public.fr/particuliers/vosdroits/F2405
    """
    PROVINCES = [
     'Métropole', 'Alsace-Moselle', 'Guadeloupe', 'Guyane',
     'Martinique', 'Mayotte', 'Nouvelle-Calédonie', 'La Réunion',
     'Polynésie Française', 'Saint-Barthélémy', 'Saint-Martin',
     'Wallis-et-Futuna']

    def __init__(self, **kwargs):
        self.country = 'FR'
        self.prov = kwargs.pop('prov', 'Métropole')
        HolidayBase.__init__(self, **kwargs)

    def _populate(self, year):
        if year > 1810:
            self[date(year, JAN, 1)] = "Jour de l'an"
        if year > 1919:
            name = 'Fête du Travail'
            if year <= 1948:
                name += ' et de la Concorde sociale'
            self[date(year, MAY, 1)] = name
        if 1953 <= year <= 1959 or year > 1981:
            self[date(year, MAY, 8)] = 'Armistice 1945'
        if year >= 1880:
            self[date(year, JUL, 14)] = 'Fête nationale'
        if year >= 1918:
            self[date(year, NOV, 11)] = 'Armistice 1918'
        if self.prov in ('Alsace-Moselle', 'Guadeloupe', 'Guyane', 'Martinique', 'Polynésie Française'):
            self[easter(year) - rd(days=2)] = 'Vendredi saint'
        if self.prov == 'Alsace-Moselle':
            self[date(year, DEC, 26)] = 'Deuxième jour de Noël'
        if year >= 1886:
            self[easter(year) + rd(days=1)] = 'Lundi de Pâques'
            self[easter(year) + rd(days=50)] = 'Lundi de Pentecôte'
        if year >= 1802:
            self[easter(year) + rd(days=39)] = 'Ascension'
            self[date(year, AUG, 15)] = 'Assomption'
            self[date(year, NOV, 1)] = 'Toussaint'
            name = 'Noël'
            if self.prov == 'Alsace-Moselle':
                name = 'Premier jour de ' + name
            self[date(year, DEC, 25)] = name
        if self.prov == 'Mayotte':
            self[date(year, APR, 27)] = "Abolition de l'esclavage"
        if self.prov == 'Wallis-et-Futuna':
            self[date(year, APR, 28)] = 'Saint Pierre Chanel'
        if self.prov == 'Martinique':
            self[date(year, MAY, 22)] = "Abolition de l'esclavage"
        if self.prov in ('Guadeloupe', 'Saint-Martin'):
            self[date(year, MAY, 27)] = "Abolition de l'esclavage"
        if self.prov == 'Guyane':
            self[date(year, JUN, 10)] = "Abolition de l'esclavage"
        if self.prov == 'Polynésie Française':
            self[date(year, JUN, 29)] = "Fête de l'autonomie"
        if self.prov in ('Guadeloupe', 'Martinique'):
            self[date(year, JUL, 21)] = 'Fête Victor Schoelcher'
        if self.prov == 'Wallis-et-Futuna':
            self[date(year, JUL, 29)] = 'Fête du Territoire'
        if self.prov == 'Nouvelle-Calédonie':
            self[date(year, SEP, 24)] = 'Fête de la Citoyenneté'
        if self.prov == 'Saint-Barthélémy':
            self[date(year, OCT, 9)] = "Abolition de l'esclavage"
        if self.prov == 'La Réunion' and year >= 1981:
            self[date(year, DEC, 20)] = "Abolition de l'esclavage"


class FRA(France):
    pass


class Belgium(HolidayBase):
    """
    https://www.belgium.be/nl/over_belgie/land/belgie_in_een_notendop/feestdagen
    https://nl.wikipedia.org/wiki/Feestdagen_in_Belgi%C3%AB
    """

    def __init__(self, **kwargs):
        self.country = 'BE'
        HolidayBase.__init__(self, **kwargs)

    def _populate(self, year):
        self[date(year, JAN, 1)] = 'Nieuwjaarsdag'
        easter_date = easter(year)
        self[easter_date] = 'Pasen'
        self[easter_date + rd(days=1)] = 'Paasmaandag'
        self[easter_date + rd(days=39)] = 'O.L.H. Hemelvaart'
        self[easter_date + rd(days=49)] = 'Pinksteren'
        self[easter_date + rd(days=50)] = 'Pinkstermaandag'
        self[date(year, MAY, 1)] = 'Dag van de Arbeid'
        self[date(year, JUL, 21)] = 'Nationale feestdag'
        self[date(year, AUG, 15)] = 'O.L.V. Hemelvaart'
        self[date(year, NOV, 1)] = 'Allerheiligen'
        self[date(year, NOV, 11)] = 'Wapenstilstand'
        self[date(year, DEC, 25)] = 'Kerstmis'


class BE(Belgium):
    pass


class SouthAfrica(HolidayBase):

    def __init__(self, **kwargs):
        self.country = 'ZA'
        HolidayBase.__init__(self, **kwargs)

    def _populate(self, year):
        if year > 1909:
            self[date(year, 1, 1)] = "New Year's Day"
            e = easter(year)
            good_friday = e - rd(days=2)
            easter_monday = e + rd(days=1)
            self[good_friday] = 'Good Friday'
            if year > 1979:
                self[easter_monday] = 'Family Day'
            else:
                self[easter_monday] = 'Easter Monday'
            if 1909 < year < 1952:
                dec_16_name = "Dingaan's Day"
            elif 1951 < year < 1980:
                dec_16_name = 'Day of the Covenant'
            elif 1979 < year < 1995:
                dec_16_name = 'Day of the Vow'
            else:
                dec_16_name = 'Day of Reconciliation'
            self[date(year, DEC, 16)] = dec_16_name
            self[date(year, DEC, 25)] = 'Christmas Day'
            if year > 1979:
                dec_26_name = 'Day of Goodwill'
            else:
                dec_26_name = 'Boxing Day'
            self[date(year, 12, 26)] = dec_26_name
        if year > 1994:
            self[date(year, MAR, 21)] = 'Human Rights Day'
            self[date(year, APR, 27)] = 'Freedom Day'
            self[date(year, MAY, 1)] = "Workers' Day"
            self[date(year, JUN, 16)] = 'Youth Day'
            self[date(year, AUG, 9)] = "National Women's Day"
            self[date(year, SEP, 24)] = 'Heritage Day'
        national_election = 'National and provincial government elections'
        y2k = 'Y2K changeover'
        local_election = 'Local government elections'
        presidential = 'By presidential decree'
        if year == 1999:
            self[date(1999, JUN, 2)] = national_election
            self[date(1999, DEC, 31)] = y2k
        if year == 2000:
            self[date(2000, JAN, 2)] = y2k
        if year == 2004:
            self[date(2004, APR, 14)] = national_election
        if year == 2006:
            self[date(2006, MAR, 1)] = local_election
        if year == 2008:
            self[date(2008, MAY, 2)] = presidential
        if year == 2009:
            self[date(2009, APR, 22)] = national_election
        if year == 2011:
            self[date(2011, MAY, 18)] = local_election
            self[date(2011, DEC, 27)] = presidential
        if year == 2014:
            self[date(2014, MAY, 7)] = national_election
        if year == 2016:
            self[date(2016, AUG, 3)] = local_election
        if year == 2019:
            self[date(2019, MAY, 8)] = national_election
        for k, v in list(self.items()):
            if self.observed and year > 1994 and k.weekday() == SUN:
                self[k + rd(days=1)] = v + ' (Observed)'

        if 1951 < year < 1974:
            self[date(year, APR, 6)] = "Van Riebeeck's Day"
        elif 1979 < year < 1995:
            self[date(year, APR, 6)] = "Founder's Day"
        if 1986 < year < 1990:
            historic_workers_day = datetime(year, MAY, 1)
            while historic_workers_day.weekday() != FRI:
                historic_workers_day += rd(days=1)

            self[historic_workers_day] = "Workers' Day"
        if 1909 < year < 1994:
            ascension_day = e + rd(days=40)
            self[ascension_day] = 'Ascension Day'
        if 1909 < year < 1952:
            self[date(year, MAY, 24)] = 'Empire Day'
        if 1909 < year < 1961:
            self[date(year, MAY, 31)] = 'Union Day'
        elif 1960 < year < 1994:
            self[date(year, MAY, 31)] = 'Republic Day'
        if 1951 < year < 1961:
            queens_birthday = datetime(year, JUN, 7)
            while queens_birthday.weekday() != 0:
                queens_birthday += rd(days=1)

            self[queens_birthday] = "Queen's Birthday"
        if 1960 < year < 1974:
            self[date(year, JUL, 10)] = 'Family Day'
        if 1909 < year < 1952:
            kings_birthday = datetime(year, AUG, 1)
            while kings_birthday.weekday() != 0:
                kings_birthday += rd(days=1)

            self[kings_birthday] = "King's Birthday"
        if 1951 < year < 1980:
            settlers_day = datetime(year, SEP, 1)
            while settlers_day.weekday() != 0:
                settlers_day += rd(days=1)

            self[settlers_day] = "Settlers' Day"
        if 1951 < year < 1994:
            self[date(year, OCT, 10)] = 'Kruger Day'


class ZA(SouthAfrica):
    pass


class Slovenia(HolidayBase):
    """
    Contains all work-free public holidays in Slovenia.
    No holidays are returned before year 1991 when Slovenia became independent
    country. Before that Slovenia was part of Socialist federal republic of
    Yugoslavia.

    List of holidays (including those that are not work-free:
    https://en.wikipedia.org/wiki/Public_holidays_in_Slovenia
    """

    def __init__(self, **kwargs):
        self.country = 'SI'
        HolidayBase.__init__(self, **kwargs)

    def _populate(self, year):
        if year <= 1990:
            return
        if year > 1991:
            self[date(year, JAN, 1)] = 'novo leto'
            if year < 2013 or year > 2016:
                self[date(year, JAN, 2)] = 'novo leto'
            self[date(year, FEB, 8)] = 'Prešernov dan'
            easter_day = easter(year)
            self[easter_day + rd(days=1)] = 'Velikonočni ponedeljek'
            self[date(year, APR, 27)] = 'dan upora proti okupatorju'
            self[date(year, MAY, 1)] = 'praznik dela'
            self[date(year, MAY, 2)] = 'praznik dela'
            self[date(year, JUN, 25)] = 'dan državnosti'
            self[date(year, AUG, 15)] = 'Marijino vnebovzetje'
            self[date(year, OCT, 31)] = 'dan reformacije'
            self[date(year, NOV, 1)] = 'dan spomina na mrtve'
            self[date(year, DEC, 25)] = 'Božič'
            self[date(year, DEC, 26)] = 'dan samostojnosti in enotnosti'


class SI(Slovenia):
    pass


class Finland(HolidayBase):

    def __init__(self, **kwargs):
        self.country = 'FI'
        HolidayBase.__init__(self, **kwargs)

    def _populate(self, year):
        e = easter(year)
        self[date(year, JAN, 1)] = 'Uudenvuodenpäivä'
        self[date(year, JAN, 6)] = 'Loppiainen'
        self[e - rd(days=2)] = 'Pitkäperjantai'
        self[e] = 'Pääsiäispäivä'
        self[e + rd(days=1)] = '2. pääsiäispäivä'
        self[date(year, MAY, 1)] = 'Vappu'
        self[e + rd(days=39)] = 'Helatorstai'
        self[e + rd(days=49)] = 'Helluntaipäivä'
        self[date(year, JUN, 20) + rd(weekday=SA)] = 'Juhannuspäivä'
        self[date(year, OCT, 31) + rd(weekday=SA)] = 'Pyhäinpäivä'
        self[date(year, DEC, 6)] = 'Itsenäisyyspäivä'
        self[date(year, DEC, 25)] = 'Joulupäivä'
        self[date(year, DEC, 26)] = 'Tapaninpäivä'
        self[date(year, JUN, 19) + rd(weekday=FR)] = 'Juhannusaatto'
        self[date(year, DEC, 24)] = 'Jouluaatto'


class FI(Finland):
    pass


class Switzerland(HolidayBase):
    PROVINCES = [
     'AG', 'AR', 'AI', 'BL', 'BS', 'BE', 'FR', 'GE', 'GL',
     'GR', 'JU', 'LU', 'NE', 'NW', 'OW', 'SG', 'SH', 'SZ',
     'SO', 'TG', 'TI', 'UR', 'VD', 'VS', 'ZG', 'ZH']

    def __init__(self, **kwargs):
        self.country = 'CH'
        HolidayBase.__init__(self, **kwargs)

    def _populate(self, year):
        self[date(year, JAN, 1)] = 'Neujahrestag'
        if self.prov in ('AG', 'BE', 'FR', 'GE', 'GL', 'GR', 'JU', 'LU', 'NE', 'OW',
                         'SH', 'SO', 'TG', 'VD', 'ZG', 'ZH'):
            self[date(year, JAN, 2)] = 'Berchtoldstag'
        if self.prov in ('SZ', 'TI', 'UR'):
            self[date(year, JAN, 6)] = 'Heilige Drei Könige'
        if self.prov == 'NE':
            self[date(year, MAR, 1)] = 'Jahrestag der Ausrufung der Republik'
        if self.prov in ('NW', 'SZ', 'TI', 'UR', 'VS'):
            self[date(year, MAR, 19)] = 'Josefstag'
        if self.prov == 'GL' and year >= 1835:
            if date(year, APR, 1) + rd(weekday=FR) != easter(year) - rd(days=2):
                self[date(year, APR, 1) + rd(weekday=TH)] = 'Näfelser Fahrt'
            else:
                self[date(year, APR, 8) + rd(weekday=TH)] = 'Näfelser Fahrt'
        self[easter(year)] = 'Ostern'
        if self.prov != 'VS':
            self[easter(year) - rd(days=2)] = 'Karfreitag'
            self[easter(year) + rd(weekday=MO)] = 'Ostermontag'
        if self.prov in ('BL', 'BS', 'JU', 'NE', 'SH', 'SO', 'TG', 'TI', 'ZH'):
            self[date(year, MAY, 1)] = 'Tag der Arbeit'
        self[easter(year) + rd(days=39)] = 'Auffahrt'
        self[easter(year) + rd(days=49)] = 'Pfingsten'
        self[easter(year) + rd(days=50)] = 'Pfingstmontag'
        if self.prov in ('AI', 'JU', 'LU', 'NW', 'OW', 'SZ', 'TI', 'UR', 'VS', 'ZG'):
            self[easter(year) + rd(days=60)] = 'Fronleichnam'
        if self.prov == 'JU':
            self[date(year, JUN, 23)] = 'Fest der Unabhängigkeit'
        if self.prov == 'TI':
            self[date(year, JUN, 29)] = 'Peter und Paul'
        if year >= 1291:
            self[date(year, AUG, 1)] = 'Nationalfeiertag'
        if self.prov in ('AI', 'JU', 'LU', 'NW', 'OW', 'SZ', 'TI', 'UR', 'VS', 'ZG'):
            self[date(year, AUG, 15)] = 'Mariä Himmelfahrt'
        if self.prov == 'VD':
            dt = date(year, SEP, 1) + rd(weekday=SU(+3)) + rd(weekday=MO)
            self[dt] = 'Lundi du Jeûne'
        if self.prov == 'OW':
            self[date(year, SEP, 25)] = 'Bruder Klaus'
        if self.prov in ('AI', 'GL', 'JU', 'LU', 'NW', 'OW', 'SG', 'SZ', 'TI', 'UR',
                         'VS', 'ZG'):
            self[date(year, NOV, 1)] = 'Allerheiligen'
        if self.prov in ('AI', 'LU', 'NW', 'OW', 'SZ', 'TI', 'UR', 'VS', 'ZG'):
            self[date(year, DEC, 8)] = 'Mariä Empfängnis'
        if self.prov == 'GE':
            self[date(year, DEC, 12)] = 'Escalade de Genève'
        self[date(year, DEC, 25)] = 'Weihnachten'
        if self.prov in ('AG', 'AR', 'AI', 'BL', 'BS', 'BE', 'FR', 'GL', 'GR', 'LU',
                         'NE', 'NW', 'OW', 'SG', 'SH', 'SZ', 'SO', 'TG', 'TI', 'UR',
                         'ZG', 'ZH'):
            self[date(year, DEC, 26)] = 'Stephanstag'
        if self.prov == 'GE':
            self[date(year, DEC, 31)] = 'Wiederherstellung der Republik'


class CH(Switzerland):
    pass


class Honduras(HolidayBase):

    def __init__(self, **kwargs):
        self.country = 'HND'
        HolidayBase.__init__(self, **kwargs)

    def _populate(self, year):
        if self.observed and date(year, JAN, 1):
            self[date(year, JAN, 1)] = "Año Nuevo [New Year's Day]"
        if self.observed and date(year, JAN, 6):
            name = 'Día de los Reyes Magos [The Three Wise Men Day] (Observed)'
            self[date(year, JAN, 6)] = name
        if self.observed and date(year, FEB, 3):
            name = 'Día de la virgen de Suyapa [Our Lady of Suyapa] (Observed)'
            self[date(year, FEB, 3)] = name
        if self.observed and date(year, MAR, 19):
            name = "Día del Padre [Father's Day] (Observed)"
            self[date(year, MAR, 19)] = name
        self[easter(year) + rd(weekday=TH(-1))] = 'Jueves Santo [Maundy Thursday]'
        self[easter(year) + rd(weekday=FR(-1))] = 'Viernes Santo [Good Friday]'
        self[easter(year) + rd(weekday=SA(-1))] = 'Sábado de Gloria [Holy Saturday]'
        self[easter(year) + rd(weekday=SU(-1))] = 'Domingo de Resurrección [Easter Sunday]'
        if self.observed and date(year, APR, 14):
            self[date(year, APR, 14)] = 'Día de las Américas [America Day]'
        if self.observed and date(year, MAY, 1):
            self[date(year, MAY, 1)] = 'Día del Trabajo [Labour Day]'
        may_first = date(int(year), 5, 1)
        weekday_seq = may_first.weekday()
        mom_day = 14 - weekday_seq
        if self.observed and date(year, MAY, mom_day):
            str_day = "Día de la madre [Mother's Day] (Observed)"
            self[date(year, MAY, mom_day)] = str_day
        if self.observed and date(year, SEP, 10):
            name = 'Día del niño [Children day] (Observed)'
            self[date(year, SEP, 10)] = name
        if self.observed and date(year, SEP, 15):
            name = 'Día de la Independencia [Independence Day]'
            self[date(year, SEP, 15)] = name
        if self.observed and date(year, SEP, 17):
            name = "Día del Maestro [Teacher's day] (Observed)"
            self[date(year, SEP, 17)] = name
        if year <= 2014:
            if self.observed and date(year, OCT, 3):
                self[date(year, OCT, 3)] = "Día de Morazán [Morazan's Day]"
            if self.observed and date(year, OCT, 12):
                self[date(year, OCT, 12)] = 'Día de la Raza [Columbus Day]'
            if self.observed and date(year, OCT, 21):
                str_day = 'Día de las Fuerzas Armadas [Army Day]'
                self[date(year, OCT, 21)] = str_day
        else:
            if self.observed and date(year, OCT, 3):
                name = 'Semana Morazánica [Morazan Weekend]'
                self[date(year, OCT, 3)] = name
            if self.observed and date(year, OCT, 4):
                name = 'Semana Morazánica [Morazan Weekend]'
                self[date(year, OCT, 4)] = name
            if self.observed and date(year, OCT, 5):
                name = 'Semana Morazánica [Morazan Weekend]'
                self[date(year, OCT, 5)] = name
        self[date(year, DEC, 25)] = 'Navidad [Christmas]'


class HND(Honduras):
    pass


class Hungary(HolidayBase):

    def __init__(self, **kwargs):
        self.country = 'HU'
        HolidayBase.__init__(self, **kwargs)

    def _populate(self, year):
        self._add_with_observed_day_off(date(year, JAN, 1), 'Újév', since=2014)
        if 1945 <= year <= 1950 or 1989 <= year:
            self._add_with_observed_day_off(date(year, MAR, 15), 'Nemzeti ünnep')
        if 1950 <= year <= 1989:
            self[date(year, MAR, 21)] = 'A Tanácsköztársaság kikiáltásának ünnepe'
            self[date(year, APR, 4)] = 'A felszabadulás ünnepe'
            if year not in (1956, 1989):
                self[date(year, NOV, 7)] = 'A nagy októberi szocialista forradalom ünnepe'
        easter_date = easter(year)
        if 2017 <= year:
            self[easter_date + rd(weekday=FR(-1))] = 'Nagypéntek'
        self[easter_date] = 'Húsvét'
        if 1955 != year:
            self[easter_date + rd(days=1)] = 'Húsvét Hétfő'
        self[easter_date + rd(days=49)] = 'Pünkösd'
        if year <= 1952 or 1992 <= year:
            self[easter_date + rd(days=50)] = 'Pünkösdhétfő'
        if 1946 <= year:
            self._add_with_observed_day_off(date(year, MAY, 1), 'A Munka ünnepe')
        if 1950 <= year <= 1953:
            self[date(year, MAY, 2)] = 'A Munka ünnepe'
        if 1950 <= year < 1990:
            self[date(year, AUG, 20)] = 'A kenyér ünnepe'
        else:
            self._add_with_observed_day_off(date(year, AUG, 20), 'Az államalapítás ünnepe')
        if 1991 <= year:
            self._add_with_observed_day_off(date(year, OCT, 23), 'Nemzeti ünnep')
        if 1999 <= year:
            self._add_with_observed_day_off(date(year, NOV, 1), 'Mindenszentek')
        if self.observed and 2010 <= year and date(year, DEC, 24).weekday() not in WEEKEND:
            self[date(year, DEC, 24)] = 'Szenteste'
        self[date(year, DEC, 25)] = 'Karácsony'
        if 1955 != year:
            self._add_with_observed_day_off(date(year, DEC, 26), 'Karácsony másnapja', since=2013, before=False, after=True)
        if self.observed and 2014 <= year and date(year, DEC, 31).weekday() == MON:
            self[date(year, DEC, 31)] = 'Szilveszter'

    def _add_with_observed_day_off(self, day, desc, since=2010, before=True, after=True):
        self[day] = desc
        if self.observed and since <= day.year:
            if day.weekday() == TUE and before:
                self[day - rd(days=1)] = desc + ' előtti pihenőnap'
            elif day.weekday() == THU and after:
                self[day + rd(days=1)] = desc + ' utáni pihenőnap'


class HU(Hungary):
    pass


class India(HolidayBase):
    PROVINCES = [
     'AS', 'CG', 'SK', 'KA', 'GJ', 'BR', 'RJ', 'OD',
     'TN', 'AP', 'WB', 'KL', 'HR', 'MH', 'MP', 'UP', 'UK', 'TS']

    def __init__(self, **kwargs):
        self.country = 'IND'
        HolidayBase.__init__(self, **kwargs)

    def _populate(self, year):
        self[date(year, JAN, 14)] = 'Makar Sankranti / Pongal'
        if year >= 1950:
            self[date(year, JAN, 26)] = 'Republic Day'
        if year >= 1947:
            self[date(year, AUG, 15)] = 'Independence Day'
        self[date(year, OCT, 2)] = 'Gandhi Jayanti'
        self[date(year, MAY, 1)] = 'Labour Day'
        self[date(year, DEC, 25)] = 'Christmas'
        if self.prov == 'GJ':
            self[date(year, JAN, 14)] = 'Uttarayan'
            self[date(year, MAY, 1)] = 'Gujarat Day'
            self[date(year, OCT, 31)] = 'Sardar Patel Jayanti'
        if self.prov == 'BR':
            self[date(year, MAR, 22)] = 'Bihar Day'
        if self.prov == 'RJ':
            self[date(year, MAR, 30)] = 'Rajasthan Day'
            self[date(year, JUN, 15)] = 'Maharana Pratap Jayanti'
        if self.prov == 'OD':
            self[date(year, APR, 1)] = 'Odisha Day (Utkala Dibasa)'
            self[date(year, APR, 15)] = 'Maha Vishuva Sankranti / Pana Sankranti'
        if self.prov in ('OD', 'AP', 'BR', 'WB', 'KL', 'HR', 'MH', 'UP', 'UK', 'TN'):
            self[date(year, APR, 14)] = "Dr. B. R. Ambedkar's Jayanti"
        if self.prov == 'TN':
            self[date(year, APR, 14)] = 'Puthandu (Tamil New Year)'
            self[date(year, APR, 15)] = 'Puthandu (Tamil New Year)'
        if self.prov == 'WB':
            self[date(year, APR, 14)] = 'Pohela Boishakh'
            self[date(year, APR, 15)] = 'Pohela Boishakh'
            self[date(year, MAY, 9)] = 'Rabindra Jayanti'
        if self.prov == 'AS':
            self[date(year, APR, 15)] = 'Bihu (Assamese New Year)'
        if self.prov == 'MH':
            self[date(year, MAY, 1)] = 'Maharashtra Day'
        if self.prov == 'SK':
            self[date(year, MAY, 16)] = 'Annexation Day'
        if self.prov == 'KA':
            self[date(year, NOV, 1)] = 'Karnataka Rajyotsava'
        if self.prov == 'AP':
            self[date(year, NOV, 1)] = 'Andhra Pradesh Foundation Day'
        if self.prov == 'HR':
            self[date(year, NOV, 1)] = 'Haryana Foundation Day'
        if self.prov == 'MP':
            self[date(year, NOV, 1)] = 'Madhya Pradesh Foundation Day'
        if self.prov == 'KL':
            self[date(year, NOV, 1)] = 'Kerala Foundation Day'
        if self.prov == 'CG':
            self[date(year, NOV, 1)] = 'Chhattisgarh Foundation Day'
        if self.prov == 'TS':
            self[date(year, OCT, 6)] = 'Bathukamma Festival'
            self[date(year, APR, 6)] = 'Eid al-Fitr'


class IND(India):
    pass


class Croatia(HolidayBase):

    def __init__(self, **kwargs):
        self.country = 'HR'
        HolidayBase.__init__(self, **kwargs)

    def _populate(self, year):
        self[date(year, JAN, 1)] = 'Nova Godina'
        self[date(year, JAN, 6)] = 'Sveta tri kralja'
        easter_date = easter(year)
        self[easter_date] = 'Uskrs'
        self[easter_date + rd(days=1)] = 'Uskrsni ponedjeljak'
        self[easter_date + rd(days=60)] = 'Tijelovo'
        self[date(year, MAY, 1)] = 'Međunarodni praznik rada'
        self[date(year, JUN, 22)] = 'Dan antifašističke borbe'
        self[date(year, JUN, 25)] = 'Dan državnosti'
        self[date(year, AUG, 5)] = 'Dan pobjede i domovinske zahvalnosti'
        self[date(year, AUG, 15)] = 'Velika Gospa'
        self[date(year, OCT, 8)] = 'Dan neovisnosti'
        self[date(year, NOV, 1)] = 'Svi sveti'
        self[date(year, DEC, 25)] = 'Božić'
        self[date(year, DEC, 26)] = 'Sveti Stjepan'


class HR(Croatia):
    pass


class Luxembourg(HolidayBase):

    def __init__(self, **kwargs):
        self.country = 'LU'
        HolidayBase.__init__(self, **kwargs)

    def _populate(self, year):
        self[date(year, JAN, 1)] = 'Neijoerschdag'
        self[easter(year) + rd(weekday=MO)] = 'Ouschterméindeg'
        self[date(year, MAY, 1)] = 'Dag vun der Aarbecht'
        if year >= 2019:
            self[date(year, MAY, 9)] = 'Europadag'
        self[easter(year) + rd(days=39)] = 'Christi Himmelfaart'
        self[easter(year) + rd(days=50)] = 'Péngschtméindeg'
        self[date(year, JUN, 23)] = 'Nationalfeierdag'
        self[date(year, AUG, 15)] = 'Léiffrawëschdag'
        self[date(year, NOV, 1)] = 'Allerhellgen'
        self[date(year, DEC, 25)] = 'Chrëschtdag'
        self[date(year, DEC, 26)] = 'Stiefesdag'


class LU(Luxembourg):
    pass


class Russia(HolidayBase):
    """
    https://en.wikipedia.org/wiki/Public_holidays_in_Russia
    """

    def __init__(self, **kwargs):
        self.country = 'RU'
        HolidayBase.__init__(self, **kwargs)

    def _populate(self, year):
        self[date(year, JAN, 1)] = 'Новый год'
        self[date(year, JAN, 2)] = 'Новый год'
        self[date(year, JAN, 3)] = 'Новый год'
        self[date(year, JAN, 4)] = 'Новый год'
        self[date(year, JAN, 5)] = 'Новый год'
        self[date(year, JAN, 6)] = 'Новый год'
        self[date(year, JAN, 7)] = 'Православное Рождество'
        self[date(year, JAN, 8)] = 'Новый год'
        self[date(year, FEB, 23)] = 'День защитника отечества'
        self[date(year, MAR, 8)] = 'День женщин'
        self[date(year, MAY, 1)] = 'Праздник Весны и Труда'
        self[date(year, MAY, 9)] = 'День Победы'
        self[date(year, JUN, 12)] = 'День России'
        self[date(year, NOV, 4)] = 'День народного единства'


class RU(Russia):
    pass


class Lithuania(HolidayBase):

    def __init__(self, **kwargs):
        self.country = 'LT'
        HolidayBase.__init__(self, **kwargs)

    def _populate(self, year):
        self[date(year, 1, 1)] = 'Naujieji metai'
        if year >= 1918:
            self[date(year, 2, 16)] = 'Lietuvos valstybės atkūrimo diena'
        if year >= 1990:
            self[date(year, 3, 11)] = 'Lietuvos nepriklausomybės atkūrimo diena'
        easter_date = easter(year)
        self[easter_date] = 'Velykos'
        self[easter_date + rd(days=1)] = 'Velykų antroji diena'
        self[date(year, 5, 1)] = 'Tarptautinė darbo diena'
        self[date(year, 5, 1) + rd(weekday=SU)] = 'Motinos diena'
        self[date(year, 6, 1) + rd(weekday=SU)] = 'Tėvo diena'
        if year >= 2003:
            self[date(year, 6, 24)] = 'Joninės, Rasos'
        if year >= 1991:
            self[date(year, 7, 6)] = 'Valstybės (Lietuvos karaliaus Mindaugo karūnavimo) diena'
        self[date(year, 8, 15)] = 'Žolinė (Švč. Mergelės Marijos ėmimo į dangų diena)'
        self[date(year, 11, 1)] = 'Visų šventųjų diena (Vėlinės)'
        self[date(year, 12, 24)] = 'Šv. Kūčios'
        self[date(year, 12, 25)] = 'Šv. Kalėdų pirma diena'
        self[date(year, 12, 26)] = 'Šv. Kalėdų antra diena'


class LT(Lithuania):
    pass


class Estonia(HolidayBase):

    def __init__(self, **kwargs):
        self.country = 'EE'
        HolidayBase.__init__(self, **kwargs)

    def _populate(self, year):
        e = easter(year)
        self[date(year, JAN, 1)] = 'uusaasta'
        self[date(year, FEB, 24)] = 'iseseisvuspäev'
        self[e - rd(days=2)] = 'suur reede'
        self[e] = 'ülestõusmispühade 1. püha'
        self[date(year, MAY, 1)] = 'kevadpüha'
        self[e + rd(days=49)] = 'nelipühade 1. püha'
        self[date(year, JUN, 23)] = 'võidupüha'
        self[date(year, JUN, 24)] = 'jaanipäev'
        self[date(year, AUG, 20)] = 'taasiseseisvumispäev'
        self[date(year, DEC, 24)] = 'jõululaupäev'
        self[date(year, DEC, 25)] = 'esimene jõulupüha'
        self[date(year, DEC, 26)] = 'teine jõulupüha'


class EE(Estonia):
    pass


class Iceland(HolidayBase):

    def __init__(self, **kwargs):
        self.country = 'IS'
        HolidayBase.__init__(self, **kwargs)

    def _populate(self, year):
        self[date(year, JAN, 1)] = 'Nýársdagur'
        self[easter(year) - rd(days=3)] = 'Skírdagur'
        self[easter(year) + rd(weekday=FR(-1))] = 'Föstudagurinn langi'
        self[easter(year)] = 'Páskadagur'
        self[easter(year) + rd(days=1)] = 'Annar í páskum'
        self[date(year, APR, 19) + rd(weekday=TH(+1))] = 'Sumardagurinn fyrsti'
        self[date(year, MAY, 1)] = 'Verkalýðsdagurinn'
        self[easter(year) + rd(days=39)] = 'Uppstigningardagur'
        self[easter(year) + rd(days=49)] = 'Hvítasunnudagur'
        self[easter(year) + rd(days=50)] = 'Annar í hvítasunnu'
        self[date(year, JUN, 17)] = 'Þjóðhátíðardagurinn'
        self[date(year, AUG, 1) + rd(weekday=MO(+1))] = 'Frídagur verslunarmanna'
        self[date(year, DEC, 24)] = 'Aðfangadagur'
        self[date(year, DEC, 25)] = 'Jóladagur'
        self[date(year, DEC, 26)] = 'Annar í jólum'
        self[date(year, DEC, 31)] = 'Gamlársdagur'


class IS(Iceland):
    pass


class Kenya(HolidayBase):

    def __init__(self, **kwargs):
        self.country = 'KE'
        HolidayBase.__init__(self, **kwargs)

    def _populate(self, year):
        self[date(year, JAN, 1)] = "New Year's Day"
        self[date(year, MAY, 1)] = 'Labour Day'
        self[date(year, JUN, 1)] = 'Madaraka Day'
        self[date(year, OCT, 20)] = 'Mashujaa Day'
        self[date(year, DEC, 12)] = 'Jamhuri (Independence) Day'
        self[date(year, DEC, 25)] = 'Christmas Day'
        self[date(year, DEC, 26)] = 'Boxing Day'
        for k, v in list(self.items()):
            if self.observed and k.weekday() == SUN:
                self[k + rd(days=1)] = v + ' (Observed)'

        self[easter(year) - rd(weekday=FR(-1))] = 'Good Friday'
        self[easter(year) + rd(weekday=MO(+1))] = 'Easter Monday'


class KE(Kenya):
    pass


class HongKong(HolidayBase):

    def __init__(self, **kwargs):
        self.country = 'HK'
        HolidayBase.__init__(self, **kwargs)

    def _populate(self, year):
        day_following = 'The day following '
        name = 'The first day of January'
        first_date = date(year, JAN, 1)
        if self.observed:
            if first_date.weekday() == SUN:
                self[first_date + rd(days=+1)] = day_following + self.first_lower(name)
                first_date = first_date + rd(days=+1)
            else:
                self[first_date] = name
        else:
            self[first_date] = name
        name = "Lunar New Year's Day"
        preceding_day_lunar = "The day preceding Lunar New Year's Day"
        second_day_lunar = 'The second day of Lunar New Year'
        third_day_lunar = 'The third day of Lunar New Year'
        fourth_day_lunar = 'The fourth day of Lunar New Year'
        dt = self.get_solar_date(year, 1, 1)
        new_year_date = date(dt.year, dt.month, dt.day)
        if self.observed:
            self[new_year_date] = name
            if new_year_date.weekday() in [MON, TUE, WED, THU]:
                self[new_year_date] = name
                self[new_year_date + rd(days=+1)] = second_day_lunar
                self[new_year_date + rd(days=+2)] = third_day_lunar
            elif new_year_date.weekday() == FRI:
                self[new_year_date] = name
                self[new_year_date + rd(days=+1)] = second_day_lunar
                self[new_year_date + rd(days=+3)] = fourth_day_lunar
            elif new_year_date.weekday() == SAT:
                self[new_year_date] = name
                self[new_year_date + rd(days=+2)] = third_day_lunar
                self[new_year_date + rd(days=+3)] = fourth_day_lunar
            elif new_year_date.weekday() == SUN:
                if year in (2006, 2007, 2010):
                    self[new_year_date + rd(days=-1)] = preceding_day_lunar
                    self[new_year_date + rd(days=+1)] = second_day_lunar
                    self[new_year_date + rd(days=+2)] = third_day_lunar
                else:
                    self[new_year_date + rd(days=+1)] = second_day_lunar
                    self[new_year_date + rd(days=+2)] = third_day_lunar
                    self[new_year_date + rd(days=+3)] = fourth_day_lunar
        else:
            self[new_year_date] = name
            self[new_year_date + rd(days=+1)] = second_day_lunar
            self[new_year_date + rd(days=+2)] = third_day_lunar
        name = 'Ching Ming Festival'
        if self.isLeapYear(year) or self.isLeapYear(year - 1) and year > 2008:
            ching_ming_date = date(year, APR, 4)
        else:
            ching_ming_date = date(year, APR, 5)
        if self.observed:
            if ching_ming_date.weekday() == SUN:
                self[ching_ming_date + rd(days=+1)] = day_following + name
                ching_ming_date = ching_ming_date + rd(days=+1)
            else:
                self[ching_ming_date] = name
        else:
            self[ching_ming_date] = name
        good_friday = 'Good Friday'
        easter_monday = 'Easter Monday'
        if self.observed:
            self[easter(year) + rd(weekday=FR(-1))] = good_friday
            self[easter(year) + rd(weekday=SA(-1))] = day_following + good_friday
            if ching_ming_date == easter(year) + rd(weekday=MO):
                self[easter(year) + rd(weekday=MO) + rd(days=+1)] = day_following + easter_monday
            else:
                self[easter(year) + rd(weekday=MO)] = easter_monday
        else:
            self[easter(year) + rd(weekday=FR(-1))] = good_friday
            self[easter(year) + rd(weekday=SA(-1))] = day_following + good_friday
            self[easter(year) + rd(weekday=MO)] = easter_monday
        name = 'Birthday of the Buddha'
        dt = self.get_solar_date(year, 4, 8)
        buddha_date = date(dt.year, dt.month, dt.day)
        if self.observed:
            if buddha_date.weekday() == SUN:
                self[buddha_date + rd(days=+1)] = day_following + name
            else:
                self[buddha_date] = name
        else:
            self[buddha_date] = name
        name = 'Labour Day'
        labour_date = date(year, MAY, 1)
        if self.observed:
            if labour_date.weekday() == SUN:
                self[labour_date + rd(days=+1)] = day_following + name
            else:
                self[labour_date] = name
        else:
            self[labour_date] = name
        name = 'Tuen Ng Festival'
        dt = self.get_solar_date(year, 5, 5)
        tuen_ng_date = date(dt.year, dt.month, dt.day)
        if self.observed:
            if tuen_ng_date.weekday() == SUN:
                self[tuen_ng_date + rd(days=+1)] = day_following + name
            else:
                self[tuen_ng_date] = name
        else:
            self[tuen_ng_date] = name
        name = 'Hong Kong Special Administrative Region Establishment Day'
        hksar_date = date(year, JUL, 1)
        if self.observed:
            if hksar_date.weekday() == SUN:
                self[hksar_date + rd(days=+1)] = day_following + name
            else:
                self[hksar_date] = name
        else:
            self[hksar_date] = name
        name = 'The 70th anniversary day of the victory of the Chinese ' + "people's war of resistance against Japanese aggression"
        if year == 2015:
            self[date(year, SEP, 3)] = name
        name = 'Chinese Mid-Autumn Festival'
        dt = self.get_solar_date(year, 8, 15)
        mid_autumn_date = date(dt.year, dt.month, dt.day)
        if self.observed:
            if mid_autumn_date.weekday() == SAT:
                self[mid_autumn_date] = name
            else:
                self[mid_autumn_date + rd(days=+1)] = day_following + 'the ' + name
            mid_autumn_date = mid_autumn_date + rd(days=+1)
        else:
            self[mid_autumn_date] = name
        name = 'National Day'
        national_date = date(year, OCT, 1)
        if self.observed:
            if national_date.weekday() == SUN or national_date == mid_autumn_date:
                self[national_date + rd(days=+1)] = day_following + name
            else:
                self[national_date] = name
        else:
            self[national_date] = name
        name = 'Chung Yeung Festival'
        dt = self.get_solar_date(year, 9, 9)
        chung_yeung_date = date(dt.year, dt.month, dt.day)
        if self.observed:
            if chung_yeung_date.weekday() == SUN:
                self[chung_yeung_date + rd(days=+1)] = day_following + name
            else:
                self[chung_yeung_date] = name
        else:
            self[chung_yeung_date] = name
        name = 'Christmas Day'
        first_after_christmas = 'The first weekday after ' + name
        second_after_christmas = 'The second weekday after ' + name
        christmas_date = date(year, DEC, 25)
        if self.observed:
            if christmas_date.weekday() == SUN:
                self[christmas_date] = name
                self[christmas_date + rd(days=+1)] = first_after_christmas
                self[christmas_date + rd(days=+2)] = second_after_christmas
            elif christmas_date.weekday() == SAT:
                self[christmas_date] = name
                self[christmas_date + rd(days=+2)] = first_after_christmas
            else:
                self[christmas_date] = name
                self[christmas_date + rd(days=+1)] = first_after_christmas
        else:
            self[christmas_date] = name
            self[christmas_date + rd(days=+1)] = day_following + name

    def isLeapYear(self, year):
        if year % 4 != 0:
            return False
        else:
            if year % 100 != 0:
                return True
            if year % 400 != 0:
                return False
            return True

    def first_lower(self, s):
        return s[0].lower() + s[1:]

    g_lunar_month_days = [
     986788, 990538, 339092, 986262, 988470,
     273068, 985812, 988850, 143012, 986788,
     407114, 988746, 988310, 338262, 984410,
     985814, 136914, 990034, 473892, 990500,
     989770, 341146, 988332, 984428, 273258,
     986536, 990546, 146724, 990500, 399948,
     985686, 988334, 337260, 988852, 986536,
     204178, 986770, 470310, 988454, 985686,
     398518, 988506, 985812, 276138, 989000,
     988818, 144678, 988458, 469594, 985708,
     988506, 338772, 985956, 990026, 211604,
     989844, 529706, 988462, 985772, 398698,
     988586, 986532, 269642, 990538, 986260,
     203054, 988470, 469684, 985812, 988882,
     339620, 988836, 988746, 273558, 988310,
     534870, 984410, 985818, 399058, 990034,
     989988, 277066, 989770, 668826, 988332,
     984428, 396138, 986538, 990610, 343332,
     990500, 989772, 201900, 988334, 534956,
     984756, 986538, 339346, 986770, 986406,
     272982, 985686, 988342, 142004, 985812,
     472746, 989000, 988818, 341286, 988458,
     985690, 267610, 988522, 600916, 986020,
     990026, 408212, 989844, 989482, 272988,
     985772, 988522, 142180, 986532, 400722,
     986698, 986262, 334126, 989526, 985780,
     202156, 988882, 732836, 988836, 988746,
     406678, 988310, 985430, 330422, 985946,
     988884, 145060, 989988, 473674, 989770,
     988330, 338266, 985452, 985962, 203604,
     990610, 539940, 990500, 989772, 398508,
     988334, 985516, 265642, 986794, 986770,
     204070, 986406, 469590, 985686, 988342,
     338612, 985812, 988874, 274068, 988820,
     537898, 988458, 985690, 398682, 988522,
     985940, 268106, 990026, 989844, 211242,
     989484, 471708, 985772, 988522, 338788,
     986532, 990538, 269460, 986262, 530734,
     985430, 985782, 398764, 988884, 986788,
     273994, 988746, 988438, 141622]
    START_YEAR, END_YEAR = 1901, 1900 + len(g_lunar_month_days)
    LUNAR_START_DATE, SOLAR_START_DATE = (1901, 1, 1), datetime(1901, 2, 19)
    LUNAR_END_DATE, SOLAR_END_DATE = (2099, 12, 30), datetime(2100, 2, 18)

    def get_leap_month(self, lunar_year):
        return self.g_lunar_month_days[(lunar_year - self.START_YEAR)] >> 16 & 15

    def lunar_month_days(self, lunar_year, lunar_month):
        return 29 + (self.g_lunar_month_days[(lunar_year - self.START_YEAR)] >> lunar_month & 1)

    def lunar_year_days(self, year):
        days = 0
        months_day = self.g_lunar_month_days[(year - self.START_YEAR)]
        for i in range(1, 13 if self.get_leap_month(year) == 15 else 14):
            day = 29 + (months_day >> i & 1)
            days += day

        return days

    def get_solar_date(self, year, month, day):
        span_days = 0
        for y in range(self.START_YEAR, year):
            span_days += self.lunar_year_days(y)

        leap_month = self.get_leap_month(year)
        for m in range(1, month + (month > leap_month)):
            span_days += self.lunar_month_days(year, m)

        span_days += day - 1
        return self.SOLAR_START_DATE + timedelta(span_days)


class HK(HongKong):
    pass


class Peru(HolidayBase):

    def __init__(self, **kwargs):
        self.country = 'PE'
        HolidayBase.__init__(self, **kwargs)

    def _populate(self, year):
        self[date(year, JAN, 1)] = "Año Nuevo [New Year's Day]"
        name = 'San Pedro y San Pablo [Feast of Saints Peter and Paul]'
        self[date(year, JUN, 29)] = name
        name = 'Día de la Independencia [Independence Day]'
        self[date(year, JUL, 28)] = name
        name = 'Día de las Fuerzas Armadas y la Policía del Perú'
        self[date(year, JUL, 29)] = name
        name = 'Día de Santa Rosa de Lima'
        self[date(year, AUG, 30)] = name
        name = 'Combate Naval de Angamos [Battle of Angamos]'
        self[date(year, OCT, 8)] = name
        self[easter(year) + rd(weekday=TH(-1))] = 'Jueves Santo [Maundy Thursday]'
        self[easter(year) + rd(weekday=FR(-1))] = 'Viernes Santo [Good Friday]'
        self[easter(year) + rd(weekday=SA(-1))] = 'Sábado de Gloria [Holy Saturday]'
        self[easter(year) + rd(weekday=SU(-1))] = 'Domingo de Resurrección [Easter Sunday]'
        self[date(year, MAY, 1)] = 'Día del Trabajo [Labour Day]'
        name = 'Día de Todos Los Santos [All Saints Day]'
        self[date(year, NOV, 1)] = name
        name = 'Inmaculada Concepción [Immaculate Conception]'
        self[date(year, DEC, 8)] = name
        self[date(year, DEC, 25)] = 'Navidad [Christmas]'


class PE(Peru):
    pass


class Nigeria(HolidayBase):

    def __init__(self, **kwargs):
        self.country = 'NG'
        HolidayBase.__init__(self, **kwargs)

    def _populate(self, year):
        self[date(year, JAN, 1)] = "New Year's day"
        self[date(year, MAY, 1)] = "Worker's day"
        self[date(year, MAY, 27)] = "Children's day"
        self[date(year, JUN, 12)] = 'Democracy day'
        self[date(year, OCT, 1)] = 'Independence day'
        self[date(year, DEC, 25)] = 'Christmas day'
        self[date(year, DEC, 26)] = 'Boxing day'


class NG(Nigeria):
    pass


class DominicanRepublic(HolidayBase):

    def __init__(self, **kwargs):
        self.country = 'DO'
        HolidayBase.__init__(self, **kwargs)

    @staticmethod
    def __change_day_by_law(holiday, latest_days=(3, 4)):
        if holiday >= date(1997, 6, 27):
            if holiday.weekday() in (1, 2):
                holiday -= rd(weekday=MO(-1))
            elif holiday.weekday() in latest_days:
                holiday += rd(weekday=MO(1))
        return holiday

    def _populate(self, year):
        self[date(year, JAN, 1)] = "Año Nuevo [New Year's Day]"
        epiphany_day = self.__change_day_by_law(date(year, JAN, 6))
        self[epiphany_day] = 'Día de los Santos Reyes [Epiphany]'
        self[date(year, JAN, 21)] = 'Día de la Altagracia [Lady of Altagracia]'
        duarte_day = self.__change_day_by_law(date(year, JAN, 26))
        self[duarte_day] = 'Día de Duarte [Juan Pablo Duarte Day]'
        self[date(year, FEB, 27)] = 'Día de Independencia [Independence Day]'
        self[easter(year) + rd(weekday=FR(-1))] = 'Viernes Santo [Good Friday]'
        labor_day = self.__change_day_by_law(date(year, MAY, 1), (3, 4, 6))
        self[labor_day] = 'Día del Trabajo [Labor Day]'
        self[date(year, JUN, 11)] = 'Corpus Christi [Feast of Corpus Christi]'
        restoration_day = date(year, AUG, 16) if (year - 2000) % 4 == 0 and year < 2008 else self.__change_day_by_law(date(year, AUG, 16))
        self[restoration_day] = 'Día de la Restauración [Restoration Day]'
        self[date(year, SEP, 24)] = 'Día de las Mercedes             [Our Lady of Mercedes Day]'
        constitution_day = self.__change_day_by_law(date(year, NOV, 6))
        self[constitution_day] = 'Día de la Constitución [Constitution Day]'
        self[date(year, DEC, 25)] = 'Día de Navidad [Christmas Day]'


class DO(DominicanRepublic):
    pass


class Nicaragua(HolidayBase):
    PROVINCES = [
     'MN']

    def __init__(self, **kwargs):
        self.country = 'NI'
        self.prov = kwargs.pop('prov', kwargs.pop('state', 'MN'))
        HolidayBase.__init__(self, **kwargs)

    def _populate(self, year):
        self[date(year, JAN, 1)] = "Año Nuevo [New Year's Day]"
        self[easter(year) + rd(weekday=TH(-1))] = 'Jueves Santo [Maundy Thursday]'
        self[easter(year) + rd(weekday=FR(-1))] = 'Viernes Santo [Good Friday]'
        self[date(year, MAY, 1)] = 'Día del Trabajo [Labour Day]'
        if 2020 >= year >= 1979:
            self[date(year, JUL, 19)] = 'Día de la Revolución [Revolution Day]'
        self[date(year, SEP, 14)] = 'Batalla de San Jacinto [Battle of San Jacinto]'
        self[date(year, SEP, 15)] = 'Día de la Independencia [Independence Day]'
        self[date(year, DEC, 8)] = "Concepción de María [Virgin's Day]"
        self[date(year, DEC, 25)] = 'Navidad [Christmas]'
        if self.prov:
            if self.prov == 'MN':
                self[date(year, AUG, 1)] = 'Bajada de Santo Domingo'
                self[date(year, AUG, 10)] = 'Subida de Santo Domingo'


class NI(Nicaragua):
    pass