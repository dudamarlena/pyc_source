# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/chiararasi/Documents/work/GITs/patientMatcher/patientMatcher/match/genotype_matcher.py
# Compiled at: 2019-04-23 03:57:58
# Size of source mod 2**32: 4462 bytes
import logging
from patientMatcher.parse.patient import gtfeatures_to_genes, gtfeatures_to_variants
LOG = logging.getLogger(__name__)

def match(database, gt_features, max_score):
    """Handles genotype matching algorithm

    Args:
        database(pymongo.database.Database)
        gt_features(list): a list of genomic features (objects)
        max_score(float): a number between 0 and 1

    Returns:
        matches(dict): a dictionary of patient matches with GT score
    """
    matches = {}
    n_gtfeatures = len(gt_features)
    LOG.info('\n\n###### Running genome matcher module ######')
    if n_gtfeatures > 0:
        max_feature_similarity = max_score / n_gtfeatures
        LOG.info('Query patient has {0} genotype features.'.format(n_gtfeatures))
        LOG.info('Each GT feature will contribute with a weight of {0} to a total GT score (max GT score is {1})'.format(max_feature_similarity, max_score))
        query = {}
        query_fields = []
        genes = gtfeatures_to_genes(gt_features)
        if genes:
            query_fields.append({'genomicFeatures.gene.id': {'$in': genes}})
        variants = gtfeatures_to_variants(gt_features)
        if variants:
            query_fields.append({'genomicFeatures.variant': {'$in': variants}})
        if len(query_fields) > 0:
            query = {'$or': query_fields}
            LOG.info('Querying database for genomic features:{}'.format(query))
            matching_patients = list(database['patients'].find(query))
            LOG.info('Found {0} matching patients'.format(len(matching_patients)))
            for patient in matching_patients:
                gt_similarity = evaluate_GT_similarity(gt_features, patient['genomicFeatures'], max_feature_similarity)
                match = {'patient_obj':patient, 
                 'geno_score':gt_similarity}
                matches[patient['_id']] = match

    LOG.info("\n\nFOUND {} patients matching patients's genomic tracts\n\n".format(len(matching_patients)))
    return matches


def evaluate_GT_similarity(query_features, db_patient_features, max_feature_similarity):
    """ Evaluates the genomic similarity of two patients based on genomic similarities

        Args:
            query_patient(list of dictionaries): genomic features of the query patient
            db_patient_features(list of dictionaries): genomic features of a patient in patientMatcher database
            max_similarity(float): a floating point number representing the highest value allowed for a feature

                ## Explanation: for a query patient with one feature max_similarity will be equal to MAX_GT_SCORE
                   For a patient with 2 features max_similarity will be MAX_GT_SCORE/2 and so on.

        Returns:
            patient_similarity(float): the computed genetic similarity among the patients
    """
    matched_features = []
    n_feature = 0
    for feature in query_features:
        matched_features.append(0)
        q_gene = feature['gene']
        q_variant = feature.get('variant', None)
        for matching_feature in db_patient_features:
            m_gene = matching_feature['gene']
            m_variant = matching_feature.get('variant')
            if q_variant and m_variant:
                if q_variant == m_variant:
                    matched_features[n_feature] = max_feature_similarity
            else:
                if q_gene:
                    if m_gene:
                        if matched_features[n_feature] == 0:
                            if q_gene == m_gene:
                                matched_features[n_feature] = max_feature_similarity / 4

        n_feature += 1

    features_sum = sum(matched_features)
    return features_sum