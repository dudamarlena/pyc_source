# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python3.6/dist-packages/pyxrd/project/importing.py
# Compiled at: 2020-03-07 03:51:50
# Size of source mod 2**32: 8389 bytes
import os, string, numpy as np, xml.etree.ElementTree as ET
from pyxrd.mixture.models import Mixture
from pyxrd.project.models import Project
from pyxrd.specimen.models import Specimen
from pyxrd.phases.models import Phase
from pyxrd.atoms.models import Atom

def safe_float(num):
    return float(num.replace(',', '.'))


def create_project_from_sybilla_xml(filename, **kwargs):
    """
        Creates a new project structure from a Sybilla XML file.
        Some information (e.g. the actual XRD pattern) is not present and will
        still need to be imported manually.
    """
    tree = ET.parse(filename)
    root = tree.getroot()
    basename = os.path.basename(filename)
    if 'name' in kwargs:
        kwargs.pop('name')
    if 'layout_mode' in kwargs:
        kwargs.pop('layout_mode')
    project = Project(name=basename, layout_mode='FULL', **kwargs)
    specimen = Specimen(name=basename, parent=project)
    project.specimens.append(specimen)
    mixture = Mixture(name=basename, auto_run=False, parent=project)
    mixture.add_specimen_slot(specimen, 1.0, 0.0)
    project.mixtures.append(mixture)
    with project.data_changed.ignore():
        with mixture.data_changed.ignore():
            for child in root:
                if child.tag == 'basic_params':
                    step_size = safe_float(child.attrib['step_size'])
                    wavelength = safe_float(child.attrib['lambda']) / 10.0
                    steps = int(1 + (specimen.goniometer.max_2theta - specimen.goniometer.min_2theta) / step_size)
                    specimen.goniometer.min_2theta = safe_float(child.attrib['min2theta'])
                    specimen.goniometer.max_2theta = safe_float(child.attrib['max2theta'])
                    specimen.goniometer.steps = steps
                    specimen.goniometer.wavelength = wavelength
                else:
                    if child.tag == 'diffractometer':
                        specimen.goniometer.radius = safe_float(child.attrib['gonio_radius'])
                        specimen.goniometer.divergence = safe_float(child.attrib['diverg_slit'])
                        specimen.goniometer.soller1 = safe_float(child.attrib['Soller1'])
                        specimen.goniometer.soller2 = safe_float(child.attrib['Soller2'])
                        specimen.sample_length = safe_float(child.attrib['sample_length'])
                    else:
                        if child.tag == 'content':
                            for xmlPhaseContent in child:
                                name = xmlPhaseContent.attrib['name']
                                fraction = safe_float(xmlPhaseContent.attrib['content']) / 100.0
                                mixture.add_phase_slot(name, fraction)

                        else:
                            if child.tag == 'mixture':
                                for xmlPhase in child:
                                    name = xmlPhase.attrib['name']
                                    sigma = xmlPhase.attrib['sigma_star']
                                    csds = safe_float(xmlPhase.find('distribution').attrib['Tmean'])
                                    G = 1
                                    R = 0
                                    W = [1.0]
                                    if xmlPhase.attrib['type'] != 'mono':
                                        prob = xmlPhase.find('probability')
                                        G = int(prob.attrib['no_of_comp'])
                                        R = int(prob.attrib['R'])
                                    phase = Phase(name=name, sigma_star=sigma, G=G, R=R, parent=project)
                                    phase.CSDS_distribution.average = csds
                                    project.phases.append(phase)
                                    if R == 0:
                                        if G != 1:
                                            xmlW = prob.find('W')
                                            W = np.array([float(int(safe_float(xmlW.attrib[string.ascii_lowercase[i]]) * 1000.0)) / 1000.0 for i in range(G)])
                                            for i in range(G - 1):
                                                setattr(phase.probabilities, 'F%d' % (i + 1), W[i] / np.sum(W[i:]))

                                    if R == 1:
                                        if G == 2:
                                            pass
                                    for i, layer in enumerate(xmlPhase.findall('./layer_and_edge/layer')):
                                        component = phase.components[i]
                                        component.name = layer.attrib['name']
                                        component.d001 = safe_float(layer.attrib['d_spacing']) / 10.0
                                        component.default_c = safe_float(layer.attrib['d_spacing']) / 10.0
                                        component.delta_c = safe_float(layer.attrib['d_spacing_delta']) / 10.0
                                        component.ucp_b.value = 0.9
                                        component.ucp_a.factor = 0.57735
                                        component.ucp_a.prop = (component, 'cell_b')
                                        component.ucp_a.enabled = True
                                        atom_type_map = {'K':'K1+', 
                                         'O':'O1-', 
                                         'Si':'Si2+', 
                                         'OH':'OH1-', 
                                         'Fe':'Fe1.5+', 
                                         'Al':'Al1.5+', 
                                         'Mg':'Mg1+', 
                                         'H2O':'H2O', 
                                         'Gly':'Glycol', 
                                         'Ca':'Ca2+', 
                                         'Na':'Na1+'}
                                        fe_atom = None
                                        encountered_oxygen = False
                                        for atom in layer.findall('atom'):
                                            atom_type_name = atom_type_map.get(atom.attrib['type'], None)
                                            if atom_type_name:
                                                if atom_type_name == 'O1-':
                                                    encountered_oxygen = True
                                                else:
                                                    atom = Atom(name=(atom.attrib['type']),
                                                      default_z=(safe_float(atom.attrib['position']) / 10.0),
                                                      pn=(safe_float(atom.attrib['content'])),
                                                      atom_type_name=atom_type_name,
                                                      parent=component)
                                                    if encountered_oxygen:
                                                        component.layer_atoms.append(atom)
                                                    else:
                                                        component.interlayer_atoms.append(atom)
                                                atom.resolve_json_references()
                                                if encountered_oxygen and atom_type_name == 'Fe1.5+':
                                                    fe_atom = atom

                                        if fe_atom is not None:
                                            component.ucp_b.constant = 0.9
                                            component.ucp_b.factor = 0.0043
                                            component.ucp_b.prop = (fe_atom, 'pn')
                                            component.ucp_b.enabled = True

            for phase in project.phases:
                for slot, phase_name in enumerate(mixture.phases):
                    if phase.name == phase_name:
                        mixture.set_phase(0, slot, phase)

    return project