from src.funcs import make_list_of_lists
from src.settings import (SWEET_PIC_NAMES,
                          SWEETS_ON_THE_LINE, )
from django.shortcuts import (render,
                              redirect, )
from candy_shop.models import (SweetType,
                               User, )


def home_page(request):
    sweet_types = SweetType.objects.filter()
    signed_user = User.objects.filter(login=1).first()
    # добавление картинки "отсутствует" новому типу сладости.
    loaded_pics_number = len(SWEET_PIC_NAMES)
    sweet_types_number = len(sweet_types)
    if sweet_types_number > loaded_pics_number:
        for i in range(loaded_pics_number, sweet_types_number):
            SWEET_PIC_NAMES.append('none.png')
    # вывод типов сладостей в ряд в заданном количестве.
    sweet_types = make_list_of_lists(sweet_types, SWEETS_ON_THE_LINE, sweet_types_number)
    sweet_pic_names = make_list_of_lists(SWEET_PIC_NAMES, SWEETS_ON_THE_LINE, sweet_types_number)
    sweet_object = []
    for type, pic in zip(sweet_types, sweet_pic_names):
        row = list(zip(type, pic))
        sweet_object.append(row)
    if request.method == 'GET':
        return render(request, 'home_page.html', {
            'sweet_object': sweet_object, 'signed_user': signed_user, 'row_len': SWEETS_ON_THE_LINE})
    # выход пользователя с перенаправлением на страницу откуда выход был совершен.
    elif request.method == 'POST':
        User.objects.filter(login=1).update(login=0)
        referer = request.META['HTTP_REFERER']
        return redirect(referer)
