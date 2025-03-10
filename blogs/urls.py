from django.urls import path
from .import views


urlpatterns = [
    path('news/', views.news, name='news'),
    path('details/<int:pk>/<int:author_id>/', views.details ,name='details'),
]