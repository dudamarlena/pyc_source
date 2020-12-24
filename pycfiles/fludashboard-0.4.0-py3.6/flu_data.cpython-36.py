# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /storage/Marcelo/codes/FluVigilanciaBR/fludashboard/fludashboard/libs/flu_data.py
# Compiled at: 2018-06-21 10:51:14
# Size of source mod 2**32: 25887 bytes
from unidecode import unidecode
from ..settings import DATABASE
import pandas as pd, sqlalchemy as sqla

def prepare_keys_name(df):
    """
    Standardises data frame keys

    :param df:
    :type df: pd.DataFrame
    :return: pd.DataFrame
    """
    for k in df.keys():
        df.rename(columns={k: unidecode(k.replace(' ', '_').replace('-', '_').lower()).encode('ascii').decode('utf8')},
          inplace=True)

    return df


class FluDB:
    conn = None

    def __init__(self):
        dsn = 'postgresql://%(USER)s:%(PASSWORD)s@%(HOST)s/%(NAME)s'
        self.conn = sqla.create_engine(dsn % DATABASE)

    def get_territory_id_from_name(self, state_name: str) -> int:
        """

        :param state_name:
        :return:
        """
        state_name = state_name.upper()
        with self.conn.connect() as (conn):
            sql = "\n            SELECT id FROM territory \n            WHERE UPPER(name)='%s'\n            " % state_name
            result = conn.execute(sql).fetchone()
            if not result:
                raise Exception('State not found.')
            return result[0]

    def get_territory_from_name(self, state_name: str) -> int:
        """

        :param state_name:
        :return:
        """
        state_name = state_name.upper()
        with self.conn.connect() as (conn):
            sql = "\n            SELECT * FROM territory \n            WHERE UPPER(name)='%s'\n            " % state_name
            result = conn.execute(sql).fetchone()
            if not result:
                raise Exception('Territory not found.')
            return result

    def get_season_situation(self, df):
        """

        :param df:
        :return:
        """

        def _fn(se):
            return df[((df.territory_id == se.territory_id) & (df.epiyear == se.epiyear))].situation_id.unique()[0]

        return _fn

    def get_season_level(self, se):
        """
        Generate season level code based on counts over weekly activity

        """
        if se.high_level + se.very_high_level > 4:
            return 4
        else:
            if se.high_level + se.very_high_level >= 1:
                return 3
            if se.epidemic_level >= 1:
                return 2
            return 1

    def group_data_by_season(self, df, df_age_dist=None, season=None):
        """

        :param df:
        :param df_age_dist:
        :param season:
        :return:
        """
        level_dict = {'low_level':'Baixa', 
         'epidemic_level':'Epidêmica',  'high_level':'Alta', 
         'very_high_level':'Muito alta'}
        season_basic_cols = [
         'territory_id', 'territory_name', 'epiyear', 'value']
        season_cols = season_basic_cols + [
         'territory_type_name', 'situation_id', 'situation_name', 'level']
        df['level'] = df[list(level_dict.keys())].idxmax(axis=1)
        df_tmp = df[season_cols].copy()
        situation = list(df_tmp[(df_tmp.epiyear == season)].situation_id.unique())
        l_incomplete = [
         1, 2, 4]
        if set(l_incomplete).intersection(situation):
            df_tmp.loc[(df_tmp.epiyear == season, 'situation_id')] = 4
        else:
            df_tmp.loc[(df_tmp.epiyear == season, 'situation_id')] = 3
        if df_age_dist is not None:
            tgt_cols = ['territory_id', 'territory_name', 'epiyear', 'gender',
             'value', 'years_lt_2', 'years_2_4', 'years_0_4', 'years_5_9',
             'years_10_19', 'years_20_29', 'years_30_39', 'years_40_49',
             'years_50_59', 'years_60_or_more']
            df_by_season = df_age_dist[tgt_cols].groupby([
             'territory_id', 'territory_name', 'epiyear', 'gender'],
              as_index=False).sum()
        else:
            df_by_season = df_tmp[season_basic_cols].groupby([
             'territory_id', 'territory_name', 'epiyear'],
              as_index=False).sum()
        situations_id = {1:'unknown', 
         2:'estimated', 
         3:'stable', 
         4:'incomplete'}
        df_by_season['situation_id'] = df_by_season.apply((self.get_season_situation(df_tmp)),
          axis=1)
        df_by_season['situation_name'] = df_by_season['situation_id'].map(situations_id)
        df_by_season_level = pd.crosstab([
         df_tmp.territory_id, df_tmp.territory_name, df_tmp.epiyear], df_tmp.level).reset_index()
        df_by_season_level.columns.name = None
        for lv in ('low_level', 'epidemic_level', 'high_level', 'very_high_level'):
            if lv not in df_by_season_level.keys():
                df_by_season_level[lv] = 0

        df_by_season['level'] = df_by_season_level[list(level_dict.keys())].apply((self.get_season_level),
          axis=1)
        df_by_season['epiweek'] = 0
        return df_by_season

    def report_incidence(self, x, situation, low=None, high=None):
        """
        original name: report_inc

        :param x:
        :param situation:
        :param low:
        :param high:
        :return:
        """
        if situation == 3:
            y = '%.2f' % x
        else:
            if situation == 2:
                y = '%.2f [%.2f - %.2f]' % (x, low, high)
            else:
                y = '*%.2f' % x
        return y

    def read_data(self, table_name: str, dataset_id: int, scale_id: int, territory_id: int=None, year: int=None, week: int=None, base_year: int=None, base_week: int=None, historical_week: int=None, return_sql=False, extra_fields: list=None, selected_fields: list=None, excluded_fields: list=[], **kwargs):
        """

        :param table_name:
        :param dataset_id:
        :param scale_id:
        :param territory_id:
        :param year:
        :param week:
        :param base_year:
        :param base_week:
        :param historical_week:
        :param return_sql:
        :param extra_fields:
        :param selected_fields:
        :param excluded_fields:
        :param kwargs:
        :return:

        """
        if selected_fields is None:
            sql = "\n            SELECT column_name\n            FROM information_schema.columns\n            WHERE table_name   = '%s'\n            ORDER BY ordinal_position\n            " % table_name
            with self.conn.connect() as (conn):
                selected_fields = conn.execute(sql).fetchall()
            selected_fields = [f[0] for f in selected_fields if f[0] not in ['dataset_id', 'scale_id'] + excluded_fields]
        else:
            if extra_fields is not None:
                selected_fields += extra_fields
            else:
                sql_param = {'table_name':table_name, 
                 'dataset_id':dataset_id, 
                 'scale_id':scale_id, 
                 'fields':','.join(selected_fields)}
                sql = '\n        SELECT %(fields)s, territory.name AS territory_name\n        FROM %(table_name)s \n          INNER JOIN territory\n            ON (%(table_name)s.territory_id = territory.id)\n        WHERE dataset_id=%(dataset_id)s \n          AND scale_id=%(scale_id)s\n        '
                if territory_id is not None:
                    sql += ' AND territory_id=%(territory_id)s'
                    sql_param['territory_id'] = territory_id
                if year is not None:
                    sql += ' AND epiyear=%(year)s'
                    sql_param['year'] = year
                if base_year is not None:
                    sql += ' AND base_epiyear=%(base_year)s'
                    sql_param['base_year'] = base_year
                if week is not None:
                    if week > 0:
                        sql += ' AND epiweek=%(week)s'
                        sql_param['week'] = week
                if base_week is not None:
                    sql += ' AND base_epiweek=%(base_week)s'
                    sql_param['base_week'] = base_week
                elif historical_week is not None:
                    sql += ' AND epiweek<=%(historical_week)s'
                    sql_param['historical_week'] = historical_week
            if return_sql:
                return sql % sql_param
        with self.conn.connect() as (conn):
            return pd.read_sql(sql % sql_param, conn)

    def get_data(self, dataset_id: int, scale_id: int, year: int, territory_id: int=None, week: int=None, show_historical_weeks: bool=False, territory_type_id: int=None):
        """

        :param dataset_id:
        :param scale_id:
        :param year:
        :param territory_id:
        :param week: 0 week == all weeks
        :param show_historical_weeks:
        :param territory_type_id:
        :return:
        """
        sql = '\n        SELECT\n          mem_typical.dataset_id AS dataset_id,\n          mem_typical.scale_id AS scale_id,\n          mem_typical.territory_id AS territory_id,\n          incidence.epiyear AS epiyear,\n          mem_typical.epiweek AS epiweek,\n          incidence.value, \n          incidence.low_level as low_level,\n          incidence.epidemic_level as epidemic_level,\n          incidence.high_level as high_level,\n          incidence.very_high_level as very_high_level,\n          incidence.situation_id AS situation_id,\n          incidence.run_date,\n          %(estimates_columns_selection)s\n          mem_typical.population, \n          mem_typical.low AS typical_low, \n          mem_typical.median-mem_typical.low AS typical_median, \n          mem_typical.high-mem_typical.median AS typical_high,\n          mem_report.geom_average_peak, \n          mem_report.low_activity_region, \n          mem_report.pre_epidemic_threshold as pre_epidemic_threshold, \n          mem_report.high_threshold as high_threshold, \n          mem_report.very_high_threshold as very_high_threshold, \n          mem_report.epi_start, \n          mem_report.epi_start_ci_lower,\n          mem_report.epi_start_ci_upper, \n          mem_report.epi_duration, \n          mem_report.epi_duration_ci_lower, \n          mem_report.epi_duration_ci_upper,\n          mem_report.regular_seasons,\n          historical.base_epiyear, \n          historical.base_epiweek,\n          territory.name AS territory_name,\n          territory_type.name AS territory_type_name,\n          situation.name AS situation_name,\n          contingency_level.contingency AS contingency,\n          contingency_level.contingency_max AS contingency_max,\n          weekly_alert.alert AS alert,\n          season_level.season_level AS season_level\n        FROM\n          (\n            SELECT\n            epiyear,\n            epiweek,\n            dataset_id,\n            scale_id,\n            territory_id,\n            situation_id,\n            "value",\n            low_level,\n            epidemic_level,\n            high_level,\n            very_high_level,\n            run_date \n            %(incidence_table_select)s\n            FROM current_estimated_values\n            WHERE dataset_id=%(dataset_id)s \n              AND scale_id=%(scale_id)s \n              AND epiyear=%(epiyear)s \n              AND epiweek %(incidence_week_operator)s %(epiweek)s\n              %(territory_id_condition)s\n              %(situation_id_condition)s\n          ) AS incidence \n          INNER JOIN situation\n            ON (incidence.situation_id=situation.id)\n          FULL OUTER JOIN (\n            SELECT * FROM mem_typical\n            WHERE dataset_id=%(dataset_id)s \n              AND scale_id=%(scale_id)s\n              %(territory_id_condition)s \n            ) AS mem_typical\n            ON (\n              incidence.dataset_id=mem_typical.dataset_id\n              AND incidence.scale_id=mem_typical.scale_id\n              AND incidence.territory_id=mem_typical.territory_id\n              AND incidence.epiweek=mem_typical.epiweek\n            )\n          LEFT JOIN (\n            SELECT * FROM weekly_alert\n            WHERE dataset_id=%(dataset_id)s\n              AND epiyear=%(epiyear)s\n              %(territory_id_condition)s\n            ) AS weekly_alert\n            ON (\n              mem_typical.dataset_id=weekly_alert.dataset_id\n              AND mem_typical.territory_id=weekly_alert.territory_id\n              AND mem_typical.epiweek=weekly_alert.epiweek            \n            )\n          INNER JOIN territory\n            ON (mem_typical.territory_id=territory.id)\n          INNER JOIN territory_type\n            ON (territory.territory_type_id=territory_type.id)\n          %(historical_table)s\n          FULL OUTER JOIN (\n            SELECT * FROM mem_report\n            WHERE dataset_id=%(dataset_id)s \n              AND scale_id=%(scale_id)s\n              %(territory_id_condition)s\n            ) AS mem_report\n            ON (\n              mem_typical.dataset_id=mem_report.dataset_id\n              AND mem_typical.scale_id=mem_report.scale_id\n              AND mem_typical.territory_id=mem_report.territory_id\n              AND mem_typical.year=mem_report.year\n            )\n          FULL OUTER JOIN (\n            SELECT * FROM contingency_level\n            WHERE epiyear=%(epiyear)s\n            %(territory_id_condition)s\n            ) AS contingency_level\n            ON (\n            mem_report.territory_id=contingency_level.territory_id\n            )\n          FULL OUTER JOIN (\n            SELECT * FROM season_level\n            WHERE epiyear=%(epiyear)s\n            %(territory_id_condition)s\n            ) AS season_level\n            ON (\n            mem_report.territory_id=season_level.territory_id\n            AND mem_typical.dataset_id=season_level.dataset_id\n\n            )\n         WHERE 1=1\n           %(where_extras)s\n        ORDER BY epiyear, epiweek\n        '
        sql_param = {'dataset_id':dataset_id, 
         'scale_id':scale_id, 
         'territory_id':territory_id, 
         'epiweek':week, 
         'epiyear':year, 
         'epiweekstop':54, 
         'base_epiweek_condition':'', 
         'estimates_columns_selection':'\n            incidence.mean  AS "mean",\n            incidence.median AS estimated_cases, \n            incidence.ci_lower AS ci_lower, \n            incidence.ci_upper AS ci_upper, \n            ', 
         'where_extras':'', 
         'historical_table':'\n            FULL OUTER JOIN (\n              SELECT * \n              FROM historical_estimated_values LIMIT 0\n            ) AS historical ON (1=1)\n            ', 
         'incidence_week_operator':'=', 
         'territory_id_condition':'', 
         'situation_id_condition':'', 
         'incidence_table_select':' \n            ,mean,\n            median,\n            ci_lower,\n            ci_upper\n            '}
        if territory_id is not None:
            sql_param['territory_id_condition'] += ' AND territory_id=%s ' % territory_id
        else:
            if week is None or week == 0:
                sql_param['epiweek'] = 54
                sql_param['incidence_week_operator'] = '<='
                sql_param['base_epiweek_condition'] = '\n            AND base_epiweek = (\n                SELECT MAX(base_epiweek)\n                FROM historical_estimated_values\n                WHERE base_epiyear = %(epiyear)s                AND dataset_id = %(dataset_id)s\n                AND scale_id = %(scale_id)s\n                %(territory_id_condition)s )\n            ' % sql_param
                with self.conn.connect() as (conn):
                    sql_param['epiweekstop'] = conn.execute('\n                SELECT MAX(epiweek) FROM current_estimated_values\n                WHERE epiyear = %(epiyear)s\n                  AND "value" IS NOT NULL\n                ' % sql_param).fetchone()[0] - 4
            else:
                sql_param['epiweekstop'] = week - 4
                sql_param['base_epiweek_condition'] = '\n            AND base_epiweek = (\n                SELECT MAX(LEAST(base_epiweek, %(epiweek)s))\n                FROM historical_estimated_values\n                WHERE base_epiyear=%(epiyear)s\n                    AND dataset_id = %(dataset_id)s\n                    AND scale_id = %(scale_id)s\n                    AND base_epiweek <= %(epiweek)s\n                    %(territory_id_condition)s )\n            AND epiyear =%(epiyear)s\n            ' % sql_param
            if show_historical_weeks:
                with self.conn.connect() as (conn):
                    epiyearmax = conn.execute('SELECT MAX(epiyear) FROM current_estimated_values').fetchone()[0]
                if year < epiyearmax:
                    sql_param['situation_id_condition'] = ' AND situation_id = 3'
                else:
                    sql_param['situation_id_condition'] = ' AND epiweek <= %(epiweekstop)s' % sql_param
                sql_param['estimates_columns_selection'] = '\n            historical.mean  AS mean,\n            historical.median AS estimated_cases, \n            historical.ci_lower AS ci_lower, \n            historical.ci_upper AS ci_upper, \n            '
                sql_param['incidence_table_select'] = ''
                sql_param['historical_table'] = '\n          LEFT JOIN (\n            SELECT territory_id,\n                epiweek,\n                mean,\n                median,\n                ci_lower,\n                ci_upper,\n                low_level,\n                epidemic_level,\n                high_level,\n                very_high_level,\n                base_epiyear,\n                base_epiweek,\n                base_epiyearweek\n            FROM historical_estimated_values\n            WHERE dataset_id=%(dataset_id)s \n             AND scale_id=%(scale_id)s \n             AND territory_id=%(territory_id)s \n             AND base_epiyear=%(epiyear)s\n             AND situation_id = 2\n             %(base_epiweek_condition)s\n          ) AS historical\n            ON (\n              mem_typical.epiweek=historical.epiweek\n            )\n            ' % sql_param
                sql_param['incidence_week_operator'] = '<='
            else:
                sql_param['where_extras'] += ' AND incidence.epiweek %s %s' % (
                 sql_param['incidence_week_operator'], sql_param['epiweek'])
        if territory_type_id is not None:
            if territory_type_id > 0:
                sql_param['where_extras'] += ' AND territory.territory_type_id=%s' % territory_type_id
        sql = sql % sql_param
        with self.conn.connect() as (conn):
            return pd.read_sql(sql, conn)

    def get_data_age_sex(self, dataset_id: int, scale_id: int, year: int, territory_id: int=0, week: int=0):
        """

        :param dataset_id:
        :param scale_id:
        :param year:
        :param territory_id:
        :param week:
        :return:

        """
        season = year
        if scale_id == 1:
            age_cols = [
             'years_0_4']
        else:
            age_cols = [
             'years_lt_2', 'years_2_4']
        age_cols.extend([
         'years_5_9', 'years_10_19', 'years_20_29',
         'years_30_39', 'years_40_49', 'years_50_59', 'years_60_or_more'])
        df_age_dist = self.read_data('clean_data_epiweek_weekly_incidence_w_situation',
          dataset_id=dataset_id,
          scale_id=scale_id,
          year=season,
          territory_id=territory_id,
          low_memory=False,
          excluded_fields=[
         'ADNO', 'PARA1', 'PARA2', 'PARA3'])
        if week is not None:
            if week > 0:
                df_age_dist = df_age_dist[(df_age_dist.epiweek == week)]
                df = df_age_dist
        else:
            df = self.get_data(dataset_id=dataset_id,
              scale_id=scale_id,
              year=year,
              territory_id=territory_id)
            df = self.group_data_by_season(df=df,
              df_age_dist=df_age_dist,
              season=season)
        df = df[(age_cols + ['gender'])].set_index('gender').transpose()
        df.rename(columns={'F':'Mulheres',  'M':'Homens'}, inplace=True)
        if 'I' in df.columns:
            df.rename(columns={'I': 'Sexo ignorado'}, inplace=True)
            df = df[['Mulheres', 'Homens', 'Sexo ignorado', 'Total']]
        return df

    def get_etiological_data(self, dataset_id: int, scale_id: int, year: int, week: int=None, territory_id: int=None) -> pd.DataFrame:
        """
        Generate timeseries for each ethiological agent and other relevant lab
        data

        :param dataset_id: SRAG (1) or SRAGFLU (2) or OBITOFLU (3)
        :param scale_id: Incidence (1) or cases (2)
        :param year: epidemiological year
        :param week: epidemiological week or all (None or 0)
        :param territory_id:
        """
        sql_param = {'epiweek':week, 
         'epiyear':year, 
         'territory_id':territory_id, 
         'dataset_id':dataset_id, 
         'scale_id':scale_id}
        if week == None or week == 0:
            sql_param['epiweek'] = 53
        if territory_id == None:
            sql_param['territory_id'] = 0
        sql = '\n        SELECT\n          notification.epiweek AS epiweek,\n          notification.positive_cases AS "Testes positivos",\n          notification.flu_a AS "Influenza A",\n          notification.flu_b AS "Influenza B",\n          notification.vsr AS "VSR",\n          notification."ADNO" AS "Adenovirus",\n          notification."PARA1" AS "Parainfluenza 1",\n          notification."PARA2" AS "Parainfluenza 2",\n          notification."PARA3" AS "Parainfluenza 3",\n          notification.negative AS "Testes negativos",\n          notification.not_tested AS "Casos sem teste laboratorial",\n          notification.delayed AS "Casos aguardando resultado",\n          notification.testing_ignored AS "Casos sem informação laboratorial",\n          territory.name AS territory_name\n        FROM\n          (SELECT \n            epiweek,\n            epiyear,\n            dataset_id,\n            scale_id,\n            gender,\n            positive_cases,\n            flu_a,\n            flu_b,\n            vsr,\n            "ADNO",\n            "PARA1",\n            "PARA2",\n            "PARA3",\n            negative,\n            not_tested,\n            delayed,\n            testing_ignored,\n            territory_id\n          FROM\n            clean_data_epiweek_weekly_incidence_w_situation\n          WHERE\n            epiyear=%(epiyear)s\n            AND dataset_id=%(dataset_id)s\n            AND territory_id=%(territory_id)s\n            AND scale_id=%(scale_id)s\n            AND gender=\'Total\'\n            AND epiweek <= %(epiweek)s\n          ) as notification\n        LEFT JOIN territory\n            ON (notification.territory_id=territory.id)\n        WHERE 1=1\n        ORDER BY epiweek\n        ' % sql_param
        with self.conn.connect() as (conn):
            return pd.read_sql(sql, conn)

    def get_opportunities(self, dataset_id: int, scale_id: int, year: int, territory_type_id: int, week: int=None, territory_id: int=None) -> pd.DataFrame:
        """
        Grab data for opportunity boxplots

        :param dataset_id:
        :param scale_id:
        :param year: selected year
        :param week: selected week. 0 or Nonoe for all
        :param territory_id: territory. 0 or None for whole country
        :param territory_type_id: territory type. None or 4 for whole country
        :return pd.DataFrame:

        """
        sql_param = {'dataset_id':dataset_id, 
         'scale_id':scale_id, 
         'epiweek':week, 
         'epiyear':year, 
         'territory_id':territory_id, 
         'territory_select':'', 
         'territory_name':'', 
         'territory_join':''}
        territory_type2column = {1:'territory_id', 
         2:'regional', 
         3:'region'}
        if territory_id not in (0, None):
            sql_param['territory_name'] = ', territory.name AS territory_name'
            sql_param['territory_column'] = territory_type2column[territory_type_id]
            sql_param['territory_select'] = 'AND %(territory_column)s = %(territory_id)s' % sql_param
            sql_param['territory_join'] = 'LEFT JOIN territory\n                ON (delay.%(territory_column)s=territory.id)\n            WHERE 1=1\n            ' % sql_param
        if week is None or week == 0:
            sql_param['epiweek'] = 53
        sql = '\n        SELECT\n        delay.symptoms2notification as "Primeiros sintomas à notificação",\n        delay.symptoms2digitalization AS "Primeiros sintomas à digitalização",\n        delay.notification2digitalization AS "Notificação à digitalização",\n        delay.symptoms2antiviral AS "Primeiros sintomas ao tratamento",\n        delay.symptoms2sample AS "Primeiros sintomas à coleta",\n        delay.sample2ifi AS "Coleta a resultado de IFI",\n        delay.sample2PCR AS "Coleta a resultado de PCR",\n        delay.notification2closure AS "Notificação ao encerramento"        \n        %(territory_name)s\n        FROM\n            (SELECT * \n            FROM\n                delay_table\n            WHERE\n                epiyear=%(epiyear)s\n                AND dataset_id=%(dataset_id)s\n                AND epiweek <= %(epiweek)s\n                %(territory_select)s\n            ) as delay\n            %(territory_join)s\n        ' % sql_param
        with self.conn.connect() as (conn):
            df = pd.read_sql(sql, conn)
        if territory_id in (0, None):
            df['territory_name'] = 'Brasil'
        return df