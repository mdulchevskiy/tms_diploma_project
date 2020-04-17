from datetime import datetime
from django.conf import settings
from pytz import UTC
from django.core.mail import send_mail
from django.contrib import messages
from django.template import loader
from django.shortcuts import (render,
                              redirect, )
from src.funcs import (generate_logo,
                       sweets_to_json,
                       get_superuser_email,
                       check_connection, )
from candy_shop.models import (User,
                               Basket,
                               Order, )
from candy_shop.forms import (CheckoutGuestForm,
                              CheckoutUserForm, )


def checkout(request):
    sweets = Basket.objects.filter().order_by('sweet')
    signed_user = User.objects.filter(login=1).first()
    sweets_costs = Basket.objects.filter().values_list('cost')
    sweets_costs = [cost[0] for cost in sweets_costs]
    order_total = round(sum(sweets_costs), 2)
    if signed_user:
        Form = CheckoutUserForm
        address = signed_user.address
    else:
        Form = CheckoutGuestForm
        address = None
    if request.method == 'GET':
        current_hour = datetime.now().hour
        if settings.CLOSING_HOUR > current_hour >= settings.OPENING_HOUR:
            return render(request, 'checkout_page.html', {
                'sweets': sweets, 'signed_user': signed_user, 'order_total': order_total,
                'logo_name': generate_logo(), 'form': Form(initial={'address': address})})
        else:
            return render(request, 'checkout_page.html', {
                'signed_user': signed_user, 'logo_name': generate_logo(), 'closed_status': True})
    elif request.method == 'POST':
        form = Form(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            json_sweets = sweets_to_json(sweets)
            order_date = datetime.now(tz=UTC)
            if signed_user:
                Order.objects.create(
                    user_type='User',
                    first_name=signed_user.first_name,
                    last_name=signed_user.last_name,
                    email=signed_user.email,
                    phone_number=signed_user.phone_number,
                    address=data['address'],
                    order_date=order_date,
                    delivery_date=data['delivery_date'],
                    comment=data['comment'],
                    order_info=json_sweets,
                    user=signed_user, )
            else:
                Order.objects.create(
                    first_name=data['first_name'],
                    last_name=data['last_name'],
                    email=data['email'],
                    phone_number=data['phone_number'],
                    address=data['address'],
                    order_date=order_date,
                    delivery_date=data['delivery_date'],
                    comment=data['comment'],
                    order_info=json_sweets, )
            admin_email = settings.ADMIN_EMAIL
            if not admin_email:
                admin_email = get_superuser_email()
            customer_email = signed_user.email if signed_user else data['email']
            order = Order.objects.filter(order_date=order_date).first()
            if check_connection():
                html_message = loader.render_to_string(
                    'email_message.html',
                    {'sweets': sweets, 'order_total': order_total, 'order': order}, )
                send_mail(
                    subject='Candy Shop (M.D.)',
                    message='',
                    html_message=html_message,
                    from_email=settings.EMAIL_HOST_USER,
                    recipient_list=[customer_email, admin_email])
                messages.add_message(request, messages.SUCCESS,
                                     f'{order.first_name}, thank you for your order!')
                messages.add_message(request, messages.SUCCESS,
                                     'You will shortly receive a confirmation email.')
            else:
                messages.add_message(request, messages.SUCCESS,
                                     f'{order.first_name}, thank you for your order!')
                messages.add_message(request, messages.INFO,
                                     'Cannot send a confirmation email. Check your internet connection.')
            Basket.objects.all().delete()
            return redirect('home_page')
        return render(request, 'checkout_page.html', {
            'sweets': sweets, 'signed_user': signed_user, 'order_total': order_total,
            'logo_name': generate_logo(), 'form': form})
