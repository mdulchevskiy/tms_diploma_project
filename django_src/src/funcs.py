import json
import socket
from random import choice
from django.forms import model_to_dict
from django.contrib.auth.models import User as SuperUser


def generate_logo():
    logo_names = ['logo_2_1.png', 'logo_2_2.png', 'logo_2_3.png']
    logo_name = choice(logo_names)
    return logo_name


def sweets_to_json(sweets):
    sweets = [model_to_dict(sweet) for sweet in sweets]
    sweets_dict = {}
    for sweet in sweets:
        sweet_id = sweet['sweet_id']
        del sweet['id']
        del sweet['sweet_id']
        sweets_dict[sweet_id] = sweet
    json_sweets = json.dumps(sweets_dict)
    return json_sweets


def check_connection():
    try:
        socket.gethostbyaddr('www.yandex.ru')
    except socket.gaierror:
        return False
    return True


def get_superuser_email():
    superusers_emails = SuperUser.objects.filter(is_superuser=True).values_list('email')
    return superusers_emails[0][0]


def make_list_of_lists(iter_object, row, amount):
    list_of_lists = []
    count = 1
    for i, elem in enumerate(iter_object):
        if count == 1:
            line = []
        line.append(elem)
        count += 1
        if count > row:
            count = 1
            list_of_lists.append(line)
            line = []
        elif i + 1 == amount:
            list_of_lists.append(line)
    return list_of_lists


def order_message(order, sweets, order_total):
    message = f'Hello, {order.first_name}!\n\n' \
              f'Your order was successfully accepted {order.order_date.date()} at ' \
              f'{(order.order_date.time()).replace(microsecond=0)}\n\n' \
              'Delivery date:' + f'{order.delivery_date.date()} at {order.delivery_date.time()}'.rjust(45, '.') + \
              '\nDelivery address:' + f'{order.address}'.rjust(42, '.') + '\n' \
              'Phone number:' + f'{order.phone_number}'.rjust(46, '.') + '\n\n\n\n\n' \
              'Your order:\n' \
              '\nSweet'.ljust(53, ' ') + 'Price'.rjust(8, ' ') + 'Amount'.rjust(8, ' ') + 'Cost'.rjust(8, ' ') + \
              '\n' + ''.rjust(59, '-') + '\n'
    for sweet in sweets:
        message += f'{sweet.sweet}'.ljust(35, ' ') + \
                   f'{sweet.price}'.rjust(8, ' ') + \
                   f'{int(sweet.amount)}'.rjust(8, ' ') + \
                   f'{sweet.cost}'.rjust(8, ' ') + '\n'
    message += ''.rjust(59, '-') + '\n' + f'Order Total: {order_total} BYN'.rjust(59, ' ') + '\n\n\n' \
               'Comment:' + '\n\n'
    comment = order.comment.split()
    row_len = 0
    for word in comment:
        row_len += len(word)
        if row_len < 44:
            message += f'{word} '
        else:
            message += f'{word}\n'
            row_len = 0
    return message
