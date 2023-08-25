from django.urls import path
from .views import cart, add_to_cart, remove_from_cart, update_cart
from . import views


urlpatterns = [
    path('cart/', cart, name='cart'),
    path('add-to-cart/<int:product_id>/<int:color_id>/', add_to_cart, name='add_to_cart'),
    path('remove-from-cart/<int:cart_item_id>/', remove_from_cart, name='remove_from_cart'),
    path('update-cart/', update_cart, name='update_cart'),
    path('order/', views.order_view, name='order'),

]