# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/mkoenig/git/sbmlutils/sbmlutils/dfba/toy_wholecell/model_factory.py
# Compiled at: 2019-10-27 06:58:29
# Size of source mod 2**32: 16840 bytes
"""
This module creates the sub-models and combined comp model for the toy model.

The toy model consists hereby of
- a FBA submodels
- deterministic ODE models
- and stochastic ODE models

The SBML comp extension is used for hierarchical model composition, i.e. to create
the main model and the kinetic model parts.
"""
import os
from os.path import join as pjoin
import libsbml
from libsbml import UNIT_KIND_SECOND, UNIT_KIND_METRE, UNIT_KIND_ITEM, UNIT_KIND_KILOGRAM, UNIT_KIND_MOLE
from sbmlutils import comp
from sbmlutils import fbc
from sbmlutils import sbmlio
from sbmlutils import factory as mc
from sbmlutils.report import sbmlreport
from sbmlutils.annotation import annotator
from sbmlutils.dfba import builder
from sbmlutils.dfba import utils
from sbmlutils.dfba.toy_wholecell import settings
libsbml.XMLOutputStream.setWriteTimestamp(False)
DT_SIM = 0.1
notes = '\n    <body xmlns=\'http://www.w3.org/1999/xhtml\'>\n    <h1>Wholecell Toy Model</h1>\n    <p><strong>Model version: {}</strong></p>\n\n    {}\n\n    <h2>Description</h2>\n    <p>This is a toy model for coupling models with different modeling frameworks via comp.</p>\n\n    <div class="dc:publisher">This file has been produced by\n      <a href="https://livermetabolism.com/contact.html" title="Matthias Koenig" target="_blank">Matthias Koenig</a>.\n      </div>\n\n    <h2>Terms of use</h2>\n      <div class="dc:rightsHolder">Copyright © 2017 Matthias Koenig</div>\n      <div class="dc:license">\n      <p>Redistribution and use of any part of this model, with or without modification, are permitted provided that\n      the following conditions are met:\n        <ol>\n          <li>Redistributions of this SBML file must retain the above copyright notice, this list of conditions\n              and the following disclaimer.</li>\n          <li>Redistributions in a different form must reproduce the above copyright notice, this list of\n              conditions and the following disclaimer in the documentation and/or other materials provided\n          with the distribution.</li>\n        </ol>\n        This model is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even\n             the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.</p>\n      </div>\n    </body>\n'.format(settings.VERSION, '{}')
creators = [
 mc.Creator(familyName='Koenig', givenName='Matthias', email='konigmatt@googlemail.com', organization='Humboldt University Berlin',
   site='http://livermetabolism.com')]
main_units = {'time':'s', 
 'extent':UNIT_KIND_ITEM, 
 'substance':UNIT_KIND_ITEM, 
 'length':'m', 
 'area':'m2', 
 'volume':'m3'}
units = [
 mc.Unit('s', [(UNIT_KIND_SECOND, 1.0)], name='second'),
 mc.Unit('kg', [(UNIT_KIND_KILOGRAM, 1.0)], name='kilogram'),
 mc.Unit('m', [(UNIT_KIND_METRE, 1.0)], name='meter'),
 mc.Unit('m2', [(UNIT_KIND_METRE, 2.0)], name='square meter'),
 mc.Unit('m3', [(UNIT_KIND_METRE, 3.0)], name='cubic meter'),
 mc.Unit('mM', [(UNIT_KIND_MOLE, 1.0, 0),
  (
   UNIT_KIND_METRE, -3.0)],
   name='millimolar'),
 mc.Unit('per_s', [(UNIT_KIND_SECOND, -1.0)]),
 mc.Unit('item_per_s', [(UNIT_KIND_ITEM, 1.0),
  (
   UNIT_KIND_SECOND, -1.0)]),
 mc.Unit('item_per_m3', [(UNIT_KIND_ITEM, 1.0),
  (
   UNIT_KIND_METRE, -3.0)])]
UNIT_TIME = 's'
UNIT_AMOUNT = str(UNIT_KIND_ITEM)
UNIT_AREA = 'm2'
UNIT_VOLUME = 'm3'
UNIT_CONCENTRATION = 'item_per_m3'
UNIT_FLUX = 'item_per_s'

def fba_model(sbml_file, directory, annotations=None):
    """ FBA model
    
    :param sbml_file: output file name 
    :param directory: output directory
    :return: SBMLDocument
    """
    fba_notes = notes.format('\n    <h2>FBA submodel</h2>\n    <p>DFBA fba submodel. Unbalanced metabolites are encoded via exchange fluxes.</p>\n    ')
    doc = builder.template_doc_fba(settings.MODEL_ID)
    model = doc.getModel()
    utils.set_model_info(model, notes=fba_notes,
      creators=creators,
      units=units,
      main_units=main_units)
    objects = [
     mc.Compartment(sid='extern', value=1.0, unit=UNIT_VOLUME, constant=True, name='external compartment', spatialDimensions=3),
     mc.Compartment(sid='cell', value=1.0, unit=UNIT_VOLUME, constant=True, name='cell', spatialDimensions=3),
     mc.Compartment(sid='membrane', value=1.0, unit=UNIT_AREA, constant=True, name='membrane', spatialDimensions=2),
     mc.Species(sid='A', name='A', initialConcentration=0, substanceUnit=UNIT_AMOUNT, hasOnlySubstanceUnits=True, compartment='extern'),
     mc.Species(sid='C', name='C', initialConcentration=0, substanceUnit=UNIT_AMOUNT, hasOnlySubstanceUnits=True, compartment='extern'),
     mc.Species(sid='B1', name='B1', initialConcentration=0, substanceUnit=UNIT_AMOUNT, hasOnlySubstanceUnits=True, compartment='cell'),
     mc.Species(sid='B2', name='B2', initialConcentration=0, substanceUnit=UNIT_AMOUNT, hasOnlySubstanceUnits=True, compartment='cell'),
     mc.Parameter(sid='ub_R1', value=1.0, unit=UNIT_FLUX, constant=True, sboTerm=(builder.FLUX_BOUND_SBO)),
     mc.Parameter(sid='zero', value=0.0, unit=UNIT_FLUX, constant=True, sboTerm=(builder.FLUX_BOUND_SBO)),
     mc.Parameter(sid='ub_default', value=(builder.UPPER_BOUND_DEFAULT), unit=UNIT_FLUX, constant=True, sboTerm=(builder.FLUX_BOUND_SBO))]
    mc.create_objects(model, objects)
    r1 = mc.create_reaction(model, rid='R1', name='A import (R1)', fast=False, reversible=True, reactants={'A': 1},
      products={'B1': 1},
      compartment='membrane')
    r2 = mc.create_reaction(model, rid='R2', name='B1 <-> B2 (R2)', fast=False, reversible=True, reactants={'B1': 1},
      products={'B2': 1},
      compartment='cell')
    r3 = mc.create_reaction(model, rid='R3', name='B2 export (R3)', fast=False, reversible=True, reactants={'B2': 1},
      products={'C': 1},
      compartment='membrane')
    fbc.set_flux_bounds(r1, lb='zero', ub='ub_R1')
    fbc.set_flux_bounds(r2, lb='zero', ub='ub_default')
    fbc.set_flux_bounds(r3, lb='zero', ub='ub_default')
    builder.create_exchange_reaction(model, species_id='A', flux_unit=UNIT_FLUX)
    builder.create_exchange_reaction(model, species_id='C', flux_unit=UNIT_FLUX)
    model_fbc = model.getPlugin('fbc')
    fbc.create_objective(model_fbc, oid='R3_maximize', otype='maximize', fluxObjectives={'R3': 1.0},
      active=True)
    comp.create_ports(model, portType=(comp.PORT_TYPE_PORT), idRefs=[
     'ub_R1'])
    if annotations:
        annotator.annotate_sbml_doc(doc, annotations)
    sbmlio.write_sbml(doc, filepath=(os.path.join(directory, sbml_file)), validate=True)
    return doc


def bounds_model(sbml_file, directory, doc_fba, annotations=None):
    """"
    Bounds model.
    """
    bounds_notes = notes.format('\n    <h2>BOUNDS submodel</h2>\n    <p>Submodel for dynamically calculating the flux bounds.\n    The dynamically changing flux bounds are the input to the\n    FBA model.</p>\n    ')
    doc = builder.template_doc_bounds(settings.MODEL_ID)
    model = doc.getModel()
    utils.set_model_info(model, notes=bounds_notes,
      creators=creators,
      units=units,
      main_units=main_units)
    builder.create_dfba_dt(model, step_size=DT_SIM, time_unit=UNIT_TIME, create_port=True)
    compartment_id = 'extern'
    builder.create_dfba_compartment(model, compartment_id=compartment_id, unit_volume=UNIT_VOLUME, create_port=True)
    model_fba = doc_fba.getModel()
    builder.create_dfba_species(model, model_fba, compartment_id=compartment_id, unit_amount=UNIT_AMOUNT, hasOnlySubstanceUnits=True,
      create_port=True)
    builder.create_exchange_bounds(model, model_fba=model_fba, unit_flux=UNIT_FLUX, create_ports=True)
    objects = [
     mc.Parameter(sid='lb_default', value=(builder.LOWER_BOUND_DEFAULT), unit=UNIT_FLUX, constant=True),
     mc.Parameter(sid='ub_R1', value=1.0, unit=UNIT_FLUX, constant=False, sboTerm='SBO:0000625'),
     mc.Parameter(sid='k1', value=(-0.2), unit='per_s', name='k1', constant=False),
     mc.RateRule(sid='ub_R1', value='k1*ub_R1'),
     mc.AssignmentRule(sid='lb_EX_A', value='max(lb_default, -A/dt)'),
     mc.AssignmentRule(sid='lb_EX_C', value='max(lb_default, -C/dt)')]
    mc.create_objects(model, objects)
    comp.create_ports(model, portType=(comp.PORT_TYPE_PORT), idRefs=[
     'ub_R1'])
    if annotations:
        annotator.annotate_sbml_doc(doc, annotations)
    sbmlio.write_sbml(doc, filepath=(os.path.join(directory, sbml_file)), validate=True)


def update_model(sbml_file, directory, doc_fba=None, annotations=None):
    """ Update model.
    """
    update_notes = notes.format('\n        <h2>UPDATE submodel</h2>\n        <p>Submodel for dynamically updating the metabolite count.\n        This updates the ode model based on the FBA fluxes.</p>\n        ')
    doc = builder.template_doc_update(settings.MODEL_ID)
    model = doc.getModel()
    utils.set_model_info(model, notes=update_notes,
      creators=creators,
      units=units,
      main_units=main_units)
    compartment_id = 'extern'
    builder.create_dfba_compartment(model, compartment_id=compartment_id, unit_volume=UNIT_VOLUME, create_port=True)
    model_fba = doc_fba.getModel()
    builder.create_dfba_species(model, model_fba, compartment_id=compartment_id, unit_amount=UNIT_AMOUNT, hasOnlySubstanceUnits=True,
      create_port=True)
    builder.create_update_reactions(model, model_fba=model_fba, formula='-{}', unit_flux=UNIT_FLUX, modifiers=[])
    if annotations:
        annotator.annotate_sbml_doc(doc, annotations)
    sbmlio.write_sbml(doc, filepath=(os.path.join(directory, sbml_file)), validate=True)


def top_model(sbml_file, directory, emds, doc_fba, annotations=None):
    """ Create top comp model.

    Creates full comp model by combining fba, update and bounds
    model with additional kinetics in the top model.
    """
    top_notes = notes.format('\n        <h2>TOP model</h2>\n        <p>Main comp DFBA model by combining fba, update and bounds\n            model with additional kinetics in the top model.</p>\n        ')
    working_dir = os.getcwd()
    os.chdir(directory)
    doc = builder.template_doc_top(settings.MODEL_ID, emds)
    model = doc.getModel()
    utils.set_model_info(model, notes=top_notes,
      creators=creators,
      units=units,
      main_units=main_units)
    builder.create_dfba_dt(model, step_size=DT_SIM, time_unit=UNIT_TIME, create_port=False)
    compartment_id = 'extern'
    builder.create_dfba_compartment(model, compartment_id=compartment_id, unit_volume=UNIT_VOLUME, create_port=False)
    model_fba = doc_fba.getModel()
    builder.create_dfba_species(model, model_fba, compartment_id=compartment_id, hasOnlySubstanceUnits=True, unit_amount=UNIT_AMOUNT,
      create_port=False)
    builder.create_dummy_species(model, compartment_id=compartment_id, hasOnlySubstanceUnits=True, unit_amount=UNIT_AMOUNT)
    builder.create_exchange_bounds(model, model_fba=model_fba, unit_flux=UNIT_FLUX, create_ports=False)
    builder.create_dummy_reactions(model, model_fba=model_fba, unit_flux=UNIT_FLUX)
    builder.create_top_replacedBy(model, model_fba=model_fba)
    builder.create_top_replacements(model, model_fba, compartment_id=compartment_id)
    initial_c = {'A':10.0, 
     'C':0.0}
    for sid, value in initial_c.items():
        species = model.getSpecies(sid)
        species.setInitialConcentration(value)

    mc.create_objects(model, [
     mc.Species(sid='D', initialConcentration=0, substanceUnit=UNIT_AMOUNT, hasOnlySubstanceUnits=True,
       compartment='extern'),
     mc.Parameter(sid='k_R4', value=0.1, constant=True, unit='per_s', sboTerm='SBO:0000009'),
     mc.Parameter(sid='ub_R1', value=1.0, unit=UNIT_FLUX, constant=False, sboTerm='SBO:0000625')])
    mc.create_reaction(model, rid='R4', name='R4: C -> D', fast=False, reversible=False, reactants={'C': 1},
      products={'D': 1},
      formula='k_R4*C',
      compartment='extern')
    comp.replace_elements(model, 'ub_R1', ref_type=(comp.SBASE_REF_TYPE_PORT), replaced_elements={'bounds':[
      'ub_R1_port'], 
     'fba':[
      'ub_R1_port']})
    if annotations:
        annotator.annotate_sbml_doc(doc, annotations)
    sbmlio.write_sbml(doc, filepath=(os.path.join(directory, sbml_file)), validate=True)
    os.chdir(working_dir)


def create_model(output_dir):
    """ Create all submodels and comp model.

    :param output_dir: results directory
    :rtype:
    :return directory in which model files exist.
    """
    directory = utils.versioned_directory(output_dir, version=(settings.VERSION))
    f_annotations = os.path.join(os.path.dirname(os.path.abspath(__file__)), settings.ANNOTATIONS_LOCATION)
    annotations = annotator.ModelAnnotator.read_annotations(f_annotations)
    doc_fba = fba_model((settings.FBA_LOCATION), directory, annotations=annotations)
    bounds_model((settings.BOUNDS_LOCATION), directory, doc_fba=doc_fba, annotations=annotations)
    update_model((settings.UPDATE_LOCATION), directory, doc_fba=doc_fba, annotations=annotations)
    emds = {'{}_fba'.format(settings.MODEL_ID): settings.FBA_LOCATION, 
     '{}_bounds'.format(settings.MODEL_ID): settings.BOUNDS_LOCATION, 
     '{}_update'.format(settings.MODEL_ID): settings.UPDATE_LOCATION}
    top_model((settings.TOP_LOCATION), directory, emds, doc_fba, annotations=annotations)
    comp.flattenSBMLFile(sbml_path=(pjoin(directory, settings.TOP_LOCATION)), output_path=(pjoin(directory, settings.FLATTENED_LOCATION)))
    locations = [
     settings.FBA_LOCATION,
     settings.BOUNDS_LOCATION,
     settings.UPDATE_LOCATION,
     settings.TOP_LOCATION,
     settings.FLATTENED_LOCATION]
    sbml_paths = [pjoin(directory, fname) for fname in locations]
    sbmlreport.create_reports(sbml_paths, directory, validate=False)
    from sbmlutils.dfba.sedml import create_sedml
    species_ids = ', '.join(['A', 'C', 'D'])
    reaction_ids = ', '.join(['R4', 'EX_A', 'EX_C'])
    create_sedml((settings.SEDML_LOCATION), (settings.TOP_LOCATION), directory=directory, dt=0.1,
      tend=50,
      species_ids=species_ids,
      reaction_ids=reaction_ids)
    return directory


if __name__ == '__main__':
    create_model(output_dir=(settings.OUT_DIR))