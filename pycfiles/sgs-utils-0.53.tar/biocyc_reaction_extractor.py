# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/philippebordron/git/work/sgs-utils/src/sgs_utils/biocyc/biocyc_reaction_extractor.py
# Compiled at: 2016-03-23 14:59:50
from __future__ import absolute_import
import sys, os
try:
    from biocyc_parser import *
except ImportError:
    from sgs_utils.biocyc.biocyc_parser import *

LEFT = 'LEFT'
RIGHT = 'RIGHT'
ENZYMATIC_REACTION = 'ENZYMATIC-REACTION'
EC_NUMBER = 'EC-NUMBER'
SPONTANEOUS = 'SPONTANEOUS?'
COEFFICIENT = 'COEFFICIENT'
COMMON_NAME = 'COMMON-NAME'
REACTION = 'REACTION'
ENZYME = 'ENZYME'
REQUIRED_PROTEIN_COMPLEX = 'REQUIRED-PROTEIN-COMPLEX'
REACTION_DIRECTION = 'REACTION-DIRECTION'
CATALYZES = 'CATALYZES'
COMPONENTS = 'COMPONENTS'
COMPONENT_OF = 'COMPONENT-OF'
GENE = 'GENE'
UNMODIFIED_FORM = 'UNMODIFIED-FORM'

def complete_map(map_, key, values):
    try:
        map_[key].update(values)
    except KeyError:
        map_[key] = set(values)


def deep_search(map_proteins, prots):
    result = set()
    file_ = list(prots)
    while file_:
        p = file_.pop(0)
        if p in map_proteins:
            result.add(p)
            for c in map_proteins[p][0]:
                if c not in file_:
                    file_.append(c)

    return result


def coef_list(compound_list, coef_map):
    results = []
    for c in compound_list:
        results.append(coef_map[c])

    return results


def main(argv, prog=os.path.basename(sys.argv[0])):
    import argparse, textwrap
    parser = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter, description=textwrap.dedent('\t\tGenerate the reaction list from Biocyc flat files\n\n\t\texemple:\n\t\t%(prog)s reactions.dat -enz enzrxns.dat proteins.dat -o reaction_list.tsv\n\t\t'), prog=prog)
    parser.add_argument('reaction_file', help='reaction file in Biocyc flat format')
    parser.add_argument('-o', '--output', default=None, help='set an output file')
    parser.add_argument('-enz', '--enzymatic_reactions', nargs=2, metavar=('ENZRXNS',
                                                                           'PROTEINS'), help='enzymatic file and protein file in Biocyc flat format')
    parser.add_argument('-rds', '--reaction_direction_strategy', choices=['consensus', 'enzyme', 'reaction'], default='consensus', help="Specify the stategy when an enzyme catalyzes a reaction in another direction than the reaction direction (default: %(default)s). The 'consensus' choice consists in keeping the less restrictive direction (i.e. reversible) when a conflit exists. The 'enzyme' choice consists in thrusting enzymes more than reactions. When a conflit exists between two enzymes, the less restrictive direction is choosen. If an enzyme does not precise the direction, then the reaction direction will be used as direction for this enzyme. The 'reaction' choice consists in only considering the reaction's direction without thrusting enzyme's direction.")
    parser.add_argument('-sc', '--stoichiometric_coef', default=False, action='store_true', help='add two columns for stochiometric coef for left and right parts')
    args = parser.parse_args(argv)
    stream_out = sys.stdout
    if args.output:
        stream_out = open(args.output, 'w')
    reactions_flat_map = load_flat_file(args.reaction_file, args.stoichiometric_coef)
    enzrxns_flat_map = {}
    proteins_flat_map = {}
    if args.enzymatic_reactions:
        enzrxns_flat_map = load_flat_file(args.enzymatic_reactions[0])
        proteins_flat_map = load_flat_file(args.enzymatic_reactions[1])
    map_reactions = {}
    map_proteins = {}
    map_enzrxns = {}
    map_reactant_coefs = {}
    map_product_coefs = {}
    if args.enzymatic_reactions:
        sys.stderr.write('Protein part\n')
    for prot_id, p_data in proteins_flat_map.items():
        cpds = []
        genes = []
        if COMPONENTS in p_data:
            cpds = p_data[COMPONENTS]
        if GENE in p_data:
            genes = p_data[GENE]
        map_proteins[prot_id] = tuple((cpds, genes))

    if args.enzymatic_reactions:
        sys.stderr.write('Enzymatic reactions part\n')
    for enzrxn_id, e_data in enzrxns_flat_map.items():
        enz = []
        req = []
        if REACTION in e_data:
            rlist = e_data[REACTION]
        else:
            sys.stderr.write('Info: %s has no reaction id\n' % enzrxn_id)
        if ENZYME in e_data:
            enz = e_data[ENZYME]
        if REQUIRED_PROTEIN_COMPLEX in e_data:
            req = e_data[ENZYME]
        direction = None
        if REACTION_DIRECTION in e_data:
            if e_data[REACTION_DIRECTION][0] in ('LEFT-TO-RIGHT', 'PHYSIOL-LEFT-TO-RIGHT',
                                                 'IRREVERSIBLE-LEFT-TO-RIGHT'):
                direction = 1
            if e_data[REACTION_DIRECTION][0] in ('RIGHT-TO-LEFT', 'PHYSIOL-RIGHT-TO-LEFT',
                                                 'IRREVERSIBLE-RIGHT-TO-LEFT'):
                direction = -1
            if e_data[REACTION_DIRECTION][0] == 'REVERSIBLE':
                direction = 0
        map_enzrxns[enzrxn_id] = tuple((rlist, direction, enz, req))

    sys.stderr.write('Reactions part with %s strategy\n' % args.reaction_direction_strategy)
    for react_id, r_data in reactions_flat_map.items():
        left = []
        right = []
        enzrxn = []
        ec_numbers = []
        name = ''
        map_product_coefs[react_id] = {}
        map_reactant_coefs[react_id] = {}
        given_direction = 0
        corrected_direction = 0
        spontaneous = False
        if LEFT in r_data:
            left = r_data[LEFT]
        else:
            sys.stderr.write('Warning: %s has no left part.\n' % react_id)
        if RIGHT in r_data:
            right = r_data[RIGHT]
        else:
            sys.stderr.write('Warning: %s has no right part.\n' % react_id)
        if ENZYMATIC_REACTION in r_data:
            enzrxn = r_data[ENZYMATIC_REACTION]
        if EC_NUMBER in r_data:
            ec_numbers = r_data[EC_NUMBER]
        if COMMON_NAME in r_data:
            name = r_data[COMMON_NAME][0]
        reactants = left
        products = right
        if REACTION_DIRECTION in r_data:
            if r_data[REACTION_DIRECTION][0] in ('LEFT-TO-RIGHT', 'PHYSIOL-LEFT-TO-RIGHT',
                                                 'IRREVERSIBLE-LEFT-TO-RIGHT'):
                given_direction = 1
                corrected_direction = 1
            if r_data[REACTION_DIRECTION][0] in ('RIGHT-TO-LEFT', 'PHYSIOL-RIGHT-TO-LEFT',
                                                 'IRREVERSIBLE-RIGHT-TO-LEFT'):
                given_direction = -1
                corrected_direction = 1
                reactants = right
                products = left
        for c in reactants:
            coef = '1'
            if not isinstance(c, basestring):
                if COEFFICIENT in c[1]:
                    coef = c[1][COEFFICIENT]
                c = c[0]
            map_reactant_coefs[react_id][c] = coef

        for c in products:
            coef = '1'
            if not isinstance(c, basestring):
                if COEFFICIENT in c[1]:
                    coef = c[1][COEFFICIENT]
                c = c[0]
            map_product_coefs[react_id][c] = coef

        reactants = remove_additional_info(reactants)
        products = remove_additional_info(products)
        if SPONTANEOUS in r_data:
            spontaneous = r_data[SPONTANEOUS][0] == 'T'
        ec_number = []
        gene_association = set()
        current_enzymatic_direction = given_direction
        if args.reaction_direction_strategy != 'reaction':
            current_enzymatic_direction = None
        for erxn in enzrxn:
            if erxn in map_enzrxns:
                renz = map_enzrxns[erxn]
                enz_dir = renz[1]
                if enz_dir == None:
                    enz_dir = given_direction
                if args.reaction_direction_strategy == 'consensus':
                    if enz_dir != given_direction:
                        current_enzymatic_direction = 0
                        if enz_dir * given_direction < 0:
                            sys.stderr.write('Info: %s (%d) inverses the direction of %s (%d). The %s direction is now reversible (%d)\n' % (erxn, enz_dir, react_id, given_direction, react_id, current_enzymatic_direction))
                        elif given_direction == 0:
                            sys.stderr.write('Info: %s (%d) specializes the direction of the reaction %s (%d). The reaction %s is keept reversible (%d)\n' % (erxn, enz_dir, react_id, given_direction, react_id, current_enzymatic_direction))
                        else:
                            sys.stderr.write('Info: %s (%d) reverses the direction of the reaction %s (%d). The reaction %s becomes reversible (%d).\n' % (erxn, enz_dir, react_id, given_direction, react_id, current_enzymatic_direction))
                if args.reaction_direction_strategy == 'enzyme':
                    if current_enzymatic_direction:
                        if current_enzymatic_direction == 0 and enz_dir != 0:
                            sys.stderr.write('Info: %s (%d) specializes the direction of %s (%d), but reaction %s will be reversible (%d)\n' % (erxn, enz_dir, react_id, given_direction, react_id, current_enzymatic_direction))
                        elif enz_dir != current_enzymatic_direction:
                            if enz_dir * current_enzymatic_direction < 0:
                                sys.stderr.write('Info: %s (%d) inverses the direction of %s (%d). The reaction %s become reversible (%d).\n' % (erxn, enz_dir, react_id, current_enzymatic_direction, react_id, 0))
                            else:
                                sys.stderr.write('Info: %s (%d) reverses the current reaction %s (%d). The reaction %s become reversible (%d).\n' % (erxn, enz_dir, react_id, current_enzymatic_direction, react_id, 0))
                            current_enzymatic_direction = 0
                    else:
                        current_enzymatic_direction = enz_dir
                        if enz_dir != given_direction:
                            sys.stderr.write('Info: %s (%d) specializes the direction of %s (%d). The reaction %s become irreversible (%d)\n' % (erxn, enz_dir, react_id, given_direction, react_id, current_enzymatic_direction))
                prots = renz[2]
                prots = deep_search(map_proteins, prots)
                for p in prots:
                    for g in map_proteins[p][1]:
                        gene_association.add(g)

        if given_direction < 0 and current_enzymatic_direction >= 0:
            reactants, products = products, reactants
            map_reactant_coefs[react_id], map_product_coefs[react_id] = map_product_coefs[react_id], map_reactant_coefs[react_id]
        if corrected_direction:
            corrected_direction = current_enzymatic_direction
        map_reactions[react_id] = tuple((react_id, name, sorted(reactants), sorted(products), corrected_direction == 0, gene_association, ec_numbers, spontaneous))

    header = [
     'reaction_id', 'name', 'reactants', 'products', 'reversible', 'association', 'ec_number', 'spontaneous']
    if args.stoichiometric_coef:
        header.append('reactant_coefs')
        header.append('product_coefs')
    stream_out.write('%s\n' % ('\t').join(header))
    list_reactions = map_reactions.keys()
    list_reactions.sort()
    for r in list_reactions:
        react_id, name, reactants, products, rev, gene_association, ec_number, spontaneous = map_reactions[r]
        ec_number = remove_additional_info(ec_number)
        line = [react_id,
         name,
         (' ').join(reactants),
         (' ').join(products),
         str(rev),
         (' ').join(gene_association),
         (' ').join(ec_number),
         str(spontaneous)]
        if args.stoichiometric_coef:
            line.append((' ').join(coef_list(reactants, map_reactant_coefs[react_id])))
            line.append((' ').join(coef_list(products, map_product_coefs[react_id])))
        stream_out.write('%s\n' % ('\t').join(line))

    if args.output:
        stream_out.close()
    return


if __name__ == '__main__':
    main(sys.argv[1:])