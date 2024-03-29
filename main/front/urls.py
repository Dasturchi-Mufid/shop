from django.urls import path
from . import views


app_name = 'front'



urlpatterns = [
    path('',views.index,name='index'),
    path('product/<str:code>',views.product_detail,name='product_detail'),
    path('category/<str:code>',views.product_list,name='product_list'),
]