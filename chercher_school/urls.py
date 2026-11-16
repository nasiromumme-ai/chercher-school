from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls')),
    path('documents/', include('documents.urls')),
    path('dashboard/', include('dashboard.urls')),
    path('academics/', include('academics.urls')), # <--- Add this line
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

admin.site.site_header = "Chercher Secondary School — Admin"
admin.site.site_title = "Chercher SS Admin"
admin.site.index_title = "School Management"