from django.shortcuts import render
from src.funcs import generate_logo
from candy_shop.models import (SweetType,
                               User, )


def sweet_page(request, sweet_type):
    sweet_types = SweetType.objects.filter().values_list()
    sweet_types = [type[1] for type in sweet_types]
    if sweet_type in sweet_types:
        sweets = SweetType.objects.get(sweet_type=sweet_type).sweets.all().order_by('sweet')
        signed_user = User.objects.filter(login=1).first()
        pic_name = f"{(sweet_type.lower()).replace(' ', '_')}.png"
        return render(request, 'sweet_page.html', {
            'sweets': sweets, 'signed_user': signed_user, 'pic_name': pic_name,
            'sweet_type': sweet_type, 'logo_name': generate_logo()})
    else:
        return render(request, '404.html')
