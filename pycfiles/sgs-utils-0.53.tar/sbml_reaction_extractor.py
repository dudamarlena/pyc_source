# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/philippebordron/git/work/sgs-utils/src/sgs_utils/sbml/sbml_reaction_extractor.py
# Compiled at: 2016-03-17 14:36:36
import sys, os, re, libsbml

def check(value, message):
    """If 'value' is None, prints an error message constructed using
   'message' and then exits with status code 1.  If 'value' is an integer,
   it assumes it is a libSBML return status code.  If the code value is
   LIBSBML_OPERATION_SUCCESS, returns without further action; if it is not,
   prints an error message constructed using 'message' along with text from
   libSBML explaining the meaning of the code, and exits with status code 1.
        """
    if value == None:
        raise SystemExit('LibSBML returned a null value trying to ' + message + '.')
    elif type(value) is int:
        if value == LIBSBML_OPERATION_SUCCESS:
            return
        err_msg = 'Error encountered trying to ' + message + '.' + 'LibSBML returned error code ' + str(value) + ': "' + OperationReturnValue_toString(value).strip() + '"'
        raise SystemExit(err_msg)
    else:
        return
    return


def coef_list(compound_list, coef_map):
    results = []
    for c in compound_list:
        results.append(str(coef_map[c]))

    return results


def main(argv, prog=os.path.basename(sys.argv[0])):
    import argparse, textwrap
    parser = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter, description=textwrap.dedent("\t\tExtract, from the given metabolic network in Nico's sbml file format, the reaction list with reactants, products, reversible, association, ec_number and spontaneous informations and write them in the standard output in .tsv format\n\n\t\texemple:\n\t\tpython sbml_reaction_extractor.py sbml_file reaction_list_file reaction_graph_file [-c 40] > reaction_list.tsv\n\t\t"), prog=prog)
    parser.add_argument('sbml_file', help='metabolic network file in SBML file format')
    parser.add_argument('-o', '--output', default=None, help='set an output file')
    parser.add_argument('-sc', '--stoichiometric_coef', default=False, action='store_true', help='add two columns for stochiometric coef for left and right parts')
    args = parser.parse_args(argv)
    stream_out = sys.stdout
    if args.output:
        stream_out = open(args.output, 'w')
    document = libsbml.readSBML(args.sbml_file)
    model = document.getModel()
    if model == None:
        sys.stderr.write('No model present.\n')
        sys.exit(1)
    map_gene_id_to_gene_label = {}
    if model.isPackageEnabled('fbc'):
        for g in model.getPlugin('fbc').getListOfGeneProducts():
            map_gene_id_to_gene_label[g.getId()] = g.getLabel()

    map_reactions = {}
    map_reactant_coefs = {}
    map_product_coefs = {}
    for i in range(0, model.getNumReactions()):
        r = model.getReaction(i)
        react_id = r.getId()
        name = r.getName()
        reactants = []
        products = []
        map_reactant_coefs[react_id] = {}
        map_product_coefs[react_id] = {}
        for c in r.getListOfReactants():
            n = c.getSpecies()
            reactants.append(n)
            map_reactant_coefs[react_id][n] = c.getStoichiometry()

        for c in r.getListOfProducts():
            n = c.getSpecies()
            products.append(n)
            map_product_coefs[react_id][n] = c.getStoichiometry()

        rev = r.getReversible()
        spontaneous = False
        gene_association = set()
        ec_number = set()
        if r.isSetNotes():
            for note in r.getNotesString().splitlines():
                m = re.match('\\s*<(?:html:)*p>GENE_ASSOCIATION:\\s*([^<]*)</(?:html:)*p>\\s*', note)
                if m:
                    for g in m.group(1).split():
                        if g not in ('and', 'or', '(', ')', 'SPONTANEOUS', 'AUTOCOMPLETION',
                                     'UNIVERSAL'):
                            if g.startswith('('):
                                g = g[1:]
                            if g.endswith(')'):
                                g = g[:-1]
                            gene_association.add(g)
                        if g in ('SPONTANEOUS', ):
                            spontaneous = True

                m = re.match('\\s*<(?:html:)*p>PROTEIN_CLASS:(.*)</(?:html:)*p>\\s*', note)
                if m:
                    for e in m.group(1).split():
                        if e not in ('and', 'or', '(', ')'):
                            ec_number.add(e)

                m = re.match('\\s*<(?:html:)*p>EC Number:(.*)</(?:html:)*p>\\s*', note)
                if m:
                    for e in m.group(1).split('/'):
                        ec_number.add(e)

        if r.isPackageEnabled('fbc'):
            if r.getPlugin('fbc').getGeneProductAssociation():
                asso = r.getPlugin('fbc').getGeneProductAssociation().getAssociation().toInfix()
                for g in asso.split():
                    if g not in ('and', 'or', '(', ')'):
                        if g.startswith('('):
                            g = g[1:]
                        if g.endswith(')'):
                            g = g[:-1]
                        if g in map_gene_id_to_gene_label:
                            g = map_gene_id_to_gene_label[g]
                        gene_association.add(g)

        map_reactions[react_id] = tuple((react_id, name, reactants, products, rev, gene_association, ec_number, spontaneous))

    header = ['reaction_id', 'name', 'reactants', 'products', 'reversible', 'association', 'ec_number', 'spontaneous']
    if args.stoichiometric_coef:
        header.append('reactant_coefs')
        header.append('product_coefs')
    stream_out.write('%s\n' % ('\t').join(header))
    list_reactions = map_reactions.keys()
    list_reactions.sort()
    for r in list_reactions:
        react_id, name, reactants, products, rev, gene_association, ec_number, spontaneous = map_reactions[r]
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