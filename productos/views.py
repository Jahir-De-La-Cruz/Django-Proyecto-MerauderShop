from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from .models import Productos, Compra, CompraProducto
from .forms import ProductosForm
from django.contrib import messages
from django.urls import reverse

# Create your views here.
def index(request):
    if request.method == 'GET':
        return render(request, 'index.html', {
            'form' : UserCreationForm
        })
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                usuario = User.objects.create_user(username=request.POST['username'], password=request.POST['password1'])
                usuario.save()
                login(request, usuario)
                return render(request, 'index.html', {
                    'usuario' : usuario,
                    'form' : UserCreationForm
                })
            except IntegrityError:
                return render(request, 'index.html', {
                    'form' : UserCreationForm,
                    'error' : "El usuario ingresado ya existe"
                })
        return render(request, 'index.html', {
            'form' : UserCreationForm,
            'error' : "Las contraseñas no coinciden"
        })

def terminos(request):
        return render(request, 'terminos_y_servicios.html')
        
def nosotros(request):
        return render(request, 'nosotros.html')
        
def iniciar_sesion(request):
    if request.method == 'GET':
        return render(request, 'iniciar_sesion.html', {
            'form' : AuthenticationForm
        })
    else:
        usuario = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if usuario is None:
            return render(request, 'iniciar_sesion.html', {
                'form' : AuthenticationForm,
                'error' : 'Usuario o contraseña incorrectos'
            })
        else:
            login(request, usuario)
            return render(request, 'index.html', {
                'usuario' : usuario
            })
    
@login_required
def cerrar_sesion(request):
    logout(request)
    return redirect('home')

@login_required
def agregar_productos(request):
    if request.method == 'GET':
        return render(request, 'agregar_productos.html', {
            'form' : ProductosForm
        })
    else:
        try:
            form = ProductosForm(request.POST, request.FILES)
            if form.is_valid():
                nuevo_producto = form.save()
                nuevo_producto.save()
                return redirect('tienda')
            else:
                return render(request, 'agregar_productos.html', {
                    'form': form,
                    'error': "Por favor, complete correctamente el formulario."
                })
        except ValueError:
            return render(request, 'agregar_productos.html', {
                'form' : ProductosForm,
                'error' : "Porfavor agregue datos válidos."
            })
    
def Tienda(request):
    productos = Productos.objects.filter(disponibilidad=True)
    return render(request, 'Tienda.html', {
        'productos' : productos
    })
    
@login_required
def editar_productos(request, producto_id):
    if request.method == 'GET':
        producto = get_object_or_404(Productos, pk=producto_id)
        form = ProductosForm(instance=producto)
        return render(request, 'editar_productos.html', {
            'producto' : producto,
            'form' : form
        })
    else:
        try:
            producto = get_object_or_404(Productos, pk=producto_id)
            form = ProductosForm(request.POST, instance=producto)
            form.save()
            return redirect('tienda')
        except ValueError:
            return render(request, 'editar_productos.html', {
                'producto' : producto,
                'form' : form,
                'error' : "Hubo un error al actualizar el producto"
            })
            
@login_required
def eliminar_productos(request, producto_id):
    producto = get_object_or_404(Productos, pk=producto_id)
    if request.method == 'POST':
        producto.delete()
        return redirect('tienda')
    
def comprar_productos(request):
    if request.method == 'POST':
        # Obteniendo los datos del formulario
        nombre_comprador = request.POST.get('nombre_comprador')
        correo = request.POST.get('correo')
        telefono = request.POST.get('telefono')
        productos_nombres = request.POST.get('productos').split(',')  # Convertir a lista
        cantidades = request.POST.get('cantidad_productos').split(',')  # Convertir a lista
        precio_final = request.POST.get('precio_final')

        # Validar si la cantidad de productos y las cantidades coinciden
        if len(productos_nombres) != len(cantidades):
            mensaje = "La cantidad de productos y la cantidad no coinciden."
            return render(request, 'comprar_productos.html', {
                'error': mensaje
            })

        # Crear la compra y guardarla en la base de datos
        nueva_compra = Compra.objects.create(
            nombre_del_comprador=nombre_comprador,
            correo=correo,
            telefono=telefono,
            precio_final=precio_final
        )

        # Procesar los productos comprados
        for nombre, cantidad in zip(productos_nombres, cantidades):
            cantidad = int(cantidad)
            producto = Productos.objects.get(nombre=nombre)
            
            # Verificar si hay suficiente cantidad disponible
            if producto.cantidad >= cantidad:
                # Restar la cantidad comprada del inventario
                producto.cantidad -= cantidad
                producto.save()
            else:
                # Manejar caso de cantidad insuficiente
                mensaje = f"No hay suficiente cantidad disponible para el producto {nombre}"
                return render(request, 'comprar_productos.html', {
                    'error': mensaje
                })

            # Asociar el producto a la compra y guardar en la base de datos
            CompraProducto.objects.create(
                compra=nueva_compra,
                producto=producto,
                cantidad=cantidad
            )

        # Redireccionar a la página de la tienda
        messages.success(request, 'Compra realizada con éxito.')
        return redirect(reverse('tienda') + '?success=true')
    else:
        return render(request, 'comprar_productos.html')
