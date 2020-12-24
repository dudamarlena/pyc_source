# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/mal/pCloud/Python/cold-start-recommender/csrec/recommender.py
# Compiled at: 2017-12-01 12:35:53
import pandas as pd, numpy as np
from time import time
import logging
from csrec.tools.singleton import Singleton
from csrec import factory_dal

class Recommender(Singleton):
    """
    Cold Start Recommender
    """

    def __init__(self, dal_name='mem', dal_params={}, max_rating=5, log_level=logging.INFO):
        self.logger = logging.getLogger('csrc')
        self.logger.setLevel(log_level)
        ch = logging.StreamHandler()
        ch.setLevel(log_level)
        self.logger.addHandler(ch)
        self.logger.debug('============ Logger initialized ================')
        self.db = factory_dal.Dal.get_dal(name=dal_name, **dal_params)
        self.db.register(self.db.serialize, self.on_serialize)
        self.db.register(self.db.restore, self.on_restore)
        self._items_cooccurrence = pd.DataFrame
        self.cooccurrence_updated = 0.0
        self._categories_cooccurrence = {}
        self.items_by_popularity = []
        self.last_serialization_time = 0.0
        self.max_rating = max_rating

    def on_serialize(self, filepath, return_value):
        if return_value is None or return_value:
            self.last_serialization_time = time()
        else:
            self.logger.error('[on_serialize] data backup failed on file %s, last successful backup at: %f' % (
             filepath,
             self.last_serialization_time))
        return

    def on_restore(self, filepath, return_value):
        if return_value is not None and not return_value:
            self.logger.error('[on_restore] restore from serialized data fail: ', filepath)
        else:
            self._create_cooccurrence()
        return

    def _create_cooccurrence(self):
        """
        Create or update the co-occurrence matrix
        :return:
        """
        all_ratings = self.db.get_item_actions()
        df = pd.DataFrame(all_ratings).fillna(0).astype(int)
        df_items = (df / df).replace(np.inf, 0).replace(np.nan, 0)
        co_occurrence = df_items.fillna(0).dot(df_items.T)
        self._items_cooccurrence = co_occurrence
        df_n_cat_item = {}
        info_used = self.db.get_info_used()
        if len(info_used) > 0:
            n_categories_item_ratings = self.db.get_n_categories_item_ratings()
            for i in info_used:
                df_n_cat_item[i] = pd.DataFrame(n_categories_item_ratings.get(i)).fillna(0).astype(int)

            for i in info_used:
                if type(df_n_cat_item.get(i)) == pd.DataFrame:
                    df_n_cat_item[i] = (df_n_cat_item[i] / df_n_cat_item[i]).replace(np.nan, 0)
                    self._categories_cooccurrence[i] = df_n_cat_item[i].T.dot(df_n_cat_item[i])

        self.cooccurrence_updated = time()

    def compute_items_by_popularity(self):
        """
        As per name, get self.items_by_popularity
        :return: None
        """
        df_item = pd.DataFrame(self.db.get_item_actions()).T.fillna(0).astype(int).sum()
        df_item.sort_values(inplace=True, ascending=False)
        pop_items = list(df_item.index)
        all_items = set(self.db.get_items().keys())
        self.items_by_popularity = pop_items + list(all_items - set(pop_items))

    def get_recommendations(self, user_id, max_recs=50, fast=False, algorithm='item_based'):
        """
        algorithm item_based:
            - Compute recommendation to user using item co-occurrence matrix (if the user
            rated any item...)
            - If there are less than max_recs recommendations, the remaining
            items are given according to popularity. Scores for the popular ones
            are given as score[last recommended]*index[last recommended]/n
            where n is the position in the list.
            - Recommended items above receive a further score according to categories
        :param user_id: the user id as in the collection of 'users'
        :param max_recs: number of recommended items to be returned
        :param fast: Compute the co-occurrence matrix only if it is one hour old or
                     if matrix and user vector have different dimension
        :return: list of recommended items
        """
        user_id = str(user_id).replace('.', '')
        df_tot_cat_user = {}
        df_n_cat_user = {}
        rec = pd.Series()
        user_has_rated_items = False
        rated_infos = []
        df_user = None
        if self.db.get_item_actions(user_id=user_id):
            user_has_rated_items = True
            df_user = pd.DataFrame(self.db.get_item_actions()).fillna(0).astype(int)[[user_id]]
        info_used = self.db.get_info_used()
        if len(info_used) > 0:
            tot_categories_user_ratings = self.db.get_tot_categories_user_ratings()
            n_categories_user_ratings = self.db.get_n_categories_user_ratings()
            for i in info_used:
                if i in tot_categories_user_ratings and user_id in tot_categories_user_ratings[i]:
                    rated_infos.append(i)
                    df_tot_cat_user[i] = pd.DataFrame(tot_categories_user_ratings.get(i)).fillna(0).astype(int)[[user_id]]
                    df_n_cat_user[i] = pd.DataFrame(n_categories_user_ratings.get(i)).fillna(0).astype(int)[[user_id]]

        if user_has_rated_items:
            if not fast or time() - self.cooccurrence_updated > 1800:
                self._create_cooccurrence()
            try:
                rec = self._items_cooccurrence.T.dot(df_user[user_id])
            except:
                self.logger.debug('[get_recommendations] 1st rec production failed, calling _create_cooccurrence.')
                self._create_cooccurrence()
                rec = self._items_cooccurrence.T.dot(df_user[user_id])
                self.logger.debug('[get_recommendations] Rec: %s', rec)

            rec.sort_values(inplace=True, ascending=False)
            if len(rec) < max_recs:
                if not fast or len(self.items_by_popularity) == 0:
                    self.compute_items_by_popularity()
                for v in self.items_by_popularity:
                    if len(rec) == max_recs:
                        break
                    elif v not in rec.index:
                        n = len(rec)
                        rec.set_value(v, rec.values[(n - 1)] * n / (n + 1.0))

        else:
            if not fast or len(self.items_by_popularity) == 0:
                self.compute_items_by_popularity()
            for i, v in enumerate(self.items_by_popularity):
                if len(rec) == max_recs:
                    break
                rec.set_value(v, self.max_rating / (i + 1.0))

            global_rec = rec.copy()
            if len(info_used) > 0:
                cat_rec = {}
                if not fast or time() - self.cooccurrence_updated > 1800:
                    self._create_cooccurrence()
                for cat in rated_infos:
                    user_vec = df_tot_cat_user[cat][user_id] / df_n_cat_user[cat][user_id].replace(0, 1)
                    try:
                        cat_rec[cat] = self._categories_cooccurrence[cat].T.dot(user_vec)
                        cat_rec[cat].sort_values(inplace=True, ascending=False)
                    except:
                        self._create_cooccurrence()
                        cat_rec[cat] = self._categories_cooccurrence[cat].T.dot(user_vec)
                        cat_rec[cat].sort(ascending=False)

                    for item_id, score in rec.iteritems():
                        try:
                            item = self.db.get_items(item_id=item_id)
                            item_info_value = item.get(cat, '')
                            if item_info_value:
                                global_rec[item_id] = score + cat_rec.get(cat, {}).get(item_info_value, 0)
                        except Exception as e:
                            self.logger.error('item %s, category %s', item_id, cat)
                            logging.exception(e)

            global_rec.sort_values(inplace=True, ascending=False)
            if user_has_rated_items:
                rated = df_user[user_id] != 0
                items = [ i for i in global_rec.index if not rated.get(i, False) ]
                if items:
                    return items[:max_recs]
                return []
            else:
                try:
                    return list(global_rec.index)[:max_recs]
                except:
                    return

        return