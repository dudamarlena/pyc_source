# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/chiararasi/Documents/work/GITs/patientMatcher/patientMatcher/match/phenotype_matcher.py
# Compiled at: 2019-04-25 09:29:38
# Size of source mod 2**32: 7776 bytes
import os, logging
from patientMatcher.parse.patient import features_to_hpo, disorders_to_omim
from patientMatcher.resources import path_to_hpo_terms, path_to_phenotype_annotations
from patient_similarity import HPO, Diseases, HPOIC, Patient
from patient_similarity.__main__ import compare_patients
LOG = logging.getLogger(__name__)
PHENOTYPE_ROOT = 'HP:0000001'

def match(database, max_score, features, disorders):
    """Handles phenotype matching algorithm

    Args:
        database(pymongo.database.Database)
        max_score(float): a number between 0 and 1
        features(list): a list of phenotype feature objects (example ID = HP:0008619)
        disorders(list): a list of OMIM diagnoses (example ID = MIM:616007 )

    Returns:
        matches(dict): a dictionary of patient matches with phenotype matching score
    """
    matches = {}
    hpo_terms = []
    omim_terms = []
    query_fields = []
    hpoic = None
    hpo = None
    LOG.info('\n\n###### Running phenotype matcher module ######')
    if features:
        hpo_terms = features_to_hpo(features)
        query_fields.append({'features': {'$exists':True,  '$ne':[]}})
        LOG.info('Creating HPO information content')
        hpo = HPO(path_to_hpo_terms, new_root=PHENOTYPE_ROOT)
        diseases = Diseases(path_to_phenotype_annotations)
        hpoic = HPOIC(hpo, diseases, orphanet=None, patients=False, use_disease_prevalence=False,
          use_phenotype_frequency=False,
          distribute_ic_to_leaves=False)
    if disorders:
        omim_terms = disorders_to_omim(disorders)
        query_fields.append({'disorders.id': {'$in': omim_terms}})
    if len(query_fields) > 0:
        query = {'$or': query_fields}
        LOG.info('Searching for patients in database with the following query:{}'.format(query))
        pheno_matching_patients = list(database['patients'].find(query))
        LOG.info("\n\nFOUND {} patients matching patients's phenotype tracts\n\n".format(len(pheno_matching_patients)))
        for i in range(len(pheno_matching_patients)):
            patient = pheno_matching_patients[i]
            LOG.info('## Evaluating phenotype similarity with patient {} ##'.format(i + 1))
            similarity = evaluate_pheno_similariy(hpoic, hpo, hpo_terms, omim_terms, patient, max_score)
            match = {'patient_obj':patient, 
             'pheno_score':similarity}
            matches[patient['_id']] = match

    return matches


def evaluate_pheno_similariy(hpoic, hpo, hpo_terms, disorders, pheno_matching_patient, max_similarity):
    """Evaluates the similarity of two patients based on phenotype features

        Args:
            hpoic(class) : the information content for the HPO
            hpo(class): an instance of the class for interacting with HPO
            hpo_terms(list): HPO terms of the query patient
            disorders(list): OMIM disorders of the query patient
            pheno_matching_patient(patient_obj): a patient object from the database
            max_similarity(float): a floating point number representing the highest value allowed for a feature

        Returns:
            patient_similarity(float): the computed phenotype similarity among the patients
    """
    patient_similarity = 0
    hpo_score = 0
    omim_score = 0
    max_omim_score = 0
    max_hpo_score = 0
    matching_hpo_terms = features_to_hpo(pheno_matching_patient.get('features'))
    matching_omim_terms = disorders_to_omim(pheno_matching_patient.get('disorders'))
    if hpo_terms:
        if matching_hpo_terms:
            LOG.info('HPO terms available for comparison')
            if disorders:
                if matching_omim_terms:
                    LOG.info('OMIM diagnoses available for comparison')
                    max_omim_score = max_similarity / 2
                    max_hpo_score = max_similarity / 2
            else:
                max_hpo_score = max_similarity
            hpo_score = similarity_wrapper(hpoic, hpo, max_hpo_score, hpo_terms, matching_hpo_terms)
    else:
        LOG.debug('Missing HPO terms, phenotype comparison based on OMIM diagnoses.')
        max_omim_score = max_similarity / 2
    if max_omim_score:
        omim_score = evaluate_subcategories(disorders, matching_omim_terms, max_omim_score)
    patient_similarity = hpo_score + omim_score
    LOG.info('patient phenotype score: {0} (OMIM:{1}, HPO:{2})'.format(patient_similarity, omim_score, hpo_score))
    return patient_similarity


def similarity_wrapper(hpoic, hpo, max_hpo_score, hpo_terms_q, hpo_terms_m):
    """A wrapper around patient-similarity repository:
    https://github.com/buske/patient-similarity.

    Args:
        hpoic(class) : the information content for the HPO
        hpo(class): an instance of the class for interacting with HPO
        max_hpo_score(float): max score which can be assigned to HPO similarity
        hpo_terms_q(list): a list of HPO terms from query patient
        hpo_terms_m(list): a list of HPO terms from match patient

    Returns:
        score(float): simgic similarity score after HPO term comparison
    """
    terms = set()
    for term_id in hpo_terms_q:
        term = hpo[term_id]
        if term:
            terms.add(term)

    query_patient = Patient(id='q', hp_terms=terms)
    terms = set()
    for term_id in hpo_terms_m:
        term = hpo[term_id]
        if term:
            terms.add(term)

    match_patient = Patient(id='m', hp_terms=terms)
    score_obj = compare_patients(hpoic=hpoic, patient1=query_patient, patient2=match_patient,
      scores=['simgic'])
    simgic_score = score_obj.get('simgic')
    LOG.info('patient-similarity module returned a simgic score of {}'.format(simgic_score))
    relative_simgic_score = simgic_score * max_hpo_score
    return relative_simgic_score


def evaluate_subcategories(list1, list2, max_score):
    """returns a numerical representation of the similarity of two lists of strings

        Args:
            list1(list): a list of strings (this is a list of items from the query patient)
            list2(list): another list of strings (list of items from the patients in database)
            max_score(float): the maximum value to return if the lists are identical

        Returns:
            matching_score(float): a number reflecting the similarity between the lists
    """
    matching_score = 0
    if len(list1) > 0:
        list_item_score = max_score / len(list1)
        n_shared_items = len(set(list1).intersection(list2))
        matching_score = n_shared_items * list_item_score
    return matching_score