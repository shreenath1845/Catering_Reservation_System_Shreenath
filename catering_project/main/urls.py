# main/urls.py
from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import LogoutView


urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register, name='register'),
    path('admin/dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('admin/add-item/', views.add_menu_item_view, name='add_item_page'),
    path('admin/view-menu/', views.view_menu_admin, name='view_menu_admin'),
    path('customer/dashboard/', views.customer_dashboard, name='customer_dashboard'),
    path('logout/', LogoutView.as_view(next_page='home'), name='logout'),  # ✔️ logout to home
    path('customer/menu/', views.view_menu, name='view_menu'),
    path('customer/cart/', views.my_cart, name='my_cart'),
    path('admin/add-item/', views.add_menu_item, name='add_menu_item'),
    path('admin/edit-item/<int:item_id>/', views.edit_menu_item, name='edit_menu_item'),
    path('admin/delete-item/<int:item_id>/', views.delete_menu_item, name='delete_menu_item'),
    path('customer/view-menu/', views.view_menu, name='view_menu'),
    path('customer/orders/', views.my_orders, name='my_orders'),
    path('customer/view-menu/', views.view_menu, name='view_menu'),
    path('cart/add/<int:item_id>/', views.add_to_cart, name='add_to_cart'),
    path('customer/cart/', views.view_cart, name='view_cart'),
    path('cart/remove/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('customer/place-order/', views.place_order, name='place_order'),
    path('cancel-order/<int:order_id>/', views.cancel_order, name='cancel_order'),
    path('admin/orders/', views.admin_orders, name='admin_orders'),
    path('admin/orders/update/<int:order_id>/', views.update_order_status, name='update_order_status'),
    path('admin/orders/', views.admin_orders, name='admin_orders'),
    path('admin/orders/delete/<int:order_id>/', views.delete_cancelled_order, name='delete_cancelled_order'),
    path('customer/reserve/', views.make_reservation, name='make_reservation'),
    path('customer/reserve/', views.make_reservation, name='make_reservation'),
    path('customer/my-reservations/', views.my_reservations, name='my_reservations'),
    path('customer/cancel-reservation/<int:reservation_id>/', views.cancel_reservation, name='cancel_reservation'),
    path('admin/reservations/', views.admin_reservations, name='admin_reservations'),
    path('admin/reservations/update/<int:reservation_id>/', views.update_reservation_status, name='update_reservation_status'),
    path('admin/reservations/delete/<int:reservation_id>/', views.delete_reservation, name='delete_reservation'),
    path('customer/profile/', views.customer_profile, name='customer_profile'),
]
