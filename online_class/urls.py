from django.contrib.auth import views as auth_views
from django.contrib import admin
from django.urls import include, path
from django.views.generic.base import RedirectView
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
     path('admin/', admin.site.urls),
     path('captcha/', include('captcha.urls')),
     path('tinymce/', include('tinymce.urls')),
     path('', include(('homepage.urls', 'homepage'), namespace='homepage')),
     path('accounts/', include(('accounts.urls','accounts'),namespace='accounts')),
     path('partnership/', include(('partnership.urls','partnership'),namespace='partnership')),
     path('contact_us/', include(('contact_us.urls','contact_us'),namespace='contact_us')),
     path('blogs/', include(('blogs.urls','blogs'),namespace='blogs')),
     path('primary/', include(('primary.urls','primary'),namespace='primary')),
     path('favicon.ico', RedirectView.as_view(url='/staticfiles/favico/favicon.ico')),
     path('reset/<uidb64>/<token>/', 
         auth_views.PasswordResetConfirmView.as_view(template_name="password_reset_form.html"),
         name="password_reset_confirm"),
     path('accounts/reset_password_sent/', 
         auth_views.PasswordResetDoneView.as_view(template_name="password_reset_sent.html"), 
         name='password_reset_done'),
     path('accounts/reset_password_complete/', 
         auth_views.PasswordResetCompleteView.as_view(template_name="password_reset_done.html"), 
         name='password_reset_complete'),


]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
