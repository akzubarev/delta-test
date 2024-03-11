# from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import path, include

from config.views import swagger

# _project_title = 'Delta Test'
# admin.site.site_header = _project_title
# admin.site.site_title = _project_title
# admin.site.index_title = _project_title

urlpatterns = [
    # swagger
    path('api/swagger/', swagger().with_ui('swagger', cache_timeout=0),
         name='schema-swagger-ui'),
    path('api/redoc/', swagger().with_ui('redoc', cache_timeout=0),
         name='schema-redoc'),
    path('api/v1/', include('apps.parcels.urls')),
    # admin
    # path('', admin.site.urls)
]

urlpatterns = staticfiles_urlpatterns() + urlpatterns
