from django.db import models

# Create your models here.
class Productos(models.Model):
    nombre = models.CharField(max_length=200)
    descripcion = models.TextField(blank=True)
    cantidad = models.IntegerField()
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    disponibilidad = models.BooleanField(default=True)
    imagen = models.ImageField(upload_to="productos", null=True)
    
    def __str__(self):
        return self.nombre + " - " + "Cantidad: " + str(self.cantidad) + " unidades"

class Compra(models.Model):
    nombre_del_comprador = models.CharField(max_length=100)
    correo = models.EmailField()
    telefono = models.IntegerField()
    productos = models.ManyToManyField(Productos, through='CompraProducto')  # Relación muchos a muchos
    precio_final = models.DecimalField(max_digits=10, decimal_places=2)
    fecha_compra = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Compro: " + self.nombre_del_comprador + ", el día " + str(self.fecha_compra.date())

class CompraProducto(models.Model):
    compra = models.ForeignKey(Compra, on_delete=models.CASCADE)
    producto = models.ForeignKey(Productos, on_delete=models.CASCADE)
    cantidad = models.IntegerField()

    def __str__(self):
        return f"Cliente: {self.compra.nombre_del_comprador} - Producto: {self.producto.nombre} - {self.cantidad} unidades"