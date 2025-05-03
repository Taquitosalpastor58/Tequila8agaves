from django.db import models
from django.contrib.auth.models import AbstractUser, User
from django.conf import settings

# Modelo de usuario personalizado que extiende el modelo de usuario predeterminado de Django
class CustomUser(AbstractUser):
    # Definición de las opciones de roles de usuario
    ROLE_CHOICES = [
        ('cocina', 'Cocina'),
        ('barra1', 'Barra 1'),
        ('barra2', 'Barra 2'),
        ('admin', 'Administrador'),
    ]
    # Campo de rol del usuario con opciones predefinidas
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='cocina')

    # Método para representar el objeto como una cadena
    def __str__(self):
        return f"{self.username} - {self.role}"
    pass

# Modelo de tarea
class Task(models.Model):
    # Título de la tarea
    title = models.CharField(max_length=100)
    # Descripción de la tarea (opcional)
    description = models.TextField(blank=True)
    # Fecha y hora de creación de la tarea (se establece automáticamente al crear)
    created = models.DateTimeField(auto_now_add=True)
    # Fecha y hora de finalización de la tarea (opcional)
    datecompleted = models.DateTimeField(null=True, blank=True)
    # Indicador de si la tarea es importante
    important = models.BooleanField(default=False)
    # Relación de clave foránea con el modelo CustomUser
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

    # Método para representar el objeto como una cadena
    def __str__(self):
        return self.title

# Modelo de 
class Proveedor(models.Model):
    nombre_proveedor = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre_proveedor

# Modelo de Categorías
class Categoria(models.Model):
    nombre_categoria = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre_categoria

# Modelo de Inventario
class Inventario(models.Model):
    UNIDADES_CHOICES = [
        ('pz', 'Pieza'),
        ('g', 'Gramo'),
        ('kg', 'Kilogramo'),
        ('ml', 'Mililitro'),
        ('l', 'Litro'),
    ]

    nombre_producto = models.CharField(max_length=255)
    cantidad = models.DecimalField(max_digits=10, decimal_places=2)
    unidad = models.CharField(max_length=20, choices=UNIDADES_CHOICES)  # Opciones de unidades
    categoria = models.ForeignKey('Categoria', on_delete=models.CASCADE)
    proveedor = models.ForeignKey('Proveedor', on_delete=models.CASCADE)
    limite_stock = models.DecimalField(max_digits=10, decimal_places=2)
    para_barra = models.BooleanField(default=False)
    para_cocina = models.BooleanField(default=False)
   

    def __str__(self):
        return self.nombre_producto

# Modelo de Ventas en Barra
class VentaBarra(models.Model):
    # Relación de clave foránea con el modelo Inventario
    producto = models.ForeignKey(Inventario, on_delete=models.CASCADE)
    # Cantidad vendida del producto
    cantidad_vendida = models.PositiveIntegerField()
    # Fecha y hora de creación del registro de la venta (se establece automáticamente al crear)
    creado_en = models.DateTimeField(auto_now_add=True)
    # Área de la venta
    area = models.CharField(max_length=50, choices=[('barra', 'Barra'), ('cocina', 'Cocina')], default='barra')

    # Método para representar el objeto como una cadena
    def __str__(self):
        return f"{self.producto.nombre_producto} - {self.cantidad_vendida}"

# Modelo de Platillos en Cocina
class PlatilloCocina(models.Model):
    # Nombre del platillo
    nombre_platillo = models.CharField(max_length=100)
    # Ingredientes del platillo
    ingredientes = models.TextField()
    # Fecha y hora de creación del registro del platillo (se establece automáticamente al crear)
    creado_en = models.DateTimeField(auto_now_add=True)

    # Método para representar el objeto como una cadena
    def __str__(self):
        return self.nombre_platillo

# Modelo de Preparaciones en Cocina
class PreparacionCocina(models.Model):
    # Relación de clave foránea con el modelo CustomUser
    usuario = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    # Relación de clave foránea con el modelo PlatilloCocina
    platillo = models.ForeignKey(PlatilloCocina, on_delete=models.CASCADE)
    # Cantidad preparada del platillo
    cantidad_preparada = models.IntegerField()
    # Fecha y hora de creación del registro de la preparación (se establece automáticamente al crear)
    creado_en = models.DateTimeField(auto_now_add=True)

    # Método para representar el objeto como una cadena
    def __str__(self):
        return f"{self.usuario} - {self.platillo} - {self.cantidad_preparada}"

# Modelo de Logs de Inventario
class LogInventario(models.Model):
    # Definición de las acciones de inventario
    ACCIONES = [
        ('ingreso', 'Ingreso'),
        ('descuento', 'Descuento'),
    ]
    # Relación de clave foránea con el modelo Inventario
    inventario = models.ForeignKey(Inventario, on_delete=models.CASCADE)
    # Acción realizada en el inventario
    accion = models.CharField(max_length=10, choices=ACCIONES)
    # Cantidad afectada en el inventario
    cantidad = models.DecimalField(max_digits=10, decimal_places=2)
    # Relación de clave foránea con el modelo CustomUser
    usuario_responsable = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    # Fecha y hora de la acción en el inventario (se establece automáticamente al crear)
    fecha = models.DateTimeField(auto_now_add=True)

    # Método para representar el objeto como una cadena
    def __str__(self):
        return f"{self.inventario} - {self.accion} - {self.cantidad}"

# Modelo de Baja de Inventario
class BajaInventario(models.Model):
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)  # Usuario que realizó la baja
    producto = models.ForeignKey(Inventario, on_delete=models.CASCADE)  # Producto dado de baja
    cantidad = models.PositiveIntegerField()  # Cantidad dada de baja
    creado_en = models.DateTimeField(auto_now_add=True)  # Fecha y hora de la baja
    TIPO_BAJA_CHOICES = [
        ('inicio', 'Inicio de Turno'),
        ('medio', 'Medio Turno'),
        ('final', 'Final de Turno'),
    ]
    tipo_baja = models.CharField(max_length=10, choices=TIPO_BAJA_CHOICES, default='inicio')

    # Método para representar el objeto como una cadena
    def __str__(self):
        return f"{self.usuario.username} - {self.producto.nombre_producto} - {self.cantidad} ({self.tipo_baja})"
