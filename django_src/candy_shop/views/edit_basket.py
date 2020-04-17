from django.contrib import messages
from django.shortcuts import (render,
                              redirect, )
from candy_shop.models import (Sweet,
                               User,
                               Basket, )


def add_to_basket(request, sweet_id):
    sweets = Sweet.objects.filter().values_list('id')
    sweets = [sweet[0] for sweet in sweets]
    if not int(sweet_id) in sweets:
        return render(request, '404.html')
    sweet_in_order = Basket.objects.filter(sweet_id=sweet_id).first()
    sweet_to_order = Sweet.objects.get(id=sweet_id)
    sweet_amount = int(request.POST.get('amount'))
    sweet_type = sweet_to_order.type
    referer = request.META['HTTP_REFERER']
    inclusion = 'checkout' in referer
    if sweet_amount or inclusion:
        # если сладость в корзине и зад. кол-во равно 0, сладость удаляется из корзины.
        if not sweet_amount:
            Basket.objects.filter(sweet_id=sweet_id).delete()
        # если сладость в корзине и зад. кол-во не равно 0, то ее кол-во в заказе обновляется на зад. величину.
        elif sweet_in_order:
            Basket.objects.filter(sweet_id=sweet_id).update(
                amount=sweet_amount,
                cost=sweet_amount * sweet_to_order.price)
            # если обновление количества произошло на странице сладости, выводится уведомление.
            if not inclusion:
                messages.add_message(request, messages.SUCCESS,
                                     f'The amount of "{sweet_to_order.sweet}" in your cart has been successfully '
                                     f'changed to {int(sweet_amount)} pcs.')
        # если сладость отсутсвует в корзине, она добавляется туда с зад. кол-вом.
        else:
            Basket.objects.create(
                sweet_id=sweet_id,
                sweet_type=sweet_to_order.type,
                sweet=sweet_to_order.sweet,
                price=sweet_to_order.price,
                amount=sweet_amount,
                cost=sweet_amount * sweet_to_order.price, )
            messages.add_message(request, messages.SUCCESS,
                                 f'{int(sweet_amount)} pcs. of "{sweet_to_order.sweet}" '
                                 f'has been successfully added to your cart.')
    if inclusion:
        return redirect('checkout')
    return redirect('sweet_page', sweet_type=sweet_type)


def delete_from_basket(request, sweet_id):
    sweet = Basket.objects.filter(sweet_id=sweet_id).first()
    if sweet:
        sweet.delete()
        return redirect('checkout')
    else:
        return render(request, '404.html')
