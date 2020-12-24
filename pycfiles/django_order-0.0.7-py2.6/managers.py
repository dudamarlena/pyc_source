# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/order/managers.py
# Compiled at: 2011-09-15 03:14:50
import order

def user_order_by(self, field):
    """
    Queryset method ordering objects by user ordering field.
    """
    model_label = order.utils.resolve_labels(('.').join([
     self.model._meta.app_label, self.model._meta.object_name]))
    orderitem_set = getattr(self.model, order.utils.resolve_order_item_related_set_name(model_label))
    order_model = orderitem_set.related.model
    db_table = order_model._meta.db_table
    pk_name = self.model._meta.pk.attname
    sanitized_field = field.lstrip('-')
    extra_select = {sanitized_field: '(SELECT %s from %s WHERE item_id=%s.%s)' % (
                       sanitized_field, db_table, self.model._meta.db_table, pk_name)}
    return self.extra(select=extra_select).all().order_by(field)