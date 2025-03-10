from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
app_name = 'accounts'
urlpatterns = [
    path('login_user/', views.login_user, name='login_user'),
    path('user_register/', views.user_register, name='user_register'),
    path('logout/', views.logout_view, name='logout'),
    path('forgot_username/',views.forgot_username, name='forgot_username'),
    path('changepassword/',views.changepassword, name='changepassword'),
    path('activate/<str:activation_key>/<int:user_id>/', views.activate_account, name='activate'),
    path('accounts/reset_password/', 
         auth_views.PasswordResetView.as_view(template_name="password_reset.html"), 
         name='reset_password'),
    path('change_username/',views.change_username, name='change_username'),
]
