from django.urls import path
from .import views

app_name = 'contact_us'

urlpatterns = [
    path('form/',views.contact_us, name='form'),
]