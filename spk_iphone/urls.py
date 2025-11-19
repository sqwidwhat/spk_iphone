from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('main.urls')),
]

#jazzmin
from django.conf.urls.i18n import i18n_patterns
urlpatterns += [
    path('i18n/', include('django.conf.urls.i18n')),
]