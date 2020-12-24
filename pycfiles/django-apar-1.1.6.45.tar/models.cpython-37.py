# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ali/ownCloud/Project/python/django-aparnik-framework-project/testandbuildprojectframework/aparnik/packages/shops/vouchers/models.py
# Compiled at: 2020-03-03 06:09:02
# Size of source mod 2**32: 11326 bytes
from django.db import models
from django.db.models import Q, Sum
from django.db.models.functions import Coalesce
from django.db.models.signals import post_save
from django.db.models import Sum
from django.contrib.auth import get_user_model
from django.utils.timezone import now
import django.utils.translation as _
from django.core.exceptions import ValidationError
import datetime
import dateutil.relativedelta as relativedelta
from aparnik.settings import Setting
from aparnik.utils.utils import round, field_with_prefix
from aparnik.utils.formattings import formatprice
from aparnik.utils.fields import *
from aparnik.contrib.basemodels.models import BaseModel, BaseModelManager
User = get_user_model()

class VoucherManager(BaseModelManager):

    def get_queryset(self):
        return super(VoucherManager, self).get_queryset()

    def active(self, only_accessible=True):
        dict = {'is_active': True}
        if only_accessible:
            dict['expire_at__date__gte'] = now()
            dict['is_spent'] = False
        return (super(VoucherManager, self).active().filter)(**dict)

    def this_user(self, user, only_accessible=True):
        return self.active(only_accessible).filter(user_obj=user)

    def add_voucher_by_admin_command(self, user, quantity, description):
        from aparnik.packages.shops.orders.models import Order, Product
        product = Product.objects.get(id=(Setting.objects.get(key='MANAGER_PRODUCT_ID').get_value()))
        order = Order.objects.create(user=user)
        order.add_item(product, quantity, description)
        if order.get_total_cost_order() > 0:
            order.save()
            order.pay_success()
            voucher = Voucher.objects.get(order_item_obj=(order.items.first()), user_obj=user)
            voucher.quantity = quantity
            voucher.quantity_remain = quantity
            voucher.save()
        else:
            order.delete()

    def quantities_accessible(self, user):
        return self.this_user(user).aggregate(quantities=(Sum('quantity_remain')))['quantities'] or 0

    def price_accessible(self, user):
        quantities = self.quantities_accessible(user)
        price = round(quantities * Setting.objects.get(key='APARNIK_BON_VALUE').get_value())
        return price

    def price_accessible_string(self, user):
        return '%s' % formatprice.format_price(self.price_accessible(user))

    def quantities_accessible_on_order(self, order):
        max_order_bon = 0
        try:
            max_order_bon = int(order.get_total_cost_order() / Setting.objects.get(key='APARNIK_BON_VALUE').get_value())
        except:
            pass

        if order.is_success:
            return VoucherOrderItem.objects.active().filter(item_obj__order_obj=order).aggregate(quantities=(Sum('quantity_usage')))['quantities'] or 0
        quantity_order = 0
        for item in order.items.all():
            quantity_order = quantity_order + item.maximum_use_aparnik_bon
            if quantity_order >= max_order_bon:
                quantity_order = max_order_bon
                break

        quantity_user = self.quantities_accessible(order.user)
        if quantity_order > quantity_user:
            return quantity_user
        return quantity_order

    def price_accessible_on_order(self, order):
        quantities = self.quantities_accessible_on_order(order)
        price = round(quantities * Setting.objects.get(key='APARNIK_BON_VALUE').get_value())
        return price

    def price_accessible_on_order_string(self, order):
        return '%s' % formatprice.format_price(self.price_accessible_on_order(order))

    def change_order--- This code section failed: ---

 L. 108         0  SETUP_LOOP          154  'to 154'
                2  LOAD_FAST                'order'
                4  LOAD_ATTR                items
                6  LOAD_METHOD              all
                8  CALL_METHOD_0         0  '0 positional arguments'
               10  GET_ITER         
               12  FOR_ITER            152  'to 152'
               14  STORE_FAST               'item'

 L. 109        16  SETUP_EXCEPT         62  'to 62'

 L. 110        18  LOAD_FAST                'self'
               20  LOAD_METHOD              get_queryset
               22  CALL_METHOD_0         0  '0 positional arguments'
               24  LOAD_ATTR                get
               26  LOAD_FAST                'item'
               28  LOAD_CONST               ('order_item_obj',)
               30  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
               32  STORE_FAST               'voucher'

 L. 111        34  LOAD_FAST                'item'
               36  LOAD_ATTR                aparnik_bon_return
               38  LOAD_FAST                'voucher'
               40  STORE_ATTR               quantity

 L. 112        42  LOAD_FAST                'order'
               44  LOAD_ATTR                is_success
               46  LOAD_FAST                'voucher'
               48  STORE_ATTR               is_active

 L. 113        50  LOAD_FAST                'voucher'
               52  LOAD_METHOD              save
               54  CALL_METHOD_0         0  '0 positional arguments'
               56  POP_TOP          
               58  POP_BLOCK        
               60  JUMP_BACK            12  'to 12'
             62_0  COME_FROM_EXCEPT     16  '16'

 L. 115        62  POP_TOP          
               64  POP_TOP          
               66  POP_TOP          

 L. 116        68  LOAD_FAST                'order'
               70  LOAD_ATTR                is_success
               72  POP_JUMP_IF_FALSE   110  'to 110'
               74  LOAD_FAST                'item'
               76  LOAD_ATTR                aparnik_bon_return
               78  LOAD_CONST               0
               80  COMPARE_OP               ==
               82  POP_JUMP_IF_FALSE   112  'to 112'
               84  LOAD_FAST                'item'
               86  LOAD_ATTR                product_obj
               88  LOAD_ATTR                pk
               90  LOAD_GLOBAL              Setting
               92  LOAD_ATTR                objects
               94  LOAD_ATTR                get
               96  LOAD_STR                 'MANAGER_PRODUCT_ID'
               98  LOAD_CONST               ('key',)
              100  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
              102  LOAD_METHOD              get_value
              104  CALL_METHOD_0         0  '0 positional arguments'
              106  COMPARE_OP               !=
              108  POP_JUMP_IF_FALSE   112  'to 112'
            110_0  COME_FROM            72  '72'

 L. 117       110  BREAK_LOOP       
            112_0  COME_FROM           108  '108'
            112_1  COME_FROM            82  '82'

 L. 119       112  LOAD_GLOBAL              Voucher
              114  LOAD_ATTR                objects
              116  LOAD_ATTR                create

 L. 120       118  LOAD_FAST                'item'

 L. 121       120  LOAD_FAST                'item'
              122  LOAD_ATTR                aparnik_bon_return

 L. 122       124  LOAD_FAST                'item'
              126  LOAD_ATTR                aparnik_bon_return

 L. 123       128  LOAD_FAST                'order'
              130  LOAD_ATTR                user

 L. 124       132  LOAD_FAST                'item'
              134  LOAD_ATTR                product_obj
              136  LOAD_ATTR                aparnik_bon_return_expire_date
              138  LOAD_CONST               ('order_item_obj', 'quantity', 'quantity_remain', 'user_obj', 'expire_at')
              140  CALL_FUNCTION_KW_5     5  '5 total positional and keyword args'
              142  STORE_FAST               'voucher'
              144  POP_EXCEPT       
              146  JUMP_BACK            12  'to 12'
              148  END_FINALLY      
              150  JUMP_BACK            12  'to 12'
              152  POP_BLOCK        
            154_0  COME_FROM_LOOP        0  '0'

Parse error at or near `POP_EXCEPT' instruction at offset 144

    def redeem_for_order(self, order):
        allow_vouchers_quantity = self.quantities_accessible(order.user)
        total_usage = 0
        queryset = Voucher.objects.this_user(order.user).order_by('-quantity_remain')
        items = sorted((order.items.all()), key=(lambda x: x.maximum_use_aparnik_bon), reverse=True)
        for item in items:
            quantity = item.maximum_use_aparnik_bon
            for voucher in queryset.all():
                q = 0
                if total_usage >= allow_vouchers_quantity:
                    break
                elif voucher.quantity_remain >= quantity:
                    q = quantity
                else:
                    q = voucher.quantity_remain
                if total_usage + q >= allow_vouchers_quantity:
                    q = allow_vouchers_quantity - total_usage
                total_usage = total_usage + q
                VoucherOrderItem.objects.create(voucher_obj=voucher,
                  item_obj=item,
                  quantity_usage=q)
                if quantity - q == 0:
                    break
                quantity = quantity - q


class Voucher(BaseModel):
    user_obj = models.ForeignKey(User, related_name='voucher_user', on_delete=(models.CASCADE), verbose_name=(_('User')))
    quantity = models.PositiveIntegerField(default=0, verbose_name=(_('Quantity')))
    quantity_remain = models.PositiveIntegerField(default=0, verbose_name=(_('Quantity Remain')))
    order_item_obj = models.OneToOneField('orders.OrderItem', related_name='voucher_order_item', on_delete=(models.CASCADE), verbose_name=(_('Order Item')))
    expire_at = models.DateTimeField(default=(datetime.datetime(2300, 10, 5, 18, 0)), verbose_name=(_('Expire at')))
    is_active = models.BooleanField(default=True, verbose_name=(_('Is Active')))
    is_spent = models.BooleanField(default=False, verbose_name=(_('Is spent')))
    order_item_obj_spent = models.ManyToManyField('orders.OrderItem', through='VoucherOrderItem', related_name='voucher_order_item_spent', verbose_name=(_('Item Spent this voucher')))
    objects = VoucherManager()

    def clean(self):
        pass

    def save(self, *args, **kwargs):
        self.full_clean()
        return (super(Voucher, self).save)(*args, **kwargs)

    def __str__(self):
        return str(self.order_item_obj)

    class Meta:
        verbose_name = _('Voucher')
        verbose_name_plural = _('Vouchers')

    @property
    def price(self):
        price = round(self.quantity * Setting.objects.get(key='APARNIK_BON_VALUE').get_value())
        return price

    @property
    def price_string(self):
        return '%s' % formatprice.format_price(self.price)

    @staticmethod
    def sort_voucher(return_key='voucher', prefix=''):
        sort = {return_key: {'label':'بن های هدیه', 
                      'queryset_filter':Q(), 
                      'annotate_command':{'sort_count': Coalesce(Sum(field_with_prefix('quantity_usage', prefix=prefix)), 0)}, 
                      'key_sort':'sort_count'}}
        return sort


class VoucherOrderItemManager(models.Manager):

    def get_queryset(self):
        return super(VoucherOrderItemManager, self).get_queryset()

    def active(self):
        return self.get_queryset()


class VoucherOrderItem(models.Model):
    voucher_obj = models.ForeignKey(Voucher, related_name='voucher_model', on_delete=(models.CASCADE), verbose_name=(_('Voucher')))
    item_obj = models.ForeignKey('orders.OrderItem', related_name='voucher_item_spent', on_delete=(models.CASCADE), verbose_name=(_('Item Spent')))
    quantity_usage = models.IntegerField(default=0, verbose_name=(_('Quantity Usage')))
    created_at = models.DateTimeField(auto_now_add=True, auto_now=False, verbose_name=(_('Created at')))
    update_at = models.DateTimeField(auto_now_add=False, auto_now=True, verbose_name=(_('Update at')))
    objects = VoucherOrderItemManager()

    class Meta:
        verbose_name = _('Voucher Order Item')
        verbose_name_plural = _('Voucher Order Items')

    def clean(self):
        queryset = VoucherOrderItem.objects.active().filter(voucher_obj=(self.voucher_obj))
        if self.id:
            queryset = queryset.exclude(pk=(self.id))
        quantity_spent = (queryset.aggregate(quantities=(Sum('quantity_usage')))['quantities'] or 0) + self.quantity_usage
        if quantity_spent > self.voucher_obj.quantity:
            raise ValidationError({'quantity_usage': [_('Total quantity usage doesnt match.')]})

    def save(self, *args, **kwargs):
        self.full_clean()
        return (super(VoucherOrderItem, self).save)(*args, **kwargs)

    def __str__(self):
        return str(self.voucher_obj)


def post_save_voucher_order_item_receiver(sender, instance, created, *args, **kwargs):
    voucher_obj = instance.voucher_obj
    quantity = VoucherOrderItem.objects.active().filter(voucher_obj=voucher_obj).aggregate(quantities=(Sum('quantity_usage')))['quantities'] or 0
    voucher_obj.is_spent = quantity == voucher_obj.quantity
    voucher_obj.quantity_remain = voucher_obj.quantity - quantity
    voucher_obj.save()


post_save.connect(post_save_voucher_order_item_receiver, sender=VoucherOrderItem)