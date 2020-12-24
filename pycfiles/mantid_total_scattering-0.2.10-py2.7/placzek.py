# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/total_scattering/inelastic/placzek.py
# Compiled at: 2019-10-03 13:30:51
import sys, json, collections, numpy as np, scipy
from mantid import mtd
from mantid.simpleapi import CreateWorkspace, Load, SetSampleMaterial
from total_scattering.inelastic.incident_spectrum import FitIncidentSpectrum, GetIncidentSpectrumFromMonitor

def plotPlaczek(x, y, fit, fit_prime, title=None):
    plt.plot(x, y, 'bo', x, fit, '--')
    plt.legend(['Incident Spectrum', 'Fit f(x)'], loc='best')
    if title is not None:
        plt.title(title)
    plt.show()
    plt.plot(x, x * fit_prime / fit, 'x--', label="Fit x*f'(x)/f(x)")
    plt.xlabel('Wavelength')
    plt.legend()
    if title is not None:
        plt.title(title)
    plt.show()
    return


def GetLogBinning(start, stop, num=100):
    return np.logspace(np.log(start), np.log(stop), num=num, endpoint=True, base=np.exp(1))


def ConvertLambdaToQ(lam, angle):
    angle_conv = np.pi / 180.0
    sin_theta_by_2 = np.sin(angle * angle_conv / 2.0)
    q = 4.0 * np.pi / lam * sin_theta_by_2
    return q


def ConvertQToLambda(q, angle):
    angle_conv = np.pi / 180.0
    sin_theta_by_2 = np.sin(angle * angle_conv / 2.0)
    lam = 4.0 * np.pi / q * sin_theta_by_2
    return lam


def GetSampleSpeciesInfo(InputWorkspace):
    total_stoich = 0.0
    material = mtd[InputWorkspace].sample().getMaterial().chemicalFormula()
    atom_species = collections.OrderedDict()
    for atom, stoich in zip(material[0], material[1]):
        print atom.neutron()['tot_scatt_length']
        b_sqrd_bar = mtd[InputWorkspace].sample().getMaterial().totalScatterXSection() / (4.0 * np.pi)
        atom_species[atom.symbol] = {'mass': atom.mass, 'stoich': stoich, 
           'b_sqrd_bar': b_sqrd_bar}
        total_stoich += stoich

    for atom, props in atom_species.items():
        props['concentration'] = props['stoich'] / total_stoich

    return atom_species


def CalculateElasticSelfScattering(InputWorkspace):
    atom_species = GetSampleSpeciesInfo(InputWorkspace)
    elastic_self_term = 0.0
    for species, props in atom_species.items():
        elastic_self_term += props['concentration'] * props['b_sqrd_bar']

    return elastic_self_term


def CalculatePlaczekSelfScattering(IncidentWorkspace, OutputWorkspace, L1, L2, Polar, Azimuthal=None, Detector=None, ParentWorkspace=None):
    factor = 1.0 / scipy.constants.physical_constants['atomic mass unit-kilogram relationship'][0]
    neutron_mass = factor * scipy.constants.m_n
    atom_species = GetSampleSpeciesInfo(IncidentWorkspace)
    summation_term = 0.0
    for species, props in atom_species.items():
        summation_term += props['concentration'] * props['b_sqrd_bar'] * neutron_mass / props['mass']

    incident_index = 0
    incident_prime_index = 1
    x_lambda = mtd[IncidentWorkspace].readX(incident_index)
    incident = mtd[IncidentWorkspace].readY(incident_index)
    incident_prime = mtd[IncidentWorkspace].readY(incident_prime_index)
    phi_1 = x_lambda * incident_prime / incident
    if Detector is None:
        Detector = {'Alpha': None, 'LambdaD': 1.44, 'Law': '1/v'}
    if Detector['Alpha'] is None:
        Detector['Alpha'] = 2.0 * np.pi / Detector['LambdaD']
    if Detector['Law'] == '1/v':
        c = -Detector['Alpha'] / (2.0 * np.pi)
        x = x_lambda
        detector_law_term = c * x * np.exp(c * x) / (1.0 - np.exp(c * x))
    eps_1 = detector_law_term
    if Azimuthal is None:
        Azimuthal = np.zeros(len(Polar))
    x_lambdas = np.array([])
    placzek_correction = np.array([])
    for bank, (l2, theta, phi) in enumerate(zip(L2, Polar, Azimuthal)):
        L_total = L1 + l2
        f = L1 / L_total
        angle_conv = np.pi / 180.0
        sin_theta_by_2 = np.sin(theta * angle_conv / 2.0)
        term1 = (f - 1.0) * phi_1
        term2 = f * eps_1
        term3 = f - 3.0
        inelastic_placzek_self_correction = 2.0 * (term1 - term2 + term3) * sin_theta_by_2 * sin_theta_by_2 * summation_term
        x_lambdas = np.append(x_lambdas, x_lambda)
        placzek_correction = np.append(placzek_correction, inelastic_placzek_self_correction)

    if ParentWorkspace:
        CreateWorkspace(DataX=x_lambdas, DataY=placzek_correction, OutputWorkspace=OutputWorkspace, UnitX='Wavelength', NSpec=len(Polar), ParentWorkspace=ParentWorkspace, Distribution=True)
    else:
        CreateWorkspace(DataX=x_lambdas, DataY=placzek_correction, OutputWorkspace=OutputWorkspace, UnitX='Wavelength', NSpec=len(Polar), Distribution=True)
    print (
     'Placzek YUnit:', mtd[OutputWorkspace].YUnit())
    print ('Placzek distribution:', mtd[OutputWorkspace].isDistribution())
    return mtd[OutputWorkspace]


if '__main__' == __name__:
    configfile = sys.argv[1]
    with open(configfile) as (handle):
        config = json.loads(handle.read())
    sample = config['Sample']
    opts = sample['InelasticCorrection']
    runs = sample['Runs'].split(',')
    runs = [ '%s_%s' % (config['Instrument'], run) for run in runs ]
    print ('Processing Scan: ', runs[0])
    incident_ws = 'incident_ws'
    GetIncidentSpectrumFromMonitor(runs[0], OutputWorkspace=incident_ws)
    incident_fit = 'incident_fit'
    fit_type = opts['FitSpectrumWith']
    FitIncidentSpectrum(InputWorkspace=incident_ws, OutputWorkspace=incident_fit, FitSpectrumWith=fit_type, BinningForFit=opts['LambdaBinningForFit'], BinningForCalc=opts['LambdaBinningForCalc'], PlotDiagnostics=opts['PlotFittingDiagnostics'])
    SetSampleMaterial(incident_fit, ChemicalFormula=str(sample['Material']))
    CalculateElasticSelfScattering(InputWorkspace=incident_fit)
    atom_species = GetSampleSpeciesInfo(incident_fit)
    L1 = 19.5
    banks = collections.OrderedDict()
    banks[0] = {'L2': 2.01, 'theta': 15.1}
    banks[1] = {'L2': 1.68, 'theta': 31.0}
    banks[2] = {'L2': 1.14, 'theta': 65.0}
    banks[3] = {'L2': 1.11, 'theta': 120.4}
    banks[4] = {'L2': 0.79, 'theta': 150.1}
    banks[5] = {'L2': 2.06, 'theta': 8.6}
    L2 = [ x['L2'] for bank, x in banks.iteritems() ]
    Polar = [ x['theta'] for bank, x in banks.iteritems() ]
    parent = 'parent_ws'
    placzek = 'placzek_out'
    Load(Filename=runs[0], OutputWorkspace=parent)
    CalculatePlaczekSelfScattering(IncidentWorkspace=incident_fit, OutputWorkspace=placzek, L1=19.5, L2=L2, Polar=Polar, ParentWorkspace=parent)
    plot = True
    if plot:
        import matplotlib.pyplot as plt
        bank_colors = [
         'k', 'r', 'b', 'g', 'y', 'c']
        nbanks = range(mtd[placzek].getNumberHistograms())
        for bank, theta in zip(nbanks, Polar):
            x_lambda = mtd[placzek].readX(bank)
            q = ConvertLambdaToQ(x_lambda, theta)
            per_bank_placzek = mtd[placzek].readY(bank)
            label = 'Bank: %d at Theta %d' % (bank, int(theta))
            plt.plot(q, 1.0 + per_bank_placzek, bank_colors[bank] + '-', label=label)

        material = (' ').join([ symbol + str(int(props['stoich'])) + ' ' for symbol, props in atom_species.iteritems()
                              ])
        plt.title('Placzek vs. Q for ' + material)
        plt.xlabel('Q (Angstroms^-1')
        plt.ylabel('1 - P(Q)')
        axes = plt.gca()
        plt.legend()
        plt.show()