from django.urls import path
from .import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'homepage'

urlpatterns = [
    path('', views.homepage, name='homepage'),
    path('Terms_and_Conditions/',views.Terms_and_Condition, name='Terms_and_Conditions'),
    path('lesson_details/<str:ref_code_book>/',views.lesson_details, name='lesson_details'),
    path('view_details/',views.view_details, name='view_details'),
    path('view_my_basket/',views.view_my_basket, name='view_my_basket'),
    path('add_basket_item/<str:chapter>/<str:ref_code_book>/<int:price>/',views.add_basket_item, name='add_basket_item'),
    path('check_out_payment/',views.check_out_payment, name='check_out_payment'),
    path('my_basket/<str:chapter>/<str:videos_url>/',views.my_basket, name='my_basket'),
    path('delete/<int:id>', views.delete, name='delete'),
    path('add_whachtime/',views.add_whachtime, name='add_whachtime'),
    path('pay_success/',views.pay_success, name='pay_success'),
    path('pay_cancel/',views.pay_cancel, name='pay_cancel'),
    path('create_invoice/',views.create_invoice, name='create_invoice'),
    path('my_purchases/',views.my_purchases_items, name='my_purchases'),
    path('show_video/<str:chapter_title>/<str:part_title>/<str:part_video>/',views.show_video, name='show_video'),
    path('search/',views.searchbar, name='search'),
    path('lesson_details_searchbar/<str:ref_code_book>/<str:chapter_title>/',views.lesson_details_searchbar, name='lesson_details_searchbar'),
    path('book_content/<str:ref_code_book>/', views.book_content, name='book_content'),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

