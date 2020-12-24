# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.11-intel/egg/matchengine/engine.py
# Compiled at: 2017-02-10 11:07:01
"""Copyright 2016 Dana-Farber Cancer Institute"""
from cerberus1 import schema_registry
import networkx as nx, logging
from matchengine import schema
from matchengine.validation import ConsentValidatorCerberus
from matchengine.utilities import *
logging.basicConfig(level=logging.DEBUG, format='[%(levelname)s] %(message)s')
parent_schema_adv = schema.parent_schema.copy()
parent_schema_adv['children'] = {'type': 'list', 
   'schema': {'type': 'dict', 
              'schema': 'child_schema'}}
parent_schema_adv['match'] = {'type': 'list', 
   'schema': {'type': 'dict', 
              'schema': 'yaml_match_schema'}}
schema_registry.add('parent_schema', parent_schema_adv)
schema_registry.add('yaml_match_schema', schema.yaml_match_schema)
schema_registry.add('yaml_genomic_schema', schema.yaml_genomic_schema)
schema_registry.add('yaml_clinical_schema', schema.yaml_clinical_schema)
schema_registry.add('map', schema.map)

class MatchEngine(object):

    def __init__(self, db):
        self.db = db
        self.all_match = set(self.db.clinical.distinct('SAMPLE_ID'))
        self.bootstrap_map()
        self.mapping = list(self.db.map.find())

    def bootstrap_map(self):
        """Loads the map into the database between yaml field names and their corresponding database field names"""
        key_map = {'AGE_NUMERICAL': 'BIRTH_DATE', 
           'EXON': 'TRUE_TRANSCRIPT_EXON', 
           'HUGO_SYMBOL': 'TRUE_HUGO_SYMBOL', 
           'PROTEIN_CHANGE': 'TRUE_PROTEIN_CHANGE', 
           'WILDCARD_PROTEIN_CHANGE': 'TRUE_PROTEIN_CHANGE', 
           'ONCOTREE_PRIMARY_DIAGNOSIS': 'ONCOTREE_PRIMARY_DIAGNOSIS_NAME', 
           'VARIANT_CLASSIFICATION': 'TRUE_VARIANT_CLASSIFICATION', 
           'VARIANT_CATEGORY': 'VARIANT_CATEGORY', 
           'CNV_CALL': 'CNV_CALL', 
           'WILDTYPE': 'WILDTYPE', 
           'GENDER': 'GENDER'}
        val_map = {'VARIANT_CATEGORY': {'Mutation': 'MUTATION', 
                                'Copy Number Variation': 'CNV', 
                                'Structural Variation': 'SV'}, 
           'CNV_CALL': {'High Amplification': 'High level amplification', 
                        'Homozygous Deletion': 'Homozygous deletion', 
                        'Heterozygous Deletion': 'Heterozygous deletion'}, 
           'WILDTYPE': {'true': True, 
                        'false': False}}
        mapping = []
        for old_key, new_key in key_map.iteritems():
            item = {'key_old': old_key, 
               'key_new': new_key}
            if old_key in val_map:
                item['values'] = val_map[old_key]
            else:
                item['values'] = {}
            mapping.append(item)

        self.db.drop_collection('map')
        self.db.map.insert_many(mapping)

    @staticmethod
    def validate_yaml_format(data):
        """ check if yaml is in correct format

        :param data:
        :return:
        """
        if isinstance(data, dict):
            return (0, data)
        try:
            data_json = yaml.load(data)
            return (0, data_json)
        except yaml.YAMLError as exc:
            return (
             1, exc)

    def validate_yaml_data(self, data_json):
        """ Validates yaml specs

        :param data_json:
        :return:
        """
        v = ConsentValidatorCerberus(schema.parent_schema)
        v.validate(data_json)
        return v.errors

    @staticmethod
    def _test_type(data):
        """ returns the type
        :param data:
        :return:
        """
        is_dict = isinstance(data, dict)
        is_list = isinstance(data, list)
        is_value = False
        if not is_dict and not is_list:
            is_value = True
        return (
         is_dict, is_list, is_value)

    @staticmethod
    def create_match_tree(data):
        """
        Given json object of MATCH clause , the function returns a directed graph

        :param data: json match clause
        :return: diGraph match tree
        """
        key = data.keys()[0]
        value = data[key]
        global_node = 1
        g = nx.DiGraph()
        s = []
        s.append([0, global_node, key, value])
        while len(s) > 0:
            current = s.pop(0)
            parent = current[0]
            node = current[1]
            key = current[2]
            value = current[3]
            g.add_node(node)
            g.add_edges_from([(parent, node)])
            g.node[node]['type'] = key
            if isinstance(value, dict):
                g.node[node]['value'] = value
            elif isinstance(value, list):
                for i in range(0, len(value)):
                    global_node += 1
                    s.append([node, global_node, value[i].keys()[0], value[i][value[i].keys()[0]]])

        g.remove_node(0)
        return g

    def create_trial_tree(self, raw_data, no_validate=False):
        """ creates networkx tree of trial from a python dictionary
        :return:
        """
        if not no_validate:
            status, data = self.validate_yaml_format(raw_data)
            if status != 0:
                logging.error('invalid trial data')
                return (
                 1, data)
            errors = self.validate_yaml_data(data)
            if len(errors) > 0:
                logging.error('schema error')
                return (
                 2, errors)
        else:
            data = raw_data
        G = nx.DiGraph()
        self._recursive_create(None, data, G)
        self._annotate_match(G)
        return (
         0, G)

    def run_query(self, node):
        """
        Runs genomic or clinical query against Mongo database and returns a set of sample ids that matched

        :param node: node location with the trial match tree
        :param db: database connection
        :return: set of matched sample ids
        """
        matches = []
        if node['type'] == 'genomic':
            item = node['value']
            g, neg = self.prepare_genomic_criteria(item)
            if len(g.keys()) == 0:
                results = list()
            else:
                if neg:
                    proj = {'SAMPLE_ID': 1}
                else:
                    proj = {'SAMPLE_ID': 1, 
                       'TRUE_HUGO_SYMBOL': 1, 
                       'TRUE_PROTEIN_CHANGE': 1, 
                       'TRUE_VARIANT_CLASSIFICATION': 1, 
                       'VARIANT_CATEGORY': 1, 
                       'CNV_CALL': 1, 
                       'WILDTYPE': 1, 
                       'CHROMOSOME': 1, 
                       'POSITION': 1, 
                       'TRUE_CDNA_CHANGE': 1, 
                       'REFERENCE_ALLELE': 1, 
                       'TRUE_TRANSCRIPT_EXON': 1, 
                       'CANONICAL_STRAND': 1, 
                       'ALLELE_FRACTION': 1, 
                       'TIER': 1, 
                       'CLINICAL_ID': 1, 
                       '_id': 1}
                results = list(self.db.genomic.find(g, proj))
                if neg:
                    results = self.all_match - set(x['SAMPLE_ID'] for x in results)
                    alteration, is_variant = format_not_match(g)
                    matches = [ {'sample_id': sample_id, 'match_type': is_variant, 'genomic_alteration': alteration} for sample_id in results
                              ]
                else:
                    for item in results:
                        alteration, is_variant = format_genomic_alteration(item, g)
                        genomic_info = {'match_type': is_variant, 
                           'genomic_alteration': alteration}
                        for field in proj:
                            if field in item:
                                if field == '_id':
                                    genomic_info['genomic_id'] = item[field]
                                else:
                                    genomic_info[field.lower()] = item[field]

                        matches.append(genomic_info)

                    results = set(item['SAMPLE_ID'] for item in results)
        elif node['type'] == 'clinical':
            item = node['value']
            c = self.prepare_clinical_criteria(item)
            if len(c.keys()) == 0:
                results = list()
                matches = list()
            else:
                results = set(self.db.clinical.find(c).distinct('SAMPLE_ID'))
        else:
            logging.info('bad match tree')
            return
        return (
         results, matches)

    def traverse_match_tree(self, g):
        """ Finds matches for a given match tree

        :param g: diGraph match tree
        :return: match set for a tree
        """
        for node_id in list(nx.dfs_postorder_nodes(g, source=1)):
            node = g.node[node_id]
            successors = g.successors(node_id)
            if len(successors) == 0:
                result, matches = self.run_query(node)
                node['result'] = result
                if node['type'] == 'genomic':
                    node['genomic'] = matches
                if node['type'] == 'clinical':
                    node['genomic'] = []
            else:
                node['result'] = set([])
                node['genomic'] = g.node[successors[0]]['genomic']
                node['result'].update(g.node[successors[0]]['result'])
                print '%s: %s' % (node_id, node['result'])
                for i in range(1, len(successors)):
                    s_list = g.node[successors[i]]['result']
                    if node['type'] == 'and':
                        node['result'].intersection_update(s_list)
                    elif node['type'] == 'or':
                        node['result'].update(s_list)
                    node['genomic'] = [ item for item in node['genomic'] if item['sample_id'] in node['result'] ]
                    node['genomic'] += [ item for item in g.node[successors[i]]['genomic'] if item['sample_id'] in node['result'] and item not in node['genomic']
                                       ]

        return (
         g.node[1]['result'], g.node[1]['genomic'])

    def prepare_clinical_criteria(self, item):
        """
        Translates match criteria from yaml format into a Mongo query

        :param item: the match tree criteria for a given node in yaml format
        :return: Mongo query for clinical collection
        """
        c = {}
        onco_tree = build_oncotree()
        map_keys = [
         'oncotree_primary_diagnosis', 'age_numerical', 'gender']
        for key in item.keys():
            if key.lower() not in map_keys:
                del item[key]

        for field in item:
            norm_field, _ = normalize_fields(self.mapping, field)
            txt = item[field]
            c = build_cquery(c, norm_field, txt)

        if 'ONCOTREE_PRIMARY_DIAGNOSIS_NAME' in c:
            c['ONCOTREE_PRIMARY_DIAGNOSIS_NAME'] = self._search_oncotree_diagnosis(onco_tree, c)
        if 'BIRTH_DATE' in c:
            c['BIRTH_DATE'] = search_birth_date(c)
        return c

    def prepare_genomic_criteria(self, item):
        """
        Translates match criteria from yaml format into a Mongo query

        :param item: The match tree criteria for a given node in yaml format
        :return: Mongo query for genomic collection
        """
        g = {}
        track_neg = False
        wildtype = False
        map_keys = [
         'hugo_symbol', 'variant_category', 'protein_change', 'wildcard_protein_change',
         'variant_classification', 'exon', 'cnv_call', 'wildtype']
        for key in item.keys():
            if key.lower() not in map_keys:
                del item[key]
            if key.lower() == 'wildtype':
                wildtype = True

        for field, val in item.iteritems():
            norm_field, norm_val = normalize_values(self.mapping, field, val)
            txt = norm_val
            key, txt, neg = build_gquery(field, txt)
            if key is None and txt is None and neg is None:
                return ({}, False)
            if neg and not track_neg:
                track_neg = True
            g[norm_field] = {key: txt}

        if not wildtype:
            g = {'$and': [g, {'$or': [{'WILDTYPE': False}, {'WILDTYPE': {'$exists': False}}]}]}
        return (
         g, track_neg)

    def find_trial_matches(self):
        """
        Iterates through all match clauses of all trials located in the database and matches patients to trials
        based on their clinical and genomic documents.

        :return: Dictionary containing matches
        """
        mrns = self.db.clinical.distinct('DFCI_MRN')
        proj = {'protocol_no': 1, 'treatment_list': 1, '_summary': 1}
        all_trials = list(self.db.trial.find({}, proj))
        mrn_map = samples_from_mrns(self.db, mrns)
        trial_matches = []
        for trial in all_trials:
            logging.info('Matching trial %s' % trial['protocol_no'])
            trial_status = 'open'
            if '_summary' in trial:
                if 'status' in trial['_summary'] and isinstance(trial['_summary']['status'], list):
                    if 'value' in trial['_summary']['status'][0]:
                        if trial['_summary']['status'][0]['value'].lower() != 'open to accrual':
                            trial_status = 'closed'
            for step in trial['treatment_list']['step']:
                if 'match' in step:
                    trial_matches = self._assess_match(mrn_map, trial_matches, trial, step, 'step', trial_status)
                for arm in step['arm']:
                    if 'match' in arm:
                        trial_matches = self._assess_match(mrn_map, trial_matches, trial, arm, 'arm', trial_status)
                    for dose in arm['dose_level']:
                        if 'match' in dose:
                            trial_matches = self._assess_match(mrn_map, trial_matches, trial, dose, 'dose', trial_status)

        logging.info('Adding trial matches to database')
        add_matches(trial_matches, self.db)
        return trial_matches

    def _assess_match(self, mrn_map, trial_matches, trial, trial_segment, match_segment, trial_status):
        """
        Given a trial's match tree, finds all patients that matches to it and records the step, arm, or dose
        internal id that it matched to along with the genomic alteration that matched.

        :param mrn_map: Dictionary mapping patient sample ids to MRNs
        :param trial_matches: Dictionary containing the matches
        :param trial: Trial document
        :param trial_segment: Either the step, arm, or dose segment of the trial document
        :param match_segment: Marker indicating if segment is step, arm, or dose
        :param trial_status: Overall trial status. either open or closed.
        :return: Dictionary containing the matches
        """
        match_tree = self.create_match_tree(trial_segment['match'][0])
        results, ginfos = self.traverse_match_tree(match_tree)
        clinical = []
        cids = list(set(item['sample_id'] for item in ginfos if 'sample_id' in item))
        if cids:
            cproj = {'SAMPLE_ID': 1, 'ORD_PHYSICIAN_NAME': 1, 
               'ORD_PHYSICIAN_EMAIL': 1, 
               'ONCOTREE_PRIMARY_DIAGNOSIS_NAME': 1, 
               'REPORT_DATE': 1, 
               'VITAL_STATUS': 1, 
               'FIRST_LAST': 1, 
               '_id': 1}
            clinical = list(self.db.clinical.find({'SAMPLE_ID': {'$in': cids}}, cproj))
        for item in ginfos:
            match = item
            match['mrn'] = mrn_map[item['sample_id']]
            match['protocol_no'] = trial['protocol_no']
            match['match_level'] = match_segment
            match['trial_accrual_status'] = trial_status
            if clinical:
                for citem in clinical:
                    if citem['SAMPLE_ID'] == item['sample_id']:
                        for field in citem:
                            if field == '_id':
                                match['clinical_id'] = citem[field]
                            else:
                                match[field.lower()] = citem[field]

            if match_segment == 'dose':
                match['internal_id'] = str(trial_segment['level_internal_id'])
                match['code'] = trial_segment['level_code']
                if 'level_suspended' in trial_segment and trial_segment['level_suspended'].lower() == 'y':
                    match['trial_accrual_status'] = 'closed'
            elif match_segment == 'arm':
                match['internal_id'] = str(trial_segment['arm_internal_id'])
                match['code'] = str(trial_segment['arm_code'])
                if 'arm_suspended' in trial_segment and trial_segment['arm_suspended'].lower() == 'y':
                    match['trial_accrual_status'] = 'closed'
            elif match_segment == 'step':
                match['internal_id'] = str(trial_segment['step_internal_id'])
                match['code'] = trial_segment['step_code']
            trial_matches.append(match)

        return trial_matches

    @staticmethod
    def _search_oncotree_diagnosis(onco_tree, c):
        """Add all the oncotree nodes """
        nodes = []
        tmpc = {'ONCOTREE_PRIMARY_DIAGNOSIS_NAME': {}}
        for key in c['ONCOTREE_PRIMARY_DIAGNOSIS_NAME'].keys():
            diagnoses = c['ONCOTREE_PRIMARY_DIAGNOSIS_NAME'][key]
            if not isinstance(diagnoses, list):
                diagnoses = [
                 diagnoses]
            for txt in diagnoses:
                if txt.endswith('_LIQUID_') or txt.endswith('_SOLID_'):
                    node1 = oncotreenx.lookup_text(onco_tree, 'Lymph')
                    node2 = oncotreenx.lookup_text(onco_tree, 'Blood')
                    nodes1 = list(nx.dfs_tree(onco_tree, node1))
                    nodes2 = list(nx.dfs_tree(onco_tree, node2))
                    nodes = list(set(nodes1).union(set(nodes2)))
                    if txt == '_SOLID_':
                        all_nodes = set(list(onco_tree.nodes()))
                        tmp_nodes = all_nodes - set(nodes)
                        nodes = list(tmp_nodes)
                else:
                    node = oncotreenx.lookup_text(onco_tree, txt)
                    if onco_tree.has_node(node):
                        nodes = list(nx.dfs_tree(onco_tree, node))
                nodes_txt = [ onco_tree.node[n]['text'] for n in nodes ]
                if key == '$eq':
                    key = '$in'
                    tmpc['ONCOTREE_PRIMARY_DIAGNOSIS_NAME'][key] = nodes_txt
                elif key == '$ne':
                    key = '$nin'
                    tmpc['ONCOTREE_PRIMARY_DIAGNOSIS_NAME'][key] = nodes_txt
                elif key == '$in':
                    if '$in' in tmpc['ONCOTREE_PRIMARY_DIAGNOSIS_NAME']:
                        tmpc['ONCOTREE_PRIMARY_DIAGNOSIS_NAME']['$in'] += nodes_txt
                    else:
                        tmpc['ONCOTREE_PRIMARY_DIAGNOSIS_NAME']['$in'] = nodes_txt
                elif key == '$nin':
                    if '$nin' in tmpc['ONCOTREE_PRIMARY_DIAGNOSIS_NAME']:
                        tmpc['ONCOTREE_PRIMARY_DIAGNOSIS_NAME']['$nin'] += nodes_txt
                    else:
                        tmpc['ONCOTREE_PRIMARY_DIAGNOSIS_NAME']['$nin'] = nodes_txt

        for k in tmpc['ONCOTREE_PRIMARY_DIAGNOSIS_NAME']:
            tmpc['ONCOTREE_PRIMARY_DIAGNOSIS_NAME'][k] = list(set(tmpc['ONCOTREE_PRIMARY_DIAGNOSIS_NAME'][k]))

        return tmpc['ONCOTREE_PRIMARY_DIAGNOSIS_NAME']

    def _recursive_create(self, parent_id, data, G):
        child_id_set = [
         'protocol_id', 'arm_internal_id', 'level_internal_id', 'step_internal_id']
        key_set = set(['treatment_list', 'step', 'arm', 'dose_level'])
        if parent_id is None:
            n = G.add_node(0)
            cur_name = 0
            G.graph['nidx'] = 1
        else:
            cur_name = G.graph['nidx']
            n = G.add_node(cur_name)
            G.graph['nidx'] += 1
            G.add_edge(parent_id, cur_name)
        for key, value in data.items():
            if key in child_id_set:
                G.node[cur_name]['node_id'] = value
            if key not in key_set:
                G.node[cur_name][key] = value

        for key in data:
            if key in key_set:
                if key == 'treatment_list':
                    list_val = data[key]['step']
                else:
                    list_val = data[key]
                for child_data in list_val:
                    self._recursive_create(cur_name, child_data, G)

        return

    def _annotate_match(self, G):
        for n in G.nodes():
            if 'match' not in G.node[n]:
                continue
            content = {'match': G.node[n]['match']}
            match_tree = self.create_match_tree(content)
            G.node[n]['match_tree'] = match_tree