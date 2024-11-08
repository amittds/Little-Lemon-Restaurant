from django.urls import path
from .views import (
    home,
    about,
    book,
    booking_confirmation,
    review_booking,
    cancel_booking,
    booking_canceled,
    menu,
    category_menu,
    display_menu_items,
    customer_login,
    customer_logout,
    order_menu,
    add_to_cart,
    confirm_order,
    update_cart,
    order_summary,
)

urlpatterns = [
    path('', home, name='home'),
    path('about/', about, name='about'),
    path('book/', book, name='book'),
    path('booking/confirmation/<int:pk>/', booking_confirmation, name='booking_confirmation'),
    path('booking/review/<int:pk>/', review_booking, name='review_booking'),
    path('booking/cancel/<int:pk>/', cancel_booking, name='cancel_booking'),
    path('booking/canceled/', booking_canceled, name='booking_canceled'),
    path('menu/', menu, name='menu'),
    path('menu/category/<str:category_name>/', category_menu, name='category_menu'),
    path('menu/item/<int:pk>/', display_menu_items, name='display_menu_items'),
    path('customer/login/', customer_login, name='customer_login'),
    path('customer/logout/', customer_logout, name='customer_logout'),
    path('order/menu/', order_menu, name='order_menu'),
    path('order/add/<int:menu_id>/', add_to_cart, name='add_to_cart'),
    path('order/confirm/', confirm_order, name='confirm_order'),
    path('order/update/<int:item_id>/', update_cart, name='update_cart'),
    path('order/summary/<int:pk>/', order_summary, name='order_summary'),
]
