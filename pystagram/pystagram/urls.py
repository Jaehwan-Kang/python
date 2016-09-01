from django.conf.urls import include, url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    # Examples:
    # url(r'^$', 'pystagram.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^photo/(?P<photo_id>\d+)$', 'photo.views.single_photo', name='view_single_photo'),
    url(r'^admin/', include(admin.site.urls)),
]



urlpatterns += static('static_files', document_root=settings.MEDIA_ROOT)