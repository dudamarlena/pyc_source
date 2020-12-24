# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.10-intel/egg/bayesdb/tests/test_engine.py
# Compiled at: 2015-02-12 15:25:14
import time, inspect, pickle, os, numpy, pytest, random, bayesdb.diagnostics_utils as diag_utils, bayesdb.data_utils as data_utils
from bayesdb.client import Client
from bayesdb.engine import Engine
from bayesdb.parser import Parser
import bayesdb.bql_grammar as bql, bayesdb.utils as utils
engine = Engine()
parser = Parser()
test_tablenames = None
notimplemented = pytest.mark.skipif(True, reason='Test not implemented')

def setup_function(function):
    global engine
    global test_tablenames
    test_tablenames = []
    engine = Engine()


def teardown_function(function):
    for test_tablename in test_tablenames:
        engine.drop_btable(test_tablename)


def create_dha(path='data/dha.csv'):
    test_tablename = 'dhatest' + str(int(time.time() * 1000000)) + str(int(random.random() * 10000000))
    header, rows = data_utils.read_csv(path)
    create_btable_result = engine.create_btable(test_tablename, header, rows, key_column=0)
    test_tablenames.append(test_tablename)
    return (
     test_tablename, create_btable_result)


def create_describe_btable(data_path='data/describe.csv', codebook_path='data/describe_codebook.csv', use_codebook=True):
    test_tablename = 'describetest' + str(int(time.time() * 1000000)) + str(int(random.random() * 10000000))
    if use_codebook:
        codebook_header, codebook_rows = data_utils.read_csv(codebook_path)
        codebook = dict()
        for codebook_row in codebook_rows:
            codebook[codebook_row[0]] = dict(zip(['short_name', 'description', 'value_map'], codebook_row[1:]))

    else:
        codebook = None
    header, rows = data_utils.read_csv(data_path)
    create_btable_result = engine.create_btable(test_tablename, header, rows, key_column=0, codebook=codebook)
    test_tablenames.append(test_tablename)
    return (
     test_tablename, create_btable_result)


def test_create_btable():
    test_tablename, create_btable_result = create_dha()
    assert 'column_labels' in create_btable_result
    assert 'data' in create_btable_result
    assert 'message' in create_btable_result
    assert len(create_btable_result['data']) == 65
    assert len(create_btable_result['data'][0]) == 3
    list_btables_result = engine.list_btables()['data']
    assert [test_tablename] in list_btables_result
    engine.drop_btable(test_tablename)


def test_drop_btable():
    test_tablename, _ = create_dha()
    list_btables_result = engine.list_btables()['data']
    assert [test_tablename] in list_btables_result
    engine.drop_btable(test_tablename)
    list_btables_result = engine.list_btables()['data']
    assert [test_tablename] not in list_btables_result


def test_select():
    test_tablename, _ = create_dha()
    functions = bql.bql_statement.parseString('select name, qual_score from test', parseAll=True).functions
    whereclause = None
    limit = float('inf')
    order_by = False
    select_result = engine.select(test_tablename, functions, whereclause, limit, order_by, None)
    assert 'column_labels' in select_result
    assert 'data' in select_result
    assert select_result['column_labels'] == ['key', 'name', 'qual_score']
    assert len(select_result['data']) == 307 and len(select_result['data'][0]) == len(select_result['column_labels'])
    assert type(select_result['data'][0][0]) == numpy.string_
    t = type(select_result['data'][0][1])
    assert t == unicode or t == str or t == numpy.string_
    assert type(select_result['data'][0][2]) == float
    original_select_result = select_result['data']
    limit = 10
    select_result = engine.select(test_tablename, functions, whereclause, limit, order_by, None)
    assert len(select_result['data']) == limit
    ground_truth_ordered_results = sorted(original_select_result, key=lambda t: t[2], reverse=True)[:10]
    order_by = [('qual_score', True)]
    order_by = bql.bql_statement.parseString('select name, qual_score, similarity to 5 from test order by qual_score desc', parseAll=True).order_by
    select_result = engine.select(test_tablename, functions, whereclause, limit, order_by, None)
    assert select_result['data'] == ground_truth_ordered_results
    ground_truth_ordered_results = sorted(original_select_result, key=lambda t: t[2])[:10]
    order_by = [('qual_score', False)]
    order_by = bql.bql_statement.parseString('select name, qual_score, similarity to 5 from test order by qual_score asc', parseAll=True).order_by
    select_result = engine.select(test_tablename, functions, whereclause, limit, order_by, None)
    assert select_result['data'] == ground_truth_ordered_results
    engine.initialize_models(test_tablename, 2)
    functions = bql.bql_statement.parseString('select name, qual_score, similarity to 5 from test order by similarity to 5', parseAll=True).functions
    order_by = bql.bql_statement.parseString('select name, qual_score, similarity to 5 from test order by similarity to 5', parseAll=True).order_by
    select_result = engine.select(test_tablename, functions, whereclause, limit, order_by, None)
    functions = bql.bql_statement.parseString('select name, qual_score, similarity to 5 from test order by similarity to 5', parseAll=True).functions
    order_by = bql.bql_statement.parseString('select name, qual_score, similarity to 5 from test order by similarity to 5 with respect to qual_score', parseAll=True).order_by
    select_result = engine.select(test_tablename, functions, whereclause, limit, order_by, None)
    functions = bql.bql_statement.parseString('select name, qual_score from test', parseAll=True).functions
    order_by = bql.bql_statement.parseString('select * from test order by similarity to 5 with respect to qual_score', parseAll=True).order_by
    select_result = engine.select(test_tablename, functions, whereclause, limit, order_by, None)
    functions = bql.bql_statement.parseString('select name, qual_score, similarity to 5 with respect to name from test', parseAll=True).functions
    order_by = bql.bql_statement.parseString('select * from test order by similarity to 5', parseAll=True).order_by
    select_result = engine.select(test_tablename, functions, whereclause, limit, order_by, None)
    functions = bql.bql_statement.parseString("select name, qual_score, similarity to name='Albany NY' with respect to qual_score from test", parseAll=True).functions
    order_by = bql.bql_statement.parseString('select * from test order by similarity to 5', parseAll=True).order_by
    select_result = engine.select(test_tablename, functions, whereclause, limit, order_by, None)
    functions = bql.bql_statement.parseString('select * from test', parseAll=True).functions
    order_by = bql.bql_statement.parseString('select * from test order by similarity to 5 with respect to name', parseAll=True).order_by
    whereclause = bql.bql_statement.parseString('select * from test where qual_score > 6', parseAll=True).where_conditions
    select_result = engine.select(test_tablename, functions, whereclause, limit, order_by, None)
    whereclause = bql.bql_statement.parseString('select * from test where name="Albany NY"', parseAll=True).where_conditions
    functions = bql.bql_statement.parseString('select * from test', parseAll=True).functions
    order_by = bql.bql_statement.parseString('select * from test order by similarity to 5 with respect to name', parseAll=True).order_by
    select_result = engine.select(test_tablename, functions, whereclause, limit, order_by, None)
    order_by = False
    whereclause = None
    functions = bql.bql_statement.parseString('select name, qual_score, typicality from test', parseAll=True).functions
    select_result = engine.select(test_tablename, functions, whereclause, limit, order_by, None)
    functions = bql.bql_statement.parseString('select name, qual_score, typicality from test', parseAll=True).functions
    order_by = bql.bql_statement.parseString('select * from test order by typicality', parseAll=True).order_by
    select_result = engine.select(test_tablename, functions, whereclause, limit, order_by, None)
    functions = bql.bql_statement.parseString('select typicality of name from test', parseAll=True).functions
    order_by = bql.bql_statement.parseString('select * from test order by typicality', parseAll=True).order_by
    select_result = engine.select(test_tablename, functions, whereclause, limit, order_by, None)
    return


@notimplemented
def test_delete_model():
    pass


def test_update_schema():
    test_tablename, _ = create_dha()
    m_c, m_r, t = engine.persistence_layer.get_metadata_and_table(test_tablename)
    cctypes = engine.persistence_layer.get_cctypes(test_tablename)
    assert cctypes[m_c['name_to_idx']['qual_score']] == 'numerical'
    assert cctypes[m_c['name_to_idx']['name']] == 'categorical'
    mappings = dict(qual_score=dict(cctype='categorical', parameters=None))
    engine.update_schema(test_tablename, mappings)
    cctypes = engine.persistence_layer.get_cctypes(test_tablename)
    assert cctypes[m_c['name_to_idx']['qual_score']] == 'categorical'
    mappings = dict(name=dict(cctype='categorical', parameters=dict(cardinality=350)))
    engine.update_schema(test_tablename, mappings)
    cctypes = engine.persistence_layer.get_cctypes(test_tablename)
    assert cctypes[m_c['name_to_idx']['name']] == 'categorical'
    mappings = dict(qual_score=dict(cctype='cyclic', parameters=dict(min=0, max=100)))
    engine.update_schema(test_tablename, mappings)
    cctypes = engine.persistence_layer.get_cctypes(test_tablename)
    assert cctypes[m_c['name_to_idx']['qual_score']] == 'cyclic'
    mappings = dict(qual_score=dict(cctype='ignore', parameters=None))
    engine.update_schema(test_tablename, mappings)
    m_c, m_r, t = engine.persistence_layer.get_metadata_and_table(test_tablename)
    cctypes = engine.persistence_layer.get_cctypes(test_tablename)
    assert 'qual_score' not in m_c['name_to_idx'].keys()
    mappings = dict(name=dict(cctype='numerical', parameters=None))
    with pytest.raises(ValueError):
        engine.update_schema(test_tablename, mappings)
    mappings = dict(qual_score=dict(cctype='cyclic', parameters=dict(min=50, max=60)))
    with pytest.raises(utils.BayesDBError):
        engine.update_schema(test_tablename, mappings)
    mappings = dict(name=dict(cctype='categorical', parameters=dict(cardinality=10)))
    with pytest.raises(utils.BayesDBError):
        engine.update_schema(test_tablename, mappings)
    return


def test_save_and_load_models():
    test_tablename, _ = create_dha()
    engine.initialize_models(test_tablename, 3)
    engine.analyze(test_tablename, model_indices='all', iterations=1, background=False)
    original_models = engine.save_models(test_tablename)
    test_tablename2, _ = create_dha()
    models = original_models['models']
    model_schema = original_models['schema']
    engine.load_models(test_tablename2, models, model_schema)
    assert engine.save_models(test_tablename2).values() == original_models.values()


def test_initialize_models():
    test_tablename, _ = create_dha(path='data/dha_missing.csv')
    engine = Engine(seed=0)
    num_models = 5
    engine.initialize_models(test_tablename, num_models)
    model_ids = engine.persistence_layer.get_model_ids(test_tablename)
    assert sorted(model_ids) == range(num_models)
    for i in range(num_models):
        model = engine.persistence_layer.get_models(test_tablename, i)
        assert model['iterations'] == 0


def test_analyze():
    test_tablename, _ = create_dha()
    num_models = 3
    engine.initialize_models(test_tablename, num_models)
    for it in (1, 2):
        engine.analyze(test_tablename, model_indices='all', iterations=1, background=True)
        while 'not currently being analyzed' not in engine.show_analyze(test_tablename)['message']:
            import time
            time.sleep(0.1)

        model_ids = engine.persistence_layer.get_model_ids(test_tablename)
        assert sorted(model_ids) == range(num_models)
        for i in range(num_models):
            model = engine.persistence_layer.get_models(test_tablename, i)
            assert model['iterations'] == it

    for it in (3, 4):
        engine.analyze(test_tablename, model_indices='all', iterations=1, background=False)
        analyze_results = engine.show_analyze(test_tablename)
        assert 'not currently being analyzed' in analyze_results['message']
        model_ids = engine.persistence_layer.get_model_ids(test_tablename)
        assert sorted(model_ids) == range(num_models)
        for i in range(num_models):
            model = engine.persistence_layer.get_models(test_tablename, i)
            assert model['iterations'] == it


def test_subsampling():
    test_tablename = 'kivatest' + str(int(time.time() * 1000000)) + str(int(random.random() * 10000000))
    test_tablenames.append(test_tablename)
    path = 'data/kiva_small.csv'
    header, rows = data_utils.read_csv(path)
    num_rows = 4
    num_rows_subsample = 2
    engine.create_btable(test_tablename, header, rows, subsample=num_rows_subsample, key_column=0)
    functions = bql.bql_statement.parseString('select loan_id, loan_status from test', parseAll=True).functions
    whereclause = None
    limit = float('inf')
    order_by = False
    select_result = engine.select(test_tablename, functions, whereclause, limit, order_by, None)
    assert len(select_result['data']) == num_rows
    num_models = 2
    iterations = 1
    engine.initialize_models(test_tablename, num_models)
    engine.analyze(test_tablename, model_indices='all', iterations=iterations, background=False)
    print 'analyzed'
    model_ids = engine.persistence_layer.get_model_ids(test_tablename)
    for i in range(num_models):
        model = engine.persistence_layer.get_models(test_tablename, i)
        assert model['iterations'] == iterations

    functions = bql.bql_statement.parseString('select loan_id, predictive probability of loan_status from test', parseAll=True).functions
    whereclause = None
    limit = float('inf')
    order_by = False
    select_result = engine.select(test_tablename, functions, whereclause, limit, order_by, None)
    assert len(select_result['data']) == num_rows
    return


def test_nan_handling():
    test_tablename1, _ = create_dha(path='data/dha_missing.csv')
    test_tablename2, _ = create_dha(path='data/dha_missing_nan.csv')
    m1 = engine.persistence_layer.get_metadata(test_tablename1)
    m2 = engine.persistence_layer.get_metadata(test_tablename2)
    assert m1['M_c'] == m2['M_c']
    assert m1['M_r'] == m2['M_r']
    assert m1['cctypes'] == m2['cctypes']
    numpy.testing.assert_equal(numpy.array(m1['T']), numpy.array(m2['T']))


def test_infer():
    test_tablename, _ = create_dha(path='data/dha_missing.csv')
    engine = Engine(seed=0)
    engine.initialize_models(test_tablename, 20)
    functions = bql.bql_statement.parseString('infer name, qual_score from test', parseAll=True).functions
    whereclause = None
    limit = float('inf')
    order_by = False
    numsamples = 30
    confidence = 0
    infer_result = engine.infer(test_tablename, functions, confidence, whereclause, limit, numsamples, order_by)
    assert 'column_labels' in infer_result
    assert 'data' in infer_result
    assert infer_result['column_labels'] == ['key', 'name', 'qual_score']
    assert len(infer_result['data']) == 307 and len(infer_result['data'][0]) == len(infer_result['column_labels'])
    assert type(infer_result['data'][0][0]) == numpy.string_
    t = type(infer_result['data'][0][1])
    assert t == unicode or t == numpy.string_
    assert type(infer_result['data'][0][2]) == float
    all_possible_names = [ infer_result['data'][row][1] for row in range(5) + range(10, 307) ]
    all_observed_qual_scores = [ infer_result['data'][row][2] for row in range(5, 307) ]
    for row in range(5):
        inferred_name = infer_result['data'][(row + 5)][1]
        inferred_qual_score = infer_result['data'][row][2]
        assert inferred_name in all_possible_names
        assert type(inferred_qual_score) == type(1.2)
        assert inferred_qual_score > min(all_observed_qual_scores)
        assert inferred_qual_score < max(all_observed_qual_scores)

    confidence = 0.9
    infer_result = engine.infer(test_tablename, functions, confidence, whereclause, limit, numsamples, order_by)
    for row in range(5):
        inferred_name = infer_result['data'][(row + 5)][1]
        inferred_qual_score = infer_result['data'][row][2]
        assert numpy.isnan(inferred_name)
        assert numpy.isnan(inferred_qual_score)

    return


def test_simulate():
    test_tablename, _ = create_dha()
    engine.initialize_models(test_tablename, 2)
    columnstring = 'name, qual_score'
    functions = bql.bql_statement.parseString('simulate name, qual_score from test', parseAll=True).functions
    whereclause = None
    givens = None
    order_by = False
    numpredictions = 10
    simulate_result = engine.simulate(test_tablename, functions, givens, numpredictions, order_by)
    assert 'column_labels' in simulate_result
    assert 'data' in simulate_result
    assert simulate_result['column_labels'] == ['name', 'qual_score']
    assert len(simulate_result['data']) == 10 and len(simulate_result['data'][0]) == len(simulate_result['column_labels'])
    for row in range(numpredictions):
        t = type(simulate_result['data'][row][0])
        assert t == unicode or t == numpy.string_
        assert type(simulate_result['data'][row][1]) == float

    return


def test_estimate_pairwise_dependence_probability():
    test_tablename, _ = create_dha()
    engine.initialize_models(test_tablename, 2)
    dep_mat = engine.estimate_pairwise(test_tablename, 'dependence probability')


@pytest.mark.skipif(True, reason="Calculation too slow due to analysis on non-ignored, unique, multinomial 'name' variable")
def test_estimate_pairwise_mutual_information():
    test_tablename, _ = create_dha()
    engine.initialize_models(test_tablename, 2)
    mi_mat = engine.estimate_pairwise(test_tablename, 'mutual information', numsamples=2)


def test_estimate_pairwise_correlation():
    test_tablename, _ = create_dha()
    engine.initialize_models(test_tablename, 2)
    cor_mat = engine.estimate_pairwise(test_tablename, 'correlation')


def test_list_btables():
    list_btables_result = engine.list_btables()['data']
    assert type(list_btables_result) == list
    initial_btable_count = len(list_btables_result)
    test_tablename1, create_btable_result = create_dha()
    test_tablename2, create_btable_result = create_dha()
    list_btables_result = engine.list_btables()['data']
    assert [test_tablename1] in list_btables_result
    assert [test_tablename2] in list_btables_result
    assert len(list_btables_result) == 2 + initial_btable_count
    engine.drop_btable(test_tablename1)
    test_tablename3, create_btable_result = create_dha()
    list_btables_result = engine.list_btables()['data']
    assert [test_tablename1] not in list_btables_result
    assert [test_tablename3] in list_btables_result
    assert [test_tablename2] in list_btables_result
    engine.drop_btable(test_tablename2)
    engine.drop_btable(test_tablename3)
    list_btables_result = engine.list_btables()['data']
    assert len(list_btables_result) == 0 + initial_btable_count


@notimplemented
def test_execute_file():
    pass


def test_show_schema():
    test_tablename, _ = create_dha()
    m_c, m_r, t = engine.persistence_layer.get_metadata_and_table(test_tablename)
    cctypes = engine.persistence_layer.get_cctypes(test_tablename)
    assert cctypes[m_c['name_to_idx']['qual_score']] == 'numerical'
    assert cctypes[m_c['name_to_idx']['name']] == 'categorical'
    schema = engine.show_schema(test_tablename)
    cctypes_full = engine.persistence_layer.get_cctypes_full(test_tablename)
    assert sorted([ d[1] for d in schema['data'] ]) == sorted(cctypes_full)
    assert schema['data'][0][0] == 'key'
    mappings = dict(qual_score=dict(cctype='categorical', parameters=None))
    engine.update_schema(test_tablename, mappings)
    cctypes = engine.persistence_layer.get_cctypes(test_tablename)
    assert cctypes[m_c['name_to_idx']['qual_score']] == 'categorical'
    schema = engine.show_schema(test_tablename)
    cctypes_full = engine.persistence_layer.get_cctypes_full(test_tablename)
    assert sorted([ d[1] for d in schema['data'] ]) == sorted(cctypes_full)
    assert schema['data'][0][0] == 'key'
    return


def test_show_models():
    test_tablename, _ = create_dha()
    num_models = 3
    engine.initialize_models(test_tablename, num_models)
    for it in (1, 2):
        analyze_out = engine.analyze(test_tablename, model_indices='all', iterations=1, background=False)
        model_ids = engine.persistence_layer.get_model_ids(test_tablename)
        assert sorted(model_ids) == range(num_models)
        for i in range(num_models):
            model = engine.persistence_layer.get_models(test_tablename, i)
            assert model['iterations'] == it

        models = engine.show_models(test_tablename)['models']
        assert len(models) == num_models
        for iter_id, m in enumerate(models):
            assert iter_id == m[0]
            assert it == m[1]


def test_describe():
    test_tablename, metadata = create_describe_btable()
    bql_string = 'describe c_0 for %s' % test_tablename
    bql_query = bql.bql_statement.parseString(bql_string, parseAll=True)
    result = engine.describe(test_tablename, bql_query.columnset)
    assert len(result['data']) == 1
    assert result['data'][0][0] == 'c_0'
    assert result['data'][0][1] == 'column zero'
    assert result['data'][0][2] == 'description for column zero'
    metadata = engine.persistence_layer.get_metadata(test_tablename)
    col_0_idx = metadata['M_c']['name_to_idx']['c_0']
    assert metadata['M_c']['column_metadata'][col_0_idx]['parameters']['cardinality'] == 6
    assert len(metadata['M_c']['column_metadata'][col_0_idx]['value_to_code']) == 6
    assert len(metadata['M_c']['column_metadata'][col_0_idx]['code_to_value']) == 6
    assert '6' in result['data'][0][3]
    bql_string = 'describe c_1, c_2, c_3 for %s' % test_tablename
    bql_query = bql.bql_statement.parseString(bql_string, parseAll=True)
    result = engine.describe(test_tablename, bql_query.columnset)
    assert len(result['data']) == 3
    for row in result['data']:
        assert len(row) == 4

    bql_string = 'describe * for %s' % test_tablename
    bql_query = bql.bql_statement.parseString(bql_string, parseAll=True)
    result = engine.describe(test_tablename, bql_query.columnset)
    assert len(result['data']) == 4
    for row in result['data']:
        assert len(row) == 4


def test_update_descriptions_single():
    test_tablename, metadata = create_describe_btable()
    description_proposed = 'Hamish the cat'
    bql_string = 'update description for %s set c_0="%s"' % (test_tablename, description_proposed)
    bql_query = bql.bql_statement.parseString(bql_string, parseAll=True)
    _, args, _ = parser.parse_update_descriptions(bql_query)
    result = engine.update_descriptions(test_tablename, args['mappings'])
    column_name_output = result['data'][0][0]
    description_output = result['data'][0][1]
    assert column_name_output == 'c_0'
    assert description_output == description_proposed
    bql_string = 'describe c_0 for %s' % test_tablename
    bql_query = bql.bql_statement.parseString(bql_string, parseAll=True)
    result = engine.describe(test_tablename, bql_query.columnset)
    description_updated = result['data'][0][2]
    assert description_updated == description_proposed


def test_update_descriptions_multiple():
    test_tablename, metadata = create_describe_btable()
    description_proposed_0 = 'Hamish thh cat'
    description_proposed_1 = 'Winter Ninjaturtle'
    bql_string = 'update descriptions for %s set c_0="%s", c_2="%s"' % (
     test_tablename, description_proposed_0, description_proposed_1)
    bql_query = bql.bql_statement.parseString(bql_string, parseAll=True)
    _, args, _ = parser.parse_update_descriptions(bql_query)
    result = engine.update_descriptions(test_tablename, args['mappings'])
    column_name_output_0 = result['data'][0][0]
    description_output_0 = result['data'][0][1]
    column_name_output_1 = result['data'][1][0]
    description_output_1 = result['data'][1][1]
    assert column_name_output_0 == 'c_0'
    assert description_output_0 == description_proposed_0
    assert column_name_output_1 == 'c_2'
    assert description_output_1 == description_proposed_1
    bql_string = 'describe c_0, c_2 for %s' % test_tablename
    bql_query = bql.bql_statement.parseString(bql_string, parseAll=True)
    result = engine.describe(test_tablename, bql_query.columnset)
    description_updated_0 = result['data'][0][2]
    description_updated_1 = result['data'][1][2]
    assert description_updated_0 == description_proposed_0
    assert description_updated_1 == description_proposed_1


def test_update_short_names_single():
    test_tablename, metadata = create_describe_btable()
    short_name_proposed = 'Hamish'
    bql_string = 'update short name for %s set c_0=%s' % (test_tablename, short_name_proposed)
    bql_query = bql.bql_statement.parseString(bql_string, parseAll=True)
    _, args, _ = parser.parse_update_short_names(bql_query)
    result = engine.update_short_names(test_tablename, args['mappings'])
    column_name_output = result['data'][0][0]
    short_name_output = result['data'][0][1]
    assert column_name_output == 'c_0'
    assert short_name_output == short_name_proposed
    bql_string = 'describe c_0 for %s' % test_tablename
    bql_query = bql.bql_statement.parseString(bql_string, parseAll=True)
    result = engine.describe(test_tablename, bql_query.columnset)
    short_name_updated = result['data'][0][1]
    assert short_name_updated == short_name_proposed


@notimplemented
def test_update_codebook():
    pass


def test_update_short_names_multiple():
    test_tablename, metadata = create_describe_btable()
    short_name_proposed_0 = 'Hamish'
    short_name_proposed_1 = 'Winter Ninjaturtle'
    bql_string = 'update short names for %s set c_0="%s", c_2="%s"' % (
     test_tablename, short_name_proposed_0, short_name_proposed_1)
    bql_query = bql.bql_statement.parseString(bql_string, parseAll=True)
    _, args, _ = parser.parse_update_short_names(bql_query)
    result = engine.update_short_names(test_tablename, args['mappings'])
    column_name_output_0 = result['data'][0][0]
    short_name_output_0 = result['data'][0][1]
    column_name_output_1 = result['data'][1][0]
    short_name_output_1 = result['data'][1][1]
    assert column_name_output_0 == 'c_0'
    assert short_name_output_0 == short_name_proposed_0
    assert column_name_output_1 == 'c_2'
    assert short_name_output_1 == short_name_proposed_1
    bql_string = 'describe c_0, c_2 for %s' % test_tablename
    bql_query = bql.bql_statement.parseString(bql_string, parseAll=True)
    result = engine.describe(test_tablename, bql_query.columnset)
    short_name_updated_0 = result['data'][0][1]
    short_name_updated_1 = result['data'][1][1]
    assert short_name_updated_0 == short_name_proposed_0
    assert short_name_updated_1 == short_name_proposed_1


def test_show_diagnostics():
    test_tablename, _ = create_describe_btable()
    with pytest.raises(utils.BayesDBError) as (excinfo):
        result = engine.show_diagnostics(test_tablename)
    assert 'No models for btable' in excinfo.value.message
    engine.initialize_models(test_tablename, n_models=2)
    with pytest.raises(utils.BayesDBError) as (excinfo):
        result = engine.show_diagnostics(test_tablename)
    assert 'No diagnostics found' in excinfo.value.message
    num_iters = 5
    engine.analyze(test_tablename, iterations=num_iters, background=False)
    results = engine.show_diagnostics(test_tablename)
    entry_length = len(diag_utils.single_state_diagnostics) + 4
    assert len(results['column_labels']) == entry_length
    assert len(results['data']) == 2
    assert len(results['data'][0]) == entry_length
    assert len(results['data'][1]) == entry_length
    assert results['data'][0][0] == 0
    assert results['data'][0][1] == num_iters
    assert results['data'][1][0] == 1
    assert results['data'][1][1] == num_iters


@notimplemented
def test_drop_models():
    pass


def test_estimate_columns():
    test_tablename, _ = create_dha()
    metadata = engine.persistence_layer.get_metadata(test_tablename)
    all_columns = metadata['M_c']['name_to_idx'].keys()
    engine.initialize_models(test_tablename, 2)
    whereclause = None
    limit = float('inf')
    order_by = False
    name = None
    functions = None
    column_labels = engine.estimate_columns(test_tablename, functions, whereclause, limit, order_by, name)['column_labels']
    assert column_labels == ['column label', 'column name']
    return


if __name__ == '__main__':
    run_test()