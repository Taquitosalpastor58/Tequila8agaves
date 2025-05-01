# Importaciones necesarias
from django.contrib import admin
from .models import CustomUser, Task, Proveedor, Categoria, Inventario, VentaBarra, PlatilloCocina, PreparacionCocina, LogInventario

# Registrar el modelo CustomUser en el sitio de administración
admin.site.register(CustomUser)

# Registrar el modelo Task en el sitio de administración
admin.site.register(Task)

# Registrar el modelo Proveedor en el sitio de administración
admin.site.register(Proveedor)

# Registrar el modelo Categoria en el sitio de administración
admin.site.register(Categoria)

# Registrar el modelo Inventario en el sitio de administración
admin.site.register(Inventario)

# Registrar el modelo VentaBarra en el sitio de administración
admin.site.register(VentaBarra)

# Registrar el modelo PlatilloCocina en el sitio de administración
admin.site.register(PlatilloCocina)

# Registrar el modelo PreparacionCocina en el sitio de administración
admin.site.register(PreparacionCocina)

# Registrar el modelo LogInventario en el sitio de administración
admin.site.register(LogInventario)
