"""src URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from candy_shop.views import (home_page,
                              sign_in,
                              registration,
                              sweet_page,
                              add_to_basket,
                              delete_from_basket,
                              checkout,
                              db_info,
                              delete_from_order,
                              delete_from_user, )


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home_page, name='home_page'),
    path('sign_in/', sign_in, name='sign_in'),
    path('registration/', registration, name='registration'),
    path('<str:sweet_type>', sweet_page, name='sweet_page'),
    path('add_sw/<str:sweet_id>', add_to_basket, name='add_to_basket'),
    path('del_sw/<str:sweet_id>', delete_from_basket, name='del_from_basket'),
    path('checkout/', checkout, name='checkout'),
    path('db/', db_info, name='bd_info'),
    path('del_or/<str:order_id>', delete_from_order, name='del_from_order'),
    path('del_us/<str:user_id>', delete_from_user, name='del_from_user'),
]
