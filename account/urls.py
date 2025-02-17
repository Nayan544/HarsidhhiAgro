from django.urls import path
from django.contrib.auth import views as auth_views
from .views import (home,product,product_detail,category_detail,register,login_fun,logout_fun,
                     add_to_cart, view_cart, remove_from_cart, update_cart,checkout,
                     vendor_list,add_vendor,product_list,profile)
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('',home, name='home'),
    path('product',product, name='product'),
    path('product/<int:product_id>/', product_detail, name='product_detail'),
    path('products/category/<int:category_id>/', product_list, name='filtered_products'),
    path('category/<int:category_id>/',category_detail, name='category_detail'),
    path('register',register,name="register"),
    path('login',login_fun,name="login"),
    path('logout',logout_fun,name="logout"),
    path('cart/', view_cart, name='view_cart'),
    path('cart/add/<int:product_id>/', add_to_cart, name='add_to_cart'),
    path('cart/remove/<int:item_id>/', remove_from_cart, name='remove_from_cart'),
    path('cart/update/<int:item_id>/', update_cart, name='update_cart'),
    path('checkout/', checkout, name='checkout'),
    path('vendors/', vendor_list, name='vendor_list'),
    path('vendors/add/', add_vendor, name='add_vendor'),
    path('profile/',profile, name='profile'),

]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)



urlpatterns += [
    # Password reset URLs
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name="registrition/password_reset_email.html"), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name="registrition/password_reset_done.html"), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name="registrition/password_reset_confirm.html"), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name="registrition/password_reset_complete.html"), name='password_reset_complete'),
]