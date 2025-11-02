from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('ontology_app.urls')),
    path('', include('ontology_app.urls')),
]