from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('usuarios.urls')),  # Enlaza todas las rutas de la app users
]
