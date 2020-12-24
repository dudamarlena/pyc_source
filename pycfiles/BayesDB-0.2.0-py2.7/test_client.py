# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.10-intel/egg/bayesdb/tests/test_client.py
# Compiled at: 2015-02-12 15:25:14
import time, inspect, sys, pickle, os, numpy, pytest, random, shutil, pandas
from cStringIO import StringIO
import bayesdb.utils as utils
from bayesdb.client import Client
from bayesdb.engine import Engine
import bayesdb.bql_grammar as bql
test_tablenames = None
client = None
test_filenames = None

def setup_function(function):
    global client
    global test_filenames
    global test_tablenames
    test_tablenames = []
    test_filenames = []
    client = Client(testing=True)


def teardown_function(function):
    for test_tablename in test_tablenames:
        client.engine.drop_btable(test_tablename)

    for test_filename in test_filenames:
        if os.path.exists(test_filename):
            os.remove(test_filename)


def create_dha(path='data/dha.csv', key_column=0):
    test_tablename = 'dhatest' + str(int(time.time() * 1000000)) + str(int(random.random() * 10000000))
    csv_file_contents = open(path, 'r').read()
    client('create btable %s from %s' % (test_tablename, path), debug=True, pretty=False, key_column=key_column)
    test_tablenames.append(test_tablename)
    return test_tablename


def test_drop_btable():
    """
  Test to make sure drop btable prompts the user for confirmation, and responds appropriately when
  given certain input.
  """
    import sys
    from cStringIO import StringIO
    backup = sys.stdout
    sys.stdout = StringIO()
    out = sys.stdout.getvalue()
    sys.stdout.close()
    sys.stdout = backup


def test_btable_list():
    global client
    out = set(client('list btables', pretty=False, debug=True)[0]['btable'])
    init_btable_count = len(out)
    test_tablename1 = create_dha()
    out = set(client('list btables', pretty=False, debug=True)[0]['btable'])
    assert len(out) == 1 + init_btable_count
    assert test_tablename1 in out
    test_tablename2 = create_dha()
    out = set(client('list btables', pretty=False, debug=True)[0]['btable'])
    assert len(out) == 2 + init_btable_count
    assert test_tablename1 in out
    assert test_tablename2 in out
    client('drop btable %s' % test_tablename1, yes=True, debug=True, pretty=False)
    out = set(client('list btables', pretty=False, debug=True)[0]['btable'])
    assert len(out) == 1 + init_btable_count
    assert test_tablename1 not in out
    assert test_tablename2 in out
    del client
    client = Client()
    out = set(client('list btables', pretty=False, debug=True)[0]['btable'])
    assert len(out) == 1 + init_btable_count
    assert test_tablename1 not in out
    assert test_tablename2 in out


def test_save_and_load_models():
    test_tablename1 = create_dha()
    test_tablename2 = create_dha()
    client('initialize 2 models for %s' % test_tablename1, debug=True, pretty=False)
    pkl_path = 'test_models.pkl.gz'
    test_filenames.append(pkl_path)
    client('save models from %s to %s' % (test_tablename1, pkl_path), debug=True, pretty=False)
    original_models = client.engine.save_models(test_tablename1)
    client('load models %s into %s' % (pkl_path, test_tablename2), debug=True, pretty=False)
    new_models = client.engine.save_models(test_tablename2)
    assert new_models.values() == original_models.values()
    client('load models %s into %s' % (pkl_path, test_tablename2), debug=True, pretty=False)
    test_tablename3 = create_dha()
    client('update schema for %s set qual_score = categorical' % test_tablename3, debug=True, pretty=False)
    client('load models %s into %s' % (pkl_path, test_tablename3), debug=True, pretty=False)
    test_tablename4 = create_dha()
    client('update schema for %s set qual_score = categorical' % test_tablename4, debug=True, pretty=False)
    client('initialize 2 models for %s' % test_tablename4, debug=True, pretty=False)
    with pytest.raises(utils.BayesDBError):
        client('load models %s into %s' % (pkl_path, test_tablename4), debug=True, pretty=False)


def test_column_lists():
    """ smoke test """
    test_tablename = create_dha()
    client('initialize 2 models for %s' % test_tablename, debug=True, pretty=False)
    cname1 = 'cname1'
    cname2 = 'cname2'
    client('show column lists for %s' % test_tablename, debug=True, pretty=False)
    out = client('estimate columns from %s as %s' % (test_tablename, cname1), debug=True, pretty=False)[0]
    assert type(out) == pandas.DataFrame
    assert (out.columns == ['column label', 'column name']).all()
    client('show column lists for %s' % test_tablename, debug=True, pretty=False)
    out = client('estimate columns from %s order by typicality limit 5 as %s' % (test_tablename, cname1), debug=True, pretty=False)[0]
    assert out.shape == (5, 3)
    client('estimate columns from %s limit 5 as %s' % (test_tablename, cname2), debug=True, pretty=False)
    client('show column lists for %s' % test_tablename, debug=True, pretty=False)
    tmp = 'asdf_test.png'
    test_filenames.append(tmp)
    if os.path.exists(tmp):
        os.remove(tmp)
    client('estimate pairwise dependence probability from %s for %s save to %s' % (test_tablename, cname1, tmp), debug=True, pretty=False)
    test_ast = bql.bql_statement.parseString('estimate pairwise dependence probability from %s for %s save to %s' % (test_tablename, cname1, tmp), parseAll=True)
    assert test_ast.filename == 'asdf_test.png'
    client('estimate pairwise dependence probability from %s for %s' % (test_tablename, cname2), debug=True, pretty=False)
    client('select %s from %s limit 10' % (cname1, test_tablename), debug=True, pretty=False)
    client('select %s from %s limit 10' % (cname2, test_tablename), debug=True, pretty=False)
    client('infer %s from %s with confidence 0.1 limit 10' % (cname1, test_tablename), debug=True, pretty=False)
    client('infer %s from %s with confidence 0.1 limit 10' % (cname2, test_tablename), debug=True, pretty=False)
    client('simulate %s from %s times 10' % (cname1, test_tablename), debug=True, pretty=False)
    client('simulate %s from %s times 10' % (cname2, test_tablename), debug=True, pretty=False)
    client('drop column list %s from %s' % (cname1, test_tablename), debug=True, pretty=False)
    client('drop column list %s from %s' % (cname2, test_tablename), debug=True, pretty=False)
    out = client('show column lists for %s' % test_tablename, debug=True, pretty=False)[0]
    assert out.shape == (0, 1)


def test_simulate():
    """ smoke test """
    test_tablename = create_dha()
    client('initialize 2 models for %s' % test_tablename, debug=True, pretty=False)
    assert len(client("simulate qual_score from %s given name='Albany NY' times 5" % test_tablename, debug=True, pretty=False)[0]) == 5
    assert len(client("simulate qual_score from %s given name='Albany NY' and ami_score = 80 times 5" % test_tablename, debug=True, pretty=False)[0]) == 5
    assert len(client("simulate name from %s given name='Albany NY' and ami_score = 80 times 5" % test_tablename, debug=True, pretty=False)[0]) == 5
    assert len(client("simulate name from %s given name='Albany NY', ami_score = 80 times 5" % test_tablename, debug=True, pretty=False)[0]) == 5
    assert len(client("simulate name from %s given name='Albany NY' AND ami_score = 80 times 5" % test_tablename, debug=True, pretty=False)[0]) == 5
    assert len(client('simulate name from %s given ami_score = 80 times 5' % test_tablename, debug=True, pretty=False)[0]) == 5


def test_estimate_columns():
    """ smoke test """
    test_tablename = create_dha()
    client('initialize 2 models for %s' % test_tablename, debug=True, pretty=False)
    client('estimate columns from %s where typicality > 1' % test_tablename, debug=True, pretty=False)
    client('estimate columns from %s where typicality > 0' % test_tablename, debug=True, pretty=False)
    client('estimate columns from %s where typicality > 0 order by typicality' % test_tablename, debug=True, pretty=False)
    client('estimate columns from %s where dependence probability with qual_score > 0' % test_tablename, debug=True, pretty=False)
    client('estimate columns from %s order by dependence probability with qual_score' % test_tablename, debug=True, pretty=False)
    client('estimate columns from %s order by dependence probability with qual_score limit 5' % test_tablename, debug=True, pretty=False)
    out = client('estimate columns from %s order by correlation with qual_score limit 5' % test_tablename, debug=True, pretty=False)[0]
    scores = out['correlation with qual_score']
    assert (0 <= scores).all() and (scores <= 1).all()
    out = client('estimate columns from %s where correlation with qual_score > 0 order by correlation with qual_score limit 5' % test_tablename, debug=True, pretty=False)[0]
    scores = out['correlation with qual_score']
    assert (0 <= scores).all() and (scores <= 1).all()
    client('estimate columns from %s order by mutual information with qual_score limit 5' % test_tablename, debug=True, pretty=False)
    client('estimate columns from %s where mutual information with qual_score > 1 order by typicality' % test_tablename, debug=True, pretty=False)


def test_row_clusters():
    """ smoke test """
    test_tablename = create_dha()
    client('initialize 2 models for %s' % test_tablename, debug=True, pretty=False)
    row_lists = client('show row lists for %s' % test_tablename, debug=True, pretty=False)[0]
    assert row_lists.shape == (0, 2)
    client('estimate pairwise row similarity from %s save clusters with threshold 0.1 as rcc' % test_tablename, debug=True, pretty=False)
    row_lists = client('show row lists for %s' % test_tablename, debug=True, pretty=False)[0]
    assert row_lists.shape[0] > 0
    client('select * from %s where key in rcc_0' % test_tablename, debug=True, pretty=False)
    client('drop row list rcc from %s' % test_tablename, debug=True, pretty=False)
    out = client('show row lists for %s' % test_tablename, debug=True, pretty=False)[0]
    assert out.shape == (0, 2)


def test_select_whereclause_functions():
    """ smoke test """
    test_tablename = create_dha()
    client('initialize 2 models for %s' % test_tablename, debug=True, pretty=False)
    client('select name from %s where similarity to 0 > 0' % test_tablename, debug=True, pretty=False)
    client('select name from %s where similarity to 0 = 0 order by similarity to 0' % test_tablename, debug=True, pretty=False)
    client('select name from %s where similarity to 1 with respect to qual_score > 0.01' % test_tablename, debug=True, pretty=False)
    client('select name from %s where similarity to 1 with respect to qual_score, ami_score > 0.01' % test_tablename, debug=True, pretty=False)
    client('select * from %s where typicality > 0.04' % test_tablename, debug=True, pretty=False)
    client('select *, typicality from %s where typicality > 0.06' % test_tablename, debug=True, pretty=False)
    client('select qual_score from %s where predictive probability of qual_score > 0.01' % test_tablename, debug=True, pretty=False)
    client('select qual_score from %s where predictive probability of name > 0.01' % test_tablename, debug=True, pretty=False)
    with pytest.raises(utils.BayesDBError):
        client('select qual_score from %s where probability of qual_score = 6 > 0.01' % test_tablename, debug=True, pretty=False)
    with pytest.raises(utils.BayesDBError):
        client("select qual_score from %s where probability of name='Albany NY' > 0.01" % test_tablename, debug=True, pretty=False)


def test_model_config():
    test_tablename = create_dha()
    client('initialize 2 models for %s with config naive bayes' % test_tablename, debug=True, pretty=False)
    client.engine.analyze(test_tablename, model_indices=[0], iterations=2, background=False)
    dep_mat = client('estimate pairwise dependence probability from %s' % test_tablename, debug=True, pretty=False)[0]['matrix']
    assert numpy.all(dep_mat == numpy.identity(dep_mat.shape[0]))
    with pytest.raises(utils.BayesDBNoModelsError):
        client('drop models from %s' % test_tablename, yes=True, debug=True, pretty=False)
    client('initialize 2 models for %s with config crp mixture' % test_tablename, debug=True, pretty=False)
    client.engine.analyze(test_tablename, model_indices='all', iterations=2, background=False)
    dep_mat = client('estimate pairwise dependence probability from %s' % test_tablename, debug=True, pretty=False)[0]['matrix']
    assert numpy.all(dep_mat == 1)
    with pytest.raises(utils.BayesDBNoModelsError):
        client('drop models from %s' % test_tablename, yes=True, debug=True, pretty=False)
    client('initialize 2 models for %s' % test_tablename, debug=True, pretty=False)
    client.engine.analyze(test_tablename, model_indices='all', iterations=2, background=False)
    dep_mat = client('estimate pairwise dependence probability from %s' % test_tablename, debug=True, pretty=False)[0]['matrix']
    assert not numpy.all(dep_mat == 1) and not numpy.all(dep_mat == 0)
    with pytest.raises(utils.BayesDBError):
        client.engine.initialize_models(test_tablename, 2, 'crp mixture')


@pytest.mark.xfail
def test_analyze():
    """ test designed to make sure that analyze in background runs correct number of iterations """
    test_tablename = create_dha(key_column=1)
    models = 3
    out = client('initialize %d models for %s' % (models, test_tablename), debug=True, pretty=False)[0]
    iterations = 3
    out = client('analyze %s for %d iterations' % (test_tablename, iterations), debug=True, pretty=False)[0]
    out = ''
    while 'not currently being analyzed' not in out:
        out = client('show analyze for %s' % test_tablename, debug=True, pretty=False)[0]['message']

    models = client('show models for %s' % test_tablename, debug=True, pretty=False)[0]['models']
    iters_by_model = [ v for k, v in models ]
    for i in iters_by_model:
        assert i == iterations


def test_using_models():
    """ smoke test """
    test_tablename = create_dha(path='data/dha_missing.csv')
    client('initialize 3 models for %s' % test_tablename, debug=True, pretty=False)
    client('select name from %s using model 1' % test_tablename, debug=True, pretty=False)
    with pytest.raises(utils.BayesDBError):
        client('infer name from %s with confidence 0.1 using models 3' % test_tablename, debug=True, pretty=False)
    with pytest.raises(utils.BayesDBError):
        client("simulate qual_score from %s given name='Albany NY' times 5 using models 3" % test_tablename, debug=True, pretty=False)
    with pytest.raises(utils.BayesDBError):
        client('infer name from %s with confidence 0.1 using models 0-3' % test_tablename, debug=True, pretty=False)
    client('infer name from %s with confidence 0.1 limit 10 using models 2' % test_tablename, debug=True, pretty=False)
    client("simulate qual_score from %s given name='Albany NY' times 5 using models 1-2" % test_tablename, debug=True, pretty=False)
    client('estimate columns from %s limit 5 using models 1-2' % test_tablename, debug=True, pretty=False)
    client('estimate pairwise dependence probability from %s using models 1' % test_tablename, debug=True, pretty=False)
    client('estimate pairwise row similarity from %s save clusters with threshold 0.1 as rcc using models 1-2' % test_tablename, debug=True, pretty=False)
    client('drop model 0 from %s' % test_tablename, debug=True, pretty=False, yes=True)
    with pytest.raises(utils.BayesDBError):
        client('infer name from %s with confidence 0.1 limit 10 using models 0-2' % test_tablename, debug=True, pretty=False)


def test_select():
    """ smoke test """
    test_tablename = create_dha()
    client('initialize 2 models for %s' % test_tablename, debug=True, pretty=False)
    client('select name, qual_score from %s' % test_tablename, debug=True, pretty=False)
    client('select name, qual_score from %s limit 10' % test_tablename, debug=True, pretty=False)
    client('select name, qual_score from %s order by qual_score limit 10' % test_tablename, debug=True, pretty=False)
    client('select name, qual_score from %s order by qual_score ASC limit 10' % test_tablename, debug=True, pretty=False)
    client('select name, qual_score from %s order by qual_score DESC limit 10' % test_tablename, debug=True, pretty=False)
    client('select * from %s order by qual_score DESC limit 10' % test_tablename, debug=True, pretty=False)
    client('select name, qual_score from %s where qual_score > 6' % test_tablename, debug=True, pretty=False)
    client('select * from %s where qual_score > 6' % test_tablename, debug=True, pretty=False)
    client("select * from %s where qual_score > 80 and name = 'Albany NY'" % test_tablename, debug=True, pretty=False)
    client('select * from %s where qual_score > 80 and ami_score > 85' % test_tablename, debug=True, pretty=False)
    client('estimate columns from %s limit 5 as clist' % test_tablename, debug=True, pretty=False)
    client('select name, similarity to 0 from %s' % test_tablename, debug=True, pretty=False)
    client('select name from %s order by similarity to 0' % test_tablename, debug=True, pretty=False)
    client('select name, similarity to 0 from %s order by similarity to 0' % test_tablename, debug=True, pretty=False)
    client('select name, similarity to 0 with respect to name from %s order by similarity to 1 with respect to qual_score' % test_tablename, debug=True, pretty=False)
    client('select name, similarity to 0 from %s order by similarity to 1 with respect to qual_score, ami_score' % test_tablename, debug=True, pretty=False)
    client('select name, similarity to 0 from %s order by similarity to 1 with respect to clist' % test_tablename, debug=True, pretty=False)
    out1 = client('select name, qual_score, similarity to 161 from %s order by similarity to 161 limit 5' % test_tablename, debug=True, pretty=False)[0]
    out2 = client('select name, qual_score, similarity to name = "McAllen TX" from %s order by similarity to name = "McAllen TX" limit 5' % test_tablename, debug=True, pretty=False)[0]
    out3 = client('select name, qual_score, similarity to key = 161 from %s order by similarity to key = 161 limit 5' % test_tablename, debug=True, pretty=False)[0]
    for col_idx in range(out1.shape[1]):
        assert (out1.iloc[col_idx] == out2.iloc[col_idx]).all()
        assert (out2.iloc[col_idx] == out3.iloc[col_idx]).all()

    client('select typicality from %s' % test_tablename, debug=True, pretty=False)
    client('select *, typicality from %s' % test_tablename, debug=True, pretty=False)
    client('select typicality from %s order by typicality limit 10' % test_tablename, debug=True, pretty=False)
    st = time.time()
    client('select probability of qual_score = 6 from %s' % test_tablename, debug=True, pretty=False)
    el = time.time() - st
    st = time.time()
    client("select probability of name='Albany NY' from %s" % test_tablename, debug=True, pretty=False)
    el2 = time.time() - st
    client('select predictive probability of qual_score from %s' % test_tablename, debug=True, pretty=False)
    client('select predictive probability of name from %s' % test_tablename, debug=True, pretty=False)
    client('select predictive probability of qual_score from %s order by predictive probability of name' % test_tablename, debug=True, pretty=False)
    client('select predictive probability of qual_score from %s order by predictive probability of qual_score' % test_tablename, debug=True, pretty=False)
    client('select name, qual_score, mutual information of name with qual_score from %s' % test_tablename, debug=True, pretty=False)
    client('select dependence probability of name with qual_score from %s' % test_tablename, debug=True, pretty=False)
    client('select name, qual_score, dependence probability of name with qual_score from %s' % test_tablename, debug=True, pretty=False)
    client('select name, qual_score, correlation of name with qual_score from %s' % test_tablename, debug=True, pretty=False)
    client('select typicality of qual_score, typicality of name from %s' % test_tablename, debug=True, pretty=False)
    client('select typicality of qual_score from %s' % test_tablename, debug=True, pretty=False)
    test_tablename = create_dha(path='data/dha_missing.csv')
    client('select name, qual_score, correlation of name with qual_score from %s' % test_tablename, debug=True, pretty=False)


def test_into():
    test_tablename = create_dha()
    client('drop btable test_btable_select', yes=True)
    client('select name, qual_score from %s limit 5 into test_btable_select' % test_tablename, debug=True, pretty=False)
    out = client('select * from test_btable_select', debug=True, pretty=False)[0]
    assert len(out) == 5
    assert (out.columns == ['key', 'name', 'qual_score']).all()
    client('summarize select * from test_btable_select')
    client('label columns for test_btable_select set qual_score = quality')
    client('initialize 2 models for test_btable_select')
    client('analyze test_btable_select for 2 iterations')
    client('simulate * from test_btable_select times 5')
    client('drop btable test_btable_select', yes=True)


def test_pandas():
    test_tablename = create_dha()
    out = client('select name, qual_score from %s limit 10' % test_tablename, debug=True, pretty=False, pandas_output=False)
    assert type(out[0]) == dict
    out = client('select name, qual_score from %s limit 10' % test_tablename, debug=True, pretty=False)
    assert type(out[0]) == pandas.DataFrame
    client('select name, qual_score from %s where qual_score < 0' % test_tablename, debug=True, pretty=False)
    test_df = out[0]
    client('drop btable %s' % test_tablename, yes=True)
    client('create btable %s from pandas' % test_tablename, debug=True, pretty=False, pandas_df=test_df, key_column=1)


def test_summarize():
    test_tablename = create_dha()
    out = client('summarize select name, qual_score from %s' % test_tablename, debug=True, pretty=False)[0]
    assert type(out) == pandas.DataFrame
    assert (out.columns == ['', 'name', 'qual_score']).all()
    expected_indices = [
     'type', 'count', 'unique', 'mean', 'std', 'min', '25%', '50%', '75%', 'max',
     'mode', 'prob_mode']
    assert all([ x in list(out['']) for x in expected_indices ])
    client('initialize 2 models for %s' % test_tablename, debug=True, pretty=False)
    client('summarize select correlation of name with qual_score from %s' % test_tablename, debug=True, pretty=False)
    out = client('summarize select name, qual_score from %s limit 3' % test_tablename, debug=True, pretty=False)[0]
    assert out.shape == (12, 3)
    out = client('summarize select name, qual_score from %s where qual_score < 0' % test_tablename, debug=True, pretty=False)[0]
    assert out.shape == (0, 3)
    client('summarize select name from %s' % test_tablename, debug=True, pretty=False)
    client('summarize select qual_score from %s' % test_tablename, debug=True, pretty=False)


def test_select_where_col_equal_val():
    test_tablename = create_dha()
    client('initialize 2 models for %s' % test_tablename, debug=True, pretty=False)
    basic_similarity = client('select * from %s where similarity to 1 > .6 limit 5' % test_tablename, pretty=False, debug=True)[0]['key']
    col_val_similarity = client('select * from %s where similarity to name = "Akron OH" > .6 limit 5' % test_tablename, pretty=False, debug=True)[0]['key']
    assert len(basic_similarity) == len(col_val_similarity)


def test_labeling():
    test_tablename = create_dha()
    client('label columns for %s set name = Name of the hospital, qual_score = Overall quality score' % test_tablename, debug=True, pretty=False)
    client('show label for %s name, qual_score' % test_tablename, debug=True, pretty=False)
    client('show label for %s' % test_tablename, debug=True, pretty=False)
    client('label columns for %s from data/dha_labels.csv' % test_tablename, debug=True, pretty=False)


def test_user_metadata():
    test_tablename = create_dha()
    client('update metadata for %s set data_source = Dartmouth Atlas of Health, url = http://www.dartmouthatlas.org/tools/downloads.aspx' % test_tablename, debug=True, pretty=False)
    client('update metadata for %s from data/dha_user_metadata.csv' % test_tablename, debug=True, pretty=False)
    client('show metadata for %s data_source, url' % test_tablename, debug=True, pretty=False)
    client('show metadata for %s' % test_tablename, debug=True, pretty=False)


def test_freq_hist():
    test_tablename = create_dha()
    out = client('freq select qual_score from %s' % test_tablename, debug=True, pretty=False)[0]
    assert type(out) == pandas.DataFrame
    assert out['qual_score'][0] == 87.5
    assert out['frequency'][0] == 7
    out = client('hist select qual_score from %s' % test_tablename, debug=True, pretty=False)[0]
    assert type(out) == pandas.DataFrame
    assert out.shape == (10, 4)
    assert out['frequency'][0] == 1
    client('initialize 2 models for %s' % test_tablename, debug=True, pretty=False)
    client.engine.analyze(tablename=test_tablename, iterations=2, background=False)
    out = client('freq infer qual_score from %s with confidence 0' % test_tablename, debug=True, pretty=False)[0]
    assert type(out) == pandas.DataFrame
    assert out['qual_score'][0] == 87.5
    assert out['frequency'][0] == 7
    out = client('hist infer qual_score from %s with confidence 0' % test_tablename, debug=True, pretty=False)[0]
    assert type(out) == pandas.DataFrame
    assert out.shape == (10, 4)
    assert out['frequency'][0] == 1
    out = client('freq simulate qual_score from %s times 20' % test_tablename, debug=True, pretty=False)[0]
    assert out.shape[1] == 3
    assert (out['probability'] < 1).all()
    out = client('hist simulate qual_score from %s times 20' % test_tablename, debug=True, pretty=False)[0]
    assert out.shape[1] == 4
    assert (out['frequency'] <= 20).all()
    assert (out['probability'] < 1).all()


def test_update_schema():
    test_tablename = create_dha()
    out = client('update schema for %s set qual_score = ignore, ami_score = categorical, pneum_score = cyclic(0, 100)' % test_tablename, debug=True, pretty=False)[0]
    assert (out['datatype'][(out['column'] == 'qual_score')] == 'ignore').all()
    assert (out['datatype'][(out['column'] == 'ami_score')] == 'categorical').all()
    assert (out['datatype'][(out['column'] == 'pneum_score')] == 'cyclic').all()
    out = client('update schema for %s set name = categorical(350)' % test_tablename, debug=True, pretty=False)[0]
    assert (out['datatype'][(out['column'] == 'name')] == 'categorical').all()
    client('select qual_score from %s' % test_tablename, debug=True, pretty=False)
    out = client('select name, qual_score, ami_score from %s where qual_score > 90 order by qual_score' % test_tablename, debug=True, pretty=False)[0]
    assert (out['qual_score'] > 90).all()
    assert (out['qual_score'] == out['qual_score'].order(ascending=False)).all()
    client('update schema for %s set name = ignore' % test_tablename, debug=True, pretty=False)
    out = client('select name, qual_score from %s where name = "Albany NY"' % test_tablename, debug=True, pretty=False)[0]
    assert out.shape == (1, 3)
    assert (out['name'] == 'Albany NY').all()
    client('update schema for %s set qual_score = numerical, ami_score = numerical, pneum_score = numerical, total_fte = numerical' % test_tablename, debug=True, pretty=False)
    client('update schema for %s set qual_score = ignore' % test_tablename, debug=True, pretty=False)
    client('initialize 2 models for %s' % test_tablename, debug=True, pretty=False)
    client.engine.analyze(tablename=test_tablename, iterations=2, background=False)
    with pytest.raises(utils.BayesDBError):
        client('estimate columns from %s order by correlation with qual_score limit 5' % test_tablename, debug=True, pretty=False)
        client('estimate columns from %s order by dependence probability with qual_score limit 5' % test_tablename, debug=True, pretty=False)
        client('update schema for %s set name = key' % test_tablename, debug=True, pretty=False)
        client('update schema for %s set key = numerical' % test_tablename, debug=True, pretty=False)
        client('update schema for %s set name = categorical(3)' % test_tablename, debug=True, pretty=False)
        client('update schema for %s set qual_score = cyclic(0, 10)' % test_tablename, debug=True, pretty=False)