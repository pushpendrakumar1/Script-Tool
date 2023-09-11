from django.contrib import admin
from django.urls import path, include
from myapp import views
from django.conf import settings
from django.conf.urls.static import static




urlpatterns = [
    # path('admin/', admin.site.urls),
    path("", views.process_view, name='process_view'),  
    path('download/<path:script_path>/', views.download_script, name='download_script'),
    path('replace_variables/', views.replace_variables, name='replace_variables'),
  

]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


