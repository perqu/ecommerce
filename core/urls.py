from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import SpectacularRedocView, SpectacularSwaggerView, SpectacularAPIView
from core.views import health_check, view1, view2, index

urlpatterns = [
    # admin
    path("admin/", admin.site.urls),
    # apps
    path('users', include('users.urls')),
    path('items', include('items.urls')),
    path('chat', include('chat.urls')),
    # test
    path('', index, name='index'),
    path('button1', view1, name='view1'),
    path('button2', view2, name='view2'),
    # docs
    path('health/', health_check, name='health_check'),
    path('docs', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('redoc', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
    path('api/schema', SpectacularAPIView.as_view(), name='schema'),
]