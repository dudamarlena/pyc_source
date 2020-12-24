# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/rachelle2/webprojects/toucan-connectors/toucan_connectors/common.py
# Compiled at: 2020-04-23 04:23:41
# Size of source mod 2**32: 6632 bytes
import ast, asyncio, re
from copy import deepcopy
import pyjq
from jinja2 import Environment, StrictUndefined, Template, meta
from pydantic import Field
from toucan_data_sdk.utils.helpers import slugify
RE_PARAM = '%\\(([^(%\\()]*)\\)s'
RE_JINJA = '{{([^({{)}]*)}}'
RE_PARAM_ALONE = '^' + RE_PARAM + '$'
RE_JINJA_ALONE = '^' + RE_JINJA + '$'
RE_JINJA_ALONE_IN_STRING = [
 RE_JINJA + '([ )])', RE_JINJA + '()$']
RE_SET_KEEP_TYPE = '{{__keep_type__\\1}}\\2'
RE_GET_KEEP_TYPE = '{{(__keep_type__[^({{)}]*)}}'

def nosql_apply_parameters_to_query(query, parameters):
    """
    WARNING : DO NOT USE THIS WITH VARIANTS OF SQL
    Instead use your client library parameter substitution method.
    https://www.owasp.org/index.php/Query_Parameterization_Cheat_Sheet
    """

    def _has_parameters(query):
        t = Environment().parse(query)
        return meta.find_undeclared_variables(t) or re.search(RE_PARAM, query)

    def _prepare_parameters(p):
        if isinstance(p, str):
            return repr(p)
        else:
            if isinstance(p, list):
                return [_prepare_parameters(e) for e in p]
            if isinstance(p, dict):
                return {k:_prepare_parameters(v) for k, v in p.items()}
            return p

    def _prepare_result(res):
        if isinstance(res, str):
            return ast.literal_eval(res)
        else:
            if isinstance(res, list):
                return [_prepare_result(e) for e in res]
            if isinstance(res, dict):
                return {k:_prepare_result(v) for k, v in res.items()}
            return res

    def _render_query(query, parameters):
        if isinstance(query, dict):
            return {key:_render_query(value, parameters) for key, value in deepcopy(query).items()}
        else:
            if isinstance(query, list):
                return [_render_query(elt, parameters) for elt in deepcopy(query)]
            if type(query) is str:
                if not _has_parameters(query):
                    return query
                clean_p = deepcopy(parameters)
                if re.match(RE_PARAM_ALONE, query) or re.match(RE_JINJA_ALONE, query):
                    clean_p = _prepare_parameters(clean_p)
                res = Template(query).render(clean_p) % clean_p
                try:
                    res = ast.literal_eval(res)
                    if isinstance(res, str):
                        return res
                    else:
                        return _prepare_result(res)
                except (SyntaxError, ValueError):
                    return res

            return query

    def _handle_missing_params(elt, params):
        if isinstance(elt, dict):
            e = {}
            for k, v in elt.items():
                if isinstance(v, str):
                    matches = re.findall(RE_PARAM, v) + re.findall(RE_JINJA, v)
                    missing_params = []
                    for m in matches:
                        try:
                            Template(('{{ %s }}' % m), undefined=StrictUndefined).render(params)
                        except Exception:
                            missing_params.append(m)

                    if any(missing_params):
                        continue
                    else:
                        e[k] = v
                else:
                    e[k] = _handle_missing_params(v, params)

            return e
        else:
            if isinstance(elt, list):
                return [_handle_missing_params(e, params) for e in elt]
            return elt

    query = _handle_missing_params(query, parameters)
    if parameters is None:
        return query
    else:
        query = _render_query(query, parameters)
        return query


def apply_query_parameters(query: str, parameters: dict) -> str:
    """
    Apply parameters to query

    Interpolate the query, which is a Jinja templates, with the provided parameters.
    """

    def _flatten_dict(p, parent_key=''):
        new_p = {}
        for k, v in deepcopy(p).items():
            new_key = f"{parent_key}_{k}" if parent_key else k
            new_p[new_key] = v
            if isinstance(v, list):
                v = {idx:elt for idx, elt in enumerate(v)}
            if isinstance(v, dict):
                new_p.update(_flatten_dict(v, new_key))
            else:
                if isinstance(v, str):
                    new_p.update({new_key: f'"{v}"'})
                else:
                    new_p.update({new_key: v})

        return new_p

    if parameters is None:
        return query
    else:
        for pattern in RE_JINJA_ALONE_IN_STRING:
            query = re.sub(pattern, RE_SET_KEEP_TYPE, query)

        p_keep_type = re.findall(RE_GET_KEEP_TYPE, query)
        for key in p_keep_type:
            query = query.replace(key, slugify(key, separator='_'))

        if len(p_keep_type):
            p_keep_type = _flatten_dict(parameters, parent_key='__keep_type_')
            parameters.update(p_keep_type)
        return Template(query).render(parameters)


def transform_with_jq(data: object, jq_filter: str) -> list:
    data = pyjq.all(jq_filter, data)
    multiple_output = len(data) == 1 and isinstance(data[0], list)
    single_cols_dict = isinstance(data[0], dict) and isinstance(list(data[0].values())[0], list)
    if multiple_output or single_cols_dict:
        return data[0]
    else:
        return data


FilterSchema = Field('.',
  description='You can apply filters to json response if data is nested. As we rely on a library called jq, we suggest the refer to the dedicated <a href="https://stedolan.github.io/jq/manual/">documentation</a>')

def get_loop():
    """Sets up event loop"""
    try:
        loop = asyncio.get_event_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

    return loop