# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/bdgt/commands/budget.py
# Compiled at: 2014-10-09 13:38:05
import calendar, datetime, logging
from collections import defaultdict
from StringIO import StringIO
import asciitable
from sqlalchemy.orm.exc import NoResultFound
from bdgt.models import BudgetItem, Category
from bdgt.storage.gateway import session_scope
_log = logging.getLogger(__name__)

class CmdSet(object):

    def __init__(self, category_name, period, amount):
        self.category_name = category_name
        self.period = period
        self.amount = amount

    def __call__(self):
        with session_scope() as (session):
            try:
                category = session.query(Category).filter_by(name=self.category_name).one()
            except NoResultFound:
                raise ValueError(('{} not found').format(self.category_name))

            budget_item = BudgetItem(datetime.datetime.now().date(), self.period, self.amount)
            category.budget_items.append(budget_item)
            session.add(category)
        return ('Budget for "{}" is set to {} per {}').format(self.category_name, self.amount, self.period)


class CmdStatus(object):

    def __init__(self, month, year):
        self.month = month
        self.year = year

    def __call__(self):
        with session_scope() as (session):
            categories = session.query(Category).order_by(Category.name).all()
        output = defaultdict(list)
        for category in categories:
            if category.budget_items is None or category.budget_items == []:
                continue
            txs = category.transactions
            _, num_days = calendar.monthrange(self.year, self.month)
            beg_date = datetime.date(self.year, self.month, 1)
            end_date = beg_date + datetime.timedelta(days=num_days)
            txs = filter(lambda x: x.is_debit(), txs)
            txs = filter(lambda x: x.is_in_period(beg_date, end_date), txs)
            budget_item = category.budget_items[(-1)]
            spent = sum([ abs(tx.amount) for tx in txs ], 0)
            rem = budget_item.amount - spent
            spent_pct = spent / budget_item.amount * 100.0
            rem_pct = rem / budget_item.amount * 100.0
            output['category'].append(category.name)
            output['budget'].append(('{:.2f}').format(budget_item.amount))
            output['spent'].append(('{:.2f} ({:.0f}%)').format(spent, spent_pct))
            output['remaining'].append(('{:.2f} ({:.0f}%)').format(rem, rem_pct))
            output['transactions'].append(len(txs))

        if not output:
            return 'No budget set'
        else:
            output_io = StringIO()
            asciitable.write(output, output_io, Writer=asciitable.FixedWidth, names=[
             'category', 'budget', 'spent', 'remaining',
             'transactions'])
            return output_io.getvalue()