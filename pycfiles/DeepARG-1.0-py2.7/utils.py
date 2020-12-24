# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/deeparg/argdb/utils.py
# Compiled at: 2018-12-06 14:22:32
import json
from sklearn.feature_extraction import DictVectorizer
from sklearn import preprocessing
from sklearn.ensemble import ExtraTreesClassifier
from sklearn.feature_selection import SelectFromModel
import numpy as np
from sklearn.cross_validation import train_test_split
from sklearn.metrics import classification_report, accuracy_score
from lasagne import layers
from lasagne import init
import lasagne
from lasagne.updates import sgd, nesterov_momentum
from nolearn.lasagne import NeuralNet
import numpy as np
from sklearn.datasets import fetch_mldata
from sklearn.utils import shuffle
import theano
floatX = theano.config.floatX

def make_metadata_json(fname):
    metadata = {}
    for i in open(fname):
        i = i.strip().split('\t')
        try:
            metadata[i[2]].append({'database': i[1], 
               'type': i[3], 
               'description': i[4], 
               'inference': i[5], 
               'status': i[6], 
               'subType': i[7], 
               'class': ''})
        except:
            metadata[i[2]] = [
             {'database': i[1], 'type': i[3], 
                'description': i[4], 
                'inference': i[5], 
                'status': i[6], 
                'subType': i[7], 
                'class': ''}]

    json.dump(metadata, open(fname + '.json', 'w'))
    return metadata


def make_clusters_json(fname):
    clusters = {}
    for i in open(fname):
        i = i.strip().split('\t')
        try:
            identity = float(i[5])
        except:
            identity = 100

        try:
            clusters[i[1]].append({'seq_len': int(i[2]), 
               'database': i[3], 
               'protein_id': i[4], 
               'identity': identity, 
               'rep_seq': int(i[6])})
        except:
            clusters[i[1]] = [
             {'seq_len': int(i[2]), 'database': i[3], 
                'protein_id': i[4], 
                'identity': identity, 
                'rep_seq': int(i[6])}]

    json.dump(clusters, open(fname + '.json', 'w'))
    return clusters


def make_alignments_json(fname):
    alignments = {}
    for i in open(fname):
        i = i.strip().split('\t')
        if i[0] == i[1]:
            continue
        if i[0].split('|')[0] == 'UNIPROT' and i[1].split('|')[0] == 'UNIPROT':
            continue
        if i[0].split('|')[0] != 'UNIPROT' and i[1].split('|')[0] == 'UNIPROT':
            continue
        try:
            alignments[i[0].split('|')[1]].append({'dbquery': i[0].split('|')[0], 
               'dbsubject': i[1].split('|')[0], 
               'subject': i[1].split('|')[1], 
               'identity': i[2], 
               'length': i[3], 
               'mismatches': i[4], 
               'gap_open_count': i[5], 
               'query_start': i[6], 
               'query_end': i[7], 
               'subject_start': i[8], 
               'subject_end': i[9], 
               'evalue': i[10], 
               'BitScore': i[11]})
        except:
            alignments[i[0].split('|')[1]] = [
             {'dbquery': i[0].split('|')[0], 'dbsubject': i[1].split('|')[0], 
                'subject': i[1].split('|')[1], 
                'identity': i[2], 
                'length': i[3], 
                'mismatches': i[4], 
                'gap_open_count': i[5], 
                'query_start': i[6], 
                'query_end': i[7], 
                'subject_start': i[8], 
                'subject_end': i[9], 
                'evalue': i[10], 
                'BitScore': i[11]}]

    json.dump(alignments, open(fname + '.json', 'w'))
    return alignments


def best_hit(hits, db=None):
    hits = [ i for i in hits if i['dbsubject'] != 'RESFAMS' ]
    if db == 'ARDB':
        hits = [ i for i in hits if i['dbsubject'] != 'ARDB' ]
    if not hits:
        return False
    bhit = hits[0]
    for hit in hits:
        if float(hit['BitScore']) > float(bhit['BitScore']):
            bhit = hit

    return (
     bhit, bhit)


class consensus_type:

    def __init__(self, clusters, metadata, alignments):
        self.type = {}
        self.protein_ids = {cluster['protein_id']:cluster['identity'] for cluster in clusters}
        for cnt, protein_id in enumerate(self.protein_ids):
            try:
                self.type[metadata[protein_id][0]['type']]['freq'] += 1
                self.type[metadata[protein_id][0]['type']]['count'] += 1
                (self.type[metadata[protein_id][0]['type']]['avg_identity'].append(self.protein_ids[protein_id]),)
                self.type[metadata[protein_id][0]['type']]['protein_id'].append(protein_id)
            except:
                try:
                    self.type[metadata[protein_id][0]['type']] = {'freq': 1, 
                       'count': 1, 
                       'avg_identity': [
                                      self.protein_ids[protein_id]], 
                       'protein_id': [
                                    protein_id]}
                except:
                    pass

        for i in self.type:
            self.type[i]['freq'] = 100 * round(self.type[i]['freq'] / float(cnt + 1), 2)
            self.type[i]['avg_identity'] = round(sum(self.type[i]['avg_identity']) / float(len(self.type[i]['avg_identity'])), 2)

        self.bstype = {}
        for tp in self.type:
            protmd = {}
            bhit1, bhit2 = None, None
            for pid in self.type[tp]['protein_id']:
                if metadata[pid][0]['database'] == 'UNIPROT':
                    try:
                        hits = alignments[pid]
                        bhit1, bhit2 = best_hit(hits, metadata[pid])
                        bhm1, bhm2 = metadata[bhit1['subject']], metadata[bhit2['subject']]
                        protmd.update({pid: [metadata[pid][0], bhit1, bhm1]})
                    except:
                        info = metadata[pid][0]
                        protmd.update({pid: [info, None, None]})

                else:
                    protmd.update({pid: [metadata[pid][0], None, None]})

            self.bstype[tp] = protmd

        self.ctype = {i:{'freq': self.type[i]['freq'], 'iden': self.type[i]['avg_identity'], 'count': self.type[i]['count']} for i in self.type}
        return


def annotate2(gene_id, bhitm, bhit, factor, category):
    if bhitm[0]['type'] == 'Other' and category != 'unknown':
        Type = category
    else:
        Type = bhitm[0]['type']
    return {gene_id: {'type': Type, 'subtype': bhitm[0]['subType'], 
                 'bestHit': bhit['subject'], 
                 'AnFactor': factor, 
                 'prevType': category, 
                 'iden': bhit['identity'], 
                 'evalue': bhit['evalue'], 
                 'database': 'UNIPROT'}}


def cluster_annotation(cluster_stats, iden, evalue, metadata):
    DB = {}
    for category_name in cluster_stats.bstype.keys():
        category = cluster_stats.bstype[category_name]
        for gene_id in category:
            try:
                gene = category[gene_id]
                mtd = gene[0]
                bhit = gene[1]
                bhitm = gene[2]
                cnd = [ ai for ai in mtd['type'].split('---') if ai in bhitm[0]['type'].split('---') ]
                if cnd:
                    cnd = True
                else:
                    cnd = False
                if float(bhit['identity']) > iden:
                    DB.update(annotate2(gene_id, bhitm, bhit, 'High', category_name))
                elif cnd and float(bhit['evalue']) < evalue and bhit['identity'] >= 50:
                    DB.update(annotate2(gene_id, bhitm, bhit, 'Mid', category_name))
                elif float(bhit['evalue']) < evalue and cnd and bhit['identity'] < 50:
                    DB.update(annotate2(gene_id, bhitm, bhit, 'Manual Inspection', category_name))
                else:
                    DB.update(annotate2(gene_id, bhitm, bhit, 'Low', category_name))
            except Exception as inst:
                if metadata[gene_id][0]['database'] == 'UNIPROT':
                    DB.update({gene_id: {'type': 'unknown', 'subtype': 'unknown', 
                                 'bestHit': 'unknown', 
                                 'AnFactor': 'Low', 
                                 'prevType': metadata[gene_id][0]['type'], 
                                 'iden': 0, 
                                 'evalue': 1, 
                                 'database': 'UNIPROT-NO-MATCHES'}})
                else:
                    DB.update({gene_id: {'type': metadata[gene_id][0]['type'], 'subtype': metadata[gene_id][0]['subType'], 
                                 'bestHit': gene_id, 
                                 'AnFactor': 'High', 
                                 'prevType': category_name, 
                                 'iden': 100, 
                                 'evalue': 0, 
                                 'database': metadata[gene_id][0]['database']}})

    return DB


def get_hits_selF(query, alignments, SF):
    matches = alignments[query]
    MT = {}
    MT[query] = {}
    for match in matches:
        try:
            if SF[match['subject']]:
                MT[query].update({match['subject']: float(match['BitScore'])})
        except:
            pass

    return MT


def validate(data, alignments, Features, clf):
    SF = {i:1 for i in Features}
    M = {}
    ft = data.keys()[0]
    featV = get_hits_selF(ft, alignments, SF)
    ax = {ft: {}}
    for i in SF:
        try:
            ax[ft].update({i: featV[ft][i]})
        except:
            ax[ft].update({i: 0})

    M.update(ax)
    for i in data.keys()[1:]:
        try:
            featV = get_hits_selF(i, alignments, SF)
            M.update(featV)
        except:
            M.update({i: {}})

    X = M.values()
    I = np.array(M.keys())
    Y = []
    for i in M:
        try:
            Y.append(data[i]['type'])
        except:
            pass

    h = DictVectorizer(sparse=False)
    X = h.fit_transform(X)
    X = X.astype(floatX)
    min_max_scaler = preprocessing.MinMaxScaler()
    X = min_max_scaler.fit_transform(X)
    proba = clf.predict_proba(X)
    preds = clf.predict(X)
    return {'clf': clf, 'x_test': X, 'y_test': Y, 
       'M': M, 'features': Features, 'preds': preds, 
       'proba': proba}


def get_hits(query, alignments):
    matches = alignments[query]
    MT = {}
    MT[query] = {}
    for match in matches:
        if query != match['subject']:
            MT[query].update({match['subject']: float(match['BitScore'])})

    return MT


def model(NDB, alignments):
    cls = {}
    for i in NDB:
        try:
            cls[NDB[i]['type']] += 1
        except:
            cls[NDB[i]['type']] = 1

    M = {}
    error_ids = []
    for i in NDB:
        try:
            M.update(get_hits(i, alignments))
        except:
            M.update({i: {i: 1000}})
            error_ids.append(i[0])

    X = M.values()
    Y = []
    cls2 = {}
    for i in M.keys():
        try:
            Y.append(NDB[i]['type'])
            cls2[NDB[i]['type']] += 1
        except:
            cls2[NDB[i]['type']] = 1

    Y_dict = {i:ix for ix, i in enumerate(set(Y))}
    Y_rev = {y:x for x, y in Y_dict.iteritems()}
    Y = np.array([ Y_dict[i] for i in Y ], dtype='int32')
    h = DictVectorizer(sparse=False)
    X = h.fit_transform(X)
    X = X.astype(floatX)
    print X.shape
    X = np.array(X, dtype='float32')
    feature_names = h.get_feature_names()
    min_max_scaler = preprocessing.MinMaxScaler()
    NX = min_max_scaler.fit_transform(X)
    clf = ExtraTreesClassifier(bootstrap=True)
    clf = clf.fit(NX, Y)
    model = SelectFromModel(clf, prefit=True)
    X_new = model.transform(NX)
    feature_dict = {feature_names[ix]:True for ix, i in enumerate(model.get_support()) if i == True}
    feature_names = feature_dict.keys()
    x_train, x_test, y_train, y_test = train_test_split(X_new, Y, test_size=0.3, random_state=0)
    sample_names = M.keys()
    X2 = []
    Y2 = []
    for ix, i in enumerate(x_test):
        try:
            a = feature_dict[sample_names[ix]]
        except:
            X2.append(x_test[ix])
            Y2.append(y_test[ix])

    x_test = np.array(X2, dtype='float32')
    y_test = np.array(Y2, dtype='int32')
    print 'dataset: ', X.shape, Y.shape
    print 'training set: ', x_train.shape, y_train.shape
    print 'testing set: ', x_test.shape, y_test.shape
    clf = NeuralNet(layers=[
     (
      layers.InputLayer, {'shape': (None, x_train.shape[1])}),
     (
      layers.DenseLayer, {'num_units': 800}),
     (
      layers.DropoutLayer, {'p': 0.3}),
     (
      layers.DenseLayer, {'num_units': 400}),
     (
      layers.DropoutLayer, {'p': 0.2}),
     (
      layers.DenseLayer, {'num_units': 200}),
     (
      layers.DropoutLayer, {'p': 0.1}),
     (
      layers.DenseLayer, {'num_units': 100}),
     (
      layers.DenseLayer,
      {'num_units': len(set(Y)), 'nonlinearity': lasagne.nonlinearities.softmax})], update=nesterov_momentum, update_learning_rate=0.01, update_momentum=0.9, regression=False, max_epochs=100, verbose=2)
    clf.fit(x_test, y_test)
    proba = clf.predict_proba(x_test)
    preds = clf.predict(x_test)
    print classification_report([ Y_rev[i] for i in y_test ], [ Y_rev[i] for i in preds ])
    return {'clf': clf, 'x_test': x_test, 'y_test': y_test, 
       'x_train': x_train, 'y_train': y_train, 'M': M, 'Y_dict': Y_dict, 'Y_rev': Y_rev, 
       'features': feature_names, 'preds': preds, 
       'proba': proba, 'error_ids': error_ids}


def annotation_optimization(NDB, D):
    clf = D['clf']
    x_test = D['x_test']
    y_test = D['y_test']
    Y_dict = D['Y_dict']
    Y_rev = D['Y_rev']
    M = D['M']
    min_prob = 0.5
    from operator import itemgetter
    for term in Y_rev.values():
        y_test_1 = y_test[(y_test == Y_dict[term])]
        x_test_1 = x_test[(y_test == Y_dict[term])]
        ids = np.array(M.keys())
        ids = ids[(y_test == Y_dict[term])]
        proba = clf.predict_proba(x_test_1)
        preds = clf.predict(x_test_1)
        print classification_report([ Y_rev[i] for i in y_test_1 ], [ Y_rev[i] for i in preds ])
        for px, prot in enumerate(proba):
            probp = [ [Y_rev[ix], i] for ix, i in enumerate(prot) ]
            probp = sorted(probp, key=itemgetter(1))
            if probp[(-1)][0] == term:
                continue
            for i in probp[-1:]:
                if i[1] >= min_prob:
                    NDB[ids[px]]['type'] = i[0]

    return NDB


def check_category(NDB, D, category, top):
    clf = D['clf']
    x_test = D['x_test']
    y_test = D['y_test']
    Y_dict = D['Y_dict']
    Y_rev = D['Y_rev']
    M = D['M']
    min_prob = 0.0
    from operator import itemgetter
    term = category
    y_test_1 = y_test[(y_test == Y_dict[term])]
    x_test_1 = x_test[(y_test == Y_dict[term])]
    ids = np.array(M.keys())
    ids = ids[(y_test == Y_dict[term])]
    proba = clf.predict_proba(x_test_1)
    preds = clf.predict(x_test_1)
    print classification_report([ Y_rev[i] for i in y_test_1 ], [ Y_rev[i] for i in preds ])
    for px, prot in enumerate(proba):
        probp = [ [Y_rev[ix], i] for ix, i in enumerate(prot) ]
        probp = sorted(probp, key=itemgetter(1))
        for i in probp[-1 * top:]:
            if i[1] >= min_prob:
                NDB[ids[px]]['type'] = i[0]
            print ids[px], term, i

    return NDB


from pylab import *
import numpy as np

def inspect_protein(metadata, alignments, protein, identity):
    data = [ metadata[i['subject']][0] for i in alignments[protein] if float(i['identity']) > identity ]
    pie1 = {}
    for i in data:
        try:
            pie1[i['type']] += 1
        except:
            pie1[i['type']] = 1

    figure(1)
    ax = axes([0.1, 0.1, 0.8, 0.8])
    labels = pie1.keys()
    fracs = np.array(pie1.values()) / float(len(pie1))
    pie(fracs, labels=labels, autopct='%1.1f%%', shadow=True, startangle=90)
    show()
    figure(2)
    histx = [ [float(i['identity']), metadata[i['subject']][0]['type']] for i in alignments[protein] if float(i['identity']) > identity ]
    hist([ i[0] for i in histx ], 50)
    show()


def correct_split(CN, NDB):
    CN.update({'unknown': 'unknown'})
    CN.update({'other': 'unknown'})
    CN.update({'t_choride': 'chloride'})
    CN.update({'chloride': 'chloride'})
    CN.update({'tetracyclin': 'tetracycline'})
    CN.update({'rifampicin': 'rifampin'})
    CN.update({'cationic_peptides': 'peptide'})
    CN.update({'tetracenomycin': 'tetracenomycin'})
    CN.update({'aminocumarin': 'aminocoumarin'})
    CN.update({'lipopeptide': 'peptide'})
    CN.update({'cabapenem': 'beta_lactam'})
    CN.update({'hygromycin': 'aminoglycoside'})
    CN.update({'apamycin': 'apramycin'})
    TPD = {}
    TPO = {}
    for i in NDB:
        ntp = {}
        for tp in NDB[i]['type'].split('---'):
            ntp.update({CN[tp.lower()]: 1})

        NDB[i]['prev1type'] = NDB[i]['type']
        if len(ntp) > 1:
            TPD.update({i: NDB[i]})
            TPD[i]['type'] = ('--').join(ntp.keys())
            TPO.update({i: NDB[i]})
            TPO[i]['type'] = 'multidrug'
            print i, '\t', ntp.keys()
        else:
            TPO.update({i: NDB[i]})
            TPO[i]['type'] = ('--').join(ntp.keys())

    return [TPD, TPO]


def check_predictions(deepT, deepL, top, min_prob):
    from operator import itemgetter
    r_pred = []
    for px, prot in enumerate(deepT['proba']):
        probp = [ [deepL['Y_rev'][ix], i] for ix, i in enumerate(prot) ]
        probp = sorted(probp, key=itemgetter(1))
        for i in probp[-1 * top:]:
            r_pred.append([deepT['samples'][px]] + i + [deepT['Y'][px]])

    return r_pred


def plot_confusion_matrix(cm, title='Confusion matrix', cmap=plt.cm.Blues):
    plt.imshow(cm, interpolation='nearest', cmap=cmap)
    plt.title(title)
    plt.colorbar()
    plt.tight_layout()
    plt.ylabel('True label')
    plt.xlabel('Predicted label')
    plt.show()