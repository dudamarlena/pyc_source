# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/mw/dev/pixelcms-shop-server/shop/sale/views.py
# Compiled at: 2016-12-28 12:52:27
# Size of source mod 2**32: 7612 bytes
from django.shortcuts import get_object_or_404, Http404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import generics, status, permissions
from rest_framework.decorators import permission_classes
from shop import settings as shop_settings
from .models import Cart, CartProduct, CartProductOptionValue, Order, OrderBillingData, OrderShippingData
from .serializers import CartDataSerializer, AddToCartSerializer, CartChangeQuantitySerializer, RemoveFromCartSerializer, PlaceOrderSerializer

class GetCartView(generics.RetrieveAPIView):
    serializer_class = CartDataSerializer

    def get_object(self):
        if self.request.user.is_authenticated:
            cart = Cart.objects.filter(customer=self.request.user.customer).first()
            if cart and not cart.converted_to_order:
                return cart
        elif self.kwargs.get('pk'):
            cart = Cart.objects.filter(converted_to_order=False, customer=None, pk=self.kwargs.get('pk')).first()
            if cart:
                pass
            return cart
        raise Http404


@api_view(['POST'])
def add_to_cart_view(request, cart_pk=None):
    serializer = AddToCartSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(status=status.HTTP_400_BAD_REQUEST)
    if not cart_pk:
        if request.user.is_authenticated:
            customer = request.user.customer
        else:
            customer = None
        cart = Cart.objects.create(customer=customer)
    else:
        if request.user.is_authenticated:
            customer = request.user.customer
        else:
            customer = None
        try:
            cart = Cart.objects.get(converted_to_order=False, customer=customer, pk=cart_pk)
        except Cart.DoesNotExist:
            cart = Cart.objects.create(customer=customer)

        product = serializer.validated_data['product']
        options = serializer.validated_data['options']
        possible_objects = CartProduct.objects.filter(cart=cart, product=product)
        obj = None
        for possible_obj in possible_objects:
            if len(possible_obj.options.all()) == len(options):
                obj = possible_obj
                for o in options:
                    if not possible_obj.options.filter(options_group=o['options_group'], option=o['option']).exists():
                        obj = None
                        break

                if obj:
                    break

        if obj:
            obj.quantity += serializer.validated_data['quantity']
            if obj.quantity > shop_settings.SHOP_QUANTITY_LIMIT:
                obj.quantity = shop_settings.SHOP_QUANTITY_LIMIT
            obj.save()
        else:
            obj = CartProduct.objects.create(cart=cart, product=product, quantity=serializer.validated_data['quantity'])
            for o in options:
                CartProductOptionValue.objects.create(cart_product=obj, options_group=o['options_group'], option=o['option'])

            obj.save()
    cart.save()
    return Response(CartDataSerializer(cart, context={'request': request}).data)


@permission_classes(permissions.IsAuthenticated)
@api_view(['POST'])
def bind_cart_view(request, pk):
    cart = get_object_or_404(Cart, customer=None, pk=pk)
    cart.customer = request.user.customer
    cart.save()
    return Response(CartDataSerializer(cart, context={'request': request}).data)


@api_view(['POST'])
def cart_change_quantity_view(request, cart_pk):
    serializer = CartChangeQuantitySerializer(data=request.data)
    if not serializer.is_valid():
        return Response(status=status.HTTP_400_BAD_REQUEST)
    if request.user.is_authenticated:
        customer = request.user.customer
    else:
        customer = None
    cart_product = get_object_or_404(CartProduct, cart__converted_to_order=False, cart__customer=customer, cart__pk=cart_pk, product__pk=serializer.validated_data['product'])
    cart_product.quantity = serializer.validated_data['quantity']
    cart_product.save()
    cart_product.cart.save()
    return Response(CartDataSerializer(cart_product.cart, context={'request': request}).data)


@api_view(['POST'])
def remove_from_cart_view(request, cart_pk):
    serializer = RemoveFromCartSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(status=status.HTTP_400_BAD_REQUEST)
    if request.user.is_authenticated:
        customer = request.user.customer
    else:
        customer = None
    cart_product = get_object_or_404(CartProduct, cart__converted_to_order=False, cart__customer=customer, cart__pk=cart_pk, product__pk=serializer.validated_data['product'])
    cart = cart_product.cart
    cart_product.delete()
    cart.save()
    return Response(CartDataSerializer(cart, context={'request': request}).data)


@api_view(['POST'])
@permission_classes((permissions.IsAuthenticated,))
def place_order_view(request, cart_pk):
    cart = get_object_or_404(Cart, converted_to_order=False, customer=request.user.customer, pk=cart_pk)
    serializer = PlaceOrderSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        payment_method = serializer.validated_data['payment_method']
        shipping_method = serializer.validated_data['shipping_method']
        if payment_method.set_waiting_for_payment_status:
            order_status = 'WAITING_FOR_PAYMENT'
    else:
        if shipping_method.set_waiting_for_shipping_status:
            order_status = 'WAITING_FOR_SHIPPING'
        else:
            order_status = 'COMPLETED'
        bd = serializer.validated_data['bd']
        if serializer.validated_data['shipping_data_form']:
            sd = serializer.validated_data['sd']
        else:
            sd = {'name': bd['name'], 
             'address': bd['address'], 
             'postal_code': bd['postal_code'], 
             'place': bd['place'], 
             'phone': bd.get('phone')}
        order = Order.objects.create(cart=cart, shipping_method=shipping_method, payment_method=payment_method, status=order_status, additional_comment=serializer.validated_data.get('additional_comment'))
        OrderBillingData.objects.create(order=order, **bd)
        OrderShippingData.objects.create(order=order, **sd)
        cart.converted_to_order = True
        cart.save()
        response_data = {'order_id': order.order_id, 
         'order_status': order.get_status_display(), 
         'payment_additional_info': order.payment_method.additional_info, 
         'has_payment_gateway': payment_method.has_gateway}
        return Response(response_data)