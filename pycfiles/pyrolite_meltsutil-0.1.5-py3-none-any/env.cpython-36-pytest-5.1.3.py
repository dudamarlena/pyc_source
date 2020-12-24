# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: c:\github\pyrolite-meltsutil\pyrolite_meltsutil\data\env.py
# Compiled at: 2019-10-30 03:01:56
# Size of source mod 2**32: 52523 bytes
import builtins as @py_builtins, _pytest.assertion.rewrite as @pytest_ar
from pyrolite.util.text import normalise_whitespace, to_width
from pathlib import Path

def mvar(**kwargs):
    """A data dictonary specifying MELTS environment variables."""
    d = dict(validate=None,
      desc=None,
      type=None,
      units=None,
      set=True,
      default=None,
      overridden_by=None,
      dependent_on=None,
      priorty=0)
    d.update(kwargs)
    return d


def description(text, width=69):
    return to_width((normalise_whitespace(text)), width=width)


def filepath_validator(path):
    """Validator for file paths."""
    if isinstance(path, str):
        path = Path(path)
    return path.exists() and path.isfile()


def dirpath_validator(path):
    """Validator for directory paths."""
    if isinstance(path, str):
        path = Path(path)
    return path.exists() and path.isdir()


def numeric_validator(value):
    """Validator for numeric values."""
    return isinstance(float(value), float) or isinstance(int(value), int)


def typecast(type, item):
    """Typecasts argument input for lambda functions."""
    if isinstance(item, list):
        return [lambda x: f(type(x)) if callable(f) else f for f in item]
    else:
        return lambda x: item(type(x))


MELTS_environment_variables = {'VERSION':mvar(default='pMELTS',
   validate=lambda x: x in ('MELTS', 'pMELTS'),
   desc=description('Set to choose the liquid thermodynamic model.\n           pMELTS is only recommended for peridotite bulk\n           compositions between 1 and 4 GPa. If doing pHMELTS\n           calculations then use ‘pMELTS’ for melting and\n           ‘MELTS’ for low-pressure crystallization.')), 
 'OLD_GARNET':mvar(set=False,
   type=bool,
   desc=description('Uses the old, incorrect, garnet model. When set,\n              the behavior will resemble that of all GUI\n              versions of MELTS released before 2005 (including\n              Java MELTS) and the default behavior of\n              Adiabat_1ph versions 1.4 – 2.X. When unset,\n              will behave as if ADIABAT_FIX_GARNET was set in\n              older (pre-3.0) versions of Adiabat_1ph.')), 
 'OLD_SPINEL':mvar(set=False,
   type=bool,
   desc=description('Use the spinel model from Sack and\n              Ghiorso [1991], with perfectly ideal\n              mixing of volumes. When set, gives the\n              same behavior as Java MELTS and\n              earlier (pre-3.0) versions of\n              Adiabat_1ph. When unset, uses the\n              spinel volume model as formulated in\n              Ghiorso and Sack [1991].')), 
 'OLD_BIOTITE':mvar(set=False,
   type=bool,
   desc=description('Uses the biotite model from Sack and Ghiorso\n           [1989] instead of the default alphaMELTS one.\n           When set, the program uses the same code as\n           GUI versions of MELTS (2005-present). The\n           behavior may differ slightly from earlier GUI\n           versions of MELTS as a small error was fixed.')), 
 '2_AMPH':mvar(set=False,
   type=bool,
   desc=description('Uses separate orthoamphibole and clinoamphibole\n              phases. When set, gives the same behavior as Java\n              MELTS and Corba MELTS applets, and earlier versions\n              of Adiabat_1ph (which inherited its code from the\n              Java MELTS branch). When unset, will use a single\n              cummingtonite-grunerite-tremolite solution and deduce\n              the amphibole structure from the energetics.')), 
 'NO_CHLORITE':mvar(set=False,
   type=bool,
   desc=description('As of version 1.6, the chlorite model of\n               Hunziker [2003] is included in alphaMELTS\n               (see Smith et al. [2007]). To reproduce previous\n               results for bulk compositions that may stabilize\n               chlorite, add a ‘Suppress: chlorite’ line to the\n               melts_file or set this variable.')), 
 'MODE':mvar(validate=lambda x: x in ('geothermal', 'isenthalpic', 'isentropic', 'isobaric', 'isochoric', 'isothermal',
      'ptfile', 'ptgrid', 'tpgrid'),
   default='isentropic',
   desc=description('Sets the calculation mode. This variable is case\n             insensitive. ‘PTfile’ (‘PTPath’ is also accepted\n             for backwards compatibility) reads in P and T from\n             a file; see below. ‘PTgrid’ and ‘TPgrid’ perform\n             calculations on a grid bounded by the starting T\n             and ALPHAMELTS_MINT/MAXT, and by the starting P and\n             ALPHAMELTS_MINP/MAXP. For ‘PTgrid’ the T-loop is\n             inside the P-loop, whereas ‘TPgrid’ is the other\n             way round; in either case the (superliquidus or\n             subsolidus) starting solution migrates with the\n             outer loop. Generally, unless liquid is suppressed,\n             ‘PTgrid’ with ALPHAMELTS_DELTAT < 0 will be the\n             easiest combination. For other modes, there are\n             various ways to initialize P, T and / or reference\n             entropy, enthalpy or volume, and the thermodynamic\n             path is set using ALPHAMELTS_DELTAP and / or\n             ALPHAMELTS_DELTAT.')), 
 'PTPATH_FILE':mvar(set=False,
   validate=filepath_validator,
   desc=description('Gives the name of the ptpath_file, which is a simple\n            space delimited text file with one ‘P_value T_value’\n            pair per line. If ALPHAMELTS_DELTAP and\n            ALPHAMELTS_DELTAT are both zero the user will be asked\n            for a maximum number of iterations to perform.')), 
 'DELTAP':mvar(validate=numeric_validator,
   type=float,
   default=1000.0,
   units='bars',
   desc=description('This sets the pressure increment for isentropic,\n               isothermal, geothermal or phase diagram mode.\n               This is a signed number; i.e., a positive value steps\n               upwards in P, negative steps down. If using a ptpath_file,\n               a non-zero ALPHAMELTS_DELTAP means the whole will be read\n               in and executed. Setting ALPHAMELTS_DELTAP to zero, with a\n               non-zero value for ALPHAMELTS_DELTAT, means that phase\n               diagram mode will step in temperature instead of pressure\n               (except for liquid).')), 
 'DELTAT':mvar(validate=numeric_validator,
   default=10.0,
   type=float,
   units='Degrees Celsius',
   desc=description('This sets the temperature increment for isobaric,\n               isochoric, geothermal or phase diagram mode. This is a\n               signed number; i.e., a positive value steps upwards in T,\n               negative steps down. If using a ptpath_file, a non-zero\n               ALPHAMELTS_DELTAT means the whole will be read in and\n               executed. For phase diagram mode to step in temperature\n               ALPHAMELTS_DELTAP must be set to zero.')), 
 'MAXP':mvar(validate=numeric_validator,
   type=float,
   default=lambda env: [
  30000, 40000][(env['VERSION'] != 'MELTS')],
   dependent_on=[
  'VERSION'],
   units='bars',
   desc=description('Sets the maximum pressure the program will go to on\n                 execution.')), 
 'MINP':mvar(validate=numeric_validator,
   type=float,
   default=lambda env: [
  1, 10000][(env['VERSION'] != 'MELTS')],
   dependent_on=[
  'VERSION'],
   units='bars',
   desc=description('Sets the minimum pressure the program will go to on\n                 execution.')), 
 'MAXT':mvar(validate=numeric_validator,
   type=float,
   default=2000,
   units='Degrees Celsius',
   desc=description('Sets the maximum temperature the program will go to on\n                  execution.')), 
 'MINT':mvar(validate=numeric_validator,
   type=float,
   default=0,
   units='Degrees Celsius',
   desc=description('Sets the minimum temperature the program will go to on\n                  execution.')), 
 'ALTERNATIVE_FO2':mvar(set=False,
   type=bool,
   desc=description('Normally, the parameterization of Kress and\n            Carmichael [1991] is used to calculate fO2 in the\n            liquid. If conditions are subsolidus or liquid is\n            suppressed then the approach detailed in Asimow and\n            Ghiorso [1998] is used to construct an appropriate\n            redox reaction to solve for fO2 of the bulk\n            assemblage. If this environment variable is set,\n            however, then the method of Asimow and Ghiorso\n            [1998] is used to calculate fO2 regardless of\n            whether liquid is present and so, in theory, allows\n            for a smoother transition across the solidus. ')), 
 'LIQUID_FO2':mvar(set=False,
   type=bool,
   overridden_by=[
  'LIQUID_FO2'],
   desc=description('The method of Asimow and Ghiorso\n           [1998] is computationally more involved than the\n           parameterization of Kress and Carmichael [1991] and it\n           is not uncommon for fO2 calculations to be successful\n           with liquid present but fail subsolidus. It is possible\n           to turn off the fO2 buffer manually (option 5).\n           Alternatively, if this environment variable is set then\n           the fO2 buffer, as formulated in Kress and Carmichael\n           [1991], will only be imposed when liquid is present.\n           Note that setting this variable does not change the\n           fO2 buffer setting (e.g. ‘FMQ’); the program just ignores\n            the flag if no liquid is around.')), 
 'IMPOSE_FO2':mvar(set=False,
   type=bool,
   desc=description('Normally, for isentropic, isenthalpic and isochoric\n           modes any fO2 buffer will be switched off on execution\n           once the reference entropy, enthalpy or volume has been\n           set (usually after the first calculation or before if set\n           manually). If this environment variable is set then the\n           program will alternate between (1) an unbuffered\n           isenthalpic / isentropic / isochoric step and (2) an\n           isobaric / isothermal fO2 buffered step. Overall this\n           approximates an isenthalpic, isentropic or isochoric\n           path with a desired fO2 buffer.')), 
 'FO2_PRESSURE_TERM':mvar(set=False,
   type=bool,
   desc=description('In most versions of MELTS, including Corba\n              MELTS and alphaMELTS, by default, reference fO2\n              buffers in the system Fe-Si-O are calculated from\n              the equations given in Myers and Eugster [1983].\n              In the standalone GUI version of MELTS a pressure\n              term is added to the fayalite-magnetite-quartz\n              buffer (FMQ) to give:\n\n              log(fO2) = − 24441.9/T + 0.110 (P − 1)/T + 8.290\n\n              When this environment variable is set then\n              alphaMELTS uses the equation as shown whereas by\n              default the second term is omitted. Inclusion of\n              the pressure term can have subtle effects on the\n              stability of certain phases such as pyroxenes.\n              Note that in Kessel et al. [2001] the coefficient\n              on the pressure term is 0.05, rather than 0.110;\n              the value of 0.110 was chosen by Ghiorso to\n              maintain consistency with Berman [1988].')), 
 'CONTINUOUS_MELTING':mvar(set=False,
   type=bool,
   desc=description('By default, batch melting equations are used.\n               Setting this environment variable will change the\n               melting mode to continuous or fractional, where\n               melt is extracted after each equilibrium. Set\n               ALPHAMELTS_MINF to 0 for perfect fractional\n               melting. In practice though, the program will\n               run more smoothly if ALPHAMELTS_MINF is slightly\n               greater than 0. See the next four environment\n               variables’ entries for more details.')), 
 'MINF':mvar(default=0.005,
   type=float,
   validator=typecast(float, [numeric_validator, lambda x: (x >= 0.0) & (x < 1.0)]),
   overridden_by=[
  'MINPHI'],
   desc=description('If ALPHAMELTS_CONTINUOUS_MELTING is set, then by default a\n         fixed melt fraction, by mass, marks the threshold above which\n         melt is extracted. This variable is used to change the amount\n         of melt retained. If the current melt fraction is less than\n         ALPHAMELTS_MINF then all the melt will be retained until the\n         next step, otherwise the amount of melt removed (approximately\n         F - ALPHAMELTS_MINF) will be adjusted so such that the melt\n         fraction is exactly ALPHAMELTS_MINF after extraction.')), 
 'MINPHI':mvar(set=False,
   type=float,
   validator=typecast(float, [numeric_validator, lambda x: (x >= 0.0) & (x < 1.0)]),
   overridden_by=[
  'CONTINUOUS_RATIO'],
   desc=description('If ALPHAMELTS_CONTINUOUS_MELTING is set, then set this\n           environment variable controls the retained melt fraction,\n           by volume i.e. the ‘residual porosity’. If the current melt\n           fraction is less than ALPHAMELTS_MINPHI then all the melt\n           will be retained until the next step, otherwise the amount\n           of melt removed (approximately phi - ALPHAMELTS_MINPHI) will\n           be adjusted so that the melt fraction, by volume, is exactly\n           ALPHAMELTS_MINPHI after extraction.')), 
 'CONTINUOUS_RATIO':mvar(set=False,
   type=float,
   validator=typecast(float, [numeric_validator, lambda x: (x >= 0.0) & (x < 1.0)]),
   overridden_by=[
  'CONTINUOUS_VOLUME'],
   desc=description('This implements another alternative definition\n             of continuous melting. Instead of extracting all\n             liquid above a fixed mass or volume fraction, this\n             option, if set, causes the program to multiply the\n             liquid mass by a fixed ratio.')), 
 'CONTINUOUS_VOLUME':mvar(set=False,
   type=float,
   desc=description('"This option, if set, extracts the required\n              amount of melt to retain a constant total volume.\n              This reference volume is set the first time\n              melting occurs and is equal to the solid volume\n              plus whatever melt volume is retained according\n              to the ALPHAMELTS_MINPHI variable (or a default\n              value of 0.002 if that is unset). Only for\n              isobaric or isothermal calculations. Note that\n              this is not an ‘isochoric’ calculation as far\n              as alphaMELTS is concerned because melting is\n              still allowed to cause expansion; this option\n              only controls how much melt must be extracted\n              to return to the original volume and, if\n              necessary, also adjusts pressure (for isothermal\n              calculations) or temperature (for isobaric\n              calculations) to maintain equilibrium.')), 
 'FRACTIONATE_SOLIDS':mvar(set=False,
   type=bool,
   desc=description('To turn on fractional crystallization of all\n               solid phases, set this option to true (does not\n               include water, see below). Do not use this\n               option if you wish to selectively fractionate\n               just a few phases; instead put ‘Fractionate:\n               phase’ lines in you melts_file (see the ‘MELTS\n               file’ section) or adjust individual phase\n               settings with menu option 8.')), 
 'MASSIN':mvar(default=0.001,
   type=float,
   validator=typecast(float, [numeric_validator, lambda x: (x >= 0.0) & (x < 1.0)]),
   overridden_by=[
  'MINW'],
   desc=description('Set to the mass in grams of each solid phase that is\n                   retained during fractional crystallization. An increased\n                   value may help to stabilize the calculation. A smaller value\n                   can also be used, but a minimum of 10-6 grams is recommended.\n                   nce the phase is no longer in the equilibrium assemblage it\n                   will be completely exhausted, regardless of the\n                   ALPHAMELTS_MASSIN value.')), 
 'FRACTIONATE_WATER':mvar(set=False,
   type=bool,
   desc=description('To remove free water at each calculation stage\n                              in an analogous way to how melt is removed during\n                              continuous melting, set this variable true. (Note\n                              that, in MELTS and pMELTS, water is treated like\n                              a ‘solid’, in the sense that it is not melt, so\n                              you can achieve the same effect by putting a\n                              ‘Fractionate: water’ line in your melts_file.\n                              However, water is treated differently from the\n                              other mineral phases in that it may be extracted\n                              during melting or crystallization.)')), 
 'MINW':mvar(set=False,
   type=float,
   validator=typecast(float, [numeric_validator, lambda x: (x >= 0.0) & (x < 1.0)]),
   desc=description('Set to the proportion of retained water, relative to the\n                 total system mass. Works in a similar way, for water, as\n                 ALPHAMELTS_MINF does for melt; may be set to exactly zero. If\n                 not set then fractionation of water is treated in a similar way\n                 to fractionation of a solid phase i.e. a nominal mass of 10-4\n                 grams is retained at each stage to stabilize the calculation;\n                 the smaller mass of water retained, compared to other solid\n                 phases, reflects its significantly lower molecular mass.')), 
 'FRACTIONATE_TARGET':mvar(set=False,
   type=float,
   desc=description('During normal forward fractional\n                               crystallization a (negative) increment is added\n                               to the temperature at each step,\n                               ALPHAMELTS_DELTAT, and the run is terminated when\n                               the temperature goes below ALPHAMELTS_MINT. If\n                               this environment variable is set then forward or\n                               backward fractionation is performed so that the\n                               MgO content (in wt %) or the Mg# (in mol %) hits\n                               a particular target; see the next two entries.\n                               When option 3 is called alphaMELTS will perform\n                               a single calculation for the current P-T\n                               conditions, in the normal way. When option 4 is\n                               used it will first try to find the liquidus\n                               instead and use that to decide whether forward\n                               or backwards fractionation is required to move\n                               the liquid towards the target composition.\n                               For forward fractionation, temperature will be\n                               reduced, by an amount equal to the absolute value\n                               of ALPHAMELTS_DELTAT, each time. For backwards\n                               fractionation the program will step down (by the\n                               same temperature increment) until one or more\n                               ‘allowed’ solid phases join the assemblage. The\n                               ‘allowed’ solid phases are any MgO-brearing\n                               phases that have been ‘allowed’ by setting\n                               ALPHAMELTS_FRACTIONATE_SOLIDS or by having\n                               ‘Fractionate:’ lines in the melts_file. The\n                               routine then assimilates these phases before\n                               searching for the new liquidus. For H2O-rich\n                               compositions, the liquidus temperature will be\n                               for a melt composition that is water-saturated,\n                               but not oversaturated enough to exsolve vapor (it\n                               may also help to buffer aH2O).\n                               Output will be written each time the new liquidus\n                               is found. Forward- or backward-fractionated trace\n                               element compostions will be calculated if\n                               ALPHAMELTS_DO_TRACE is on. Execution continues\n                               until the target MgO or Mg# is reached or just\n                               passed; therefore, the smaller ALPHAMELTS_DELTAT\n                               is, the closer the liquid composition will be to\n                               the target. In the limit as the step size tends\n                               to zero a liquid composition that is on, say,\n                               the plagioclase + clinopyroxene cotectic would\n                               be expected to stay on the cotectic as back\n                               fractionation proceeds (at least until a thermal\n                               divide is encountered); in practice one or other\n                               solid phase may occasionally be dropped from the\n                               assemblage. For complicated peritectic\n                               relationships the ‘Amoeba’ routine (menu option\n                               17) is more useful for constraining a plausible,\n                               but still non-unique, parental melt.')), 
 'MGO_TARGET':mvar(default=8.0,
   type=float,
   validator=typecast(float, [lambda x: isinstance(x, float), lambda x: (x > 0.0) & (x < 100.0)]),
   overridden_by=[
  'MGNUMBER_TARGET'],
   desc=description('Sets the target MgO content of the liquid for forward\n                       or backward fractionation to the value in wt %. When\n                       using ‘Amoeba’ (menu option 17) the value of\n                       ALPHAMELTS_MGO_TARGET is used to set the MgO of the\n                       parental liquid composition and the target MgO content\n                       for the evolved liquid composition is taken from the\n                       melts_file(s). Once ‘Amoeba’ is finished, reading in\n                       another melts_file will revert to using\n                       ALPHAMELTS_MGO_TARGET as the stop point for forward or\n                       backward fractional crystallization.')), 
 'MGNUMBER_TARGET':mvar(set=False,
   type=float,
   validator=typecast(float, [lambda x: isinstance(x, float), lambda x: (x > 0.0) & (x < 100.0)]),
   desc=description('Sets the target Mg# of the liquid for forward or\n                            backward fractionation to the value in mol %. When\n                            using ‘Amoeba’ the value of\n                            ALPHAMELTS_MGNUMBER_TARGET is used in a comparable\n                            way to ALPHAMELTS MGO_TARGET above.')), 
 'ASSIMILATE':mvar(set=False,
   type=bool,
   desc=description('This environment variable causes a user-defined mass\n                       of a second bulk composition to be added after each\n                       calculation stage (see ‘Bulk composition’). It is\n                       intended for calculations at specified P-T conditions\n                       (e.g. isobaric, isothermal or PTpath modes) or for\n                       heat-balanced assimilation in isenthalpic mode. It also\n                       works for isentropic or isochoric constraints under\n                       certain circumstances but these options are under\n                       development and, as yet, untested. Melt may be extracted\n                       or solid phases fractionated simultaneously.\n                       On execution, if the mode is isothermal or\n                       ALPHAMELTS_DELTAT is zero and the mode is isobaric or\n                       ALPHAMELTS_DELTAP is zero then you will be asked the\n                       number of iterations you wish to perform. The program\n                       will then request the file type / number of files and the\n                       name(s) before the first equilibration9. The assimilant\n                       bulk composition may be fixed by a single enrichment_file\n                       or binary restart_file, or by providing separate\n                       enrichment_files for each mineral phase in the\n                       assimilant. For separate enrichment_files, phase\n                       compositions are given in wt% oxides and it is up to the\n                       user to ensure the solid compositions are close to\n                       stoichiometric in the appropriate pure phase or solid\n                       solution model (see the forum for a list of mineral phase\n                       end members). Trace element concentrations should be the\n                       bulk assimilant values rather than individual mineral\n                       ones. A single liquid composition can be input instead\n                       of, or in addition to, mineral compositions.\n                       Alternatively, multiple enrichment_files can be requested\n                       so that the assimilant bulk composition can be changed\n                       for each iteration. To use multiple enrichment_files in\n                       this way, see the ‘Table file’ section for the filename\n                       format. The program assumes that the indices are reset\n                       each time option 4 is called.\n                       You can enter the mass of assimilant to be added at each\n                       subsequent stage or, for melts_file(s) only, take the\n                       value(s) from the ‘Initial Mass:’ line(s). If the mass of\n                       assimilant is specified for separate mineral melts_files\n                       then the value entered is the total mass and the\n                       ‘Initial Mass:’ lines will be used to determine the\n                       proportions of the mineral phases. Major and, if\n                       appropriate, trace elements will be mixed (to mix trace\n                       elements only use ALPHAMELTS_FLUX_MELTING). If trace\n                       element calculations are switched on, the\n                       enrichment_file(s) must contain the same trace elements\n                       as the melts_file. For separate mineral files, the trace\n                       elements can be included in each mineral file, to avoid\n                       read errors, but only the vales from the first\n                       enrichment_file will be used. If running in isothermal\n                       mode, or the like, then the P, T and fO2 buffer from the\n                       assimilant file will be ignored and set to the current\n                       values, regardless of the input file type. For\n                       isenthalpic mode: please set ALPHAMELTS_DELTAP to zero,\n                       for reasons given in ‘Thermodynamic Path’, and\n                       ALPHAMELTS_DELTAT to zero so that the number of\n                       iterations can be controlled. We suggest you set\n                       ALPHAMELTS_SAVE_ALL so that you can gradually build up\n                       the number of iterations. In this mode, if you use a\n                       single text enrichment_file (or files) for the assimilant\n                       then the program will try to find a thermodynamically\n                       equilibrated state, using a superliquidus start. If you\n                       use separate mineral phase enrichment_files the\n                       enthalphy of each phase is calculated at temperature\n                       given in the first enrichment_file, without\n                       re-equilibration; this is similar to the GUI\n                       assimilation routines. If you use a binary assimilant\n                       file then it will use the previously calculated starting\n                       conditions but the pressure in the file must match the\n                       current pressure (or the temperatures must match for\n                       isochoric mode). If this is not the case an error message\n                       will be printed; either (a) redo the restart_file for the\n                       correct conditions or (b) use menu option 2 to set the\n                       current values to those used to generate the restart_file\n                       and then call option 4 again.')), 
 'FLUX_MELTING':mvar(set=False,
   type=bool,
   desc=description('This variable causes a user-defined proportion of a\n                         second composition, trace elements only, to be mixed\n                         in after each calculation stage (see ‘Bulk\n                         composition’). If used in conjunction with\n                         ALPHAMELTS_CONTINUOUS_MELTING and\n                         ALPHAMELTS_DO_TRACE_H2O it can simulate flux melting by\n                         a hydrous fluid (to simulate fluxing by a metasomatic\n                         melt use ALPHAMELTS_ASSIMILATE instead). We suggest you\n                         set ALPHAMELTS_SAVE_ALL so that you can gradually build\n                         up the number of iterations, e.g. until the system\n                         achieves steady state, by repeated calling of the\n                         ‘execute’ menu option. Execution is essentially the\n                         same as for ALPHAMELTS_ASSIMILATE but for trace\n                         elements only. As the mass of the enriching\n                         composition is not necessarily defined, the user is\n                         asked instead for the mass proportion of the new\n                         composition to add (similar to ‘Source Mixer’ in menu\n                         option 12). Alternatively, for melts_files(s), the\n                         ‘Initial Mass:’ lines may be used; in which case the\n                         old and new compositions are mixed in the ratio\n                         old_mass:new_mass. Note that, as major elements are not\n                         mixed, the total system mass (i.e. old_mass) will be\n                         unaffected.')), 
 'DRY_ITER_PATIENCE':mvar(default=100,
   type=int,
   validator=typecast(int, [lambda x: isinstance(x, int), lambda x: (x >= 0) & (x <= 100)]),
   desc=description('If simulating flux melting or assimilation,\n                              this is the maximum number of consecutive\n                              iterations that alphaMELTS will run without any\n                              melting occurring before it will give up and\n                              return to the menu.')), 
 'DO_TRACE':mvar(set=False,
   type=bool,
   desc=description('Implements attached trace element partitioning function\n                     for those elements listed in the melts_file.')), 
 'DO_TRACE_H2O':mvar(set=False,
   type=bool,
   desc=description('For the case where water is to be treated as a trace\n                         element this option adds an iteration on the H2O\n                         content, as described in Asimow, et al. [2004].')), 
 'HK_OL_TRACE_H2O':mvar(set=False,
   type=bool,
   desc=description('By default the Mosenfelder, et al. [2005] model\n                            for water solubility in olivine is used. This\n                            environment variable uses the Hirth and Kohlstedt\n                            [1996] model instead, which gives lower solubility\n                            and consequently lower partition coefficients.')), 
 'HK_PXGT_TRACE_H2O':mvar(default='mineral-melt',
   type=bool,
   validator=lambda x: x in ('mineral-melt', 'mineral-mineral'),
   desc=description('If the Mosenfelder, et al. [2005] model for\n                              water solubility in olivine is used then by\n                              default the mineral-melt partition coefficients\n                              for water with orthopyroxene, clinopyroxene and\n                              garnet are still those of Hirth and Kohlstedt\n                              [1996]. Setting this variable to ‘mineral-mineral’\n                              means the solubility of water in opx, cpx and\n                              garnet are linked to the newer water solubility\n                              in olivine model, which is equivalent to\n                              preserving the mineral-mineral water partition\n                              coefficients of Hirth and Kohlstedt [1996].\n                              Setting it to ‘mineral-melt’ retains the default\n                              behavior.')), 
 '2X_OPX_TRACE_H2O':mvar(set=False,
   type=bool,
   desc=description('By default the solubility of water in\n                             clinopyroxene is twice that in orthopyroxene,\n                             based on the results of Hirth and Kohlstedt [1996].\n                             If this variable is set then the solubility of\n                             water in opx is scaled up by to be equal to the\n                             cpx value, consistent with the observations of\n                             Hauri et al. [2006]. This option can be used\n                             regardless of whether the Mosenfelder, et al.\n                             [2005] or Hirth and Kohlstedt [1996] models are\n                             being used for olivine or opx, cpx and garnet. For\n                             example, if either ALPHAMELTS_HK_OL_TRACE_H2O or\n                             ALPHAMELTS_HK_PXGT_TRACE_H2O is set then the\n                             mineral-mineral partition coefficients will be\n                             those from Table 1 of Hirth and Kohlstedt [1996],\n                             except that olivine-opx value of 0.2 will be\n                             replaced by 0.1.')), 
 'TRACE_DEFAULT_DPTX':mvar(set=False,
   type=bool,
   desc=description('By default all partition coefficients used in\n                               trace element calculations are constant. If\n                               ALPHAMELTS_TRACE_VARIABLE_D is set then D =\n                               D(P,T,X) are calculated for elements and phases\n                               in Table 1. Constant partition coefficients will\n                               be used for all other elements / phases. This\n                               list may be modified in the trace_data_file, as\n                               previously explained.')), 
 'TS_TRACE_NORMALIZATION':mvar(set=False,
   type=int,
   validator=typecast(int, [lambda x: isinstance(x, int), lambda x: (x >= 1) & (x <= 4)]),
   desc=description("If set, this chooses one of four\n                                   compositions to normalize trace elements to\n                                   (if any):\n                                   1. PM Sun and McDonough [1989];\n                                   2. DMM Workman and Hart [2005];\n                                   3. PM McKenzie and O'Nions [1991; 1995];\n                                   4. DM of McKenzie and O'Nions [1991; 1995].\n                                   Sample input files showing concentrations for\n                                   each of the idealized source compositions\n                                   above are provided as illustrations; note\n                                   that some elements (i.e. Ni, Cr, and Mn)\n                                   appear as major and trace elements because\n                                   their inclusion in the liquid calibration\n                                   differs between MELTS and pMELTS. Isotopes\n                                   are normalized to the ‘non-isotope’ abundance\n                                   (see the ‘MELTS file’ section). This option\n                                   is useful if the source composition given in\n                                   the melts_file is different from the four\n                                   options above. If you wish to normalize to\n                                   the source in the melts_file the simplest\n                                   thing is to provide the list of elements with\n                                   ‘1.0’ for each of the abundances (except\n                                   isotopes).")), 
 'TRACE_INPUT_FILE':mvar(set=False,
   desc=description('Gives the name of the trace_data_file, which may\n                             be used to change partition coefficients, determine\n                             whether variable partition coefficients are\n                             calculated and with which parameters, as described\n                             above.')), 
 'TRACE_USELIQFEMG':mvar(set=False,
   type=bool,
   desc=description('By default the Mg# of the melt, needed to\n                             estimate D(P,T,X) for clinopyroxene, is estimated\n                             from the clinopyroxene composition using Equation\n                             35 from Wood and Blundy [1997]). If this\n                             environment variable is set then the Mg# of the\n                             melt is taken directly from the (pH)MELTS\n                             calculated liquid composition. If no liquid is\n                             present then the program will revert to the default\n                             behavior and use the clinopyroxene composition.')), 
 'ALPHAMELTS_ADIABAT_BIN_FILE':mvar(set=False,
   desc=description('Unavoidable changes within the\n                                        programs mean that binary restart_files\n                                        created with version 2.0+ of Adiabat_1ph\n                                        will not read into alphaMELTS. Once you\n                                        have read in the file, if you\n                                        immediately save it again it will be\n                                        updated to Adiabat_1ph 3.0 format.\n                                        Adiabat_1ph 3.0 format is compatible\n                                        with alphaMELTS 1.0+ so unset this\n                                        environment variable for subsequent\n                                        runs. For more details see\n                                        ADIABAT_V20_BIN_FILE in the\n                                        Adiabat_1ph 3 documentation.')), 
 'CELSIUS_OUTPUT':mvar(set=False,
   type=bool,
   desc=description('By default, temperature input to alphaMELTS is in\n                           °C, whereas temperature output is in Kelvin. When\n                           this environment variable is set, text file and\n                           screen output is also in °C.')), 
 'SAVE_ALL':mvar(set=False,
   type=bool,
   desc=description('By default, the main output file is only written for\n                     calculations made in the most recent call to menu option 4.\n                     If this variable is set then results from all calculations\n                     are saved and output. This provides a simple way to record\n                     single calculations (menu option 3) or to build up results\n                     from multiple iterations or multiple melts_files. Note that\n                     even if the appropriate environment variables are set, no\n                     solid or liquid fractionation will occur until menu option\n                     4 is run. If using ‘Amoeba’ (menu option 17) the\n                     ALPHAMELTS_SAVE_ALL function will be temporarily switched\n                     off (so that iterations of the search algorithm are not\n                     saved); when it is finished a single calculation (menu\n                     option 3) may be used to write output for the best-fit\n                     parental melt.')), 
 'SKIP_FAILURE':mvar(set=False,
   type=bool,
   desc=description('Normally failure of the minimization routines means\n                         that the alphamelts executable must be restarted to\n                         clear the memory. If this environment variable is set\n                         then a copy of the thermodynamic state is made each\n                         time a successful calculation is made. If the next\n                         calculation fails, this last good state (or the bulk\n                         composition and starting conditions from the\n                         melts_file, if it is the first calculation) is used\n                         for subsequent attempts. This may be useful if you are\n                         very close to a reaction when the algorithms may have\n                         trouble deciding whether to add a phase to the\n                         assemblage and need to overstep just slightly. It is\n                         also helpful when trying out starting solutions using\n                         options 2 and 3. If ALPHAMELTS_SAVE_ALL is also set,\n                         the last good state will also be written to the output\n                         files as a placeholder; it should be obvious that this\n                         represents a skipped failure as all values, including\n                         pressure and temperature, will be identical to the\n                         previous output..')), 
 'FAILED_ITER_PATIENCE':mvar(default=10,
   type=int,
   validator=typecast(int, [lambda x: isinstance(x, int), lambda x: (x >= 0) & (x <= 10)]),
   desc=description('If the minimization routines do not recover\n                                 in the next few iterations then one drawback of\n                                 ALPHAMELTS_SKIP_FAILURE is that it can lead to\n                                 infinite loops of failure or, if triggered\n                                 repeatedly, eventually to a segmentation fault.\n                                 If ALPHAMELTS_SKIP_FAILURE is set, this\n                                 variable is the maximum number of consecutive\n                                 failed iterations that alphaMELTS will run\n                                 before a clean return to the menu where\n                                 parameters, such as the choice of fO2 buffer,\n                                 can be adjusted or alphaMELTS completely\n                                 restarted. If running in PTgrid or TPgrid\n                                 modes, it will be the maximum number of failed\n                                 iterations before alpahMELTS moves to the next\n                                 internal loop (T-loop or P-loop\n                                 respectively).')), 
 'INTEGRATE_FILE':mvar(set=False,
   type=bool,
   desc=description('Normally the integrated_output_file can be written\n                           immediately after execution finishes, but if\n                           alphamelts tends to crash before the menu option 16\n                           can be called then memory contents will be lost. As a\n                           precaution, ALPHAMELTS_INTEGRATE_FILE should be set\n                           to record details of the packets of melt extracted\n                           during melting to a file. If run_alphamelts.command\n                           is restarted with the same settings and menu option\n                           16 is called before execution then the resulting file\n                           will be used as input for the melt integration. Note\n                           that ALPHAMELTS_INTEGRATE_FILE is not the\n                           integrated_output_file itself but an intermediate\n                           file that may be used in its generation.')), 
 'LATENT_HEAT':mvar(set=False,
   type=bool,
   desc=description('Normally text file output is done just after\n                        equilibration and before any fractionation. If\n                        ALPHAMELTS_LATENT_HEAT to set to ‘true’ alphamelts will\n                        also output the state just after fractionation and just\n                        before the next equilibration (when the temperature has\n                        been lowered and the system cooled but not allowed to\n                        crystallise any more yet). This gives a simple way to\n                        calculate the latent heat of crystallization, without\n                        having to do the cooling adjustment described in Ghiorso\n                        [1997]. Note that, for the same MORB composition, the\n                        results will differ from Figure 5 of Ghiorso [1997].\n                        This apparent discrepancy is due to changes in the MELTS\n                        software since it was first released and not to\n                        differences in how the variation in latent heat is\n                        accessed.')), 
 'QUICK_OUTPUT':mvar(set=False,
   type=bool,
   desc=description('If this environment variable is set then\n                         equilibrated thermodynamic states from previous\n                         calculations are not saved, except as required for\n                         ALPHAMELTS_SKIP_FAILURE etc. For calculations\n                         comprising a large number of iterations, such as those\n                         on a closely spaced P-T grid, setting this variable can\n                         significantly reduce memory usage and therefore\n                         increase computational speed as the calculation\n                         proceeds. Reporting of fO2 will be affected slightly.\n                         The Phase_mass_tbl.txt and Phase_vol_tbl.txt files will\n                         not be written, which will cause\n                         run_alphamelts.command to issue a warning about not\n                         being able to find these files; the warning can be\n                         safely ignored.')), 
 'MULTIPLE_LIQUIDS':mvar(set=False,
   type=bool,
   desc=description('This turns on exsolution of immiscible liquids. The\n                             solvi are not very well determined, and we do not\n                             recommend serious use of this feature, but in some\n                             cases operation inside an unrecognized two-liquid field\n                             can lead to path-dependent non-unique equilibria. This\n                             option should not be used if trace element calculations\n                             are enabled.')), 
 'FRACTIONATE_SECOND_LIQUID':mvar(set=False,
   type=bool,
   desc=description('When running with\n                                      ALPHAMELTS_MULTIPLE_LIQUIDS set, treat all\n                                      liquids except the first as fractionating\n                                      phases and remove them from the system\n                                      after each equilibration.')), 
 'FOCUS':mvar(set=False,
   type=bool,
   desc=description('Option to do the focusing calculation described in Asimow\n                  and Stolper [1999]. It works by multiplying the mass of liquid\n                  in system by a fixed factor after each equilibration.')), 
 'FOCUS_FACTOR':mvar(set=False,
   type=float,
   validator=typecast(float, numeric_validator),
   desc=description('When ALPHAMELTS_FOCUS is set, this determines the\n                         multiplication factor for the mass of liquid. Usually\n                         it will be a number slightly greater than unity, like\n                         the 100th root of 2. If ALPHAMELTS_FOCUS is set without\n                         a value in ALPHAMELTS_FOCUS_FACTOR the focusing\n                         calculation loop will be ignored.')), 
 'INTEGRATE_PHI':mvar(set=False,
   type=bool,
   desc=description('Normally, packets of extracted melt are saved in\n                          memory (and, optionally, written out to the\n                          ALPHAMELTS_INTEGRATE_FILE ‘crash’ file, described\n                          above) by mass i.e. in terms of dF. If this variable\n                          is set then the packets of extracted melt will be\n                          saved by volume i.e. in terms of dPhi. As the full\n                          pressure integral (calculation of crustal thickness\n                          etc.) is not strictly correct for increments in Phi,\n                          that option will not be offered. However, the\n                          opportunity to interpolate for equal increments of\n                          melt fraction by volume will be available.'))}