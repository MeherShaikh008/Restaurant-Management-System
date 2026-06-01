from django.urls import path
from django.contrib.auth import views as auth_views
from . import views


urlpatterns = [
    path('', views.index, name='index.html'),
    path('menu', views.menu, name='menu.html'),
    path('blog', views.blog, name='blog.html'),
    path('contact', views.contact, name='contact.html'),
    path('book', views.book, name='Book.html'),
    path('registration',views.registration,name="registration.html" ),
    path('login',views.login,name="login.html" ),
    path('logout',views.logout,name="logout.html" ),
    path("order/", views.order_page, name="order"),
    path("payment/<int:order_id>/", views.payment, name="payment"),
    path('success/', views.success, name='success'),
]
