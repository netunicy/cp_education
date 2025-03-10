from django.urls import path
from .import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'partnership'

urlpatterns = [
    path('terms', views.T_C_Partner, name='terms'),
    path('partner_register', views.partner_register, name='partner_register'),
    path('partner_done', views.partner_done, name='partner_done'),
]