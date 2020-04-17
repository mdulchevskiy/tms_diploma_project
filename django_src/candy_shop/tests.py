from django.urls import reverse
from django.test import TestCase
from datetime import datetime
from pytz import UTC
from candy_shop.models import (SweetType,
                               Sweet,
                               Basket,
                               User,
                               Order, )


class CandyShopModelsTestCase(TestCase):
    def setUp(self):
        SweetType.objects.create(
            sweet_type='Chocolate', )
        SweetType.objects.create(
            sweet_type='Candy bar', )
        Sweet.objects.create(
            sweet='Milka',
            price='2.56',
            type=SweetType.objects.get(id=1), )
        Sweet.objects.create(
            sweet='Mars',
            price='1.07',
            type=SweetType.objects.get(id=2), )
        Sweet.objects.create(
            sweet='Nesquik',
            price='2.21',
            type=SweetType.objects.get(id=1), )
        Basket.objects.create(
            sweet_id=Sweet.objects.get(id=1).id,
            sweet_type=Sweet.objects.get(id=1).type,
            sweet=Sweet.objects.get(id=1).type,
            price=Sweet.objects.get(id=1).price,
            amount=2,
            cost=2 * Sweet.objects.get(id=1).price, )
        Basket.objects.create(
            sweet_id=Sweet.objects.get(id=2).id,
            sweet_type=Sweet.objects.get(id=2).type,
            sweet=Sweet.objects.get(id=2).type,
            price=Sweet.objects.get(id=2).price,
            amount=2,
            cost=2 * Sweet.objects.get(id=2).price, )
        User.objects.create(
            username='mdulchevskiy',
            password='1234567890',
            first_name='Maxim',
            last_name='Dulchevskiy',
            email='maksimdulchevskiy@mail.ru',
            phone_number='+375(29)113-84-51',
            address='Rokossovskogo 84, 235',
            login=1, )
        Order.objects.create(
            user_type=User,
            first_name=User.objects.get(id=1).first_name,
            last_name=User.objects.get(id=1).last_name,
            email=User.objects.get(id=1).email,
            phone_number=User.objects.get(id=1).phone_number,
            address=User.objects.get(id=1).address,
            order_date=datetime.now(tz=UTC),
            delivery_date=datetime(2022,12,31,15,16,tzinfo=UTC),
            comment='Good day, sir.',
            user=User.objects.get(id=1), )

    def test_create(self):
        # проверка на успешное создание объектов всех типов.
        sweet_type_object = SweetType.objects.filter(id=1).first()
        sweet_object = Sweet.objects.filter(id=1).first()
        basket_object = Basket.objects.filter(id=1).first()
        user_object = User.objects.filter(id=1).first()
        order_object = Order.objects.filter(id=1).first()
        self.assertNotEqual(sweet_type_object, None)
        self.assertNotEqual(sweet_object, None)
        self.assertNotEqual(basket_object, None)
        self.assertNotEqual(user_object, None)
        self.assertNotEqual(order_object, None)

    def test_get(self):
        # проверка отображения всех страниц.
        response1 = self.client.get('/')
        self.assertEqual(response1.status_code, 200)
        response2 = self.client.get('/Chocolate')
        self.assertEqual(response2.status_code, 200)
        response3 = self.client.get('/sign_in')
        self.assertEqual(response3.status_code, 200)
        response4 = self.client.get('/registration')
        self.assertEqual(response4.status_code, 200)
        response5 = self.client.get('/checkout')
        self.assertEqual(response5.status_code, 200)

    def test_post_home_sign_out(self):
        # проверка выхода пользователя и перенаправления на страницу, откуда был выход совершен.
        user = User.objects.get(id=1)
        self.assertEqual(user.login, 1)
        response = self.client.post('/', {}, HTTP_REFERER='/checkout')
        user = User.objects.get(id=1)
        self.assertEqual(user.login, 0)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['Location'], '/checkout')

    def test_post_sign_in(self):
        # проверка авторизации пользователя.
        user = User.objects.filter(id=1)
        user.update(login=0)
        self.assertEqual(user.first().login, 0)
        response = self.client.post('/sign_in/', {'username': 'mdulchevskiy', 'password': '1234567890'})
        user = User.objects.get(id=1)
        self.assertEqual(user.login, 1)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['Location'], '/sign_in/')

    def test_post_registration(self):
        # проверка регистрации пользователя и перенаправления на страницу авторизации.
        user = User.objects.filter(username='maxim').first()
        self.assertEqual(user, None)
        response = self.client.post('/registration/', {
            'first_name': 'Maxim',
            'last_name': 'Dulchevskiy',
            'email': 'blabla@mail.ru',
            'phone_number': '+375(29)113-84-51',
            'address': 'Rokossovskogo 84, 235',
            'username': 'maxim',
            'password': '1234567890',
            'conf_password': '1234567890',
        })
        user = User.objects.filter(username='maxim').first()
        self.assertNotEqual(user, None)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['Location'], '/sign_in/')

    def test_post_add_to_basket(self):
        # проверка добавления в корзину сладости количеством 0 шт. на странице сладости.
        response = self.client.post('/add/3', {'amount': '0'}, HTTP_REFERER='/Chocolate')
        sweet = Basket.objects.filter(id=3).first()
        self.assertEqual(sweet, None)
        self.assertEqual(response.status_code, 302)
        # проверка добавления в корзину сладости количеством 5 шт. на странице сладости.
        response = self.client.post('/add/3', {'amount': '5'}, HTTP_REFERER='/Chocolate')
        sweet = Basket.objects.get(id=3)
        self.assertEqual(sweet.amount, 5)
        self.assertEqual(response.status_code, 302)
        # проверка изменения количества сладости в корзине с 5 до 10 шт. на странице сладости.
        response = self.client.post('/add/3', {'amount': '10'}, HTTP_REFERER='/Chocolate')
        sweet = Basket.objects.get(id=3)
        self.assertEqual(sweet.amount, 10)
        self.assertEqual(response.status_code, 302)
        # проверка изменения количества сладости в корзине 10 до 0 шт. на странице сладости.
        response = self.client.post('/add/3', {'amount': '0'}, HTTP_REFERER='/Chocolate')
        sweet = Basket.objects.get(id=3)
        self.assertEqual(sweet.amount, 10)
        self.assertEqual(response.status_code, 302)
        # проверка изменения количества сладости в корзине с 10 до 5 шт. на странице корзины.
        response = self.client.post('/add/3', {'amount': '5'}, HTTP_REFERER='/checkout')
        sweet = Basket.objects.get(id=3)
        self.assertEqual(sweet.amount, 5)
        self.assertEqual(response.status_code, 302)
        # проверка изменения количества сладости в корзине с 5 до 0 шт. на странице корзины.
        response = self.client.post('/add/3', {'amount': '0'}, HTTP_REFERER='/checkout')
        sweet = Basket.objects.filter(id=3).first()
        self.assertEqual(sweet, None)
        self.assertEqual(response.status_code, 302)

    def test_post_del_from_basket(self):
        # проверка удаления сладости в корзине.
        response = self.client.post('/del/1', {}, HTTP_REFERER='/checkout')
        sweet = Basket.objects.filter(id=1).first()
        self.assertEqual(sweet, None)
        self.assertEqual(response.status_code, 302)
