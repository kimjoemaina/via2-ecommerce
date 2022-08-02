from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('store/', views.store, name = 'store'),
    path('store/category/<slug:category_slug>/', views.store, name='products_by_category'),
    path('store/category/<slug:category_slug>/<slug:product_slug>/', views.product_detail, name='product_detail'),
    path('cart/', views.cart, name='cart'),
    path('cart/checkout/', views.checkout, name='checkout'),
    path('cart/add_cart/<int:product_id>/', views.add_cart, name='add_cart'),
    path('subtract_cart/<int:product_id>/<int:cart_item_id>', views.subtract_cart, name='subtract_cart'),
    path('remove_cart_item/<int:product_id>/<int:cart_item_id>', views.remove_cart_item, name='remove_cart_item'),
    path('store/search/', views.search, name='search'), 
]
