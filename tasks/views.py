# Importaciones necesarias
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from .forms import LoginForm, CustomUserCreationForm, InventarioForm, CategoriaForm, ProveedorForm
from .models import VentaBarra, Inventario, Proveedor
from django.contrib import messages  # Importa la librería de mensajes
from django.db.models import Q, F
from datetime import date
from .models import BajaInventario
from django.contrib.auth import get_user_model
from django.core.paginator import Paginator

# Verifica los productos marcados como para barra
productos_barra = Inventario.objects.filter(para_barra=True)
print("Productos para Barra:")
for producto in productos_barra:
    print(producto.nombre_producto, producto.para_barra, producto.para_cocina)

# Verifica los productos marcados como para cocina
productos_cocina = Inventario.objects.filter(para_cocina=True)
print("Productos para Cocina:")
for producto in productos_cocina:
    print(producto.nombre_producto, producto.para_barra, producto.para_cocina)

# Vista para el inicio de sesión
def login_view(request):
    """
    Vista para manejar el inicio de sesión de los usuarios.
    Si el usuario ya está autenticado, redirige al dashboard.
    Si se envía un formulario POST válido, autentica y redirige al dashboard.
    """
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == "POST":
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            request.session['role'] = user.role
            return redirect('dashboard')
    else:
        form = LoginForm()
    
    return render(request, 'ingresar.html', {'form': form})

# Vista para el registro de usuarios
def signup_view(request):
    """
    Vista para manejar el registro de nuevos usuarios.
    Si se envía un formulario POST válido, crea el usuario y lo autentica.
    """
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            request.session['role'] = user.role
            return redirect('dashboard')
        else:
            return render(request, 'signup.html', {'form': form})
    else:
        form = CustomUserCreationForm()
    
    return render(request, 'signup.html', {'form': form})

# Vista para el dashboard (requiere autenticación)
@login_required
def dashboard(request):
    """
    Vista para mostrar el dashboard según el rol del usuario.
    Redirige a diferentes dashboards basados en el rol del usuario.
    """
    role = request.user.role

    if role == 'admin':
        return redirect('admin_dashboard')
    elif role == 'cocina':
        return redirect('cocina_dashboard')
    elif role == 'barra1':
        return redirect('barra1_dashboard')
    elif role == 'barra2':
        return redirect('barra2_dashboard')

    return redirect('login')  # Si el rol no coincide, redirige al inicio de sesión

# Vista para el cierre de sesión
def logout_view(request):
    """
    Vista para manejar el cierre de sesión de los usuarios.
    Redirige a la página de inicio de sesión después de cerrar sesión.
    """
    # Limpia la sesión completamente
    logout(request)
    request.session.flush()  # Elimina todos los datos de la sesión
    return redirect('login')

# Vista para el dashboard de Barra 1 (requiere autenticación)
@login_required
def barra1_dashboard(request):
    """
    Vista para manejar productos específicos de Barra 1.
    """
    if request.user.role != "barra1":
        messages.error(request, "No tienes permiso para acceder a esta sección.")
        return redirect("login")

    productos = Inventario.objects.filter(para_barra=True, para_cocina=False)

    if request.method == "POST":
        productos_ids = request.POST.getlist("productos")
        for producto_id in productos_ids:
            producto = get_object_or_404(Inventario, id=producto_id)
            cantidad = int(request.POST.get(f"cantidad_{producto_id}", 0))

            if cantidad > 0 and cantidad <= producto.cantidad:
                producto.cantidad -= cantidad
                producto.save()

                # Registrar la baja en el modelo BajaInventario
                BajaInventario.objects.create(
                    usuario=request.user,
                    producto=producto,
                    cantidad=cantidad,
                    tipo_baja="medio"  # Cambiar según el momento del turno
                )

        messages.success(request, "Descuento aplicado correctamente.")
        return redirect("barra1_dashboard")

    return render(request, "barra1_dashboard.html", {"productos": productos})

# Vista para el dashboard del administrador (requiere autenticación)
@login_required
def admin_dashboard(request):
    query = request.GET.get('q', '')  # Término de búsqueda
    productos = Inventario.objects.all().order_by('nombre_producto')
    usuario = request.GET.get('usuario', None)
    fecha = request.GET.get('fecha', None)

    # Filtrar productos por nombre o proveedor si hay un término de búsqueda
    if query:
        productos = productos.filter(
            Q(nombre_producto__icontains=query) | Q(proveedor__nombre_proveedor__icontains=query)
        )

    # Configurar la paginación para productos
    productos_paginator = Paginator(productos, 10)
    productos_page_number = request.GET.get('productos_page')
    productos_paginados = productos_paginator.get_page(productos_page_number)

    # Productos con stock bajo
    productos_bajo_stock = Inventario.objects.filter(cantidad__lte=F('limite_stock')).order_by('nombre_producto')

    # Bajas de inventario
       # Filtrar las bajas de inventario
    bajas_inventario = BajaInventario.objects.all().order_by('-creado_en')
    if usuario:
        bajas_inventario = bajas_inventario.filter(usuario__username=usuario)
    if fecha:
        bajas_inventario = bajas_inventario.filter(creado_en__date=fecha)


    # Usuarios registrados
    usuarios = get_user_model().objects.all().order_by('username')
    usuarios_paginator = Paginator(usuarios, 10)
    usuarios_page_number = request.GET.get('usuarios_page')
    usuarios_paginados = usuarios_paginator.get_page(usuarios_page_number)

    # Formularios
    form = InventarioForm()
    categoria_form = CategoriaForm()
    proveedor_form = ProveedorForm()
    
    # Agregar mensajes de depuración para verificar el flujo de datos
    if request.method == "POST":
        print("Datos recibidos en POST:", request.POST)
        if "categoria_form" in request.POST:
            categoria_form = CategoriaForm(request.POST)
            if categoria_form.is_valid():
                categoria_form.save()
                messages.success(request, "Categoría agregada correctamente.")
            else:
                print("Errores en el formulario de categoría:", categoria_form.errors)
                messages.error(request, "Error al agregar la categoría.")
        elif "proveedor_form" in request.POST:
            proveedor_form = ProveedorForm(request.POST)
            if proveedor_form.is_valid():
                proveedor_form.save()
                messages.success(request, "Proveedor agregado correctamente.")
            else:
                print("Errores en el formulario de proveedor:", proveedor_form.errors)
                messages.error(request, "Error al agregar el proveedor.")
        elif "producto_form" in request.POST:
            form = InventarioForm(request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, "Producto agregado correctamente.")
            else:
                print("Errores en el formulario de producto:", form.errors)
                messages.error(request, "Error al agregar el producto.")

    return render(request, "admin_dashboard.html", {
        "productos": productos_paginados,
        "productos_bajo_stock": productos_bajo_stock,
        "bajas_inventario": bajas_inventario,
        "usuarios": usuarios_paginados,
        "form": form,
        "categoria_form": categoria_form,
        "proveedor_form": proveedor_form,
        "query": query,
        'bajas_inventario': bajas_inventario,
        'usuario_filtrado': usuario,
        'fecha_filtrada': fecha,
        
    })

@login_required
def eliminar_producto(request, producto_id):
    """
    Vista para eliminar un producto del inventario.
    """
    producto = get_object_or_404(Inventario, id=producto_id)
    producto.delete()
    messages.success(request, 'Producto eliminado correctamente.')
    return redirect('admin_dashboard')

@login_required
def actualizar_producto(request, producto_id):
    """
    Vista para actualizar un producto existente en el inventario.
    """
    producto = get_object_or_404(Inventario, id=producto_id)

    if request.method == "POST":
        form = InventarioForm(request.POST, instance=producto)
        if form.is_valid():
            form.save()
            messages.success(request, 'Producto actualizado correctamente.')
            return redirect('admin_dashboard')
        else:
            messages.error(request, 'Error al actualizar el producto. Verifica los datos.')
    else:
        form = InventarioForm(instance=producto)

    return render(request, 'actualizar_producto.html', {'form': form, 'producto': producto})

@login_required
def barra_dashboard(request):
    """
    Vista para mostrar productos específicos de Barra.
    """
    productos = Inventario.objects.filter(para_barra=True, para_cocina=False)
    return render(request, "barra1_dashboard.html", {"productos": productos})

@login_required
def cocina_dashboard(request):
    if request.user.role != "cocina":
        messages.error(request, "No tienes permiso para acceder a esta sección.")
        return redirect("login")

    productos = Inventario.objects.filter(para_cocina=True)

    if request.method == "POST":
        print("Datos recibidos en POST:", request.POST)
        productos_ids = request.POST.getlist("productos")
        for producto_id in productos_ids:
            producto = get_object_or_404(Inventario, id=producto_id)
            cantidad = int(request.POST.get(f"cantidad_{producto_id}", 0))

            print(f"Procesando producto: {producto.nombre_producto}, Cantidad solicitada: {cantidad}, Cantidad disponible: {producto.cantidad}")

            if cantidad > 0 and cantidad <= producto.cantidad:
                producto.cantidad -= cantidad
                producto.save()

                # Registrar la baja en el modelo BajaInventario
                BajaInventario.objects.create(
                    usuario=request.user,
                    producto=producto,
                    cantidad=cantidad,
                    tipo_baja="medio"  # Cambiar según el momento del turno
                )
                print(f"Descuento aplicado: {cantidad} de {producto.nombre_producto}")
            else:
                print(f"Error: Cantidad inválida para {producto.nombre_producto}")

        messages.success(request, "Descuento aplicado correctamente.")
        return redirect("cocina_dashboard")

    return render(request, "cocina_dashboard.html", {"productos": productos})

@login_required
def productos_por_proveedor(request, proveedor_id):
    """
    Vista para mostrar productos asociados a un proveedor específico.
    """
    proveedor = get_object_or_404(Proveedor, id=proveedor_id)
    productos = Inventario.objects.filter(proveedor=proveedor)
    return render(request, "productos_por_proveedor.html", {"productos": productos, "proveedor": proveedor})

@login_required
def ventas_por_area(request, area):
    ventas = VentaBarra.objects.filter(area=area, creado_en__date=date.today())
    return render(request, "ventas_por_area.html", {"ventas": ventas, "area": area})

@login_required
def barra2_dashboard(request):
    """
    Vista para manejar productos específicos de Barra 2.
    """
    if request.user.role != "barra2":
        messages.error(request, "No tienes permiso para acceder a esta sección.")
        return redirect("login")

    productos = Inventario.objects.filter(para_barra=True, para_cocina=False)

    if request.method == "POST":
        productos_ids = request.POST.getlist("productos")
        for producto_id in productos_ids:
            producto = get_object_or_404(Inventario, id=producto_id)
            cantidad = int(request.POST.get(f"cantidad_{producto_id}", 0))

            if cantidad > 0 and cantidad <= producto.cantidad:
                producto.cantidad -= cantidad
                producto.save()

                # Registrar la baja en el modelo BajaInventario
                BajaInventario.objects.create(
                    usuario=request.user,
                    producto=producto,
                    cantidad=cantidad,
                    tipo_baja="medio"  # Cambiar según el momento del turno
                )

        messages.success(request, "Descuento aplicado correctamente.")
        return redirect("barra2_dashboard")

    return render(request, "barra2_dashboard.html", {"productos": productos})

@login_required
def dar_baja_producto(request, producto_id):
    """
    Vista para dar de baja productos desde el inventario.
    """
    producto = get_object_or_404(Inventario, id=producto_id)

    if request.method == "POST":
        cantidad_a_dar_baja = int(request.POST.get("cantidad", 0))

        if cantidad_a_dar_baja > 0 and cantidad_a_dar_baja <= producto.cantidad:
            producto.cantidad -= cantidad_a_dar_baja
            producto.save()

            # Registrar la baja en el modelo BajaInventario
            BajaInventario.objects.create(
                usuario=request.user,
                producto=producto,
                cantidad=cantidad_a_dar_baja
            )

            messages.success(request, f"Se dieron de baja {cantidad_a_dar_baja} {producto.unidad} de {producto.nombre_producto}.")
        else:
            messages.error(request, "Cantidad inválida o insuficiente en el inventario.")

        return redirect("cocina_dashboard")

    return render(request, "dar_baja_producto.html", {"producto": producto})

@login_required
def dar_baja_producto_barra(request, producto_id):
    """
    Vista para dar de baja productos desde el inventario en Barra.
    """
    producto = get_object_or_404(Inventario, id=producto_id)

    if request.method == "POST":
        cantidad_a_dar_baja = int(request.POST.get("cantidad", 0))

        if cantidad_a_dar_baja > 0 and cantidad_a_dar_baja <= producto.cantidad:
            producto.cantidad -= cantidad_a_dar_baja
            producto.save()

            # Registrar la baja en el modelo BajaInventario
            BajaInventario.objects.create(
                usuario=request.user,
                producto=producto,
                cantidad=cantidad_a_dar_baja
            )

            messages.success(request, f"Se dieron de baja {cantidad_a_dar_baja} {producto.unidad} de {producto.nombre_producto}.")
        else:
            messages.error(request, "Cantidad inválida o insuficiente en el inventario.")

        return redirect("barra1_dashboard")  # Cambia a "barra2_dashboard" si es para Barra 2

    return render(request, "dar_baja_producto_barra.html", {"producto": producto})

@login_required
def finalizar_turno(request):
    """
    Vista para registrar productos no utilizados al final del turno y reintegrarlos al inventario.
    Filtra los productos según el área del usuario.
    """
    # Filtrar productos según el área del usuario
    if request.user.role == "cocina":
        productos = Inventario.objects.filter(para_cocina=True)
    elif request.user.role == "barra1":
        productos = Inventario.objects.filter(para_barra=True, para_cocina=False)
    elif request.user.role == "barra2":
        productos = Inventario.objects.filter(para_barra=True, para_cocina=False)
    else:
        messages.error(request, "No tienes permiso para acceder a esta sección.")
        return redirect("dashboard")

    if request.method == "POST":
        print("Datos recibidos en POST:", request.POST)  # Depuración
        productos_ids = request.POST.getlist("productos")

        if not productos_ids:
            messages.error(request, "No se seleccionaron productos para finalizar el turno.")
            return render(request, "finalizar_turno.html", {"productos": productos})

        for producto_id in productos_ids:
            try:
                producto = get_object_or_404(productos, id=producto_id)  # Filtrar solo productos del área
                cantidad_no_utilizada = request.POST.get(f"cantidad_{producto_id}", "")

                if not cantidad_no_utilizada.isdigit() or int(cantidad_no_utilizada) <= 0:
                    messages.error(request, f"Cantidad inválida para el producto {producto.nombre_producto}.")
                    print(f"Cantidad inválida para {producto.nombre_producto}: {cantidad_no_utilizada}")  # Depuración
                    continue

                cantidad_no_utilizada = int(cantidad_no_utilizada)

                print(f"Procesando producto: {producto.nombre_producto}, Cantidad no utilizada: {cantidad_no_utilizada}, Cantidad actual: {producto.cantidad}")  # Depuración

                # Registrar como no utilizado
                BajaInventario.objects.create(
                    usuario=request.user,
                    producto=producto,
                    cantidad=cantidad_no_utilizada,
                    tipo_baja="no_utilizado"
                )

                # Reintegrar la cantidad no utilizada al inventario
                producto.cantidad += cantidad_no_utilizada
                producto.save()

                # Confirmar que el producto se actualizó en la base de datos
                producto_refrescado = Inventario.objects.get(id=producto_id)
                print(f"Cantidad actualizada en la base de datos para {producto_refrescado.nombre_producto}: {producto_refrescado.cantidad}")

                # Agregar alerta visual para confirmar la actualización
                messages.success(request, f"Se reintegraron {cantidad_no_utilizada} unidades de {producto.nombre_producto} al inventario.")
            except Exception as e:
                print(f"Error procesando producto ID {producto_id}: {e}")  # Depuración de errores

        # Refrescar los productos después de la operación
        productos = Inventario.objects.filter(para_cocina=True) if request.user.role == "cocina" else productos
        print("Productos actualizados después de finalizar el turno:", productos)  # Depuración
        return render(request, "finalizar_turno.html", {"productos": productos})

    return render(request, "finalizar_turno.html", {"productos": productos})
