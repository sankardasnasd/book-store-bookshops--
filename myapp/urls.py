
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from bookstoremanagement import settings
from myapp import views

urlpatterns = [
    path('',views.public),
    path('public1',views.public1),
    path('public_post',views.public_post),
    path('login',views.login),
    path('userreg',views.userreg),
    path('adminhome',views.admin_home),
    path('blockuser/<id>',views.blockuser),
    path('unblockuser/<id>',views.unblockuser),
    path('admin_view_user',views.admin_view_user),
    path('admin_add_category',views.admin_add_category),
    path('admin_add_books',views.admin_add_books),
    path('admin_view_books',views.admin_view_books),
    path('admin_delete_book/<id>',views.admin_delete_book),
    path('admin_edit_books/<id>',views.admin_edit_books),
    path('admin_view_booking1/<id>',views.admin_view_booking1),
    path('admin_edit_books_post', views.admin_edit_books_post),
    path('admin_view_booking', views.admin_view_booking),
    path('admin_view_payments', views.admin_view_payments),
    path('viewmorebook/<int:id>', views.viewmorebook),


    path('user_home', views.user_home),
    path('search_books', views.search_books),
    path('terms', views.terms),
    path('user_view_profile', views.user_view_profile),
    path('user_edit_profile', views.user_edit_profile),
    path('user_edit_profile_post', views.user_edit_profile_post),
    path('user_view_books/<id>', views.user_view_books),
    path('user_home2', views.user_home2),
    path('user_booking_post', views.user_booking_post),
    path('view_cart', views.view_cart),
    path('user_booking1', views.user_booking1),
    path('user_booking/<id>', views.user_booking),
    path('purchase/<id>', views.purchase),
    path('remove_cart/<id>', views.remove_cart),
    path('on_payment_success', views.on_payment_success),
    path('user_view_orders', views.user_view_orders),
    path('user_pay_proceed/<id>/<amt>', views.user_pay_proceed),

]

