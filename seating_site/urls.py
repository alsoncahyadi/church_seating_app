from django.contrib import admin
from django.urls import path
from django.conf.urls import include, url

urlpatterns = [
    url(r'^seating/', include('seating.urls')),
    url(r'^admin/', admin.site.urls),
]
