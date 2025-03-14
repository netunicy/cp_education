from django.urls import path
from homepage import views

app_name = 'primary'

urlpatterns = [
    path('pri_fir_mat',views.books_image_view, name='pri_fir_mat'),
    path('pri_fir_gre',views.books_image_view, name='pri_fir_gre'),
]