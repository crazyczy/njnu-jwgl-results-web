from django.conf.urls import url
from django.conf import settings
from django.conf.urls.static import static
from .views import index, login_view, logout_view, password, realtime

urlpatterns = [
    url(r'^$', index, name='index'),
    url(r'^login$', login_view, name='login_view'),
    url(r'^logout$', logout_view, name='logout_view'),
    url(r'^password$', password, name='password'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
