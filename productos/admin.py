from django.contrib import admin
from .models import Productos, Compra, CompraProducto

# Register your models here.
admin.site.register(Productos)
admin.site.register(Compra)
admin.site.register(CompraProducto)