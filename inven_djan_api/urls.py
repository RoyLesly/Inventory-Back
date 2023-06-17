from xml.dom.minidom import Document
from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.views.generic import TemplateView
from django.views.decorators.csrf import csrf_exempt

from rest_framework.authtoken import views


urlpatterns = [
    path('admin', admin.site.urls),
    path('user', include('user_control.urls')),
    #path('app', csrf_exempt(include('app_control.urls'))),
    path('app', include('app_control.urls')),
    path('auth/', views.obtain_auth_token),

    # REACT APP
    path('', TemplateView.as_view(template_name='index.html')),  # REACT
    path('login', TemplateView.as_view(template_name='index.html')),  # REACT
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
