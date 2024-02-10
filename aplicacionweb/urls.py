"""
URL configuration for aplicacionweb project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from productos import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name="home"),
    path('tienda/', views.Tienda, name="tienda"),
    path('agregar_productos/', views.agregar_productos, name="agregar_productos"),
    path('editar_productos/<int:producto_id>', views.editar_productos, name="editar_productos"),
    path('eliminar_productos/<int:producto_id>', views.eliminar_productos, name="eliminar_productos"),
    path('comprar_productos/', views.comprar_productos, name="compra"),
    path('nosotros/', views.nosotros, name="nosotros"),
    path('iniciar_sesion/', views.iniciar_sesion, name="iniciar_sesion"),
    path('cerrar_sesion/', views.cerrar_sesion, name="cerrar_sesion"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)